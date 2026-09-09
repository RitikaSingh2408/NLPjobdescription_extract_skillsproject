import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { loginUser } from "../services/api";
import { useAuth } from "../context/AuthContext";

function Login() {
  const navigate = useNavigate();

  const { login } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    setMessage("");

    if (!email || !password) {
      setMessage("Please enter email and password.");
      return;
    }

    try {
      const data = await loginUser({
        email,
        password,
      });

      /*
       Backend se:
       access_token
       username
       etc. aa raha hai
      */

      const userData = {
        id: data.user.id,
        username: data.user.username,
        email: data.user.email,
      };

      // AuthContext + localStorage
      login(userData, data.access_token);

      // Dashboard
      navigate("/dashboard", {
        replace: true,
      });

    } catch (error) {
      setMessage(error.message);
    }
  };

  return (
    <div className="auth-page">

      <div className="auth-card">

        <h1>JobSkill Analyse</h1>

        <h2>Welcome Back</h2>

        <p className="auth-subtitle">
          Login to continue
        </p>

        <form onSubmit={handleSubmit}>

          <label>Email</label>

          <input
            type="email"
            placeholder="Enter email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <label>Password</label>

          <input
            type="password"
            placeholder="Enter password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <button type="submit">
            Login
          </button>

        </form>

        {message && (
          <p className="message">
            {message}
          </p>
        )}

        <p className="auth-footer">
          Don't have an account?
          <Link to="/register">
            {" "}Register
          </Link>
        </p>

      </div>

    </div>
  );
}

export default Login;