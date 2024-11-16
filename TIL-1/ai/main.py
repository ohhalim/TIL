from fastapi import FastAPI

# FastAPI 인스턴스 생성
app = FastAPI()

# 루트 경로에 GET 요청이 들어왔을 때 "Hello World!"를 반환하는 엔드포인트 정의
@app.get("/test")
def read_root():
    return {"message": "Hello api"}

# uvicorn your_script_name:app --reload 터미널에서 해당 명령어 실행

@app.get("/test2")
def read_root_2():
    return {"message": "test2 "}