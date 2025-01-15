from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder


import os
from langserve import add_routes
from dotenv import load_dotenv
load_dotenv()

store={}

groq_api_key=os.getenv("GROQ_API_KEY")
model=ChatGroq(model="Gemma2-9b-It",groq_api_key=groq_api_key)




# config={"configurable":{"session_id":"chat1"}}

# 1. Create prompt template
system_template = "You are a helpful assistant. Please answer all of the question in marathi:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human","{text}")
    
])


##create chain
chain=prompt_template|model

# with_message_history=RunnableWithMessageHistory(chain, get_session_history, input_messages_key="messages")


## App definition
app=FastAPI(title="Langchain Server",
            version="1.0",
            description="A simple API server using Langchain runnable interfaces")

## Adding chain routes
add_routes(
    app,
    chain,
    path="/chain",
    playground_type = "chat"
)

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)


