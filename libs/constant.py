import json


def read_json(path):
    with open(path, "r", encoding="utf8") as f:
        return json.load(f)


URL_SEASON = "https://api.battle.pokemon-home.com/tt/cbd/competition/rankmatch/list"
URL_POKEMON = "https://resource.pokemon-home.com/battledata/ranking/scvi/{cid}/{rst}/{ts}/pokemon"
URL_POKEMON_DETAIL = "https://resource.pokemon-home.com/battledata/ranking/scvi/{cid}/{rst}/{ts}/pdetail-{num}"
MAPPING_POKEMON = read_json("./asset/pokemon_names.json")
MAPPING_ABILITY = read_json("./asset/ability_names.json")
MAPPING_MOVE = read_json("./asset/move_names.json")
MAPPING_NATURE = read_json("./asset/nature_names.json")
MAPPING_TYPE = read_json("./asset/type_names.json")
