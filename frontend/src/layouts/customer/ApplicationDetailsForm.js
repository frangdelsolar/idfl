import React from 'react';
import { Card, CardHeader, CardContent, Stack, TextField } from '@mui/material';

/**
 * Form section for capturing basic application information
 * Includes application name and description fields
 */
const ApplicationDetailsForm = ({ applicationData, onChange }) => {
    const handleChange = (field) => (event) => {
        onChange(field, event.target.value);
    };

    return (
        <Card sx={{ mb: 3 }}>
            <CardHeader title="Application Details" />
            <CardContent>
                <Stack spacing={3}>
                    <TextField
                        label="Application Name *"
                        value={applicationData.name}
                        onChange={handleChange('name')}
                        fullWidth
                        required
                    />
                    <TextField
                        label="Description"
                        value={applicationData.description}
                        onChange={handleChange('description')}
                        fullWidth
                        multiline
                        rows={3}
                        placeholder="Describe your application and products..."
                    />
                </Stack>
            </CardContent>
        </Card>
    );
};

export default ApplicationDetailsForm;
