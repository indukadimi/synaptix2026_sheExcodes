from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ---------------------------
# Matching Algorithm
# ---------------------------

def calculate_match_score(candidate, project):
    total_weight = sum(project["weights"].values())
    score = 0
    explanation = []

    for skill, weight in project["weights"].items():
        required_level = project["required_skills"].get(skill, 0)
        candidate_level = candidate["skills"].get(skill, 0)

        if required_level > 0:
            contribution = (candidate_level / required_level) * weight
        else:
            contribution = 0

        score += contribution

        if candidate_level >= required_level:
            explanation.append(f"Strong in {skill} ({candidate_level}/{required_level})")
        else:
            explanation.append(f"Needs improvement in {skill} ({candidate_level}/{required_level})")

    normalized_score = round((score / total_weight) * 100, 2)
    return normalized_score, explanation


def apply_fairness(score, candidate):
    fairness_boost = 0

    if candidate.get("background") == "underrepresented":
        fairness_boost = 5

    final_score = min(score + fairness_boost, 100)
    return final_score, fairness_boost


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/match", methods=["POST"])
def match():
    data = request.json
    candidates = data["candidates"]
    project = data["project"]

    results = []

    for candidate in candidates:
        raw_score, explanation = calculate_match_score(candidate, project)
        final_score, boost = apply_fairness(raw_score, candidate)

        results.append({
            "name": candidate["name"],
            "raw_score": raw_score,
            "final_score": final_score,
            "fairness_boost": boost,
            "explanation": explanation
        })

    ranked_results = sorted(results, key=lambda x: x["final_score"], reverse=True)
    return jsonify(ranked_results)


if __name__ == "__main__":
    app.run(debug=True)