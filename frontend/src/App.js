import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Container, Typography, AppBar, Toolbar } from '@mui/material';
import ExampleComponent from './components/ExampleComponent';

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
          <Route path="/example" element={<ExampleComponent />} />
          {/* Add more routes as needed */}
        </Routes>
      </Container>
    </Router>
  );
}

export default App;