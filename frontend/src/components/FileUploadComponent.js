import React, { useState } from 'react';
import { Container, Typography, FormControl, InputLabel, Select, MenuItem, Button, TextField, Box } from '@mui/material';

function FileUploadComponent() {
  const [file, setFile] = useState(null);
  const [uploadType, setUploadType] = useState('swimmer');
  const [message, setMessage] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUploadTypeChange = (e) => {
    setUploadType(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) {
      setMessage('Please select a file to upload.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`http://localhost:5001/api/upload-${uploadType}s`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setMessage(`${uploadType.charAt(0).toUpperCase() + uploadType.slice(1)}s uploaded successfully!`);
      } else {
        setMessage(`Error: ${data.error}`);
      }
    } catch (error) {
      setMessage(`Error: ${error.message}`);
    }
  };

  return (
    <Container maxWidth="sm" style={styles.container}>
      <Typography variant="h4" align="center" gutterBottom>
        Upload Data
      </Typography>
      <form onSubmit={handleSubmit} style={styles.form}>
        <FormControl fullWidth margin="normal">
          <InputLabel shrink>Select Upload Type</InputLabel>
          <Select
            value={uploadType}
            onChange={handleUploadTypeChange}
            label="Select Upload Type"
          >
            <MenuItem value="swimmer">Swimmers</MenuItem>
            <MenuItem value="instructor">Instructors</MenuItem>
            <MenuItem value="previous-pairing">Previous Pairings</MenuItem> {/* New option */}
          </Select>
        </FormControl>
        <Box marginY={2}>
          <TextField
            type="file"
            fullWidth
            variant="outlined"
            onChange={handleFileChange}
            InputLabelProps={{
              shrink: true,
            }}
          />
        </Box>
        <Button
          type="submit"
          variant="contained"
          color="primary"
          fullWidth
          style={styles.button}
        >
          Upload
        </Button>
      </form>
      
      {message && (
        <Typography
          variant="body1"
          color={message.includes('Error') ? 'error' : 'success'}
          align="center"
          style={styles.message}
        >
          {message}
        </Typography>
      )}

      {/* New Note to Users */}
      <Typography variant="body2" align="center" style={{ marginTop: '20px', color: 'gray' }}>
        Please ensure that the swimmer spreadsheet is uploaded before the previous pairings spreadsheet.
      </Typography>
    </Container>
  );
}

const styles = {
  container: {
    marginTop: '50px',
    padding: '20px',
    borderRadius: '10px',
    boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)',
    backgroundColor: '#fff',
  },
  form: {
    marginTop: '20px',
  },
  button: {
    marginTop: '20px',
  },
  message: {
    marginTop: '20px',
  },
};

export default FileUploadComponent