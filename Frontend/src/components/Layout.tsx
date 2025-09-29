import { ReactNode } from 'react';

const Layout = ({ children }: { children: ReactNode }) => (
  <div style={{ padding: '20px', backgroundColor: '#1E90FF', color: 'white' }}>
    <h1>User Interface Wireframe</h1>
    <div style={{ display: 'flex', gap: '20px' }}>
      <nav style={{ width: '200px' }}>
        <button>Home</button>
        <button>Upload Data</button>
        <button>Calculate</button>
        <button>Compare</button>
        <button>User Reports</button>
      </nav>
      <main style={{ flexGrow: 1 }}>{children}</main>
    </div>
  </div>
);

export default Layout;