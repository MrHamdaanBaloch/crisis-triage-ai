import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link, useLocation } from 'react-router-dom';
import { Box, Drawer, List, ListItem, ListItemButton, ListItemIcon, ListItemText, CssBaseline, Toolbar, Typography, Divider, Button, AppBar } from '@mui/material'; // Added AppBar
import DashboardIcon from '@mui/icons-material/Dashboard';
import AddAlertIcon from '@mui/icons-material/AddAlert';
import TravelExploreIcon from '@mui/icons-material/TravelExplore';
import CampaignIcon from '@mui/icons-material/Campaign';
import InfoIcon from '@mui/icons-material/Info';

// Import Page Components
import Dashboard from './pages/Dashboard';
import ReportIncident from './pages/ReportIncident';
import CrisisMap from './pages/CrisisMap';
import GenerateAppeal from './pages/GenerateAppeal';
import About from './pages/About';

const drawerWidth = 240;

const pages = [
  { text: 'Dashboard', path: '/', icon: <DashboardIcon /> },
  { text: 'Crisis Map', path: '/map', icon: <TravelExploreIcon /> },
  { text: 'Generate Appeal', path: '/appeal', icon: <CampaignIcon /> },
  { text: 'About & Credits', path: '/about', icon: <InfoIcon /> } 
];

// --- NEW FOOTER COMPONENT ---
// A clean, reusable footer component.
function Footer() {
    return (
        <Box component="footer" sx={{ p: 2, mt: 'auto', backgroundColor: 'transparent' }}>
            <Typography variant="body2" color="text.secondary" align="center">
                {'Backend & System Architecture by '}
                <a style={{color: '#1976d2', textDecoration: 'none'}} href="https://github.com/mrHamdaanbaloch" target="_blank" rel="noopener noreferrer">
                    Hamdaan Baloch
                </a>
                {' | Presented by Saad.'}
            </Typography>
        </Box>
    );
}

function MainLayout() {
    const location = useLocation();
    return (
        <Box sx={{ display: 'flex' }}>
            <CssBaseline />
            <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1, backgroundColor: '#1d3557' }}>
                <Toolbar>
                    <Typography variant="h6" noWrap component="div">
                        CrisisTriage AI
                    </Typography>
                </Toolbar>
            </AppBar>
            <Drawer
                variant="permanent"
                sx={{
                    width: drawerWidth,
                    flexShrink: 0,
                    [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
                }}
            >
                <Toolbar />
                <Box sx={{ p: 2 }}>
                    <Button variant="contained" fullWidth component={Link} to="/report" startIcon={<AddAlertIcon />}>
                        Report Incident
                    </Button>
                </Box>
                <Divider />
                <List>
                    {pages.map((page) => (
                        <ListItem key={page.text} disablePadding>
                            <ListItemButton component={Link} to={page.path} selected={location.pathname === page.path}>
                                <ListItemIcon>{page.icon}</ListItemIcon>
                                <ListItemText primary={page.text} />
                            </ListItemButton>
                        </ListItem>
                    ))}
                </List>
            </Drawer>
            <Box 
                component="main" 
                sx={{ 
                    flexGrow: 1, 
                    p: 3, 
                    backgroundColor: '#f4f6f8', 
                    display: 'flex', // Added for footer layout
                    flexDirection: 'column', // Added for footer layout
                    minHeight: '100vh' 
                }}
            >
                <Toolbar /> {/* This pushes the content below the top app bar */}
                
                {/* Main content area */}
                <Box sx={{ flexGrow: 1 }}>
                    <Routes>
                        <Route path="/" element={<Dashboard />} />
                        <Route path="/map" element={<CrisisMap />} />
                        <Route path="/appeal" element={<GenerateAppeal />} />
                        <Route path="/about" element={<About />} />
                    </Routes>
                </Box>

                {/* --- ADD THE FOOTER HERE --- */}
                <Footer />
            </Box>
        </Box>
    );
}

export default function Root() {
  return (
    <Router>
        <Routes>
            {/* The public report page has no main layout */}
            <Route path="/report" element={<ReportIncident />} />
            {/* All other routes use the main layout with the sidebar and footer */}
            <Route path="*" element={<MainLayout />} />
        </Routes>
    </Router>
  );
}