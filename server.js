const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(bodyParser.json());
app.use(express.static("public"));

let candidates = [];
let internships = [];

/* -------------------------
   Add Candidate
--------------------------*/
app.post("/add-candidate", (req, res) => {
  const candidate = req.body;
  candidates.push(candidate);
  res.json({ message: "Candidate added successfully" });
});

/* -------------------------
   Add Internship
--------------------------*/
app.post("/add-internship", (req, res) => {
  const internship = req.body;
  internships.push(internship);
  res.json({ message: "Internship added successfully" });
});

/* -------------------------
   Match Logic
--------------------------*/
app.get("/match/:internshipId", (req, res) => {
  const internship = internships.find(
    (i) => i.id == req.params.internshipId
  );

  if (!internship) {
    return res.status(404).json({ message: "Internship not found" });
  }

  let results = candidates.map((candidate) => {
    let totalScore = 0;
    let explanation = [];

    internship.skills.forEach((skillReq) => {
      const candidateSkill = candidate.skills.find(
        (s) => s.name === skillReq.name
      );

      if (candidateSkill) {
        let levelScore = Math.min(
          candidateSkill.level / skillReq.requiredLevel,
          1
        );

        let weightedScore = levelScore * skillReq.weight;
        totalScore += weightedScore;

        explanation.push({
          skill: skillReq.name,
          weight: skillReq.weight,
          candidateLevel: candidateSkill.level,
          requiredLevel: skillReq.requiredLevel,
          score: weightedScore.toFixed(2),
        });
      } else {
        explanation.push({
          skill: skillReq.name,
          weight: skillReq.weight,
          candidateLevel: 0,
          requiredLevel: skillReq.requiredLevel,
          score: 0,
        });
      }
    });

    return {
      name: candidate.name,
      totalScore: totalScore.toFixed(2),
      explanation,
    };
  });

  results.sort((a, b) => b.totalScore - a.totalScore);

  res.json(results);
});

app.listen(5000, () => console.log("Server running on port 5000"));