import './index.css';
import { ApiProvider } from './context/ApiContext';
import { BrowserRouter } from 'react-router-dom';
import AppRoutes from './AppRoutes';

function App() {
    return (
        <ApiProvider>
            <BrowserRouter>
                <AppRoutes />
            </BrowserRouter>
        </ApiProvider>
    );
}

export default App;
