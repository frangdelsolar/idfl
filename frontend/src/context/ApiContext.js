import React, {
    createContext,
    useContext,
    useState,
    useEffect,
    useMemo,
} from 'react';
import createApiClient from '../services/apiClient';
import createAuthService from '../services/authService';
import createApplicationService from '../services/applicationService';

const BASE_URL = 'http://localhost:8000';
const API_BASE_URL = `${BASE_URL}/api`;

/**
 * Context for API client and authentication state management
 */
const ApiContext = createContext(null);

/**
 * Hook to access API services and authentication state
 * @returns {Object} API services and authentication methods
 */
export const useApi = () => {
    const context = useContext(ApiContext);
    if (!context) {
        throw new Error('useApi must be used within an ApiProvider');
    }
    return context;
};

/**
 * Provider component that manages authentication state and API services
 * @param {Object} props - Component props
 * @param {ReactNode} props.children - Child components
 */
export const ApiProvider = ({ children }) => {
    const [token, setToken] = useState(localStorage.getItem('authToken'));

    /**
     * Memoized API services with authentication state management
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

        const enhancedAuth = {
            login: async (username, password) => {
                const data = await baseAuthService.login(username, password);
                const newToken = data.token;
                if (newToken) {
                    setToken(newToken);
                    localStorage.setItem('authToken', newToken);
                }
                return data;
            },
            logout: () => {
                setToken(null);
                localStorage.removeItem('authToken');
            },
            register: baseAuthService.register,
            isAuthenticated: !!token,
        };

        return {
            auth: enhancedAuth,
            applications,
        };
    }, [token]);

    return (
        <ApiContext.Provider value={services}>{children}</ApiContext.Provider>
    );
};
