from typing import List, Optional, Literal
from pydantic import BaseModel, Field, model_validator


class BaseArtifact(BaseModel):
    artifact_id: str
    artifact_type: str
    artifact_version: str = "1.0"
    source_artifacts: List[str] = Field(default_factory=list)


class HandOffSummary(BaseModel):
    task_goal: str
    key_findings: List[str]
    unresolved_items: List[str] = Field(default_factory=list)
    artifact_ids: List[str]
    next_recommended_action: str


class UserScenarioArtifact(BaseArtifact):
    artifact_type: Literal["User_Scenario"] = "User_Scenario"
    personas: List[str] = Field(default_factory=list)
    scenarios: List[str] = Field(default_factory=list)
    user_pains: List[str] = Field(default_factory=list)
    product_value: List[str] = Field(default_factory=list)
    success_moment: List[str] = Field(default_factory=list)


class PRDBrief(BaseArtifact):
    artifact_type: Literal["PRD_Brief"] = "PRD_Brief"
    project_name: Optional[str] = None
    doc_mode: Optional[Literal["complex_scenario", "iteration_spec", "mixed"]] = None
    background: List[str] = Field(default_factory=list)
    goals: List[str] = Field(default_factory=list)
    users: List[dict] = Field(default_factory=list)
    scope: dict = Field(default_factory=dict)
    constraints: List[str] = Field(default_factory=list)
    open_questions: List[str] = Field(default_factory=list)


class StageItem(BaseModel):
    stage_id: str
    stage_name: str
    entry_conditions: List[str] = Field(default_factory=list)
    exit_conditions: List[str] = Field(default_factory=list)
    actors: List[str] = Field(default_factory=list)
    key_actions: List[str] = Field(default_factory=list)
    hitl_points: List[str] = Field(default_factory=list)
    output_objects: List[str] = Field(default_factory=list)


class StageModel(BaseArtifact):
    artifact_type: Literal["Stage_Model"] = "Stage_Model"
    stages: List[StageItem]

    @model_validator(mode="after")
    def validate_non_empty(self):
        if not self.stages:
            raise ValueError("Stage_Model.stages must not be empty")
        return self


class FeatureNode(BaseModel):
    feature_id: str
    feature_name: str
    is_ai_driven: bool = False
    dependencies: List[str] = Field(default_factory=list)


class ModuleNode(BaseModel):
    module_id: str
    module_name: str
    priority: Optional[str] = None
    user_value: Optional[str] = None
    primary_user_task: Optional[str] = None
    business_goal_alignment: Optional[str] = None
    features: List[FeatureNode] = Field(default_factory=list)


class ModuleTree(BaseArtifact):
    artifact_type: Literal["Module_Tree"] = "Module_Tree"
    modules: List[ModuleNode]

    @model_validator(mode="after")
    def validate_non_empty(self):
        if not self.modules:
            raise ValueError("Module_Tree.modules must not be empty")
        return self


class FeatureDesignItem(BaseModel):
    feature_id: str
    feature_name: str
    feature_goal: str
    user_story: str
    interaction_flow: List[str] = Field(default_factory=list)
    input_data: List[str] = Field(default_factory=list)
    output_data: List[str] = Field(default_factory=list)
    rules: List[str] = Field(default_factory=list)
    edge_cases: List[str] = Field(default_factory=list)
    ui_components: List[str] = Field(default_factory=list)


class ModuleFeatureDesign(BaseModel):
    module_id: str
    module_name: str
    features: List[FeatureDesignItem]


class FeatureDesign(BaseArtifact):
    artifact_type: Literal["Feature_Design"] = "Feature_Design"
    modules: List[ModuleFeatureDesign]

    @model_validator(mode="after")
    def validate_non_empty(self):
        if not self.modules:
            raise ValueError("Feature_Design.modules must not be empty")
        return self


