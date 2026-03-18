# Workspace Instructions - AI 产品 PRD 协作

本项目主要用于支持 AI 产品经理撰写和迭代 AI 产品 PRD。请在本仓库中优先遵循以下协作约定：

## 角色与默认语言

- 默认把用户视为：从事 AI 相关产品的产品经理/负责人。
- 回答语言：优先使用简体中文，除非用户显式要求使用其他语言。

## AI PRD 工作流优先级

当用户在对话中有以下意图或关键词时，应优先考虑使用 AI PRD 相关的 agents 或工作流 Agent：

- 关键词示例：
  - PRD、产品需求文档、需求文档
  - 需求澄清、业务流程拆解、功能清单、RAG、LLM 能力设计
  - 工程级交付、交互流程、Mermaid 流程图、评估指标、监控、用户手册(Playbook)
- 对应动作：
  - 如果用户需要「从 0 到 1」完成一份 AI 产品 PRD，优先推荐并使用 Agent `ai-prd-workflow`（AI PRD 工作流助手）。
  - 如果用户只需要某一环节（如"帮我生成功能的验收条件"），则可以单独调用对应 Agent（如 `ai-prd-4-acceptance-pack`）。

## 已定义的 PRD 相关 agents

以下 agents 已在 `.github/agents` 下定义，可按需加载：

**流水线型 Workers（由 ai-prd-workflow 或 prd-orchestrator 串联调度）：**
1. ai-prd-0-user-scenario — 用户场景分析（识别用户/任务/痛点/价值，产出 User_Scenario JSON）
2. ai-prd-1-intake — 需求结构化（将散乱输入提炼为 PRD_Brief JSON）
3. ai-prd-2-workflow-breakdown — 业务阶段建模（复杂场景专用，产出 Stage_Model JSON）
4. ai-prd-3-feature-list — 模块功能树生成（用户能力视角，产出 Module_Tree JSON）
5. ai-prd-4-feature-design — 功能详细设计（交互流程/规则/Edge Cases，产出 Feature_Design JSON）
6. ai-prd-4-acceptance-pack — 验收包生成（主流程/异常流/验收标准/NFR，产出 Acceptance_Pack JSON）
7. ai-prd-7-playbook — 多角色协同故事线（Playbook，作为 PRD 合成的输入上下文）
8. ai-prd-5-consistency-check — 全局质量审查（覆盖率/一致性/边界/可测性，产出 Review_Report JSON）
9. ai-prd-6-prd-composer — PRD 最终合成（融合全部工件渲染为可交付 Markdown PRD）

**工作流入口：**
- ai-prd-workflow — 从 0 到 1 的工程级 AI PRD 完整生成工作流（端到端串联上述所有节点）
- prd-orchestrator — 总控调度节点（Task Packet 分发、Session Fact Sheet 维护）

**独立可选工具：**
- ai-prd-6-format-polisher — 对已有 PRD 文档进行术语标准化与排版润色（不属于标准流水线）
- ai-prd-8-user-story（Skill）— 快速生成用户故事 + BDD 验收条件（Given-When-Then 格式）

## 其他约定

- 在涉及业务背景、数据、合规等内容时，不应擅自虚构事实，需通过向用户提问澄清。
- 对于评估指标、监控方案、风险缓解措施等，应给出结构化清单，并明确哪些是建议、哪些需要用户/团队决策确认。
- 如用户未指定工具或流程，可主动建议使用上述工作流，但要保持解释简洁，不打断用户思路。
