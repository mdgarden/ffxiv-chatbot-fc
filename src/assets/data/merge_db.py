import json

KR_DB_PATH = "src/assets/data/ko-items.json"
GB_DB_PATH = "src/assets/data/items.json"


def parse_json(path):
    with open(path, "r") as f:
        parsed_json = json.load(f)
    return parsed_json


def merge_json(target, source):
    merged_json = {}
    for key in target:
        print(key)
        try:
            merged_json[key] = target[key].update(source[key])
        except Exception as ex:
            print(ex)
            print("passed")

    # print("merged json files")
    target.update(source)
    return target


def write_json(obj):
    # Serializing json
    json_object = json.dumps(obj, indent=4)

    # Writing to sample.json
    with open("sample.json", "w") as outfile:
        outfile.write(json_object)


kr_data = parse_json(KR_DB_PATH)
gb_data = parse_json(GB_DB_PATH)

# merge_json(gb_data, kr_data)

write_json(merge_json(gb_data, kr_data))
