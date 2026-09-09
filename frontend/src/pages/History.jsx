import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import { getHistory } from "../services/api";

function History() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  useEffect(() => {
    const loadHistory = async () => {
      try {
        const data = await getHistory();

        setHistory(data.history || []);
      } catch (error) {
        setMessage(error.message);
      } finally {
        setLoading(false);
      }
    };

    loadHistory();
  }, []);

  return (
    <div className="dashboard">

      <Navbar />

      <main className="dashboard-content">

        <section className="welcome-section">

          <p className="small-title">
            ANALYSIS HISTORY
          </p>

          <h1>
            Your History
          </h1>

          <p>
            Your previous job skill analyses will appear here.
          </p>

        </section>

        {loading && (
          <div className="empty-history">
            <h2>Loading history...</h2>
          </div>
        )}

        {!loading && message && (
          <div className="empty-history">
            <h2>{message}</h2>
          </div>
        )}

        {!loading && !message && history.length === 0 && (
          <div className="empty-history">

            <h2>
              No analysis history yet
            </h2>

            <p>
              Analyze your first job description from the dashboard.
            </p>

          </div>
        )}

        {!loading && !message && history.length > 0 && (
          <div className="history-list">

            {history.map((item) => (

              <div
                className="history-card"
                key={item.id}
              >

                <div className="history-header">

                  <span>
                    Analysis #{item.id}
                  </span>

                  <span>
                    {item.created_at}
                  </span>

                </div>

                <div className="history-description">

                  <h3>
                    Job Description
                  </h3>

                  <p>
                    {item.job_description}
                  </p>

                </div>

                <div className="history-skills">

                  <h3>
                    Detected Skills
                  </h3>

                  <div className="skill-list">

                    {item.skills.map((skill, index) => (

                      <div
                        className="history-skill"
                        key={index}
                      >

                        <strong>
                          {skill.skill}
                        </strong>

                        <span>
                          {skill.category}
                        </span>

                      </div>

                    ))}

                  </div>

                </div>

              </div>

            ))}

          </div>
        )}

      </main>

    </div>
  );
}

export default History;