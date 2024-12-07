import React, { useState, useEffect } from "react";
import axios from "axios";
import "./styles/AdminModelManager.css";

const AdminModelManager = () => {
  const [availableModels, setAvailableModels] = useState([]);
  const [availablePipelines, setAvailablePipelines] = useState([]);
  const [selectedModel, setSelectedModel] = useState("");
  const [selectedPipeline, setSelectedPipeline] = useState("");
  const [message, setMessage] = useState("");

  useEffect(() => {
    const fetchResources = async () => {
      try {
        const models = await axios.get("http://127.0.0.1:5000/admin/models");
        const pipelines = await axios.get("http://127.0.0.1:5000/admin/pipelines");
        setAvailableModels(models.data.available_models);
        setAvailablePipelines(pipelines.data.available_pipelines);
      } catch (err) {
        console.error(err);
      }
    };
    fetchResources();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:5000/admin/change_model", {
        model_name: selectedModel,
        pipeline_name: selectedPipeline,
      });
      setMessage(response.data.message);
    } catch (err) {
      console.error(err);
      setMessage("Failed to change model or pipeline.");
    }
  };

  return (
    <div>
      <h1>Admin Model Manager</h1>
      <form onSubmit={handleSubmit}>
        <select onChange={(e) => setSelectedModel(e.target.value)}>
          <option>-- Select Model --</option>
          {availableModels.map((model) => (
            <option key={model}>{model}</option>
          ))}
        </select>
        <select onChange={(e) => setSelectedPipeline(e.target.value)}>
          <option>-- Select Pipeline --</option>
          {availablePipelines.map((pipeline) => (
            <option key={pipeline}>{pipeline}</option>
          ))}
        </select>
        <button type="submit">Change Model and Pipeline</button>
      </form>
      {message && <div>{message}</div>}
    </div>
  );
};

export default AdminModelManager;
