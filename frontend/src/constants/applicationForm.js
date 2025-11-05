/**
 * Default empty state for new product certification applications
 * Provides complete nested structure matching backend API requirements
 */
export const EMPTY_APPLICATION_STATE = {
    name: '',
    description: '',
    company_info: {
        name: '',
        address: '',
        city: '',
        state: '',
        zip_code: '',
        country: '',
    },
    supply_chain_partners: [
        {
            name: '',
            address: '',
            city: '',
            state: '',
            zip_code: '',
            country: '',
            products: [
                {
                    supply_chain_partner_name_raw: '',
                    product_name: '',
                    product_category: '',
                    raw_materials_list: '',
                },
            ],
        },
    ],
};

/**
 * Template for adding new supply chain partners to an application
 * Includes partner location details and empty product array
 */
export const EMPTY_PARTNER_STATE = {
    name: '',
    address: '',
    city: '',
    state: '',
    zip_code: '',
    country: '',
    products: [
        {
            supply_chain_partner_name_raw: '',
            product_name: '',
            product_category: '',
            raw_materials_list: '',
        },
    ],
};

/**
 * Template for adding new products to supply chain partners
 * Contains product details and raw materials information
 */
export const EMPTY_PRODUCT_STATE = {
    supply_chain_partner_name_raw: '',
    product_name: '',
    product_category: '',
    raw_materials_list: '',
};
