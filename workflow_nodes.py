from typing import List
from typing_extensions import TypedDict
from langchain.schema import Document
from pprint import pprint

from prompt_templates import (
    retrieval_grader,
    rag_chain,
    hallucination_grader,
    answer_grader,
    question_rewriter,
)

class GraphState(TypedDict):
    question: str
    generation: str
    documents: List[Document]

def retrieve(state, retriever):
    """
    Retrieves relevant documents for the question in the state using the retriever.
    """
    print("---RETRIEVE---")
    question = state["question"]

    # Retrieval (UPDATED from get_relevant_documents)
    documents = retriever.invoke(question)
    return {"documents": documents, "question": question}

def generate(state):
    """
    Generates a response using the RAG chain.
    """
    print("---GENERATE---")
    question = state["question"]
    documents = state["documents"]
    
    # Format documents
    formatted_docs = "\n\n".join(doc.page_content for doc in documents)

    # RAG generation
    generation = rag_chain.invoke({"context": formatted_docs, "question": question})
    return {"documents": documents, "question": question, "generation": generation}

def grade_documents(state):
    """
    Grades the relevance of documents to the question in the state.
    """
    print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
    question = state["question"]
    documents = state["documents"]
    
    # Score each doc
    filtered_docs = []
    for d in documents:
        score = retrieval_grader.invoke({"question": question, "document": d.page_content})
        grade = score.binary_score # Accessing pydantic object attribute directly
        
        if grade.lower() == "yes":
            print("---GRADE: DOCUMENT RELEVANT---")
            filtered_docs.append(d)
        else:
            print("---GRADE: DOCUMENT NOT RELEVANT---")
            continue
    return {"documents": filtered_docs, "question": question}

def transform_query(state):
    """
    Transforms the query to a better version optimized for vector store retrieval.
    """
    print("---TRANSFORM QUERY---")
    question = state["question"]
    documents = state["documents"]

    # Re-write question
    better_question = question_rewriter.invoke({"question": question})
    return {"documents": documents, "question": better_question}

def decide_to_generate(state):
    """
    Decides whether to generate a response or transform the query based on document relevance.
    """
    print("---ASSESS GRADED DOCUMENTS---")
    filtered_documents = state["documents"]

    if not filtered_documents:
        print("---DECISION: ALL DOCUMENTS ARE NOT RELEVANT TO QUESTION, TRANSFORM QUERY---")
        return "transform_query"
    else:
        print("---DECISION: GENERATE---")
        return "generate"

def grade_generation_v_documents_and_question(state):
    """
    Grades the generated response against the documents and the question.
    """
    print("---CHECK HALLUCINATIONS---")
    question = state["question"]
    documents = state["documents"]
    generation = state["generation"]

    # Format documents
    formatted_docs = "\n\n".join(doc.page_content for doc in documents)

    score = hallucination_grader.invoke({"documents": formatted_docs, "generation": generation})
    grade = score.binary_score

    if grade.lower() == "yes":
        print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---")
        # Check if generation addresses the question
        print("---GRADE GENERATION VS QUESTION---")
        score = answer_grader.invoke({"question": question, "generation": generation})
        grade = score.binary_score
        if grade.lower() == "yes":
            print("---DECISION: GENERATION ADDRESSES QUESTION---")
            return "useful"
        else:
            print("---DECISION: GENERATION DOES NOT ADDRESS QUESTION---")
            return "not useful"
    else:
        print("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, RE-TRY---")
        return "not supported"