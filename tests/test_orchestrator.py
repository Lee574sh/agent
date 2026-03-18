import pytest

from orchestrator.router import classify_doc_mode
from orchestrator.planner import Planner

def test_routing_logic():
    complex_input = "在本次招聘场景重构中，需要清晰定义多角色协作、投递节点状态机、阶段退回操作及不同角色的生命周期控制。"
    iter_input = "本期迭代重点优化：添加离线模式缓存、改善会话搜索体验，进行压测评估、修改UI布局。"
    mixed_input = "既要新增离线模式与UI重构，也要把底层的审核流转动作改成多阶段的人工协作状态机。"
    
    assert classify_doc_mode(complex_input) == "complex_scenario"
    assert classify_doc_mode(iter_input) == "iteration_spec"
    assert classify_doc_mode(mixed_input) == "mixed"
    
def test_planner_output_iterations():
    planner = Planner()
    
    # 迭代模式不应该有 Stage Model 步骤
    iter_plan = planner.build_plan("iteration_spec")
    worker_names = [step.worker_type for step in iter_plan.steps]
    assert "Stage_Model_Producer" not in worker_names
    assert len(iter_plan.steps) == 7
    
def test_planner_output_complex():
    planner = Planner()
    
    # 复杂模式下应必须包含 Stage Model 且排在 Brief 之后, Module 之前
    complex_plan = planner.build_plan("complex_scenario")
    worker_names = [step.worker_type for step in complex_plan.steps]
    assert "Stage_Model_Producer" in worker_names
    assert worker_names[2] == "Stage_Model_Producer"
    assert len(complex_plan.steps) == 8
