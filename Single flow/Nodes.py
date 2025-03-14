from langchain_google_genai.chat_models import ChatGoogleGenerativeAI

def llm_calling(query:dict):

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key="AIzaSyB_AYAC6eyvfN_6t-3DAqI-lMHTVCBPrXs")

    return {"messages":llm.invoke(query.get("messages"))}
