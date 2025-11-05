import React from 'react';
import { Card, CardHeader, CardContent, Stack, TextField } from '@mui/material';

/**
 * Form section for capturing company information including address details
 * Handles company name, address, and location fields in a vertical layout
 */
const CompanyInfoForm = ({ companyInfo, onChange }) => {
    const handleChange = (field) => (event) => {
        onChange(field, event.target.value);
    };

    return (
        <Card sx={{ mb: 3 }}>
            <CardHeader title="Company Information" />
            <CardContent>
                <Stack spacing={3}>
                    <TextField
                        label="Company Name *"
                        value={companyInfo.name}
                        onChange={handleChange('name')}
                        fullWidth
                        required
                    />
                    <TextField
                        label="Address *"
                        value={companyInfo.address}
                        onChange={handleChange('address')}
                        fullWidth
                        required
                    />
                    <Stack direction={{ xs: 'column', sm: 'row' }} spacing={3}>
                        <TextField
                            label="City"
                            value={companyInfo.city}
                            onChange={handleChange('city')}
                            fullWidth
                        />
                        <TextField
                            label="State"
                            value={companyInfo.state}
                            onChange={handleChange('state')}
                            fullWidth
                        />
                    </Stack>
                    <Stack direction={{ xs: 'column', sm: 'row' }} spacing={3}>
                        <TextField
                            label="ZIP Code"
                            value={companyInfo.zip_code}
                            onChange={handleChange('zip_code')}
                            fullWidth
                        />
                        <TextField
                            label="Country"
                            value={companyInfo.country}
                            onChange={handleChange('country')}
                            fullWidth
                        />
                    </Stack>
                </Stack>
            </CardContent>
        </Card>
    );
};

export default CompanyInfoForm;
