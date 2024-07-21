import React, { useState, useEffect } from 'react';
import api from '../api';
import { TextField, Button } from '@mui/material';

const ExampleComponent = () => {
  const [data, setData] = useState([]);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');  // Adding name field
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get('/parents');
        setData(response.data);
      } catch (error) {
        setError('Error fetching data');
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  const handleCreateParent = async () => {
    try {
      const newParent = { username, password, name, type: 'parent' };
      const response = await api.post('/parents', newParent);
      setData([...data, response.data]);
      setUsername('');
      setPassword('');
      setName('');  // Reset name field
    } catch (error) {
      setError('Error creating parent');
      console.error('Error creating parent:', error);
    }
  };

  return (
    <div>
      <h1>Parents</h1>
      {error && <p>{error}</p>}
      {data.length === 0 && !error ? (
        <p>No parents available</p>
      ) : (
        <ul>
          {data.map((parent) => (
            <li key={parent.id}>{parent.username}</li>
          ))}
        </ul>
      )}
      <div>
        <TextField
          label="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <TextField
          label="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <TextField
          label="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <Button variant="contained" color="primary" onClick={handleCreateParent}>
          Add Parent
        </Button>
      </div>
    </div>
  );
};

export default ExampleComponent;
