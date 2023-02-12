import requests
import json
from extract_season_data import get_requirement_parameter

url = (
    "https://resource.pokemon-home.com/battledata/ranking/scvi/{cid}/{rst}/{ts}/pokemon"
)
url_2 = "https://resource.pokemon-home.com/battledata/ranking/scvi/{cid}/{rst}/{ts}/pdetail-{num}"

parameters = get_requirement_parameter(3, 0)
response = requests.get(
    url.format(cid=parameters["cid"], rst=parameters["rst"], ts=parameters["ts2"])
)

response_detail = requests.get(
    url_2.format(
        cid=parameters["cid"], rst=parameters["rst"], ts=parameters["ts2"], num=1
    )
)


def save_json(content, file_name):
    with open(file_name, "w", encoding="utf8") as f:
        json.dump(content, f, indent=2, ensure_ascii=False)


save_json(json.loads(response.text), "./asset/sample/pokemon.json")
save_json(json.loads(response_detail.text), "./asset/sample/detail-1.json")
