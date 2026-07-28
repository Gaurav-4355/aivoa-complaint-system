from langgraph.graph import StateGraph, END
from app.agents.state import ComplaintState
from app.agents import nodes


def build_complaint_graph():
    graph = StateGraph(ComplaintState)

    graph.add_node("extract_fields", nodes.extract_fields_node)
    graph.add_node("check_completeness", nodes.check_completeness_node)
    graph.add_node("classify_severity", nodes.classify_severity_node)
    graph.add_node("detect_duplicates", nodes.duplicate_detection_node)
    graph.add_node("suggest_root_cause", nodes.root_cause_node)
    graph.add_node("suggest_capa", nodes.capa_node)
    graph.add_node("summarize", nodes.summary_node)
    graph.add_node("classify_risk", nodes.risk_classification_node)

    graph.set_entry_point("extract_fields")
    graph.add_edge("extract_fields", "check_completeness")

    graph.add_conditional_edges(
        "check_completeness",
        nodes.route_after_completeness,
        {"classify_severity": "classify_severity", "extract_fields": "extract_fields"},
    )

    graph.add_edge("classify_severity", "classify_risk")
    graph.add_edge("classify_risk", "detect_duplicates")
    graph.add_edge("detect_duplicates", "suggest_root_cause")
    graph.add_edge("suggest_root_cause", "suggest_capa")
    graph.add_edge("suggest_capa", "summarize")
    graph.add_edge("summarize", END)

    return graph.compile()


complaint_graph = build_complaint_graph()
