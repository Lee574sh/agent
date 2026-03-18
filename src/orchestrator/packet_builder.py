from typing import List
import uuid

from src.orchestrator.types import TaskPacket, ExecutionStep
from src.orchestrator.fact_sheet import SessionFactSheet
from src.artifacts.store import ArtifactStore

class MissingArtifactError(Exception):
    pass

def resolve_input_artifacts(step: ExecutionStep, store: ArtifactStore) -> List[str]:
    """
    根据 step 所需的工件类型，从 Store 中反查最新对应的 artifact ID。
    如果必选前置工件不存在，抛出 MissingArtifactError，以防止系统吞报错。
    """
    artifact_ids: List[str] = []

    for artifact_type in step.input_artifact_types:
        latest = store.latest_by_type(artifact_type)
        if latest is None:
            raise MissingArtifactError(
                f"Missing required artifact for step={step.step_id}, "
                f"artifact_type={artifact_type}"
            )
        artifact_ids.append(latest.artifact_id)

    return artifact_ids

def build_task_packet(
    step: ExecutionStep,
    store: ArtifactStore,
    fact_sheet: SessionFactSheet,
    scenario: str = "generic"
) -> TaskPacket:
    """
    将执行阶段的模板动作、当前存活的最新上游工件引用以及总控面板的状态，缝合封装为标准 TaskPacket。
    """
    input_artifact_ids = resolve_input_artifacts(step, store)

    return TaskPacket(
        task_id=f"task_{uuid.uuid4().hex[:8]}",
        worker_type=step.worker_type,
        doc_mode=fact_sheet.doc_mode or "unknown",
        goal=step.goal,
        input_artifact_ids=input_artifact_ids,
        required_output_type=step.required_output_type,
        scenario=scenario,
        constraints={
            "session_open_questions": fact_sheet.open_questions,
        },
        completion_rule=f"Return exactly one {step.required_output_type} artifact and one Hand-off Summary."
    )
