import os
import openai
import json
import re
import random
import tqdm
from rag_tool import ragTool
from langchain_core.messages import SystemMessage, HumanMessage
# 初始化OpenAI客户端
client = openai.OpenAI(
    api_key="",
    base_url='https://api.openai.com/v1'
)

# 定义一个函数来提取有用的信息
# def extract_useful_information(content):
#     system_message = (
#         "Analyze the following text to determine if it contains valuable information "
#         "such as data, tables, chemical substances, biology compositions, or other important information"
#         "excluding information about the author or the article itself."
#         "in the field of biologys science. Additionally, determine if the answer to a potential retrieval query "
#         "can be described in a few concise words. If both conditions are met, return 'True'. "
#         "If not, return 'False'. Do not return anything else."
#     )
#     user_message = f"The text to be analyzed is: '{content}'"
    
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": system_message},
#             {"role": "user", "content": user_message}
#         ]
#     )
#     result = response.choices[0].message.content
#     return result

# 定义一个函数来生成选择题
def generate_question(content):
    system_message = (
        "You are an expert in information retrieval in the field of biological sciences. Based on the provided data, your task is to generate retrieval questions that focus on retrieving specific attributes, relationships, or properties related to proteins, IDs, confidence scores, experiments, or other biological data. Ensure that the questions are precise and target clearly defined attributes or entities within the dataset."
        
        "Each question must explicitly specify a biological entity (e.g., a protein name, ID) and its associated attribute or relationship to ensure the retrieval task is highly specific and actionable. The query should aim to retrieve one of the following:"
        "- Unique identifiers (e.g., protein IDs)."
        "- Relationships between two proteins (e.g., Confidence_Score or experimental methods)."
        "- Specific biological data related to a protein (e.g., experiments or PMIDs)."
        
        "The questions must:"
        "- Be precise and directly reference specific entities or attributes."
        "- Avoid vague or generalized phrasing such as 'relevant information.'"
        "- Ensure clarity and focus, making it clear what needs to be retrieved."
        
        "Structure your output in JSON format as follows:"
        "{"
        "  \"query\": \"the retrieval query that specifies the target information\","
        "  \"answer\": \"the corresponding value extracted from the data\""
        "}"
        
        "Key emphasis:"
        "- Explicitly include protein names, IDs, or relationships in the query."
        "- Focus on actionable and specific retrieval tasks (e.g., 'Retrieve the specific charactors for substance (or flipped)')."
        "- Avoid ambiguity and ensure the query aligns with the dataset's structure."

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

# # 定义一个函数来验证答案是否符合要求
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
# def split_content(content, max_length=1024):
#     paragraphs = content.split('\n\n')
#     parts = []
#     current_part = ''
#     current_length = 0

#     for paragraph in paragraphs:
#         lines = paragraph.split('\n')
#         for line in lines:
#             if current_length + len(line) <= max_length:
#                 current_part += line + '\n'
#                 current_length += len(line)
#             else:
#                 parts.append(current_part.strip())
#                 current_part = line + '\n'
#                 current_length = len(line)
#         current_part += '\n'  # 添加段落之间的空行

#     if current_part.strip():
#         parts.append(current_part.strip())
    
#     return parts


# 定义一个函数从txt文件中提取文本
def extract_text_from_txt(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


# 读取文件夹中的所有MMD文件
# folder_path = r""  # 替换为你的文件夹路径

def save_questions_and_answers(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# 存储所有问题和回答的列表
all_questions_and_answers = []
rag_tool = ragTool()

# 遍历文件夹中的每个MMD文件
for i in range(300):
    try:
        parts = rag_tool.random_retrieve_milvus("medical_collection", )  # 调用检索函数，不指定查询关键词
        #question_count = 0  # 初始化计数器
        #for i, part in tqdm.tqdm(enumerate(parts), desc="Qa process"):
            #try:    
                # if question_count >= 6:
                #     break  # 如果问题数量达到6个，停止生成
                # print(f"正在处理文件: {file_path} 的第 {i+1} 部分")
                # # useful_info = extract_useful_information(part)
        if 1:
            #print(f"有用的信息提取自文件: {file_path} 的第 {i+1} 部分")
            #print(part)
            retrieval_data = generate_question(parts)
            if retrieval_data is not None:
                query = retrieval_data.get("query", "")
                answer = retrieval_data.get("answer", "")
                source = parts
                print(f"生成的检索问题: {query}\n")
                print(f"提取的回答: {answer}\n")
                # 验证答案是否符合要求
                #is_valid = validate_answer(query, answer)
                if 1:
                    question_and_answer = {
                        "question": query,
                        "answer": answer,
                        "source": source,
                        "domain": "biology",
                        "details": {
                            "type": "QA",
                            "task": "information_retrieval",
                            "database type": "corpus",
                            "source": "arxiv"
                        }
                    }
                    all_questions_and_answers.append(question_and_answer)
                    save_questions_and_answers("L1_questions_answers.json", all_questions_and_answers)
                    #question_count += 1  # 增加计数器
                else:
                    print("生成的问答不符合要求，已跳过。")
    except Exception as e:
        # 捕获并显示错误信息，但不中断循环
        print(f"生成问答时出错，已跳过。错误信息: {e}")
                        # else:
                        #     print("生成的答案不符合要求，已跳过。")
            #         else:
            #             print(f"无法生成检索数据，文件: {file_path} 的第 {i+1} 部分")
            #     else:
            #         print(f"文件 {file_path} 的第 {i+1} 部分中没有有用的信息")
            # except Exception as e:
            #     print(f"读取文件 {file_path} 第 {i+1} 部分时出错: {e}")

# 将所有问题和回答保存到文件
save_questions_and_answers("L1_questions_answers.json", all_questions_and_answers)

print("所有文件处理完成。")
