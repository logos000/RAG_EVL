import json

# 定义关键词
keywords = ["experiment", "material", "txt","study","research","text","mention"]  # 替换为您的关键词

# 加载JSON文件
input_file = "total_biomedi.json"  # 替换为你的输入文件路径
output_file = "final_biomedi.json"  # 替换为你的输出文件路径

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# 过滤数据
filtered_data = []
for entry in data:
    # 获取问题文本
    question_text = entry["question"][0] if isinstance(entry["question"][0], str) else ""
    # 检查是否包含任何关键词
    if not any(keyword in question_text.lower() for keyword in keywords):
        filtered_data.append(entry)

# 保存过滤后的JSON数据
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(filtered_data, f, indent=4, ensure_ascii=False)

print(f"过滤完成！结果已保存到 {output_file}")
