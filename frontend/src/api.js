import axios from 'axios';

const API = axios.create({
    baseURL: 'http://127.0.0.1:8000',
});

export const getIncidents = () => API.get('/incidents/');
export const getIncidentDetails = (id) => API.get(`/incidents/${id}`);
export const acknowledgeIncident = (id) => API.post(`/incidents/${id}/acknowledge`);
export const dispatchTeam = (id) => API.post(`/incidents/${id}/dispatch`);
export const reportIncident = (message) => API.post('/triage/', { message });
export const generateAppeal = (incident_ids) => API.post('/generate-appeal/', { incident_ids });