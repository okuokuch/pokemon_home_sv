import json
from constant import MAPPING_POKEMON, MAPPING_MOVE
import pandas as pd


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


def make_move_list(detail_json: dict, lang="JPN") -> list[list[str, str, str, float]]:
    output = []
    for name_id, value_all in detail_json.items():
        name = MAPPING_POKEMON[lang][int(name_id) - 1]
        for form_id, value_2 in value_all.items():
            for i, waza_val in enumerate(value_2["temoti"]["waza"]):
                move_name = MAPPING_MOVE[lang][waza_val["id"]]
                raito = waza_val["val"]
                output.append([name, form_id, i, move_name, raito])
    return output


if __name__ == "__main__":
    # ピカチュウの技が表示されるかのテスト
    df = pd.DataFrame(
        make_move_list(detail_json),
        columns=["pokemon", "form", "rank", "move", "raito"],
    )
    df.to_csv("./test/df.csv", encoding="shift-jis")
