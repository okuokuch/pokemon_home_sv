import json
from constant import MAPPING_POKEMON, MAPPING_MOVE


def read_json(path):
    with open(path, "r", encoding="utf8") as f:
        return json.load(f)


detail_json: dict = read_json("./asset/sample/detail-1.json")


def apply_mapping_name(data, lang="JPN"):
    data = {}
    for name_id, value in detail_json.items():
        name = MAPPING_POKEMON[lang][int(name_id) - 1]
        data[name] = value
    return data


def apply_mapping_data(id_persentage_data: list[dict], mapping_data: dict, lang="JPN"):
    data = {}
    for value in id_persentage_data:
        name = mapping_data[lang][value["id"]]
        percent = value["val"]
        data[name] = percent
    return data


if __name__ == "__main__":
    # ピカチュウの技が表示されるかのテスト
    print(apply_mapping_data(detail_json["25"]["0"]["temoti"]["waza"], MAPPING_MOVE))
