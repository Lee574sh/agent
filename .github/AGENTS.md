# 自定义 Agents 概览

本仓库为 AI 产品 PRD 设计提供了一套自定义工作流 Agent，所有 Agent 遵循 PRD-PROTOCOLS.md 中定义的结构化工件协议，通过 JSON 工件 + Hand-off Summary 在节点之间传递数据。

---

## 完整流水线 — ai-prd-workflow（工程级端到端 PRD 生成）

**用途**：从 0 到 1 生成一份达到研发交付标准的工程级 AI 产品 PRD。

**执行顺序**（与 planner.py 保持一致）：

| 序号 | Agent | 职责 | 产出工件 |
|------|-------|------|---------|
| 0 | ai-prd-0-user-scenario | 用户场景分析：识别目标用户、任务、痛点与产品价值 | User_Scenario |
| 1 | ai-prd-1-intake | 需求结构化：将散乱描述提炼为结构化 PRD Brief | PRD_Brief |
| 2* | ai-prd-2-workflow-breakdown | **复杂场景专用**：业务阶段建模，定义流转与 HITL 节点 | Stage_Model |
| 3 | ai-prd-3-feature-list | 模块功能树：将需求归并为用户能力视角的模块树 | Module_Tree |
| 4 | ai-prd-4-feature-design | 功能详细设计：交互流程、业务规则、Edge Cases、AI 降级 | Feature_Design |
| 5 | ai-prd-4-acceptance-pack | 验收包生成：主/异常流、验收标准、NFR | Acceptance_Pack |
| 6 | ai-prd-7-playbook | 多角色协同故事线：作为文档合成的输入上下文 | Playbook（Markdown） |
| 7 | ai-prd-5-consistency-check | 质量审查：覆盖率、深度、一致性、边界与可测性 | Review_Report |
| 8 | ai-prd-6-prd-composer | 文档合成：融合全部工件渲染最终 Markdown PRD | PRD_Document |

> *步骤 2（ai-prd-2-workflow-breakdown）仅复杂多阶段场景必须，普通迭代型需求可跳过。

---

## 两条执行路径

**路径 A — 复杂场景**（多角色协作 / 多阶段流转 / AI 深度参与）：
> 0 → 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8（共 9 步）

**路径 B — 普通迭代**（模块功能增改 / 版本迭代 / UI 优化）：
> 0 → 1 → 3 → 4 → 5 → 6 → 7 → 8（共 8 步，跳过阶段建模）

---

## 总控节点

**prd-orchestrator**：AI PRD 总控调度。职责：判断场景类型（复杂/迭代/混合）、下发结构化 Task Packet、接收 Hand-off Summary、维护 Session Fact Sheet，并驱动整个工件流转。**不直接撰写任何 PRD 正文**。

---

## 独立可选工具

- **ai-prd-6-format-polisher**：章节润色。对**已有的 PRD 文档**（人工撰写的旧 PRD 或外部导入文档）进行术语标准化、Markdown 排版整理和 Executive Summary 补充，不改变任何业务逻辑。**不属于标准生成流水线**。

- **ai-prd-8-user-story**（Skill）：快速生成单功能点的用户故事（User Story）和 BDD 格式验收条件（Given-When-Then）。适合在已知功能边界的前提下快速补全叙事卡片。

---

## 核心协议

所有 Agent 的结构化工件定义均在 PRD-PROTOCOLS.md 中，包含：
1. Hand-off Summary 交接协议
2. PRD_Brief Schema
3. Stage_Model Schema
4. Module_Tree Schema
5. Acceptance_Pack Schema
6. Review_Report Schema
7. PRD_Document Schema