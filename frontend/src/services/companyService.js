const COMPANIES_ENDPOINT = 'companies/';

/**
 * Factory function to create a company service
 * @param {Function} executeApiCall - Configured API client function
 * @returns {Object} Company service methods
 */
const createCompanyService = (executeApiCall) => {
    /**
     * Retrieves a list of companies (just id and name)
     * @param {Object} params - Query parameters for filtering
     * @returns {Promise<Array>} List of company objects with id and name
     */
    const listCompanies = (params = {}) => {
        return executeApiCall({
            method: 'GET',
            relativePath: COMPANIES_ENDPOINT,
            params: {
                ...params,
                // You can add specific fields if your API supports field selection
                // fields: 'id,name'
            },
        });
    };

    /**
     * Retrieves a single company by ID
     * @param {string|number} id - Company identifier
     * @returns {Promise<Object>} Company object
     */
    const getCompany = (id) => {
        return executeApiCall({
            method: 'GET',
            relativePath: `${COMPANIES_ENDPOINT}${id}/`,
        });
    };

    return {
        listCompanies,
        getCompany,
    };
};

export default createCompanyService;
