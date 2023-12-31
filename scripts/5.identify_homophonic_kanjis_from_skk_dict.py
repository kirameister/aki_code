
import json
import re
import sys
joyo_kanji_set = set()
new_kanji_score_dict = dict()

with open('data/kanji.json') as f:
    kanji_data = json.load(f)

year_keys = ["1", "2", "3", "4", "5", "6", "7"]
for y in year_keys:
    ks = set(list(kanji_data[y]["s"]))
    ky = kanji_data[y]["w"]
    for k in ks:
        joyo_kanji_set.add(k)

lines = sys.stdin.read()

for line in lines.split('\n'):
    if(line == ""):
        continue
    if(re.search(';;', line)): # ignore the comment-line
        continue
    line = re.sub(';.*?/', '/', line) # strip the comment segment
    #print(line)
    [yomi, kanji_str] = re.split(' ', line)
    if(yomi is None or kanji_str is None):
        print(f'something went wrong on {line}') # actually this should never need to be called..
        continue
    if(kanji_str.count('/') <= 2):
        continue

    #print(f'{yomi} \t {kanji_str}')
    for kanji in kanji_str.split('/'):
        if(kanji == ''):
            continue
        if(len(kanji) == 1):
            continue
        for c in list(kanji):
            if(c in joyo_kanji_set):
                #new_kanji_score_dict[c] = new_kanji_score_dict.get(c, [kanji]) + [kanji]
                #new_kanji_score_dict[c] = new_kanji_score_dict.get(c, [kanji+"-"+yomi]) + [kanji+"-"+yomi]
                new_kanji_score_dict[c] = new_kanji_score_dict.get(c, []) + [kanji+"-"+yomi]

kanji_rank_sorted_list = sorted(new_kanji_score_dict.items(), key=lambda item: len(item[1]), reverse=True)

for entry in kanji_rank_sorted_list:
    pass
    print(entry)

