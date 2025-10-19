/**
 * ============================================================================
 * L.I.F.E PLATFORM BACKEND INTEGRATION
 * October 17, 2025
 * ============================================================================
 * 
 * THIS FILE IS THE ACTUAL INTEGRATION THAT CONNECTS PLATFORMS TO:
 * 1. Backend server (life_backend_server.py on localhost:5000)
 * 2. Real algorithm (experimentP2L.py)
 * 3. Autonomous self-optimization
 * 
 * ADD THIS FILE TO EVERY PLATFORM AND RUN THE BACKEND SERVER
 * ============================================================================
 */

// ============================================================================
// 1. BACKEND CLIENT CLASS
// ============================================================================

class LifeBackendClient {
    constructor(backendUrl = 'http://localhost:5000') {
        this.backendUrl = backendUrl;
        this.isConnected = false;
        this.sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        this.processingHistory = [];
        this.optimizationMetrics = {
            totalAnalyses: 0,
            successfulAnalyses: 0,
            averageLatency: 0,
            latencies: []
        };

        console.log(`🧠 L.I.F.E Backend Client initialized`);
        console.log(`   Session ID: ${this.sessionId}`);
        console.log(`   Backend URL: ${this.backendUrl}`);

        this.init();
    }

    async init() {
        // Check backend on init
        await this.checkHealth();
    }

    /**
     * Check if backend is running and responding
     */
    async checkHealth() {
        try {
            const response = await fetch(`${this.backendUrl}/health`, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            });

            if (response.ok) {
                const data = await response.json();
                this.isConnected = true;
                console.log('✅ Backend connected:', {
                    status: data.status,
                    algorithmAvailable: data.algorithm_available,
                    version: data.version
                });
                return true;
            }
        } catch (error) {
            this.isConnected = false;
            console.warn('⚠️  Backend connection failed:', error.message);
            return false;
        }
    }

    /**
     * MAIN FUNCTION: Send EEG data to backend for analysis
     * This is where the real algorithm processing happens
     */
    async analyzeEEG(eegSignal, metadata = {}) {
        const startTime = performance.now();
        this.optimizationMetrics.totalAnalyses++;

        try {
            if (!this.isConnected) {
                console.warn('⚠️  Backend not connected. Checking health...');
                await this.checkHealth();

                if (!this.isConnected) {
                    console.log('📡 Using fallback simulated results');
                    return this.getSimulatedResults(eegSignal, metadata);
                }
            }

            // Ensure EEG is array
            const eegArray = Array.isArray(eegSignal) ? eegSignal : [eegSignal];

            const payload = {
                session_id: this.sessionId,
                eeg_signal: eegArray,
                sample_rate: 256,
                duration_seconds: eegArray.length / 256,
                user_type: metadata.user_type || 'general',
                scenario: metadata.scenario || 'standard',
                metadata: metadata
            };

            console.log(`📊 Sending EEG to backend (${eegArray.length} samples)...`);

            const response = await fetch(`${this.backendUrl}/analyze-eeg`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                throw new Error(`Backend returned ${response.status}: ${response.statusText}`);
            }

            const result = await response.json();

            // Track latency for optimization
            const latency = performance.now() - startTime;
            this.optimizationMetrics.latencies.push(latency);
            this.optimizationMetrics.averageLatency =
                this.optimizationMetrics.latencies.reduce((a, b) => a + b, 0) /
                this.optimizationMetrics.latencies.length;
            this.optimizationMetrics.successfulAnalyses++;

            console.log(`✅ Analysis complete in ${latency.toFixed(2)}ms`);
            console.log(`   Results:`, result.results);

            // Store in history for learning
            this.processingHistory.push({
                timestamp: new Date().toISOString(),
                input: { length: eegArray.length, metadata },
                output: result.results,
                latency: latency,
                source: 'REAL_ALGORITHM'
            });

            if (result.status === 'SUCCESS') {
                return {
                    source: 'REAL_ALGORITHM',
                    ...result.results,
                    backend_response: result
                };
            }

            return this.getSimulatedResults(eegSignal, metadata);

        } catch (error) {
            console.error(`❌ Backend error: ${error.message}`);
            console.log('   Falling back to simulated results');
            return this.getSimulatedResults(eegSignal, metadata);
        }
    }

    /**
     * Fallback: Generate realistic simulated results if backend unavailable
     */
    getSimulatedResults(eegSignal, metadata = {}) {
        const eegArray = Array.isArray(eegSignal) ? eegSignal : [eegSignal];

        // Generate semi-realistic values based on signal characteristics
        const mean = eegArray.reduce((a, b) => a + b, 0) / eegArray.length;
        const variance = eegArray.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / eegArray.length;
        const stdDev = Math.sqrt(variance);

        return {
            source: 'SIMULATED',
            eeg_quality: Math.min(100, Math.max(0, 50 + stdDev * 5)),
            neural_engagement: Math.min(100, Math.max(0, 60 + stdDev * 3)),
            learning_readiness: Math.min(100, Math.max(0, 70 + Math.random() * 20)),
            cognitive_load: Math.min(100, Math.max(0, 40 + Math.random() * 40)),
            attention_score: Math.min(100, Math.max(0, 65 + Math.random() * 25)),
            adaptability_index: Math.min(100, Math.max(0, 60 + Math.random() * 30)),
            timestamp: new Date().toISOString(),
            note: 'Simulated results - backend not available'
        };
    }

    /**
     * Get backend status and statistics
     */
    async getStatus() {
        try {
            const response = await fetch(`${this.backendUrl}/status`);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Failed to get status:', error);
            return null;
        }
    }

    /**
     * Get optimization metrics and learning statistics
     */
    getOptimizationMetrics() {
        return {
            ...this.optimizationMetrics,
            sessionId: this.sessionId,
            historyLength: this.processingHistory.length,
            isConnected: this.isConnected
        };
    }

    /**
     * Get processing history for autonomous learning
     */
    getProcessingHistory() {
        return this.processingHistory;
    }
}

