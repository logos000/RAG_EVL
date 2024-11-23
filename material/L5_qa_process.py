import json

# 读取原始JSON数据
with open('L5_questions_answers.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

new_data = []

for item in data:
    new_item = {}
    new_item['question'] = item.get('question', '')
    # 处理答案字段
    answer = item.get('answer', '')
    if isinstance(answer, list):
        new_item['answer'] = answer
    elif isinstance(answer, str):
        # 如果答案中包含逗号，按照逗号拆分，并去除每个元素的首尾空格
        if ',' in answer:
            new_item['answer'] = [ans.strip() for ans in answer.split(',')]
        else:
            new_item['answer'] = [answer.strip()]
    else:
        new_item['answer'] = [str(answer)]


    new_item['Type'] = item.get('details', {}).get('type', '')
    new_item['Source'] = item.get('details', {}).get('source', '')
    new_item['database type'] = item.get('details', {}).get('database type', '')
    new_item['domain'] = item.get('domain', '')
    new_item['URL'] = "https://arxiv.org/"
    new_data.append(new_item)


# 将新数据写入JSON文件
with open('L5_qa_output.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=4)
