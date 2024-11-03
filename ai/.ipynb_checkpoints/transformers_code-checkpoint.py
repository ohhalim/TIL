import warnings
warnings.filterwarnings('ignore')

from transformers import pipeline

sentiment_analysis = pipeline("sentiment-analysis")

result = sentiment_analysis("I hate you")
print(result)