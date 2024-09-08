import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';

const ExportLessonData = () => {
  const [lessons, setLessons] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Fetch lessons with swimmer and instructor names from the new server route
    const fetchLessons = async () => {
      try {
        const response = await axios.get('http://localhost:5001/api/lessons-with-names');
        setLessons(response.data);
      } catch (error) {
        console.error('Error fetching lessons:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchLessons();
  }, []);

  // Function to handle assigning lesson times
  const handleAssignTimes = async () => {
    try {
      await axios.post('http://localhost:5001/api/assign-lesson-times');
      // Re-fetch the lessons to update the state after assignment
      const response = await axios.get('http://localhost:5001/api/lessons-with-names');
      setLessons(response.data);
    } catch (error) {
      console.error('Error assigning lesson times:', error);
    }
  };

  // Function to handle exporting lessons to Excel
  const handleExport = async (fileType) => {
    try {
      const response = await axios.get(`http://localhost:5001/api/export-lessons`, {
        params: { fileType },
        responseType: 'blob',  // Important for handling binary data
      });

      // Create a URL for the file and download it
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `lessons.${fileType}`);  // Set the file name
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Error exporting lesson data:', error);
    }
  };

  return (
    <div>
      <h2>Lesson Schedule</h2>
      {isLoading ? (
        <p>Loading lessons...</p>
      ) : (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Lesson ID</TableCell>
                <TableCell>Swimmer Name</TableCell>
                <TableCell>Instructor Name</TableCell>
                <TableCell>Lesson Time</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {lessons.sort((a, b) => {
                const times = ['9:30 - 10:00', '10:00 - 10:30', '10:30 - 11:00', '11:00 - 11:30'];
                return times.indexOf(a.lesson_time) - times.indexOf(b.lesson_time);
              }).map((lesson) => (
                <TableRow key={lesson.id}>
                  <TableCell>{lesson.id}</TableCell>
                  <TableCell>{lesson.swimmer_name}</TableCell>
                  <TableCell>{lesson.instructor_name}</TableCell>
                  <TableCell>{lesson.lesson_time || 'Unassigned'}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      <div style={{ marginTop: '20px' }}>
        <Button variant="contained" color="primary" onClick={handleAssignTimes}>
          Assign Lesson Times
        </Button>
        <Button variant="contained" color="secondary" onClick={() => handleExport('xlsx')} style={{ marginLeft: '10px' }}>
          Export to Excel
        </Button>
      </div>
    </div>
  );
};

export default ExportLessonData;