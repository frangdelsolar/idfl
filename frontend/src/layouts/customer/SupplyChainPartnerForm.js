import React from 'react';
import {
    Card,
    CardHeader,
    CardContent,
    TextField,
    IconButton,
    Box,
    Typography,
    Button,
    Divider,
    Stack,
} from '@mui/material';
import { Delete as DeleteIcon, Add as AddIcon } from '@mui/icons-material';
import ProductForm from './ProductForm';

/**
 * Form component for capturing supply chain partner information and their products
 * Includes partner details, address information, and nested product forms
 */
const SupplyChainPartnerForm = ({
    partner,
    partnerIndex,
    onChange,
    onRemove,
    onProductChange,
    onAddProduct,
    onRemoveProduct,
    canRemove,
}) => {
    const handleChange = (field) => (event) => {
        onChange(partnerIndex, field, event.target.value);
    };

    return (
        <Card variant="outlined" sx={{ mb: 3, backgroundColor: '#fafafa' }}>
            <CardHeader
                title={`Supply Chain Partner #${partnerIndex + 1}`}
                action={
                    canRemove && (
                        <IconButton
                            onClick={() => onRemove(partnerIndex)}
                            color="error"
                        >
                            <DeleteIcon />
                        </IconButton>
                    )
                }
            />
            <CardContent>
                <Stack spacing={3}>
                    <TextField
                        label="Partner Name *"
                        value={partner.name}
                        onChange={handleChange('name')}
                        fullWidth
                        required
                    />
                    <TextField
                        label="Address"
                        value={partner.address}
                        onChange={handleChange('address')}
                        fullWidth
                    />
                    <Stack direction={{ xs: 'column', sm: 'row' }} spacing={3}>
                        <TextField
                            label="City"
                            value={partner.city}
                            onChange={handleChange('city')}
                            fullWidth
                        />
                        <TextField
                            label="State"
                            value={partner.state}
                            onChange={handleChange('state')}
                            fullWidth
                        />
                    </Stack>
                    <Stack direction={{ xs: 'column', sm: 'row' }} spacing={3}>
                        <TextField
                            label="ZIP Code"
                            value={partner.zip_code}
                            onChange={handleChange('zip_code')}
                            fullWidth
                        />
                        <TextField
                            label="Country"
                            value={partner.country}
                            onChange={handleChange('country')}
                            fullWidth
                        />
                    </Stack>
                </Stack>

                <Divider sx={{ my: 3 }} />

                <Box sx={{ mt: 2 }}>
                    <Box
                        display="flex"
                        justifyContent="space-between"
                        alignItems="center"
                        sx={{ mb: 2 }}
                    >
                        <Typography variant="h6">Products</Typography>
                        <Button
                            startIcon={<AddIcon />}
                            onClick={() => onAddProduct(partnerIndex)}
                            variant="outlined"
                            size="small"
                        >
                            Add Product
                        </Button>
                    </Box>

                    {partner.products.map((product, productIndex) => (
                        <ProductForm
                            key={productIndex}
                            product={product}
                            productIndex={productIndex}
                            partnerIndex={partnerIndex}
                            onChange={onProductChange}
                            onRemove={onRemoveProduct}
                            canRemove={partner.products.length > 1}
                        />
                    ))}
                </Box>
            </CardContent>
        </Card>
    );
};

export default SupplyChainPartnerForm;
