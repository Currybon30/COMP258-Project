import React, { useState } from "react";
import axios from "axios";
import "./styles/StudentPersistenceForm.css";

const StudentPersistenceForm = () => {
  const [formData, setFormData] = useState({});
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post("http://127.0.0.1:5000/predict", formData);
      setResult(response.data);
    } catch (err) {
      setError("An error occurred. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="form-container">
      <h1>Student Persistence Predictor</h1>
      <form onSubmit={handleSubmit}>
        {/* Add your form inputs here */}
        <button type="submit" disabled={loading}>
          {loading ? "Predicting..." : "Predict"}
        </button>
      </form>
      {error && <div>{error}</div>}
      {result && <div>Prediction: {result.prediction}</div>}
    </div>
  );
};

export default StudentPersistenceForm;
