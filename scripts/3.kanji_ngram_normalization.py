import json
import numpy as np

kanji_data_norm = dict()
ngram_data_norm = dict()

with open('data/wikipedia_joyo_kanji_occurr.json') as f:
    kanji_data = json.load(f)

# {"年": [5744064,"1"]},
for kanji_d in kanji_data:
    for kanji, vals in kanji_d.items():
        kanji_data_norm[kanji] = np.log10(vals[0]) # this really doesn't need to be log10

with open('data/wikipedia_joyo_kanji_occurr_normalized.json', 'w') as f:
    json.dump(kanji_data_norm, f, indent=4, ensure_ascii=False)


with open('data/n_gram_to_weight.json') as f:
    ngram_data = json.load(f)

# [["日本",594779],
# ["現在",246779],
for ngram in ngram_data:
   ngram_data_norm[ngram[0]] = np.log10(ngram[1])

with open('data/n_gram_to_weight_normalized.json', 'w') as f:
    json.dump(ngram_data_norm, f, indent=4, ensure_ascii=False)
