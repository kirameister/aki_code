#!/usr/bin/env python
import argparse
import json
import re

argparse_desc = """Construct aki_code JSON from given txt file

    The input text file must consist of lines with either one of following formats:
        * "^#.*" to indicate the line is a comment
        * "^\\w(\\t|\\s+)\\w(\\t\\s+)\\w$" where the first 2 chars are the sequence of key-strokes (so they must be ASCII) and the 3rd char is converted Kanji
        * "^\\w\\w(\\t|\\s+)\\w$" the same as above, but not using tab between 2 strokes
"""

def main():
    parser = argparse.ArgumentParser(description=argparse_desc)
    parser.add_argument('-o', '--output_path', type=str, default="data/stroke_layout.json", help="path to the output JSON file")
    parser.add_argument('input_text_path', type=str, help="Path to the input text file")
    args = parser.parse_args()

    json_data = dict()
    # First we load the txt file
    with open(args.input_text_path, 'r') as f:
        lines = f.readlines()

    # sanity check and char extractions
    for line in lines:
        if re.search('^#', line):
            continue
        if not re.search('\\w(\\t|\\s+)?\\w(\\t|\\s+)\\w$', line):
            continue
        match = re.match(r'(\w)(\t|\s+)?(\w)(\t|\s+)(\w)', line)
        first, _, second, _, kanji = match.groups()
        if first not in json_data:
            json_data[first] = dict()
        if second in json_data[first]:
            print(f'Collision detected for the combination \t "{first}" + "{second}" => "{json_data[first][second]}" replaced with "{kanji}"')
        json_data[first][second] = kanji

    with open(args.output_path, 'w') as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False, sort_keys=True)


if __name__ == '__main__':
    main()
