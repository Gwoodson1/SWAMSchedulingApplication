import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5001/api', // Your Flask API base URL
});

export default api;
