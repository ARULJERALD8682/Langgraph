from langgraph.graph import StateGraph, MessagesState, START, END, add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langgraph.prebuilt import ToolNode
from tools import search_flight

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key="AIzaSyB_AYAC6eyvfN_6t-3DAqI-lMHTVCBPrXs")

tools = [search_flight]
tool_node = ToolNode(tools)

llm_with_tool =llm.bind_tools(tools)

def agent_calling(querys:MessagesState):
    query = querys["messages"]
    querys["messages"].append(llm_with_tool.invoke(query))
    # add_messages(llm_with_tool.invoke(query))
    return querys

def router(message:MessagesState):
    state = message["messages"][-1]
    print(state)
    if state.tool_calls:
        print("**********")
        return "tools"
    return END

workflow = StateGraph(MessagesState)

workflow.add_node("agent", agent_calling)
workflow.add_node("flight_search", tool_node)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", router, {"tools": "flight_search", END:END})
workflow.add_edge("flight_search", "agent")

app = workflow.compile()

ai = app.invoke({"messages":["i want to fly chennai to trichy on 2025-03-28"]})
print(ai)

