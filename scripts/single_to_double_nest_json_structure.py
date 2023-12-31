
import collections
import json
import re

def detect_duplicate_keys(list_of_pairs):
    key_count = collections.Counter(k for k,v in list_of_pairs)
    #duplicate_keys = ', '.join(k for k,v in key_count.items() if v>1)
    duplicate_keys = ', '.join(k for k,v in key_count.items() if(v>1 and not k.startswith('_'))) # modified from the original detectiton versino as we'd like to allow commenting values starting with '_'
    if(len(duplicate_keys) != 0):
        raise ValueError('Duplicate key(s) found: {}'.format(duplicate_keys))

def validate_data(list_of_pairs):
    detect_duplicate_keys(list_of_pairs)
    # More dectection, each of them will raise exception upon invalid
    # data
    return dict(list_of_pairs)

def main():
    generated_json_data = dict()
    value_set = set()
    with open('data/stroke_layout_src.json') as f:
        stroke_layout_src = json.load(f, object_pairs_hook=validate_data)
    for stroke, value in stroke_layout_src.items():
        if(len(stroke) != 2):
            print(f'key detected with len(key)!=2: "{stroke}". This value is ignored')
            continue
        [first, second] = list(stroke)
        if(first not in generated_json_data):
            generated_json_data[first] = dict()
        generated_json_data[first][second] = value
        value = re.sub('\\s.*$', '', value)
        if(value in value_set):
            print(f'The value {value} has been defined with multiple strokes')
        value_set.add(value)
    with open('data/stroke_layout.json', 'w') as f:
        json.dump(generated_json_data, f, indent=4, ensure_ascii=False)


if(__name__ == '__main__'):
    main()
