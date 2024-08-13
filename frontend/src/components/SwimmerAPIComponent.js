import React, { useState, useEffect } from 'react';
import api from '../api';
import { TextField, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';

const SwimmerAPIComponent = () => {
  const [data, setData] = useState([]);
  const [name, setName] = useState('');
  const [level, setLevel] = useState('');
  const [specialNeeds, setSpecialNeeds] = useState('');
  const [parentIds, setParentIds] = useState('');
  const [lessonIds, setLessonIds] = useState('');
  const [deleteSwimmerId, setDeleteSwimmerId] = useState('');
  const [updateSwimmerId, setUpdateSwimmerId] = useState('');
  const [newName, setNewName] = useState('');
  const [newLevel, setNewLevel] = useState('');
  const [newSpecialNeeds, setNewSpecialNeeds] = useState('');
  const [newParentIds, setNewParentIds] = useState('');
  const [newLessonIds, setNewLessonIds] = useState('');
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get('/swimmers');
        const swimmers = response.data.map(swimmer => ({
          ...swimmer,
          parents: swimmer.parents || [], // Ensure parents is always an array
          lessons: swimmer.lessons || [] // Ensure lessons is always an array
        }));
        setData(swimmers);
      } catch (error) {
        setError('Error fetching data');
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  const handleCreateSwimmer = async () => {
    if (!name || !level) {
      setError('Name and Level are required');
      return;
    }

    try {
      const newSwimmer = {
        name,
        level,
        special_needs: specialNeeds,
        parent_ids: parentIds ? parentIds.split(',').map(id => parseInt(id.trim())) : [],
        lesson_ids: lessonIds ? lessonIds.split(',').map(id => parseInt(id.trim())) : []
      };
      const response = await api.post('/swimmers', newSwimmer);
      setData([...data, { ...response.data, parents: response.data.parents || [], lessons: response.data.lessons || [] }]);
      setName('');
      setLevel('');
      setSpecialNeeds('');
      setParentIds('');
      setLessonIds('');
      setError(null);
    } catch (error) {
      setError('Error creating swimmer');
      console.error('Error creating swimmer:', error);
    }
  };

  const handleUpdateSwimmer = async () => {
    if (!updateSwimmerId) {
      setError('Swimmer ID is required to update');
      return;
    }

    try {
      const updateData = {};
      if (newName) updateData.name = newName;
      if (newLevel) updateData.level = newLevel;
      if (newSpecialNeeds) updateData.special_needs = newSpecialNeeds;
      if (newParentIds) updateData.parent_ids = newParentIds.split(',').map(id => parseInt(id.trim()));
      if (newLessonIds) updateData.lesson_ids = newLessonIds.split(',').map(id => parseInt(id.trim()));

      const response = await api.put(`/swimmers/${updateSwimmerId}`, updateData);
      setData(data.map(swimmer => 
        swimmer.id === response.data.id 
          ? { ...response.data, parents: response.data.parents || [], lessons: response.data.lessons || [] } 
          : swimmer
      ));
      setUpdateSwimmerId('');
      setNewName('');
      setNewLevel('');
      setNewSpecialNeeds('');
      setNewParentIds('');
      setNewLessonIds('');
      setError(null);
    } catch (error) {
      setError('Error updating swimmer');
      console.error('Error updating swimmer:', error);
    }
  };

  const handleDeleteSwimmer = async () => {
    if (!deleteSwimmerId) {
      setError('Swimmer ID is required to delete');
      return;
    }

    try {
      await api.delete(`/swimmers/${deleteSwimmerId}`);
      setData(data.filter(swimmer => swimmer.id !== parseInt(deleteSwimmerId)));
      setDeleteSwimmerId('');
      setError(null);
    } catch (error) {
      setError('Error deleting swimmer');
      console.error('Error deleting swimmer:', error);
    }
  };

  return (
    <div>
      <h1>Swimmers</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {data.length === 0 && !error ? (
        <p>No swimmers available</p>
      ) : (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>ID</TableCell>
                <TableCell>Name</TableCell>
                <TableCell>Level</TableCell>
                <TableCell>Special Needs</TableCell>
                <TableCell>Parent IDs</TableCell>
                <TableCell>Lesson IDs</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.map((swimmer) => (
                <TableRow key={swimmer.id}>
                  <TableCell>{swimmer.id}</TableCell>
                  <TableCell>{swimmer.name}</TableCell>
                  <TableCell>{swimmer.level}</TableCell>
                  <TableCell>{swimmer.special_needs}</TableCell>
                  <TableCell>{(swimmer.parents || []).join(', ')}</TableCell>
                  <TableCell>{(swimmer.lessons || []).join(', ')}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      <div>
        <h2>Add Swimmer</h2>
        <TextField
          label="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <TextField
          label="Level"
          value={level}
          onChange={(e) => setLevel(e.target.value)}
        />
        <TextField
          label="Special Needs"
          value={specialNeeds}
          onChange={(e) => setSpecialNeeds(e.target.value)}
        />
        <TextField
          label="Parent IDs (comma-separated)"
          value={parentIds}
          onChange={(e) => setParentIds(e.target.value)}
        />
        <TextField
          label="Lesson IDs (comma-separated)"
          value={lessonIds}
          onChange={(e) => setLessonIds(e.target.value)}
        />
        <Button variant="contained" color="primary" onClick={handleCreateSwimmer}>
          Add Swimmer
        </Button>
      </div>
      <div>
        <h2>Delete Swimmer</h2>
        <TextField
          label="Swimmer ID to delete"
          value={deleteSwimmerId}
          onChange={(e) => setDeleteSwimmerId(e.target.value)}
        />
        <Button variant="contained" color="secondary" onClick={handleDeleteSwimmer}>
          Delete Swimmer
        </Button>
      </div>
      <div>
        <h2>Update Swimmer</h2>
        <TextField
          label="Swimmer ID to update"
          value={updateSwimmerId}
          onChange={(e) => setUpdateSwimmerId(e.target.value)}
        />
        <TextField
          label="New Name"
          value={newName}
          onChange={(e) => setNewName(e.target.value)}
        />
        <TextField
          label="New Level"
          value={newLevel}
          onChange={(e) => setNewLevel(e.target.value)}
        />
        <TextField
          label="New Special Needs"
          value={newSpecialNeeds}
          onChange={(e) => setNewSpecialNeeds(e.target.value)}
        />
        <TextField
          label="New Parent IDs (comma-separated)"
          value={newParentIds}
          onChange={(e) => setNewParentIds(e.target.value)}
        />
        <TextField
          label="New Lesson IDs (comma-separated)"
          value={newLessonIds}
          onChange={(e) => setNewLessonIds(e.target.value)}
        />
        <Button variant="contained" color="primary" onClick={handleUpdateSwimmer}>
          Update Swimmer
        </Button>
      </div>
    </div>
  );
};

export default SwimmerAPIComponent;
