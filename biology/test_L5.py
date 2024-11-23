# 导入 ragTool 类和消息类型
from rag_tool import ragTool
from langchain_core.messages import SystemMessage, HumanMessage
import random
import os
import openai
import json

# 定义一个函数来提取有用的信息
# def extract_useful_information(content):
#     system_message = (
#         "Analyze the following text to determine if it contains valuable information "
#         "such as data, tables, chemical substances, biology compositions, or other important information"
#         "excluding information about the author or the article itself."
#         "in the field of biologys science. Additionally, determine if the answer to a potential retrieval question "
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

# 定义一个函数来验证答案是否符合要求
# def validate_answer(question, answer):
#     if answer in question:
#         return "False"
#     if len(answer) > 10:
#         return "False"
#     if ("____" in answer) or ("?" in answer):
#         return "False"
#     system_message = (
#         "You are an assistant that checks if the given answer sufficiently and directly addresses the given question. "
#         "The question should avoid references to 'the text', 'the study', 'the research', or any unnecessary context about the article or author, and should not include the answer. "
#         "The answer should be suitable for F1 evaluation, focusing solely on addressing the core question. "
#         "Please analyze the following question and answer, and determine if the question avoids referencing specific text or unnecessary details, "
#         "Return 'True' if the question and answer meet these standards. If not, return 'False'. "
#         "Do not return anything else."
#     )
#     user_message = f"question: '{question}'\nAnswer: '{answer}'"
    
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",  # 您可以使用 "gpt-4" 或其他可用的模型
#         messages=[
#             {"role": "system", "content": system_message},
#             {"role": "user", "content": user_message},
#         ],
#     )
#     result = response.choices[0].message.content
#     return result


# 函数：随机从 RAG 数据库中检索内容并生成推理性问题
def generate_inference_question():
    # 随机检索内容片段（这里我们随机取一个片段）
    all_content = rag_tool.random_retrieve_milvus("biology_collection", )  # 调用检索函数，不指定查询关键词
    #print(all_content)
    if (not all_content) :
        #useful_info = extract_useful_information(all_content)
        if 1:
            print("数据库中没有内容可供生成问题。") 
            return "数据库中没有内容可供生成问题。"

    #random_content = random.choice(all_content)  # 随机选择一个内容片段
    # 设置系统消息来生成信息验证问题
    system_message = (
        "You are an expert in biologys science. Based on the provided `<text>`, identify a specific fact or claim that could benefit from verification, "
        "such as experimental data, references, chemical substances, biology compositions, or any other directly relevant scientific information. "
        "The fact should be relevant to the scientific context and directly relate to the content provided, without additional inference or assumption."
    
        "Then, create a natural language question in the form of a yes-or-no question to verify the identified fact or claim. "
        "The question should explore the accuracy or validity of a specific detail in the text and encourage a 'yes' or 'no' response based on context. "
        "To achieve a balance between 'yes' and 'no' answers, consider posing questions that may challenge assumptions, explore alternatives, or require careful verification of details. Examples include: "
        "- Confirming or questioning specific experimental data, such as temperature, pressure, or concentration"
        "- Verifying or challenging the use of a particular chemical substance or biology"
        "- Validating a scientific claim or hypothesis relevant to the findings, especially when there may be alternative interpretations"
    
        "Ensure the question is:"
        "- Clear and specific, formatted as a yes-or-no question"
        "- Directly focused on verifying or challenging a particular fact or claim in the context of the provided text"
        "- Answerable with a straightforward 'yes' or 'no' to provide clear verification or refutation of the information"
    
        "For example, structure your question in JSON format as follows:"
        "{"
        "  \"question\": \"Is MoS₂ definitely the most effective catalyst in this experiment, compared to other potential biologys?\""
        "}"
    
        "Do not include the answer or any specific information in the question itself, and avoid any references to 'the text', 'the study', or 'the research'."
    )




    
    # 构建人类消息，传递随机选取的内容
    user_message = f"<text>:\n{all_content}\nPlease identify one key piece of information from the text, and generate a natural language inference question that requires reasoning based on that information."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
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

def save_questions_and_answers(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# 初始化 ragTool 实例
rag_tool = ragTool()

# 1. 存储多个文档向量
# 假设当前目录下有 "小米SU7.docx" 文件
# 读取文件夹中的所有文件
folder_path = r""  # 替换为你的文件夹路径

#result = rag_tool.vector_storage("E:/AAProgramming/AAmy/llm/RAG/txt_00.txt")
#print(f"文件txt00 的处理结果: {result}")

#for filename in os.listdir(folder_path):
#   file_path = os.path.join(folder_path, filename)
#   if os.path.isfile(file_path) and filename.lower().endswith('.txt'):  # 确保是 txt 文件
#       try:
#           result = rag_tool.vector_storage(file_path)
#           print(f"文件 {filename} 的处理结果: {result}")
#       except Exception as e:
#            print(f"文件 {filename} 处理时出错，已跳过。错误信息: {e}")

# 初始化OpenAI客户端
client = openai.OpenAI(
    api_key="",
    base_url='https://api.openai.com/v1'
)

system_message = (
    "You are a biologys science expert. Based on the question and the provided context, answer the question directly with either 'yes' or 'no,' depending on whether the context supports the claim. "
    "Your answer should be concise and directly relevant to the question, without adding any additional information or explanation."

    "The answer should be:"
    "- A single word, either 'yes' or 'no,' based solely on the provided context"
    "- Precise and directly addressing the question, without further details or commentary"

    "Provide json form of the answer as follows:"
    "{"
    "  \"answer\": \" yes or no \""
    "}"
)

rag_tool.messages = [SystemMessage(content=system_message)]

# 存储所有问题和回答的列表
all_questions_and_answers = []
# 生成多个推理问题示例
for i in range(300):
    try:
        # 1. 生成推理问题
        question = generate_inference_question().get("question", "")
        print(f"生成的推理问题 {i+1}:", question)
        
        # 2. 提问并获取答案
        answer = rag_tool.get_answer(question)
        print("回答:", answer)
        
        # 3. 验证答案是否符合要求
        #is_valid = validate_answer(question, answer)
        if 1:
            # 4. 构建问题和答案的结构
            question_and_answer = {           
                "question": question,
                "answer": answer,
                "domain": "biology",
                "details": {
                    "type": "QA",
                    "task": "Verification Question",
                    "database type": "corpus",
                    "source": "arxiv"
                }
            }
            # 5. 添加到列表并保存
            all_questions_and_answers.append(question_and_answer)
            save_questions_and_answers("L5_questions_answers.json", all_questions_and_answers)
        else:
            print("生成的问答不符合要求，已跳过。")
    
    except Exception as e:
        # 捕获并显示错误信息，但不中断循环
        print(f"生成问答时出错，已跳过。错误信息: {e}")



