// src/LifeDashboardApp.js
import * as React from "react";
import { useState, useEffect } from "react";
import { initializeIcons } from "@fluentui/react";
import { Stack, CommandBar, Panel, Card, ProgressIndicator, Text, PrimaryButton } from "@fluentui/react";
import { FontWeights, mergeStyleSets } from "@fluentui/react";
import { NeuralBrainVisualization } from "./components/NeuralBrainVisualization";
import { EEGWaveform } from "./components/EEGWaveform";
import { VenturiGatesDisplay } from "./components/VenturiGatesDisplay";

initializeIcons();

const styles = mergeStyleSets({
  backgroundGradient: {
    minHeight: "100vh",
    background: "linear-gradient(135deg, #0078D4 0%, #005A9E 25%, #004578 50%, #003366 75%, #001122 100%)",
    backgroundAttachment: "fixed",
    color: "#ffffff",
    fontFamily: "'Segoe UI', -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Roboto', sans-serif",
    position: "relative",
    overflow: "hidden",
  },
  headerBar: {
    background: "rgba(255, 255, 255, 0.98)",
    backdropFilter: "blur(10px)",
    padding: "1rem 2rem",
    boxShadow: "0 2px 8px rgba(0,0,0,0.1), 0 0 20px rgba(0, 120, 212, 0.05)",
    position: "fixed",
    top: 0,
    left: 0,
    right: 0,
    zIndex: 1000,
    borderBottom: "1px solid rgba(0,0,0,0.05)",
  },
  logo: {
    fontSize: "2.2rem",
    fontWeight: 700,
    background: "linear-gradient(45deg, #00FFFF, #0078D4, #FF00FF, #00FF00)",
    backgroundSize: "400% 400%",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
    backgroundClip: "text",
    letterSpacing: "0.1em",
    animation: "logoGlow 3s ease-in-out infinite alternate",
  },
  leftNavBar: {
    width: 64,
    background: "linear-gradient(to bottom, rgba(0, 120, 212, 0.1), rgba(0, 255, 255, 0.05))",
    height: "calc(100vh - 80px)",
    marginTop: 80,
    boxShadow: "2px 0 16px rgba(0, 120, 212, 0.2)",
    borderRight: "1px solid rgba(0, 255, 255, 0.3)",
    position: "fixed",
    left: 0,
    zIndex: 900,
  },
  navIcon: {
    padding: "16px 0",
    color: "#00FFFF",
    fontSize: 24,
    cursor: "pointer",
    textAlign: "center",
    borderBottom: "2px solid transparent",
    transition: "all 0.3s ease",
    selectors: { 
      ":hover": { 
        borderBottom: "2px solid #00FFFF",
        backgroundColor: "rgba(0, 255, 255, 0.1)",
        transform: "scale(1.1)"
      } 
    },
  },
  mainContent: {
    marginLeft: 64,
    marginTop: 80,
    padding: "2rem",
    minHeight: "calc(100vh - 80px)",
  },
  dashboardGrid: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr 1fr",
    gridTemplateRows: "auto auto auto",
    gap: "1.5rem",
    marginBottom: "2rem",
  },
  neuralCard: {
    background: "rgba(0, 0, 0, 0.4)",
    backdropFilter: "blur(10px)",
    border: "1px solid rgba(0, 255, 255, 0.3)",
    borderRadius: "12px",
    padding: "1.5rem",
    boxShadow: "0 8px 32px rgba(0, 255, 255, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.1)",
    position: "relative",
    overflow: "hidden",
    gridColumn: "span 2",
  },
  metricsCard: {
    background: "rgba(0, 0, 0, 0.4)",
    backdropFilter: "blur(10px)",
    border: "1px solid rgba(0, 255, 255, 0.3)",
    borderRadius: "12px",
    padding: "1.5rem",
    boxShadow: "0 8px 32px rgba(0, 255, 255, 0.1)",
    position: "relative",
    overflow: "hidden",
  },
  cardTitle: {
    fontSize: "1.5rem",
    fontWeight: FontWeights.semibold,
    color: "#00FFFF",
    marginBottom: "1rem",
    textShadow: "0 0 10px rgba(0, 255, 255, 0.5)",
  },
  kpiValue: {
    fontSize: "2.5rem",
    fontWeight: FontWeights.bold,
    color: "#FFFFFF",
    textShadow: "0 0 20px rgba(0, 255, 255, 0.8)",
  },
  kpiLabel: {
    fontSize: "0.9rem",
    color: "rgba(255, 255, 255, 0.7)",
    textTransform: "uppercase",
    letterSpacing: "0.1em",
  },
  statusIndicator: {
    width: 12,
    height: 12,
    borderRadius: "50%",
    backgroundColor: "#00FF00",
    boxShadow: "0 0 10px #00FF00",
    animation: "pulse 2s infinite",
  },
  controlsSection: {
    marginTop: "2rem",
    padding: "1.5rem",
    background: "rgba(0, 0, 0, 0.3)",
    borderRadius: "12px",
    border: "1px solid rgba(0, 255, 255, 0.2)",
  },
  slider: {
    margin: "1rem 0",
  },
  venturiStatus: {
    display: "flex",
    alignItems: "center",
    gap: "1rem",
    marginBottom: "1rem",
  },
  realTimeUpdates: {
    position: "fixed",
    bottom: 0,
    left: 0,
    right: 0,
    background: "rgba(0, 0, 0, 0.9)",
    color: "#00FFFF",
    padding: "0.5rem 2rem",
    fontFamily: "'Roboto Mono', monospace",
    fontSize: "0.9rem",
    borderTop: "1px solid rgba(0, 255, 255, 0.3)",
    zIndex: 1000,
  },
});

