import React, { useState, useEffect } from 'react';
import { useApi } from '../context/ApiContext';

const LoginForm = () => {
    const { auth } = useApi();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleLogin = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            await auth.login(username, password);
            setError('Login successful!');
        } catch (err) {
            setError(err.detail || 'Login failed');
        } finally {
            setLoading(false);
        }
    };

    const handleLogout = () => {
        auth.logout();
        setError('Logged out');
    };

    return (
        <div>
            <h2>Login</h2>
            {auth.isAuthenticated ? (
                <div>
                    <p>Logged in</p>
                    <button onClick={handleLogout}>Logout</button>
                </div>
            ) : (
                <form onSubmit={handleLogin}>
                    <div>
                        <input
                            type="text"
                            placeholder="Username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                        />
                    </div>
                    <div>
                        <input
                            type="password"
                            placeholder="Password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                    </div>
                    <button type="submit" disabled={loading}>
                        {loading ? 'Logging in...' : 'Login'}
                    </button>
                </form>
            )}
            {error && <p>{error}</p>}
        </div>
    );
};

const ApplicationsList = () => {
    const { applications, auth } = useApi();
    const [apps, setApps] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const fetchApplications = async () => {
        if (!auth.isAuthenticated) return;

        setLoading(true);
        setError('');
        try {
            const data = await applications.listApplications();
            setApps(data);
        } catch (err) {
            setError(err.detail || 'Failed to fetch applications');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchApplications();
    }, [auth.isAuthenticated]);

    if (!auth.isAuthenticated) {
        return <p>Please login to view applications</p>;
    }

    return (
        <div>
            <h2>Applications</h2>
            <button onClick={fetchApplications} disabled={loading}>
                Refresh
            </button>
            {loading && <p>Loading...</p>}
            {error && <p>Error: {error}</p>}
            <ul>
                {apps.map((app) => (
                    <li key={app.id}>
                        {app.name} - {app.status}
                    </li>
                ))}
            </ul>
        </div>
    );
};

const DebugApp = () => {
    return (
        <div>
            <LoginForm />
            <ApplicationsList />
        </div>
    );
};

export default DebugApp;
