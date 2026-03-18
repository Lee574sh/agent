from typing import List, Dict, Any, Literal, Optional
from pydantic import BaseModel, Field

# -----------------
# 1. 任务包相关 (给 Worker 的入参)
# -----------------
class TaskPacket(BaseModel):
    task_id: str
    worker_type: str
    doc_mode: str
    goal: str
    input_artifact_ids: List[str]
    required_output_type: str
    scenario: Optional[str] = "generic"
    constraints: Dict[str, Any] = Field(default_factory=dict)
    token_budget: int = 4000
    completion_rule: Optional[str] = None

# -----------------
# 2. 计划与步骤相关 (Orchestrator 编排排期用)
# -----------------
class ExecutionStep(BaseModel):
    step_id: str
    worker_type: str
    goal: str
    depends_on: List[str] = Field(default_factory=list)
    input_artifact_types: List[str] = Field(default_factory=list)
    required_output_type: str
    can_skip: bool = False

class ExecutionPlan(BaseModel):
    plan_id: str
    doc_mode: Literal["complex_scenario", "iteration_spec", "mixed"]
    steps: List[ExecutionStep]

# -----------------
# 3. 运行上下文与结果相关 (Orchestrator 结果状态)
# -----------------
class RunResult(BaseModel):
    session_id: str
    doc_mode: str
    plan_id: str
    artifact_ids: List[str] = Field(default_factory=list)
    summary_refs: List[Dict[str, Any]] = Field(default_factory=list)
    open_questions: List[str] = Field(default_factory=list)
    status: Literal["running", "completed", "failed", "paused"]
