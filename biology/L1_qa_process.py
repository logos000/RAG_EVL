import os
import openai
import json
import re
import random
import tqdm

# 初始化 OpenAI 客户端
client = openai.OpenAI(
    api_key="",  # 请将 "YOUR_API_KEY" 替换为您的实际 API 密钥
    base_url='https://api.openai.com/v1'
)

# 定义一个函数来生成选择题
def generate_mcq(question, correct_answer, source_text):
    system_message = (
        "You are a brilliant assistant."
    )
    user_message = (
        "Based on the provided <source_text>, <question>, and <correct_answer>, please generate three plausible but incorrect options for a multiple choice question (MCQ). "
        "Ensure that the correct option can be found in the <source_text>. Do not include any additional explanations or outputs."
        "\n\n"
        "<source_text>: " + source_text +
        "\n<question>: " + question +
        "\n<correct_answer>: " + correct_answer +
        "\n\n"
        "Please output only the three wrong options in JSON format as follows:"
        "{"
        " \"wrong_option_1\": \"First wrong option\","
        " \"wrong_option_2\": \"Second wrong option\","
        " \"wrong_option_3\": \"Third wrong option\""
        "}"
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
        response_format={
            "type": "json_object"
        },
    )

    result = response.choices[0].message.content.strip()

    # 解析生成的 JSON
    try:
        wrong_options_data = json.loads(result)
    except json.JSONDecodeError:
        print("JSON 解析失败，生成的内容可能不符合 JSON 格式。")
        wrong_options_data = None

    if wrong_options_data is None:
        return None, None, None
    else:
        # 提取错误选项
        wrong_options = [
            wrong_options_data.get("wrong_option_1", ""),
            wrong_options_data.get("wrong_option_2", ""),
            wrong_options_data.get("wrong_option_3", "")
        ]

        # 组合所有选项并打乱顺序
        choices_text = [correct_answer] + wrong_options
        random.shuffle(choices_text)
        choices_label = ["A", "B", "C", "D"]

        # 将选项标签和选项文本合并
        options_with_labels = [f"{label}. {text}" for label, text in zip(choices_label, choices_text)]

        # 找到正确答案的索引
        correct_choice_index = choices_text.index(correct_answer)
        correct_choice = choices_label[correct_choice_index]

        return question, options_with_labels, correct_choice

# 读取 JSON 文件中的数据
def read_json_data(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# 保存问题和答案到文件
def save_questions_and_answers(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# 主函数
def main():
    # 输入和输出文件路径
    input_json = 'L1_questions_answers.json'  # 您提供的 JSON 文件路径
    output_json = 'L1_qa_output.json'

    # 读取 JSON 数据
    data = read_json_data(input_json)

    # 存储所有问题和回答的列表
    all_questions_and_answers = []

    # 遍历每个数据项
    for item in tqdm.tqdm(data, desc="Processing QA items"):
        try:
            question = item.get('question', '')
            correct_answer = item.get('answer', '')
            source_text = item.get('source', '')
            domain = item.get('domain', 'Material')
            details = item.get('details', {})
            if "study" in question or "research" in question or "text" in question:
                continue
            # 生成多选题
            # 生成多选题
            mcq_question, options_with_labels, correct_choice = generate_mcq(
                question, correct_answer, source_text
            )

            if mcq_question and options_with_labels and correct_choice:
                # 组织问题和答案的数据结构
                question_and_answer = {
                    "question": [
                        mcq_question,
                        {"options": options_with_labels}
                    ],
                    "answer": correct_choice,
                    "Type": "Retrieve question",
                    "Source": "arXiv",
                    "URL": "https://arxiv.org/",
                    "database type": details.get('database type', ''),
                    "domain": domain
                }

                all_questions_and_answers.append(question_and_answer)
                save_questions_and_answers(output_json, all_questions_and_answers)

            else:
                print(f"Failed to generate MCQ for question: {question}")

        except Exception as e:
            print(f"Error processing item: {e}")

    # 保存所有问题和答案到文件
    save_questions_and_answers(output_json, all_questions_and_answers)
    print("所有数据处理完成。")

if __name__ == "__main__":
    main()
