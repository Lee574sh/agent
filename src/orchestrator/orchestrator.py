from typing import Any, Dict, Optional

from src.orchestrator.router import classify_doc_mode
from src.orchestrator.planner import Planner
from src.orchestrator.packet_builder import build_task_packet
from src.orchestrator.fact_sheet import SessionFactSheet
from src.artifacts.store import ArtifactStore
from src.artifacts.schema_validator import validate_handoff_summary

class Orchestrator:
    """
    极简的 AI PRD 总控中枢。它不直接解析处理自然语言，也不执行具体的撰写任务。
    它仅仅负责：挂载路由器与计划器，把工件包和状态分发给下级 Runner，并汇总结果。
    """
    def __init__(self, worker_runner: Any):
        self.worker_runner = worker_runner
        self.store = ArtifactStore()
        self.planner = Planner()

    def run(self, session_id: str, raw_input: str, domain_tag: Optional[str] = None) -> Dict[str, Any]:
        fact_sheet = SessionFactSheet(session_id=session_id)
        
        # 1. 路由判断与计划生成
        doc_mode = classify_doc_mode(raw_input)
        fact_sheet.init_session(user_goal=raw_input, doc_mode=doc_mode)
        plan = self.planner.build_plan(doc_mode)

        # 2. 依次串联执行工件流水线
        for step in plan.steps:
            # - 获取数据引用并组包
            packet = build_task_packet(
                step=step,
                store=self.store,
                fact_sheet=fact_sheet,
                scenario=domain_tag or "generic"
            )

            # - 投喂给工人 (并将动态领域知识打在运行上下文中)
            artifact_dict, summary_dict = self.worker_runner.run(
                packet=packet, 
                raw_input=raw_input, 
                domain_tag=domain_tag
            )

            # - 工件校验及落盘
            self.store.save_artifact(artifact_dict)
            
            # - 摘要校验，并抽取部分截断更新到大盘账本
            summary = validate_handoff_summary(summary_dict)
            fact_sheet.record_summary(step.worker_type, summary)

        # 3. 最终返回运行快照
        return {
            "session_id": session_id,
            "doc_mode": doc_mode,
            "plan_id": plan.plan_id,
            "artifact_store_digest": {
                k: list(v) for k, v in self.store._by_type.items()
            },
            "fact_sheet": fact_sheet.snapshot(),
            "status": "completed"
        }
