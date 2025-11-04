import { useRoutes, Navigate } from 'react-router-dom'; // Add Navigate
import MainLayout from './layouts/MainLayout';
import authRoutes from './layouts/auth/AuthRoutes';

// Define the base routes array
export const ROUTES = [authRoutes];

// Create a new array including the catch-all fallback route
const ROUTES_WITH_FALLBACK = [
    {
        path: '/',
        element: <MainLayout />,
        children: [
            ...ROUTES,
            {
                // The '*' path will match any URL not matched by the preceding routes
                path: '*',
                element: <Navigate to="/" replace />,
            },
        ],
    },
];

function AppRoutes() {
    // Use the augmented array
    const elements = useRoutes(ROUTES_WITH_FALLBACK);
    return <>{elements}</>;
}

export default AppRoutes;
