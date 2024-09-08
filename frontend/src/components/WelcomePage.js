import React from 'react';
import { Typography, Box, Paper, Button } from '@mui/material';
import { Link } from 'react-router-dom';

const WelcomePage = () => {
  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      height="100vh"
      textAlign="center"
      bgcolor="#f0f4f8"
      padding={4}
    >
      <Paper elevation={3} style={{ padding: '40px', maxWidth: '600px', width: '100%' }}>
        <Typography variant="h3" gutterBottom style={{ color: '#1976d2' }}>
          Welcome to SWAM Scheduling!
        </Typography>
        <Typography variant="h5" gutterBottom style={{ marginBottom: '20px' }}>
          Streamline your swim lesson scheduling process.
        </Typography>
        <Typography variant="body1" paragraph>
          This application allows you to:
        </Typography>
        <Typography variant="body1" component="ul" align="left" style={{ marginLeft: '20px', marginBottom: '20px' }}>
        <li>Upload swimmer and instructor data through CSV or Excel files.</li>
          <li>Pair swimmers with instructors based on preferences and experience.</li>
          <li>Manage parents, swimmers, instructors, and lessons manually through the Management tab.</li>
          <li>Export lesson schedules to Excel for easy sharing and record-keeping.</li>
        </Typography>
        <Typography variant="body1" paragraph>
          Use the navigation bar at the top to get started.
        </Typography>
        <Typography variant="body1" paragraph>
          We hope this tool makes managing your swim lessons simpler and more efficient!
        </Typography>
        <Button
          variant="contained"
          color="primary"
          component={Link}
          to="/FileUpload"
          style={{ marginTop: '20px' }}
        >
          Get Started
        </Button>
      </Paper>
    </Box>
  );
};

export default WelcomePage;