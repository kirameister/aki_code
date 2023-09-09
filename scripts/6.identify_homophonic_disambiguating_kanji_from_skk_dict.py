
import json
import re
import sys


already_defined_kanji_set = set()
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

with open('data/stroke_layout.json') as f:
    stroke_layout = json.load(f)
    for first_key in stroke_layout:
        for second_key in stroke_layout[first_key]:
            already_defined_kanji_set.add(re.sub('\\s.*$', '', stroke_layout[first_key][second_key]))


lines = sys.stdin.read()

for line in lines.split('\n'):
    if(line == ""):
        continue
    if(re.search(';;', line)):  # ignore the comment-line
        continue
    line = re.sub(';.*?/', '/', line)  # strip the comment segment
    [yomi, kanji_str] = re.split(' ', line)
    if(yomi is None or kanji_str is None):
        print(f'something went wrong on {line}')  # actually this should never need to be called..
        continue
    if(kanji_str.count('/') <= 2):
        continue

    k_to_occur_dict = dict()
    for kanji in kanji_str.split('/'):
        if(kanji == ''):
            continue
        if(len(kanji) == 1):
            continue
        for c in list(kanji):
            k_to_occur_dict[c] = k_to_occur_dict.get(c, 0) + 1
    # ..reading of all the kanji chars done; now we are going to take only the unique char for disambiguation
    for c, v in k_to_occur_dict.items():
        if(v == 1 and c in joyo_kanji_set):
            c_key = c
            # we're going to add a suffix marker to indicate that this kanji is already defined in the layout
            if(c in already_defined_kanji_set):
                c_key = c + "_"
            new_kanji_score_dict[c_key] = new_kanji_score_dict.get(c_key, []) + [line]

kanji_rank_sorted_list = sorted(new_kanji_score_dict.items(), key=lambda item: len(item[1]), reverse=True)

for entry in kanji_rank_sorted_list:
    pass
    print(entry)
