import requests
import json

url = "https://api.battle.pokemon-home.com/tt/cbd/competition/rankmatch/list"
header = {}
data = {"soft": "Sc"}

res = requests.post(url, headers=header, json=data)
response_json = json.loads(res.text)


def get_requirement_parameter(
    response: dict, season_number: int, rule: int
) -> dict[str, int, int, int]:
    """リクエストに必要なパラメータを取得する

    param:
        response:ランクバトルの情報リストのdictデータ
        season_number:シーズン番号
        rule:シングルは1。ダブルは2を記入
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


print(get_requirement_parameter(response_json, 2, 0))
