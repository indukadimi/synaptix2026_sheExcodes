const API = "http://localhost:5000";

/* Add Candidate */
function addCandidate() {
  const data = {
    name: document.getElementById("name").value,
    skills: [
      {
        name: document.getElementById("skill1").value,
        level: parseInt(document.getElementById("level1").value),
      },
    ],
  };

  fetch(`${API}/add-candidate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  }).then((res) => alert("Candidate Added"));
}

/* Add Internship */
function addInternship() {
  const data = {
    id: document.getElementById("internId").value,
    title: document.getElementById("title").value,
    skills: [
      {
        name: document.getElementById("skillName").value,
        requiredLevel: parseInt(
          document.getElementById("requiredLevel").value
        ),
        weight: parseInt(document.getElementById("weight").value),
      },
    ],
  };

  fetch(`${API}/add-internship`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  }).then((res) => alert("Internship Added"));
}

/* Get Matches */
function getMatches() {
  const id = document.getElementById("matchId").value;

  fetch(`${API}/match/${id}`)
    .then((res) => res.json())
    .then((data) => {
      let html = "";

      data.forEach((candidate) => {
        html += `
          <div class="card">
            <h3>${candidate.name}</h3>
            <p><strong>Total Score:</strong> ${candidate.totalScore}</p>
            <h4>Breakdown:</h4>
            ${candidate.explanation
              .map(
                (e) =>
                  `<p>${e.skill}: ${e.score} (Weight: ${e.weight})</p>`
              )
              .join("")}
          </div>
        `;
      });

      document.getElementById("results").innerHTML = html;
    });
}
/* Load Candidates */
function loadCandidates() {
  fetch("http://localhost:5000/candidates")
    .then(res => res.json())
    .then(data => {
      let html = "";

      data.forEach(candidate => {
        html += `
          <div class="candidate-card">
            <h3>${candidate.name}</h3>
            <p>${candidate.degree || ""}</p>
            <div>
              ${candidate.skills.map(skill => `
                <span class="skill-badge">
                  ${skill.name} (Level ${skill.level})
                </span>
              `).join("")}
            </div>
          </div>
        `;
      });

      document.getElementById("candidateList").innerHTML = html;
    });
}

/* Add Candidate */
function addCandidate() {
  const data = {
    name: document.getElementById("name").value,
    degree: document.getElementById("degree").value,
    skills: [
      {
        name: document.getElementById("skill").value,
        level: parseInt(document.getElementById("level").value)
      }
    ]
  };

  fetch("http://localhost:5000/add-candidate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  })
  .then(res => res.json())
  .then(() => {
    loadCandidates();
    alert("Candidate Added Successfully!");
  });
}