
import argparse
import json
from PIL import Image, ImageDraw, ImageFont

output_file_path = "image/aki_code_tables.jpg"

ttfontname = "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf"
fontsize = 16
font = ImageFont.truetype(ttfontname, fontsize)

qwerty_layout = [   ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"], 
                    ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"], 
                    ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";"], 
                    ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/"] ]

char_to_pos = dict()
for i in range(len(qwerty_layout)):
    for j in range(len(qwerty_layout[i])):
        char_to_pos[qwerty_layout[i][j]] = (i, j)

def main(args):
    # load the layout data
    with open('data/stroke_layout.json') as f:
        stroke_layout = json.load(f)
    box_width  = 15
    box_height = 25
    padding_width  = 2
    padding_height = 2
    segment_height = (box_height + padding_height) * 4
    segment_width  = (box_width  + padding_width)  * 10
    if(args.no_number):
        segment_height = (box_height + padding_height) * 33
    all_width  = padding_width + 10 * segment_width
    all_height = padding_height + 4 * segment_height
    if(args.no_number):
        all_height = all_height - box_height - padding_height
    im = Image.new('RGB', (all_width, all_height), (255, 255, 255))
    draw = ImageDraw.Draw(im)

    for first_key in stroke_layout:
        if(first_key not in char_to_pos): # safe-guard
            continue
        if(args.no_number and first_key in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0")):
            continue
        # draw boxes..
        (h, w) = char_to_pos[first_key]
        segment_origin_h = padding_height + segment_height * h
        segment_origin_w = padding_width  + segment_width  * w
        for i in range(len(qwerty_layout)):
            for j in range(len(qwerty_layout[i])):
                if(i == h and j == w):
                    draw.rectangle((segment_origin_w + box_width  * j, 
                                    segment_origin_h + box_height * i, 
                                    segment_origin_w + box_width  * (j+1), 
                                    segment_origin_h + box_height * (i+1)), 
                                   fill=(0, 192, 192), outline=(0, 0, 0))
                else:
                    draw.rectangle((segment_origin_w + box_width  * j, 
                                    segment_origin_h + box_height * i, 
                                    segment_origin_w + box_width  * (j+1), 
                                    segment_origin_h + box_height * (i+1)), 
                                   fill=(255, 255, 255), outline=(0, 0, 0))

        # start drawing the char
        for second_key in stroke_layout[first_key]:
            if(second_key not in char_to_pos): # anotehr safe-guard
                continue
            (h, w) = char_to_pos[second_key]
            draw.multiline_text((segment_origin_w + (box_width * w), segment_origin_h + (box_height * h)),
                                stroke_layout[first_key][second_key], fill=(0, 0, 0), font=font)


    # save the file
    im.save(output_file_path, quality=95)

if(__name__ == '__main__'):
    parser = argparse.ArgumentParser(description='Generate layout tables given the layout JSON')
    parser.add_argument('-n', '--no_number', action='store_true', help='Do not print the number row')
    args = parser.parse_args()
    main(args)
