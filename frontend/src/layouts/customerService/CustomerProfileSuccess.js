import React from 'react';
import {
    Card,
    CardContent,
    Typography,
    Box,
    Chip,
    Divider,
} from '@mui/material';
import {
    Person as PersonIcon,
    Business as BusinessIcon,
    Email as EmailIcon,
    Phone as PhoneIcon,
    Group as GroupIcon,
} from '@mui/icons-material';

/**
 * Displays customer profile creation success details in a formatted card
 * Shows user information, company details, and role assignment
 */
const CustomerProfileSuccess = ({ responseData }) => {
    return (
        <Card
            sx={{
                mb: 3,
                border: '1px solid #4caf50',
                backgroundColor: '#f8fff8',
            }}
        >
            <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <PersonIcon color="success" sx={{ mr: 1 }} />
                    <Typography variant="h6" color="success.main">
                        ✅ Profile Created Successfully
                    </Typography>
                </Box>

                <Divider sx={{ mb: 2 }} />

                {/* User Information */}
                <Box sx={{ mb: 3 }}>
                    <Typography
                        variant="subtitle1"
                        fontWeight="bold"
                        gutterBottom
                    >
                        User Details
                    </Typography>
                    <Box sx={{ pl: 2 }}>
                        <Box
                            sx={{
                                display: 'flex',
                                alignItems: 'center',
                                mb: 1,
                            }}
                        >
                            <PersonIcon
                                sx={{
                                    fontSize: 16,
                                    mr: 1,
                                    color: 'text.secondary',
                                }}
                            />
                            <Typography variant="body2">
                                <strong>Name:</strong> {responseData.first_name}{' '}
                                {responseData.last_name}
                            </Typography>
                        </Box>
                        <Box
                            sx={{
                                display: 'flex',
                                alignItems: 'center',
                                mb: 1,
                            }}
                        >
                            <EmailIcon
                                sx={{
                                    fontSize: 16,
                                    mr: 1,
                                    color: 'text.secondary',
                                }}
                            />
                            <Typography variant="body2">
                                <strong>Email:</strong> {responseData.email}
                            </Typography>
                        </Box>
                        <Box
                            sx={{
                                display: 'flex',
                                alignItems: 'center',
                                mb: 1,
                            }}
                        >
                            <PersonIcon
                                sx={{
                                    fontSize: 16,
                                    mr: 1,
                                    color: 'text.secondary',
                                }}
                            />
                            <Typography variant="body2">
                                <strong>Username:</strong>{' '}
                                {responseData.username}
                            </Typography>
                        </Box>
                        {responseData.phone_number && (
                            <Box
                                sx={{
                                    display: 'flex',
                                    alignItems: 'center',
                                    mb: 1,
                                }}
                            >
                                <PhoneIcon
                                    sx={{
                                        fontSize: 16,
                                        mr: 1,
                                        color: 'text.secondary',
                                    }}
                                />
                                <Typography variant="body2">
                                    <strong>Phone:</strong>{' '}
                                    {responseData.phone_number}
                                </Typography>
                            </Box>
                        )}
                    </Box>
                </Box>

                {/* Company Information */}
                <Box sx={{ mb: 3 }}>
                    <Typography
                        variant="subtitle1"
                        fontWeight="bold"
                        gutterBottom
                    >
                        Company Information
                    </Typography>
                    <Box sx={{ pl: 2 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                            <BusinessIcon
                                sx={{
                                    fontSize: 16,
                                    mr: 1,
                                    color: 'text.secondary',
                                }}
                            />
                            <Typography variant="body2">
                                <strong>Company:</strong> {responseData.company}
                            </Typography>
                        </Box>
                    </Box>
                </Box>

                {/* Role and Groups */}
                <Box sx={{ mb: 2 }}>
                    <Typography
                        variant="subtitle1"
                        fontWeight="bold"
                        gutterBottom
                    >
                        Role & Permissions
                    </Typography>
                    <Box sx={{ pl: 2 }}>
                        <Box
                            sx={{
                                display: 'flex',
                                alignItems: 'center',
                                mb: 1,
                            }}
                        >
                            <GroupIcon
                                sx={{
                                    fontSize: 16,
                                    mr: 1,
                                    color: 'text.secondary',
                                }}
                            />
                            <Typography variant="body2">
                                <strong>Role:</strong>
                                <Chip
                                    label={responseData.role}
                                    size="small"
                                    color="primary"
                                    sx={{ ml: 1 }}
                                />
                            </Typography>
                        </Box>
                        <Box
                            sx={{
                                display: 'flex',
                                alignItems: 'center',
                                flexWrap: 'wrap',
                                gap: 0.5,
                            }}
                        >
                            <GroupIcon
                                sx={{
                                    fontSize: 16,
                                    mr: 1,
                                    color: 'text.secondary',
                                }}
                            />
                            <Typography variant="body2" sx={{ mr: 1 }}>
                                <strong>Groups:</strong>
                            </Typography>
                            {responseData.groups.map((group, index) => (
                                <Chip
                                    key={index}
                                    label={group}
                                    size="small"
                                    variant="outlined"
                                    color="secondary"
                                />
                            ))}
                        </Box>
                    </Box>
                </Box>

                {/* Success Message */}
                <Box
                    sx={{
                        mt: 2,
                        p: 1,
                        backgroundColor: '#e8f5e8',
                        borderRadius: 1,
                    }}
                >
                    <Typography
                        variant="body2"
                        color="success.dark"
                        fontStyle="italic"
                    >
                        {responseData.message}
                    </Typography>
                </Box>
            </CardContent>
        </Card>
    );
};

export default CustomerProfileSuccess;
