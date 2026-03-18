def classify_doc_mode(raw_input: str) -> str:
    """
    一个极简的本地静态路由判断。
    真实的生产环境中可以调用一个开销极小的分类模型，但在此作为 Phase 3 的骨架验证足够了。
    返回类型: "complex_scenario" | "iteration_spec" | "mixed"
    """
    complex_keywords = [
        "阶段", "生命周期", "多角色", "协作", "回滚", "场景拆解", "流转", "状态机"
    ]
    iteration_keywords = [
        "版本", "本期迭代", "验收", "模块优化", "压测", "限流", "UI", "离线模式"
    ]
    
    is_complex = any(k in raw_input for k in complex_keywords)
    is_iter = any(k in raw_input for k in iteration_keywords)
    
    if is_complex and is_iter:
        return "mixed"
    elif is_complex:
        return "complex_scenario"
    else:
        # Default or fallback to iteration spec
        return "iteration_spec"
