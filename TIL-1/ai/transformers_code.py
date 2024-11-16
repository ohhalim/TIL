import warnings
warnings.filterwarnings('ignore')

from transformers import BertModel, BertTokenizer
import torch
from scipy.spatial.distance import cosine


model_name = "bert-base-uncased"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)


sentences = [
    "The quick brown fox jumps over the lazy dog",
    "the king is hyeongho"
]



input1 = tokenizer(sentences[0], return_tensors='pt')
input2 = tokenizer(sentences[1], return_tensors='pt')

with torch.no_grad():
    output1 = model(**input1)
    output2 = model(**input2)

embedding1 = output1. last_hidden_state.mean(dim=1).squeeze().cpu().numpy()
embedding2 = output2. last_hidden_state.mean(dim=1).squeeze().cpu().numpy()


similarity = 1 - cosine(embedding1, embedding2)

print(f"Cosine sinilarity beteen the two sentencens: {similarity: 4f}")

