import { createContext, useState, useEffect, useContext } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [token, setToken] = useState(localStorage.getItem('token'));
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (token) {
            fetchUser(token);
        } else {
            setLoading(false);
        }
    }, [token]);

    const fetchUser = async (authToken) => {
        try {
            const res = await fetch("http://127.0.0.1:8000/users/me", {
                headers: { Authorization: `Bearer ${authToken}` }
            });
            if (res.ok) {
                const data = await res.json();
                setUser(data);
            } else {
                logout();
            }
        } catch (e) {
            console.error(e);
            logout();
        } finally {
            setLoading(false);
        }
    };

    const login = async (email, password) => {
        const res = await fetch("http://127.0.0.1:8000/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || "Login failed");
        }

        const data = await res.json();
        localStorage.setItem('token', data.access_token);
        setToken(data.access_token);
        return true;
    };

    const register = async (email, password) => {
        const res = await fetch("http://127.0.0.1:8000/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || "Registration failed");
        }
        return true;
    };

    const logout = () => {
        localStorage.removeItem('token');
        setToken(null);
        setUser(null);
    };

    const addColor = async (color) => {
        if (!token) return;
        const formData = new FormData();
        formData.append('color', color);
        const res = await fetch("http://127.0.0.1:8000/colors", {
            method: "POST",
            headers: { Authorization: `Bearer ${token}` },
            body: formData
        });
        if (res.ok) {
            const data = await res.json();
            setUser({ ...user, colors: data.colors }); // update local state
        }
    };

    return (
        <AuthContext.Provider value={{ user, token, login, register, logout, loading, addColor }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
