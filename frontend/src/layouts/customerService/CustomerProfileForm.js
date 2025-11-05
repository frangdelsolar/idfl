import React, { useState } from 'react';
import {
    Container,
    Button,
    Box,
    Typography,
    TextField,
    Paper,
    Alert,
} from '@mui/material';
import CompanyDropdown from '../../shared/CompanyDropdown';
import CustomerProfileSuccess from './CustomerProfileSuccess';
import { useApi } from '../../context/ApiContext';

/**
 * Form component for creating new customer profiles
 * Handles company selection, user details input, and API submission
 * Displays success response using CustomerProfileSuccess component
 */
const CustomerProfileForm = () => {
    const { customerProfiles } = useApi();
    const [selectedCompany, setSelectedCompany] = useState('');
    const [formData, setFormData] = useState({
        firstName: '',
        lastName: '',
        email: '',
        username: '',
        phoneNumber: '',
    });
    const [formError, setFormError] = useState('');
    const [submitLoading, setSubmitLoading] = useState(false);
    const [creationResponse, setCreationResponse] = useState(null);

    const handleCompanyChange = (companyId, company) => {
        setSelectedCompany(companyId);
        setFormError('');
    };

    const handleInputChange = (field) => (event) => {
        setFormData((prev) => ({
            ...prev,
            [field]: event.target.value,
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!selectedCompany) {
            setFormError('Please select a company');
            return;
        }

        if (
            !formData.firstName ||
            !formData.lastName ||
            !formData.email ||
            !formData.username
        ) {
            setFormError('Please fill in all required fields');
            return;
        }

        setSubmitLoading(true);
        setFormError('');
        setCreationResponse(null);

        try {
            const payload = {
                company_id: selectedCompany,
                first_name: formData.firstName,
                last_name: formData.lastName,
                email: formData.email,
                username: formData.username,
                phone_number: formData.phoneNumber,
            };

            const response = await customerProfiles.createCustomerProfile(
                payload
            );
            setCreationResponse(response);

            setSelectedCompany('');
            setFormData({
                firstName: '',
                lastName: '',
                email: '',
                username: '',
                phoneNumber: '',
            });
        } catch (error) {
            console.error('Error creating customer:', error);
            setFormError(
                'Failed to create customer profile. Please try again.'
            );
        } finally {
            setSubmitLoading(false);
        }
    };

    return (
        <Container maxWidth="md">
            <Paper elevation={3} sx={{ p: 4, mt: 4 }}>
                <Typography variant="h4" gutterBottom align="center">
                    Create Customer Profile
                </Typography>

                {formError && (
                    <Alert severity="error" sx={{ mb: 3 }}>
                        {formError}
                    </Alert>
                )}

                {creationResponse && (
                    <CustomerProfileSuccess responseData={creationResponse} />
                )}

                <Box component="form" onSubmit={handleSubmit}>
                    <CompanyDropdown
                        value={selectedCompany}
                        onChange={handleCompanyChange}
                        label="Company *"
                        required={true}
                        error={!!formError && !selectedCompany}
                        helperText={
                            formError && !selectedCompany
                                ? 'Company selection is required'
                                : ''
                        }
                        sx={{ mb: 3 }}
                    />

                    <Box display="flex" gap={2} sx={{ mb: 3 }}>
                        <TextField
                            label="First Name *"
                            value={formData.firstName}
                            onChange={handleInputChange('firstName')}
                            fullWidth
                            required
                        />
                        <TextField
                            label="Last Name *"
                            value={formData.lastName}
                            onChange={handleInputChange('lastName')}
                            fullWidth
                            required
                        />
                    </Box>

                    <Box display="flex" gap={2} sx={{ mb: 3 }}>
                        <TextField
                            label="Email *"
                            type="email"
                            value={formData.email}
                            onChange={handleInputChange('email')}
                            fullWidth
                            required
                        />
                        <TextField
                            label="Username *"
                            value={formData.username}
                            onChange={handleInputChange('username')}
                            fullWidth
                            required
                        />
                    </Box>

                    <TextField
                        label="Phone Number"
                        value={formData.phoneNumber}
                        onChange={handleInputChange('phoneNumber')}
                        fullWidth
                        sx={{ mb: 3 }}
                    />

                    <Button
                        type="submit"
                        variant="contained"
                        color="primary"
                        fullWidth
                        size="large"
                        disabled={submitLoading}
                    >
                        {submitLoading
                            ? 'Creating Customer...'
                            : 'Create Customer Profile'}
                    </Button>
                </Box>
            </Paper>
        </Container>
    );
};

export default CustomerProfileForm;
