import React, { useState, useEffect } from "react";
import axios from "axios";
import "../styles/AdminModelManager.css";
import { useNavigate } from "react-router-dom";

const AdminModelManager = () => {
  const [availableModels, setAvailableModels] = useState([]);
  const [availablePipelines, setAvailablePipelines] = useState([]);
  const [selectedModel, setSelectedModel] = useState("");
  const [selectedPipeline, setSelectedPipeline] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [redirectToPredict, setRedirectToPredict] = useState(false);
  const navigate = useNavigate();
  const API_KEY = "zu9gLCNscr8vlAKXqZ6zMH4bXIAfI43H";

  const modelPipelineMap = {
    "model1.keras": "pipeline1.pkl",
    "model2.keras": "pipeline2.pkl",
  };

  useEffect(() => {
    const fetchResources = async () => {
      try {
        const modelsResponse = await axios.get("http://localhost:5000/admin/models", {
          headers: {
            "Content-Type": "application/json",
            "x-api-key": API_KEY,
          },
        });

        const pipelinesResponse = await axios.get("http://localhost:5000/admin/pipelines", {
          headers: {
            "Content-Type": "application/json",
            "x-api-key": API_KEY,
          },
        });

        setAvailableModels(modelsResponse.data.available_models);
        setAvailablePipelines(pipelinesResponse.data.available_pipelines);
      } catch (err) {
        console.error("Error fetching resources:", err);
        setError("Failed to fetch resources. Please try again.");
      }
    };

    fetchResources();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    window.location.href = "/";
  };
  
  <button className="logout-button" onClick={handleLogout}>
    Logout
  </button>
  

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");
    setError("");
    setRedirectToPredict(false);

    const selectedPipeline = modelPipelineMap[selectedModel];

    try {
      const response = await axios.post(
        "http://localhost:5000/admin/change_model",
        {
          model_name: selectedModel,
          pipeline_name: selectedPipeline,
        },
        {
          headers: {
            "Content-Type": "application/json",
            "x-api-key": API_KEY,
          },
        }
      );
      setMessage(response.data.message);
      setRedirectToPredict(true);
    } catch (err) {
      console.error(err);
      setError("Failed to change model or pipeline.");
    }
  };

  const handleRedirect = () => {
    localStorage.setItem("chosen_model", selectedModel);
    navigate("/predict");
  };

  return (
    <div className="form-container">
      <h2 className="form-title">Admin Model Manager</h2>
      <p className="form-description">Manage models and pipelines for predictions.</p>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="model" className="form-label">Select Model</label>
          <select
            id="model"
            className="form-select"
            value={selectedModel}
            onChange={(e) => setSelectedModel(e.target.value)}
            required
          >
            <option value="">-- Select a Model --</option>
            {availableModels.map((model) => (
              <option key={model} value={model}>
                {model}
              </option>
            ))}
          </select>
        </div>

        {/* <div className="form-group">
          <label htmlFor="pipeline" className="form-label">Select Pipeline</label>
          <select
            id="pipeline"
            className="form-select"
            value={selectedPipeline}
            onChange={(e) => setSelectedPipeline(e.target.value)}
            required
          >
            <option value="">-- Select a Pipeline --</option>
            {availablePipelines.map((pipeline) => (
              <option key={pipeline} value={pipeline}>
                {pipeline}
              </option>
            ))}
          </select>
        </div> */}

        <button type="submit" className="form-button">
          Change Model and Pipeline
        </button>
      </form>

      {message && <div className="success-message">{message}</div>}
      {error && <div className="error-message">{error}</div>}

      {redirectToPredict && (
        <button onClick={handleRedirect} className="proceed-button">
          Proceed to Use the Model
        </button>
      )}
    </div>
  );
};

export default AdminModelManager;
