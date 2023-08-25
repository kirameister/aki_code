import json
import argparse

def main(args):
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
        ngram_kanji_set = set(list(ngram))
        new_kanji_list = list(ngram_kanji_set.difference(defined_kanji_set))
        if(len(new_kanji_list) != 1):
            continue
        if(len(ngram_kanji_set.intersection(defined_kanji_set)) == 0):
            continue
        if(args.mesh_mode): # only interested in tri-gram
            if(len(ngram) != 3):
                continue
            new_kanji = new_kanji_list[0]
            new_kanji_score_dict[new_kanji] = new_kanji_score_dict.get(new_kanji, [ngram]) + [ngram]
        else:
            new_kanji = new_kanji_list[0]
            if(new_kanji in defined_kanji_set):
                continue
            if(len(ngram) > 2):
                continue
            #new_kanji_score_dict[new_kanji] = new_kanji_score_dict.get(new_kanji, 0.0) + 1
            new_kanji_score_dict[new_kanji] = new_kanji_score_dict.get(new_kanji, [ngram]) + [ngram]

    #kanji_rank_sorted_list = sorted(new_kanji_score_dict.items(), key=lambda item: item[1], reverse=True)
    kanji_rank_sorted_list = sorted(new_kanji_score_dict.items(), key=lambda item: len(item[1]), reverse=True)

    for entry in kanji_rank_sorted_list:
        print(entry)


if(__name__ == '__main__'):
    parser = argparse.ArgumentParser(description='Suggest possible Kanji candidate')
    parser.add_argument('-a', '--alpha', type=float, default=0.5, help="Float value of alpha when calculating the score")
    parser.add_argument('-m', '--mesh_mode', action='store_true', help='Only prints the Kanji from tri-gram where the rest of 2 tokens are already defined in the layout')
    args = parser.parse_args()
    main(args)

