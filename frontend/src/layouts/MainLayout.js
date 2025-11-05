import { Outlet } from 'react-router-dom';
import { Box, CssBaseline } from '@mui/material';
import Header from './components/Header';
import Footer from './components/Footer';

/**
 * Main application layout component providing consistent structure across all pages
 * Features header navigation, main content area, and footer in a flexbox layout
 */
function MainLayout() {
    return (
        <>
            <CssBaseline />
            <Box
                sx={{
                    display: 'flex',
                    flexDirection: 'column',
                    minHeight: '100vh',
                    backgroundColor: '#f5f5f5',
                }}
            >
                <Header />

                <Box
                    component="main"
                    sx={{
                        flexGrow: 1,
                        display: 'flex',
                        flexDirection: 'row',
                        justifyContent: 'center',
                        alignItems: 'center',
                    }}
                >
                    <Outlet />
                </Box>

                <Footer />
            </Box>
        </>
    );
}

export default MainLayout;
