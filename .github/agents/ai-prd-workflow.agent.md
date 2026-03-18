---
name: ai-prd-workflow
label: "AI PRD 工作流 (工程落地版)"
description: "Use when: 需要从0到1写出一份达到研发可直接开发/测试标准的工程级 AI PRD（包含流程图、详细功能需求、边界异常与AI内部逻辑）。全程支持 Human-in-the-Loop 交互深挖。"
mode: workflow
steps:
  - agent: ai-prd-0-user-scenario
  - agent: ai-prd-1-intake
  - agent: ai-prd-2-workflow-breakdown   # 仅复杂多阶段场景必须；简单迭代型可跳过
  - agent: ai-prd-3-feature-list
  - agent: ai-prd-4-feature-design
  - agent: ai-prd-4-acceptance-pack
  - agent: ai-prd-7-playbook             # 在文档合成前完成，输出作为 composer 的输入上下文
  - agent: ai-prd-5-consistency-check
  - agent: ai-prd-6-prd-composer
---

# AI PRD 工作流 Agent (工程落地版)

该 Agent 按固定顺序串联整套工件流水线，产出一份**高标准、面向研发交付的工程级 AI PRD**。所有工件通过结构化 JSON + Hand-off Summary 在各节点之间传递，确保内容完整可追溯。

## 核心强制规则（必读）

**1. 保持 Human in the Loop (HITL)**：
   不允许自我臆想或一次性吐出所有层级文档！在每一步（特别是功能设计阶段），必须**主动提出 2-3 个关键问题**，获取业务细节、异常规则、前后置条件后再输出。

**2. 结构化工件优先**：
   每个 Worker 必须按 PRD-PROTOCOLS.md 中定义的 Schema 输出 JSON 工件 + Hand-off Summary，禁止返回无结构的长篇对话。只要涉及业务流程，必须使用 Mermaid 绘制流程图或时序图。

---

## 工作流四大阶段

### 阶段零：用户场景定调（产出 User_Scenario JSON）
0. ai-prd-0-user-scenario：识别目标用户、任务场景、核心痛点与产品价值锚点。此工件是整个 PRD 的用户视角基础。

### 阶段一：需求结构化与业务建模（产出 PRD_Brief + Stage_Model）
1. ai-prd-1-intake：将散乱描述提炼为 PRD_Brief JSON，明确背景、目标、用户、范围与约束。缺失信息标注为"待澄清"。
2. ai-prd-2-workflow-breakdown：**复杂多阶段场景专用**。将 Brief 转化为 Stage_Model JSON，定义阶段流转、前后置条件与 HITL 节点。**普通迭代型需求可跳过此步**。

### 阶段二：功能拆解与验收条件（产出 Module_Tree + Feature_Design + Acceptance_Pack + Playbook）
3. ai-prd-3-feature-list：将需求归并为用户能力视角的 Module_Tree JSON，标注 P0/P1 优先级与 AI 属性。
4. ai-prd-4-feature-design：下钻每个 Feature，产出带有业务策略的 Feature_Design JSON（交互流程、规则、Edge Cases、AI 降级策略）。
5. ai-prd-4-acceptance-pack：遍历 Feature_Design 中的每个功能点，产出 Acceptance_Pack JSON（主流程/异常流/验收标准/NFR）。
6. ai-prd-7-playbook：编排多角色协同故事线（Playbook），**作为最终文档合成的输入上下文**，确保 PRD 正文体现角色介入时机与系统反馈链路。

### 阶段三：质量审查与最终交付（产出 Review_Report + PRD_Document）
7. ai-prd-5-consistency-check：交叉审查所有工件的覆盖率、功能深度、一致性、边界与可测性，产出 Review_Report JSON。
8. ai-prd-6-prd-composer：融合全部上游工件（Scenario -> Brief -> Stage -> Module -> Feature -> Acceptance -> Playbook -> Review），渲染为最终可交付的长篇 Markdown PRD。

---

## 路径说明

| 场景类型 | 执行路径 |
|--------|----------|
| **复杂场景**（多角色/长流程/状态机） | 全 9 步，含 ai-prd-2-workflow-breakdown |
| **普通迭代**（模块增改/功能优化） | 跳过步骤 2，共 8 步 |