import requests
import json
import pandas as pd
from tqdm import tqdm
from typing import Union, List, Dict


class pokemon_home:
    """ポケモンHOMEのデータを取得するためのクラス。"""

    def __init__(self, folder_path: str, language: str = "JPN") -> None:
        """指定されたフォルダパスから、マッピング用のjsonファイルを取得。

        param:
            folder_path:jsonファイルが入ったフォルダを指定する。
            language:アウトプットする言語を指定する。
                JPN,USA,FRA,ITA,DEU,ESP,KOR,SCH,TCHの9種類から選ぶ。
        """
        self.POKEMON = self.__read_json("{}/pokemon_names.json".format(folder_path))[language]
        self.MOVE = self.__read_json("{}/move_names.json".format(folder_path))[language]
        self.ABILITY = self.__read_json("{}/ability_names.json".format(folder_path))[language]
        self.TYPE = self.__read_json("{}/type_names.json".format(folder_path))[language]
        # アイテム名は日本語のみ
        self.ITEM = self.__read_json("{}/item_names.json".format(folder_path))["itemname"]

    def __read_json(self, path: str):
        """jsonファイルをutf-8で読み込む"""
        with open(path, "r", encoding="utf8") as f:
            return json.load(f)

    def request_parameters_from_season_info(self, season_number: int, rule: int) -> None:
        """ポケモンHOME APIを叩くのに必要なパラメータを取得する

        param:
            season_number:シーズン番号
            rule:シングルは1。ダブルは2を記入
        """
        url = "https://api.battle.pokemon-home.com/tt/cbd/competition/rankmatch/list"
        header = {}
        data = {"soft": "Sc"}
        res = requests.post(url, headers=header, json=data)
        response_json = json.loads(res.text)
        self.params = self._fetch_requirement_parameter(season_number, rule, response_json)

    def _fetch_requirement_parameter(self, season_number: int, rule: int, response: Dict) -> Dict[Union[str, int]]:
        """jsonからリクエストに必要なパラメータを取得する

        param:
            response:ランクバトルの情報リストのdictデータ
            season_number:シーズン番号
            rule:シングルは0。ダブルは1を記入
        return:
            dict型で以下を返す。
            cid:大会ID
            rst:現在のシーズンかどうかの判定。
            ts1:ユーザ情報を取得する際に使用するtimestamp
            ts2:ポケモン情報を取得するときに利用するtimestamp
        """
        parameters = {}
        season_infos = {}
        season_infos = response["list"][str(season_number)]
        cids = season_infos.keys()
        for cid in cids:
            season_info = season_infos[cid]
            if season_info["rule"] != rule:
                continue
            parameters = {
                "cid": cid,
                "rst": season_info["rst"],
                "ts1": season_info["ts1"],
                "ts2": season_info["ts2"],
            }
        return parameters

    def __fetch_pokemon_ranking(self):
        """APIを叩いてポケモンランキングを取得する"""
        url = "https://resource.pokemon-home.com/battledata/ranking/scvi/{cid}/{rst}/{ts}/pokemon"
        response = requests.get(url.format(cid=self.params["cid"], rst=self.params["rst"], ts=self.params["ts2"]))
        return json.loads(response.text)

    def __fetch_pokemon_detail(self, num: int):
        """APIを叩いてポケモンデータ詳細を取得する"""
        url = "https://resource.pokemon-home.com/battledata/ranking/scvi/{cid}/{rst}/{ts}/pdetail-{num}"
        response = requests.get(
            url.format(cid=self.params["cid"], rst=self.params["rst"], ts=self.params["ts2"], num=num)
        )
        return json.loads(response.text)

    def __convert_id_to_name(self, id: Union[str, int], mapping_data: Union[List, Dict]) -> str:
        """マッピングデータを用いて、IDを名前に変換する"""
        if type(mapping_data) == list:
            name = mapping_data[int(id)]
        elif type(mapping_data) == dict:
            name = mapping_data[str(id)]
        return name

    def __parse_pokemon_detail(self, detail_json: Dict):
        """ポケモンデータ詳細のjsonファイルから、データを取得、加工する

        param:
            detail_json:JSON形式のデータ詳細ファイル
        return:
            output_move:技所持率に関するデータ詳細
            output_ability:特性に関するデータ詳細
            output_item:アイテム所持率に関するデータ詳細
            output_teratype:テラスタイプに関するデータ詳細
        """
        output_move = []
        output_ability = []
        output_item = []
        output_teratype = []
        for pokemon_id, value in tqdm(detail_json.items()):
            pokemon_name = self.__convert_id_to_name(int(pokemon_id) - 1, self.POKEMON)
            for form_id, value_2 in value.items():
                pokemon_info = value_2["temoti"]
                output_move.extend(
                    self.__output_detail(pokemon_info["waza"], pokemon_name, pokemon_id, form_id, self.MOVE)
                )
                output_ability.extend(
                    self.__output_detail(pokemon_info["tokusei"], pokemon_name, pokemon_id, form_id, self.ABILITY)
                )
                output_item.extend(
                    self.__output_detail(pokemon_info["motimono"], pokemon_name, pokemon_id, form_id, self.ITEM)
                )
                output_teratype.extend(
                    self.__output_detail(pokemon_info["terastal"], pokemon_name, pokemon_id, form_id, self.TYPE)
                )
        return output_move, output_ability, output_item, output_teratype

    def __output_detail(self, info_json: list, pokemon_name: str, pokemon_id: str, form_id: str, mapping_data: Dict):
        """ポケモンデータ詳細の入ったリストからデータを取得し、メタデータを付与して返す

        param:
            info_json:ポケモンデータ詳細。技、特性、アイテム、テラスタイプの4種類ある。
            pokemon_name:ポケモン名
            pokemon_id:全国図鑑ID
            form_id:フォルムID
            mapping_data:種別ごとのマッピングデータ
        return:
            リスト[ポケモン名, ポケモンID, フォルムID, 順位, 名称, 割合]を複数格納したリスト
        """
        output = []
        for i, info in enumerate(info_json):
            name = self.__convert_id_to_name(info["id"], mapping_data)
            output.append([pokemon_name, pokemon_id, form_id, i + 1, name, info["val"]])
        return output

    def output_pokemon_ranking(self):
        """ポケモンランキングデータを加工して出力

        return:
            リスト[ポケモンID, フォルムID, ポケモン名]を複数格納したリスト
        """
        pokemon_ranking = self.__fetch_pokemon_ranking()
        output = []
        for i, pokemon in enumerate(pokemon_ranking):
            pokemon_name = self.__convert_id_to_name(pokemon["id"] - 1, self.POKEMON)
            form_id = pokemon["form"]
            data = [i + 1, form_id, pokemon_name]
            output.append(data)
        return output

    def output_pokemon_detail(self):
        """全ポケモンに対する、4種類のポケモンHOMEデータを出力する

        return:
            output_move:全ポケモンの技所持率に関するデータ詳細
            output_ability:全ポケモンの特性に関するデータ詳細
            output_item:全ポケモンのアイテム所持率に関するデータ詳細
            output_teratype:全ポケモンのテラスタイプに関するデータ詳細
        """
        output_move = []
        output_ability = []
        output_item = []
        output_teratype = []
        for i in range(1, 7):
            pokemon_all_detail = self.__fetch_pokemon_detail(i)
            move, ability, item, terastype = self.__parse_pokemon_detail(pokemon_all_detail)
            output_move.extend(move)
            output_ability.extend(ability)
            output_item.extend(item)
            output_teratype.extend(terastype)
        return output_move, output_ability, output_item, output_teratype


if __name__ == "__main__":
    pokemon = pokemon_home("./asset")
    pokemon.request_parameters_from_season_info(3, 0)
    move, ability, item, terastype = pokemon.output_pokemon_detail()
    pd.DataFrame(move, columns=["pokemon", "id", "form", "rank", "move", "raito"]).to_csv(
        "./output/move.csv",
        encoding="shift-jis",
    )
    pd.DataFrame(ability, columns=["pokemon", "id", "form", "rank", "ability", "raito"]).to_csv(
        "./output/ability.csv",
        encoding="shift-jis",
    )
    pd.DataFrame(item, columns=["pokemon", "id", "form", "rank", "item", "raito"]).to_csv(
        "./output/item.csv",
        encoding="shift-jis",
    )
    pd.DataFrame(terastype, columns=["pokemon", "id", "form", "rank", "tarastype", "raito"]).to_csv(
        "./output/terastype.csv",
        encoding="shift-jis",
    )
