from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Temporary storage (hackathon demo)
candidates = []
project_data = {}

# ---------------------------
# MATCHING LOGIC
# ---------------------------

def calculate_match_score(candidate, project):
    total_weight = sum(project["weights"].values())
    score = 0
    explanation = []

    for skill, weight in project["weights"].items():
        required = project["required_skills"].get(skill, 0)
        candidate_level = candidate["skills"].get(skill, 0)

        if required > 0:
            contribution = (candidate_level / required) * weight
        else:
            contribution = 0

        score += contribution

        if candidate_level >= required:
            explanation.append(f"Strong in {skill} ({candidate_level}/{required})")
        else:
            explanation.append(f"Needs improvement in {skill} ({candidate_level}/{required})")

    raw_score = round((score / total_weight) * 100, 2)

    # Fairness
    boost = 5 if candidate["background"] == "underrepresented" else 0
    final_score = min(raw_score + boost, 100)

    return raw_score, final_score, boost, explanation


# ---------------------------
# ROUTES
# ---------------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/student", methods=["GET", "POST"])
def student():
    if request.method == "POST":
        name = request.form["name"]
        python = int(request.form["python"])
        ml = int(request.form["ml"])
        sql = int(request.form["sql"])
        background = request.form["background"]

        candidates.append({
            "name": name,
            "skills": {"Python": python, "ML": ml, "SQL": sql},
            "background": background
        })

        return redirect(url_for("home"))

    return render_template("student.html")


@app.route("/recruiter", methods=["GET", "POST"])
def recruiter():
    global project_data

    if request.method == "POST":
        project_data = {
            "title": request.form["title"],
            "description": request.form["description"],
            "domain": request.form["domain"],
            "duration": request.form["duration"],
            "required_skills": {
                "Python": int(request.form["python"]),
                "ML": int(request.form["ml"]),
                "SQL": int(request.form["sql"])
            },
            "weights": {
                "Python": float(request.form["w_python"]),
                "ML": float(request.form["w_ml"]),
                "SQL": float(request.form["w_sql"])
            }
        }

        return redirect(url_for("home"))

    return render_template("recruiter.html")


@app.route("/dashboard")
def dashboard():
    if not project_data:
        return "Please upload project details first."

    if not candidates:
        return "No students added yet."

    results = []

    for candidate in candidates:
        raw, final, boost, explanation = calculate_match_score(candidate, project_data)

        results.append({
            "name": candidate["name"],
            "raw": raw,
            "final": final,
            "boost": boost,
            "explanation": explanation
        })

    results = sorted(results, key=lambda x: x["final"], reverse=True)

    return render_template("dashboard.html", results=results, project=project_data)


@app.route("/explanation/<name>")
def explanation(name):
    for candidate in candidates:
        if candidate["name"] == name:
            raw, final, boost, explanation = calculate_match_score(candidate, project_data)
            return render_template("explanation.html",
                                   name=name,
                                   raw=raw,
                                   final=final,
                                   boost=boost,
                                   explanation=explanation)

    return "Candidate not found"


if __name__ == "__main__":
    app.run(debug=True)
