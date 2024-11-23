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
#         "such as data, tables, chemical substances, biomedicine compositions, or other important information"
#         "excluding information about the author or the article itself."
#         "in the field of biomedicine science. Additionally, determine if the answer to a potential retrieval question "
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
def validate_question(question):
    # if answer in question:
    #     return "False"
    #if len(answer) > 20:
    #    return "False"
    if "text" in question or "study" in question or "research" in question:
        return "False"

    # system_message = (
    #     "You are an assistant that checks if the given answer sufficiently and directly addresses the given question. "
    #     "The question should avoid references to 'the text', 'the study', 'the research', or any unnecessary context about the article or author, and should not include the answer. "
    #     "The answer should be suitable for F1 evaluation, focusing solely on addressing the core question, meaning it should be concise and precise. "
    #     "Please analyze the following question and answer, and determine if the question avoids referencing specific text or unnecessary details, "
    #     "and if the answer is directly relevant and appropriately concise. "
    #     "Return 'True' if the question and answer meet these standards. If not, return 'False'. "
    #     "Do not return anything else."
    # )
    # user_message = f"question: '{question}'\nAnswer: '{answer}'"
    
    # response = client.chat.completions.create(
    #     model="gpt-3.5-turbo",  # 您可以使用 "gpt-4" 或其他可用的模型
    #     messages=[
    #         {"role": "system", "content": system_message},
    #         {"role": "user", "content": user_message},
    #     ],
    # )
    # result = response.choices[0].message.content
    return "True"


# 函数：随机从 RAG 数据库中检索内容并生成推理性问题
def generate_inference_question():
    # 随机检索内容片段（这里我们随机取一个片段）
    all_content = rag_tool.random_retrieve_milvus("biomedicine_collection", )  # 调用检索函数，不指定查询关键词
    #print(all_content)
    # if (not all_content) :
    #     useful_info = extract_useful_information(all_content)
    #     if useful_info.strip() != 'True':
    #         print("数据库中没有内容可供生成问题。") 
    #         return "数据库中没有内容可供生成问题。"

    #random_content = random.choice(all_content)  # 随机选择一个内容片段
    # 设置系统消息来生成信息补全问题
    system_message = (
        "You are an expert in biomedicine science. Based on the provided `<text>`, generate specific and precise questions in the format described below. Each question must target a particular missing attribute related to biological interactions, such as confidence scores, references (e.g., PMIDs), sources, or experimental methods."
        
        "The questions must:"
        "- Clearly specify the context, including the biological entities involved (e.g., Protein_A and Protein_B)."
        "- Use placeholders (e.g., _____) to represent the missing information."
        "- Target specific, actionable details from the dataset, such as confidence scores, sources, or PMIDs."
        "- Avoid ambiguity by directly referencing entities and their attributes."
        "For example, structure your question in JSON format as follows:"
        "{"
        "  \"question\": \"the generated question\""
        "}"
        "Examples of questions include:"
        "Fill in the missing information: The interaction between NEB1_HUMAN and ACTG_HUMAN has a confidence score of _____ and is supported by PMIDs 9362513, 12052877."
        "Complete the following: The sources for the interaction between SRGN_HUMAN and CD44_HUMAN include HPRD, I2D, Rual05, and _____."
        "The interaction involving PAK1_HUMAN and ERBB2_HUMAN is supported by experiments including Affinity Capture-Western and _____."
        "For the interaction between DLG4_HUMAN and ERBB2_HUMAN, the PMIDs include 10839362 and _____, with a confidence score of 0.88."
        
        "Ensure your generated questions adhere to these rules:"
        "- Each question must specify the biological entities involved and the exact missing detail."
        "- Use a natural language format with placeholders for the missing parts."
        "- Keep the questions concise, precise, and directly related to the dataset structure."
        
        "Generate similar questions by referencing the provided `<text>` to ensure completeness and accuracy."

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
    return json.loads(result), all_content

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
#           result = rag_tool.vector_stor
# age(file_path)
#           print(f"文件 {filename} 的处理结果: {result}")
#       except Exception as e:
#            print(f"文件 {filename} 处理时出错，已跳过。错误信息: {e}")

# 初始化OpenAI客户端
client = openai.OpenAI(
    api_key="",
    base_url='https://api.openai.com/v1'
)

system_message = (
    "You are a biomedicine science expert. Based on the question and the provided context, fill in the missing or incomplete scientific information needed to make the content whole. "
    "Ensure that your completion is concise, directly relevant to the context, and does not add unnecessary information or assumptions."

    "The completed answer should be:"
    "- Brief and precise, containing only the essential missing information"
    "- Directly relevant to the context, maintaining scientific accuracy"
    "- Seamlessly integrated into the original content to create a cohesive and complete response"
    "Provide only the missing content as your answer, without any additional explanations or commentary."
    "One vacancy corresponds to one answer. if there are multiple lines to fill, separate multiple answers with a comma."
    "For example, structure your question in JSON format as follows:"
    "{"
    "  \"answer\": [\"answer1 \"]"
    "}"
    
)

rag_tool.messages = [SystemMessage(content=system_message)]

# 存储所有问题和回答的列表
all_questions_and_answers = []
# 生成多个推理问题示例
for i in range(300):
    try:
        # 1. 生成推理问题
        generate_json, source_text= generate_inference_question()
        question = generate_json.get("question", "")
        print(f"生成的推理问题 {i+1}:", question)
        
        # 2. 提问并获取答案
        rag_answer = rag_tool.get_answer(question)
        answer = json.loads(rag_answer).get("answer", "")
        print("回答:", answer)
        
        # 3. 验证问题是否符合要求
        is_valid = validate_question(question)
        if  'True':
            # 4. 构建问题和答案的结构
            question_and_answer = {           
                "question": question,
                "answer": answer,
                "Type": "Content Completion",
                "source_text": source_text,
                "Source": "arxiv",
                "database type": "corpus",
                "domain": "biomedicine",
                "URL": "https://arxiv.org/"
            }
            # 5. 添加到列表并保存
            all_questions_and_answers.append(question_and_answer)
            save_questions_and_answers("L4_questions_answers.json", all_questions_and_answers)
        else:
            print("生成的问答不符合要求，已跳过。")
    
    except Exception as e:
        # 捕获并显示错误信息，但不中断循环
        print(f"生成问答时出错，已跳过。错误信息: {e}")



