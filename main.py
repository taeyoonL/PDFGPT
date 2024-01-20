from openai import OpenAI
import streamlit as st
import time


client = OpenAI(api_key = "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")


st.title("Chat With Your PDF!!")
st.write('---')
st.write('If you upload your PDF file here, you can talk with PDFGPT about your PDF file content!!')
st.write("Isn't it amazing?? Come and check it out!!")

st.write("")

file = st.file_uploader("Choose Your File!!")
if file is not None:
    File = client.files.create(
        file = open(file.name, "rb"),
        purpose = "assistants"
    )
    assistant = client.beta.assistants.create(
        name = "PDFGPT",
        model = "gpt-3.5-turbo-1106",
        instructions = "You are PDFGPT that provides appropriate responses to user based on the contents of the pdf file that the user posted.",
        tools = [{'type' : 'retrieval'}],
        file_ids = [File.id]
    )
    assistant_id = assistant.id
    st.write('Your PDF file is sucessfully uploaded!!')

st.write("---")
st.write("")
st.write("Chat with PDFGPT based on YOUR file!!")

if 'thread_id' not in st.session_state:
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id

thread_id = st.session_state.thread_id

thread_messages = client.beta.threads.messages.list(
    thread_id = thread_id,
    order = 'asc'
)

for msg in thread_messages.data:
    with st.chat_message(msg.role):
        st.write(msg.content[0].text.value)

question = st.chat_input("If you have any questions about your file, please ask to PDFGPT!!")
if question:

    message = client.beta.threads.messages.create(
        thread_id = thread_id,
        role = "user",
        content = question
    )

    with st.chat_message(message.role):
        st.write(message.content[0].text.value)
    
    run = client.beta.threads.runs.create(
        thread_id = thread_id,
        assistant_id = assistant_id
    )

    with st.spinner("PDFGPT is creating an answer!! Please wait for a second..."):
        while run.status != 'completed':
            time.sleep(0.8)
            print(run.status)
            run = client.beta.threads.runs.retrieve(
                thread_id = thread_id,
                run_id = run.id
            )
    
    message_list = client.beta.threads.messages.list(
        thread_id = thread_id
    )

    with st.chat_message(message_list.data[0].role):
        st.write(message_list.data[0].content[0].text.value)