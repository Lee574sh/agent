import json
import re
from typing import Tuple, Dict, Any
from .exceptions import ResponseParseError

class ResponseParser:
    def extract_jsons(self, raw_text: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        激进且鲁棒的 JSON 提取器。不管大模型返回了什么聊天废话，
        强制通过正则捞取其中的两个最大的 `{ ... }` 块。
        """
        # 1. 简单清洗一些大模型可能手欠加的 ```json
        cleaned_text = re.sub(r'```(?:json)?', '', raw_input_text).replace('```', '')
        
        # 2. 找到首尾括号（极简嵌套均衡算法寻找 JSON body）
        json_strings = []
        depth = 0
        current_json = ""
        in_json = False
        
        for char in cleaned_text:
            if char == '{':
                if depth == 0:
                    in_json = True
                depth += 1
            
            if in_json:
                current_json += char
                
            if char == '}':
                depth -= 1
                if depth == 0 and in_json:
                    json_strings.append(current_json)
                    current_json = ""
                    in_json = False

        if len(json_strings) < 2:
            raise ResponseParseError(f"Expected 2 JSON objects (Artifact & Summary), but found {len(json_strings)}.")
            
        try:
            artifact_dict = json.loads(json_strings[0])
            summary_dict = json.loads(json_strings[1])
            return artifact_dict, summary_dict
        except json.JSONDecodeError as e:
            raise ResponseParseError(f"JSON Decode Failed: {e}. Raw blocks: {json_strings[:2]}")