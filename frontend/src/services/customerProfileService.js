const CUSTOMER_PROFILES_ENDPOINT = 'customer-profiles/';

/**
 * Factory function to create a customer profile service with CRUD operations
 * @param {Function} executeApiCall - Configured API client function
 * @returns {Object} Customer profile service methods
 */
const createCustomerProfileService = (executeApiCall) => {
    /**
     * Creates a new customer profile with user account
     * @param {Object} body - Customer profile data including company_id, user details, and phone number
     * @returns {Promise<Object>} Created customer profile object with user details
     */
    const createCustomerProfile = (body) => {
        return executeApiCall({
            method: 'POST',
            relativePath: `${CUSTOMER_PROFILES_ENDPOINT}create/`,
            body,
        });
    };

    /**
     * Retrieves a list of customer profiles with optional filtering
     * @param {Object} params - Query parameters for filtering and pagination
     * @returns {Promise<Array>} List of customer profile objects
     */
    const listCustomerProfiles = (params = {}) => {
        return executeApiCall({
            method: 'GET',
            relativePath: CUSTOMER_PROFILES_ENDPOINT,
            params,
        });
    };

    /**
     * Retrieves a single customer profile by ID
     * @param {string|number} id - Customer profile identifier
     * @returns {Promise<Object>} Customer profile object with full details
     */
    const getCustomerProfile = (id) => {
        return executeApiCall({
            method: 'GET',
            relativePath: `${CUSTOMER_PROFILES_ENDPOINT}${id}/`,
        });
    };

    /**
     * Updates an existing customer profile
     * @param {string|number} id - Customer profile identifier
     * @param {Object} body - Updated customer profile data
     * @returns {Promise<Object>} Updated customer profile object
     */
    const updateCustomerProfile = (id, body) => {
        return executeApiCall({
            method: 'PUT',
            relativePath: `${CUSTOMER_PROFILES_ENDPOINT}${id}/`,
            body,
        });
    };

    /**
     * Partially updates an existing customer profile
     * @param {string|number} id - Customer profile identifier
     * @param {Object} body - Partial customer profile data to update
     * @returns {Promise<Object>} Updated customer profile object
     */
    const partialUpdateCustomerProfile = (id, body) => {
        return executeApiCall({
            method: 'PATCH',
            relativePath: `${CUSTOMER_PROFILES_ENDPOINT}${id}/`,
            body,
        });
    };

    /**
     * Deletes a customer profile and associated user account
     * @param {string|number} id - Customer profile identifier
     * @returns {Promise<void>} Empty response on success
     */
    const deleteCustomerProfile = (id) => {
        return executeApiCall({
            method: 'DELETE',
            relativePath: `${CUSTOMER_PROFILES_ENDPOINT}${id}/`,
        });
    };

    /**
     * Retrieves customer profiles by company ID
     * @param {string|number} companyId - Company identifier
     * @param {Object} params - Additional query parameters
     * @returns {Promise<Array>} List of customer profiles for the specified company
     */
    const getCustomerProfilesByCompany = (companyId, params = {}) => {
        return executeApiCall({
            method: 'GET',
            relativePath: CUSTOMER_PROFILES_ENDPOINT,
            params: {
                company: companyId,
                ...params,
            },
        });
    };

    return {
        createCustomerProfile,
        listCustomerProfiles,
        getCustomerProfile,
        updateCustomerProfile,
        partialUpdateCustomerProfile,
        deleteCustomerProfile,
        getCustomerProfilesByCompany,
    };
};

export default createCustomerProfileService;
