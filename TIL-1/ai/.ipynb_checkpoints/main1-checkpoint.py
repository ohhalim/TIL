import os
import openai

# 환경 변수에서 API 키 가져오기
openai.api_key = os.getenv("OPENAI_API_KEY")  # OPENAI_API_KEY 환경 변수가 설정되어 있어야 함

# ChatCompletion 호출 예제
completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",  # 또는 "gpt-3.5-turbo" 등 사용 가능한 모델로 변경 가능
    messages=[
        {"role": "system", "content": "너는 환영 인사를 하는 인공지능이야, 농담을 넣어 재미있게 해줘"},
        {"role": "user", "content": "안녕?"}
    ]
)

# 응답 출력
print("Assistant:", completion.choices[0].message['content'])
