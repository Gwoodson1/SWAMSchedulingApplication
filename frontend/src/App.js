import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Container, Typography, AppBar, Toolbar } from '@mui/material';
import ParentAPIComponent from './components/ParentAPIComponent';
import InstructorAPIComponent from './components/InstructorAPIComponent';
import SwimmerAPIComponent from './components/SwimmerAPIComponent';
import LessonAPIComponent from './components/LessonAPIComponent';
import FileUploadComponent from './components/FileUploadComponent';
import PairSwimmerInstructor from './components/PairSwimmerInstructor';
import ExportLessonData from './components/ExportLessonData';
import NavigationTabs from './components/NavigationTabs';
import WelcomePage from './components/WelcomePage'; 
import logo from './montreal.png'; 

function App() {
  return (
    <Router>
      <AppBar position="static">
        <Toolbar>
          <img src={logo} alt="Montreal Logo" style={{ height: '40px', marginRight: '10px' }} />
          <Typography variant="h6" style={{ flexGrow: 1 }}>
            Scheduling Application
          </Typography>
          <NavigationTabs />
        </Toolbar>
      </AppBar>
      <Container>
        <Routes>
          <Route path="/" element={<WelcomePage />} /> {/* Set WelcomePage as the default route */}
          <Route path="/pair" element={<PairSwimmerInstructor />} />  
          <Route path="/parents" element={<ParentAPIComponent />} />
          <Route path="/instructors" element={<InstructorAPIComponent />} />
          <Route path="/swimmers" element={<SwimmerAPIComponent />} />
          <Route path="/lessons" element={<LessonAPIComponent />} />
          <Route path="/fileUpload" element={<FileUploadComponent />} />
          <Route path="/export-lessons" element={<ExportLessonData />} />
        </Routes>
      </Container>
    </Router>
  );
}

export default App;