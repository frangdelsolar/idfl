import { useRoutes, Navigate } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import UnauthorizedPage from './layouts/UnauthorizedPage';
import authRoutes from './layouts/auth/AuthRoutes';
import customerServiceRoutes from './layouts/customerService/CustomerServiceRoutes';
import customerRoutes from './layouts/customer/CustomerRoutes';

/**
 * Combined application routes organized by user role and functionality
 */
export const ROUTES = [authRoutes, customerServiceRoutes, customerRoutes];

/**
 * Complete route configuration including fallback and error handling
 */
const ROUTES_WITH_FALLBACK = [
    {
        path: '/',
        element: <MainLayout />,
        children: [
            ...ROUTES,
            {
                path: '/unauthorized',
                element: <UnauthorizedPage />,
            },
            {
                path: '*',
                element: <Navigate to="/" replace />,
            },
        ],
    },
];

/**
 * Main application router component
 * Handles route resolution and navigation
 */
function AppRoutes() {
    const elements = useRoutes(ROUTES_WITH_FALLBACK);
    return <>{elements}</>;
}

export default AppRoutes;
