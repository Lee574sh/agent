# PRD Protocols: 核心工件与交接摘要协议

本协议定义了 AI PRD 系统中所有 Task Worker 与 Orchestrator 协作的标准数据结构。
**任何 Worker 禁止返回非结构化的长篇对话，必须严格遵守以下 Schema 输出。**

---

## 协议 1: Hand-off Summary (交接摘要协议)
**用途**：所有 Worker 在执行完任务后，必须向 Orchestrator 返回此摘要，用于更新 Session Fact Sheet。
**格式**：Markdown结构
```markdown
### 📦 Hand-off Summary
- **当前任务**: [任务名称，如：提炼 PRD Brief]
- **生成工件 ID**: [例如：`Artifact-Brief-v1`]
- **关键结论**:
  1. [结论 1]
  2. [结论 2]
- **未决问题 (Open Issues)**:
  1. [需要 Orchestrator 或用户进一步确认的问题]
```

---

## 协议 2: PRD Brief Schema
**用途**：由 `ai-prd-1-intake` 产出，作为整个 PRD 的统领事实。
**格式**：JSON
```json
{
  "artifact_type": "PRD_Brief",
  "project_name": "项目名称",
  "background": "核心背景说明",
  "goals": ["目标1", "目标2"],
  "target_users": [
    {"role": "角色名称", "pain_points": ["痛点1"], "needs": ["需求1"]}
  ],
  "scope": {
    "in_scope": ["边界内事项"],
    "out_of_scope": ["边界外事项"]
  },
  "constraints": ["合规、性能、时间等约束"]
}
```

---

## 协议 3: Stage Model Schema
**用途**：由 `ai-prd-2-workflow` 产出，用于复杂场景的阶段流转与对象生命周期。
**格式**：JSON
```json
{
  "artifact_type": "Stage_Model",
  "stages": [
    {
      "stage_id": "STG-01",
      "stage_name": "阶段名称",
      "entry_conditions": ["进入条件"],
      "exit_conditions": ["退出/流转条件"],
      "actors": ["参与角色/Agent"],
      "key_actions": ["核心动作"],
      "hitl_points": ["人工干预点/兜底策略"],
      "output_objects": ["产生的中间数据对象"]
    }
  ]
}
```

---

## 协议 4: Module Tree Schema
**用途**：由 `ai-prd-3-feature` 产出，将离散需求结构化为功能树。
**格式**：JSON
```json
{
  "artifact_type": "Module_Tree",
  "modules": [
    {
      "module_id": "MOD-01",
      "module_name": "模块名称",
      "priority": "P0/P1/P2",
      "features": [
        {
          "feature_id": "F-01-01",
          "feature_name": "功能点名称",
          "is_ai_driven": true,
          "dependencies": ["依赖的外部或其他模块"]
        }
      ]
    }
  ]
}
```

---

## 协议 5: Acceptance Pack Schema
**用途**：由 `Acceptance_Pack_Worker` 产出，指导研发与测试的验收包。
**格式**：JSON
```json
{
  "artifact_type": "Acceptance_Pack",
  "artifact_version": "1.0",
  "source_artifacts": [
    "brief_001",
    "module_tree_001",
    "stage_model_001"
  ],
  "module_specs": [
    {
      "module_id": "M1",
      "module_name": "模块名称",
      "feature_specs": [
        {
          "feature_id": "M1-F1",
          "feature_name": "功能点名称",
          "user_value": "用户价值/目标",
          "rules": ["业务规则1", "业务规则2"],
          "main_flow": ["主流程步骤1", "主流程步骤2"],
          "edge_cases": ["异常分支1", "异常分支2"],
          "acceptance_criteria": ["验收标准1", "验收标准2"],
          "nfr": ["非功能要求(性能/安全/限流等)"],
          "risks": ["潜在风险"],
          "open_questions": ["待确认问题"]
        }
      ]
    }
  ]
}
```

---

## 协议 6: Review Report Schema
**用途**：由 `Review_Worker` 产出，结构化的质量缺陷与漏项分析报告。
**格式**：JSON
```json
{
  "artifact_type": "Review_Report",
  "artifact_version": "1.0",
  "review_scope": [
    "brief_001",
    "module_tree_001",
    "acceptance_pack_001"
  ],
  "issues": [
    {
      "issue_id": "R-001",
      "severity": "high/medium/low",
      "issue_type": "missing_acceptance/conflict/nfr_missing等",
      "location": "M1-F1",
      "description": "缺陷描述",
      "impact": "对业务或下游的影响",
      "suggestion": "修改建议",
      "related_artifacts": ["acceptance_pack_001"]
    }
  ],
  "summary": {
    "total_issues": 1,
    "high": 1,
    "medium": 0,
    "low": 0
  }
}
```

---

## 协议 7: PRD Document Schema
**用途**：由 `PRD_Composer_Worker` 产出，是对所有前置 JSON 工件的终极可读化 Markdown 渲染层，也是最终交付物。
**格式**：JSON
```json
{
  "artifact_type": "PRD_Document",
  "artifact_version": "1.0",
  "title": "项目名称或迭代标题",
  "markdown_content": "# PRD 正文\n\n## 1. 背景\n...",
  "source_artifacts": ["brief_001", "stage_001", "module_001", "acceptance_001", "review_001"]
}
```