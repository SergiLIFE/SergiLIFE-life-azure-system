"""
🔗 PLATFORM INTEGRATION GUIDE
October 17, 2025

This file shows you EXACTLY what needs to change in the HTML platforms
to connect them to the real backend and algorithm.

Current state: Platforms show SIMULATED data
Target state: Platforms show REAL algorithm results from backend
"""

PLATFORM_INTEGRATION_JAVASCRIPT = """
// ============================================================================
// ADD THIS TO EACH PLATFORM (in <head> or before </body>)
// ============================================================================

// 1. INITIALIZE BACKEND CONNECTION
const BACKEND_URL = 'http://localhost:5000';  // Change port if needed
const BACKEND_ENABLED = true;

class LifeBackendClient {
    constructor(backendUrl = 'http://localhost:5000') {
        this.backendUrl = backendUrl;
        this.isConnected = false;
    }
    
    // Check if backend is running
    async checkHealth() {
        try {
            const response = await fetch(`${this.backendUrl}/health`);
            const data = await response.json();
            this.isConnected = true;
            console.log('✅ Backend connected:', data);
            return true;
        } catch (error) {
            console.warn('⚠️  Backend not available:', error.message);
            this.isConnected = false;
            return false;
        }
    }
    
    // Send EEG data to backend for analysis
    async analyzeEEG(eegSignal, metadata = {}) {
        try {
            if (!this.isConnected) {
                console.warn('⚠️  Backend not connected, using simulated results');
                return this.getSimulatedResults();
            }
            
            const payload = {
                eeg_signal: eegSignal,
                sample_rate: 256,
                duration_seconds: eegSignal.length / 256,
                session_id: `session_${Date.now()}`,
                user_type: metadata.user_type || 'general',
                metadata: metadata
            };
            
            console.log('📊 Sending EEG to backend...');
            const response = await fetch(`${this.backendUrl}/analyze-eeg`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload)
            });
            
            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }
            
            const result = await response.json();
            console.log('✅ Analysis complete:', result);
            
            // Extract real results from backend
            if (result.status === 'SUCCESS') {
                return {
                    source: 'REAL_ALGORITHM',
                    ...result.results
                };
            }
            
            return this.getSimulatedResults();
            
        } catch (error) {
            console.error('❌ Backend error:', error);
            console.log('   Falling back to simulated results');
            return this.getSimulatedResults();
        }
    }
    
    // Fallback: Generate realistic simulated results
    getSimulatedResults() {
        return {
            source: 'SIMULATED',
            eeg_quality: Math.floor(Math.random() * 40) + 60,
            neural_engagement: Math.floor(Math.random() * 30) + 65,
            learning_readiness: Math.floor(Math.random() * 30) + 70,
            cognitive_load: Math.floor(Math.random() * 50) + 30,
            attention_score: Math.floor(Math.random() * 30) + 65,
            adaptability_index: Math.floor(Math.random() * 30) + 60,
            timestamp: new Date().toISOString(),
            note: 'Using simulated data - backend not available'
        };
    }
}

// Initialize backend client
const lifeBackend = new LifeBackendClient(BACKEND_URL);

// Check backend on page load
window.addEventListener('DOMContentLoaded', async () => {
    console.log('🧠 L.I.F.E Platform loading...');
    await lifeBackend.checkHealth();
    updateBackendStatus(lifeBackend.isConnected);
});

// Update UI to show backend status
function updateBackendStatus(connected) {
    const statusEl = document.getElementById('backend-status');
    if (statusEl) {
        if (connected) {
            statusEl.innerHTML = '🟢 Real Algorithm (Backend Connected)';
            statusEl.style.color = '#4caf50';
        } else {
            statusEl.innerHTML = '🟡 Simulated Data (Backend Not Available)';
            statusEl.style.color = '#ff9800';
        }
    }
}


// ============================================================================
// 2. REPLACE SIMULATED DATA WITH REAL ALGORITHM CALLS
// ============================================================================

// EXAMPLE: Replace this simulated function...

// OLD (SIMULATED):
async function runAnalysisOld() {
    // Old way: Just show fake data
    const mockResults = {
        eeg_quality: 75,
        neural_engagement: 82,
        // ... etc
    };
    displayResults(mockResults);
}

// NEW (REAL):
async function runAnalysis(eegData = null) {
    console.log('🧠 Running L.I.F.E Analysis...');
    
    // Generate or use provided EEG data
    const eeg = eegData || generateSimulatedEEG(2);  // 2 second recording
    
    // Send to REAL backend
    const results = await lifeBackend.analyzeEEG(eeg, {
        user_type: getCurrentUserType(),  // 'student', 'clinical', 'enterprise', 'researcher'
        session_id: `session_${Date.now()}`
    });
    
    // Display REAL results
    displayResults(results);
}

// EXAMPLE: Helper function to get current user type
function getCurrentUserType() {
    // Get from URL, session, or user preference
    const currentPage = window.location.pathname;
    if (currentPage.includes('EDUCATION')) return 'student';
    if (currentPage.includes('CLINICAL')) return 'clinical';
    if (currentPage.includes('ENTERPRISE')) return 'enterprise';
    if (currentPage.includes('RESEARCH')) return 'researcher';
    return 'general';
}

// EXAMPLE: Replace button onclick
// OLD: <button onclick="runAnalysisOld()">Run Analysis</button>
// NEW: <button onclick="runAnalysis()">Run Analysis</button>


// ============================================================================
// 3. UPDATE RESULT DISPLAY FUNCTIONS
// ============================================================================

function displayResults(results) {
    console.log('📊 Displaying results:', results);
    
    // Show if real or simulated
    const dataSource = results.source === 'REAL_ALGORITHM' ? '✅ REAL' : '⚠️  SIMULATED';
    console.log(`Data source: ${dataSource}`);
    
    // Update each metric in the UI
    updateMetricDisplay('eeg-quality', results.eeg_quality);
    updateMetricDisplay('neural-engagement', results.neural_engagement);
    updateMetricDisplay('learning-readiness', results.learning_readiness);
    updateMetricDisplay('cognitive-load', results.cognitive_load);
    updateMetricDisplay('attention-score', results.attention_score);
    updateMetricDisplay('adaptability-index', results.adaptability_index);
    
    // Show timestamp
    if (results.timestamp) {
        document.getElementById('analysis-timestamp').innerText = 
            `Last analysis: ${new Date(results.timestamp).toLocaleString()}`;
    }
    
    // Show result source
    if (results.source) {
        document.getElementById('result-source').innerText = 
            `Data: ${results.source}`;
    }
}

function updateMetricDisplay(elementId, value) {
    const el = document.getElementById(elementId);
    if (el) {
        // Update text
        el.innerText = value.toFixed(0);
        
        // Update progress bar if exists
        const progressBar = el.parentElement?.querySelector('.progress-bar');
        if (progressBar) {
            progressBar.style.width = `${value}%`;
            
            // Color based on value
            if (value >= 80) {
                progressBar.style.background = '#4caf50';  // Green
            } else if (value >= 60) {
                progressBar.style.background = '#2196f3';  // Blue
            } else if (value >= 40) {
                progressBar.style.background = '#ff9800';  // Orange
            } else {
                progressBar.style.background = '#f44336';  // Red
            }
        }
    }
}


// ============================================================================
// 4. GENERATE REALISTIC EEG DATA FOR TESTING
// ============================================================================

function generateSimulatedEEG(durationSeconds = 2) {
    const sampleRate = 256;
    const numSamples = durationSeconds * sampleRate;
    const eegData = [];
    
    for (let i = 0; i < numSamples; i++) {
        const t = i / sampleRate;
        
        // Mix of brain wave frequencies
        const alpha = 10 * Math.sin(2 * Math.PI * 10 * t);       // 8-12 Hz
        const beta = 5 * Math.sin(2 * Math.PI * 20 * t);         // 12-30 Hz
        const theta = 15 * Math.sin(2 * Math.PI * 6 * t);        // 4-8 Hz
        const noise = (Math.random() - 0.5) * 4;                 // Noise
        
        eegData.push(alpha + beta + theta + noise);
    }
    
    return eegData;
}


// ============================================================================
// 5. FILE UPLOAD SUPPORT (For real EEG data)
// ============================================================================

async function handleEEGFileUpload(file) {
    console.log('📁 Processing EEG file:', file.name);
    
    try {
        const text = await file.text();
        
        // Parse CSV or JSON
        let eegData;
        if (file.name.endsWith('.csv')) {
            eegData = parseCSV(text);
        } else if (file.name.endsWith('.json')) {
            eegData = JSON.parse(text);
        } else {
            throw new Error('Unsupported file format');
        }
        
        // Analyze the uploaded data with REAL algorithm
        const results = await lifeBackend.analyzeEEG(eegData, {
            user_type: getCurrentUserType(),
            file_name: file.name
        });
        
        displayResults(results);
        
    } catch (error) {
        console.error('❌ Error processing file:', error);
        alert('Error processing EEG file: ' + error.message);
    }
}

function parseCSV(text) {
    const lines = text.trim().split('\\n');
    const data = [];
    
    for (let i = 1; i < lines.length; i++) {
        const values = lines[i].split(',');
        if (values[0]) {
            data.push(parseFloat(values[0]));
        }
    }
    
    return data;
}


// ============================================================================
// 6. STATUS/DEBUG DISPLAY (Add to platform)
// ============================================================================

/*
Add this HTML to your platform to show backend status:

<div id="backend-status" style="
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 10px 15px;
    border-radius: 5px;
    background: white;
    border: 2px solid #ddd;
    font-weight: bold;
    font-size: 12px;
">
    🔌 Checking backend...
</div>

<div id="result-source" style="
    font-size: 12px;
    color: #666;
    margin-top: 10px;
">
    Data: Waiting for analysis...
</div>
*/

"""

