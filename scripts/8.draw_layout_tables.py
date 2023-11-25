
import collections
import argparse
import json
import re
from PIL import Image, ImageDraw, ImageFont

import single_to_double_nest_json_structure # this is goofy, but seems easier than dealing with a file starting with number and dot...

output_file_path = "image/aki_code_tables.jpg"

ttfontname = "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf"
fontsize = 16
font = ImageFont.truetype(ttfontname, fontsize)

qwerty_layout = [   ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"], 
                    ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"], 
                    ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";"], 
                    ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/"] ]

first_stroke_fill_color = (51, 255, 255)
core_color = (255, 255, 204)

qwerty_fill_color = [
        [None, None,       None,       None,       None, None, None,       None,       None,       None],
        [None, core_color, core_color, core_color, None, None, core_color, core_color, core_color, None],
        [None, core_color, core_color, core_color, None, None, core_color, core_color, core_color, None],
        [None, core_color, core_color, core_color, None, None, core_color, core_color, core_color, None]
        ]

char_to_pos = dict()
for i in range(len(qwerty_layout)):
    for j in range(len(qwerty_layout[i])):
        char_to_pos[qwerty_layout[i][j]] = (i, j)

def detect_duplicate_keys(list_of_pairs):
    key_count = collections.Counter(k for k,v in list_of_pairs)
    duplicate_keys = ', '.join(k for k,v in key_count.items() if v>1)

    if len(duplicate_keys) != 0:
        raise ValueError('Duplicate key(s) found: {}'.format(duplicate_keys))

def validate_data(list_of_pairs):
    detect_duplicate_keys(list_of_pairs)
    # More dectection, each of them will raise exception upon invalid
    # data
    return dict(list_of_pairs)

def main(args):
    # enumerate first
    if(not args.no_enumeration):
        single_to_double_nest_json_structure.main()
        
    # load the layout data
    with open('data/stroke_layout.json') as f:
        stroke_layout = json.load(f, object_pairs_hook=validate_data)
    box_width  = 18
    box_height = 28
    padding_width  = 2
    padding_height = 2
    segment_width  = (box_width  + padding_width)  * 10
    segment_height = (box_height + padding_height) * 4
    all_width  = padding_width + 10 * segment_width
    all_height = padding_height + 4 * segment_height
    im = Image.new('RGB', (all_width, all_height), (255, 255, 255))
    draw = ImageDraw.Draw(im)

    for first_key in stroke_layout:
        if(first_key not in char_to_pos): # safe-guard
            continue
        # draw boxes..
        (h, w) = char_to_pos[first_key]
        segment_origin_h = padding_height + segment_height * h
        segment_origin_w = padding_width  + segment_width  * w
        for i in range(len(qwerty_layout)):
            for j in range(len(qwerty_layout[i])):
                fill_color = (255, 255, 255)
                if(qwerty_fill_color[i][j] is not None):
                    fill_color = qwerty_fill_color[i][j]
                if(i == h and j == w):
                    fill_color = first_stroke_fill_color
                draw.rectangle((segment_origin_w + box_width  * j,
                                segment_origin_h + box_height * i,
                                segment_origin_w + box_width  * (j+1),
                                segment_origin_h + box_height * (i+1)),
                                fill=fill_color, outline=(0, 0, 0))

        # start drawing the char
        for second_key in stroke_layout[first_key]:
            if(second_key not in char_to_pos): # anotehr safe-guard
                continue
            (h, w) = char_to_pos[second_key]
            # the following line is to split the Kanji from the the comment, whihc are supposed to be split by the first space
            kanji_to_print = re.sub('\\s.*$', '', stroke_layout[first_key][second_key])
            #comment_for_the_kanji = re.sub('^.*?\\s', '', stroke_layout[first_key][second_key])
            draw.multiline_text((segment_origin_w + (box_width * w), segment_origin_h + (box_height * h)),
                                kanji_to_print, fill=(0, 0, 0), font=font)

    # save the file
    im.save(output_file_path, quality=95)

if(__name__ == '__main__'):
    parser = argparse.ArgumentParser(description='Generate layout tables given the layout JSON')
    parser.add_argument('-n', '--no_enumeration', action='store_true', help='Do not conduct enumeration from the stroke_layout_src.json; use stroke_layout.json directly instead.')
    args = parser.parse_args()
    main(args)
