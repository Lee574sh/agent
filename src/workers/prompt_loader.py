import os
import json
from typing import Dict, Any, Optional
from src.orchestrator.types import TaskPacket
from .exceptions import PromptBuildError
from .memory_resolver import MemoryResolver

class PromptLoader:
    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root
        self.agents_dir = os.path.join(self.workspace_root, ".github", "agents")
        self.knowledge_dir = os.path.join(self.workspace_root, "src", "knowledge")
        self.protocols_path = os.path.join(self.agents_dir, "PRD-PROTOCOLS.md")
        self.memory_resolver = MemoryResolver(self.workspace_root)

    def _load_agent_instruction(self, worker_type: str) -> str:
        # 简单映射 WorkerType -> 文件名，实际生产可以建个 dict 配置
        mapping = {
            "User_Scenario_Designer": "ai-prd-0-user-scenario.agent.md",
            "Brief_Producer": "ai-prd-1-intake.agent.md",
            "Stage_Model_Producer": "ai-prd-2-workflow-breakdown.agent.md",
            "Module_Tree_Producer": "ai-prd-3-feature-list.agent.md",
            "Feature_Design_Worker": "ai-prd-4-feature-design.agent.md",
            "Acceptance_Pack_Worker": "ai-prd-4-acceptance-pack.agent.md",
            "Review_Worker": "ai-prd-5-review.agent.md",
            "PRD_Composer_Worker": "ai-prd-6-prd-composer.agent.md"
        }
        filename = mapping.get(worker_type)
        if not filename:
            raise PromptBuildError(f"Cannot find agent mapping for {worker_type}")
            
        filepath = os.path.join(self.agents_dir, filename)
        if not os.path.exists(filepath):
            raise PromptBuildError(f"Agent instruction file missing: {filepath}")
            
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()

    def _load_domain_knowledge(self, domain_tag: str) -> str:
        if not domain_tag:
            return ""
        
        target_dir = os.path.join(self.knowledge_dir, domain_tag)
        if not os.path.exists(target_dir):
            return f"[Warning] Domain knowledge folder not found for tag: {domain_tag}"
            
        content = []
        for filename in os.listdir(target_dir):
            if filename.endswith(".md"):
                with open(os.path.join(target_dir, filename), 'r', encoding='utf-8') as f:
                    content.append(f"--- KNOWLEDGE: {filename} ---\n{f.read()}")
        return "\n\n".join(content)
        
    def _load_protocols_schema(self) -> str:
        with open(self.protocols_path, 'r', encoding='utf-8') as f:
            return f.read()

    def build_prompt(self, packet: TaskPacket, raw_input: str, domain_tag: Optional[str] = None, artifacts_payloads: list = None) -> Dict[str, str]:
        """
        拼装输出含有 system, user, schemas 的结构化 payload，供下一步 Executor 消费。
        """
        try:
            instruction = self._load_agent_instruction(packet.worker_type)
            knowledge = self._load_domain_knowledge(domain_tag)
            schemas = self._load_protocols_schema()
            
            # Load memory
            scenario = packet.scenario or domain_tag or "generic"
            resolved_memory = self.memory_resolver.resolve(packet.worker_type, scenario)
            
            # Print Memory Summary Log
            print(f"[MEMORY INJECT] agent={packet.worker_type}, scenario={scenario}"
                  f" -> global_rules={len(resolved_memory.get('global_rules', []))},"
                  f" agent_rules={len(resolved_memory.get('agent_rules', []))},"
                  f" experience_patterns={len(resolved_memory.get('experience', []))},"
                  f" style={1 if resolved_memory.get('style') else 0}")
            
            # Formulate memory block
            memory_block = []
            
            if resolved_memory.get("global_rules"):
                memory_block.append("[GLOBAL RULES]")
                for rule in resolved_memory["global_rules"]:
                    memory_block.append(f"- {rule.get('title', '')}: {rule.get('description', '')}")
            
            if resolved_memory.get("agent_rules"):
                memory_block.append("\n[AGENT-SPECIFIC RULES]")
                for rule in resolved_memory["agent_rules"]:
                    memory_block.append(f"- {rule.get('title', '')}: {rule.get('description', '')}")

            if resolved_memory.get("experience"):
                memory_block.append("\n[SCENARIO EXPERIENCE]")
                for exp in resolved_memory["experience"]:
                    memory_block.append(f"- {exp.get('title', '')}: {exp.get('description', '')}")

            if resolved_memory.get("style"):
                memory_block.append("\n[PRD STYLE]")
                style = resolved_memory["style"]
                memory_block.append(f"Tone: {style.get('tone', '')}")
                memory_block.append(f"Structure: {style.get('structure', '')}")
                memory_block.append(f"Detail Level: {style.get('detail_level', '')}")
                if "avoid" in style:
                    memory_block.append(f"Avoid: {', '.join(style['avoid'])}")

            memory_text = "\n".join(memory_block)

            # --- 构建 System 核心防漂移壁垒 ---
            system_prompt = f"""
{instruction}

[MEMORY INJECTIONS - 写作约束与习惯]
{memory_text}

[DOMAIN KNOWLEDGE - 强制行业规则]
{knowledge}

[SCHEMA PROTOCOLS - 结构化必须遵循此协议]
{schemas}

[CRITICAL INSTRUCTION FOR PARSER]
You must output EXACTLY TWO JSON blocks. No markdown fences like ```json.
No conversational greetings. 
Block 1: You must output the main artifact JSON.
Block 2: Then output a blank line, followed by the Hand-off Summary JSON (not markdown! please convert Summary to JSON block for this API execution).
"""

            user_prompt = f"""
[TASK GOAL]
{packet.goal}

[RAW USER INPUT]
{raw_input}

[UPSTREAM ARTIFACTS CONTENTS]
{json.dumps(artifacts_payloads or [], ensure_ascii=False)}

Please generate the required outputs now:
"""
            return {
                "system_prompt": system_prompt,
                "user_prompt": user_prompt
            }
        except Exception as e:
            raise PromptBuildError(f"Failed to build prompt: {e}")