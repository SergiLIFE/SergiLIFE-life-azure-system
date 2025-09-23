import React from 'react';
import ReactDOM from 'react-dom/client';
import LifeEnterpriseDashboard from './LifeDashboardApp';
import { initializeIcons } from '@fluentui/react';

// Initialize Fluent UI icons
initializeIcons();

// Sample user data for demo
const mockUser = {
  name: "Enterprise User",
  tier: "Professional",
  initials: "EU",
  sessionLength: "2h 34m",
  subscriptionId: "9a600d96-fe1e-420b-902a-a0c42c561adb"
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <LifeEnterpriseDashboard user={mockUser} />
  </React.StrictMode>
);