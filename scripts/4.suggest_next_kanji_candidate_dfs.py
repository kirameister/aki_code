import json

alpha = 0.5

defined_kanji_set = set()
with open('data/stroke_layout.json') as f:
    stroke_layout = json.load(f)

for stroke1 in stroke_layout.keys():
    for stroke2, k in stroke_layout[stroke1].items():
        defined_kanji_set.add(k)

with open('data/wikipedia_joyo_kanji_occurr_normalized.json') as f:
    kanji_score_data = json.load(f)

with open('data/n_gram_to_weight_normalized.json') as f:
    ngram_score_data = json.load(f)

new_kanji_score_dict = dict()

for ngram, score in ngram_score_data.items():
    if(len(ngram) > 2): #FIXME(?)
        continue
    bigram_kanji_set = set(list(ngram))
    if(len(bigram_kanji_set.intersection(defined_kanji_set)) == 0):
        continue
    if(len(bigram_kanji_set.intersection(defined_kanji_set)) == 2): 
        # we're not interested in kanji's we already have in the layout
        continue
    new_kanji = list(bigram_kanji_set.difference(defined_kanji_set))[0]
    #new_kanji_score_dict[new_kanji] = new_kanji_score_dict.get(new_kanji, 0.0) + alpha * kanji_score_data[new_kanji]
    new_kanji_score_dict[new_kanji] = new_kanji_score_dict.get(new_kanji, 0.0) + alpha * score

kanji_rank_sorted_list = sorted(new_kanji_score_dict.items(), key=lambda item: item[1], reverse=True)

for entry in kanji_rank_sorted_list:
    print(entry)


