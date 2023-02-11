import requests
import re

# ポケモンHOMEで動作しているjsファイルの取得。
url = "https://resource.pokemon-home.com/battledata/js/bundle.js"
response = requests.get(url)
response.encoding = response.apparent_encoding
response_text = response.text

# js内の表記まま
LANGUAGE_LIST = [
    "JPN",
    "USA",
    "FRA",
    "ITA",
    "DEU",
    "ESP",
    "KOR",
    "SCH",
    "TCH",
]

# jsの中に、ポケモン名、タイプ名はリスト形式、技名、特性名、性格名はdict型で記述されていた。
# それに合わせて、データを取得
poke_names_list = re.findall(r"poke:[^\]]+\]", response_text)
type_names_list = re.findall(r"pokeType:[^\]]+\]", response_text)
move_names_list = re.findall(r"waza:[^\}]+\}", response_text)
ability_names_list = re.findall(r"tokusei:[^\}]+\}", response_text)
nature_names_list = re.findall(r"seikaku:[^\}]+\}", response_text)
# アイテムの名称は、こちらのURLにGETリクエスト送ると取得できます。
# https://resource.pokemon-home.com/battledata/json/itemname_ja.json


def devide_by_language(
    names_list: list[str],
    deleted_index: str,
    langages: list[str] = LANGUAGE_LIST,
) -> dict:
    """jsから取得した各種名称データを、言語ごとに分けて出力する。

    param:
        names_list:jsonファイルから取得した各種名称。
        deleted_index:name_listから削除するindex名。例)poke:
        langages:names_listに入っている名称群に対して付与する言語名。
    return:
        言語ごとに分割された名称群のdict。言語名がキー。
    """
    output = {}
    for i, language in enumerate(langages):
        name = names_list[i].replace(deleted_index, "")
        output[language] = eval(name)
    return output


def save_text(contents, file_name):
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(contents)


POKE_NAMES = devide_by_language(poke_names_list, "poke:")
TYPE_NAMES = devide_by_language(type_names_list, "pokeType:")
MOVE_NAMES = devide_by_language(move_names_list, "waza:")
ABILITY_NAMES = devide_by_language(ability_names_list, "tokusei:")
NATURE_NAMES = devide_by_language(nature_names_list, "seikaku:")

# textファイルに出力する場合は、コメントアウトを外す。
# save_text(str(POKE_NAMES), "./asset/pokemon_names.txt")
# save_text(str(TYPE_NAMES), "./asset/type_names.txt")
# save_text(str(MOVE_NAMES), "./asset/move_names.txt")
# save_text(str(ABILITY_NAMES), "./asset/ability_names.txt")
# save_text(str(NATURE_NAMES), "./asset/nature_names.txt")
