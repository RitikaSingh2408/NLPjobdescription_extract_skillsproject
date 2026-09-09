import Navbar from "../components/Navbar";

function Profile() {

  const username = localStorage.getItem("username");

  return (

    <div className="dashboard">

      <Navbar />

      <main className="dashboard-content">

        <section className="welcome-section">

          <p className="small-title">
            USER PROFILE
          </p>

          <h1>
            My Profile
          </h1>

        </section>

        <div className="profile-card">

          <h2>
            {username}
          </h2>

          <p>
            Job Skill Analytics User
          </p>

        </div>

      </main>

    </div>

  );
}

export default Profile;