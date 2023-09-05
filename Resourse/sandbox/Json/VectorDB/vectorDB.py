import json
from hyperdb import HyperDB
from sentence_transformers import SentenceTransformer

# Load documents from the JSONL file

documents = []

with open("demo/pokemon.jsonl", "r") as f:
    for line in f:
        documents.append(json.loads(line))

# Instantiate HyperDB with the list of documents and the key "description"
model = SentenceTransformer('all-MiniLM-L6-v2')
db = HyperDB(documents, key="info.description",
             embedding_function=model.encode)

# Save the HyperDB instance to a file
db.save("demo/pokemon_hyperdb.pickle.gz")

# Load the HyperDB instance from the save file
db.load("demo/pokemon_hyperdb.pickle.gz")

# Query the HyperDB instance with a text input
results = db.query("Absolutely", top_k=5)

for i in range(len(results)):
  print(results[i][0]['message'])