// Mock real-time data hook
function useLifeMetrics() {
  const [metrics, setMetrics] = useState({
    accuracy: 78.5,
    responseTime: 0.42,
    patternsLearned: 1247,
    confidence: 94,
    neuralState: "ADAPTIVE_LEARNING",
    venturiGates: {
      gate1: { status: "active", efficiency: 98.2 },
      gate2: { status: "active", efficiency: 97.8 },
      gate3: { status: "active", efficiency: 99.1 },
    },
    systemHealth: {
      azureFunctions: "operational",
      eegPipeline: "active",
      storageSync: "synchronized",
      security: "compliant",
    },
    learningProgress: 73,
    sessionActive: true,
    lastUpdate: new Date().toLocaleTimeString(),
  });

  useEffect(() => {
    const interval = setInterval(() => {
      setMetrics(prev => ({
        ...prev,
        accuracy: (78 + Math.random() * 4).toFixed(1),
        responseTime: (0.38 + Math.random() * 0.07).toFixed(2),
        patternsLearned: Math.floor(1240 + Math.random() * 20),
        confidence: Math.floor(90 + Math.random() * 8),
        learningProgress: Math.min(100, prev.learningProgress + Math.random() * 0.5),
        lastUpdate: new Date().toLocaleTimeString(),
      }));
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  return metrics;
}

// Main L.I.F.E. Platform Dashboard Component
export function LifeEnterpriseDashboard({ user = { name: "Demo User", tier: "Professional", initials: "DU" } }) {
  const metrics = useLifeMetrics();
  const [selectedView, setSelectedView] = useState("dashboard");
  const [learningRate, setLearningRate] = useState(0.005);
  const [venturiSensitivity, setVenturiSensitivity] = useState(1.2);
  const [neuralThreshold, setNeuralThreshold] = useState(0.7);

  const navigationItems = [
    { key: "dashboard", icon: "Home", label: "Dashboard" },
    { key: "analytics", icon: "BarChartVertical", label: "Analytics" },
    { key: "neural", icon: "Brain", label: "Neural Processing" },
    { key: "settings", icon: "Settings", label: "Settings" },
    { key: "support", icon: "ContactInfo", label: "Support" },
  ];

  return (
    <div className={styles.backgroundGradient}>
      {/* Header Bar */}
      <div className={styles.headerBar}>
        <Stack horizontal horizontalAlign="space-between" verticalAlign="center">
          <div className={styles.logo}>L.I.F.E. Theory SaaS</div>
          <Stack horizontal tokens={{ childrenGap: 20 }}>
            <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
              <div style={{ 
                width: 16, 
                height: 16, 
                backgroundColor: "#0078D4", 
                borderRadius: "2px" 
              }} />
              <Text style={{ color: "#333", fontSize: "0.9rem" }}>Azure Marketplace</Text>
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
              <div className={styles.statusIndicator} />
              <Text style={{ color: "#333", fontSize: "0.9rem" }}>Azure Authenticated</Text>
            </div>
            <div style={{ 
              padding: "8px 16px", 
              backgroundColor: "#0078D4", 
              color: "white", 
              borderRadius: "20px", 
              fontSize: "0.9rem" 
            }}>
              {user.tier} Plan
            </div>
          </Stack>
        </Stack>
      </div>

      {/* Left Navigation */}
      <nav className={styles.leftNavBar}>
        {navigationItems.map((item) => (
          <div
            key={item.key}
            className={styles.navIcon}
            onClick={() => setSelectedView(item.key)}
            title={item.label}
          >
            <i className={`ms-Icon ms-Icon--${item.icon}`} />
          </div>
        ))}
      </nav>

      {/* Main Dashboard Content */}
      <div className={styles.mainContent}>
        {/* Real-time EEG Processing Section */}
        <div className={styles.dashboardGrid}>
          {/* Neural Visualization Card */}
          <Card className={styles.neuralCard}>
            <div className={styles.cardTitle}>
              <Stack horizontal verticalAlign="center" tokens={{ childrenGap: 10 }}>
                Real-time EEG Processing
                <div className={styles.statusIndicator} />
              </Stack>
            </div>
            <NeuralBrainVisualization data={metrics.neuralState} />
            <div style={{ marginTop: "1rem" }}>
              <Text style={{ color: "rgba(255, 255, 255, 0.8)" }}>
                Neural Activity: Processing EEG signals...
              </Text>
            </div>
          </Card>

          {/* Learning Metrics Card */}
          <Card className={styles.metricsCard}>
            <div className={styles.cardTitle}>Learning Metrics</div>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1rem" }}>
              <div>
                <div className={styles.kpiValue}>{metrics.accuracy}%</div>
                <div className={styles.kpiLabel}>Accuracy</div>
              </div>
              <div>
                <div className={styles.kpiValue}>{metrics.responseTime}ms</div>
                <div className={styles.kpiLabel}>Response Time</div>
              </div>
              <div>
                <div className={styles.kpiValue}>{metrics.patternsLearned.toLocaleString()}</div>
                <div className={styles.kpiLabel}>Patterns Learned</div>
              </div>
              <div>
                <div className={styles.kpiValue}>{metrics.confidence}%</div>
                <div className={styles.kpiLabel}>Confidence</div>
              </div>
            </div>
          </Card>

          {/* Adaptive Learning Progress */}
          <Card className={styles.metricsCard}>
            <div className={styles.cardTitle}>Adaptive Learning Progress</div>
            <div style={{ textAlign: "center", padding: "2rem 0" }}>
              <ProgressIndicator 
                percentComplete={metrics.learningProgress / 100} 
                description="Optimizing Neural Pathways"
                styles={{
                  progressBar: { backgroundColor: "#00FFFF" },
                  progressTrack: { backgroundColor: "rgba(255, 255, 255, 0.2)" }
                }}
              />
              <Text style={{ color: "rgba(255, 255, 255, 0.8)", marginTop: "1rem" }}>
                Venturi System Active
              </Text>
            </div>
          </Card>

          {/* System Health Card */}
          <Card className={styles.metricsCard}>
            <div className={styles.cardTitle}>System Health</div>
            <Stack tokens={{ childrenGap: 12 }}>
              {Object.entries(metrics.systemHealth).map(([key, status]) => (
                <Stack key={key} horizontal horizontalAlign="space-between" verticalAlign="center">
                  <Text style={{ color: "white", textTransform: "capitalize" }}>
                    {key.replace(/([A-Z])/g, ' $1').trim()}
                  </Text>
                  <div style={{ 
                    padding: "4px 12px", 
                    backgroundColor: status === "operational" || status === "active" || status === "synchronized" || status === "compliant" ? "#00FF00" : "#FF4444",
                    color: "black",
                    borderRadius: "12px",
                    fontSize: "0.8rem",
                    fontWeight: "bold",
                    textTransform: "capitalize"
                  }}>
                    {status}
                  </div>
                </Stack>
              ))}
            </Stack>
          </Card>

          {/* Venturi Gates Status */}
          <Card className={styles.metricsCard}>
            <div className={styles.cardTitle}>Venturi Gates System</div>
            <VenturiGatesDisplay gates={metrics.venturiGates} />
          </Card>

          {/* EEG Live Waveform */}
          <Card className={styles.metricsCard}>
            <div className={styles.cardTitle}>EEG Live Signal</div>
            <EEGWaveform />
            <Stack horizontal tokens={{ childrenGap: 20 }} style={{ marginTop: "1rem" }}>
              <div>
                <Text style={{ color: "#00FFFF", fontSize: "1.2rem", fontWeight: "bold" }}>
                  Focus: 87%
                </Text>
              </div>
              <div>
                <Text style={{ color: "#FF00FF", fontSize: "1.2rem", fontWeight: "bold" }}>
                  Adaptability: 92%
                </Text>
              </div>
            </Stack>
          </Card>
        </div>

        {/* Adaptive Learning Controls */}
        <div className={styles.controlsSection}>
          <div className={styles.cardTitle}>Adaptive Learning Controls</div>
          <Stack tokens={{ childrenGap: 20 }}>
            <div>
              <Text style={{ color: "white", marginBottom: "8px" }}>
                Learning Rate Adjustment: {learningRate}
              </Text>
              <input
                type="range"
                min="0.001"
                max="0.1"
                step="0.001"
                value={learningRate}
                onChange={(e) => setLearningRate(parseFloat(e.target.value))}
                style={{ width: "100%", height: "8px" }}
              />
            </div>
            <div>
              <Text style={{ color: "white", marginBottom: "8px" }}>
                Venturi Gate Sensitivity: {venturiSensitivity}
              </Text>
              <input
                type="range"
                min="0.1"
                max="2.0"
                step="0.1"
                value={venturiSensitivity}
                onChange={(e) => setVenturiSensitivity(parseFloat(e.target.value))}
                style={{ width: "100%", height: "8px" }}
              />
            </div>
            <div>
              <Text style={{ color: "white", marginBottom: "8px" }}>
                Neural State Threshold: {neuralThreshold}
              </Text>
              <input
                type="range"
                min="0.1"
                max="1.0"
                step="0.05"
                value={neuralThreshold}
                onChange={(e) => setNeuralThreshold(parseFloat(e.target.value))}
                style={{ width: "100%", height: "8px" }}
              />
            </div>
            <Stack horizontal tokens={{ childrenGap: 16 }}>
              <PrimaryButton 
                text="Apply Changes" 
                styles={{ root: { backgroundColor: "#00FFFF", color: "black" } }} 
              />
              <PrimaryButton 
                text="Reset to Optimal" 
                styles={{ root: { backgroundColor: "transparent", border: "1px solid #00FFFF", color: "#00FFFF" } }} 
              />
              <PrimaryButton 
                text="Save Configuration" 
                styles={{ root: { backgroundColor: "transparent", border: "1px solid #00FFFF", color: "#00FFFF" } }} 
              />
            </Stack>
          </Stack>
        </div>
      </div>

      {/* Real-time Activity Feed */}
      <div className={styles.realTimeUpdates}>
        <Stack horizontal horizontalAlign="space-between" verticalAlign="center">
          <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
            <div className={styles.statusIndicator} />
            <Text>Session Active - Real-time Processing</Text>
          </div>
          <Text>Last updated: {metrics.lastUpdate}</Text>
          <Text>🔗 Azure Marketplace Partner - Enterprise-grade neuroadaptive learning powered by Microsoft Azure</Text>
        </Stack>
      </div>
    </div>
  );
}

// Supporting Components

// Neural Brain Visualization Component
function NeuralBrainVisualization({ data }) {
  return (
    <div style={{ 
      height: "200px", 
      display: "flex", 
      alignItems: "center", 
      justifyContent: "center",
      background: "radial-gradient(circle, rgba(0, 255, 255, 0.1), transparent)",
      borderRadius: "8px",
      position: "relative"
    }}>
      <div style={{
        width: "120px",
        height: "120px",
        border: "2px solid #00FFFF",
        borderRadius: "50%",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        animation: "neuralPulse 2s infinite",
        position: "relative"
      }}>
        <div style={{
          width: "80px",
          height: "80px",
          border: "1px solid #FF00FF",
          borderRadius: "50%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          animation: "neuralPulse 1.5s infinite reverse"
        }}>
          🧠
        </div>
        {/* Neural activity indicators */}
        {[...Array(8)].map((_, i) => (
          <div
            key={i}
            style={{
              position: "absolute",
              width: "4px",
              height: "4px",
              backgroundColor: "#00FFFF",
              borderRadius: "50%",
              top: "50%",
              left: "50%",
              transform: `rotate(${i * 45}deg) translateY(-60px)`,
              animation: `neuralSpark ${1 + i * 0.1}s infinite`
            }}
          />
        ))}
      </div>
    </div>
  );
}

// EEG Waveform Component
function EEGWaveform() {
  return (
    <div style={{ 
      height: "100px", 
      background: "rgba(0, 0, 0, 0.3)",
      borderRadius: "8px",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      position: "relative",
      overflow: "hidden"
    }}>
      <svg width="100%" height="100%" viewBox="0 0 400 100">
        <path
          d="M0,50 Q50,20 100,50 T200,50 T300,50 T400,50"
          stroke="#00FFFF"
          strokeWidth="2"
          fill="none"
          style={{ animation: "eegWave 2s infinite" }}
        />
        <path
          d="M0,50 Q50,80 100,50 T200,50 T300,50 T400,50"
          stroke="#FF00FF"
          strokeWidth="1"
          fill="none"
          style={{ animation: "eegWave 1.5s infinite reverse" }}
        />
      </svg>
      <div style={{
        position: "absolute",
        top: "8px",
        left: "8px",
        color: "#00FFFF",
        fontSize: "0.8rem",
        fontFamily: "monospace"
      }}>
        256 Hz • Live Signal
      </div>
    </div>
  );
}

// Venturi Gates Display Component
function VenturiGatesDisplay({ gates }) {
  return (
    <Stack tokens={{ childrenGap: 12 }}>
      {Object.entries(gates).map(([gateKey, gate]) => (
        <Stack key={gateKey} horizontal horizontalAlign="space-between" verticalAlign="center">
          <Stack horizontal tokens={{ childrenGap: 8 }} verticalAlign="center">
            <div className={styles.statusIndicator} />
            <Text style={{ color: "white", textTransform: "capitalize" }}>
              {gateKey.replace(/([A-Z])/g, ' $1').trim()}
            </Text>
          </Stack>
          <Text style={{ color: "#00FFFF", fontWeight: "bold" }}>
            {gate.efficiency}%
          </Text>
        </Stack>
      ))}
    </Stack>
  );
}

// CSS Animations (add to your CSS file)
const additionalStyles = `
@keyframes logoGlow {
  0% {
    text-shadow: 0 0 20px rgba(0, 255, 255, 0.8);
  }
  100% {
    text-shadow: 0 0 40px rgba(0, 255, 255, 1), 0 0 60px rgba(255, 0, 255, 0.8);
  }
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.7; transform: scale(1.2); }
}

@keyframes neuralPulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

@keyframes neuralSpark {
  0%, 100% { opacity: 0; }
  50% { opacity: 1; }
}

@keyframes eegWave {
  0% { transform: translateX(-400px); }
  100% { transform: translateX(0); }
}
`;

export default LifeEnterpriseDashboard;