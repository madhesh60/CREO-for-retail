import { useState } from "react";
import { AuthProvider, useAuth } from "./AuthContext";
import Chat from "./Chat";
import Models from "./Models";
import GitHub from "./GitHub";
import Discord from "./Discord";
import Docs from "./Docs";
import Cloud from "./Cloud";
import Login from "./Login";
import Register from "./Register";
import styles from "./styles.js";

function AppContent() {
  const [currentRoute, setCurrentRoute] = useState('/');
  const { user, logout } = useAuth();

  const renderPage = () => {
    switch (currentRoute) {
      case '/':
        return <Chat />;
      case '/models':
        return <Chat />;
      case '/github':
        return <GitHub />;
      case '/discord':
        return <Discord />;
      case '/docs':
        return <Docs />;
      case '/cloud':
        return <Cloud />;
      case '/login':
        return <Login navigate={setCurrentRoute} />;
      case '/register':
        return <Register navigate={setCurrentRoute} />;
      default:
        return <Chat />;
    }
  };

  return (
    <div style={styles.app}>
      <header style={styles.header}>
        <div style={styles.nav}>
          <span
            onClick={() => setCurrentRoute('/')}
            style={{ ...styles.navIcon, cursor: 'pointer' }}
          >
            🦙
          </span>
          {/* Cleared "Models" link as requested for cleaner UI */}
          <span onClick={() => setCurrentRoute('/github')} style={styles.navLink}>GitHub</span>
          <span onClick={() => setCurrentRoute('/discord')} style={styles.navLink}>AI Gen</span>
          <span onClick={() => setCurrentRoute('/docs')} style={styles.navLink}>Docs</span>
          <span onClick={() => setCurrentRoute('/cloud')} style={styles.navLink}>Cloud Gallery</span>
        </div>
        <div style={{ marginLeft: 'auto', display: 'flex', gap: '16px' }}>
          {user ? (
            <>
              <span style={{ ...styles.navLink, fontWeight: 'bold' }}>{user.email}</span>
              <span onClick={logout} style={styles.navLink}>Logout</span>
            </>
          ) : (
            <span onClick={() => setCurrentRoute('/login')} style={styles.navLink}>Sign In</span>
          )}
        </div>
      </header>
      <main>
        {renderPage()}
      </main>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}