class FeatureSpec(BaseModel):
    feature_id: str
    feature_name: str
    user_value: Optional[str] = None
    user_visible_behavior: List[str] = Field(default_factory=list)
    rules: List[str] = Field(default_factory=list)
    main_flow: List[str] = Field(default_factory=list)
    edge_cases: List[str] = Field(default_factory=list)
    acceptance_criteria: List[str] = Field(default_factory=list)
    nfr: List[str] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)
    open_questions: List[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_acceptance(self):
        if not self.acceptance_criteria:
            raise ValueError(f"{self.feature_id} must include acceptance_criteria")
        return self


class ModuleSpec(BaseModel):
    module_id: str
    module_name: str
    feature_specs: List[FeatureSpec]


class AcceptancePack(BaseArtifact):
    artifact_type: Literal["Acceptance_Pack"] = "Acceptance_Pack"
    module_specs: List[ModuleSpec]

    @model_validator(mode="after")
    def validate_non_empty(self):
        if not self.module_specs:
            raise ValueError("Acceptance_Pack.module_specs must not be empty")
        return self


class ReviewIssue(BaseModel):
    issue_id: str
    severity: Literal["high", "medium", "low"]
    issue_type: str
    location: str
    description: str
    impact: str
    suggestion: str
    related_artifacts: List[str] = Field(default_factory=list)


class ReviewSummary(BaseModel):
    total_issues: int
    high: int = 0
    medium: int = 0
    low: int = 0


class ReviewReport(BaseArtifact):
    artifact_type: Literal["Review_Report"] = "Review_Report"
    review_scope: List[str]
    issues: List[ReviewIssue]
    summary: ReviewSummary

class PRDDocument(BaseArtifact):
    artifact_type: Literal["PRD_Document"] = "PRD_Document"
    title: str
    markdown_content: str


# =====================================================================
# Competitor Analysis Schemas (1 Orchestrator + 6 Skills Workflow)
# =====================================================================

class CompTaskIdentify(BaseArtifact):
    """阶段1: 产出分析任务识别与边界定调"""
    artifact_type: Literal["Comp_Task_Identify"] = "Comp_Task_Identify"
    analysis_goal: Literal["Strategy", "Function", "Experience", "Commercial"]
    analysis_scope: str 
    target_audience: str 
    focus_modules: List[str] = Field(default_factory=list)


class CompetitorNode(BaseModel):
    name: str
    tier: Literal["head", "direct", "substitute", "potential"]
    reason_for_inclusion: str
    priority: Literal["high", "medium", "low"]


class CompList(BaseArtifact):
    """阶段2: 产出目标竞品分层清单"""
    artifact_type: Literal["Comp_List"] = "Comp_List"
    competitors: List[CompetitorNode]
    selection_logic: str


class EvidenceCard(BaseModel):
    """阶段3: 事实归档证据卡片"""
    fact_text: str
    source_url: Optional[str] = None
    source_type: Literal["official_site", "pricing_page", "help_doc", "release_note", "user_feedback", "media", "other"]
    timestamp: Optional[str] = None
    confidence_level: Literal["high", "medium", "low"]


class ProductProfile(BaseArtifact):
    """阶段4: 竞品单体结构化画像"""
    artifact_type: Literal["Product_Profile"] = "Product_Profile"
    competitor_name: str
    positioning: str
    target_users: List[str]
    core_scenarios: List[str]
    key_features: List[str]
    ai_capabilities: dict = Field(default_factory=dict)
    commercial_model: Optional[str] = None
    evidences: List[EvidenceCard] = Field(default_factory=list)


class InsightReport(BaseArtifact):
    """阶段5 & 6: 差异横向对比及洞察归因"""
    artifact_type: Literal["Insight_Report"] = "Insight_Report"
    observation: str
    hypothesized_reason: str
    supporting_evidence: List[str] = Field(default_factory=list)
    confidence_level: Literal["high", "medium", "low"]


class ActionItemCard(BaseModel):
    audience: Literal["PM", "Boss", "R&D", "Sales", "All"]
    action_type: Literal["learn", "avoid", "differentiate", "monitor"]
    suggestion: str
    priority: Literal["high", "medium", "low"]
    risk_prompt: Optional[str] = None


class RecommendationReport(BaseArtifact):
    """阶段7 & 8: 决策建议与面向多角色的输出"""
    artifact_type: Literal["Recommendation_Report"] = "Recommendation_Report"
    recommendations: List[ActionItemCard]
