import requests
import json
import pandas as pd


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
        self.NATURE = self.__read_json("{}/nature_names.json".format(folder_path))[language]
        self.TYPE = self.__read_json("{}/type_names.json".format(folder_path))[language]
        self.ITEM = self.__read_json("{}/ability_names.json".format(folder_path))

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

    def _fetch_requirement_parameter(self, season_number: int, rule: int, response: dict) -> dict[str, int, int, int]:
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
        url = "https://resource.pokemon-home.com/battledata/ranking/scvi/{cid}/{rst}/{ts}/pokemon"
        response = requests.get(url.format(cid=self.params["cid"], rst=self.params["rst"], ts=self.params["ts2"]))
        return json.loads(response.text)

    def output_pokemon_ranking(self):
        pokemon_ranking = self.__fetch_pokemon_ranking()
        output = []
        for i, pokemon in enumerate(pokemon_ranking):
            pokemon_name = self.POKEMON[pokemon["id"] - 1]
            form_id = pokemon["form"]
            data = [i + 1, pokemon_name, form_id]
            output.append(data)
        return output


if __name__ == "__main__":
    pokemon = pokemon_home("./asset")
    pokemon.request_parameters_from_season_info(3, 0)
    print(pd.DataFrame(pokemon.output_pokemon_ranking()))
