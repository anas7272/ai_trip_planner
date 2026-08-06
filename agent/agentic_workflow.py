from utils.model_loader import ModelLoader
from promt_library.promt import SYSTEM_PROMPT
from langgraph.graph import StateGraph , MessagesState , END , START
from langgraph.prebuilt import ToolNode , tools_condition

class GraphBuilder():
    def __init__(self):
        self.tools = [

        ]
        self.system_prompt = SYSTEM_PROMPT

    def agentic_workflow(self):
        "main agent fxn"
        user_question = state["messages"]
        input_question = [self.system_prompt] + user_question
        response = self.llm_with_tools.invoke(input_question)
        return {"message" : [response]}

    def build_graph(self):
        graph_builder = StateGraph(MessagesState)
        graph_builder.add_node("agent" , self.agent_function)
        graph_builder.add_node("tools" , ToolsNode(tools = self.tools))
        graph_builder.add_edge(START , "agent")
        graph_builder.add_edge("agent" , "tools" , condition = tools_condition)
        graph_builder.add_edge("tools" , "agent")
        graph_builder.add_edge("agent" , END)
        self.graph = graph_builder.compile()
        return self.graph

    def __call__(self):
        return self.build_graph()
    