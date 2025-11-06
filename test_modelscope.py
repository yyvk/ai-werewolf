"""
测试ModelScope API连接
"""
import sys
import io
from openai import OpenAI
from dotenv import load_dotenv
import os

# 设置输出编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 加载环境变量
load_dotenv()

# 创建客户端
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE")
)

print("测试ModelScope API连接...")
print(f"API Base: {os.getenv('OPENAI_API_BASE')}")
print(f"模型: {os.getenv('OPENAI_MODEL')}")
print("-" * 60)

try:
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "Qwen/Qwen2.5-7B-Instruct"),
        messages=[
            {"role": "system", "content": "你是一个友善的AI助手。"},
            {"role": "user", "content": "请用一句话介绍狼人杀游戏。"}
        ],
        stream=True
    )
    
    print("[成功] 连接成功！AI回复：\n")
    for chunk in response:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end='', flush=True)
    
    print("\n\n" + "=" * 60)
    print("[成功] ModelScope API配置成功！")
    print("[游戏] 现在可以运行AI狼人杀项目了！")
    print("=" * 60)
    
except Exception as e:
    print(f"\n[失败] 连接失败: {e}")
    print("\n请检查：")
    print("1. ModelScope Access Token 是否正确")
    print("2. 网络连接是否正常")
    print("3. .env 文件配置是否正确")

