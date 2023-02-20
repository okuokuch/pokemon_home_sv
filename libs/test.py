import requests
import json

url = "https://resource.pokemon-home.com/battledata/json/itemname_ja.json"
response = requests.get(url)
response.encoding = response.apparent_encoding
response_text = response.text

url2 = "https://resource.pokemon-home.com/battledata/json/zkn_form_ja.json"
response2 = requests.get(url2)
response2.encoding = response2.apparent_encoding
response2_text = response2.text


def save_json(content, file_name):
    with open(file_name, "w", encoding="utf8") as f:
        json.dump(content, f, indent=2, ensure_ascii=False)


save_json(json.loads(response_text), "./asset/item_names.json")
save_json(json.loads(response2_text), "./asset/form_names.json")
