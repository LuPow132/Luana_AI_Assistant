import json

# Initialize an empty list to store the dictionaries
data_list = []

# Replace 'your_file.jsonl' with the actual filename
with open('source/conversation.jsonl', 'r') as file:
    for line in file:
        # Load each line as a JSON object and append it to the list
        data = json.loads(line)
        data_list.append(data['person'] + ":" + data['message'])

# Now, data_list contains a list of dictionaries
for i in range(len(data_list)):
    print(data_list[i])
