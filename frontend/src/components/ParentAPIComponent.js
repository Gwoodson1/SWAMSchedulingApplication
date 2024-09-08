import React, { useState, useEffect } from 'react';
import api from '../api';
import { TextField, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';

const ParentAPIComponent = () => {
  const [data, setData] = useState([]);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [childrenIds, setChildrenIds] = useState('');
  const [deleteUsername, setDeleteUsername] = useState('');
  const [updateUsername, setUpdateUsername] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [newName, setNewName] = useState('');
  const [newChildrenIds, setNewChildrenIds] = useState('');
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get('/parents');
        const parents = response.data.map(parent => ({
          ...parent,
          children: parent.children || [] // Ensure children is always an array
        }));
        setData(parents);
      } catch (error) {
        setError('Error fetching data');
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  const handleCreateParent = async () => {
    if (!username || !password || !name) {
      setError('Username, Password, and Name are required');
      return;
    }

    try {
      const newParent = {
        username,
        password,
        name,
        type: 'parent',
        children_ids: childrenIds ? childrenIds.split(',').map(id => parseInt(id.trim())) : []
      };
      const response = await api.post('/parents', newParent);
      setData([...data, { ...response.data, children: response.data.children || [] }]);
      setUsername('');
      setPassword('');
      setName('');
      setChildrenIds('');
      setError(null);
    } catch (error) {
      setError('Error creating parent');
      console.error('Error creating parent:', error);
    }
  };

  const handleDeleteParent = async () => {
    if (!deleteUsername) {
      setError('Username is required to delete');
      return;
    }

    try {
      const response = await api.get(`/parents/username/${deleteUsername}`);
      if (response.data && response.data.id) {
        await api.delete(`/parents/${response.data.id}`);
        setData(data.filter(parent => parent.id !== response.data.id));
        setDeleteUsername('');
        setError(null);
      } else {
        setError('Parent not found');
      }
    } catch (error) {
      setError('Error deleting parent');
      console.error('Error deleting parent:', error);
    }
  };

  const handleUpdateParent = async () => {
    if (!updateUsername) {
      setError('Username is required to update');
      return;
    }

    try {
      const updateData = {};
      if (newPassword) updateData.password = newPassword;
      if (newName) updateData.name = newName;
      if (newChildrenIds) updateData.children_ids = newChildrenIds.split(',').map(id => parseInt(id.trim()));

      const response = await api.put(`/parents/username/${updateUsername}`, updateData);
      setData(data.map(parent => (parent.id === response.data.id ? { ...response.data, children: response.data.children || [] } : parent)));
      setUpdateUsername('');
      setNewPassword('');
      setNewName('');
      setNewChildrenIds('');
      setError(null);
    } catch (error) {
      setError('Error updating parent');
      console.error('Error updating parent:', error);
    }
  };

  return (
    <div>
      <h1>Parents</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {data.length === 0 && !error ? (
        <p>No parents available</p>
      ) : (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>ID</TableCell>
                <TableCell>Username</TableCell>
                <TableCell>Name</TableCell>
                <TableCell>Children IDs</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.map((parent) => (
                <TableRow key={parent.id}>
                  <TableCell>{parent.id}</TableCell>
                  <TableCell>{parent.username}</TableCell>
                  <TableCell>{parent.name}</TableCell>
                  <TableCell>{parent.children.join(', ')}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      <div>
        <h2>Add Parent</h2>
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
          label="Children IDs (comma-separated)"
          value={childrenIds}
          onChange={(e) => setChildrenIds(e.target.value)}
        />
        <Button variant="contained" color="primary" onClick={handleCreateParent}>
          Add Parent
        </Button>
      </div>
      <div>
        <h2>Delete Parent</h2>
        <TextField
          label="Username to delete"
          value={deleteUsername}
          onChange={(e) => setDeleteUsername(e.target.value)}
        />
        <Button variant="contained" color="secondary" onClick={handleDeleteParent}>
          Delete Parent
        </Button>
      </div>
      <div>
        <h2>Update Parent</h2>
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
          label="New Children IDs (comma-separated)"
          value={newChildrenIds}
          onChange={(e) => setNewChildrenIds(e.target.value)}
        />
        <Button variant="contained" color="primary" onClick={handleUpdateParent}>
          Update Parent
        </Button>
      </div>
    </div>
  );
};

export default ParentAPIComponent;