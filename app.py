from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typer import prompt
from router import RouterOutput, invoke_router
from typing import Optional
from codegen_agent import invoke_graph
from state import AgentState, RouterInput
import uvicorn

app = FastAPI()

@app.post("/router")
def translate(input: RouterInput) -> AgentState:
    if input.user_query is None:
        raise HTTPException(status_code=400, detail="user_query is required")
    
    state = prepare_state(input.user_query)
        
    return invoke_graph(state)

def prepare_state(user_query: str) -> AgentState:
    """
    Prepare the initial state for the agent based on the user query.

    Args:
        user_query (str): The user's query.
        
    Returns:
        AgentState: The initial state of the agent.
    """    
    return AgentState(user_query=user_query)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")