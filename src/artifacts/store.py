from collections import defaultdict
from typing import Dict, List, Optional, Any
from .schema_validator import validate_artifact_dict


class ArtifactStore:
    def __init__(self):
        self._artifacts: Dict[str, Any] = {}
        self._by_type: Dict[str, List[str]] = defaultdict(list)

    def save_artifact(self, artifact_data: dict) -> Any:
        """
        验证并保存 artifact dict。验证失败将抛出 ValueError。
        """
        artifact = validate_artifact_dict(artifact_data)
        artifact_id = artifact.artifact_id

        self._artifacts[artifact_id] = artifact
        if artifact_id not in self._by_type[artifact.artifact_type]:
            self._by_type[artifact.artifact_type].append(artifact_id)

        return artifact

    def get_artifact(self, artifact_id: str) -> Optional[Any]:
        """
        通过明确的 artifact_id 获取工件模型实例
        """
        return self._artifacts.get(artifact_id)

    def find_by_type(self, artifact_type: str) -> List[Any]:
        """
        获取某个类型的全部工件列表
        """
        ids = self._by_type.get(artifact_type, [])
        return [self._artifacts[i] for i in ids]

    def latest_by_type(self, artifact_type: str) -> Optional[Any]:
        """
        返回某个类型最后入库的工件
        """
        ids = self._by_type.get(artifact_type, [])
        if not ids:
            return None
        return self._artifacts[ids[-1]]
