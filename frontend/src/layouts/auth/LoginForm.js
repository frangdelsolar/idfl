import React, { useState } from 'react';
import { useApi } from '../../context/ApiContext';
import {
    Box,
    Paper,
    TextField,
    Button,
    Typography,
    Alert,
    CircularProgress,
    Container,
    Card,
    CardContent,
} from '@mui/material';
import { Lock as LockIcon } from '@mui/icons-material';

const LoginForm = () => {
    const { auth } = useApi();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            await auth.login(username, password);
        } catch (err) {
            setError(
                err.detail || 'Login failed. Please check your credentials.'
            );
        } finally {
            setLoading(false);
        }
    };

    if (auth.isAuthenticated) {
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
                    <Card sx={{ width: '100%', p: 3 }}>
                        <CardContent sx={{ textAlign: 'center' }}>
                            <Typography
                                component="h1"
                                variant="h4"
                                color="success.main"
                                gutterBottom
                            >
                                Welcome!
                            </Typography>
                            <Typography
                                variant="body1"
                                color="text.secondary"
                                paragraph
                            >
                                You are successfully logged in.
                            </Typography>
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
        <Container component="main" maxWidth="xs">
            <Box
                sx={{
                    marginTop: 8,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                }}
            >
                <Paper elevation={3} sx={{ padding: 4, width: '100%' }}>
                    <Box sx={{ textAlign: 'center', mb: 3 }}>
                        <LockIcon
                            sx={{ fontSize: 40, color: 'primary.main', mb: 1 }}
                        />
                        <Typography component="h1" variant="h4" gutterBottom>
                            Sign In
                        </Typography>
                        <Typography variant="body1" color="text.secondary">
                            Login to Product Certification
                        </Typography>
                    </Box>

                    <Box
                        component="form"
                        onSubmit={handleSubmit}
                        sx={{ mt: 1 }}
                    >
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            id="username"
                            label="Username"
                            name="username"
                            autoComplete="username"
                            autoFocus
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            disabled={loading}
                        />
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            name="password"
                            label="Password"
                            type="password"
                            id="password"
                            autoComplete="current-password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            disabled={loading}
                        />
                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            sx={{ mt: 3, mb: 2 }}
                            disabled={loading}
                            size="large"
                        >
                            {loading ? (
                                <CircularProgress size={24} color="inherit" />
                            ) : (
                                'Sign In'
                            )}
                        </Button>

                        {error && (
                            <Alert severity="error" sx={{ mt: 2 }}>
                                {error}
                            </Alert>
                        )}
                    </Box>
                </Paper>
            </Box>
        </Container>
    );
};

export default LoginForm;
