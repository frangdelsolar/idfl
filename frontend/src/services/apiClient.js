import axios from 'axios';

/**
 * Factory function to create a configured API client instance
 * @param {Object} config - Configuration object
 * @param {string} config.token - Authentication token for API requests
 * @param {string} config.apiBaseUrl - Base URL for all API endpoints
 * @param {string} config.origin - Origin header value for CORS requests
 * @returns {Object} API client with executeApiCall method
 */
const createApiClient = ({ token, apiBaseUrl, origin }) => {
    const client = axios.create({
        baseURL: apiBaseUrl,
        headers: {
            'Content-Type': 'application/json',
            ...(origin && { Origin: origin }),
            ...(token && { Authorization: `Token ${token}` }),
        },
    });

    /**
     * Executes an API call with the configured client
     * @param {Object} options - Request options
     * @param {string} options.method - HTTP method (GET, POST, PUT, DELETE, etc.)
     * @param {string} options.relativePath - API endpoint path relative to baseURL
     * @param {Object} options.body - Request body for POST/PUT requests
     * @param {Object} options.params - URL parameters for GET requests
     * @param {string} options.fullUrl - Complete URL (overrides baseURL + relativePath)
     * @returns {Promise<Object>} API response data
     * @throws {Object} Error object with response data or error message
     */
    const executeApiCall = async ({
        method,
        relativePath,
        body = {},
        params,
        fullUrl,
    }) => {
        try {
            const config = {
                method,
                url: fullUrl || relativePath,
                data: body,
                params: params,
            };

            const response = await client(config);
            return response.data;
        } catch (error) {
            throw error.response?.data || { detail: error.message };
        }
    };

    return { executeApiCall };
};

export default createApiClient;
