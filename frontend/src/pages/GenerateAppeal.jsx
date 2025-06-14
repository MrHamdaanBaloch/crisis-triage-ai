import React, { useState, useEffect } from 'react';
import { Box, Paper, Typography, CircularProgress, Alert, Checkbox, FormGroup, FormControlLabel, Button, TextField } from '@mui/material';
import { getIncidents, generateAppeal } from '../api';

export default function GenerateAppeal() {
    const [incidents, setIncidents] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selectedIds, setSelectedIds] = useState([]);
    const [appeal, setAppeal] = useState('');
    const [isGenerating, setIsGenerating] = useState(false);

    useEffect(() => {
        const fetchIncidents = async () => {
            try {
                const response = await getIncidents();
                setIncidents(response.data);
            } catch (err) {
                setError('Failed to fetch incident data.');
            } finally {
                setLoading(false);
            }
        };
        fetchIncidents();
    }, []);

    const handleSelect = (event) => {
        const { value, checked } = event.target;
        const id = parseInt(value);
        if (checked) {
            setSelectedIds(prev => [...prev, id]);
        } else {
            setSelectedIds(prev => prev.filter(item => item !== id));
        }
    };

    const handleGenerate = async () => {
        if (selectedIds.length === 0) {
            setError("Please select at least one incident to generate an appeal.");
            return;
        }
        setIsGenerating(true);
        setError(null);
        setAppeal('');
        try {
            const response = await generateAppeal(selectedIds);
            setAppeal(response.data.appeal);
        } catch (err) {
            setError("Failed to generate appeal. The AI service may be temporarily down.");
        } finally {
            setIsGenerating(false);
        }
    };

    if (loading) return <CircularProgress />;
    if (error && !incidents.length) return <Alert severity="error">{error}</Alert>;

    return (
        <Paper sx={{ p: 3 }}>
            <Typography variant="h4" gutterBottom>📢 Report & Appeal Generator</Typography>
            <Typography color="textSecondary" sx={{ mb: 2 }}>
                Select relevant incidents from the live feed to automatically generate a compelling fundraising appeal for social media or donors.
            </Typography>
            <Grid container spacing={4}>
                <Grid item xs={12} md={5}>
                    <Typography variant="h6" gutterBottom>Select Incidents</Typography>
                    {error && <Alert severity="warning" sx={{mb: 2}}>{error}</Alert>}
                    <Paper variant="outlined" sx={{ p: 2, height: '50vh', overflowY: 'auto' }}>
                        <FormGroup>
                            {incidents.map(incident => (
                                <FormControlLabel
                                    key={incident.id}
                                    control={<Checkbox value={incident.id} onChange={handleSelect} />}
                                    label={`#${incident.id}: ${incident.message.substring(0, 50)}...`}
                                />
                            ))}
                        </FormGroup>
                    </Paper>
                </Grid>
                <Grid item xs={12} md={7} sx={{ display: 'flex', flexDirection: 'column' }}>
                    <Typography variant="h6" gutterBottom>Generated Appeal</Typography>
                    <Button onClick={handleGenerate} variant="contained" disabled={isGenerating || selectedIds.length === 0}>
                        {isGenerating ? <CircularProgress size={24} /> : `Generate from ${selectedIds.length} incident(s)`}
                    </Button>
                    <TextField
                        multiline
                        rows={12}
                        fullWidth
                        value={appeal}
                        placeholder="Your generated fundraising appeal will appear here..."
                        variant="outlined"
                        sx={{ mt: 2, flexGrow: 1 }}
                        InputProps={{
                            readOnly: true,
                        }}
                    />
                </Grid>
            </Grid>
        </Paper>
    );
}

// A helper Grid component needs to be imported
import { Grid } from '@mui/material';