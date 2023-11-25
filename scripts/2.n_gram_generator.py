import json
import re

import tensorflow
import tensorflow_datasets as tfds
ds = tfds.load('wiki40b/ja', split='train')

kanji_weight_dict = dict()
n_gram_to_weight_dict = dict()

# load JSON with Kanji list
with open('data/kanji.json') as f:
    kanji_data = json.load(f)

year_keys = ["1", "2", "3", "4", "5", "6", "7"]
for y in year_keys:
    ks = set(list(kanji_data[y]["s"]))
    kw = kanji_data[y]["w"]
    for k in ks:
        kanji_weight_dict[k] = kw

#print(kanji_weight_dict) ## debug

corpus_list = list(ds.as_numpy_iterator())
corpus_size = len(corpus_list)

for i in range(corpus_size):
    if(i % 1000 == 0):
        print(f"Iteration {i} passed")
        #exit()
    lines = corpus_list[i]['text'].decode('utf-8')
    for line in lines.splitlines():
        if(re.search("_START_PARAGRAPH_", line) or re.search("_START_ARTICLE_", line) or re.search("_START_SECTION_", line)):
            continue
        letter_list =  list(line)
        prev_kanji_str = ""
        for c in letter_list:
            # checking n-grams...
            if(c in kanji_weight_dict):
                if(prev_kanji_str == ""):
                    prev_kanji_str = c
                else:
                    prev_kanji_str = prev_kanji_str + c
                    if(len(prev_kanji_str) > 3): # we're only interested up to tri-gram
                        prev_kanji_str = prev_kanji_str[-3:]
                    if(prev_kanji_str in n_gram_to_weight_dict):
                        n_gram_to_weight_dict[prev_kanji_str] = n_gram_to_weight_dict[prev_kanji_str] + 1 ## this part could well be optimized.
                    else:
                        n_gram_to_weight_dict[prev_kanji_str] = 1 ## ...and this part..
            else:
                prev_kanji_str = ""

# re-formatting..
dump_list = sorted(n_gram_to_weight_dict.items(), key=lambda item: item[1], reverse=True)
dump_list = dump_list[:100000] # pure cut-off


with open('data/n_gram_to_weight.json', 'w') as f:
    #json.dump(n_gram_to_weight_dict, f, indent=4, ensure_ascii=False)
    json.dump(dump_list, f, indent=4, ensure_ascii=False)