// ============================================================================
// 2. AUTONOMOUS SELF-OPTIMIZATION ENGINE
// ============================================================================

class AutonomousOptimizationEngine {
    constructor(backendClient) {
        this.client = backendClient;
        this.learningRate = 0.1;
        this.adaptiveThresholds = {
            eegQuality: 70,
            neuralEngagement: 75,
            learningReadiness: 80,
            cognitiveLoad: 50
        };
        this.optimizationLog = [];

        console.log('🤖 Autonomous Optimization Engine initialized');
    }

    /**
     * Analyze results and automatically optimize based on patterns
     */
    async optimizeBasedOnResults(results, currentSettings = {}) {
        const optimization = {
            timestamp: new Date().toISOString(),
            beforeSettings: { ...currentSettings },
            suggestions: [],
            adjustments: {}
        };

        // If EEG quality is low, suggest improvements
        if (results.eeg_quality < this.adaptiveThresholds.eegQuality) {
            optimization.suggestions.push({
                category: 'eeg_quality',
                message: `EEG quality low (${results.eeg_quality}%). Suggest device repositioning or electrode check.`,
                severity: 'HIGH',
                autoAdjust: { checkDevice: true }
            });
        }

        // If neural engagement is low, suggest more stimulating content
        if (results.neural_engagement < this.adaptiveThresholds.neuralEngagement) {
            optimization.suggestions.push({
                category: 'neural_engagement',
                message: 'Neural engagement low. Increasing challenge level automatically.',
                severity: 'MEDIUM',
                autoAdjust: { challengeLevel: 'increase' }
            });
            optimization.adjustments.challengeLevel = 'HIGH';
        }

        // If cognitive load is too high, suggest breaks
        if (results.cognitive_load > this.adaptiveThresholds.cognitiveLoad) {
            optimization.suggestions.push({
                category: 'cognitive_load',
                message: 'Cognitive load high. Recommend a 5-minute break.',
                severity: 'MEDIUM',
                autoAdjust: { breakRecommended: true }
            });
            optimization.adjustments.breakRecommended = true;
        }

        // If learning readiness is high, suggest intensive session
        if (results.learning_readiness > this.adaptiveThresholds.learningReadiness) {
            optimization.suggestions.push({
                category: 'learning_readiness',
                message: 'Learning readiness optimal. Suggest intensive training session.',
                severity: 'INFO',
                autoAdjust: { sessionIntensity: 'high' }
            });
            optimization.adjustments.sessionIntensity = 'HIGH';
        }

        // Automatically adjust adaptive thresholds based on history
        if (this.client.processingHistory.length > 5) {
            this.adaptiveThresholds = this.calculateAdaptiveThresholds();
        }

        this.optimizationLog.push(optimization);

        console.log('🧠 Optimization suggestions:', optimization.suggestions);
        return optimization;
    }

