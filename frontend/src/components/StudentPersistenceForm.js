import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/StudentPersistenceForm.css';
import { useNavigate } from 'react-router-dom';

const StudentPersistenceForm = () => {
  const [formData, setFormData] = useState({
    firstTermGpa: '',
    secondTermGpa: '',
    firstLanguage: '',
    funding: '',
    fastTrack: '',
    coop: '',
    residency: '',
    gender: '',
    prevEducation: '',
    ageGroup: '',
    highSchoolAverage: '',
    mathScore: '',
    englishGrade: ''
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [chosenModel, setChosenModel] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const model = localStorage.getItem("chosen_model");
    setChosenModel(model);
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    
    setFormData((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

    // Handle logout functionality
    const handleLogout = () => {
      localStorage.removeItem("token"); // Remove the saved token
      localStorage.removeItem("username"); // Optional: Clear saved username
      navigate("/"); // Redirect back to the login page
    };
  

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);
  
    const adjustedFormData =
    chosenModel === "model2.keras"
      ? {
          "1st Term GPA": formData.firstTermGpa ? parseFloat(formData.firstTermGpa) : 0.0,
          "High School Average Mark": formData.highSchoolAverage ? parseFloat(formData.highSchoolAverage) : 0.0,
          "Math Score": formData.mathScore ? parseFloat(formData.mathScore) : 0.0,
        }
      : {
          "1st Term GPA": formData.firstTermGpa ? parseFloat(formData.firstTermGpa) : 0.0,
          "2nd Term GPA": formData.secondTermGpa ? parseFloat(formData.secondTermGpa) : 0.0,
          "First Language": parseInt(formData.firstLanguage) || 0,
          "Funding": parseInt(formData.funding) || 0,
          "Fast Track": parseInt(formData.fastTrack) || 0,
          "Coop": parseInt(formData.coop) || 0,
          "Residency": parseInt(formData.residency) || 0,
          "Gender": parseInt(formData.gender) || 0,
          "Prev Education": parseInt(formData.prevEducation) || 0,
          "Age Group": parseInt(formData.ageGroup) || 0,
          "High School Average Mark": formData.highSchoolAverage ? parseFloat(formData.highSchoolAverage) : 0.0,
          "Math Score": formData.mathScore ? parseFloat(formData.mathScore) : 0.0,
          "English Grade": parseInt(formData.englishGrade) || 0,
        };

  
    try {
      console.log('Adjusted form data:', adjustedFormData);
      const response = await axios.post('http://localhost:5000/predict', adjustedFormData, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
      setResult(response.data);
    } catch (err) {
      if (err.response) {
        setError(`Error: ${err.response.status} - ${err.response.data.error || 'Unknown error'}`);
      } else {
        setError('Network error: Unable to connect to the server.');
      }
      console.error('Prediction error:', err);
    } finally {
      setLoading(false);
    }
  };
    
  const isDisabled = (field) => {
    return (
      chosenModel === "model2.keras" &&
      !["firstTermGpa", "highSchoolAverage", "mathScore"].includes(field)
    );
  };

  return (
    <div className="form-container">
      {/* Logout Button */}
      <button className="logout-button" onClick={handleLogout}>
        Logout
      </button>
      <h2 className="form-title">
        {localStorage.getItem("chosen_model") === "model2.keras"
          ? "Student's Predicted GPA"
          : "Student Persistence Predictor"}
      </h2>
      <p className="form-description">
        {localStorage.getItem("chosen_model") === "model2.keras"
          ? "Enter student information to predict GPA."
          : "Enter student information to predict persistence."}
      </p>
      <form onSubmit={handleSubmit}>
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="firstTermGpa" className="form-label">First Term GPA</label>
            <input
              type="number"
              id="firstTermGpa"
              name="firstTermGpa"
              value={formData.firstTermGpa}
              disabled={isDisabled("firstTermGpa")}
              onChange={handleChange}
              min="0.0"
              max="4.5"
              step="0.1"
              required
              className="form-input"
            />
          </div>
          <div className="form-group">
            <label htmlFor="secondTermGpa" className="form-label">Second Term GPA</label>
            <input
              type="number"
              id="secondTermGpa"
              name="secondTermGpa"
              value={formData.secondTermGpa}
              onChange={handleChange}
              disabled={isDisabled("secondTermGpa")}
              min="0"
              max="4.5"
              step="any"
              required
              className="form-input"
            />
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="firstLanguage" className="form-label">First Language</label>
          <select
            name="firstLanguage"
            value={formData.firstLanguage}
            onChange={handleChange}
            disabled={isDisabled("firstLanguage")}
            required
            className="form-select"
          >
            <option value="">Select first language</option>
            <option value="1">English</option>
            <option value="2">French</option>
            <option value="3">Other</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="funding" className="form-label">Funding</label>
          <select
            name="funding"
            value={formData.funding}
            onChange={handleChange}
            disabled={isDisabled("funding")}
            required
            className="form-select"
          >
            <option value="">Select funding type</option>
            <option value="1">Apprentice_PS</option>
            <option value="2">GPOG_FT</option>
            <option value="3">Intl Offshore</option>
            <option value="4">Intl Regular</option>
            <option value="5">Intl Transfer</option>
            <option value="6">Joint Program Ryerson</option>
            <option value="7">Joint Program UTSC</option>
            <option value="8">Second Career Program</option>
            <option value="9">Work Safety Insurance Board</option>
          </select>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="fastTrack" className="form-label">Fast Track</label>
            <select
              name="fastTrack"
              value={formData.fastTrack}
              onChange={handleChange}
              disabled={isDisabled("fastTrack")}
              required
              className="form-select"
            >
              <option value="">Select option</option>
              <option value="1">Yes</option>
              <option value="2">No</option>
            </select>
          </div>
          <div className="form-group">
            <label htmlFor="coop" className="form-label">Co-op</label>
            <select
              name="coop"
              value={formData.coop}
              onChange={handleChange}
              disabled={isDisabled("coop")}
              required
              className="form-select"
            >
              <option value="">Select option</option>
              <option value="1">Yes</option>
              <option value="2">No</option>
            </select>
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="residency" className="form-label">Residency</label>
            <select
              name="residency"
              value={formData.residency}
              onChange={handleChange}
              disabled={isDisabled("residency")}
              required
              className="form-select"
            >
              <option value="">Select residency</option>
              <option value="1">Domestic</option>
              <option value="2">International</option>
            </select>
          </div>
          <div className="form-group">
            <label htmlFor="gender" className="form-label">Gender</label>
            <select
              name="gender"
              value={formData.gender}
              onChange={handleChange}
              disabled={isDisabled("gender")}
              required
              className="form-select"
            >
              <option value="">Select gender</option>
              <option value="1">Female</option>
              <option value="2">Male</option>
              <option value="3">Neutral</option>
            </select>
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="prevEducation" className="form-label">Previous Education</label>
          <select
            name="prevEducation"
            value={formData.prevEducation}
            onChange={handleChange}
            disabled={isDisabled("prevEducation")}
            required
            className="form-select"
          >
            <option value="">Select previous education</option>
            <option value="1">High School</option>
            <option value="2">Post Secondary</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="ageGroup" className="form-label">Age Group</label>
          <select
            name="ageGroup"
            value={formData.ageGroup}
            onChange={handleChange}
            disabled={isDisabled("ageGroup")}
            required
            className="form-select"
          >
            <option value="">Select age group</option>
            <option value="1">0 to 18</option>
            <option value="2">19 to 20</option>
            <option value="3">21 to 25</option>
            <option value="4">26 to 30</option>
            <option value="5">31 to 35</option>
            <option value="6">36 to 40</option>
            <option value="7">41 to 50</option>
            <option value="8">51 to 60</option>
            <option value="9">61 to 65</option>
            <option value="10">66+</option>
          </select>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="highSchoolAverage" className="form-label">High School Average Mark</label>
            <input
              type="number"
              id="highSchoolAverage"
              name="highSchoolAverage"
              value={formData.highSchoolAverage}
              onChange={handleChange}
              disabled={isDisabled("highSchoolAverage")}
              min="0"
              max="100"
              step="0.1"
              required
              className="form-input"
            />
          </div>
          <div className="form-group">
            <label htmlFor="mathScore" className="form-label">Math Score</label>
            <input
              type="number"
              id="mathScore"
              name="mathScore"
              value={formData.mathScore}
              onChange={handleChange}
              disabled={isDisabled("mathScore")}
              min="0"
              max="50"
              step="0.1"
              required
              className="form-input"
            />
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="englishGrade" className="form-label">English Grade</label>
          <select
            name="englishGrade"
            value={formData.englishGrade}
            onChange={handleChange}
            disabled={isDisabled("englishGrade")}
            required
            className="form-select"
          >
            <option value="">Select English grade</option>
            <option value="1">Level-130</option>
            <option value="2">Level-131</option>
            <option value="3">Level-140</option>
            <option value="4">Level-141</option>
            <option value="5">Level-150</option>
            <option value="6">Level-151</option>
            <option value="7">Level-160</option>
            <option value="8">Level-161</option>
            <option value="9">Level-170</option>
            <option value="10">Level-171</option>
            <option value="11">Level-180</option>
          </select>
        </div>

        <button
          type="submit"
          className="form-button"
          disabled={loading}
        >
          {loading ? 'Predicting...' : 'Predict'}
        </button>
      </form>

      {error && (
        <div className="error-message">
          <strong>Error:</strong> {error}
        </div>
      )}

      {result && (
        <div
          className={`result-message ${
            result.persist ? 'result-persist' : 'result-not-persist'
          }`}
        >
          <strong>Prediction Result:</strong>
          <p>
            {localStorage.getItem("chosen_model") !== "model2.keras" && (
              <>
                The student is predicted to {result.persist ? 'persist' : 'not persist'}.
                <br />
              </>
            )}
            {localStorage.getItem("chosen_model") === "model2.keras"
              ? `Student's predicted 2nd Term GPA: ${(result.confidence).toFixed(2)}`
              : `Confidence: ${(result.confidence * 100).toFixed(2)}%`}
          </p>
        </div>
      )}


    </div>
  );
};

export default StudentPersistenceForm;

