import { Outlet } from 'react-router-dom';
import { Box, Container, CssBaseline } from '@mui/material';
import Header from './components/Header';
import Footer from './components/Footer';

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

                {/* Main Content */}
                <Box
                    component="main"
                    sx={{
                        flexGrow: 1,
                        py: 3,
                    }}
                >
                    <Container maxWidth="lg">
                        <Outlet />
                    </Container>
                </Box>

                <Footer />
            </Box>
        </>
    );
}

export default MainLayout;
