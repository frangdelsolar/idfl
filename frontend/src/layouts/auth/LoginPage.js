import {
    Box,
    Container,
    Card,
    CardContent,
    Typography,
    Button,
} from '@mui/material';
import LoginForm from './LoginForm';
import TestCredentialsBanner from './TestCredentialsBanner';
import { useApi } from '../../context/ApiContext';

/**
 * Login page with role-based post-login dashboard and two-column layout for login form
 * Shows welcome message with role-specific instructions when authenticated
 * Displays credentials banner and login form side-by-side when not authenticated
 */
function LoginPage() {
    const { auth } = useApi();

    if (auth.isAuthenticated) {
        return (
            <Container component="main" maxWidth="md">
                <Box
                    sx={{
                        marginTop: 8,
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                    }}
                >
                    <Card sx={{ width: '100%', p: 3 }}>
                        <CardContent sx={{ textAlign: 'center' }}>
                            <Typography
                                component="h1"
                                variant="h4"
                                color="success.main"
                                gutterBottom
                            >
                                Welcome, {auth.user?.username}!
                            </Typography>
                            <Typography variant="h6" color="primary" paragraph>
                                Your role: <strong>{auth.user?.role}</strong>
                            </Typography>

                            {auth.user?.role === 'customer' && (
                                <Typography
                                    variant="body1"
                                    color="text.secondary"
                                    paragraph
                                >
                                    Click the <strong>Customer</strong> tab to
                                    submit certification applications.
                                </Typography>
                            )}

                            {auth.user?.role === 'cservice' && (
                                <Typography
                                    variant="body1"
                                    color="text.secondary"
                                    paragraph
                                >
                                    Click the <strong>Customer Service</strong>{' '}
                                    tab to create customer profiles.
                                </Typography>
                            )}

                            {auth.user?.role === 'reviewer' && (
                                <Typography
                                    variant="body1"
                                    color="text.secondary"
                                    paragraph
                                >
                                    Click the <strong>Reviewer</strong> tab to
                                    review applications.
                                </Typography>
                            )}

                            <Button
                                variant="contained"
                                color="error"
                                size="large"
                                onClick={auth.logout}
                                sx={{ mt: 2 }}
                            >
                                Logout
                            </Button>
                        </CardContent>
                    </Card>
                </Box>
            </Container>
        );
    }

    return (
        <Container component="main" maxWidth="lg">
            <Box
                sx={{
                    marginTop: 4,
                    display: 'flex',
                    flexDirection: 'row',
                    gap: 4,
                    alignItems: 'center',
                    justifyContent: 'center',
                }}
            >
                <Box sx={{ flex: 1 }}>
                    <TestCredentialsBanner />
                </Box>
                <Box sx={{ flex: 1 }}>
                    <LoginForm />
                </Box>
            </Box>
        </Container>
    );
}

export default LoginPage;
