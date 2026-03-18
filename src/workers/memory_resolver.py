import yaml
import os
from pathlib import Path
from typing import Dict, Any, List

class MemoryResolver:
    """
    Memory Resolver 负责根据 agent_name 和 scenario 裁剪和组装记忆。
    不直接负责生成 Prompt 字符串，而是返回筛选后的结构化 memory object。
    """
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.index_path = self.workspace_root / "src" / "knowledge" / "memory_index.yaml"
        self.index = self._load_yaml(self.index_path)

    def _load_yaml(self, path: Path) -> Dict[str, Any]:
        if not path.exists():
            return {}
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def _resolve_paths(self, relative_paths: List[str]) -> List[Dict[str, Any]]:
        results = []
        for rel_path in relative_paths:
            full_path = self.workspace_root / rel_path
            content = self._load_yaml(full_path)
            if content:
                content["_source"] = rel_path
                results.append(content)
        return results

    def resolve(self, agent_name: str, scenario: str = "generic") -> Dict[str, Any]:
        """
        根据 agent 和 scenario 从 index 中加载并过滤记忆。
        """
        resolved_memory = {
            "global_rules": [],
            "agent_rules": [],
            "style": {},
            "experience": []
        }

        # 0. Log fallback if it's generic
        if scenario == "generic":
            print("[MEMORY RESOLVER] explicitly running with generic scenario.")

        # 1. Global Rules
        global_rule_paths = self.index.get("rules", {}).get("global", [])
        for rule_file in self._resolve_paths(global_rule_paths):
            for rule in rule_file.get("rules", []):
                if not rule.get("enabled", True):
                    continue
                # Apply Appies To filter
                applies_to = rule.get("applies_to")
                if applies_to is None or agent_name in applies_to:
                    rule_copy = rule.copy()
                    rule_copy["_source"] = rule_file.get("_source")
                    resolved_memory["global_rules"].append(rule_copy)

        # 2. Agent Specific Rules
        agent_rule_paths = self.index.get("rules", {}).get("agent_specific", {}).get(agent_name, [])
        for rule_file in self._resolve_paths(agent_rule_paths):
            for rule in rule_file.get("rules", []):
                if rule.get("enabled", True):
                    rule_copy = rule.copy()
                    rule_copy["_source"] = rule_file.get("_source")
                    resolved_memory["agent_rules"].append(rule_copy)

        # 3. Global Style
        style_paths = self.index.get("style", {}).get("global", [])
        for style_file in self._resolve_paths(style_paths):
            if "style" in style_file:
                # 简单合并字典
                style_content = style_file["style"].copy()
                style_content["_source"] = style_file.get("_source")
                resolved_memory["style"].update(style_content)

        # 4. Scenario Experience
        experience_paths = self.index.get("experience", {}).get(scenario, [])
        if not experience_paths and scenario != "generic":
            print(f"[MEMORY RESOLVER] scenario '{scenario}' not found, falling back to 'generic'.")
            scenario = "generic"
            experience_paths = self.index.get("experience", {}).get("generic", [])

        for exp_file in self._resolve_paths(experience_paths):
            for exp in exp_file.get("patterns", []):
                exp_copy = exp.copy()
                exp_copy["_source"] = exp_file.get("_source")
                resolved_memory["experience"].append(exp_copy)

        return resolved_memory