    /**
     * Calculate adaptive thresholds based on user's historical patterns
     */
    calculateAdaptiveThresholds() {
        const history = this.client.processingHistory;
        if (history.length === 0) return this.adaptiveThresholds;

        const recentOutputs = history.slice(-10).map(h => h.output);

        // Calculate average for each metric
        const avgQuality = recentOutputs.reduce((sum, o) => sum + o.eeg_quality, 0) / recentOutputs.length;
        const avgEngagement = recentOutputs.reduce((sum, o) => sum + o.neural_engagement, 0) / recentOutputs.length;
        const avgReadiness = recentOutputs.reduce((sum, o) => sum + o.learning_readiness, 0) / recentOutputs.length;
        const avgLoad = recentOutputs.reduce((sum, o) => sum + o.cognitive_load, 0) / recentOutputs.length;

        // Adapt thresholds: set to slightly below current average
        return {
            eegQuality: Math.max(50, avgQuality - 5),
            neuralEngagement: Math.max(60, avgEngagement - 5),
            learningReadiness: Math.max(70, avgReadiness - 5),
            cognitiveLoad: Math.min(70, avgLoad + 5)
        };
    }

    /**
     * Get optimization statistics for display
     */
    getOptimizationStats() {
        return {
            suggestionsGiven: this.optimizationLog.length,
            adaptiveThresholds: this.adaptiveThresholds,
            recentSuggestions: this.optimizationLog.slice(-5),
            learningRate: this.learningRate
        };
    }
}

// ============================================================================
// 3. PLATFORM INTEGRATION HELPERS
// ============================================================================

/**
 * Initialize the entire integration for a platform
 */
async function initializeLIFEBackendIntegration(containerId = null) {
    console.log('🚀 Initializing L.I.F.E Backend Integration...');

    // Create global backend client
    window.lifeBackendClient = new LifeBackendClient('http://localhost:5000');

    // Create global optimization engine
    window.optimizationEngine = new AutonomousOptimizationEngine(window.lifeBackendClient);

    // Wait for connection
    await new Promise(resolve => setTimeout(resolve, 500));

    // Update UI if container provided
    if (containerId) {
        updateBackendStatus(containerId, window.lifeBackendClient.isConnected);
    }

    console.log('✅ L.I.F.E Integration ready');
    return {
        client: window.lifeBackendClient,
        optimizer: window.optimizationEngine,
        isConnected: window.lifeBackendClient.isConnected
    };
}

/**
 * Update UI to show backend status
 */
function updateBackendStatus(containerId, connected) {
    const el = document.getElementById(containerId);
    if (el) {
        if (connected) {
            el.innerHTML = '🟢 Real Algorithm (Backend Connected)';
            el.style.color = '#4caf50';
            el.style.background = 'rgba(76, 175, 80, 0.2)';
        } else {
            el.innerHTML = '🟡 Simulated Data (Backend Not Available)';
            el.style.color = '#ff9800';
            el.style.background = 'rgba(255, 152, 0, 0.2)';
        }
    }
}

/**
 * Generate realistic test EEG data
 */
