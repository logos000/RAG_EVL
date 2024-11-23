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
#     if len(answer) > 20:
#         return "False"
#     system_message = (
#         "You are an assistant that checks if the given answer sufficiently and directly addresses the given question. "
#         "The question should avoid references to 'the text', 'the study', 'the research', or any unnecessary context about the article or author, and should not include the answer. "
#         "The answer should be suitable for F1 evaluation, focusing solely on addressing the core question, meaning it should be concise and precise. "
#         "Please analyze the following question and answer, and determine if the question avoids referencing specific text or unnecessary details, "
#         "and if the answer is directly relevant and appropriately concise. "
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
    all_content = rag_tool.random_retrieve_milvus("test_collection", )  # 调用检索函数，不指定查询关键词
    #print(all_content)
    # if (not all_content) :
    #     useful_info = extract_useful_information(all_content)
    #     if useful_info.strip() != 'True':
    #         print("数据库中没有内容可供生成问题。") 
    #         return "数据库中没有内容可供生成问题。"

    #random_content = random.choice(all_content)  # 随机选择一个内容片段
    # 设置系统消息来生成推理性问题
    system_message = ("You are an expert in biology science. Based on the provided `<text>`, identify exactly one piece of scientifically valuable information, such as specific data, chemical substances, biology compositions, or other directly relevant scientific information. "
        "This information should be precise and directly relevant to the scientific inquiry, excluding any details about the author or the article itself. "
        "Ensure the selected information is concise, specific, and taken directly from the text with no modification, rephrasing, or inference."

        "Then, create a natural language inference question based on the selected information that requires one of the following types of reasoning: "
        "- Inferring a biology's specific composition or identifying a substance "
        "- Predicting or estimating a precise data value "
        "- Judging whether a scientific claim or hypothesis is correct (answerable with 'yes' or 'no') "
        "- Making a choice between specific options based on scientific analysis or comparison "

        "The question should be designed to elicit a highly accurate, clear, and directly extractable response. "
        "The answer must be highly specific and suitable for F1 evaluation, such as a biology name, a specific numeric value, or a clear 'yes' or 'no.' "

        "Ensure the question is:"
        "- Clear and unambiguous"
        "- Designed to encourage critical thinking or scientific reasoning"
        "- Based on the selected scientific information in a way that requires logical inference"
        "- Answerable with a concise, accurate, and directly extractable response to ensure strong alignment with F1 score calculations"

        "Structure your response in JSON format as follows:"
        "{"
        "  \"question\": \"the natural language inference question generated based on the selected information\""
        "}"

        "Again, DO NOT include the answer or the specific information in your question, and DO NOT reference 'the text', 'the study', 'the research' in your question."
        )
    
    # 构建人类消息，传递随机选取的内容
    user_message = f"<text>:\n{all_content}\nPlease identify one key piece of information from the text, and generate a natural language inference question that requires reasoning based on that information."

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

def save_questions_and_answers(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# 初始化 ragTool 实例
rag_tool = ragTool()

# 1. 存储多个文档向量
# 假设当前目录下有 "小米SU7.docx" 文件
# 读取文件夹中的所有文件
folder_path = r"E:\AAProgramming\AAmy\RAG_EVL\biology\html_3"  # 替换为你的文件夹路径
import nltk
#nltk.download('punkt', force=True)
nltk.data.path.append('C:\\Users\\Cielo\\AppData\\Roaming\\nltk_data')
#result = rag_tool.vector_storage("E:/AAProgramming/AAmy/RAG_EVL/biology/html_2/3169.html")
#print(f"文件txt00 的处理结果: {result}")

# for filename in os.listdir(folder_path):
#   file_path = os.path.join(folder_path, filename)
#   if os.path.isfile(file_path) and filename.lower().endswith('.html'):  # 确保是 txt 文件
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

system_message = ("You are a biology science expert. Please answer the question based strictly on the provided context, using reasoning as needed to give a precise response. "
                "Ensure that your answer is concise, exact, and directly derived from the context, containing only the essential information. "
                "The answer should be as brief and specific as possible, such as a substance name, a single data point, or 'yes'/'no' where appropriate, and should meet F1 evaluation standards. "
                "Do not include any additional explanations, descriptions, or unrelated details in your response."
                )
rag_tool.messages = [SystemMessage(content=system_message)]

# 存储所有问题和回答的列表
all_questions_and_answers = []
# 生成多个推理问题示例
for i in range(300):
    try:
        question = generate_inference_question().get("question", "")
        print(f"生成的推理问题 {i+1}:", question)
        # 2. 提问并获取答案
        answer = rag_tool.get_answer(question)
        print("回答:", answer)
        #is_valid = validate_answer(question, answer)
        #if is_valid.strip() == 'True':
        if answer.strip() != "":
            question_and_answer = {           
                "question": question,
                "answer": answer,
                "domain": "biology",
                "details": {
                    "type": "QA",
                    "task": "Inference Question",
                    "database type": "corpus",
                    "source": "arxiv"
                }
            }
            all_questions_and_answers.append(question_and_answer)
            save_questions_and_answers("L3_questions_answers.json", all_questions_and_answers)
        else:
            print("生成的问答不符合要求，已跳过。")
    except Exception as e:
        # 捕获并显示错误信息，但不中断循环
        print(f"生成问答时出错，已跳过。错误信息: {e}")

