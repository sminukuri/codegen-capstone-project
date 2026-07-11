from gettext import translation
from os import stat
from typing import Any
from langgraph.graph import END, START, MessagesState
from langgraph.graph import StateGraph
from code_generator import generate, translate, repair
from code_explanation import explain
from state import AgentState, Language, Task
from router import invoke_router
from compiler_agent import compile_code
from python_validation_agent import  validate_python_code
from java_validation_agent import validate_java_code


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
    if state.router.task != Task.EXPLAIN:
        code = state.generated_code or state.translated_code
    else:
        code = state.router.source_code
    
    if code is None:
        raise ValueError("No code available for explanation.")
     
    explanation = explain(code)
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
    # return {
    #     "compilation_success": True,
    #     "compiler_error": None
    # }
    compilation_success = compile_code(state)

    return {
        "compilation_success": compilation_success,
        "compiler_error": None if compilation_success else "Compilation failed."
    }

def repair_node(state: AgentState) -> dict[str, Any]:
    repair_output = repair(state)
    if state.router.task == Task.TRANSLATE:
        translated_code = repair_output
        return {
            "translated_code": translated_code
        }
    elif state.router.task == Task.GENERATE:
        generated_code = repair_output
        return {
            "generated_code": generated_code
        }
    
    return {}

def validation_node(state: AgentState) -> dict[str, Any]:
    code = state.generated_code or state.translated_code
    if code is None:
        raise ValueError("No code available for validation.")
    target_language = state.router.target_language
    if target_language == Language.JAVA:
        pass_percentage = validate_java_code(state.user_query, code)
    else:
        pass_percentage = validate_python_code(state.user_query, code)
    return {"pass_percentage": pass_percentage}

def supervisor_router(state):

    task = state.router.task

    if task == Task.TRANSLATE:
        return "translation"

    elif task == Task.GENERATE:
        return "generation"

    elif task == Task.EXPLAIN:
        return "explanation"

    else:
        return "end"
    
def compiler_router(state: AgentState) -> str:
    if state.compilation_success is False or state.compiler_error:
        return "repair"
    return "success"
    
builder = StateGraph(AgentState)

builder.add_node("router", router_node)

builder.add_node("supervisor", supervisor_node)

builder.add_node("translation", translation_node)

builder.add_node("generation", generator_node)

builder.add_node("compiler", compiler_node)

builder.add_node("repair", repair_node)

builder.add_node("validation", validation_node)

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
        "success": "validation",
        "repair": "repair"
    }
)

builder.add_edge("repair", "compiler")

builder.add_edge("validation", "explanation")

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