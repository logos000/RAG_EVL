import openai

# 设置 API 密钥和自定义 base_url
client = openai.OpenAI(
    api_key="",
    base_url='https://api.ai-gaochao.cn/v1'
)

# 定义问题生成的功能
def generate_answer(user_input, question_type):
    """
    根据用户输入和问题类型生成问题或答案
    question_type: "retrieval" (检索), "qa" (问答), "reasoning" (推理)
    """
    # 定义三类问题的提示词
    if question_type == "retrieval":
        system_message = (
            "You are an expert assistant specialized in information retrieval. When given a retrieval request, "
            "you need to retrieve relevant information or documents from a large dataset. Your task is to search for "
            "and return all relevant information related to the user's input."
        )
        user_message = f"Retrieve information about: {user_input}"
    
    elif question_type == "qa":
        system_message = (
            "You are a research assistant tasked with answering natural language questions based on known information. "
            "Given a question from the user, your task is to answer it with the most accurate information available."
        )
        user_message = f"Answer the following question: {user_input}"
    
    elif question_type == "reasoning":
        system_message = (
            "You are an expert in combining external information and logical reasoning to provide answers to complex queries. "
            "When presented with a reasoning-based question, you must analyze the available data and perform logical deduction to provide a well-reasoned answer."
        )
        user_message = f"Analyze and answer the following reasoning question: {user_input}"
    
    else:
        return "Invalid question type. Please select 'retrieval', 'qa', or 'reasoning'."
    
    # 调用 OpenAI API 生成答案
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
    )
    
    # 提取并返回生成的答案
    #print(response)
    result = response.choices[0].message.content
    return result

# 示例输入
user_input_retrieval = "Find all relevant literature about the application of deep learning in protein structure prediction."
user_input_qa = "What are the latest breakthroughs in protein folding prediction in 2022?"
user_input_reasoning = "Based on research trends in materials science over the past five years, predict the future breakthrough areas."

# 调用不同的能力生成答案
retrieval_result = generate_answer(user_input_retrieval, "retrieval")
qa_result = generate_answer(user_input_qa, "qa")
reasoning_result = generate_answer(user_input_reasoning, "reasoning")

# 打印结果
print("Retrieval Result:\n", retrieval_result)
print("\nQA Result:\n", qa_result)
print("\nReasoning Result:\n", reasoning_result)

