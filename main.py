from xkom import xkom_finder
from morele import morele_finder

import csv

user_agent = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/100.0.4896.127 Safari/537.36 OPR/86.0.4363.70 ",
}

search_terms = "iphone 12 128gb"


print("MORELE.NET")
for index, item in enumerate(morele_finder(search_terms, user_agent)):
    print(index)
    for k, v in item.items():
        print(f"{k} : {v}")

print("X-KOM.PL")
for index, item in enumerate(xkom_finder(search_terms, user_agent)):
    print(index)
    for k, v in item.items():
        print(f"{k} : {v}")

