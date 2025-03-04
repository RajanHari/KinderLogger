import os
import sys
from openai import OpenAI

# Initialize the OpenAI client
key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=key)

def list_assistants():
    """List all assistants."""
    assistants = client.beta.assistants.list()
    print("Existing Assistants:")
    for assistant in assistants.data:
        print(f"ID: {assistant.id}, Name: {assistant.name}")
    return assistants.data

def delete_assistant(assistant_id):
    """Delete an assistant by ID or delete all assistants."""
    try:
        if assistant_id == "all":
            assistants = client.beta.assistants.list().data
            for assistant in assistants:
                client.beta.assistants.delete(assistant_id=assistant.id)
                print(f"Assistant with ID {assistant.id} has been deleted.")
        else:
            client.beta.assistants.delete(assistant_id=assistant_id)
            print(f"Assistant with ID {assistant_id} has been deleted.")
    except Exception as e:
        print(f"Error deleting assistant: {e}")



def main():
    """Main function to list and delete assistants."""
    if len(sys.argv) < 2:
        print("Usage: python delete_assistant.py <assistant_id>")
        print("Available Assistants:")
        list_assistants()
        return

    assistant_id = sys.argv[1]
    assistants = list_assistants()
    if any(assistant.id == assistant_id for assistant in assistants):
        delete_assistant(assistant_id)
    elif assistant_id == "all":
        print("Deleting all assistants")
        delete_assistant(assistant_id)
    else:
        print(f"No assistant found with ID {assistant_id}.")

if __name__ == "__main__":
    main()
