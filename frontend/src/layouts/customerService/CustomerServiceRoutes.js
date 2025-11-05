import CustomerServiceLayout from './CustomerServiceLayout';
import RoleGuard from '../components/RoleGuard';
import CustomerProfileForm from './CustomerProfileForm';

/**
 * Customer route configuration defining protected customer-service-specific paths
 * Routes are wrapped with role-based authentication guard
 */
const customerServiceRoutes = {
    path: 'customer-service',
    element: (
        <RoleGuard requiredRole="cservice">
            <CustomerServiceLayout />
        </RoleGuard>
    ),
    children: [
        {
            path: '',
            element: <CustomerProfileForm />,
        },
    ],
};

export default customerServiceRoutes;
