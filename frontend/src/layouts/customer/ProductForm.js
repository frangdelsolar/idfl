import React from 'react';
import {
    Card,
    Box,
    Typography,
    TextField,
    IconButton,
    Stack,
} from '@mui/material';
import { Delete as DeleteIcon } from '@mui/icons-material';

/**
 * Individual product form component for capturing product details within supply chain partners
 * Handles product name, category, and raw materials information
 */
const ProductForm = ({
    product,
    productIndex,
    partnerIndex,
    onChange,
    onRemove,
    canRemove,
}) => {
    const handleChange = (field) => (event) => {
        onChange(partnerIndex, productIndex, field, event.target.value);
    };

    return (
        <Card
            variant="outlined"
            sx={{ mb: 2, p: 2, backgroundColor: '#dbdbdbff' }}
        >
            <Box
                display="flex"
                justifyContent="space-between"
                alignItems="flex-start"
                sx={{ mb: 2 }}
            >
                <Typography variant="subtitle1">
                    Product #{productIndex + 1}
                </Typography>
                {canRemove && (
                    <IconButton
                        onClick={() => onRemove(partnerIndex, productIndex)}
                        color="error"
                        size="small"
                    >
                        <DeleteIcon />
                    </IconButton>
                )}
            </Box>

            <Stack spacing={2}>
                <TextField
                    label="Product Name *"
                    value={product.product_name}
                    onChange={handleChange('product_name')}
                    fullWidth
                    required
                />
                <TextField
                    label="Product Category *"
                    value={product.product_category}
                    onChange={handleChange('product_category')}
                    fullWidth
                    required
                    placeholder="e.g., Apparel, Electronics, Food & Beverage"
                />
                <TextField
                    label="Raw Materials List"
                    value={product.raw_materials_list}
                    onChange={handleChange('raw_materials_list')}
                    fullWidth
                    multiline
                    rows={2}
                    placeholder="List the raw materials used in this product..."
                />
            </Stack>
        </Card>
    );
};

export default ProductForm;
