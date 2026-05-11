import json
from sentence_transformers import SentenceTransformer, util

# Load dataset
with open("../data/catalog.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Load AI model (lightweight & fast)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Prepare text corpus (name + description)
texts = [
    (item.get("name", "") + " " + item.get("description", ""))
    for item in data
]

# Create embeddings once (important for performance)
embeddings = model.encode(texts, convert_to_tensor=True)

def search(query, top_k=5):
    query_embedding = model.encode(query, convert_to_tensor=True)

    # similarity scores
    scores = util.cos_sim(query_embedding, embeddings)[0]

    # top matches
    top_results = scores.argsort(descending=True)[:top_k]

    results = []
    for idx in top_results:
        results.append({
            "name": data[int(idx)]["name"],
            "link": data[int(idx)]["link"],
            "score": float(scores[idx])
        })

    return results


# test run
if __name__ == "__main__":
    query = "excel assessment for managers"
    results = search(query)

    for r in results:
        print(r["name"], "-", round(r["score"], 3))