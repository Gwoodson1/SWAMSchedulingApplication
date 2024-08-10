import React, { useState, useEffect } from 'react';
import api from '../api';
import { TextField, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';

const InstructorAPIComponent = () => {
  const [data, setData] = useState([]);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');  
  const [deleteUsername, setDeleteUsername] = useState('');
  const [updateUsername, setUpdateUsername] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [newName, setNewName] = useState(''); 
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get('/instructors');
        setData(response.data);
      } catch (error) {
        setError('Error fetching data');
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  const handleCreateInstructor = async () => {
    try {
      const newInstructor = { username, password, name, type: 'instructor' };
      const response = await api.post('/instructors', newInstructor);
      setData([...data, response.data]);
      setUsername('');
      setPassword('');
      setName('');
    } catch (error) {
      setError('Error creating instructor');
      console.error('Error creating instructor:', error);
    }
  };

  const handleDeleteInstructor = async () => {
    try {
      const response = await api.get(`/instructors/username/${deleteUsername}`);
      if (response.data && response.data.id) {
        await api.delete(`/instructors/${response.data.id}`);
        setData(data.filter(instructor => instructor.id !== response.data.id));
        setDeleteUsername('');
      } else {
        setError('Instructor not found');
      }
    } catch (error) {
      setError('Error deleting instructor');
      console.error('Error deleting instructor:', error);
    }
  };

  const handleUpdateInstructor = async () => {
    try {
      const updateData = {};
      if (newPassword) updateData.password = newPassword;
      if (newName) updateData.name = newName; 

      const response = await api.put(`/instructors/username/${updateUsername}`, updateData);
      setData(data.map(instructor => (instructor.id === response.data.id ? response.data : instructor)));
      setUpdateUsername('');
      setNewPassword('');
      setNewName(''); 
    } catch (error) {
      setError('Error updating instructor');
      console.error('Error updating instructor:', error);
    }
  };

  return (
    <div>
      <h1>Instructors</h1>
      {error && <p>{error}</p>}
      {data.length === 0 && !error ? (
        <p>No instructors available</p>
      ) : (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Username</TableCell>
                <TableCell>Name</TableCell>
                <TableCell>Lessons</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.map((instructor) => (
                <TableRow key={instructor.id}>
                  <TableCell>{instructor.username}</TableCell>
                  <TableCell>{instructor.name}</TableCell> 
                  <TableCell>{instructor.lessons.length}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      <div>
        <h2>Add Instructor</h2>
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
          label="Name"  // Add this line
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <Button variant="contained" color="primary" onClick={handleCreateInstructor}>
          Add Instructor
        </Button>
      </div>
      <div>
        <h2>Delete Instructor</h2>
        <TextField
          label="Username to delete"
          value={deleteUsername}
          onChange={(e) => setDeleteUsername(e.target.value)}
        />
        <Button variant="contained" color="secondary" onClick={handleDeleteInstructor}>
          Delete Instructor
        </Button>
      </div>
      <div>
        <h2>Update Instructor</h2>
        <TextField
          label="Username to update"
          value={updateUsername}
          onChange={(e) => setUpdateUsername(e.target.value)}
        />
        <TextField
          label="New Password"
          type="password"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
        />
        <TextField
          label="New Name" 
          value={newName}
          onChange={(e) => setNewName(e.target.value)}
        />
        <Button variant="contained" color="primary" onClick={handleUpdateInstructor}>
          Update Instructor
        </Button>
      </div>
    </div>
  );
};

export default InstructorAPIComponent;
