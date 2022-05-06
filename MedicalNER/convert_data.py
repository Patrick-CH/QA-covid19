import json

'''
 Example::

        Nadim NNP B-NP B-PER
        Ladki NNP I-NP I-PER

        AL-AIN NNP B-NP B-LOC
        United NNP B-NP B-LOC
        Arab NNP I-NP I-LOC
        Emirates NNPS I-NP I-LOC
        1996-12-06 CD I-NP O
        ...
'''

train_path = "D:/workspace/PycharmProjects/Covid-19-QA/data/CMeEE/CMeEE_train.json"
dev_path = "D:/workspace/PycharmProjects/Covid-19-QA/data/CMeEE/CMeEE_dev.json"


def convert(data, to_path):
    with open(to_path, 'w', encoding='utf-8') as txt_file:
        for example in data:
            tags = ['O' for i in range(len(example['text']))]
            if len(tags) > 200:
                continue
            for e in example['entities']:
                tags[e['start_idx']] = f"B-{e['type']}".upper()
                for idx in range(e['start_idx'] + 1, e['end_idx'] + 1):
                    tags[idx] = f"I-{e['type']}".upper()
            for i, char in enumerate(example['text']):
                txt_file.write(f'{char} {tags[i]}\n')
            txt_file.write('\n')


if __name__ == '__main__':
    with open(train_path, "r", encoding='UTF-8') as f:
        train_data = json.loads(f.read())
        convert(train_data, "D:/Data/chinese_ner/CMeEE/CMeEE_train_clip.txt")
    with open(dev_path, "r", encoding='UTF-8') as f:
        dev_data = json.loads(f.read())
        convert(train_data, "D:/Data/chinese_ner/CMeEE/CMeEE_test_clip.txt")
