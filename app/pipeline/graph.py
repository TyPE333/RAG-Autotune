from langgraph.graph import Graph, END

def retrieval_node(state: dict) -> dict:
    """Simulates document retrieval."""
    state["Docs"] = ["Dummy Doc1", "Dummy Doc2"]
    return state

def generation_node(state: dict) -> dict:
    """Generates an answer based on retrieved documents."""
    q = state.get("question", "No question provided")  
    docs = ",".join(state.get("Docs", []))  
    
    state["answer"] = f"Answer: {q}"
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
