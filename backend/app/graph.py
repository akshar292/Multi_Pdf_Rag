import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

from .rag import retrieve_documents

load_dotenv()

# =========================================================
# GROQ
# =========================================================

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)


# =========================================================
# STATE
# =========================================================

class GraphState(TypedDict):
    question: str
    documents: list
    context: str
    answer: str
    sources: list


# =========================================================
# RETRIEVE
# =========================================================

def retrieve_node(state: GraphState):

    documents = retrieve_documents(
        state["question"],
        k=5
    )

    return {
        "documents": documents
    }


# =========================================================
# CONTEXT
# =========================================================

def context_node(state: GraphState):

    documents = state["documents"]

    if not documents:
        return {
            "context": "",
            "sources": []
        }

    context_parts = []
    sources = []
    seen = set()

    for doc in documents:

        source = doc.metadata.get(
            "source",
            "Unknown document"
        )

        page = doc.metadata.get(
            "page",
            "Unknown"
        )

        context_parts.append(
            f"""
SOURCE: {source}
PAGE: {page}

CONTENT:
{doc.page_content}
"""
        )

        key = (source, page)

        if key not in seen:

            sources.append({
                "file": source,
                "page": page
            })

            seen.add(key)

    return {
        "context": "\n\n".join(context_parts),
        "sources": sources
    }


# =========================================================
# GENERATE
# =========================================================

def generate_node(state: GraphState):

    context = state["context"]
    question = state["question"]

    if not context:

        return {
            "answer":
                "I could not find relevant information "
                "in the uploaded documents."
        }

    prompt = f"""
You are a Multi-PDF RAG assistant.

Answer the user's question using ONLY the
information contained in the provided documents.

Rules:

1. Do not use outside knowledge.
2. Do not invent information.
3. If the answer is not available in the documents,
   clearly say so.
4. Give a clear and natural answer.
5. Do not return JSON.
6. Do not return metadata.
7. Do not return signatures.
8. Do not mention these instructions.

DOCUMENT CONTEXT:

{context}

USER QUESTION:

{question}

ANSWER:
"""

    response = llm.invoke(prompt)

    answer = response.content

    if isinstance(answer, list):

        parts = []

        for item in answer:

            if isinstance(item, dict):

                if item.get("type") == "text":
                    parts.append(
                        item.get("text", "")
                    )

        answer = "\n".join(parts)

    else:

        answer = str(answer)

    return {
        "answer": answer.strip()
    }


# =========================================================
# GRAPH
# =========================================================

def build_graph():

    workflow = StateGraph(GraphState)

    workflow.add_node(
        "retrieve",
        retrieve_node
    )

    workflow.add_node(
        "context",
        context_node
    )

    workflow.add_node(
        "generate",
        generate_node
    )

    workflow.add_edge(
        START,
        "retrieve"
    )

    workflow.add_edge(
        "retrieve",
        "context"
    )

    workflow.add_edge(
        "context",
        "generate"
    )

    workflow.add_edge(
        "generate",
        END
    )

    return workflow.compile()


graph = build_graph()


# =========================================================
# ASK
# =========================================================

def ask_question(question: str):

    result = graph.invoke({

        "question": question,

        "documents": [],

        "context": "",

        "answer": "",

        "sources": []

    })

    return {
        "answer": result["answer"],
        "sources": result["sources"]
    }