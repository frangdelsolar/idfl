import AuthLayout from './AuthLayout';
import LoginPage from './LoginPage';

const authRoutes = {
    path: 'auth',
    element: <AuthLayout />,
    children: [
        {
            path: 'login',
            element: <LoginPage />,
        },
    ],
};

export default authRoutes;
