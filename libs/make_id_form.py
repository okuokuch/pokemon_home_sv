import pandas as pd

data = pd.read_csv("./output/move.csv", encoding="shift-jis", index_col=0)
print(
    data[["id", "form", "pokemon"]]
    .drop_duplicates()
    .to_json("./output/id_form.json", orient="records", force_ascii=False)
)
