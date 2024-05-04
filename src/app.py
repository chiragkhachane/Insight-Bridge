# pip install langchain streamlit langchain-openai python-dotenv

import streamlit as st 
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
#from langchain.agent import create_csv_agent
from langchain_experimental.agents.agent_toolkits.csv.base import create_csv_agent
from langchain_openai import OpenAI
from dotenv import load_dotenv
import os

if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        

    
#define main function
def main():

    load_dotenv()

    openai_api_key = os.getenv("OPENAI_API_KEY")


    if openai_api_key is None:
        raise ValueError("OpenAI API key not found in environment variable OPENAI_API_KEY")

    st.set_page_config(page_title="Insight-Bridge", page_icon="📄")
    st.title("Lets have a chat! 📄")
    st.write("This is your personal AI Data Analyst Assistant. You can ask questions about your CSV file and get answers from the chat.")

    user_csv = st.file_uploader("Upload a CSV file", type="csv")

#conversation:
    for message in st.session_state.chat_history:
        if isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.markdown(message.content)
        else:
            with st.chat_message("AI"):
                st.markdown(message.content)

    

    
    
    if user_csv is not None:

        with st.chat_message("Human"):
            user_question = st.text_input("Ask a question about your CSV: ")

        llm=OpenAI(temperature=0.1)
        agent = create_csv_agent(llm, user_csv, verbose=True)


        if user_question is not None and user_question!= "":
            st.session_state.chat_history.append(HumanMessage(user_question))
            
#            ai_response = st.write_stream(get_response(user_question, st.session_state.chat_history, max_tokens, agent))
            
            with st.spinner(text="In progress..."):
                response = agent.run(user_question) 
            
            with st.chat_message("AI"):
                st.write("Response: ",AIMessage(response), unsafe_allow_html=False)
                st.session_state.chat_history.append(AIMessage(response))    
        
        
    

if __name__ == "__main__":
    main()


