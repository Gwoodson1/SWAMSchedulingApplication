import React, { useState, useEffect } from 'react';
import api from '../api';
import { TextField, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';

const SwimmerAPIComponent = () => {
  const [data, setData] = useState([]);
  const [name, setName] = useState('');
  const [level, setLevel] = useState('');
  const [specialNeeds, setSpecialNeeds] = useState('');
  const [parentId, setParentId] = useState('');
  const [deleteSwimmerId, setDeleteSwimmerId] = useState('');
  const [updateSwimmerId, setUpdateSwimmerId] = useState('');
  const [newName, setNewName] = useState('');
  const [newLevel, setNewLevel] = useState('');
  const [newSpecialNeeds, setNewSpecialNeeds] = useState('');
  const [newParentId, setNewParentId] = useState('');
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get('/swimmers');
        const swimmers = response.data.map(swimmer => ({
          ...swimmer,
          parents: swimmer.parents || [] // Ensure parents is always an array
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
    try {
      const newSwimmer = {
        name,
        level,
        special_needs: specialNeeds,
        parent_id: parentId
      };
      const response = await api.post('/swimmers', newSwimmer);
      setData([...data, { ...response.data, parents: response.data.parents || [] }]);
      setName('');
      setLevel('');
      setSpecialNeeds('');
      setParentId('');
    } catch (error) {
      setError('Error creating swimmer');
      console.error('Error creating swimmer:', error);
    }
  };

  const handleDeleteSwimmer = async () => {
    try {
      await api.delete(`/swimmers/${deleteSwimmerId}`);
      setData(data.filter(swimmer => swimmer.id !== parseInt(deleteSwimmerId)));
      setDeleteSwimmerId('');
    } catch (error) {
      setError('Error deleting swimmer');
      console.error('Error deleting swimmer:', error);
    }
  };

  const handleUpdateSwimmer = async () => {
    try {
      const updateData = {};
      if (newName) updateData.name = newName;
      if (newLevel) updateData.level = newLevel;
      if (newSpecialNeeds) updateData.special_needs = newSpecialNeeds;
      if (newParentId) updateData.parent_id = newParentId;

      const response = await api.put(`/swimmers/${updateSwimmerId}`, updateData);
      setData(data.map(swimmer => (swimmer.id === response.data.id ? { ...response.data, parents: response.data.parents || [] } : swimmer)));
      setUpdateSwimmerId('');
      setNewName('');
      setNewLevel('');
      setNewSpecialNeeds('');
      setNewParentId('');
    } catch (error) {
      setError('Error updating swimmer');
      console.error('Error updating swimmer:', error);
    }
  };

  return (
    <div>
      <h1>Swimmers</h1>
      {error && <p>{error}</p>}
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
              </TableRow>
            </TableHead>
            <TableBody>
              {data.map((swimmer) => (
                <TableRow key={swimmer.id}>
                  <TableCell>{swimmer.id}</TableCell>
                  <TableCell>{swimmer.name}</TableCell>
                  <TableCell>{swimmer.level}</TableCell>
                  <TableCell>{swimmer.special_needs}</TableCell>
                  <TableCell>{swimmer.parents.join(', ')}</TableCell>
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
          label="Parent ID"
          value={parentId}
          onChange={(e) => setParentId(e.target.value)}
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
          label="New Parent ID"
          value={newParentId}
          onChange={(e) => setNewParentId(e.target.value)}
        />
        <Button variant="contained" color="primary" onClick={handleUpdateSwimmer}>
          Update Swimmer
        </Button>
      </div>
    </div>
  );
};

export default SwimmerAPIComponent;
