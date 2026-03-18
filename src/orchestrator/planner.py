from .types import ExecutionPlan, ExecutionStep
import uuid

class Planner:
    def build_plan(self, doc_mode: str) -> ExecutionPlan:
        step_scenario = ExecutionStep(
            step_id="step_0",
            worker_type="User_Scenario_Designer",
            goal="识别目标用户、预测用户行为、梳理用户痛点及场景，定义产品价值",
            input_artifact_types=[],
            required_output_type="User_Scenario",
            depends_on=[]
        )

        step_brief = ExecutionStep(
            step_id="step_1",
            worker_type="Brief_Producer",
            goal="提炼需求背景、目标、靶向用户、范围与约束",
            input_artifact_types=["User_Scenario"],
            required_output_type="PRD_Brief",
            depends_on=["step_0"]
        )
        
        step_stage_auth = ExecutionStep(
            step_id="step_2",
            worker_type="Stage_Model_Producer",
            goal="抽象角色与系统的阶段流、关键对象动作与状态边界",
            input_artifact_types=["PRD_Brief"],
            required_output_type="Stage_Model",
            depends_on=["step_1"]
        )
        
        step_module = ExecutionStep(
            step_id="step_3",
            worker_type="Module_Tree_Producer",
            goal="将抽象需求下钻归并为结构化的特征/功能模块树",
            input_artifact_types=["User_Scenario", "PRD_Brief"],
            required_output_type="Module_Tree",
            depends_on=["step_0", "step_1"]
        )

        step_feature_design = ExecutionStep(
            step_id="step_3_5",
            worker_type="Feature_Design_Worker",
            goal="将颗粒度粗的模块下钻为带有业务策略的具体功能点（交互流、规则边界、异常处理等）",
            input_artifact_types=["User_Scenario", "PRD_Brief", "Module_Tree"],
            required_output_type="Feature_Design",
            depends_on=["step_0", "step_3"]
        )

        step_acceptance = ExecutionStep(
            step_id="step_4",
            worker_type="Acceptance_Pack_Worker",
            goal="为模块树内所有功能生成主/异常流、验收条件、边界规则",
            input_artifact_types=["User_Scenario", "PRD_Brief", "Module_Tree", "Feature_Design"],
            required_output_type="Acceptance_Pack",
            depends_on=["step_0", "step_3_5"]
        )

        step_review = ExecutionStep(
            step_id="step_5",
            worker_type="Review_Worker",
            goal="交叉检验上游工件间的一致性、覆盖率缺陷并产出漏项报告",
            input_artifact_types=["PRD_Brief", "Module_Tree", "Feature_Design", "Acceptance_Pack"],
            required_output_type="Review_Report",
            depends_on=["step_4"]
        )

        step_composer = ExecutionStep(
            step_id="step_6",
            worker_type="PRD_Composer_Worker",
            goal="融合全部已生成的上游结构化工件，根据标准 PRD 模板将其格式化、视觉化渲染为一份长篇纯 Markdown 可交付物",
            input_artifact_types=["User_Scenario", "PRD_Brief", "Module_Tree", "Feature_Design", "Acceptance_Pack", "Review_Report"],
            required_output_type="PRD_Document",
            depends_on=["step_0", "step_5"]
        )

        plan = ExecutionPlan(
            plan_id=str(uuid.uuid4()),
            doc_mode=doc_mode,
            steps=[]
        )

        if doc_mode == "iteration_spec":
            plan.steps = [step_scenario, step_brief, step_module, step_feature_design, step_acceptance, step_review, step_composer]
        elif doc_mode == "complex_scenario":
            step_module.input_artifact_types.append("Stage_Model")
            step_module.depends_on.append("step_2")
            step_feature_design.input_artifact_types.append("Stage_Model")
            step_acceptance.input_artifact_types.append("Stage_Model")
            step_review.input_artifact_types.append("Stage_Model")
            step_composer.input_artifact_types.append("Stage_Model")
            
            plan.steps = [step_scenario, step_brief, step_stage_auth, step_module, step_feature_design, step_acceptance, step_review, step_composer]
        elif doc_mode == "mixed":
            step_stage_auth.can_skip = True
            step_module.input_artifact_types.append("Stage_Model")
            step_feature_design.input_artifact_types.append("Stage_Model")
            step_composer.input_artifact_types.append("Stage_Model")
            plan.steps = [step_scenario, step_brief, step_stage_auth, step_module, step_feature_design, step_acceptance, step_review, step_composer]
            
        return plan
