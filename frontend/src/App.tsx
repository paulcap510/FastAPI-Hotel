import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import Register from './components/Register';
import RoomTypes from './components/RoomTypes';

const App: React.FC = () => {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Register />} />
        <Route path="/room-types" element={<RoomTypes />} />
      </Routes>
    </Router>
  );
};

export default App;
