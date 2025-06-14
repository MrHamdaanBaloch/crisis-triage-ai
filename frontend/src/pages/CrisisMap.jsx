import React, { useState, useEffect, useCallback, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import { Paper, Typography, CircularProgress, Alert, Box, Switch, FormControlLabel } from '@mui/material';
import { getIncidents } from '../api';

export default function CrisisMap() {
    const [incidents, setIncidents] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [isLive, setIsLive] = useState(false);
    const intervalRef = useRef(null);

    const fetchIncidents = useCallback(async () => {
        setLoading(true);
        try {
            const response = await getIncidents();
            const incidentsWithCoords = response.data.filter(inc => {
                const details = typeof inc.details === 'string' ? JSON.parse(inc.details || '{}') : inc.details;
                return details && details.latitude != null && details.longitude != null;
            });
            setIncidents(incidentsWithCoords);
        } catch (err) {
            setError('Failed to fetch incident data.');
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchIncidents();
    }, [fetchIncidents]);

    useEffect(() => {
        if (isLive) {
            intervalRef.current = setInterval(fetchIncidents, 5000); // Refresh every 5 seconds
        } else {
            clearInterval(intervalRef.current);
        }
        return () => clearInterval(intervalRef.current);
    }, [isLive, fetchIncidents]);

    return (
        <Paper sx={{ p: 2, height: '85vh', width: '100%', display: 'flex', flexDirection: 'column' }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Box>
                    <Typography variant="h4" gutterBottom>🗺️ Real-Time Crisis Map</Typography>
                    <Typography color="textSecondary">Incidents with location data are plotted below. Turn on Live Mode to see new reports appear automatically.</Typography>
                </Box>
                <FormControlLabel control={<Switch checked={isLive} onChange={(e) => setIsLive(e.target.checked)} />} label="Live Mode" />
            </Box>
            
            <Box sx={{ flexGrow: 1, mt: 2 }}>
                {loading && <CircularProgress />}
                {error && <Alert severity="error">{error}</Alert>}
                {!loading && !error && (
                    incidents.length === 0 ? (
                        <Alert severity="info" sx={{ flexGrow: 1 }}>No incidents with location data to display. Please submit a new report with a clear location like "Eiffel Tower".</Alert>
                    ) : (
                        <MapContainer center={[20, 0]} zoom={2} style={{ height: '100%', width: '100%' }}>
                            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" attribution='© OpenStreetMap contributors' />
                            {incidents.map(incident => {
                                const details = typeof incident.details === 'string' ? JSON.parse(incident.details || '{}') : incident.details;
                                return (
                                    <Marker key={incident.id} position={[details.latitude, details.longitude]}>
                                        <Popup><b>Incident #{incident.id}</b><br/>Priority: {incident.priority_score}<br/>{incident.message}</Popup>
                                    </Marker>
                                );
                            })}
                        </MapContainer>
                    )
                )}
            </Box>
        </Paper>
    );
}