import json
with open('agriculture/train_dataset.json','r',encoding='utf8') as fr:
    h = json.load(fr)

print(h[0]['sentence'])
