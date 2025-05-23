import json

def convert_to_new_format(old_data):
    new_data = []
    for conversation in old_data:
        utterances = conversation.get("utterances", [])
        # 'speaker'와 바로 다음 'listener' 쌍으로 묶기
        for i in range(len(utterances) - 1):
            curr_uttr = utterances[i]
            next_uttr = utterances[i+1]

            if curr_uttr["role"] == "speaker" and next_uttr["role"] == "listener":
                new_entry = {
                    "messages": [
                        {"role": "user", "content": curr_uttr["text"]},
                        {"role": "assistant", "content": next_uttr["text"]}
                    ]
                }
                new_data.append(new_entry)
    return new_data

# 파일 불러오기
with open('merged_all.json', 'r', encoding='utf-8') as f:
    old_data = json.load(f)

converted_data = convert_to_new_format(old_data)

with open('converted_new.jsonl', 'w', encoding='utf-8') as f:
    for entry in converted_data:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')