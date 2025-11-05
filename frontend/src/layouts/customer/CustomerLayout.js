import { Outlet } from 'react-router-dom';

/**
 * Layout container for customer routes
 * Provides structural wrapper for customer service specific pages and components
 */
function CustomerLayout() {
    return <Outlet />;
}

export default CustomerLayout;
