import json

def appendConversation(message, file_location):
    try:
        # Open the file in append mode and create it if it doesn't exist
        with open(file_location, "a") as jsonl_file:
            # Write the JSON object on a new line
            jsonl_file.write(json.dumps(message) + '\n')
    except Exception as e:
        print(f"An error occurred: {str(e)}")

while True:
    A = input("ConversationA: ")
    B = input("ConversationB: ")
    json_formatA = {"person": "A", "message": A}
    appendConversation(json_formatA, "conversation.jsonl")
    json_formatB = {"person": "B", "message": B}
    appendConversation(json_formatB, "conversation.jsonl")
