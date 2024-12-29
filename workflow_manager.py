from langgraph.graph import END, StateGraph

from workflow_nodes import (
    retrieve,
    generate,
    grade_documents,
    transform_query,
    decide_to_generate,
    grade_generation_v_documents_and_question,
    GraphState,
)

def create_workflow(retriever):
    """
    Creates and compiles the workflow using the retriever.

    Args:
        retriever (Retriever): The retriever object.

    Returns:
        StateGraph: The compiled workflow.
    """
    workflow = StateGraph(GraphState)

    # Define the nodes
    workflow.add_node("retrieve", lambda state: retrieve(state, retriever))
    workflow.add_node("grade_documents", grade_documents)
    workflow.add_node("generate", generate)
    workflow.add_node("transform_query", transform_query)

    # Build graph
    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "grade_documents")
    workflow.add_conditional_edges(
        "grade_documents",
        decide_to_generate,
        {
            "transform_query": "transform_query",
            "generate": "generate",
        },
    )
    workflow.add_edge("transform_query", "retrieve")
    workflow.add_conditional_edges(
        "generate",
        grade_generation_v_documents_and_question,
        {
            "not supported": "generate",
            "useful": END,
            "not useful": "transform_query",
        },
    )

    # Compile
    app = workflow.compile()
    return app