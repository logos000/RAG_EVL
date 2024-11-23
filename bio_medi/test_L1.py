import os
import openai
import json
import re
import random
import tqdm

# 初始化OpenAI客户端
client = openai.OpenAI(
    api_key="",
    base_url='https://api.openai.com/v1'
)

# 定义一个函数来提取有用的信息
def extract_useful_information(content):
    system_message = (
        "Analyze the following text to determine if it contains valuable information "
        "such as data, tables, chemical substances, biomedicine compositions, or other important information"
        "excluding information about the author or the article itself."
        "in the field of biomedicines science. Additionally, determine if the answer to a potential retrieval query "
        "can be described in a few concise words. If both conditions are met, return 'True'. "
        "If not, return 'False'. Do not return anything else."
    )
    user_message = f"The text to be analyzed is: '{content}'"
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
    )
    result = response.choices[0].message.content
    return result

# 定义一个函数来生成选择题
def generate_question(content):
    system_message = (
        "You are an expert in information retrieval in the field of biomedicines science. "
        "Based on the provided <text>, identify <target> to be exactly one piece of valuable information "
        "such as data, tables, chemical substances, biomedicine compositions, or other scientific information "
        "excluding information about the author or the article itself. "
        "Ensure that the <target> is concise, highly precise, and directly taken from the text with no modification, rephrasing, or inference. "
        "Then, create a comprehensive, precise, and strongly directive retrieval <query> that starts with 'Retrieve' "
        "and is specifically targeted to the <target>. "
        "The <query> should focus on locating similar key information as provided in <target>, without referencing <text> itself or including unnecessary context. "
        "Do not include the answer or any part of the <target> in your retrieval query. "
        "Ensure that the <query> does not contain the answer. "
        "Extract that exact correct information directly from <target> that answers the <query>. "
        "Ensure that the <answer> can be used for F1 evaluation metric, meaning it should be concise and precise. "
        "Ensure the <answer> only contains a few concise words, without any rephrasing or reorganization. "
        "The goal is to generate a <query> that would lead to retrieving the exact information, ensuring the <answer> is optimal for F1 score calculations. "
        "Structure your response in JSON format as follows:\n"
        "{\n"
        "  \"query\": \"the retrieval query generated that targets the <answer>\",\n"
        "  \"answer\": \"the correct information extracted from <text>\"\n"
        "}\n"
        "Again, DO NOT let your retrieval query rely on the <text>'s context, "
        "and DO NOT show the <text> in your question."
    )
    user_message = f"<text>:\n{content}\nPlease identify the key information and create the retrieval query and provide the anwer as specified."
    

    
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
    result = response.choices[0].message.content
    #return result
    return json.loads(result)

# 定义一个函数来验证答案是否符合要求
# def validate_answer(query, answer):
#     if answer in query:
#         return "False"
#     system_message = (
#         "You are an assistant that checks if the given answer sufficiently and directly answers the given query. "
#         "The query should not reference 'the text' or asking unnecessary context about article or author, or include the answer. "
#         "The answer should be used for F1 evaluation metric, focusing on addressing the core question. "
#         "Please analyze the following query and answer, and determine if the query avoids referencing specific text or unnecessary details, "
#         "and if the answer is directly relevant and appropriately concise. "
#         "Return 'True' if the query and answer meet these standards. If not, return 'False'. "
#         "Do not return anything else."
#     )
#     user_message = f"Query: '{query}'\nAnswer: '{answer}'"
    
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",  # 您可以使用 "gpt-4" 或其他可用的模型
#         messages=[
#             {"role": "system", "content": system_message},
#             {"role": "user", "content": user_message},
#         ],
#     )
#     result = response.choices[0].message.content
#     return result

# 定义一个函数将内容分成若干部分
def split_content(content, max_length=1024):
    paragraphs = content.split('\n\n')
    parts = []
    current_part = ''
    current_length = 0

    for paragraph in paragraphs:
        lines = paragraph.split('\n')
        for line in lines:
            if current_length + len(line) <= max_length:
                current_part += line + '\n'
                current_length += len(line)
            else:
                parts.append(current_part.strip())
                current_part = line + '\n'
                current_length = len(line)
        current_part += '\n'  # 添加段落之间的空行

    if current_part.strip():
        parts.append(current_part.strip())
    
    return parts


# 定义一个函数从txt文件中提取文本
def extract_text_from_txt(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


# 读取文件夹中的所有MMD文件
folder_path = r"E:\AAProgramming\AAmy\RAG_EVL\bio_medi\PMC000xxxxxx"  # 替换为你的文件夹路径

def save_questions_and_answers(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# 存储所有问题和回答的列表
all_questions_and_answers = []

# 遍历文件夹中的每个MMD文件
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path) and filename.lower().endswith('.txt'):  # 确保是txt文件
        
        content = extract_text_from_txt(file_path)
        #print(content)
        parts = split_content(content)
        question_count = 0  # 初始化计数器
        for i, part in tqdm.tqdm(enumerate(parts), desc="Qa process"):
            try:    
                if question_count >= 6:
                    break  # 如果问题数量达到6个，停止生成
                print(f"正在处理文件: {file_path} 的第 {i+1} 部分")
                useful_info = extract_useful_information(part)
                if useful_info.strip() == 'True':
                    print(f"有用的信息提取自文件: {file_path} 的第 {i+1} 部分")
                    #print(part)
                    retrieval_data = generate_question(part)
                    if retrieval_data is not None:
                        query = retrieval_data.get("query", "")
                        answer = retrieval_data.get("answer", "")
                        source = part
                        print(f"生成的检索问题: {query}\n")
                        print(f"提取的回答: {answer}\n")
                        # 验证答案是否符合要求
                        #is_valid = validate_answer(query, answer)
                        if 1:
                            question_and_answer = {
                                "question": query,
                                "answer": answer,
                                "source": source,
                                "domain": "biomedicine",
                                "details": {
                                    "type": "QA",
                                    "task": "information_retrieval",
                                    "database type": "corpus",
                                    "source": "arxiv"
                                }
                            }
                            all_questions_and_answers.append(question_and_answer)
                            save_questions_and_answers("L1_questions_answers.json", all_questions_and_answers)
                            question_count += 1  # 增加计数器
                        else:
                            print("生成的答案不符合要求，已跳过。")
                    else:
                        print(f"无法生成检索数据，文件: {file_path} 的第 {i+1} 部分")
                else:
                    print(f"文件 {file_path} 的第 {i+1} 部分中没有有用的信息")
            except Exception as e:
                print(f"读取文件 {file_path} 第 {i+1} 部分时出错: {e}")

# 将所有问题和回答保存到文件
save_questions_and_answers("L1_questions_answers.json", all_questions_and_answers)

print("所有文件处理完成。")
