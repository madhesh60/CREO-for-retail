import { useState } from 'react';
import { useAuth } from './AuthContext';
import styles from './styles';

export default function Register({ navigate }) {
    const { register, login } = useAuth();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        try {
            await register(email, password);
            // Auto login after register
            await login(email, password);
            navigate('/');
        } catch (err) {
            setError(err.message);
        }
    };

    return (
        <div style={styles.page}>
            <div style={{ ...styles.panel, maxWidth: '480px' }}>
                <h2 style={styles.cardTitle}>Create Account</h2>
                {error && <p style={{ color: '#e53e3e', marginBottom: '16px' }}>{error}</p>}
                <form onSubmit={handleSubmit}>
                    <label style={styles.label}>Email</label>
                    <input
                        style={styles.input}
                        type="email"
                        placeholder="name@example.com"
                        value={email}
                        onChange={e => setEmail(e.target.value)}
                        required
                    />
                    <label style={styles.label}>Password</label>
                    <input
                        style={styles.input}
                        type="password"
                        placeholder="Create a password"
                        value={password}
                        onChange={e => setPassword(e.target.value)}
                        required
                    />
                    <button style={styles.button}>Sign Up</button>
                </form>
                <p
                    style={{ marginTop: '24px', cursor: 'pointer', color: '#667eea', textAlign: 'center' }}
                    onClick={() => navigate('/login')}
                >
                    Already have an account? Sign In
                </p>
            </div>
        </div>
    );
}
