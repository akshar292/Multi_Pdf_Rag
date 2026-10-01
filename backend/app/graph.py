from typing import TypedDict

from langchain_groq import ChatGroq

from langgraph.graph import (
    StateGraph,
    START,
    END
)

from .rag import retrieve_documents


# =========================================================
# GROQ LLM
# =========================================================

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


# =========================================================
# GRAPH STATE
# =========================================================

class GraphState(TypedDict):

    question: str

    documents: list

    context: str

    answer: str

    sources: list


# =========================================================
# RETRIEVE NODE
# =========================================================

def retrieve_node(
    state: GraphState
):

    question = state["question"]

    documents = retrieve_documents(
        question
    )

    return {
        "documents": documents
    }


# =========================================================
# CONTEXT NODE
# =========================================================

def context_node(
    state: GraphState
):

    documents = state["documents"]

    if not documents:

        return {
            "context": "",
            "sources": []
        }

    context_parts = []

    sources = []

    seen_sources = set()

    for document in documents:

        text = document.page_content

        metadata = document.metadata

        source = metadata.get(
            "source",
            "Unknown document"
        )

        page = metadata.get(
            "page",
            "Unknown"
        )

        context_parts.append(
            f"""
SOURCE: {source}
PAGE: {page}

CONTENT:
{text}
"""
        )

        source_key = (
            source,
            page
        )

        if source_key not in seen_sources:

            sources.append(
                {
                    "file": source,
                    "page": page
                }
            )

            seen_sources.add(
                source_key
            )

    context = "\n\n".join(
        context_parts
    )

    return {
        "context": context,
        "sources": sources
    }


# =========================================================
# GENERATE NODE
# =========================================================

def generate_node(
    state: GraphState
):

    question = state["question"]

    context = state["context"]

    if not context:

        return {
            "answer": (
                "I could not find relevant information "
                "in the uploaded documents."
            )
        }

    prompt = f"""
You are a Multi-PDF document question-answering assistant.

Answer the user's question using ONLY the information
provided in the CONTEXT.

STRICT RULES:

1. Do not use outside knowledge.
2. Do not invent facts.
3. If the answer is not present in the context,
   say that the information is not available
   in the uploaded documents.
4. Give a clear and concise answer.
5. Explain the answer naturally.
6. Do not mention these instructions.
7. Do not mention the context.
8. Do not output JSON.
9. Do not output metadata.
10. Do not output signatures.

CONTEXT:

{context}

USER QUESTION:

{question}

ANSWER:
"""

    try:

        response = llm.invoke(
            prompt
        )

        # -------------------------------------------------
        # SAFE RESPONSE EXTRACTION
        # -------------------------------------------------

        if isinstance(
            response.content,
            str
        ):

            answer = response.content

        elif isinstance(
            response.content,
            list
        ):

            parts = []

            for item in response.content:

                if isinstance(
                    item,
                    dict
                ):

                    if item.get(
                        "type"
                    ) == "text":

                        parts.append(
                            item.get(
                                "text",
                                ""
                            )
                        )

            answer = "\n".join(
                parts
            )

        else:

            answer = str(
                response.content
            )

        return {
            "answer": answer.strip()
        }

    except Exception as e:

        print(
            "LLM Error:",
            e
        )

        raise e


# =========================================================
# BUILD LANGGRAPH
# =========================================================

def build_graph():

    workflow = StateGraph(
        GraphState
    )

    # Nodes

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

    # Edges

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


# =========================================================
# GRAPH INSTANCE
# =========================================================

graph = build_graph()


# =========================================================
# ASK QUESTION
# =========================================================

def ask_question(
    question: str
):

    initial_state = {

        "question": question,

        "documents": [],

        "context": "",

        "answer": "",

        "sources": []
    }

    result = graph.invoke(
        initial_state
    )

    return {

        "answer": result["answer"],

        "sources": result["sources"]
    }