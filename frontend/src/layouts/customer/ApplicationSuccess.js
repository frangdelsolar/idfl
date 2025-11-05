import React from 'react';
import {
    Card,
    CardContent,
    Typography,
    Box,
    Chip,
    Divider,
    Stack,
} from '@mui/material';
import {
    Business as BusinessIcon,
    Inventory as InventoryIcon,
    CheckCircle as CheckCircleIcon,
    LocationOn as LocationIcon,
} from '@mui/icons-material';

/**
 * Success banner component for displaying application submission details
 * Shows application information, company details, and supply chain partners
 */
const ApplicationSuccess = ({ responseData }) => {
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
                    <CheckCircleIcon color="success" sx={{ mr: 1 }} />
                    <Typography variant="h6" color="success.main">
                        ✅ Application Submitted Successfully
                    </Typography>
                </Box>

                <Divider sx={{ mb: 2 }} />

                {/* Application Information */}
                <Box sx={{ mb: 3 }}>
                    <Typography
                        variant="subtitle1"
                        fontWeight="bold"
                        gutterBottom
                    >
                        Application Details
                    </Typography>
                    <Stack spacing={1} sx={{ pl: 2 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                            <BusinessIcon
                                sx={{
                                    fontSize: 16,
                                    mr: 1,
                                    color: 'text.secondary',
                                }}
                            />
                            <Typography variant="body2">
                                <strong>Name:</strong> {responseData.name}
                            </Typography>
                        </Box>
                        {responseData.description && (
                            <Box
                                sx={{
                                    display: 'flex',
                                    alignItems: 'flex-start',
                                }}
                            >
                                <BusinessIcon
                                    sx={{
                                        fontSize: 16,
                                        mr: 1,
                                        color: 'text.secondary',
                                        mt: 0.5,
                                    }}
                                />
                                <Typography variant="body2">
                                    <strong>Description:</strong>{' '}
                                    {responseData.description}
                                </Typography>
                            </Box>
                        )}
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                            <InventoryIcon
                                sx={{
                                    fontSize: 16,
                                    mr: 1,
                                    color: 'text.secondary',
                                }}
                            />
                            <Typography variant="body2">
                                <strong>Status:</strong>
                                <Chip
                                    label={responseData.status}
                                    size="small"
                                    color="primary"
                                    sx={{ ml: 1, textTransform: 'capitalize' }}
                                />
                            </Typography>
                        </Box>
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                            <BusinessIcon
                                sx={{
                                    fontSize: 16,
                                    mr: 1,
                                    color: 'text.secondary',
                                }}
                            />
                            <Typography variant="body2">
                                <strong>Application ID:</strong>{' '}
                                {responseData.id}
                            </Typography>
                        </Box>
                    </Stack>
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
                    <Stack spacing={1} sx={{ pl: 2 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                            <BusinessIcon
                                sx={{
                                    fontSize: 16,
                                    mr: 1,
                                    color: 'text.secondary',
                                }}
                            />
                            <Typography variant="body2">
                                <strong>Company:</strong>{' '}
                                {responseData.company_info.name}
                            </Typography>
                        </Box>
                        <Box sx={{ display: 'flex', alignItems: 'flex-start' }}>
                            <LocationIcon
                                sx={{
                                    fontSize: 16,
                                    mr: 1,
                                    color: 'text.secondary',
                                    mt: 0.5,
                                }}
                            />
                            <Typography variant="body2">
                                <strong>Address:</strong>{' '}
                                {responseData.company_info.address},{' '}
                                {responseData.company_info.city},{' '}
                                {responseData.company_info.state}{' '}
                                {responseData.company_info.zip_code},{' '}
                                {responseData.company_info.country}
                            </Typography>
                        </Box>
                    </Stack>
                </Box>

                {/* Supply Chain Partners */}
                <Box sx={{ mb: 2 }}>
                    <Typography
                        variant="subtitle1"
                        fontWeight="bold"
                        gutterBottom
                    >
                        Supply Chain Partners (
                        {responseData.supply_chain_partners.length})
                    </Typography>
                    <Stack spacing={2} sx={{ pl: 2 }}>
                        {responseData.supply_chain_partners.map(
                            (partner, index) => (
                                <Box
                                    key={partner.id}
                                    sx={{
                                        p: 1,
                                        backgroundColor: '#f0f0f0',
                                        borderRadius: 1,
                                    }}
                                >
                                    <Typography
                                        variant="body2"
                                        fontWeight="medium"
                                        gutterBottom
                                    >
                                        Partner #{index + 1}: {partner.name}
                                    </Typography>
                                    <Typography
                                        variant="body2"
                                        color="text.secondary"
                                    >
                                        {partner.address}, {partner.city},{' '}
                                        {partner.state} {partner.zip_code},{' '}
                                        {partner.country}
                                    </Typography>
                                </Box>
                            )
                        )}
                    </Stack>
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
                        Your application has been received and is now under
                        review.
                    </Typography>
                </Box>
            </CardContent>
        </Card>
    );
};

export default ApplicationSuccess;
