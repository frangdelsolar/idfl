import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';
import { useApi } from '../../context/ApiContext';

const loginPath = '/auth/login';

/**
 * Application header with navigation and authentication controls
 * Displays role-based navigation items and login/logout functionality
 */
function Header() {
    const navigate = useNavigate();
    const location = useLocation();
    const { auth } = useApi();

    const navigationItems = [
        { label: 'Customer', path: '/customer' },
        { label: 'Customer Service', path: '/customer-service' },
    ];

    return (
        <AppBar position="static" elevation={2}>
            <Toolbar>
                <Typography
                    variant="h6"
                    component="div"
                    sx={{ flexGrow: 1, cursor: 'pointer' }}
                    onClick={() => navigate('/')}
                >
                    Product Certification
                </Typography>

                <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
                    {navigationItems.map((item) => (
                        <Button
                            key={item.path}
                            color="inherit"
                            variant={
                                location.pathname === item.path
                                    ? 'outlined'
                                    : 'text'
                            }
                            onClick={() => navigate(item.path)}
                            sx={{
                                fontWeight:
                                    location.pathname === item.path
                                        ? 'bold'
                                        : 'normal',
                                border:
                                    location.pathname === item.path
                                        ? '1px solid white'
                                        : 'none',
                                '&:hover': {
                                    backgroundColor: 'rgba(255, 255, 255, 0.1)',
                                },
                            }}
                        >
                            {item.label}
                        </Button>
                    ))}

                    {auth.isAuthenticated ? (
                        <Button
                            color="inherit"
                            onClick={auth.logout}
                            sx={{
                                marginLeft: 2,
                                border: '1px solid rgba(255, 255, 255, 0.5)',
                                '&:hover': {
                                    backgroundColor: 'rgba(255, 255, 255, 0.2)',
                                },
                            }}
                        >
                            Logout
                        </Button>
                    ) : (
                        <Button
                            color="inherit"
                            onClick={() => navigate(loginPath)}
                            variant={
                                location.pathname === loginPath
                                    ? 'outlined'
                                    : 'text'
                            }
                            sx={{
                                marginLeft: 2,
                                fontWeight:
                                    location.pathname === loginPath
                                        ? 'bold'
                                        : 'normal',
                                border:
                                    location.pathname === loginPath
                                        ? '1px solid white'
                                        : 'none',
                                '&:hover': {
                                    backgroundColor: 'rgba(255, 255, 255, 0.1)',
                                },
                            }}
                        >
                            Login
                        </Button>
                    )}
                </Box>
            </Toolbar>
        </AppBar>
    );
}

export default Header;