# ============================================================================
# STEP-BY-STEP MODIFICATION GUIDE
# ============================================================================

MODIFICATION_STEPS = """
🔧 STEP-BY-STEP: How to Modify Each Platform

STEP 1: Add JavaScript Backend Client
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Location: Before </head> or before </body>
Action: Copy the LifeBackendClient class from above
Result: Platform can now communicate with backend

STEP 2: Initialize Backend Connection
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Location: In <head>
Action: Add initialization code that runs on page load
Result: Backend status checked when platform opens

STEP 3: Replace Analysis Functions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Location: Find all buttons with onclick="runAnalysis()" or similar
Action: Change to send data to backend using lifeBackend.analyzeEEG()
Result: Clicking "Run Analysis" sends real data to backend

STEP 4: Update Result Display
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Location: Find function that displays results
Action: Use displayResults() to show real backend results
Result: Metrics show real algorithm output

STEP 5: Add Visual Feedback
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Location: Top right corner
Action: Add backend status indicator
Result: Users see if backend is connected (green) or simulated (yellow)

TESTING SEQUENCE:
1. Start backend: python life_backend_server.py (port 5000)
2. Start HTTP server: python -m http.server 8080
3. Open platform: http://localhost:8080/LIFE_AI_PLATFORM_REAL.html
4. Check console (F12) - should see "✅ Backend connected"
5. Click "Run Analysis"
6. Results should come from REAL algorithm via backend

SUCCESS INDICATORS:
✅ Console shows "✅ Backend connected"
✅ Status indicator shows green (🟢 Real Algorithm)
✅ Results change each time (real algorithm is processing)
✅ Clicking "Run Analysis" calls backend endpoint
✅ Can see actual metrics from experimentP2L.py
"""

# ============================================================================
# FILES THAT NEED MODIFICATION
# ============================================================================

FILES_TO_MODIFY = [
    "LIFE_AI_PLATFORM_REAL.html",
    "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html",
    "LIFE_ENTERPRISE_PLATFORM_REAL.html",
    "LIFE_EDUCATION_PLATFORM_REAL.html",
    "LIFE_RESEARCH_PLATFORM_REAL.html",
]

if __name__ == "__main__":
    print("🔗 PLATFORM INTEGRATION GUIDE")
    print("=" * 80)
    print("\nFiles to modify:")
    for f in FILES_TO_MODIFY:
        print(f"  - {f}")

    print("\n" + "=" * 80)
    print("NEXT STEPS:")
    print("=" * 80)
    print(
        """
1. Copy the LifeBackendClient class into each platform
   (Place before </body> tag)

2. Replace "runAnalysis()" functions to use lifeBackend.analyzeEEG()

3. Update result display functions to show backend results

4. Test:
   - Start backend: python life_backend_server.py
   - Start HTTP server: python -m http.server 8080
   - Open platform and verify real results

See PLATFORM_INTEGRATION_JAVASCRIPT above for complete code.
    """
    )
