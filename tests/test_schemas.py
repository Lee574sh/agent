import pytest
from pydantic import ValidationError
from artifacts.schemas import (
    PRDBrief, ModuleTree, AcceptancePack, ReviewReport, HandOffSummary
)
from artifacts.schema_validator import validate_artifact_dict, validate_handoff_summary

def test_prdbrief_schema():
    valid_data = {
        "artifact_id": "brief_1",
        "artifact_type": "PRD_Brief",
        "background": ["背景测试"],
        "goals": ["目标测试"]
    }
    brief = PRDBrief.model_validate(valid_data)
    assert brief.artifact_id == "brief_1"

def test_acceptance_pack_validation():
    # 缺少 acceptance_criteria 将引发校验错误
    invalid_data = {
        "artifact_id": "ap_1",
        "artifact_type": "Acceptance_Pack",
        "module_specs": [
            {
                "module_id": "m1",
                "module_name": "模块1",
                "feature_specs": [
                    {
                        "feature_id": "m1_f1",
                        "feature_name": "功能1",
                        "acceptance_criteria": [] # Empty, should fail via validate_acceptance
                    }
                ]
            }
        ]
    }
    with pytest.raises(ValidationError):
        AcceptancePack.model_validate(invalid_data)

def test_schema_validator():
    valid_data = {
        "artifact_id": "brief_1",
        "artifact_type": "PRD_Brief",
        "background": ["背景测试"],
        "goals": ["目标测试"]
    }
    artifact = validate_artifact_dict(valid_data)
    assert artifact.artifact_type == "PRD_Brief"

    with pytest.raises(ValueError, match="Unknown artifact_type"):
        validate_artifact_dict({"artifact_id": "x", "artifact_type": "Fake_Type"})
