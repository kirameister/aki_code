import json
import re

import tensorflow
import tensorflow_datasets as tfds
joyo_kanji_set = set()
kanji_year_dict = dict()
wikipedia_kanji_occurr_dict = dict()

# load JSON with Kanji list
with open('data/kanji.json') as f:
    kanji_data = json.load(f)

year_keys = ["1", "2", "3", "4", "5", "6", "7"]
for y in year_keys:
    ks = set(list(kanji_data[y]["s"]))
    ky = kanji_data[y]["w"]
    for k in ks:
        joyo_kanji_set.add(k)
        kanji_year_dict[k] = y

ds = tfds.load('wiki40b/ja', split='train')
corpus_list = list(ds.as_numpy_iterator())
corpus_size = len(corpus_list)

for i in range(corpus_size):
    #if(i % 1000 == 0):
    if(i+1 % 100 == 0):
        print(f"Iteration {i} passed")
        #break
    lines = corpus_list[i]['text'].decode('utf-8')
    for line in lines.splitlines():
        if(re.search("_START_PARAGRAPH_", line) or re.search("_START_ARTICLE_", line) or re.search("_START_SECTION_", line)):
            continue
        letter_list =  list(line)
        for c in letter_list:
            if(c in joyo_kanji_set):
                if(c in wikipedia_kanji_occurr_dict):
                    wikipedia_kanji_occurr_dict[c] += 1
                else:
                    wikipedia_kanji_occurr_dict[c] = 1

# re-formatting..
dump_list_temp = sorted(wikipedia_kanji_occurr_dict.items(), key=lambda item: item[1], reverse=True)
dump_list = []
for i in dump_list_temp:
    d = dict()
    d[i[0]] = [i[1], kanji_year_dict[i[0]]]
    dump_list.append(d)

# dump data in JSON format
with open('data/wikipedia_joyo_kanji_occurr.json', 'w') as f:
    #json.dump(wikipedia_kanji_occurr_dict, f, indent=4, ensure_ascii=False)
    json.dump(dump_list, f, indent=4, ensure_ascii=False)

