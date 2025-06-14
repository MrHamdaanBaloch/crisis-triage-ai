import React from 'react';
import { Box, Paper, Typography, Grid, Button, Avatar, Divider, Link } from '@mui/material';
import GitHubIcon from '@mui/icons-material/GitHub';
import LinkedInIcon from '@mui/icons-material/LinkedIn';

// --- Importing your local logo images ---
// The paths are based on your screenshot's file structure.
import traeAILogo from '../images/5pyt9wg5.png'; 
import novitaAILogo from '../images/logo.svg';

// --- Creator Info with Your Provided Links ---
const creators = {
    hamdaan: {
        name: 'Hamdaan Baloch',
        role: 'Lead Backend Developer & System Architect',
        github: 'https://github.com/mrHamdaanbaloch',
        linkedin: 'https://pk.linkedin.com/in/hamdaan-baloch-3ba3b51ab',
        avatar: 'HB'
    },
    saad: {
        name: 'Asif Ullah Saad',
        role: 'Presenter & Frontend Contributor',
        github: 'https://github.com/asif-ullah-saad',
        linkedin: 'https://www.linkedin.com/in/asif-ullah-saad-724103154',
        avatar: 'S'
    }
};

// --- Technology Info Using Your Logos and Links ---
const technologies = [
    { name: 'Trae.ai', logo: traeAILogo, siteUrl: 'https://www.trae.ai/' },
    { name: 'Novita.ai', logo: novitaAILogo, siteUrl: 'https://novita.ai/' }
];

export default function About() {
    return (
        <Paper sx={{ p: 3, mx: 'auto', maxWidth: 900 }}>
            <Typography variant="h4" gutterBottom>About CrisisTriage AI</Typography>
            <Typography variant="body1" color="textSecondary" paragraph>
                This platform is a proof-of-concept for a next-generation crisis response system, developed for a hackathon. It leverages cutting-edge AI to provide real-time intelligence, enabling faster and more effective humanitarian aid.
            </Typography>

            <Divider sx={{ my: 3 }} />

            <Typography variant="h5" gutterBottom>The Team</Typography>
            <Grid container spacing={4}>
                {Object.values(creators).map(creator => (
                    <Grid item xs={12} md={6} key={creator.name}>
                        <Paper variant="outlined" sx={{ p: 2, textAlign: 'center', height: '100%' }}>
                            <Avatar sx={{ width: 64, height: 64, mb: 1, mx: 'auto', bgcolor: 'primary.main', fontSize: '2rem' }}>{creator.avatar}</Avatar>
                            <Typography variant="h6">{creator.name}</Typography>
                            <Typography variant="body2" color="textSecondary">{creator.role}</Typography>
                            <Box sx={{ mt: 1.5 }}>
                                <Button startIcon={<GitHubIcon />} href={creator.github} target="_blank" size="small">GitHub</Button>
                                <Button startIcon={<LinkedInIcon />} href={creator.linkedin} target="_blank" size="small">LinkedIn</Button>
                            </Box>
                        </Paper>
                    </Grid>
                ))}
            </Grid>

            <Divider sx={{ my: 3 }} />

            <Typography variant="h5" gutterBottom>Core Technology</Typography>
            <Typography variant="body2" color="textSecondary" sx={{mb: 2}}>
                This project is powered by several incredible, developer-friendly AI and cloud services.
            </Typography>
            <Grid container spacing={3} alignItems="stretch">
                {technologies.map(tech => (
                    <Grid item xs={12} sm={6} key={tech.name}>
                         <Link href={tech.siteUrl} target="_blank" rel="noopener noreferrer" underline="none" sx={{ display: 'block', height: '100%' }}>
                            <Paper variant="outlined" sx={{ p: 3, height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', '&:hover': {boxShadow: 3} }}>
                                <Box sx={{ textAlign: 'center' }}>
                                    <Typography variant="caption" color="text.secondary" component="div" sx={{ mb: 1.5 }}>Powered by</Typography>
                                    <img src={tech.logo} alt={`${tech.name} Logo`} style={{ maxHeight: '40px', maxWidth: '150px' }} />
                                </Box>
                            </Paper>
                        </Link>
                    </Grid>
                ))}
            </Grid>
        </Paper>
    );
}