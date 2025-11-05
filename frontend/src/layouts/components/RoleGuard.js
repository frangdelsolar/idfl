import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useApi } from '../../context/ApiContext';
import { CircularProgress, Box } from '@mui/material';

/**
 * Protects routes by verifying user authentication and role permissions
 * Redirects unauthorized users to login or unauthorized pages
 * Shows loading state during authentication checks
 */
function RoleGuard({ children, requiredRole }) {
    const { auth } = useApi();
    const navigate = useNavigate();

    /**
     * Handle authentication and role-based routing
     * Redirects to login if not authenticated
     * Redirects to unauthorized page if wrong role
     */
    useEffect(() => {
        if (!auth.isAuthenticated) {
            navigate('/login');
            return;
        }

        if (auth.user?.role !== requiredRole) {
            navigate('/unauthorized');
            return;
        }
    }, [auth.isAuthenticated, auth.user?.role, requiredRole, navigate]);

    /**
     * Show loading spinner while authentication is being initialized
     * Prevents flash of unauthorized content
     */
    if (!auth.isInitialized) {
        return (
            <Box
                display="flex"
                justifyContent="center"
                alignItems="center"
                minHeight="200px"
            >
                <CircularProgress />
            </Box>
        );
    }

    /**
     * Show loading spinner during redirects or if access is denied
     * Provides better UX than immediate redirect without feedback
     */
    if (!auth.isAuthenticated || auth.user?.role !== requiredRole) {
        return (
            <Box
                display="flex"
                justifyContent="center"
                alignItems="center"
                minHeight="200px"
            >
                <CircularProgress />
            </Box>
        );
    }

    /**
     * Render protected content only when user is authenticated and has correct role
     */
    return children;
}

export default RoleGuard;
