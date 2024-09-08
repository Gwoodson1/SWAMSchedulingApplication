import React, { useState, useEffect } from 'react';

function PairSwimmerInstructor() {
  const [swimmers, setSwimmers] = useState([]);
  const [instructors, setInstructors] = useState([]);
  const [selectedSwimmer, setSelectedSwimmer] = useState(null);
  const [selectedInstructor, setSelectedInstructor] = useState(null);
  const [message, setMessage] = useState('');

  const [swimmerSearchQuery, setSwimmerSearchQuery] = useState('');
  const [instructorSearchQuery, setInstructorSearchQuery] = useState('');
  const [selectedSwimmerGenderFilter, setSelectedSwimmerGenderFilter] = useState('all');
  const [selectedInstructorGenderFilter, setSelectedInstructorGenderFilter] = useState('all');
  const [selectedSwimmerLanguageFilter, setSelectedSwimmerLanguageFilter] = useState('all');
  const [selectedInstructorLanguageFilter, setSelectedInstructorLanguageFilter] = useState('all');
  const [selectedSwimmerLevelFilter, setSelectedSwimmerLevelFilter] = useState('all');
  const [selectedLessonExperienceFilter, setSelectedLessonExperienceFilter] = useState('all');
  const [selectedSpecialNeedsExperienceFilter, setSelectedSpecialNeedsExperienceFilter] = useState('all');
  const [selectedInstructorPreferenceFilter, setSelectedInstructorPreferenceFilter] = useState('all');
  const [selectedSwimmerPairStatusFilter, setSelectedSwimmerPairStatusFilter] = useState('not_paired');
  const [selectedInstructorPairStatusFilter, setSelectedInstructorPairStatusFilter] = useState('not_paired');
  const [selectedAssignedChildPreferenceFilter, setSelectedAssignedChildPreferenceFilter] = useState('full');

  useEffect(() => {
    // Fetch swimmers
    fetch('http://localhost:5001/api/swimmers')
      .then(response => response.json())
      .then(data => {
        const swimmersWithLessons = data.map(swimmer => ({
          ...swimmer,
          lessons: swimmer.lessons || []  // Ensure lessons is always an array
        }));
        setSwimmers(swimmersWithLessons);
      })
      .catch(error => console.error('Error fetching swimmers:', error));
  
    // Fetch instructors
    fetch('http://localhost:5001/api/instructors')
      .then(response => response.json())
      .then(data => {
        const instructorsWithLessons = data.map(instructor => ({
          ...instructor,
          lessons: instructor.lessons || []  // Ensure lessons is always an array
        }));
        setInstructors(instructorsWithLessons);
      })
      .catch(error => console.error('Error fetching instructors:', error));
  }, []);

  const handlePair = () => {
    if (!selectedSwimmer || !selectedInstructor) return;
  
    fetch('http://localhost:5001/api/lessons', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        swimmer_ids: [selectedSwimmer.id],
        instructor_ids: [selectedInstructor.id],
      }),
    })
      .then(response => response.json())
      .then(data => {
        if (data.error) {
          setMessage(`Error: ${data.error}`);
        } else {
          setMessage('Lesson created successfully!');
  
          // Update state to move the paired swimmer and instructor to the "paired" category
          setSwimmers(prevSwimmers => 
            prevSwimmers.map(swimmer => 
              swimmer.id === selectedSwimmer.id ? { ...swimmer, lessons: [...swimmer.lessons, data.lesson_id] } : swimmer
            )
          );
  
          setInstructors(prevInstructors => 
            prevInstructors.map(instructor => 
              instructor.id === selectedInstructor.id ? { ...instructor, lessons: [...instructor.lessons, data.lesson_id] } : instructor
            )
          );
  
          // Optionally, clear selections
          setSelectedSwimmer(null);
          setSelectedInstructor(null);
          setInstructorSearchQuery('');
        }
      })
      .catch(error => {
        console.error('Error creating lesson:', error);
        setMessage(`Error: ${error.message}`);
      });
  };

  // Filter the swimmers based on various criteria
  const filteredSwimmers = swimmers.filter(swimmer => {
    const matchesSearch = swimmer.name.toLowerCase().includes(swimmerSearchQuery.toLowerCase());
    const matchesGender = selectedSwimmerGenderFilter === 'all' || (
      selectedSwimmerGenderFilter === 'male' && swimmer.gender === 'Male // Masculin'
    ) || (
      selectedSwimmerGenderFilter === 'female' && swimmer.gender === 'Female // Féminin'
    ) || (
      selectedSwimmerGenderFilter === 'other' && swimmer.gender !== 'Male // Masculin' && swimmer.gender !== 'Female // Féminin'
    );
    const matchesLanguage = selectedSwimmerLanguageFilter === 'all' || (
      selectedSwimmerLanguageFilter === 'english' && swimmer.language === 'Yes, English // Oui, Anglais'
    ) || (
      selectedSwimmerLanguageFilter === 'french' && swimmer.language === 'No, French // Non, Français'
    ) || (
      selectedSwimmerLanguageFilter === 'other' && swimmer.language !== 'Yes, English // Oui, Anglais' && swimmer.language !== 'No, French // Non, Français'
    );
    const matchesLevel = selectedSwimmerLevelFilter === 'all' || swimmer.level === selectedSwimmerLevelFilter;
    const matchesInstructorPreference = selectedInstructorPreferenceFilter === 'all' || (
      selectedInstructorPreferenceFilter === 'same_instructor' && swimmer.instructor_preference === "Yes, I would like the same instructor if they are available. // Oui, j'aimerais le même instructeur s'ils sont disponibles."
    ) || (
      selectedInstructorPreferenceFilter === 'new_instructor' && swimmer.instructor_preference === "No, I would like a new instructor. // Non, je voudrais un nouvel instructeur."
    ) || (
      selectedInstructorPreferenceFilter === 'no_preference' && swimmer.instructor_preference !== "Yes, I would like the same instructor if they are available. // Oui, j'aimerais le même instructeur s'ils sont disponibles." && swimmer.instructor_preference !== "No, I would like a new instructor. // Non, je voudrais un nouvel instructeur."
    );

    const matchesPairStatus = selectedSwimmerPairStatusFilter === 'all' || (
      selectedSwimmerPairStatusFilter === 'paired' && swimmer.lessons && swimmer.lessons.length > 0
    ) || (
      selectedSwimmerPairStatusFilter === 'not_paired' && (!swimmer.lessons || swimmer.lessons.length === 0)
    );

    return matchesSearch && matchesGender && matchesLanguage && matchesLevel && matchesInstructorPreference && matchesPairStatus;
  });

  // Filter the instructors based on various criteria
  const filteredInstructors = instructors.filter(instructor => {
    const matchesSearch = instructor.name.toLowerCase().includes(instructorSearchQuery.toLowerCase());
    const matchesGender = selectedInstructorGenderFilter === 'all' || (
      selectedInstructorGenderFilter === 'male' && instructor.gender === 'Male'
    ) || (
      selectedInstructorGenderFilter === 'female' && instructor.gender === 'Female'
    ) || (
      selectedInstructorGenderFilter === 'other' && instructor.gender !== 'Male' && instructor.gender !== 'Female'
    );
    const matchesLanguage = selectedInstructorLanguageFilter === 'all' || (
      selectedInstructorLanguageFilter === 'english' && instructor.languages === 'No'
    ) || (
      selectedInstructorLanguageFilter === 'french' && instructor.languages === 'Yes, French'
    ) || (
      selectedInstructorLanguageFilter === 'other' && instructor.languages !== 'No' && instructor.languages !== 'Yes, French'
    );
    const matchesLessonExperience = selectedLessonExperienceFilter === 'all' || (
      selectedLessonExperienceFilter === 'has_experience_with_swam' && instructor.previous_swam_lessons !== '0'
    ) || (
      selectedLessonExperienceFilter === 'has_experience' && instructor.taught_lessons === 'Yes'
    ) || (
      selectedLessonExperienceFilter === 'no_experience' && instructor.taught_lessons === 'No'
    );
    const matchesSpecialNeedsExperience = selectedSpecialNeedsExperienceFilter === 'all' || (
      selectedSpecialNeedsExperienceFilter === 'has_experience' && instructor.worked_with_disabilities === 'Yes'
    ) || (
      selectedSpecialNeedsExperienceFilter === 'no_experience' && instructor.worked_with_disabilities === 'No'
    );
    const matchesPairStatus = selectedInstructorPairStatusFilter === 'all' || (
      selectedInstructorPairStatusFilter === 'not_paired' && (!instructor.lessons || instructor.lessons.length === 0)
    ) || (
      selectedInstructorPairStatusFilter === '1_pairing' && instructor.lessons && instructor.lessons.length === 1
    ) || (
      selectedInstructorPairStatusFilter === '2_pairings' && instructor.lessons && instructor.lessons.length === 2
    ) || (
      selectedInstructorPairStatusFilter === '3_plus_pairings' && instructor.lessons && instructor.lessons.length >= 3
    );
    const matchesAssignedChildPreference = selectedAssignedChildPreferenceFilter === 'all' || (
      selectedAssignedChildPreferenceFilter === 'full' && instructor.assigned_child_preference === '(Full) I would like to have an assigned child and am able to commit to 7 of the 8 lessons'
    ) || (
      selectedAssignedChildPreferenceFilter === 'sub' && instructor.assigned_child_preference === 'SUB'
    );
    return matchesSearch && matchesGender && matchesLanguage && matchesLessonExperience && matchesSpecialNeedsExperience && matchesPairStatus && matchesAssignedChildPreference;
  });

  return (
    <div style={styles.container}>
      <h2 style={styles.heading}>Pair Swimmers with Instructors</h2>
      <button
        onClick={handlePair}
        disabled={!selectedSwimmer || !selectedInstructor}
        style={{
          ...styles.button,
          backgroundColor: !selectedSwimmer || !selectedInstructor ? '#cccccc' : '#007bff',
          cursor: !selectedSwimmer || !selectedInstructor ? 'not-allowed' : 'pointer',
        }}
      >
        Pair
      </button>
      <div style={styles.mainContent}>
        <div style={styles.infoCard}>
          {selectedSwimmer ? (
            <div>
              <h3>Swimmer Info</h3>
              <p><strong>Name:</strong> {selectedSwimmer.name}</p>
              <p><strong>Gender:</strong> {selectedSwimmer.gender}</p>
              <p><strong>Age:</strong> {Math.floor(Number(selectedSwimmer.age))}</p>
              <p><strong>Language:</strong> {selectedSwimmer.language}</p>
              <p><strong>Swim Experience:</strong> {selectedSwimmer.swim_experience}</p>
              <p><strong>Additonal Swim Experience Info:</strong> {selectedSwimmer.experience_details}</p>
              <p><strong>Number of previous SWAM sessions:</strong> {selectedSwimmer.previous_swam_lessons}</p>
              <p><strong>Level:</strong> {selectedSwimmer.level}</p>
              <p><strong>Instructor Preference:</strong> {selectedSwimmer.instructor_preference}</p>
              <p><strong>Previous Instructor:</strong> {selectedSwimmer.previous_instructor}</p>
              <p><strong>Instructor Preference Explanation:</strong> {selectedSwimmer.new_instructor_explanation}</p>
              <p><strong>Special Needs:</strong> {selectedSwimmer.special_needs}</p>
              <p><strong>Additonal Special Needs Info:</strong> {selectedSwimmer.special_needs_info}</p>
            </div>
          ) : (
            <p>Select a swimmer to see details</p>
          )}
        </div>
        <div style={styles.listsContainer}>
          <div style={styles.list}>
            <h3 style={styles.subheading}>Swimmers</h3>
            <input
              type="text"
              placeholder="Search Swimmers"
              value={swimmerSearchQuery}
              onChange={e => setSwimmerSearchQuery(e.target.value)}
              style={styles.searchBar}
            />
            <select
              value={selectedSwimmerGenderFilter}
              onChange={e => setSelectedSwimmerGenderFilter(e.target.value)}
              style={styles.filterSelect}
            >
              <option value="all">All Genders</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="other">Other</option>
            </select>
            <select
              value={selectedSwimmerLanguageFilter}
              onChange={e => setSelectedSwimmerLanguageFilter(e.target.value)}
              style={styles.filterSelect}
            >
              <option value="all">All Languages</option>
              <option value="english">English</option>
              <option value="french">French</option>
              <option value="other">Other</option>
            </select>
            <select
              value={selectedSwimmerLevelFilter}
              onChange={e => setSelectedSwimmerLevelFilter(e.target.value)}
              style={styles.filterSelect}
            >
              <option value="all">All Levels</option>
              <option value="1">Level 1</option>
              <option value="2">Level 2</option>
              <option value="3">Level 3</option>
              <option value="4">Level 4</option>
              <option value="5">Level 5</option>
            </select>
            <select
              value={selectedInstructorPreferenceFilter}
              onChange={e => setSelectedInstructorPreferenceFilter(e.target.value)}
              style={styles.filterSelect}
            >
              <option value="all">All Instructor Preferences</option>
              <option value="same_instructor">Wants Same Instructor</option>
              <option value="new_instructor">Wants New Instructor</option>
              <option value="no_preference">No Preference</option>
            </select>
            <select
              value={selectedSwimmerPairStatusFilter}
              onChange={e => setSelectedSwimmerPairStatusFilter(e.target.value)}
              style={styles.filterSelect}
            >
              <option value="all">All Pair Statuses</option>
              <option value="paired">Paired</option>
              <option value="not_paired">Not Paired</option>
            </select>
            <ul style={styles.ul}>
            {filteredSwimmers.map(swimmer => (
              <li
                key={swimmer.id}
                onClick={() => {
                  setSelectedSwimmer(swimmer);
                  if (swimmer.previous_instructor) {
                    setInstructorSearchQuery(swimmer.previous_instructor); 
                  } else {
                    setInstructorSearchQuery(''); 
                  }
                }}
                style={{
                  ...styles.listItem,
                  backgroundColor: selectedSwimmer?.id === swimmer.id ? 'lightblue' : 'white'
                }}
              >
                {swimmer.name}
              </li>
            ))}
          </ul>
          </div>
          <div style={styles.list}>
            <h3 style={styles.subheading}>Instructors</h3>
            <input
              type="text"
              placeholder="Search Instructors"
              value={instructorSearchQuery}
              onChange={e => setInstructorSearchQuery(e.target.value)}
              style={styles.searchBar}
            />
            <select
              value={selectedInstructorGenderFilter}
              onChange={e => setSelectedInstructorGenderFilter(e.target.value)}
              style={styles.filterSelect}
            >
              <option value="all">All Genders</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="other">Other</option>
            </select>
            <select
              value={selectedInstructorLanguageFilter}
              onChange={e => setSelectedInstructorLanguageFilter(e.target.value)}
              style={styles.filterSelect}
            >
              <option value="all">All Languages</option>
              <option value="english">Just English</option>
              <option value="french">English and French</option>
              <option value="other">Other</option>
            </select>
            <select
              value={selectedLessonExperienceFilter}
              onChange={e => setSelectedLessonExperienceFilter(e.target.value)}
              style={styles.filterSelect}
            >
              <option value="all">All Swim Lesson Experience</option>
              <option value="has_experience_with_swam">Has Taught Swim Lessons with SWAM Before</option>
              <option value="has_experience">Has Taught Swim Lessons Before</option>
              <option value="no_experience">Hasn't Taught Swim Lessons Before</option>
            </select>
            <select
              value={selectedSpecialNeedsExperienceFilter}
              onChange={e => setSelectedSpecialNeedsExperienceFilter(e.target.value)}
              style={styles.filterSelect}
            >
              <option value="all">All Special Needs Experience</option>
              <option value="has_experience">Has Worked With Special Needs</option>
              <option value="no_experience">Hasn't Worked With Special Needs</option>
            </select>
            <select
              value={selectedInstructorPairStatusFilter}
              onChange={e => setSelectedInstructorPairStatusFilter(e.target.value)}
              style={styles.filterSelect}
            >
              <option value="all">All Pair Statuses</option>
              <option value="not_paired">Not Paired</option>
              <option value="1_pairing">1 Pairing</option>
              <option value="2_pairings">2 Pairings</option>
              <option value="3_plus_pairings">3+ Pairings</option>
            </select>
            <select
              value={selectedAssignedChildPreferenceFilter}
              onChange={e => setSelectedAssignedChildPreferenceFilter(e.target.value)}
              style={styles.filterSelect}
            >
              <option value="all">All Assigned Child Preferences</option>
              <option value="full">Full</option>
              <option value="sub">Sub</option>
            </select>
            <ul style={styles.ul}>
              {filteredInstructors.map(instructor => (
                <li
                  key={instructor.id}
                  onClick={() => setSelectedInstructor(instructor)}
                  style={{
                    ...styles.listItem,
                    backgroundColor: selectedInstructor?.id === instructor.id ? 'lightgreen' : 'white'
                  }}
                >
                  {instructor.name}
                </li>
              ))}
            </ul>
          </div>
        </div>
        <div style={styles.infoCard}>
          {selectedInstructor ? (
            <div>
              <h3>Instructor Info</h3>
              <p><strong>Name:</strong> {selectedInstructor.name}</p>
              <p><strong>Gender:</strong> {selectedInstructor.gender}</p>
              <p><strong>Speaks Non-English Languages:</strong> {selectedInstructor.languages}</p>
              <p><strong>Prefers to be Assigned to Previous Swimmer:</strong> {selectedInstructor.swimmer_preference}</p>
              <p><strong>Prefers to be Assigned a Swimmer:</strong> {selectedInstructor.assigned_child_preference}</p>
              <p><strong>Has Taught Swim Lessons Before:</strong> {selectedInstructor.taught_lessons}</p>
              <p><strong>Has Worked with Children with Disabilities:</strong> {selectedInstructor.worked_with_disabilities}</p>
              <p><strong>Number of Previous Semesters with SWAM:</strong> {selectedInstructor.previous_swam_lessons}</p>
              <p><strong>Relevant Experience:</strong> {selectedInstructor.relevant_experience}</p>
              <p><strong>I'm looking forward to:</strong> {selectedInstructor.expectations}</p>
              <p><strong>Additonal Info:</strong> {selectedInstructor.additional_info}</p>
            </div>
          ) : (
            <p>Select an instructor to see details</p>
          )}
        </div>
      </div>
      {message && <p style={styles.message}>{message}</p>}
    </div>
  );
}

