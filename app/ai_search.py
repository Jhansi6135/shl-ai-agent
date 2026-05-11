import os
import json
from sentence_transformers import SentenceTransformer, util

# Get project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to catalog.json
DATA_PATH = os.path.join(BASE_DIR, "data", "catalog.json")

# Load dataset
with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# Load AI model (lightweight & fast)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Prepare searchable text corpus
texts = [
    (item.get("name", "") + " " + item.get("description", ""))
    for item in data
]

# Generate embeddings once for performance
embeddings = model.encode(texts, convert_to_tensor=True)


def search(query, top_k=5):
    """
    Search catalog using semantic similarity
    """

    # Convert query into embedding
    query_embedding = model.encode(query, convert_to_tensor=True)

    # Compute cosine similarity
    scores = util.cos_sim(query_embedding, embeddings)[0]

    # Get top matching results
    top_results = scores.argsort(descending=True)[:top_k]

    results = []

    for idx in top_results:
        idx = int(idx)

        results.append({
            "name": data[idx].get("name", ""),
            "description": data[idx].get("description", ""),
            "link": data[idx].get("link", ""),
            "score": round(float(scores[idx]), 4)
        })

    return results


# Test locally
if __name__ == "__main__":
    query = "excel assessment for managers"

    results = search(query)

    print("\nTop Matches:\n")

    for r in results:
        print(f"Name : {r['name']}")
        print(f"Score: {r['score']}")
        print(f"Link : {r['link']}")
        print("-" * 50)