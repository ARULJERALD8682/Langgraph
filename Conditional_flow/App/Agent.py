from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import MessageGraph, MessagesState
from langgraph.checkpoint.memory import MemorySaver
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
# from langchain.tools import tool
from langgraph.prebuilt import ToolNode
from langchain_community.tools import TavilySearchResults
from Tools import search_flight


class ChatBot:
    def __init__(self, api_key: str, model_name: str):

        self.llm = ChatGoogleGenerativeAI(api_key= api_key, model= model_name)
        tool = [search_flight]
        self.tool_node = ToolNode([search_flight])
        self.llm_with_tool = self.llm.bind_tools(tool)
        
    
        
    def calling_llm(self, query:MessagesState):
        # print(query)
        
        state = query["messages"]
        print(state)
        response = self.llm_with_tool.invoke(state)
        print(response)
        # print(response)
        return {"messages": [response]}
    
    def router_function(self, message: MessagesState):
        state = message["messages"][-1]
        if state.tool_calls:
            return "tools"
        return END
        

    def __call__(self):
        memory = MemorySaver()
        workflow = StateGraph(MessagesState)
        
        
        
        workflow.add_node("llm_call", self.calling_llm)
        workflow.add_node("Search_flight", self.tool_node)

        workflow.add_edge(START, "llm_call")
        workflow.add_conditional_edges("llm_call", self.router_function, {"tools": "Search_flight", END: END})
        workflow.add_edge("Search_flight", "llm_call")

        self.app = workflow.compile(checkpointer=memory)
        print(memory.get({"configurable":{"thread_id":"abc"}}))
        return self.app
    
if __name__ =="__main__":
    app =ChatBot(api_key = "", model_name = "gemini-1.5-flash")

    apps = app()

    while True:
        query = input("Enter query:")
        response = apps.invoke({"messages":[query]}, config={"configurable":{"thread_id":"abc"}})
        print(response)