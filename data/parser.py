import json

input_path = "data/python_faq_dataset.jsonl"
output_path = "data/python_faq_dataset_enhanced.jsonl"

records = []
with open(input_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
            records.append(rec)
        except Exception as e:
            print("Error parsing line:", line[:100], e)

def make_id(subsource, idx):
    return f"{subsource.lower()}_{idx:04d}"

def make_tags(question, subsource):
    tags = set()
    tags.add(subsource.lower())
    for token in question.replace("`","").replace("?", "").replace(",", "").split():
        token = token.lower()
        if len(token) > 3 and token.isalpha():
            tags.add(token)
    return list(tags)[:5]

enhanced = []
counters = {}
for rec in records:
    sub = rec.get("subsource", "misc")
    counters[sub] = counters.get(sub, 0) + 1
    new = rec.copy()
    new["id"] = make_id(sub, counters[sub])
    new["metadata"] = {"tags": make_tags(rec.get("question",""), sub)}
    enhanced.append(new)

with open(output_path, "w", encoding="utf-8") as f:
    for rec in enhanced:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")

output_path
