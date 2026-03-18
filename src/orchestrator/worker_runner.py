import os
from typing import Optional
from src.orchestrator.types import TaskPacket

class WorkerRunnerBase:
    """
    Runner 基类。
    Phase 7的真正实现应该由其子类 `WorkerExecutor` 继承，它会去读 .github/agents 下的 Prompt并调用大模型。
    下面暴露 `load_domain_knowledge` 用于挂载 Phase 8 的行业静态知识注入。
    """
    def _load_domain_knowledge(self, domain_tag: str) -> str:
        """
        根据指定的业务分类去 src/knowledge/ 抓取相应的场景知识白皮书。
        将其作为系统级约束注入给下游 Worker。
        """
        base_dir = os.path.join(os.path.dirname(__file__), '..', 'knowledge')
        content = []
        
        target_dir = ""
        if domain_tag == "recruiting":
            target_dir = os.path.join(base_dir, "recruiting")
        elif domain_tag == "csr":
            target_dir = os.path.join(base_dir, "csr")
        elif domain_tag == "ai_product":
            target_dir = os.path.join(base_dir, "ai_product")
            
        if not target_dir or not os.path.exists(target_dir):
            return "No specific domain knowledge loaded."

        for filename in os.listdir(target_dir):
            if filename.endswith(".md"):
                with open(os.path.join(target_dir, filename), 'r', encoding='utf-8') as f:
                    content.append(f.read())
                    
        return "\n\n".join(content)

    def run(self, packet: TaskPacket, raw_input: str = "", domain_tag: Optional[str] = None) -> tuple[dict, dict]:
        raise NotImplementedError


class MockWorkerRunner(WorkerRunnerBase):
    """
    一阶 Mock runner。
    """
    def run(self, packet: TaskPacket, raw_input: str = "", domain_tag: Optional[str] = None) -> tuple[dict, dict]:
        # 演示知识注入机制：虽然不开大模型，但我们先准备好上下文
        domain_knowledge = self._load_domain_knowledge(domain_tag) if domain_tag else ""

        # ------------------------------
        #  原 Mock 代码 (节省篇幅已折叠)
        # ------------------------------
        if packet.required_output_type == "User_Scenario":
            artifact = {
                "artifact_id": "scenario_001",
                "artifact_type": "User_Scenario",
                "personas": ["学生", "职场人"],
                "scenarios": ["场景1：整理复习资料", "场景2：查阅工作文档"],
                "user_pains": ["文档太多找不到", "检索不准确"],
                "product_value": ["快速找到关键信息"],
                "success_moment": ["通过一句话问答获得总结好的长文摘要并定位原文"]
            }
            summary = {
                "task_goal": packet.goal,
                "key_findings": ["已成功提取用户场景和痛点"],
                "artifact_ids": ["scenario_001"],
                "next_recommended_action": "基于场景进行PRD问题定义(Brief)"
            }
            return artifact, summary

        if packet.required_output_type == "PRD_Brief":
            artifact = {
                "artifact_id": "brief_001",
                "artifact_type": "PRD_Brief",
                "background": ["测试背景", f"挂载的行业约束长度: {len(domain_knowledge)}"],
                "goals": ["测试目标"]
            }
            summary = {
                "task_goal": packet.goal,
                "key_findings": ["已成功提取需求背景"],
                "artifact_ids": ["brief_001"],
                "next_recommended_action": "进行下一步拆解"
            }
            return artifact, summary

        if packet.required_output_type == "Module_Tree":
            return {"artifact_id": "module_tree_001", "artifact_type": "Module_Tree", "modules": [{"module_id": "m1", "module_name": "Login", "features": []}]}, {"task_goal": packet.goal, "key_findings": [""], "artifact_ids": ["module_tree_001"], "next_recommended_action": ""}
        if packet.required_output_type == "Stage_Model":
            return {"artifact_id": "stage_001", "artifact_type": "Stage_Model", "stages": [{"stage_id": "1", "stage_name": "S"}]}, {"task_goal": packet.goal, "key_findings": [""], "artifact_ids": ["stage_001"], "next_recommended_action": ""}
        if packet.required_output_type == "Feature_Design":
            return {"artifact_id": "feature_design_001", "artifact_type": "Feature_Design", "modules": [{"module_id": "1", "module_name": "N", "features": [{"feature_id": "1", "feature_name": "N", "feature_goal": "Goal", "user_story": "Story", "interaction_flow": [], "input_data": [], "output_data": [], "rules": [], "edge_cases": [], "ui_components": []}]}]}, {"task_goal": packet.goal, "key_findings": [""], "artifact_ids": ["feature_design_001"], "next_recommended_action": ""}
        if packet.required_output_type == "Acceptance_Pack":
            return {"artifact_id": "acceptance_001", "artifact_type": "Acceptance_Pack", "module_specs": [{"module_id": "1", "module_name": "N", "feature_specs": [{"feature_id": "1", "feature_name": "N", "acceptance_criteria": ["X"]}]}]}, {"task_goal": packet.goal, "key_findings": [""], "artifact_ids": ["acceptance_001"], "next_recommended_action": ""}
        if packet.required_output_type == "Review_Report":
            return {"artifact_id": "review_001", "artifact_type": "Review_Report", "review_scope": [], "issues": [], "summary": {"total_issues": 0}}, {"task_goal": packet.goal, "key_findings": [""], "unresolved_items": ["待人工确认是否需要增加流控"], "artifact_ids": ["review_001"], "next_recommended_action": ""}
        if packet.required_output_type == "PRD_Document":
            return {"artifact_id": "doc_001", "artifact_type": "PRD_Document", "title": "Mock PRD", "markdown_content": "# PRD\n...mocked...", "source_artifacts": []}, {"task_goal": packet.goal, "key_findings": [""], "artifact_ids": ["doc_001"], "next_recommended_action": ""}

        raise NotImplementedError(f"Mock not implemented for {packet.required_output_type}")