const styles = {
  container: {
    maxWidth: '1200px',
    margin: '20px auto',
    padding: '20px',
    borderRadius: '10px',
    boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)',
    backgroundColor: '#f9f9f9',
  },
  heading: {
    textAlign: 'center',
    marginBottom: '20px',
    color: '#333',
  },
  mainContent: {
    display: 'flex',
    justifyContent: 'space-between',
  },
  infoCard: {
    width: '24%', 
    padding: '20px',
    border: '1px solid #ddd',
    borderRadius: '10px',
    boxShadow: '0 5px 5px rgba(0, 0, 0, 0.1)',
    backgroundColor: '#fff',
    wordWrap: 'break-word',
  },
  listsContainer: {
    display: 'flex',
    justifyContent: 'space-between',
    width: '70%',
  },
  list: {
    width: '48%',
  },
  subheading: {
    textAlign: 'center',
    marginBottom: '10px',
    color: '#555',
  },
  ul: {
    listStyleType: 'none',
    padding: 0,
  },
  listItem: {
    padding: '10px',
    margin: '5px 0',
    border: '1px solid #ddd',
    borderRadius: '5px',
    cursor: 'pointer',
    textAlign: 'center',
  },
  searchBar: {
    width: '100%',
    padding: '10px',
    marginBottom: '10px',
    marginTop: '10px',
    borderRadius: '5px',
    border: '1px solid #ddd',
  },
  filterSelect: {
    width: '100%',
    padding: '10px',
    marginBottom: '10px',
    borderRadius: '5px',
    border: '1px solid #ddd',
  },
  button: {
    width: '300px',
    padding: '10px',
    margin: '10px auto',
    display: 'block',
    marginTop: '20px',
    fontSize: '16px',
    color: 'white',
    border: 'none',
    borderRadius: '5px',
    boxShadow: '0 5px 5px rgba(0, 0, 0, 0.1)',
  },
  message: {
    marginTop: '20px',
    textAlign: 'center',
    color: '#333',
  },
};

export default PairSwimmerInstructor;