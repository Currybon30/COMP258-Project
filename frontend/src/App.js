import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import StudentPersistenceForm from "./components/StudentPersistenceForm";
import AdminModelManager from "./components/AdminModelManager";

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/predict" element={<StudentPersistenceForm />} />
        <Route path="/admin" element={<AdminModelManager />} />
      </Routes>
    </Router>
  );
};

export default App;
