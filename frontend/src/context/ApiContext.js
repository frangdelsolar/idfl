import React, { createContext, useContext, useState, useMemo } from 'react';
import createApiClient from '../services/apiClient';
import createAuthService from '../services/authService';
import createApplicationService from '../services/applicationService';
import createCompanyService from '../services/companyService';
import createCustomerProfileService from '../services/customerProfileService';

const BASE_URL = 'http://localhost:8000';
const API_BASE_URL = `${BASE_URL}/api`;

/**
 * Detects user role based on username patterns for demo purposes
 * In production, roles should come from the backend authentication response
 */
const detectRoleFromUsername = (username) => {
    if (!username) return null;

    const usernameLower = username.toLowerCase();

    if (
        usernameLower.includes('cservice') ||
        usernameLower.includes('customer_service') ||
        usernameLower.includes('support') ||
        usernameLower.includes('agent')
    ) {
        return 'cservice';
    }

    if (
        usernameLower.includes('customer') ||
        usernameLower.includes('client') ||
        usernameLower.includes('user') ||
        usernameLower.startsWith('cust_')
    ) {
        return 'customer';
    }

    if (
        usernameLower.includes('reviewer') ||
        usernameLower.includes('admin') ||
        usernameLower.includes('manager') ||
        usernameLower.includes('approver')
    ) {
        return 'reviewer';
    }

    return 'customer';
};

const ApiContext = createContext(null);

/**
 * Hook to access API services and authentication state
 * @throws {Error} If used outside of ApiProvider
 */
export const useApi = () => {
    const context = useContext(ApiContext);
    if (!context) {
        throw new Error('useApi must be used within an ApiProvider');
    }
    return context;
};

/**
 * Main API context provider that manages:
 * - Authentication state and token management
 * - API service instances
 * - User role detection and session persistence
 */
export const ApiProvider = ({ children }) => {
    const [token, setToken] = useState(localStorage.getItem('authToken'));
    const [user, setUser] = useState(null);

    /**
     * Memoized service instances that depend on authentication state
     * Recreates services only when token or user changes
     */
    const services = useMemo(() => {
        const apiClient = createApiClient({
            token,
            apiBaseUrl: API_BASE_URL,
        });

        const baseAuthService = createAuthService(
            BASE_URL,
            apiClient.executeApiCall
        );
        const applications = createApplicationService(apiClient.executeApiCall);
        const companies = createCompanyService(apiClient.executeApiCall);
        const customerProfiles = createCustomerProfileService(
            apiClient.executeApiCall
        );

        /**
         * Enhanced authentication service with role detection and state management
         */
        const enhancedAuth = {
            login: async (username, password) => {
                const data = await baseAuthService.login(username, password);
                const newToken = data.token;
                if (newToken) {
                    setToken(newToken);
                    localStorage.setItem('authToken', newToken);

                    const detectedRole = detectRoleFromUsername(username);
                    console.log(
                        `User ${username} logged in, detected role: ${detectedRole}`
                    );

                    setUser({
                        username: username,
                        role: detectedRole,
                    });
                }
                return data;
            },
            logout: () => {
                setToken(null);
                setUser(null);
                localStorage.removeItem('authToken');
                console.log('User logged out');
            },
            register: baseAuthService.register,
            isAuthenticated: !!token,
            user: user,
            isInitialized: true,
        };

        return {
            auth: enhancedAuth,
            applications,
            companies,
            customerProfiles,
        };
    }, [token, user]);

    return (
        <ApiContext.Provider value={services}>{children}</ApiContext.Provider>
    );
};
