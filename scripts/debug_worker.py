import os
import sys

# 将工程根目录强制加入 sys.path, 方便脚本作为独立命令跑
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.orchestrator.types import TaskPacket
from src.workers.prompt_loader import PromptLoader
import json

def run_debug():
    loader = PromptLoader(workspace_root=project_root)
    
    # 模拟 Orchestrator 的一个底层分发 Task
    packet = TaskPacket(
        task_id="debug_001",
        worker_type="Brief_Producer", 
        doc_mode="iteration_spec",
        goal="提炼需求背景、目标、范围",
        input_artifact_ids=[],
        required_output_type="PRD_Brief"
    )
    
    raw_input = "本次小版本迭代，我们需要给现有的智能招聘系统补充加一个‘离线断网缓存模式’，并且要重构一下首页会话搜索的历史模块。"
    domain_tag = "ai_product" # 注入 AI 产品约束
    
    try:
        # Step 1: Prompt Builder 测试
        print("\n--- 1. Testing Prompt Loader ---")
        prompt_obj = loader.build_prompt(packet, raw_input, domain_tag)
        print("System Prompt Length:", len(prompt_obj["system_prompt"]))
        print("User Prompt Preview:\n", prompt_obj["user_prompt"][:200])
        
        # Step 2: [Mock] 替换为真实的 LLM SDK Call
        print("\n--- 2. [Simulated] Model Call ---")
        print(">> Mocking OpenAI/Gemini call with prompt_obj...")
        mocked_llm_response = """
{
  "artifact_type": "PRD_Brief",
  "project_name": "智能招聘系统-断网缓存与搜索改版",
  "background": ["现有系统在弱网环境下可用性差", "首页会话历史搜索模块体验待重构"],
  "goals": ["提高离线环境下的可用性", "优化历史记录检索体验"],
  "constraints": ["需满足搜索响应 < 2s (Domain注入约束)", "设计考虑降级容灾"]
}

{
  "task_goal": "提炼需求背景、目标、范围",
  "key_findings": ["核心是高可用建设(缓存)与搜索能力优化"],
  "unresolved_items": ["客户端离线缓存的最大容量设定是多少？"],
  "artifact_ids": ["brief_mock_debug"],
  "next_recommended_action": "进行功能清单梳理 (Module Tree)"
}
"""
        
        # Step 3: Response Parser 测试
        print("\n--- 3. Testing Response Parser ---")
        from src.workers.response_parser import ResponseParser
        # Patch local for test
        global raw_input_text
        raw_input_text = mocked_llm_response
        parser = ResponseParser()
        
        artifact, summary = parser.extract_jsons(mocked_llm_response)
        
        print("✓ Successfully parsed Artifact!")
        print(json.dumps(artifact, indent=2, ensure_ascii=False))
        print("\n✓ Successfully parsed Summary!")
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        
        # Step 4: Schema Validator 测试
        print("\n--- 4. Testing Core Validator ---")
        from src.artifacts.schema_validator import validate_artifact_dict, validate_handoff_summary
        
        valid_artifact = validate_artifact_dict(artifact)
        valid_summary = validate_handoff_summary(summary)
        print(f"✓ All validations passed! Final Artifact Type: {valid_artifact.artifact_type}")

    except Exception as e:
        print(f"\n[ERROR] Debug Pipeline broke at Error: {e}")

if __name__ == "__main__":
    run_debug()