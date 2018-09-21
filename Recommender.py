import sys
import pandas as pd
import csv
from ChefRequest import makeRequest
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

starter_problems = {
    "0": "CHCHCL",
    "1": "TEST",
    "2": "INTEST",
    "3": "TSORT",
    "4": "FCTRL2",
    "5": "ATM",
    "6": "LADDU",
    "7": "START01",
    "8": "AMR15A",
    "9": "RNDPAIR"
}


def create_soup(x):
    return x["tags"] + ' ' + x["author"]


csv_file = "problem_data.csv"
metadata = pd.read_csv(csv_file, low_memory=False)

# Create a new soup feature
metadata["soup"] = metadata.apply(create_soup, axis=1)

count = CountVectorizer(stop_words="english")
count_matrix = count.fit_transform(metadata["soup"])

cosine_sim = cosine_similarity(count_matrix, count_matrix)

metadata = metadata.reset_index()
indices = pd.Series(metadata.index, index=metadata["code"])


def getRecommendations(code="", contestCode="", cosine_sim=cosine_sim):
    # Get the index of the problem that matches the problem code

    global metadata, count, count_matrix, indices

    if not code:
        return starter_problems

    idx = indices.get(code, -1)

    if idx == -1:
        response = makeRequest(
            "GET", "https://api.codechef.com/contests/" + contestCode + "/problems/" + code).json()

        problem_dict = response.get("result", {}).get(
            "data", {}).get("content", {})

        data_dict = {}
        data_dict["code"] = problem_dict.get("problemCode", "")
        data_dict["tags"] = problem_dict.get("tags", [])
        data_dict["author"] = problem_dict.get("author", "")
        data_dict["solved"] = problem_dict.get("successfulSubmissions", 0)
        data_dict["attempted"] = problem_dict.get("totalSubmissions", 0)
        data_dict["partiallySolved"] = problem_dict.get("partialSubmissions")

        csv_columns = ["code", "tags", "author",
                       "solved", "attempted", "partiallySolved"]

        try:
            with open(csv_file, 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writerow(data_dict)
        except IOError:
            print("I/O error")

        metadata = pd.read_csv(csv_file, low_memory=False)

        # Create a new soup feature
        metadata["soup"] = metadata.apply(create_soup, axis=1)

        count = CountVectorizer(stop_words="english")
        count_matrix = count.fit_transform(metadata["soup"])

        cosine_sim = cosine_similarity(count_matrix, count_matrix)

        metadata = metadata.reset_index()

    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the problems based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar problems
    sim_scores = sim_scores[1:11]

    # Get the problem indices
    problem_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar problems
    return metadata["code"].iloc[problem_indices]


def recommendProblem(problem_code, contest_code):
    res = getRecommendations(code=problem_code, contestCode=contest_code)
    print(res)


if __name__ == '__main__':
    sys.exit(recommendProblem("JAGAM", "PRACTICE"))
