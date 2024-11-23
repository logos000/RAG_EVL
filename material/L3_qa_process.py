import json

# 读取原始JSON数据
with open('L3_questions_answers.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

new_data = []

for item in data:
    new_item = {}
    new_item['question'] = item.get('question', '')
    # 处理答案字段
    answer = item.get('answer', '')
    if not ("Yes" in answer or "No" in answer):
        continue
    if "Yes" in answer:
        new_item['answer'] = ["True"]
    else:
        new_item['answer'] = ["False"]

    new_item['Type'] = "Verification Question"
    new_item['Source'] = item.get('details', {}).get('source', '')
    new_item['database type'] = item.get('details', {}).get('database type', '')
    new_item['domain'] = item.get('domain', '')
    new_item['URL'] = "https://arxiv.org/"
    new_data.append(new_item)


# 将新数据写入JSON文件
with open('L3_qa_output.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=4)
