#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Version : Python 3.6

import json
import re
from nltk.tokenize import word_tokenize

RELEVANT_SEM_REL = { "Cause-Effect", "Component-Whole", "Product-Producer" }

def search_entity(sentence):
    e1 = re.findall(r'<e1>(.*)</e1>', sentence)[0]
    e2 = re.findall(r'<e2>(.*)</e2>', sentence)[0]
    sentence = sentence.replace('<e1>' + e1 + '</e1>', ' <e1> ' + e1 + ' </e1> ', 1)
    sentence = sentence.replace('<e2>' + e2 + '</e2>', ' <e2> ' + e2 + ' </e2> ', 1)
    sentence = word_tokenize(sentence)
    sentence = ' '.join(sentence)
    sentence = sentence.replace('< e1 >', '<e1>')
    sentence = sentence.replace('< e2 >', '<e2>')
    sentence = sentence.replace('< /e1 >', '</e1>')
    sentence = sentence.replace('< /e2 >', '</e2>')
    sentence = sentence.split()

    assert '<e1>' in sentence
    assert '<e2>' in sentence
    assert '</e1>' in sentence
    assert '</e2>' in sentence

    return sentence


def convert(path_src, path_des):
    with open(path_src, 'r', encoding='utf-8') as fr:
        data = fr.readlines()
    with open(path_des, 'w', encoding='utf-8') as fw:
        for i in range(0, len(data), 4):
            id_s, sentence = data[i].strip().split('\t')
            sentence = sentence[1:-1]
            sentence = search_entity(sentence)
            relation = data[i+1].strip()
            label_class = relation.split("(")[0]
            if label_class not in RELEVANT_SEM_REL:
                relation = "Other"
            meta = dict(
                id=id_s,
                relation=relation,
                sentence=sentence,
                comment=data[i+2].strip()[8:]
            )
            json.dump(meta, fw, ensure_ascii=False)
            fw.write('\n')


if __name__ == '__main__':
    path_train = './data/SemEval2010_task8_all_data/SemEval2010_task8_training/TRAIN_FILE.TXT'
    path_test = './data/SemEval2010_task8_all_data/SemEval2010_task8_testing_keys/TEST_FILE_FULL.TXT'

    convert(path_train, 'train.json')
    convert(path_test, 'test.json')
