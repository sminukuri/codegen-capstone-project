
from gettext import translation
from typing import Any
from langgraph.graph import END, START, MessagesState
from langgraph.graph import StateGraph
from code_generator import generate, translate
from code_explanation import explain
from state import AgentState, Task
from router import invoke_router


def generator_node(state: AgentState) -> dict[str, Any]:
    code = generate(state)
    return {
        "generated_code": code
    }

def translation_node(state: AgentState) -> dict[str, Any]:
    code = translate(state)
    return {
        "translated_code": code
    }

def explain_node(state: AgentState) -> dict[str, Any]:
    explanation = explain(state)
    return {
        "explanation": explanation
    }
    
def router_node(state: AgentState) -> dict[str, Any]:
    router_output = invoke_router(state)
    
    return {
        "router": router_output
    }

def supervisor_node(state: AgentState) -> dict[str, Any]:
    return {}

def compiler_node(state: AgentState) -> dict[str, Any]:
    return {}

def repair_node(state: AgentState) -> dict[str, Any]:
    return {}

def supervisor_router(state):

    task = state["router"].task

    if task == Task.TRANSLATE:
        return "translation"

    elif task == Task.GENERATE:
        return "generation"

    elif task == Task.EXPLAIN:
        return "explanation"

    else:
        return "end"
    
def compiler_router(state: AgentState) -> dict[str, Any]:
    return {}
    
builder = StateGraph(AgentState)

builder.add_node("router", router_node)

builder.add_node("supervisor", supervisor_node)

builder.add_node("translation", translation_node)

builder.add_node("generation", generator_node)

builder.add_node("compiler", compiler_node)

builder.add_node("repair", repair_node)

builder.add_node("explanation", explain_node)

builder.set_entry_point("router")

builder.add_edge("router", "supervisor")

builder.add_conditional_edges(
    "supervisor",
    supervisor_router,
    {
        "translation": "translation",
        "generation": "generation",
        "explanation": "explanation",
        "end": END
    }
)

builder.add_edge("generation", "compiler")

builder.add_edge("translation", "compiler")

builder.add_conditional_edges("compiler",
    compiler_router,
    {
        "success": "explanation",
        "repair": "repair"
    }
)

builder.add_edge("repair", "compiler")

builder.add_edge("explanation", END)

graph  = builder.compile()

print(graph.get_graph().draw_mermaid())

png = graph.get_graph().draw_mermaid_png()

with open("graph.png", "wb") as f:
    f.write(png)

# query = "Please write a Python function to calculate the sum of two numbers."
# response = graph.invoke({
#     "messages": [HumanMessage(content=query)],
#     "query": query,
#     "translation": False,
#     "source_language": "",
#     "target_language": "",
#     "source_code": "",
#     "generated_code": "",
#     "explanation": ""
# })

# for message in response["messages"]:
#     print(message.content)

# print("Output Code: \n")    
# print(response["generated_code"])
# print("Explanation: \n")
# print(response["explanation"])

def invoke_graph(state: AgentState) ->AgentState:
    response = graph.invoke(state)
    return response