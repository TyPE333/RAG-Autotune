from langgraph.graph import Graph, END
from app.pipeline.retriever.custom_retriever import Retriever
from app.pipeline.generator.local_hf_generator import HuggingFaceGenerator

retriever = Retriever()
generator = HuggingFaceGenerator()

def retrieval_node(state: dict) -> dict:
    """Simulates document retrieval."""
    query = state["question"]
    results = retriever.retrieve(query)
    state["Docs"] = [r["text"] for r in results]
    state["Scores"] = [r["score"] for r in results]
    return state

def generation_node(state: dict) -> dict:
    """Generates an answer based on retrieved documents."""
    q = state.get("question", "No question provided")  
    docs = ",".join(state.get("Docs", []))  
    response = generator.generate(question=q, context_docs=docs)
    state["answer"] = f"Answer: {response}"
    state["citations"] = f"Sources: {docs}"

    return state  

# Setting up LangGraph workflow
g = Graph()
g.add_node("retrieval", retrieval_node)
g.add_node("generation", generation_node)
g.add_edge("retrieval", "generation")
g.add_edge("generation", END)     
g.set_entry_point("retrieval")

pipeline = g.compile()

def run(query: str) -> dict:
    """Executes the LangGraph pipeline."""

    result = pipeline.invoke({"question": query})

    if not result or "answer" not in result or "citations" not in result:
        print("Pipeline returned None or incomplete data. Debugging required.")  
        return {"error": "Pipeline execution failed"}

    return result
