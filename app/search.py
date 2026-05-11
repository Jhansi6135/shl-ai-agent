import json

with open("../data/catalog.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def simple_search(query):
    results = []

    for item in data:
        text = (item.get("name", "") + " " + item.get("description", "")).lower()

        if query.lower() in text:
            results.append(item)

    return results


# test
query = "excel"
results = simple_search(query)

for r in results[:5]:
    print(r["name"])