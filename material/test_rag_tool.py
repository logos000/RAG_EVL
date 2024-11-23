# 导入 ragTool 类
from rag_tool import ragTool

# 初始化 ragTool 实例
rag_tool = ragTool()

# 1. 存储多个文档向量
# 假设当前目录下有 "example1.docx" 和 "example2.csv" 文件
for filename in ["小米SU7.docx"]:
    result = rag_tool.vector_storage(filename)
    print(f"文件 {filename} 的处理结果: {result}")

# 2. 提问并获取答案
question = "小米SU7的续航怎么样"
answer = rag_tool.get_answer(question)
print("回答:", answer)
