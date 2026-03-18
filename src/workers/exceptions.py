class PromptBuildError(Exception):
    """构建提示词时（引包缺失、物理文件损坏等）发生错误"""
    pass

class ModelExecutionError(Exception):
    """网络超时、鉴权失败等 API 物理层错误"""
    pass

class ResponseParseError(Exception):
    """大模型返回了答复，但 JSON 不合法或含有污染文本"""
    pass
