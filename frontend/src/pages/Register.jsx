import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { registerUser } from "../services/api";

function Register() {

  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: ""
  });

  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

const handleSubmit = async (e) => {
  e.preventDefault();

  if (!formData.username || !formData.email || !formData.password) {
    setMessage("Please fill all fields.");
    return;
  }

  try {
    await registerUser(formData);

    setMessage("Registration successful!");

    setTimeout(() => {
      navigate("/login");
    }, 1000);

  } catch (error) {
    setMessage(error.message);
  }
};

  return (
    <div className="auth-page">

      <div className="auth-card">

        <h1>JobSkill Analyse</h1>

        <h2>Create Account</h2>

        <p className="auth-subtitle">
          Start extracting skills from job descriptions
        </p>

        <form onSubmit={handleSubmit}>

          <label>Username</label>

          <input
            type="text"
            name="username"
            placeholder="Enter username"
            value={formData.username}
            onChange={handleChange}
          />

          <label>Email</label>

          <input
            type="email"
            name="email"
            placeholder="Enter email"
            value={formData.email}
            onChange={handleChange}
          />

          <label>Password</label>

          <input
            type="password"
            name="password"
            placeholder="Enter password"
            value={formData.password}
            onChange={handleChange}
          />

          <button type="submit">
            Register
          </button>

        </form>

        {message && (
          <p className="message">{message}</p>
        )}

        <p className="auth-footer">
          Already have an account?
          <Link to="/login"> Login</Link>
        </p>

      </div>

    </div>
  );
}

export default Register;