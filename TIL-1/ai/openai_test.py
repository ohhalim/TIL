
import os
from openai import OpenAI

# 환경 변수에서 API 키를 가져오기
api_key = os.getenv("OPENAI_API_KEY")

# OpenAI 클라이언트 설정
client = OpenAI(api_key=api_key)

# 예시 API 호출
completion = client.chat.completions.create(
  model="gpt-4",
  messages=[
    {"role": "system", "content": "너는 환영 인사를 하는 인공지능이야, 농담을 넣어 재미있게 해줘"},
    {"role": "user", "content": "안녕?"}
  ]
)

print("Assistant: " + completion.choices[0].message.content)
