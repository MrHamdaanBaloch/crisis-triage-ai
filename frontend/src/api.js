import axios from 'axios';


// --- THIS IS THE CRUCIAL CHANGE ---
// This line now smartly chooses the correct URL.
// On Netlify, import.meta.env.VITE_API_BASE_URL will be your live Render URL.
// On your local machine, it will be undefined, so it falls back to your localhost address.
const API_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

console.log(`Connecting to API at: ${API_URL}`); // A helpful log to see which URL is being used

const API = axios.create({
    baseURL: API_URL,
});

export const getIncidents = () => API.get('/incidents/');
export const getIncidentDetails = (id) => API.get(`/incidents/${id}`);
export const acknowledgeIncident = (id) => API.post(`/incidents/${id}/acknowledge`);
export const dispatchTeam = (id) => API.post(`/incidents/${id}/dispatch`);
export const reportIncident = (message) => API.post('/triage/', { message });
export const generateAppeal = (incident_ids) => API.post('/generate-appeal/', { incident_ids });