function generateTestEEGData(durationSeconds = 2, sampleRate = 256) {
    const samples = durationSeconds * sampleRate;
    const eeg = [];

    for (let i = 0; i < samples; i++) {
        // Mix multiple frequency bands for realistic EEG
        const alpha = Math.sin(2 * Math.PI * 10 * i / sampleRate) * 20;  // 10 Hz
        const beta = Math.sin(2 * Math.PI * 20 * i / sampleRate) * 15;   // 20 Hz
        const theta = Math.sin(2 * Math.PI * 6 * i / sampleRate) * 25;   // 6 Hz
        const noise = (Math.random() - 0.5) * 10;

        eeg.push(alpha + beta + theta + noise);
    }

    return eeg;
}

/**
 * Run a complete analysis cycle with optimization
 */
async function runCompleteAnalysisCycle(userType = 'general', scenario = 'standard') {
    console.log('🧠 Running complete L.I.F.E analysis cycle...');

    if (!window.lifeBackendClient || !window.optimizationEngine) {
        console.error('❌ Backend integration not initialized. Call initializeLIFEBackendIntegration() first.');
        return null;
    }

    try {
        // Generate or get EEG data
        const eegData = generateTestEEGData(2, 256);

        // Analyze with backend
        const results = await window.lifeBackendClient.analyzeEEG(eegData, {
            user_type: userType,
            scenario: scenario
        });

        console.log('📊 Analysis results:', results);

        // Get optimization suggestions
        const optimization = await window.optimizationEngine.optimizeBasedOnResults(results);

        console.log('🤖 Optimization suggestions:', optimization);

        // Return complete analysis
        return {
            results: results,
            optimization: optimization,
            metrics: window.lifeBackendClient.getOptimizationMetrics(),
            timestamp: new Date().toISOString()
        };

    } catch (error) {
        console.error('❌ Analysis cycle failed:', error);
        return null;
    }
}

// ============================================================================
// 4. DISPLAY HELPERS
// ============================================================================

/**
 * Format analysis results for display
 */
function formatAnalysisResults(results) {
    if (!results) return 'No results';

    return `
🧠 L.I.F.E Analysis Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Source: ${results.source}
Timestamp: ${new Date(results.timestamp).toLocaleTimeString()}

📊 Neural Metrics:
  • EEG Quality: ${results.eeg_quality?.toFixed(1)}%
  • Neural Engagement: ${results.neural_engagement?.toFixed(1)}%
  • Learning Readiness: ${results.learning_readiness?.toFixed(1)}%
  • Cognitive Load: ${results.cognitive_load?.toFixed(1)}%
  • Attention Score: ${results.attention_score?.toFixed(1)}%
  • Adaptability: ${results.adaptability_index?.toFixed(1)}%

${results.note ? `ℹ️ Note: ${results.note}` : ''}
━━━━━━━━━━━━━━━━━━━━━━━━━━━
  `;
}

/**
 * Format optimization suggestions for display
 */
function formatOptimizationSuggestions(optimization) {
    if (!optimization || !optimization.suggestions) return 'No suggestions';

    let text = `🤖 Autonomous Optimization Suggestions\n━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;

    if (optimization.suggestions.length === 0) {
        text += '✅ All metrics optimal - no adjustments needed\n';
    } else {
        optimization.suggestions.forEach(s => {
            text += `${s.severity === 'HIGH' ? '🔴' : s.severity === 'MEDIUM' ? '🟡' : '🔵'} ${s.message}\n`;
        });
    }

    if (Object.keys(optimization.adjustments).length > 0) {
        text += `\nAutomatic Adjustments:\n`;
        Object.entries(optimization.adjustments).forEach(([key, value]) => {
            text += `  • ${key}: ${value}\n`;
        });
    }

    text += `━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
    return text;
}

// ============================================================================
// 5. AUTO-INIT ON SCRIPT LOAD
// ============================================================================

console.log('✅ L.I.F.E Platform Backend Integration module loaded');
console.log('📝 Usage: await initializeLIFEBackendIntegration("status-container-id")');
console.log('📝 Then: await runCompleteAnalysisCycle("user_type", "scenario")');
