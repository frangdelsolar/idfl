import React, { useState, useEffect } from 'react';
import {
    FormControl,
    InputLabel,
    Select,
    MenuItem,
    CircularProgress,
    FormHelperText,
    Box,
    Alert,
} from '@mui/material';
import PropTypes from 'prop-types';
import { useApi } from '../context/ApiContext';

/**
 * Dropdown component for selecting companies from API data
 * Handles loading states, errors, and provides selection interface
 */
const CompanyDropdown = ({
    value,
    onChange,
    label = 'Company',
    required = false,
    disabled = false,
    error = null,
    helperText = null,
    sx = {},
    showLoading = true,
    emptyMessage = 'No companies available',
}) => {
    const { companies: companyService } = useApi();
    const [companies, setCompanies] = useState([]);
    const [loading, setLoading] = useState(false);
    const [fetchError, setFetchError] = useState(null);

    useEffect(() => {
        const fetchCompanies = async () => {
            if (!companyService) {
                setFetchError('Company service not available');
                return;
            }

            setLoading(true);
            setFetchError(null);

            try {
                const response = await companyService.listCompanies();
                setCompanies(response.data || response || []);
            } catch (err) {
                console.error('Error fetching companies:', err);
                setFetchError('Failed to load companies. Please try again.');
                setCompanies([]);
            } finally {
                setLoading(false);
            }
        };

        fetchCompanies();
    }, [companyService]);

    const handleChange = (event) => {
        const selectedValue = event.target.value;
        const selectedCompany = companies.find(
            (company) => company.id.toString() === selectedValue.toString()
        );
        onChange(selectedValue, selectedCompany);
    };

    if (loading && showLoading) {
        return (
            <Box display="flex" alignItems="center" sx={sx}>
                <CircularProgress size={24} />
                <Box ml={2}>Loading companies...</Box>
            </Box>
        );
    }

    if (fetchError && !loading) {
        return (
            <Alert severity="error" sx={sx}>
                {fetchError}
            </Alert>
        );
    }

    return (
        <FormControl
            fullWidth
            required={required}
            disabled={disabled || loading}
            error={!!error || !!fetchError}
            sx={sx}
        >
            <InputLabel id="company-select-label">{label}</InputLabel>
            <Select
                labelId="company-select-label"
                id="company-select"
                value={value || ''}
                label={label}
                onChange={handleChange}
                displayEmpty
                renderValue={(selected) => {
                    if (!selected) {
                        return <em>Select a company...</em>;
                    }
                    const selectedCompany = companies.find(
                        (company) =>
                            company.id.toString() === selected.toString()
                    );
                    return selectedCompany
                        ? selectedCompany.name
                        : 'Unknown company';
                }}
                MenuProps={{
                    PaperProps: {
                        sx: {
                            maxHeight: 300,
                            '& .MuiMenuItem-root': {
                                padding: '8px 16px',
                            },
                        },
                    },
                }}
            >
                <MenuItem value="">
                    <em>Select a company...</em>
                </MenuItem>

                {companies.length === 0 && !loading ? (
                    <MenuItem disabled>{emptyMessage}</MenuItem>
                ) : (
                    companies.map((company) => (
                        <MenuItem key={company.id} value={company.id}>
                            {company.name}
                        </MenuItem>
                    ))
                )}
            </Select>

            {(helperText || fetchError) && (
                <FormHelperText>{fetchError || helperText}</FormHelperText>
            )}
        </FormControl>
    );
};

CompanyDropdown.propTypes = {
    value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    onChange: PropTypes.func.isRequired,
    label: PropTypes.string,
    required: PropTypes.bool,
    disabled: PropTypes.bool,
    error: PropTypes.bool,
    helperText: PropTypes.string,
    sx: PropTypes.object,
    showLoading: PropTypes.bool,
    emptyMessage: PropTypes.string,
};

export default CompanyDropdown;
