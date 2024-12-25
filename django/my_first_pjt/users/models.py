from django.db import models

from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):  # 클래스 이름이 MYuser가 아닌 MyUser인지 확인
    # 추가 필드 정의
    pass