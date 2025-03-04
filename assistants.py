# "This script sets up an AI assistant called 'KinderLogger' using OpenAI's Assistants API. It processes JSON files containing transcriptions of audio feedback and enables users to interact with the assistant to retrieve relevant information."



# Key Functionalities:

# Creates an AI Assistant (KinderLogger) with predefined instructions.
# Processes JSON files (containing transcribed audio feedback) and stores them in a Vector Store for efficient searching.
# Uploads and indexes files into OpenAI’s Vector Store for document retrieval.
# Updates the assistant to utilize the Vector Store for searching within documents when responding to queries.
# Creates a conversation thread to handle user interactions.
# Prompts the user for a query and appends additional context (current date and school week).
# Runs the assistant's response generation loop while polling for completion.
# Displays the assistant's response based on the uploaded documents.


import os
import time
import glob
from openai import OpenAI
from datetime_utils import *

MODEL = "gpt-3.5-turbo-1106"

TODAY = date.today()
START_OF_WEEK, END_OF_WEEK = get_school_week_bounds(date.today())

key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=key)

assistant = client.beta.assistants.create(
    name = "KinderLogger",
    instructions=f"""
    You are an intelligent assistant equipped with a wealth of information contained in various internal files. When addressing user questions, it's essential to rely on this information to formulate your responses. However, it's crucial to present these answers as though they are derived from your own knowledge base, without referencing or hinting at the existence of these files. The user should perceive the assistance you provide as coming directly from your own expertise, without any visible reliance on external sources or annotations. Your role is to seamlessly offer informed responses, creating an impression of innate understanding and proficiency.

    ***IMPORTANT***

    Please review the contents of the uploaded file(s) before answering.
    
    If you don't know an answer, you must respond 'I don't know.'. No other responses will be accepted.
    """,
    tools=[{"type":"file_search"},{"type":"code_interpreter"}],
    model=MODEL
)

pattern = "*.json"
json_files = glob.glob(pattern)


# Create a vector store caled "Audio Feedbacks"
vector_store = client.beta.vector_stores.create(name="Audio Feedbacks")

file_streams = []
for file_path in json_files:
    print(f'Processing file: {file_path}')
    file = open(file_path, 'rb')
    file_streams.append(file)
    
    
# Use the upload and poll SDK helper to upload the files, add them to the vector store,
# and poll the status of the file batch for completion.
file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
vector_store_id=vector_store.id, files=file_streams
)

# You can print the status and the file counts of the batch to see the result of this operation.
print(file_batch.status)
print(file_batch.file_counts)
    

# Update the assistant to use the new Vector Store
assistant = client.beta.assistants.update(
assistant_id=assistant.id,
tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
)
    
    
    

thread = client.beta.threads.create()

def display_main_menu():
    print("\n[KinderLogger Assistant]")
    prompt=input("\nEnter your prompt: ")
    handle_main_menu_option(prompt)

def handle_main_menu_option(prompt):
    client.beta.threads.messages.create(
        thread.id,
        role="user",
        content=prompt
    )
    
    client.beta.threads.messages.create(
        thread.id,
        role="user",
        content=f""" 
        ---------------------
        Today is {TODAY}.
        ---------------------
        The current school week goes from {START_OF_WEEK} and {END_OF_WEEK}.
        ---------------------
        SEARCH IN ALL THE DOCUMENTS.
        """
    )
    
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )
    still_running = True
    while still_running:
        latest_run = client.beta.threads.runs.retrieve(
            thread_id=thread.id, run_id=run.id)
        still_running = latest_run.status != "completed"
        if (still_running):
            time.sleep(2)

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    print(messages.data[0].content)

while True:
    display_main_menu()