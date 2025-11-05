import { Paper, Typography, Box, Alert, Divider } from '@mui/material';
import { Info as InfoIcon } from '@mui/icons-material';

/**
 * TestCredentials Component
 *
 * Displays a formatted card with test login credentials for different user roles.
 * Used for demonstration and testing purposes during development.
 *
 */
function TestCredentialsBanner() {
    const credentials = [
        {
            role: 'Customer Service',
            username: 'cservice',
            password: 'cservice',
        },
        { role: 'Customer', username: 'customer', password: 'customer' },
    ];

    return (
        <Paper elevation={2} sx={{ p: 3, maxWidth: 500, mx: 'auto', mt: 1 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <InfoIcon color="info" sx={{ mr: 1 }} />
                <Typography variant="h6" component="h2">
                    Test Credentials
                </Typography>
            </Box>

            <Alert severity="info" sx={{ mb: 3 }}>
                Use these credentials to test the application:
            </Alert>

            {credentials.map((cred, index) => (
                <Box key={cred.role}>
                    <Typography
                        variant="subtitle1"
                        fontWeight="bold"
                        color="primary"
                        gutterBottom
                    >
                        {cred.role}
                    </Typography>
                    <Box sx={{ pl: 2, mb: 2 }}>
                        <Typography variant="body2">
                            <strong>Username:</strong> {cred.username}
                        </Typography>
                        <Typography variant="body2">
                            <strong>Password:</strong> {cred.password}
                        </Typography>
                    </Box>
                    {index < credentials.length - 1 && (
                        <Divider sx={{ my: 2 }} />
                    )}
                </Box>
            ))}
        </Paper>
    );
}

export default TestCredentialsBanner;
