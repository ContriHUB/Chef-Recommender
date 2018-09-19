from flask import abort
from flask import Flask
from flask import jsonify
from flask import make_response
from flask import request

from Recommender import getRecommendations
from ChefRequest import makeRequest

app = Flask(__name__)


@app.route("/")
def recommenderApp():
    return "Hello World!"


@app.route("/api/recommend/problem/<string:code>", methods=['GET'])
def problemRecommenderApi(code):

    res = getRecommendations(code)
    recommended_problem = []

    for key, value in res.items():
        recommended_problem.append(value)

    return jsonify({"recommendedProblems": recommended_problem}), 201


@app.route("/api/recommend/user/<string:username>", methods=['GET'])
def recommenderApi(username):

    response = makeRequest(
        "GET", "https://api.codechef.com/submissions/?username=" + username + "&limit=20").json()

    submission_list = response.get("result", {}).get(
        "data", {}).get("content", {})

    recent_problem = set()

    for submission in submission_list:
        recent_problem.add([submission.get("problemCode"), submission.get("contestCode")])

    if not recent_problem:
        recent_problem.add("")

    response = makeRequest(
        "GET", "https://api.codechef.com/users/" + username + "?fields=problemStats").json()

    problem_dict = response.get("result", {}).get(
        "data", {}).get("content", {}).get("problemStats", {}).get("solved", {})

    all_problem = set()

    for key, value in problem_dict.items():
        for problem in value:
            all_problem.add(problem)

    recommended_problem = set()

    for problem in recent_problem:
        res = getRecommendations(code=problem[0], problemCode=problem[1])
        for key, value in res.items():
            recommended_problem.add(value)

    recommended_problem = recommended_problem.difference(all_problem)
    recommended_problem = list(recommended_problem)

    return jsonify({"recommendedProblems": recommended_problem}), 201


@app.errorhandler(404)
def notFound(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)
