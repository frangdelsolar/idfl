import { Box, Typography, Button, Container, Paper } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { Warning as WarningIcon } from '@mui/icons-material';

function UnauthorizedPage() {
    const navigate = useNavigate();

    return (
        <Container component="main" maxWidth="sm">
            <Box
                sx={{
                    marginTop: 8,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                }}
            >
                <Paper
                    elevation={3}
                    sx={{ p: 4, width: '100%', textAlign: 'center' }}
                >
                    <WarningIcon color="error" sx={{ fontSize: 64, mb: 2 }} />

                    <Typography variant="h4" color="error" gutterBottom>
                        Access Denied
                    </Typography>

                    <Typography
                        variant="body1"
                        color="text.secondary"
                        paragraph
                    >
                        You don't have permission to access this page.
                    </Typography>

                    <Typography
                        variant="body2"
                        color="text.secondary"
                        sx={{ mb: 3 }}
                    >
                        Please contact your administrator if you believe this is
                        an error.
                    </Typography>

                    <Box
                        sx={{
                            display: 'flex',
                            gap: 2,
                            justifyContent: 'center',
                            flexWrap: 'wrap',
                        }}
                    >
                        <Button
                            variant="contained"
                            onClick={() => navigate('/')}
                        >
                            Go to Home
                        </Button>
                        <Button variant="outlined" onClick={() => navigate(-1)}>
                            Go Back
                        </Button>
                        <Button
                            variant="text"
                            onClick={() => navigate('/login')}
                        >
                            Sign In as Different User
                        </Button>
                    </Box>
                </Paper>
            </Box>
        </Container>
    );
}

export default UnauthorizedPage;
