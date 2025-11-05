import React, { useState } from 'react';
import {
    Container,
    Paper,
    Typography,
    Button,
    Box,
    Card,
    CardHeader,
    Alert,
} from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import { useApi } from '../../context/ApiContext';
import ApplicationDetailsForm from './ApplicationDetailsForm';
import CompanyInfoForm from './CompanyInfoForm';
import SupplyChainPartnerForm from './SupplyChainPartnerForm';
import {
    EMPTY_APPLICATION_STATE,
    EMPTY_PARTNER_STATE,
    EMPTY_PRODUCT_STATE,
} from '../../constants/applicationForm';
import ApplicationSuccess from './ApplicationSuccess';

/**
 * Main application form component for product certification submissions
 * Manages complex nested form state for applications, company info, and supply chain partners
 */
const ApplicationForm = () => {
    const { applications } = useApi();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);
    const [formData, setFormData] = useState(EMPTY_APPLICATION_STATE);
    const [creationResponse, setCreationResponse] = useState(null);

    const handleApplicationChange = (field, value) => {
        setFormData((prev) => ({
            ...prev,
            [field]: value,
        }));
    };

    const handleCompanyInfoChange = (field, value) => {
        setFormData((prev) => ({
            ...prev,
            company_info: {
                ...prev.company_info,
                [field]: value,
            },
        }));
    };

    const handlePartnerChange = (partnerIndex, field, value) => {
        setFormData((prev) => ({
            ...prev,
            supply_chain_partners: prev.supply_chain_partners.map(
                (partner, index) =>
                    index === partnerIndex
                        ? { ...partner, [field]: value }
                        : partner
            ),
        }));
    };

    const addSupplyChainPartner = () => {
        setFormData((prev) => ({
            ...prev,
            supply_chain_partners: [
                ...prev.supply_chain_partners,
                { ...EMPTY_PARTNER_STATE },
            ],
        }));
    };

    const removeSupplyChainPartner = (partnerIndex) => {
        setFormData((prev) => ({
            ...prev,
            supply_chain_partners: prev.supply_chain_partners.filter(
                (_, index) => index !== partnerIndex
            ),
        }));
    };

    const handleProductChange = (partnerIndex, productIndex, field, value) => {
        setFormData((prev) => ({
            ...prev,
            supply_chain_partners: prev.supply_chain_partners.map(
                (partner, pIndex) =>
                    pIndex === partnerIndex
                        ? {
                              ...partner,
                              products: partner.products.map(
                                  (product, prIndex) =>
                                      prIndex === productIndex
                                          ? { ...product, [field]: value }
                                          : product
                              ),
                          }
                        : partner
            ),
        }));
    };

    const addProduct = (partnerIndex) => {
        setFormData((prev) => ({
            ...prev,
            supply_chain_partners: prev.supply_chain_partners.map(
                (partner, index) =>
                    index === partnerIndex
                        ? {
                              ...partner,
                              products: [
                                  ...partner.products,
                                  { ...EMPTY_PRODUCT_STATE },
                              ],
                          }
                        : partner
            ),
        }));
    };

    const removeProduct = (partnerIndex, productIndex) => {
        setFormData((prev) => ({
            ...prev,
            supply_chain_partners: prev.supply_chain_partners.map(
                (partner, index) =>
                    index === partnerIndex
                        ? {
                              ...partner,
                              products: partner.products.filter(
                                  (_, prIndex) => prIndex !== productIndex
                              ),
                          }
                        : partner
            ),
        }));
    };

    const validateForm = () => {
        if (!formData.name.trim()) {
            setError('Application name is required');
            return false;
        }
        if (!formData.company_info.name.trim()) {
            setError('Company name is required');
            return false;
        }
        if (!formData.company_info.address.trim()) {
            setError('Company address is required');
            return false;
        }

        for (let i = 0; i < formData.supply_chain_partners.length; i++) {
            const partner = formData.supply_chain_partners[i];
            if (!partner.name.trim()) {
                setError(`Supply chain partner #${i + 1} name is required`);
                return false;
            }

            for (let j = 0; j < partner.products.length; j++) {
                const product = partner.products[j];
                if (!product.product_name.trim()) {
                    setError(
                        `Product name is required for partner #${
                            i + 1
                        }, product #${j + 1}`
                    );
                    return false;
                }
                if (!product.product_category.trim()) {
                    setError(
                        `Product category is required for partner #${
                            i + 1
                        }, product #${j + 1}`
                    );
                    return false;
                }
            }
        }

        return true;
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        setError(null);
        setSuccess(null);
        setCreationResponse(null);

        if (!validateForm()) return;

        setLoading(true);

        try {
            const submissionData = {
                ...formData,
                supply_chain_partners: formData.supply_chain_partners.map(
                    (partner) => ({
                        ...partner,
                        products: partner.products.map((product) => ({
                            ...product,
                            supply_chain_partner_name_raw:
                                partner.name ||
                                product.supply_chain_partner_name_raw,
                        })),
                    })
                ),
            };

            const response = await applications.createApplication(
                submissionData
            );
            setCreationResponse(response);
            setSuccess('Application submitted successfully!');
            setFormData(EMPTY_APPLICATION_STATE);
        } catch (err) {
            setError(
                err.response?.data?.message ||
                    'Failed to create application. Please try again.'
            );
        } finally {
            setLoading(false);
        }
    };

    return (
        <Container maxWidth="lg" sx={{ py: 4 }}>
            <Paper elevation={3} sx={{ p: 4 }}>
                <Typography variant="h4" gutterBottom align="center">
                    Create New Application
                </Typography>
                <Typography
                    variant="subtitle1"
                    color="textSecondary"
                    align="center"
                    sx={{ mb: 4 }}
                >
                    Submit a new product certification application
                </Typography>

                {error && (
                    <Alert severity="error" sx={{ mb: 3 }}>
                        {error}
                    </Alert>
                )}
                {success && creationResponse && (
                    <ApplicationSuccess responseData={creationResponse} />
                )}

                <Box
                    component="form"
                    onSubmit={handleSubmit}
                    sx={{ mt: 3, p: 5, backgroundColor: '#fcfcfcff' }}
                >
                    <ApplicationDetailsForm
                        applicationData={formData}
                        onChange={handleApplicationChange}
                    />
                    <CompanyInfoForm
                        companyInfo={formData.company_info}
                        onChange={handleCompanyInfoChange}
                    />

                    <Card sx={{ mb: 3 }}>
                        <CardHeader
                            title="Supply Chain Partners"
                            action={
                                <Button
                                    startIcon={<AddIcon />}
                                    onClick={addSupplyChainPartner}
                                    variant="outlined"
                                >
                                    Add Partner
                                </Button>
                            }
                        />
                        <Box sx={{ p: 3 }}>
                            {formData.supply_chain_partners.map(
                                (partner, partnerIndex) => (
                                    <SupplyChainPartnerForm
                                        key={partnerIndex}
                                        partner={partner}
                                        partnerIndex={partnerIndex}
                                        onChange={handlePartnerChange}
                                        onRemove={removeSupplyChainPartner}
                                        onAddProduct={addProduct}
                                        onRemoveProduct={removeProduct}
                                        canRemove={
                                            formData.supply_chain_partners
                                                .length > 1
                                        }
                                        onProductChange={handleProductChange}
                                    />
                                )
                            )}
                        </Box>
                    </Card>

                    <Box display="flex" justifyContent="center" sx={{ mt: 4 }}>
                        <Button
                            type="submit"
                            variant="contained"
                            color="primary"
                            size="large"
                            disabled={loading}
                            sx={{ minWidth: 200 }}
                        >
                            {loading ? 'Submitting...' : 'Submit Application'}
                        </Button>
                    </Box>
                </Box>
            </Paper>
        </Container>
    );
};

export default ApplicationForm;
