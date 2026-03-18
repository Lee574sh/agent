from typing import Any, Dict, Type
from pydantic import ValidationError
from .schemas import (
    PRDBrief, StageModel, ModuleTree, FeatureDesign,
    AcceptancePack, ReviewReport, PRDDocument, HandOffSummary,
    UserScenarioArtifact
)

ARTIFACT_REGISTRY: dict[str, Type] = {
    "User_Scenario": UserScenarioArtifact,
    "PRD_Brief": PRDBrief,
    "Stage_Model": StageModel,
    "Module_Tree": ModuleTree,
    "Feature_Design": FeatureDesign,
    "Acceptance_Pack": AcceptancePack,
    "Review_Report": ReviewReport,
    "PRD_Document": PRDDocument,
}

def validate_artifact_dict(data: Dict[str, Any]):
    artifact_type = data.get("artifact_type")
    if not artifact_type:
        raise ValueError("Missing 'artifact_type' in payload")
        
    if artifact_type not in ARTIFACT_REGISTRY:
        raise ValueError(f"Unknown artifact_type: {artifact_type}")

    model_cls = ARTIFACT_REGISTRY[artifact_type]
    try:
        return model_cls.model_validate(data)
    except ValidationError as e:
        raise ValueError(f"Schema validation failed for {artifact_type}: {e}")


def validate_handoff_summary(data: Dict[str, Any]):
    try:
        return HandOffSummary.model_validate(data)
    except ValidationError as e:
        raise ValueError(f"Schema validation failed for HandOffSummary: {e}")
