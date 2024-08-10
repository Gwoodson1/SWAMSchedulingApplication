import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Container, Typography, AppBar, Toolbar } from '@mui/material';
import ParentAPIComponent from './components/ParentAPIComponent';
import InstructorAPIComponent from './components/InstructorAPIComponent';
import SwimmerAPIComponent from './components/SwimmerAPIComponent';
import LessonAPIComponent from './components/LessonAPIComponent';

function App() {
  return (
    <Router>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6">SWAM Scheduling Application</Typography>
        </Toolbar>
      </AppBar>
      <Container>
        <Routes>
          <Route path="/parents" element={<ParentAPIComponent />} />
          <Route path="/instructors" element={<InstructorAPIComponent />} />
          <Route path="/swimmers" element={<SwimmerAPIComponent />} />
          <Route path="/lessons" element={<LessonAPIComponent />} />
        </Routes>
      </Container>
    </Router>
  );
}

export default App;
