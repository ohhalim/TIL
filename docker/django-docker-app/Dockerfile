
# (베이스 이미지)
# python:3.9-slim이라는 이미지를 Docker hub에서 가져와 줘!
FROM python:3.9-slim

# (작업 디렉토리 설정)
# 앞으로 돌아갈 컨테이너에는 app이라는 폴더를 만들어서, 거기에서 작업할 거야
WORKDIR /app

# (종속성 설치)
# requirements.txt을 WORKDIR로 설정한 app이라는 폴더에 옮겨줘.
COPY requirements.txt .

# requirements.txt에 있는 거 전부 설치해줘.
RUN pip install -r requirements.txt


# (소스 코드 복사)
# 지금 폴더를 컨테이너에 다 복사해줘.
COPY . .

# (포트 노출)
# 8000번 포트만 컨테이너에서 외부에 노출(expose)시킬 거야.
EXPOSE 8000

# (명령 실행)
# python manage.py runserver 0.0.0.0:8000 명령어를 컨테이너에서 실행해줘.
# 0.0.0.0은 외부에 연결 가능한 것을 의미 '외부에 가능하다!'
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
