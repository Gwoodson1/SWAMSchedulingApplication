import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Container, Typography, AppBar, Toolbar } from '@mui/material';
import ParentAPIComponent from './components/ParentAPIComponent';

function App() {
  return (
    <Router>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6">Swam Scheduling Application</Typography>
        </Toolbar>
      </AppBar>
      <Container>
        <Routes>
          <Route path="/parents" element={<ParentAPIComponent />} />
          {/* Add more routes as needed */}
        </Routes>
      </Container>
    </Router>
  );
}

export default App;