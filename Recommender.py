import sys
import pandas as pd
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


def getRecommendations(code, cosine_sim=cosine_sim):
    # Get the index of the problem that matches the problem code
    idx = indices.get(code, -1)

    if idx == -1:
        return starter_problems

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


def recommendProblem(problem_code):
    res = getRecommendations(problem_code)
    print(res)


if __name__ == '__main__':
    sys.exit(recommendProblem("DIRECTI"))
