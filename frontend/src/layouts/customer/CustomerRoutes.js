import CustomerLayout from './CustomerLayout';
import RoleGuard from '../components/RoleGuard';
import ApplicationForm from './ApplicationForm';

/**
 * Customer route configuration defining protected customer-specific paths
 * Routes are wrapped with role-based authentication guard
 */
const customerRoutes = {
    path: 'customer',
    element: (
        <RoleGuard requiredRole="customer">
            <CustomerLayout />
        </RoleGuard>
    ),
    children: [
        {
            path: '',
            element: <ApplicationForm />,
        },
    ],
};

export default customerRoutes;
