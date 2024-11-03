from openai import OpenAI

client = OpenAI()

completion = client.chat.completions.create(
    model = "gpt-3.5_turbo",
    message = [
       {"role":"system","content":"너는 변호사야 나에게 법적인 상담을 해줘"},
       {"role":"user","content":"안녕하세요 저는 배형호입니다."}
    ]
)


print("대답" + completionchoices[0].message.comtent)
