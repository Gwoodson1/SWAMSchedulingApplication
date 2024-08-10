import React, { useState, useEffect } from 'react';
import api from '../api';
import { TextField, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';

const LessonAPIComponent = () => {
  const [data, setData] = useState([]);
  const [lessonTime, setLessonTime] = useState('');
  const [swimmerId, setSwimmerId] = useState('');
  const [instructorId, setInstructorId] = useState('');
  const [deleteLessonId, setDeleteLessonId] = useState('');
  const [updateLessonId, setUpdateLessonId] = useState('');
  const [newLessonTime, setNewLessonTime] = useState('');
  const [newSwimmerId, setNewSwimmerId] = useState('');
  const [newInstructorId, setNewInstructorId] = useState('');
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get('/lessons');
        setData(response.data);
      } catch (error) {
        setError('Error fetching data');
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  const handleCreateLesson = async () => {
    try {
      const newLesson = { lesson_time: lessonTime, swimmer_id: swimmerId, instructor_id: instructorId };
      const response = await api.post('/lessons', newLesson);
      setData([...data, response.data]);
      setLessonTime('');
      setSwimmerId('');
      setInstructorId('');
    } catch (error) {
      setError('Error creating lesson');
      console.error('Error creating lesson:', error);
    }
  };

  const handleDeleteLesson = async () => {
    try {
      await api.delete(`/lessons/${deleteLessonId}`);
      setData(data.filter(lesson => lesson.id !== parseInt(deleteLessonId)));
      setDeleteLessonId('');
    } catch (error) {
      setError('Error deleting lesson');
      console.error('Error deleting lesson:', error);
    }
  };

  const handleUpdateLesson = async () => {
    try {
      const updateData = {};
      if (newLessonTime) updateData.lesson_time = newLessonTime;
      if (newSwimmerId) updateData.swimmer_id = newSwimmerId;
      if (newInstructorId) updateData.instructor_id = newInstructorId;

      const response = await api.put(`/lessons/${updateLessonId}`, updateData);
      setData(data.map(lesson => (lesson.id === response.data.id ? response.data : lesson)));
      setUpdateLessonId('');
      setNewLessonTime('');
      setNewSwimmerId('');
      setNewInstructorId('');
    } catch (error) {
      setError('Error updating lesson');
      console.error('Error updating lesson:', error);
    }
  };

  return (
    <div>
      <h1>Lessons</h1>
      {error && <p>{error}</p>}
      {data.length === 0 && !error ? (
        <p>No lessons available</p>
      ) : (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Lesson ID</TableCell>
                <TableCell>Lesson Time</TableCell>
                <TableCell>Swimmer ID</TableCell>
                <TableCell>Instructor ID</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.map((lesson) => (
                <TableRow key={lesson.id}>
                 <TableCell>{lesson.id}</TableCell>
                  <TableCell>{lesson.lesson_time}</TableCell>
                  <TableCell>{lesson.swimmer_id}</TableCell>
                  <TableCell>{lesson.instructor_id}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      <div>
        <h2>Add Lesson</h2>
        <TextField
          label="Lesson Time"
          value={lessonTime}
          onChange={(e) => setLessonTime(e.target.value)}
        />
        <TextField
          label="Swimmer ID"
          value={swimmerId}
          onChange={(e) => setSwimmerId(e.target.value)}
        />
        <TextField
          label="Instructor ID"
          value={instructorId}
          onChange={(e) => setInstructorId(e.target.value)}
        />
        <Button variant="contained" color="primary" onClick={handleCreateLesson}>
          Add Lesson
        </Button>
      </div>
      <div>
        <h2>Delete Lesson</h2>
        <TextField
          label="Lesson ID to delete"
          value={deleteLessonId}
          onChange={(e) => setDeleteLessonId(e.target.value)}
        />
        <Button variant="contained" color="secondary" onClick={handleDeleteLesson}>
          Delete Lesson
        </Button>
      </div>
      <div>
        <h2>Update Lesson</h2>
        <TextField
          label="Lesson ID to update"
          value={updateLessonId}
          onChange={(e) => setUpdateLessonId(e.target.value)}
        />
        <TextField
          label="New Lesson Time"
          value={newLessonTime}
          onChange={(e) => setNewLessonTime(e.target.value)}
        />
        <TextField
          label="New Swimmer ID"
          value={newSwimmerId}
          onChange={(e) => setNewSwimmerId(e.target.value)}
        />
        <TextField
          label="New Instructor ID"
          value={newInstructorId}
          onChange={(e) => setNewInstructorId(e.target.value)}
        />
        <Button variant="contained" color="primary" onClick={handleUpdateLesson}>
          Update Lesson
        </Button>
      </div>
    </div>
  );
};

export default LessonAPIComponent;
