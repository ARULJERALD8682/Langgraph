from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from Tools import search_flight
from Output_structure import AgentState, FinalResponse

class structed_output_agent:

    def __init__(self, api_key, model_name):
        llm = ChatGoogleGenerativeAI(api_key=api_key, model= model_name)
        tool = [search_flight]
        self.tool_node = ToolNode(tool)
        self.llm_with_structured_output = llm.with_structured_output(FinalResponse)
        self.llm_with_tool = llm.bind_tools(tool)

    
    def calling_llm(self, user_query: AgentState):
        query = user_query["messages"]
        response = self.llm_with_tool.invoke(query)
        return ({"messages":[response]})
    
    def router(self, messages:AgentState):
        state = messages["messages"][-1]
        if state.tool_calls:
            return "tool"
        else:
            return "final"
        
    def structure(self, message: AgentState):

        state = message["messages"][-1].content
        print(state)
        response = self.llm_with_structured_output.invoke(state)
        print({"final_response":[response]})
        return ({"final_response":[response]})
    
    def __call__(self):

        memory = MemorySaver()
        workflow = StateGraph(AgentState)
        
        workflow.add_node("llm", self.calling_llm)
        workflow.add_node("flight_search", self.tool_node)
        workflow.add_node("response", self.structure)

        workflow.add_edge(START, "llm")
        workflow.add_conditional_edges("llm", self.router, {"tool": "flight_search", "final": "response" })
        workflow.add_edge("flight_search", "llm")
        workflow.add_edge("response", END)

        self.app = workflow.compile(checkpointer=memory)
        return self.app

