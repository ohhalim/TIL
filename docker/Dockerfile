# 기본 이미지 설정해준다
FROM python:3.8-slim

# 파이썬 쓸건데 가장 가벼ㅜㄴ 이미졸 골라줘
# 애플리케이션 파일 복사
# 내가 만든 app.py 만 붕어빵에 담아야지

COPY app.py /app.py
# 컨테이너 안의 이름 바꾸고 싶어면 오른쪽거 바꾸면됨 뭐 main.py 이런식으로
# 플라스크를 설치해야함 플라스크로 만들었으니까
# Flask 설치
RUN pip install Flask

# 이제 애플리케이션 프로그램 실행
# 애플리케이션 실행
CMD ["python", "/app.py"]

# run 이랑 다름  run 은 그냥돌리는거고 CMD 는 형식이 정해져있을떄 함


