import React, { useState } from 'react';
import { Box, Paper, Typography, TextField, Button, CircularProgress, Alert } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import { reportIncident } from '../api';

export default function ReportIncident() {
    const [message, setMessage] = useState('');
    const [loading, setLoading] = useState(false);
    const [feedback, setFeedback] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setFeedback(null);
        try {
            await reportIncident(message);
            setFeedback({ type: 'success', text: 'Report submitted successfully. Thank you. Our team has been notified.' });
            setMessage('');
        } catch (err) {
            setFeedback({ type: 'error', text: 'Failed to submit report. The service may be temporarily unavailable.' });
        } finally {
            setLoading(false);
        }
    };

    return (
        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh', width: '100vw', backgroundColor: '#f4f6f8' }}>
            <Paper sx={{ p: 4, maxWidth: 600, width: '90%' }}>
                <Typography variant="h4" gutterBottom align="center">📝 Report an Incident</Typography>
                <Typography variant="body1" color="textSecondary" sx={{ mb: 3 }} align="center">
                    This public reporting form is the fastest way to get help. Please provide a clear location and describe the situation in detail.
                </Typography>
                <form onSubmit={handleSubmit}>
                    <TextField
                        label="Describe the situation"
                        multiline
                        rows={6}
                        fullWidth
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        required
                        placeholder="Example: A building has collapsed at 5th and Main. I can hear people inside. We need search and rescue and medical teams."
                    />
                    <Button type="submit" variant="contained" fullWidth sx={{ mt: 3 }} disabled={loading}>
                        {loading ? <CircularProgress size={24} /> : 'Submit Emergency Report'}
                    </Button>
                    {feedback && <Alert severity={feedback.type} sx={{ mt: 2 }}>{feedback.text}</Alert>}
                </form>
            </Paper>
            <Button component={RouterLink} to="/" sx={{ mt: 3 }}>← Back to Dashboard</Button>
        </Box>
    );
}