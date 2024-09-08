import React, { useState, useEffect } from 'react';
import api from '../api';
import { TextField, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';

const LessonAPIComponent = () => {
  const [data, setData] = useState([]);
  const [lessonTime, setLessonTime] = useState('');
  const [swimmerIds, setSwimmerIds] = useState('');
  const [instructorIds, setInstructorIds] = useState('');
  const [deleteLessonId, setDeleteLessonId] = useState('');
  const [updateLessonId, setUpdateLessonId] = useState('');
  const [newLessonTime, setNewLessonTime] = useState('');
  const [newSwimmerIds, setNewSwimmerIds] = useState('');
  const [newInstructorIds, setNewInstructorIds] = useState('');
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get('/lessons');
        const lessons = response.data.map(lesson => ({
          ...lesson,
          swimmers: lesson.swimmers || [], // Ensure swimmers is always an array
          instructors: lesson.instructors || [] // Ensure instructors is always an array
        }));
        setData(lessons);
      } catch (error) {
        setError('Error fetching data');
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  const handleCreateLesson = async () => {
    if (!lessonTime) {
      setError('Lesson Time is required');
      return;
    }

    try {
      const newLesson = {
        lesson_time: lessonTime,
        swimmer_ids: swimmerIds ? swimmerIds.split(',').map(id => parseInt(id.trim())) : [],
        instructor_ids: instructorIds ? instructorIds.split(',').map(id => parseInt(id.trim())) : []
      };
      const response = await api.post('/lessons', newLesson);
      setData([...data, { ...response.data, swimmers: response.data.swimmers || [], instructors: response.data.instructors || [] }]);
      setLessonTime('');
      setSwimmerIds('');
      setInstructorIds('');
      setError(null);
    } catch (error) {
      setError('Error creating lesson');
      console.error('Error creating lesson:', error);
    }
  };

  const handleDeleteLesson = async () => {
    if (!deleteLessonId) {
      setError('Lesson ID is required to delete');
      return;
    }

    try {
      await api.delete(`/lessons/${deleteLessonId}`);
      setData(data.filter(lesson => lesson.id !== parseInt(deleteLessonId)));
      setDeleteLessonId('');
      setError(null);
    } catch (error) {
      setError('Error deleting lesson');
      console.error('Error deleting lesson:', error);
    }
  };

  const handleUpdateLesson = async () => {
    if (!updateLessonId) {
      setError('Lesson ID is required to update');
      return;
    }
  
    try {
      const updateData = {};
  
      // Only include fields with non-empty values
      if (newLessonTime) {
        updateData.lesson_time = newLessonTime;
      }
  
      // If swimmerIds field is not empty, process it; otherwise, skip it
      if (newSwimmerIds.trim()) {
        updateData.swimmer_ids = newSwimmerIds.split(',').map(id => parseInt(id.trim()));
      }
  
      // If instructorIds field is not empty, process it; otherwise, skip it
      if (newInstructorIds.trim()) {
        updateData.instructor_ids = newInstructorIds.split(',').map(id => parseInt(id.trim()));
      }
  
      const response = await api.put(`/lessons/${updateLessonId}`, updateData);
  
      setData(data.map(lesson =>
        lesson.id === response.data.id
          ? { ...response.data, swimmers: response.data.swimmers || [], instructors: response.data.instructors || [] }
          : lesson
      ));
  
      // Reset form fields
      setUpdateLessonId('');
      setNewLessonTime('');
      setNewSwimmerIds('');
      setNewInstructorIds('');
      setError(null);
    } catch (error) {
      setError('Error updating lesson');
      console.error('Error updating lesson:', error);
    }
  };

  return (
    <div>
      <h1>Lessons</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {data.length === 0 && !error ? (
        <p>No lessons available</p>
      ) : (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Lesson ID</TableCell>
                <TableCell>Lesson Time</TableCell>
                <TableCell>Swimmer IDs</TableCell>
                <TableCell>Instructor IDs</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.map((lesson) => (
                <TableRow key={lesson.id}>
                  <TableCell>{lesson.id}</TableCell>
                  <TableCell>{lesson.lesson_time}</TableCell>
                  <TableCell>{(lesson.swimmers || []).join(', ')}</TableCell>
                  <TableCell>{(lesson.instructors || []).join(', ')}</TableCell>
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
          label="Swimmer IDs (comma-separated)"
          value={swimmerIds}
          onChange={(e) => setSwimmerIds(e.target.value)}
        />
        <TextField
          label="Instructor IDs (comma-separated)"
          value={instructorIds}
          onChange={(e) => setInstructorIds(e.target.value)}
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
        <h2>Update Lesson (include all fields) </h2>
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
          label="New Swimmer IDs (comma-separated)"
          value={newSwimmerIds}
          onChange={(e) => setNewSwimmerIds(e.target.value)}
        />
        <TextField
          label="New Instructor IDs (comma-separated)"
          value={newInstructorIds}
          onChange={(e) => setNewInstructorIds(e.target.value)}
        />
        <Button variant="contained" color="primary" onClick={handleUpdateLesson}>
          Update Lesson
        </Button>
      </div>
    </div>
  );
};

export default LessonAPIComponent;