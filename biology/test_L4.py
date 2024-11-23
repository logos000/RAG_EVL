# 导入 ragTool 类和消息类型
from rag_tool import ragTool
from langchain_core.messages import SystemMessage, HumanMessage
import random
import os
import openai
import json

# 定义一个函数来提取有用的信息
def extract_useful_information(content):
    system_message = (
        "Analyze the following text to determine if it contains valuable information "
        "such as data, tables, chemical substances, biology compositions, or other important information"
        "excluding information about the author or the article itself."
        "in the field of biology science. Additionally, determine if the answer to a potential retrieval question "
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
    all_content = rag_tool.random_retrieve_milvus("biology_collection", )  # 调用检索函数，不指定查询关键词
    #print(all_content)
    if (not all_content) :
        useful_info = extract_useful_information(all_content)
        if useful_info.strip() != 'True':
            print("数据库中没有内容可供生成问题。") 
            return "数据库中没有内容可供生成问题。"

    #random_content = random.choice(all_content)  # 随机选择一个内容片段
    # 设置系统消息来生成信息补全问题
    system_message = (
        "You are an expert in biology science. Based on the provided `<text>`, identify any missing or incomplete scientific information needed to complete the content, "
        "such as specific experimental data, references, chemical substances, biology compositions, or other directly relevant details. "
        "This missing information should be directly relevant to the scientific inquiry, excluding any details about the author or general context of the article itself. "
        "Ensure the identified missing information is precise, relevant, and directly related to the context of the provided text, without additional inference or assumption."

        "Next, create a natural language question in the following format to request the missing information, using placeholders for the missing parts: "
        "\"Fill in the missing information in the following sentence: <sentence with missing parts>.\" Ensure the question includes specific placeholders (e.g., ______) for each missing detail, such as data values, chemical names, or conditions, "
        "so that it is clear exactly what information needs to be filled in. Examples of completion types include: "
        "- Adding specific experimental data such as temperature, pressure, or reagent concentration "
        "- Adding missing chemical substances or biology compositions "
        "- Supplementing with specific references or scientific claims "

        "Ensure the question is:"
        "- Clear and specific, using placeholders to indicate where information is missing"
        "- Focused on guiding the completion of the missing information in the context of the provided text"
        "- Answerable with a fixed, concise response to accurately complete the content"

        "For example, structure your question in JSON format as follows:"
        "{"
        "  \"question\": \"Fill in the missing information in the following sentence: In this study, we used ______ as a catalyst, with experimental conditions of temperature ______ and concentration ______.\""
        "}"

        "Again, DO NOT include the answer or any specific information in the question itself, and avoid any references to 'the text', 'the study', or 'the research'."
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
    "You are a biology science expert. Based on the question and the provided context, fill in the missing or incomplete scientific information needed to make the content whole. "
    "Ensure that your completion is concise, directly relevant to the context, and does not add unnecessary information or assumptions."

    "The completed answer should be:"
    "- Brief and precise, containing only the essential missing information"
    "- Directly relevant to the context, maintaining scientific accuracy"
    "- Seamlessly integrated into the original content to create a cohesive and complete response"
    "Provide only the missing content as your answer, without any additional explanations or commentary."
    "One vacancy corresponds to one answer. if there are multiple lines to fill, separate multiple answers with a comma."
    "For example, structure your question in JSON format as follows:"
    "{"
    "  \"answer\": [\"answer1 \", \"answer2\"]"
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
                "domain": "biology",
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



