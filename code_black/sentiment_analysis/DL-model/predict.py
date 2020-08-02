import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from model import Model
import spacy

def predict_class(model, sentence, nlp, TEXT, LABELS, min_len = 4, device='cpu'):
    model.eval()
    tokenized = [tok.text for tok in nlp.tokenizer(sentence)]
    if len(tokenized) < min_len:
        tokenized += ['<pad>'] * (min_len - len(tokenized))
    indexed = [TEXT.stoi[t] for t in tokenized]
    tensor = torch.LongTensor(indexed).to(device)
    tensor = tensor.unsqueeze(1)
    preds = torch.sigmoid(model(tensor))
    #max_preds = preds.argmax(dim = 1) # for multiclass
    return preds[0][0]


def predict(review_list):
    TEXT = torch.load("vocab.pt")
    LABELS = torch.load("label.pt")
    nlp = spacy.load('en')
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    model = Model()
    model = model.to(device)
    sentiment=[]
    for review in review_list:
        ans = predict_class(model, review, nlp, TEXT, LABELS, device=device)
        ans = round(float(ans*5))
        if ans==0:
            ans=1
        sentiment.append(ans)
    return sentiment

x = input("Input the string: ")
l = []
l.append(x)
ans = predict(l)
print(ans)
