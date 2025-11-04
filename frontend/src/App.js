import './global.css';
import { ApiProvider } from './context/ApiContext';

import DebugApp from './layouts/debug';

function App() {
    return (
        <ApiProvider>
            <div className="App">
                <h1>Product Certification</h1>
                <DebugApp />
            </div>
        </ApiProvider>
    );
}

export default App;
