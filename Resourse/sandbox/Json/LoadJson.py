import json

def readConversation(file_location):
    conversation = []
    with open(file_location, "r") as jsonl_file:
        for line in jsonl_file:
            try:
                message = json.loads(line)
                conversation.append(message)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
    
    return conversation

def printConversation(conversation):
    # Print the conversation
    for message in conversation:
        person = message["person"]
        text = message["message"]
        print(f"{person}: {text}")

# Read the conversation from the JSON Lines file
conversation = readConversation("conversation.jsonl")

# Print the conversation
printConversation(conversation)
