import json

KR_DB_PATH = "src/assets/data/ko-items.json"
GB_DB_PATH = "src/assets/data/items.json"


def parse_json(path):
    with open(path, "r") as f:
        parsed_json = json.load(f)
    return parsed_json


parse_json(KR_DB_PATH)
parse_json(GB_DB_PATH)


def merge_json(target, source):
    merged_json = {}
    for item in target:
        merged_json = merged_json.append(item[0].append(source[item[0]]))
    return merged_json
