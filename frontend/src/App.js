import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./components/Login";
import AdminModelManager from "./components/AdminModelManager";
import StudentPersistenceForm from "./components/StudentPersistenceForm";
import ProtectedRoute from "./components/ProtectedRoute";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/predict" element={<StudentPersistenceForm />} />
        <Route
          path="/admin"
          element={
            <ProtectedRoute>
              <AdminModelManager />
            </ProtectedRoute>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
