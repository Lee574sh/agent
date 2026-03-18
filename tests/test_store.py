import pytest
from artifacts.store import ArtifactStore
from artifacts.schemas import PRDBrief

def test_artifact_store_crud():
    store = ArtifactStore()
    valid_data = {
        "artifact_id": "brief_v1",
        "artifact_type": "PRD_Brief",
        "background": ["测试1"],
        "goals": ["产出1"]
    }
    
    # Test Save
    artifact = store.save_artifact(valid_data)
    assert isinstance(artifact, PRDBrief)
    assert artifact.artifact_id == "brief_v1"
    
    # Test Get
    fetched = store.get_artifact("brief_v1")
    assert fetched == artifact
    
    # Test Find By Type
    all_briefs = store.find_by_type("PRD_Brief")
    assert len(all_briefs) == 1
    
    # Test Latest By Type
    latest = store.latest_by_type("PRD_Brief")
    assert latest.artifact_id == "brief_v1"
    
    # Update to newer version
    valid_data_v2 = {
        "artifact_id": "brief_v2",
        "artifact_type": "PRD_Brief",
        "background": ["测试2"],
        "goals": ["产出2"]
    }
    store.save_artifact(valid_data_v2)
    latest_v2 = store.latest_by_type("PRD_Brief")
    assert latest_v2.artifact_id == "brief_v2"
