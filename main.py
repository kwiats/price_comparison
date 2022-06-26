from xkom import xkom_finder
from morele import morele_finder
import pandas as pd

user_agent = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/100.0.4896.127 Safari/537.36 OPR/86.0.4363.70 ",
}

search_terms = "laptop macbook air m1 8gb"

print("MORELE.NET")
morele_data = morele_finder(search_terms, user_agent)
# for index, item in enumerate(morele_data):
#     print(index)
#     for k, v in item.items():
#         print(f"{k} : {v}")

print("X-KOM.PL")
xkom_data = xkom_finder(search_terms, user_agent)
# for index, item in enumerate(xkom_data):
#     print(index)
#     for k, v in item.items():
#         print(f"{k} : {v}")

md = pd.DataFrame.from_dict(morele_data)
xkd = pd.DataFrame.from_dict(xkom_data)
frames = [md, xkd]
result = pd.concat(frames)
result.to_csv(r'data\data.csv', index=False, header=True)
