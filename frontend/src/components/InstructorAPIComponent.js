import React, { useState, useEffect } from 'react';
import api from '../api';
import { TextField, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';

const InstructorAPIComponent = () => {
  const [data, setData] = useState([]);
  
  // Separate state for adding instructors
  const [addInstructor, setAddInstructor] = useState({
    name: '',
    gender: '',
    languages: '',
    swimmerPreference: '',
    assignedChildPreference: '',
    taughtLessons: '',
    workedWithDisabilities: '',
    relevantExperience: '',
    expectations: '',
    additionalInfo: '',
    previousSwamLessons: '',
    lessonIds: ''
  });

  // Separate state for updating instructors
  const [updateInstructor, setUpdateInstructor] = useState({
    id: '',
    name: '',
    gender: '',
    languages: '',
    swimmerPreference: '',
    assignedChildPreference: '',
    taughtLessons: '',
    workedWithDisabilities: '',
    relevantExperience: '',
    expectations: '',
    additionalInfo: '',
    previousSwamLessons: '',
    lessonIds: ''
  });

  const [deleteInstructorId, setDeleteInstructorId] = useState(''); // State for deleting an instructor
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

  // Create instructor handler
  const handleCreateInstructor = async () => {
    try {
      const newInstructor = {
        name: addInstructor.name,
        gender: addInstructor.gender,
        languages: addInstructor.languages,
        swimmer_preference: addInstructor.swimmerPreference,
        assigned_child_preference: addInstructor.assignedChildPreference,
        taught_lessons: addInstructor.taughtLessons,
        worked_with_disabilities: addInstructor.workedWithDisabilities,
        relevant_experience: addInstructor.relevantExperience,
        expectations: addInstructor.expectations,
        additional_info: addInstructor.additionalInfo,
        previous_swam_lessons: addInstructor.previousSwamLessons,
        lesson_ids: addInstructor.lessonIds ? addInstructor.lessonIds.split(',').map(id => parseInt(id.trim())) : []
      };

      const response = await api.post('/instructors', newInstructor);
      setData([...data, { ...response.data, lessons: response.data.lessons || [] }]);
      
      // Reset form
      setAddInstructor({
        name: '',
        gender: '',
        languages: '',
        swimmerPreference: '',
        assignedChildPreference: '',
        taughtLessons: '',
        workedWithDisabilities: '',
        relevantExperience: '',
        expectations: '',
        additionalInfo: '',
        previousSwamLessons: '',
        lessonIds: ''
      });
      setError(null);
    } catch (error) {
      setError('Error creating instructor');
      console.error('Error creating instructor:', error);
    }
  };

  // Delete instructor handler
  const handleDeleteInstructor = async () => {
    if (!deleteInstructorId) {
      setError('Instructor ID is required to delete');
      return;
    }

    try {
      await api.delete(`/instructors/${deleteInstructorId}`);
      setData(data.filter(instructor => instructor.id !== parseInt(deleteInstructorId)));
      setDeleteInstructorId('');
      setError(null);
    } catch (error) {
      setError('Error deleting instructor');
      console.error('Error deleting instructor:', error);
    }
  };

  // Update instructor handler
const handleUpdateInstructor = async () => {
  if (!updateInstructor.id) {
    setError('Instructor ID is required to update');
    return;
  }

  try {
    const updateData = {};

    // Only include fields with non-empty values in the updateData
    if (updateInstructor.name) updateData.name = updateInstructor.name;
    if (updateInstructor.gender) updateData.gender = updateInstructor.gender;
    if (updateInstructor.languages) updateData.languages = updateInstructor.languages;
    if (updateInstructor.swimmerPreference) updateData.swimmer_preference = updateInstructor.swimmerPreference;
    if (updateInstructor.assignedChildPreference) updateData.assigned_child_preference = updateInstructor.assignedChildPreference;
    if (updateInstructor.taughtLessons) updateData.taught_lessons = updateInstructor.taughtLessons;
    if (updateInstructor.workedWithDisabilities) updateData.worked_with_disabilities = updateInstructor.workedWithDisabilities;
    if (updateInstructor.relevantExperience) updateData.relevant_experience = updateInstructor.relevantExperience;
    if (updateInstructor.expectations) updateData.expectations = updateInstructor.expectations;
    if (updateInstructor.additionalInfo) updateData.additional_info = updateInstructor.additionalInfo;
    if (updateInstructor.previousSwamLessons) updateData.previous_swam_lessons = updateInstructor.previousSwamLessons;
    if (updateInstructor.lessonIds) {
      updateData.lesson_ids = updateInstructor.lessonIds.split(',').map(id => parseInt(id.trim()));
    }

    const response = await api.put(`/instructors/${updateInstructor.id}`, updateData);
    setData(data.map(instructor =>
      instructor.id === response.data.id
        ? { ...response.data, lessons: response.data.lessons || [] }
        : instructor
    ));

    // Reset update form
    setUpdateInstructor({
      id: '',
      name: '',
      gender: '',
      languages: '',
      swimmerPreference: '',
      assignedChildPreference: '',
      taughtLessons: '',
      workedWithDisabilities: '',
      relevantExperience: '',
      expectations: '',
      additionalInfo: '',
      previousSwamLessons: '',
      lessonIds: ''
    });
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
                <TableCell>Name</TableCell>
                <TableCell>Lesson IDs</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.map((instructor) => (
                <TableRow key={instructor.id}>
                  <TableCell>{instructor.id}</TableCell>
                  <TableCell>{instructor.name}</TableCell>
                  <TableCell>{(instructor.lessons || []).join(', ')}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      
      {/* Add Instructor Section */}
      <div>
        <h2>Add Instructor</h2>
        <TextField
          label="Name"
          value={addInstructor.name}
          onChange={(e) => setAddInstructor({ ...addInstructor, name: e.target.value })}
        />
        <TextField
          label="Gender"
          value={addInstructor.gender}
          onChange={(e) => setAddInstructor({ ...addInstructor, gender: e.target.value })}
        />
        <TextField
          label="Languages"
          value={addInstructor.languages}
          onChange={(e) => setAddInstructor({ ...addInstructor, languages: e.target.value })}
        />
        <TextField
          label="Swimmer Preference"
          value={addInstructor.swimmerPreference}
          onChange={(e) => setAddInstructor({ ...addInstructor, swimmerPreference: e.target.value })}
        />
        <TextField
          label="Assigned Child Preference"
          value={addInstructor.assignedChildPreference}
          onChange={(e) => setAddInstructor({ ...addInstructor, assignedChildPreference: e.target.value })}
        />
        <TextField
          label="Taught Lessons"
          value={addInstructor.taughtLessons}
          onChange={(e) => setAddInstructor({ ...addInstructor, taughtLessons: e.target.value })}
        />
        <TextField
          label="Worked with Disabilities"
          value={addInstructor.workedWithDisabilities}
          onChange={(e) => setAddInstructor({ ...addInstructor, workedWithDisabilities: e.target.value })}
        />
        <TextField
          label="Relevant Experience"
          value={addInstructor.relevantExperience}
          onChange={(e) => setAddInstructor({ ...addInstructor, relevantExperience: e.target.value })}
        />
        <TextField
          label="Expectations"
          value={addInstructor.expectations}
          onChange={(e) => setAddInstructor({ ...addInstructor, expectations: e.target.value })}
        />
        <TextField
          label="Additional Info"
          value={addInstructor.additionalInfo}
          onChange={(e) => setAddInstructor({ ...addInstructor, additionalInfo: e.target.value })}
        />
        <TextField
          label="Previous Swim Lessons"
          value={addInstructor.previousSwamLessons}
          onChange={(e) => setAddInstructor({ ...addInstructor, previousSwamLessons: e.target.value })}
        />
        <TextField
          label="Lesson IDs (comma-separated)"
          value={addInstructor.lessonIds}
          onChange={(e) => setAddInstructor({ ...addInstructor, lessonIds: e.target.value })}
        />
        <Button variant="contained" color="primary" onClick={handleCreateInstructor}>
          Add Instructor
        </Button>
      </div>

      {/* Delete Instructor Section */}
      <div>
        <h2>Delete Instructor</h2>
        <TextField
          label="Instructor ID to delete"
          value={deleteInstructorId}
          onChange={(e) => setDeleteInstructorId(e.target.value)}
        />
        <Button variant="contained" color="secondary" onClick={handleDeleteInstructor}>
          Delete Instructor
        </Button>
      </div>

      {/* Update Instructor Section */}
      <div>
        <h2>Update Instructor</h2>
        <TextField
          label="Instructor ID to update"
          value={updateInstructor.id}
          onChange={(e) => setUpdateInstructor({ ...updateInstructor, id: e.target.value })}
        />
        <TextField
          label="New Name"
          value={updateInstructor.name}
          onChange={(e) => setUpdateInstructor({ ...updateInstructor, name: e.target.value })}
        />
        <TextField
          label="New Gender"
          value={updateInstructor.gender}
          onChange={(e) => setUpdateInstructor({ ...updateInstructor, gender: e.target.value })}
        />
        <TextField
          label="New Languages"
          value={updateInstructor.languages}
          onChange={(e) => setUpdateInstructor({ ...updateInstructor, languages: e.target.value })}
        />
        <TextField
          label="New Swimmer Preference"
          value={updateInstructor.swimmerPreference}
          onChange={(e) => setUpdateInstructor({ ...updateInstructor, swimmerPreference: e.target.value })}
        />
        <TextField
          label="New Assigned Child Preference"
          value={updateInstructor.assignedChildPreference}
          onChange={(e) => setUpdateInstructor({ ...updateInstructor, assignedChildPreference: e.target.value })}
        />
        <TextField
          label="New Taught Lessons"
          value={updateInstructor.taughtLessons}
          onChange={(e) => setUpdateInstructor({ ...updateInstructor, taughtLessons: e.target.value })}
        />
        <TextField
          label="New Worked with Disabilities"
          value={updateInstructor.workedWithDisabilities}
          onChange={(e) => setUpdateInstructor({ ...updateInstructor, workedWithDisabilities: e.target.value })}
        />
        <TextField
          label="New Relevant Experience"
          value={updateInstructor.relevantExperience}
          onChange={(e) => setUpdateInstructor({ ...updateInstructor, relevantExperience: e.target.value })}
        />
        <TextField
          label="New Expectations"
          value={updateInstructor.expectations}
          onChange={(e) => setUpdateInstructor({ ...updateInstructor, expectations: e.target.value })}
        />
        <TextField
          label="New Additional Info"
          value={updateInstructor.additionalInfo}
          onChange={(e) => setUpdateInstructor({ ...updateInstructor, additionalInfo: e.target.value })}
        />
        <TextField
          label="New Previous Swim Lessons"
          value={updateInstructor.previousSwamLessons}
          onChange={(e) => setUpdateInstructor({ ...updateInstructor, previousSwamLessons: e.target.value })}
        />
        <TextField
          label="New Lesson IDs (comma-separated)"
          value={updateInstructor.lessonIds}
          onChange={(e) => setUpdateInstructor({ ...updateInstructor, lessonIds: e.target.value })}
        />
        <Button variant="contained" color="primary" onClick={handleUpdateInstructor}>
          Update Instructor
        </Button>
      </div>
    </div>
  );
};

export default InstructorAPIComponent;