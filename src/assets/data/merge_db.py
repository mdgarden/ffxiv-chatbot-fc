import json

KR_DB_PATH = "src/assets/data/ko-items.json"
GB_DB_PATH = "src/assets/data/items.json"

# 팀크래프트 DB업데이트 후 한번씩 실행시킬 것


def parse_json(path):
    with open(path, "r") as f:
        parsed_json = json.load(f)
    return parsed_json


def merge_json(target, source):
    merged_json = {}
    for key in target:
        try:
            merged_json[key] = target[key] | source[key]
        except Exception as ex:
            print(ex)
            source[key] = {"ko": ""}
            merged_json[key] = target[key] | source[key]

    return merged_json


def write_json(obj):
    # Serializing json
    json_object = json.dumps(obj, indent=4, ensure_ascii=False)

    # Writing to sample.json
    with open("merged_db.json", "w") as outfile:
        outfile.write(json_object)


kr_data = parse_json(KR_DB_PATH)
gb_data = parse_json(GB_DB_PATH)

write_json(merge_json(gb_data, kr_data))
