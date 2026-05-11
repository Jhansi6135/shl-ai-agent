import json

with open("../data/catalog.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(type(data))
print(len(data))

print(data[0])
