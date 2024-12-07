import React from "react";
import { Navigate } from "react-router-dom";

const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem("token"); // Retrieve token from localStorage

  if (!token) {
    return <Navigate to="/" />; // Redirect to homepage if not logged in
  }

  return children; // Render protected component
};

export default ProtectedRoute;
