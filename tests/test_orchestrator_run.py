import pytest

from src.orchestrator.orchestrator import Orchestrator
from src.orchestrator.worker_runner import MockWorkerRunner
from src.orchestrator.packet_builder import MissingArtifactError

def test_iteration_full_workflow():
    runner = MockWorkerRunner()
    orchestrator = Orchestrator(runner)
    
    raw_input = "本期迭代：我们要增加离线模式并修一些UI。"
    result = orchestrator.run(session_id="S01", raw_input=raw_input, domain_tag="ai_product")
    
    assert result["status"] == "completed"
    assert result["doc_mode"] == "iteration_spec"
    
    # 普通迭代有 4 步 (包含最新加的 Composer 共5步)
    digest = result["artifact_store_digest"]
    assert "PRD_Brief" in digest
    assert "Module_Tree" in digest
    assert "Acceptance_Pack" in digest
    assert "Review_Report" in digest
    assert "PRD_Document" in digest
    
    # 测试静态知识包是否被挂载
    assert "挂载的行业约束长度: 5" not in result["fact_sheet"] # Length should be > 5 for ai_product domain
    
def test_complex_scenario_full_workflow():
    runner = MockWorkerRunner()
    orchestrator = Orchestrator(runner)
    
    raw_input = "重构一个极度烧脑的多阶段生命周期人工审批流系统，需要多角色协作和工单流转节点。"
    result = orchestrator.run(session_id="S02", raw_input=raw_input, domain_tag="recruiting")
    
    assert result["doc_mode"] == "complex_scenario"
    # 复杂流程包含 Stage_Model
    digest = result["artifact_store_digest"]
    assert "Stage_Model" in digest
    
    sheet = result["fact_sheet"]
    # 断言 Sheet 捕获了来自 Review 节点的 open question (来自 mock)
    assert len(sheet["top_open_questions"]) == 1
    assert sheet["top_open_questions"][0] == "待人工确认是否需要增加流控"
