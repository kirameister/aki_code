import argparse
import json

def main(args):
    joyo_kanji_set = set()
    with open(args.input_json) as f:
        radical_to_kanji = json.load(f)
    with open(args.joyo_kanji_json) as f:
        joyo_kanjis = json.load(f)
    for year in joyo_kanjis.keys():
        if(year.startswith('.')):
            continue
        kl = list(joyo_kanjis[year]['s'])
        joyo_kanji_set |= set(kl)
    #print(joyo_kanji_set)
    if(len(args.radical) == 1):
        if(args.radical not in radical_to_kanji):
            print(f'{args.radical} not found in the element dictionary. Exiting..')
            exit()
        for k in radical_to_kanji[args.radical]:
            if(k in joyo_kanji_set):
                print(k)


if(__name__ == '__main__'):
    parser = argparse.ArgumentParser(description='Print Joyo Kanjis from a given radical (部首)')
    parser.add_argument('-i', '--input_json', type=str, default="../kanjivg-radical/data/element2kanji.json", help="Path to the JSON file storing dictionary of Radical to Kanjis")
    parser.add_argument('-j', '--joyo_kanji_json', type=str, default="./data/kanji.json", help="Path to the JSON file storing list of Joyo Kanjis")
    parser.add_argument('radical', type=str, help="Radical to extract Kanjis of")
    args = parser.parse_args()
    main(args)

