from langgraph.graph import StateGraph,END, MessagesState, START, END
from Nodes import llm_calling
from IPython.display import display,Image

Workflow = StateGraph(MessagesState)



Workflow.add_node("LLM", llm_calling)

Workflow.add_edge(START,"LLM")

Workflow.add_edge("LLM",END)

Workflow.set_entry_point("LLM")

Workflow.set_finish_point("LLM")

app = Workflow.compile()

input = {"messages":"Hii"}

print(app.invoke(input).get("messages"))


