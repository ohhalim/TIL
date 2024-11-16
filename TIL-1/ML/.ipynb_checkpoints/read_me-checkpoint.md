# 머신러닝 첫 실습임

> 뭘공부할지 몰라서 문제은행에 있는거 공부중
    1. 머신러닝은 사람처럼 생각하고 행동하는 기술을 의미한다. (O/X)
    2. 딥러닝은 머신러닝의 한 분야로, 이미지 인식이나 자연어 처리에 뛰어나다. (O/X)
    3. 머신러닝에서는 수학 공식에 대한 깊은 이해가 필수적이다. (O/X)
    4. 머신러닝의 구성요소에는 데이터셋, 특징(Feature), 레이블이 포함된다. (O/X)
    5. 전통적인 프로그래밍은 데이터를 통해 스스로 학습하고 예측하는 능력을 갖춘다. (O/X)
    6. 지도 학습은 레이블이 없는 데이터셋을 이용하여 모델을 학습시키는 방법이다. (O/X)
    7. 배깅(Bagging)은 여러 모델을 독립적으로 학습시키고 예측을 평균내거나 다수결 투표로 최종 예측을 수행한다. (O/X)
    8. 과적합(Overfitting)은 모델이 훈련 데이터에 지나치게 적응하여 새로운 데이터에 대한 일반화 성능이 떨어지는 현상이다. (O/X)
    9. 모든 데이터셋에 대해 완벽한 성능을 보이는 모델이 존재한다. (O/X)
> \





문제 풀이 준비 먼저, 다양한 전처리 기법을 적용할 수 있는 가상의 데이터를 제공하겠습니다. 데이터는 Pandas DataFrame 형식으로 제공하며, 각 열은 다음과 같은 속성을 가집니다:
TransactionID: 거래 고유 ID
CustomerID: 고객 고유 ID
PurchaseAmount: 구매 금액 (USD)
PurchaseDate: 구매 날짜
ProductCategory: 제품 카테고리 (범주형 데이터)
CustomerAge: 고객 나이
CustomerGender: 고객 성별 (범주형 데이터)
ReviewScore: 제품 리뷰 점수 (1~5 사이의 값, 결측값 포함) 가상의 데이터를 생성하는 파이썬 코드는 다음과 같습니다: import pandas as pd import numpy as np # 가상 데이터 생성 data = { 'TransactionID': range(1, 21), 'CustomerID': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110], 'PurchaseAmount': [250, -50, 3000000, 450, 0, 300, 200, 150, -10, 800, 50, 75, 400, np.nan, 600, 1000, 20, 5000, 150, 80], 'PurchaseDate': pd.date_range(start='2024-01-01', periods=20, freq='ME').tolist(), 'ProductCategory': ['Electronics', 'Clothing', 'Electronics', 'Home', 'Electronics', 'Home', 'Clothing', 'Home', 'Clothing', 'Electronics', 'Electronics', 'Home', 'Clothing', 'Electronics', 'Home', 'Home', 'Clothing', 'Electronics', 'Home', 'Electronics'], 'CustomerAge': [25, 35, 45, np.nan, 22, 29, 33, 41, 27, 36, 28, 34, 42, 39, 24, 30, 32, 40, 38, 26], 'CustomerGender': ['Male', 'Female', 'Female', 'Male', 'Female', 'Male', 'Female', np.nan, 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female'], 'ReviewScore': [5, np.nan, 4, 3, 2, 5, 3, 4, 1, 2, np.nan, 4, 5, 3, 4, np.nan, 1, 5, 2, 4] } df = pd.DataFrame(data)
위 데이터에 대한 요구 사항입니다

다음은 데이터 전처리를 위한 문제입니다:
1. 결측값 처리:
   * PurchaseAmount, CustomerAge, CustomerGender, ReviewScore 열의 결측값을 적절히 처리하세요.
2. 이상치 처리:
   * PurchaseAmount 열에서 비정상적으로 큰 값과 음수 값을 처리하세요.
3. 중복 데이터 제거:
   * 중복된 TransactionID가 있는 경우 제거하세요.
4. 데이터 타입 변환:
   * PurchaseDate 열의 데이터 타입을 날짜 형식으로 변환하세요.
5. 정규화:
   * PurchaseAmount 열을 정규화하세요.
6. 범주형 데이터 선별 및 인코딩:
   * ProductCategory와 CustomerGender 열을 인코딩하세요.
7. 샘플링:
   * 데이터를 무작위로 5개 샘플링하세요.