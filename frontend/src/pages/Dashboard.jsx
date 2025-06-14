import React, { useState, useEffect } from 'react';
import { Box, Paper, Typography, CircularProgress, Alert, Button, Dialog, DialogTitle, DialogContent, DialogContentText, DialogActions, Grid } from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';
import { getIncidents, acknowledgeIncident, dispatchTeam } from '../api';

// --- REVERTED TO YOUR WORKING COLUMNS ---
// This uses 'message' directly and is guaranteed to work.
const columns = [
    { field: 'id', headerName: 'ID', width: 90 },
    { field: 'priority_score', headerName: 'Priority', width: 120, cellClassName: (params) => params.value >= 75 ? 'critical-priority' : (params.value >= 50 ? 'high-priority' : '') },
    { field: 'status', headerName: 'Status', width: 220 },
    { field: 'message', headerName: 'Message', flex: 1 },
];

// This is your original, working helper function.
const safeParseDetails = (details) => {
    if (!details) return {};
    if (typeof details === 'object') return details;
    try {
        return JSON.parse(details);
    } catch (e) {
        console.error("Failed to parse incident details:", e);
        return {};
    }
};

// This is your original, working component structure.
export default function Dashboard() {
    const [incidents, setIncidents] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selectedIncident, setSelectedIncident] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);

    const fetchIncidents = async () => {
        setLoading(true);
        try {
            const response = await getIncidents();
            setIncidents(response.data);
            setError(null);
        } catch (err) {
            setError('Failed to fetch incidents. Is the backend server running?');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchIncidents();
    }, []);
    
    const handleRowClick = (params) => {
        setSelectedIncident(params.row);
        setIsModalOpen(true);
    };

    const handleAction = async (actionFunc) => {
        if (!selectedIncident) return;
        await actionFunc(selectedIncident.id);
        setIsModalOpen(false);
        fetchIncidents();
    };
    
    if (loading) return <CircularProgress />;
    if (error) return <Alert severity="error">{error}</Alert>;

    const needsDispatch = incidents.filter(i => i.status === 'Needs Dispatch').length;
    const dispatched = incidents.filter(i => i.status.startsWith('Dispatched')).length;
    
    const selectedIncidentDetails = selectedIncident ? safeParseDetails(selectedIncident.details) : {};

    const canAcknowledge = selectedIncident?.status === 'Needs Dispatch';
    const canDispatch = selectedIncident?.status === 'Acknowledged';

    return (
        <Box>
            <Typography variant="h4" gutterBottom>🚀 Live Incident Dashboard</Typography>
            <Typography color="textSecondary" sx={{ mb: 2 }}>Overview of all incoming crisis reports. Click a row to manage an incident.</Typography>

            <Grid container spacing={3} sx={{ mb: 3 }}>
                <Grid item xs={4}><Paper sx={{p:2, textAlign: 'center'}}><Typography variant="h6">Total Incidents</Typography><Typography variant="h3">{incidents.length}</Typography></Paper></Grid>
                <Grid item xs={4}><Paper sx={{p:2, textAlign: 'center'}}><Typography variant="h6">Pending Acknowledgment</Typography><Typography variant="h3" color="error">{needsDispatch}</Typography></Paper></Grid>
                <Grid item xs={4}><Paper sx={{p:2, textAlign: 'center'}}><Typography variant="h6">Teams Dispatched</Typography><Typography variant="h3" color="primary">{dispatched}</Typography></Paper></Grid>
            </Grid>

            <Paper sx={{ height: '60vh', width: '100%', '& .critical-priority': { backgroundColor: '#ffcdd2' }, '& .high-priority': { backgroundColor: '#ffe0b2' } }}>
                <DataGrid rows={incidents} columns={columns} onRowClick={handleRowClick} sx={{ '& .MuiDataGrid-cell:hover': { cursor: 'pointer' } }} />
            </Paper>

            {selectedIncident && (
                 <Dialog open={isModalOpen} onClose={() => setIsModalOpen(false)} fullWidth maxWidth="sm">
                    <DialogTitle>Manage Incident #{selectedIncident.id}</DialogTitle>
                    <DialogContent>
                        <DialogContentText component="div">
                            <Typography variant="body1" gutterBottom><strong>Original Report:</strong> {selectedIncident.message}</Typography>
                            <Typography variant="body2" color="textSecondary" sx={{mb: 2}}><strong>Current Status:</strong> {selectedIncident.status}</Typography>
                            
                            {/* --- THIS IS THE ONLY ADDITION --- */}
                            {selectedIncidentDetails.reasoning && (
                                <Alert severity={selectedIncident.priority_score >= 75 ? "error" : "warning"} sx={{mb: 2}}>
                                    <strong>AI Score Reasoning:</strong> {selectedIncidentDetails.reasoning}
                                </Alert>
                            )}
                            
                            <Paper variant="outlined" sx={{ p: 2, mt: 2, backgroundColor: '#f5f5f5' }}>
                                <Typography variant="caption">Extracted Intelligence</Typography>
                                <pre style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-all' }}>{JSON.stringify(selectedIncidentDetails, null, 2)}</pre>
                            </Paper>
                        </DialogContentText>
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={() => setIsModalOpen(false)}>Close</Button>
                        <Button onClick={() => handleAction(acknowledgeIncident)} disabled={!canAcknowledge}>Acknowledge</Button>
                        <Button onClick={() => handleAction(dispatchTeam)} variant="contained" disabled={!canDispatch}>Dispatch Team</Button>
                    </DialogActions>
                </Dialog>
            )}
        </Box>
    );
}