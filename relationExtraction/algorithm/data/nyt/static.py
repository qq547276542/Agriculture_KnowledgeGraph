import json

with open('test.json') as fr:
    train_data = json.load(fr)
    for x in train_data:
        if(x['relation'] != 'NA'):
            print(x['head']['word'])
            print(x['tail']['word'])
            print(x['relation'])
            print("====================")

