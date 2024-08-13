import React, { useState, useEffect } from 'react';
import api from '../api';
import { TextField, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';

const InstructorAPIComponent = () => {
  const [data, setData] = useState([]);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');  
  const [lessonIds, setLessonIds] = useState(''); // State for lesson IDs
  const [deleteUsername, setDeleteUsername] = useState('');
  const [updateUsername, setUpdateUsername] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [newName, setNewName] = useState(''); 
  const [newLessonIds, setNewLessonIds] = useState(''); // State for updated lesson IDs
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get('/instructors');
        const instructors = response.data.map(instructor => ({
          ...instructor,
          lessons: instructor.lessons || [] // Ensure lessons is always an array
        }));
        setData(instructors);
      } catch (error) {
        setError('Error fetching data');
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  const handleCreateInstructor = async () => {
    if (!username || !password || !name) {
      setError('Username, Password, and Name are required');
      return;
    }

    try {
      const newInstructor = { 
        username, 
        password, 
        name, 
        type: 'instructor',
        lesson_ids: lessonIds ? lessonIds.split(',').map(id => parseInt(id.trim())) : [] // Handle multiple lessons
      };
      const response = await api.post('/instructors', newInstructor);
      setData([...data, { ...response.data, lessons: response.data.lessons || [] }]);
      setUsername('');
      setPassword('');
      setName('');
      setLessonIds('');
      setError(null);
    } catch (error) {
      setError('Error creating instructor');
      console.error('Error creating instructor:', error);
    }
  };

  const handleDeleteInstructor = async () => {
    if (!deleteUsername) {
      setError('Username is required to delete');
      return;
    }

    try {
      const response = await api.get(`/instructors/username/${deleteUsername}`);
      if (response.data && response.data.id) {
        await api.delete(`/instructors/${response.data.id}`);
        setData(data.filter(instructor => instructor.id !== response.data.id));
        setDeleteUsername('');
        setError(null);
      } else {
        setError('Instructor not found');
      }
    } catch (error) {
      setError('Error deleting instructor');
      console.error('Error deleting instructor:', error);
    }
  };

  const handleUpdateInstructor = async () => {
    if (!updateUsername) {
      setError('Username is required to update');
      return;
    }

    try {
      const updateData = {};
      if (newPassword) updateData.password = newPassword;
      if (newName) updateData.name = newName; 
      if (newLessonIds) updateData.lesson_ids = newLessonIds.split(',').map(id => parseInt(id.trim())); // Handle multiple lessons

      const response = await api.put(`/instructors/username/${updateUsername}`, updateData);
      setData(data.map(instructor => 
        instructor.id === response.data.id 
          ? { ...response.data, lessons: response.data.lessons || [] } // Ensure lessons array is handled safely
          : instructor
      ));
      setUpdateUsername('');
      setNewPassword('');
      setNewName(''); 
      setNewLessonIds('');
      setError(null);
    } catch (error) {
      setError('Error updating instructor');
      console.error('Error updating instructor:', error);
    }
  };

  return (
    <div>
      <h1>Instructors</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {data.length === 0 && !error ? (
        <p>No instructors available</p>
      ) : (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>ID</TableCell>
                <TableCell>Username</TableCell>
                <TableCell>Name</TableCell>
                <TableCell>Lesson IDs</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.map((instructor) => (
                <TableRow key={instructor.id}>
                  <TableCell>{instructor.id}</TableCell>
                  <TableCell>{instructor.username}</TableCell>
                  <TableCell>{instructor.name}</TableCell> 
                  <TableCell>{(instructor.lessons || []).join(', ')}</TableCell>
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
          label="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <TextField
          label="Lesson IDs (comma-separated)"
          value={lessonIds}
          onChange={(e) => setLessonIds(e.target.value)}
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
        <TextField
          label="New Lesson IDs (comma-separated)"
          value={newLessonIds}
          onChange={(e) => setNewLessonIds(e.target.value)}
        />
        <Button variant="contained" color="primary" onClick={handleUpdateInstructor}>
          Update Instructor
        </Button>
      </div>
    </div>
  );
};

export default InstructorAPIComponent;
