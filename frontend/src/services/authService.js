const AUTH_TOKEN_ENDPOINT = 'api-token-auth/';
const CUSTOMER_REGISTER_ENDPOINT = 'users/register/';

/**
 * Factory function to create authentication service with login and registration
 * @param {string} baseURL - Base URL for authentication endpoints
 * @param {Function} executeApiCall - Configured API client function
 * @returns {Object} Authentication service methods
 */
const createAuthService = (baseURL, executeApiCall) => {
    /**
     * Authenticates user and retrieves authentication token
     * @param {string} username - User's username
     * @param {string} password - User's password
     * @returns {Promise<Object>} Authentication token object
     */
    const login = (username, password) => {
        const data = {
            method: 'POST',
            fullUrl: `${baseURL}/${AUTH_TOKEN_ENDPOINT}`,
            body: { username, password },
        };
        return executeApiCall(data);
    };

    /**
     * Registers a new customer user
     * @param {Object} body - User registration data
     * @returns {Promise<Object>} Created user object
     */
    const register = (body) => {
        return executeApiCall({
            method: 'POST',
            relativePath: CUSTOMER_REGISTER_ENDPOINT,
            body,
        });
    };

    return { login, register };
};

export default createAuthService;
