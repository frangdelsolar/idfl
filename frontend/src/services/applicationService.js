const APPLICATIONS_ENDPOINT = 'applications/';

/**
 * Factory function to create an application service with CRUD operations
 * @param {Function} executeApiCall - Configured API client function
 * @returns {Object} Application service methods
 */
const createApplicationService = (executeApiCall) => {
    /**
     * Retrieves a list of applications with optional filtering
     * @param {Object} params - Query parameters for filtering and pagination
     * @returns {Promise<Array>} List of application objects
     */
    const listApplications = (params = {}) => {
        return executeApiCall({
            method: 'GET',
            relativePath: APPLICATIONS_ENDPOINT,
            params,
        });
    };

    /**
     * Retrieves a single application by ID
     * @param {string|number} id - Application identifier
     * @returns {Promise<Object>} Application object with full details
     */
    const getApplication = (id) => {
        return executeApiCall({
            method: 'GET',
            relativePath: `${APPLICATIONS_ENDPOINT}${id}/`,
        });
    };

    /**
     * Creates a new application
     * @param {Object} body - Application data including company info and supply chain partners
     * @returns {Promise<Object>} Created application object
     */
    const createApplication = (body) => {
        return executeApiCall({
            method: 'POST',
            relativePath: APPLICATIONS_ENDPOINT,
            body,
        });
    };

    /**
     * Updates an existing application
     * @param {string|number} id - Application identifier
     * @param {Object} body - Updated application data
     * @returns {Promise<Object>} Updated application object
     */
    const updateApplication = (id, body) => {
        return executeApiCall({
            method: 'PUT',
            relativePath: `${APPLICATIONS_ENDPOINT}${id}/`,
            body,
        });
    };

    /**
     * Deletes an application
     * @param {string|number} id - Application identifier
     * @returns {Promise<void>} Empty response on success
     */
    const deleteApplication = (id) => {
        return executeApiCall({
            method: 'DELETE',
            relativePath: `${APPLICATIONS_ENDPOINT}${id}/`,
        });
    };

    return {
        listApplications,
        getApplication,
        createApplication,
        updateApplication,
        deleteApplication,
    };
};

export default createApplicationService;
