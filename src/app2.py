import streamlit as st 
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAI
from langchain_experimental.agents.agent_toolkits.csv.base import create_csv_agent
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Define condense_prompt function to handle long prompts
def condense_prompt(prompt):
    if isinstance(prompt, ChatPromptTemplate):
        messages = prompt.to_messages()
        num_tokens = llm.get_num_tokens_from_messages(messages)
        ai_function_messages = messages[2:]
        while num_tokens > 4000:
            ai_function_messages = ai_function_messages[2:]
            num_tokens = llm.get_num_tokens_from_messages(messages[:2] + ai_function_messages)
        messages = messages[:2] + ai_function_messages
        return ChatPromptTemplate(messages=messages)
    else:
        # Handle invalid prompt format
        st.error("Invalid prompt format. Please provide a valid ChatPromptTemplate object.")
        return None


def main():
    load_dotenv()

    # Check for OpenAI API key
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key is None:
        raise ValueError("OpenAI API key not found in environment variable OPENAI_API_KEY")

    # Set up Streamlit page
    st.title("Let's have a chat! 📄")
    st.write("This is a demo of a chatbot using langchain and langchain-openai")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Generate a unique key for the file uploader
    file_uploader_key = "file_uploader_1"

    # Handle file upload
    user_csv = st.file_uploader("Upload a CSV file", type="csv", key=file_uploader_key)
    if user_csv is not None:
        # Initialize OpenAI model and agent
        llm = OpenAI(temperature=0.1)
        agent = create_csv_agent(llm, user_csv, verbose=True)

        # Get user question
        user_question = st.text_input("Ask a question about your CSV: ")

        # Process user question
        if user_question:
            st.session_state.chat_history.append(HumanMessage(user_question))
            response = agent.run(user_question)

            with st.chat_message("AI"):
                st.markdown(AIMessage(response))

            st.session_state.chat_history.append(AIMessage(response))

if __name__ == "__main__":
    main()
