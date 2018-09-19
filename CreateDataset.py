from ChefRequest import makeRequest
import json
import time
import csv

response = makeRequest("GET", "https://api.codechef.com/tags/problems").json()
tags_dict = response.get("result", {}).get("data", {}).get("content", {})

tags = []

for key, value in tags_dict.items():

    if value.get("type", "") == "tag" and value.get("count", 0) > 10:
        tags.append(value.get("tag", ""))

problems = {}

for tag in tags:

    response = makeRequest(
        "GET", "https://api.codechef.com/tags/problems/?filter=" + tag).json()

    problems_dict = response.get("result", {}).get(
        "data", {}).get("content", {})

    problems.update(problems_dict)
    # To make sure that only 30 api calls are made in five minutes .....
    print(tag)
    time.sleep(10)

problems_list = []

for key, value in problems.items():
    problems_list.append(value)

csv_columns = ["code", "tags", "author",
               "solved", "attempted", "partiallySolved"]

csv_file = "problem_data.csv"

try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in problems_list:
            writer.writerow(data)
except IOError:
    print("I/O error")
