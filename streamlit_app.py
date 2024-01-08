import streamlit as st
from hugchat import hugchat  # agent for converstaional ai
from hugchat.login import Login
import pandas as pd

# Log in to Hugging Face and obtain cookies
email = "add your hugging chat email here"
passwd = "Add your password here"
sign = Login(email, passwd)
cookies = sign.login()

# Function to load and preprocess the dataset


def load_dataset(file_path):
    data = pd.read_csv(file_path)
    return data

# Function to convert the row of dataset into string


def query_chatbot(chatbot, data, query):
    context = " ".join(data.apply(
        lambda row: " ".join(row.astype(str)), axis=1).tolist())
    full_query = query + context  # combining the context
    query_result = chatbot.query(full_query)
    return query_result

# Streamlit UI


def main():
    st.title("ChatCSV bot")

    # Upload dataset
    uploaded_file = st.file_uploader("Upload CSV Dataset", type=["csv"])

    if uploaded_file is not None:
        data = load_dataset(uploaded_file)  # process the dataset file

        st.subheader("View Uploaded Dataset")
        st.dataframe(data)

        st.subheader("Chatbot Query")
        query = st.text_input("Ask a question to the chatbot:")
        if st.button("Ask"):
            chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
            # initializing the chatbot
            query_result = query_chatbot(chatbot, data, query)
            st.success(f"Chatbot Response: {query_result['text']}")


if __name__ == "__main__":
    main()
