import { useState } from "react";
import Navbar from "../components/Navbar";

import {
  extractSkills as extractSkillsAPI
} from "../services/api";


function Dashboard() {

  const username = localStorage.getItem("username");

  const [jobDescription, setJobDescription] = useState("");

  const [skills, setSkills] = useState([]);

  const [recommendations, setRecommendations] = useState([]);

  const [loading, setLoading] = useState(false);


  const extractSkills = async () => {

    if (!jobDescription.trim()) {

      alert("Please paste a job description.");

      return;
    }

    setLoading(true);

    try {

      const data = await extractSkillsAPI(
        jobDescription
      );

      // Detected skills
      setSkills(data.skills || []);

      // Recommended technologies
      setRecommendations(
        data.recommended_technologies || []
      );

    } catch (error) {

      alert(error.message);

    } finally {

      setLoading(false);
    }
  };


  return (

    <div className="dashboard">

      <Navbar />


      <main className="dashboard-content">


        {/* Welcome */}

        <section className="welcome-section">

          <p className="small-title">
            NLP-POWERED SKILL EXTRACTION
          </p>

          <h1>
            Welcome, {username} 👋
          </h1>

          <p>
            Extract, normalize and categorize skills
            from any job description.
          </p>

        </section>


        {/* Input */}

        <section className="input-section">

          <h2>
            Analyze Job Description
          </h2>

          <p>
            Paste a job description below and let
            JobSkill Analyzer detect the required skills.
          </p>


          <textarea

            placeholder="Example: Looking for Data Analyst with SQL, Python, Power BI and Excel experience..."

            value={jobDescription}

            onChange={(e) =>
              setJobDescription(e.target.value)
            }

          />


          <button

            className="extract-btn"

            onClick={extractSkills}

            disabled={loading}

          >

            {loading
              ? "Extracting..."
              : "Extract Skills"}

          </button>

        </section>


        {/* Results */}

        {skills.length > 0 && (

          <section className="results-section">


            {/* Detected Skills */}

            <h2>
              Detected Skills
            </h2>


            <div className="skills-grid">

              {skills.map((item, index) => (

                <div

                  className="skill-card"

                  key={index}

                >

                  <h3>
                    {item.skill}
                  </h3>

                  <span>
                    {item.category}
                  </span>

                </div>

              ))}

            </div>


            {/* Recommendations */}

            <div className="recommendation">

              <h2>
                Recommended Technologies
              </h2>


              <div className="recommendation-list">

                {recommendations.length > 0 ? (

                  recommendations.map(
                    (technology, index) => (

                      <div

                        className="recommended-item"

                        key={index}

                      >

                        {technology}

                      </div>

                    )
                  )

                ) : (

                  <p>
                    No recommendations available.
                  </p>

                )}

              </div>

            </div>


          </section>

        )}


      </main>

    </div>
  );
}


export default Dashboard;