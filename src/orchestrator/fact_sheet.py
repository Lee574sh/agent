from typing import List, Dict, Any
from artifacts.schemas import HandOffSummary

class SessionFactSheet:
    def __init__(self, session_id: str):
        self.session_id: str = session_id
        self.doc_mode: str = None
        self.user_goal: str = None
        
        self.completed_tasks: List[str] = []
        self.completed_artifacts: List[str] = []
        self.open_questions: List[str] = []
        
        # 记录所有的 handover 摘要，以备主控查询
        self.last_summaries: List[HandOffSummary] = []
        self.next_recommended_action: str = None
        self.decision_refs: List[str] = []

    def init_session(self, user_goal: str, doc_mode: str):
        self.user_goal = user_goal
        self.doc_mode = doc_mode
        self.completed_tasks.clear()
        self.completed_artifacts.clear()
        self.open_questions.clear()
        self.last_summaries.clear()

    def record_summary(self, worker_type: str, summary: HandOffSummary):
        """
        每次 Worker 执行完毕后，只基于 summary 更新状态，不碰 payload
        """
        self.completed_tasks.append(worker_type)
        
        # 更新最新产出的工件
        for a_id in summary.artifact_ids:
            if a_id not in self.completed_artifacts:
                self.completed_artifacts.append(a_id)
                
        # 追加并去重遗留问题
        for issue in summary.unresolved_items:
            if issue not in self.open_questions:
                self.open_questions.append(issue)
                
        self.next_recommended_action = summary.next_recommended_action
        self.last_summaries.append(summary)

    def snapshot(self) -> Dict[str, Any]:
        """
        截取一份最小状态字典，供大模型 Prompt 或前端页面展示
        """
        return {
            "session_id": self.session_id,
            "doc_mode": self.doc_mode,
            "goal": self.user_goal,
            "completed_artifacts_count": len(self.completed_artifacts),
            "top_open_questions": self.open_questions[:3],  # 只送头部悬而未决的问题
            "latest_action": self.next_recommended_action
        }
