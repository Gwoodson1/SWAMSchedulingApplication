import React, { useState, useEffect } from 'react';
import api from '../api';
import { TextField, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';

const SwimmerAPIComponent = () => {
  const [data, setData] = useState([]);
  const [name, setName] = useState('');
  const [gender, setGender] = useState('');
  const [age, setAge] = useState('');
  const [language, setLanguage] = useState('');
  const [instructorPreference, setInstructorPreference] = useState('');
  const [availabilities, setAvailabilities] = useState('');
  const [specialNeedsInfo, setSpecialNeedsInfo] = useState('');
  const [swimExperience, setSwimExperience] = useState('');
  const [experienceDetails, setExperienceDetails] = useState('');
  const [previousSwamLessons, setPreviousSwamLessons] = useState('');
  const [newInstructorExplanation, setNewInstructorExplanation] = useState('');
  const [lessonIds, setLessonIds] = useState('');
  const [deleteSwimmerId, setDeleteSwimmerId] = useState('');
  const [updateSwimmerId, setUpdateSwimmerId] = useState('');
  const [newName, setNewName] = useState('');
  const [newGender, setNewGender] = useState('');
  const [newAge, setNewAge] = useState('');
  const [newLanguage, setNewLanguage] = useState('');
  const [newInstructorPreference, setNewInstructorPreference] = useState('');
  const [newAvailabilities, setNewAvailabilities] = useState('');
  const [newSpecialNeedsInfo, setNewSpecialNeedsInfo] = useState('');
  const [newSwimExperience, setNewSwimExperience] = useState('');
  const [newExperienceDetails, setNewExperienceDetails] = useState('');
  const [newPreviousSwamLessons, setNewPreviousSwamLessons] = useState('');
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
    if (!name || !age || !language) {
      setError('Name, Age, and Language are required');
      return;
    }

    try {
      const newSwimmer = {
        name,
        gender,
        age,
        language,
        instructor_preference: instructorPreference,
        availabilities,
        special_needs_info: specialNeedsInfo,
        swim_experience: swimExperience,
        experience_details: experienceDetails,
        previous_swam_lessons: previousSwamLessons,
        new_instructor_explanation: newInstructorExplanation,
        lesson_ids: lessonIds ? lessonIds.split(',').map(id => parseInt(id.trim())) : []
      };
      const response = await api.post('/swimmers', newSwimmer);
      setData([...data, { ...response.data, parents: response.data.parents || [], lessons: response.data.lessons || [] }]);
      setName(''); setGender(''); setAge(''); setLanguage(''); setInstructorPreference('');
      setAvailabilities(''); setSpecialNeedsInfo(''); setSwimExperience(''); setExperienceDetails('');
      setPreviousSwamLessons(''); setNewInstructorExplanation(''); setLessonIds('');
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
      if (newGender) updateData.gender = newGender;
      if (newAge) updateData.age = newAge;
      if (newLanguage) updateData.language = newLanguage;
      if (newInstructorPreference) updateData.instructor_preference = newInstructorPreference;
      if (newAvailabilities) updateData.availabilities = newAvailabilities;
      if (newSpecialNeedsInfo) updateData.special_needs_info = newSpecialNeedsInfo;
      if (newSwimExperience) updateData.swim_experience = newSwimExperience;
      if (newExperienceDetails) updateData.experience_details = newExperienceDetails;
      if (newPreviousSwamLessons) updateData.previous_swam_lessons = newPreviousSwamLessons;
      if (newInstructorExplanation) updateData.new_instructor_explanation = newInstructorExplanation;
      if (newLessonIds) updateData.lesson_ids = newLessonIds.split(',').map(id => parseInt(id.trim()));

      const response = await api.put(`/swimmers/${updateSwimmerId}`, updateData);
      setData(data.map(swimmer => 
        swimmer.id === response.data.id 
          ? { ...response.data, parents: response.data.parents || [], lessons: response.data.lessons || [] } 
          : swimmer
      ));
      setUpdateSwimmerId(''); setNewName(''); setNewGender(''); setNewAge(''); setNewLanguage('');
      setNewInstructorPreference(''); setNewAvailabilities(''); setNewSpecialNeedsInfo('');
      setNewSwimExperience(''); setNewExperienceDetails(''); setNewPreviousSwamLessons('');
      setNewInstructorExplanation(''); setNewLessonIds(''); 
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
 // Modify the table to display only ID, Name, and Lesson IDs
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
            {data.map((swimmer) => (
              <TableRow key={swimmer.id}>
                <TableCell>{swimmer.id}</TableCell>
                <TableCell>{swimmer.name}</TableCell>
                <TableCell>{(swimmer.lessons || []).join(', ')}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>      )}
      <div>
        <h2>Add Swimmer</h2>
        <TextField label="Name" value={name} onChange={(e) => setName(e.target.value)} />
        <TextField label="Gender" value={gender} onChange={(e) => setGender(e.target.value)} />
        <TextField label="Age" value={age} onChange={(e) => setAge(e.target.value)} />
        <TextField label="Language" value={language} onChange={(e) => setLanguage(e.target.value)} />
        <TextField label="Instructor Preference" value={instructorPreference} onChange={(e) => setInstructorPreference(e.target.value)} />
        <TextField label="Availabilities" value={availabilities} onChange={(e) => setAvailabilities(e.target.value)} />
        <TextField label="Special Needs Info" value={specialNeedsInfo} onChange={(e) => setSpecialNeedsInfo(e.target.value)} />
        <TextField label="Swim Experience" value={swimExperience} onChange={(e) => setSwimExperience(e.target.value)} />
        <TextField label="Experience Details" value={experienceDetails} onChange={(e) => setExperienceDetails(e.target.value)} />
        <TextField label="Previous Swam Lessons" value={previousSwamLessons} onChange={(e) => setPreviousSwamLessons(e.target.value)} />
        <TextField label="New Instructor Explanation" value={newInstructorExplanation} onChange={(e) => setNewInstructorExplanation(e.target.value)} />
        <TextField label="Lesson IDs (comma-separated)" value={lessonIds} onChange={(e) => setLessonIds(e.target.value)} />
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
        <TextField label="New Name" value={newName} onChange={(e) => setNewName(e.target.value)} />
        <TextField label="New Gender" value={newGender} onChange={(e) => setNewGender(e.target.value)} />
        <TextField label="New Age" value={newAge} onChange={(e) => setNewAge(e.target.value)} />
        <TextField label="New Language" value={newLanguage} onChange={(e) => setNewLanguage(e.target.value)} />
        <TextField label="New Instructor Preference" value={newInstructorPreference} onChange={(e) => setNewInstructorPreference(e.target.value)} />
        <TextField label="New Availabilities" value={newAvailabilities} onChange={(e) => setNewAvailabilities(e.target.value)} />
        <TextField label="New Special Needs Info" value={newSpecialNeedsInfo} onChange={(e) => setNewSpecialNeedsInfo(e.target.value)} />
        <TextField label="New Swim Experience" value={newSwimExperience} onChange={(e) => setNewSwimExperience(e.target.value)} />
        <TextField label="New Experience Details" value={newExperienceDetails} onChange={(e) => setNewExperienceDetails(e.target.value)} />
        <TextField label="New Previous Swam Lessons" value={newPreviousSwamLessons} onChange={(e) => setNewPreviousSwamLessons(e.target.value)} />
        <TextField label="New Instructor Explanation" value={newInstructorExplanation} onChange={(e) => setNewInstructorExplanation(e.target.value)} />
        <TextField label="New Lesson IDs (comma-separated)" value={newLessonIds} onChange={(e) => setNewLessonIds(e.target.value)} />
        <Button variant="contained" color="primary" onClick={handleUpdateSwimmer}>
          Update Swimmer
        </Button>
      </div>
    </div>
  );
};

export default SwimmerAPIComponent;
