// L.I.F.E. Algorithm Client - Browser-based Implementation
// Learning Individually from Experience - Real-time Processing

class LIFEAlgorithmClient {
    constructor() {
        this.version = "2.0.1";
        this.isInitialized = false;

        // Core EEG Metrics (matches your Python dataclass structure)
        this.eegMetrics = {
            attentionIndex: 0,
            learningEfficiency: 0,
            cognitiveLoad: 0,
            neuralAdaptation: 0,
            focusStability: 0,
            memoryConsolidation: 0
        };

        // User Traits (matches your Python dataclass structure)
        this.userTraits = {
            curiosity: 0.5,
            persistence: 0.5,
            openness: 0.5,
            processingSpeed: 0.5,
            learningEfficiency: 0.5
        };

        // Learning Outcomes
        this.learningOutcome = {
            comprehensionScore: 0,
            retentionProbability: 0,
            optimalReviewTime: 0,
            learningVelocity: 0,
            cognitiveResonance: 0
        };

        // Processing State
        this.isProcessing = false;
        this.sessionData = [];
        this.typingHistory = [];
        this.lastInputTime = Date.now();

        // Venturi Gates Integration
        this.venturiGates = null;

        // Initialize
        this.init();
    }

    async init() {
        console.log(`🧠 L.I.F.E. Algorithm v${this.version} initializing...`);

        try {
            // Initialize Venturi Gates System
            this.venturiGates = new VenturiGatesSystem();

            // Load user profile from storage
            await this.loadUserProfile();

            // Set up real-time processing
            this.setupRealTimeProcessing();

            this.isInitialized = true;
            console.log('✅ L.I.F.E. Algorithm initialized successfully');

        } catch (error) {
            console.error('❌ L.I.F.E. Algorithm initialization failed:', error);
        }
    }

    // Core Learning Session Processing (async like your Python version)
    async processLearningSession(userInput, learningContent) {
        if (!this.isInitialized) {
            throw new Error('L.I.F.E. Algorithm not initialized');
        }

        this.isProcessing = true;
        console.log('🧠 Processing learning session...');

        try {
            // Step 1: Generate EEG simulation based on input
            const simulatedEEGData = await this.generateEEGSimulation(userInput);

            // Step 2: Process through Venturi Gates
            const processedSignal = await this.venturiGates.processSignal(simulatedEEGData);

            // Step 3: Calculate EEG metrics
            this.eegMetrics = await this.calculateEEGMetrics(processedSignal, userInput);

            // Step 4: Adapt user traits based on behavior
            await this.adaptUserTraits(userInput, learningContent);

            // Step 5: Calculate learning outcomes
            this.learningOutcome = await this.calculateLearningOutcome(
                this.eegMetrics,
                learningContent,
                this.userTraits
            );

            // Step 6: Store session data
            this.storeSessionData({
                timestamp: Date.now(),
                input: userInput,
                eegMetrics: { ...this.eegMetrics },
                userTraits: { ...this.userTraits },
                learningOutcome: { ...this.learningOutcome }
            });

            console.log('✅ Learning session processed successfully');
            return this.learningOutcome;

        } catch (error) {
            console.error('❌ Learning session processing failed:', error);
            throw error;
        } finally {
            this.isProcessing = false;
        }
    }

    // Generate realistic EEG simulation based on user input
    async generateEEGSimulation(userInput) {
        const inputComplexity = this.analyzeInputComplexity(userInput);
        const inputLength = userInput.length;
        const typingSpeed = this.calculateTypingSpeed();

        // Simulate EEG data array (like your Python numpy arrays)
        const dataPoints = 256; // Standard EEG sample size
        const eegData = new Float32Array(dataPoints);

        // Generate realistic EEG patterns
        for (let i = 0; i < dataPoints; i++) {
            const time = i / dataPoints;

            // Alpha waves (8-12 Hz) - attention and relaxation
            const alpha = Math.sin(2 * Math.PI * 10 * time) * (0.5 + inputComplexity * 0.3);

            // Beta waves (13-30 Hz) - focused thinking
            const beta = Math.sin(2 * Math.PI * 20 * time) * (0.3 + typingSpeed * 0.4);

            // Theta waves (4-7 Hz) - creativity and learning
            const theta = Math.sin(2 * Math.PI * 6 * time) * (0.2 + this.userTraits.curiosity * 0.3);

            // Gamma waves (30-100 Hz) - consciousness and binding
            const gamma = Math.sin(2 * Math.PI * 40 * time) * (0.1 + inputComplexity * 0.2);

            // Add some realistic noise
            const noise = (Math.random() - 0.5) * 0.1;

            eegData[i] = alpha + beta + theta + gamma + noise;
        }

        return eegData;
    }

    // Calculate EEG metrics (similar to your Python implementation)
    async calculateEEGMetrics(eegData, userInput) {
        // Simulate processing delay (like your sub-millisecond targets)
        await this.simulateProcessingDelay(0.42);

        const inputComplexity = this.analyzeInputComplexity(userInput);
        const focusIndicators = this.calculateFocusIndicators(eegData);

        return {
            attentionIndex: Math.min(0.95, 0.3 + inputComplexity * 0.5 + focusIndicators.attention * 0.2),
            learningEfficiency: Math.min(0.90, 0.4 + this.userTraits.persistence * 0.3 + focusIndicators.stability * 0.3),
            cognitiveLoad: Math.min(0.85, inputComplexity * 0.6 + (userInput.length / 1000) * 0.4),
            neuralAdaptation: Math.min(0.88, this.userTraits.openness * 0.5 + focusIndicators.adaptation * 0.4),
            focusStability: focusIndicators.stability,
            memoryConsolidation: Math.min(0.92, this.userTraits.processingSpeed * 0.4 + focusIndicators.attention * 0.5)
        };
    }

    // Adapt user traits based on behavior (like your adaptive system)
    async adaptUserTraits(userInput, learningContent) {
        const interactionData = {
            inputLength: userInput.length,
            typingSpeed: this.calculateTypingSpeed(),
            complexity: this.analyzeInputComplexity(userInput),
            sessionTime: Date.now() - this.lastInputTime,
            wordCount: userInput.split(' ').filter(word => word.length > 0).length
        };

        // Adaptive algorithms (like your neural adaptation)
        this.userTraits.curiosity = this.adaptTrait(
            this.userTraits.curiosity,
            interactionData.complexity * 0.3 + (interactionData.wordCount > 50 ? 0.2 : 0),
            0.05
        );

        this.userTraits.persistence = this.adaptTrait(
            this.userTraits.persistence,
            (interactionData.sessionTime > 30000 ? 0.2 : 0) + (interactionData.inputLength > 200 ? 0.1 : 0),
            0.03
        );

        this.userTraits.openness = this.adaptTrait(
            this.userTraits.openness,
            interactionData.complexity * 0.4,
            0.04
        );

        this.userTraits.processingSpeed = this.adaptTrait(
            this.userTraits.processingSpeed,
            interactionData.typingSpeed * 0.5,
            0.06
        );

        this.userTraits.learningEfficiency = this.adaptTrait(
            this.userTraits.learningEfficiency,
            (this.eegMetrics.attentionIndex + this.eegMetrics.learningEfficiency) / 2 * 0.3,
            0.04
        );

        // Store adaptation in history
        this.typingHistory.push({
            timestamp: Date.now(),
            traits: { ...this.userTraits },
            interaction: interactionData
        });

        // Keep only recent history (memory management)
        if (this.typingHistory.length > 100) {
            this.typingHistory = this.typingHistory.slice(-50);
        }
    }

    // Calculate learning outcomes (core L.I.F.E. algorithm logic)
    async calculateLearningOutcome(eegMetrics, learningContent, userTraits) {
        // Simulate your advanced neural processing
        await this.simulateProcessingDelay(0.38);

        const contentAnalysis = this.analyzeLearningContent(learningContent);

        return {
            comprehensionScore: Math.min(0.95,
                eegMetrics.attentionIndex * 0.4 +
                userTraits.processingSpeed * 0.3 +
                contentAnalysis.clarity * 0.3
            ),

            retentionProbability: Math.min(0.90,
                eegMetrics.memoryConsolidation * 0.5 +
                userTraits.persistence * 0.3 +
                eegMetrics.focusStability * 0.2
            ),

            optimalReviewTime: this.calculateOptimalReviewTime(eegMetrics, userTraits),

            learningVelocity: Math.min(0.88,
                userTraits.learningEfficiency * 0.4 +
                eegMetrics.neuralAdaptation * 0.4 +
                userTraits.curiosity * 0.2
            ),

            cognitiveResonance: Math.min(0.92,
                (eegMetrics.attentionIndex + eegMetrics.learningEfficiency + userTraits.openness) / 3
            )
        };
    }

    // Real-time adaptation to user behavior
    adaptToUserBehavior(interactionData) {
        if (!this.isInitialized) return;

        // Update traits in real-time
        this.userTraits.curiosity = this.adaptTrait(
            this.userTraits.curiosity,
            interactionData.complexity || 0,
            0.02
        );

        this.userTraits.persistence = this.adaptTrait(
            this.userTraits.persistence,
            (interactionData.inputLength > 100 ? 0.1 : 0),
            0.02
        );

        // Trigger visual updates
        this.updateUIMetrics();
    }

    // Integrate with Azure Functions (like your existing Python backend)
    async syncWithAzureFunctions(data) {
        try {
            const response = await fetch('/api/life-algorithm-sync', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-L.I.F.E-Version': this.version
                },
                body: JSON.stringify({
                    ...data,
                    timestamp: Date.now(),
                    algorithmVersion: this.version,
                    sessionId: this.getSessionId()
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const result = await response.json();
            console.log('✅ Azure Functions sync successful');
            return result;

        } catch (error) {
            console.error('❌ Azure Functions sync failed:', error);
            // Graceful fallback - continue with local processing
            return {
                success: false,
                error: error.message,
                fallback: true
            };
        }
    }

    // Helper Methods
    analyzeInputComplexity(input) {
        if (!input || input.length === 0) return 0;

        const words = input.split(' ').filter(word => word.length > 0);
        const avgWordLength = words.reduce((sum, word) => sum + word.length, 0) / words.length;
        const uniqueWords = new Set(words.map(word => word.toLowerCase())).size;
        const vocabularyRichness = uniqueWords / words.length;

        // Complexity score (0-1)
        return Math.min(1, (avgWordLength / 10) * 0.4 + vocabularyRichness * 0.6);
    }

    calculateTypingSpeed() {
        if (this.typingHistory.length < 2) return 0.5;

        const recent = this.typingHistory.slice(-10);
        const intervals = [];

        for (let i = 1; i < recent.length; i++) {
            const interval = recent[i].timestamp - recent[i - 1].timestamp;
            if (interval > 0 && interval < 5000) { // Ignore very long pauses
                intervals.push(interval);
            }
        }

        if (intervals.length === 0) return 0.5;

        const avgInterval = intervals.reduce((sum, int) => sum + int, 0) / intervals.length;
        const wpm = Math.min(1, 60000 / (avgInterval * 5)); // Rough WPM calculation

        return wpm / 80; // Normalize to 0-1 (80 WPM as reference)
    }

    calculateFocusIndicators(eegData) {
        // Analyze EEG patterns for focus indicators
        let attentionSum = 0;
        let stabilitySum = 0;
        let adaptationSum = 0;

        for (let i = 0; i < eegData.length; i++) {
            const value = Math.abs(eegData[i]);
            attentionSum += value;

            if (i > 0) {
                stabilitySum += Math.abs(eegData[i] - eegData[i - 1]);
            }

            if (i > 10) {
                const trend = eegData.slice(i - 10, i).reduce((sum, v, idx) => sum + v * idx, 0);
                adaptationSum += Math.abs(trend);
            }
        }

        return {
            attention: Math.min(1, attentionSum / eegData.length),
            stability: Math.max(0, 1 - (stabilitySum / eegData.length) * 2),
            adaptation: Math.min(1, adaptationSum / (eegData.length * 100))
        };
    }

    adaptTrait(currentValue, influence, learningRate) {
        const newValue = currentValue + (influence - currentValue) * learningRate;
        return Math.max(0, Math.min(1, newValue));
    }

    calculateOptimalReviewTime(eegMetrics, userTraits) {
        // Based on forgetting curve and user traits
        const baseTime = 24; // hours
        const efficiency = userTraits.learningEfficiency;
        const retention = eegMetrics.memoryConsolidation;

        const optimalHours = baseTime * (2 - efficiency) * (2 - retention);
        return Math.round(optimalHours);
    }

    analyzeLearningContent(content) {
        if (!content || !content.content) {
            return { clarity: 0.5, complexity: 0.5, structure: 0.5 };
        }

        const text = content.content;
        const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 0);
        const avgSentenceLength = sentences.reduce((sum, s) => sum + s.split(' ').length, 0) / sentences.length;

        return {
            clarity: Math.max(0.1, Math.min(1, 1 - (avgSentenceLength - 15) / 30)),
            complexity: this.analyzeInputComplexity(text),
            structure: sentences.length > 0 ? Math.min(1, sentences.length / 10) : 0.1
        };
    }

    setupRealTimeProcessing() {
        // Set up continuous metrics updates
        setInterval(() => {
            if (this.isInitialized && !this.isProcessing) {
                this.updateRealtimeMetrics();
            }
        }, 1000);
    }

    updateRealtimeMetrics() {
        // Simulate slight variations in metrics for realism
        const variation = 0.02;

        Object.keys(this.eegMetrics).forEach(key => {
            const current = this.eegMetrics[key];
            const change = (Math.random() - 0.5) * variation;
            this.eegMetrics[key] = Math.max(0, Math.min(1, current + change));
        });

        this.updateUIMetrics();
    }

    updateUIMetrics() {
        // Update UI elements with current metrics
        try {
            // EEG Metrics
            this.updateMetricDisplay('attention', this.eegMetrics.attentionIndex);
            this.updateMetricDisplay('efficiency', this.eegMetrics.learningEfficiency);
            this.updateMetricDisplay('cognitive', this.eegMetrics.cognitiveLoad);

            // User Traits
            this.updateTraitDisplay('curiosity', this.userTraits.curiosity);
            this.updateTraitDisplay('persistence', this.userTraits.persistence);
            this.updateTraitDisplay('openness', this.userTraits.openness);
            this.updateTraitDisplay('speed', this.userTraits.processingSpeed);
            this.updateTraitDisplay('learning', this.userTraits.learningEfficiency);

        } catch (error) {
            // Silently handle UI update errors
            console.warn('UI update warning:', error.message);
        }
    }

    updateMetricDisplay(metricName, value) {
        const valueElement = document.getElementById(`${metricName}-value`);
        const barElement = document.getElementById(`${metricName}-bar`);

        if (valueElement) {
            valueElement.textContent = `${Math.round(value * 100)}%`;
        }

        if (barElement) {
            barElement.style.width = `${value * 100}%`;
        }
    }

    updateTraitDisplay(traitName, value) {
        const valueElement = document.getElementById(`${traitName}-value`);
        const barElement = document.getElementById(`${traitName}-bar`);

        if (valueElement) {
            valueElement.textContent = `${Math.round(value * 100)}%`;
        }

        if (barElement) {
            barElement.style.width = `${value * 100}%`;
        }
    }

    storeSessionData(sessionData) {
        this.sessionData.push(sessionData);

        // Persist to localStorage
        try {
            localStorage.setItem('life-algorithm-sessions', JSON.stringify(this.sessionData.slice(-50)));
            localStorage.setItem('life-user-traits', JSON.stringify(this.userTraits));
        } catch (error) {
            console.warn('Local storage save failed:', error);
        }
    }

    async loadUserProfile() {
        try {
            const savedTraits = localStorage.getItem('life-user-traits');
            if (savedTraits) {
                this.userTraits = { ...this.userTraits, ...JSON.parse(savedTraits) };
            }

            const savedSessions = localStorage.getItem('life-algorithm-sessions');
            if (savedSessions) {
                this.sessionData = JSON.parse(savedSessions);
            }
        } catch (error) {
            console.warn('Failed to load user profile:', error);
        }
    }

    getSessionId() {
        let sessionId = sessionStorage.getItem('life-session-id');
        if (!sessionId) {
            sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
            sessionStorage.setItem('life-session-id', sessionId);
        }
        return sessionId;
    }

    simulateProcessingDelay(milliseconds) {
        return new Promise(resolve => setTimeout(resolve, milliseconds));
    }

    // Public API methods for external use
    reset() {
        this.eegMetrics = {
            attentionIndex: 0,
            learningEfficiency: 0,
            cognitiveLoad: 0,
            neuralAdaptation: 0,
            focusStability: 0,
            memoryConsolidation: 0
        };

        this.userTraits = {
            curiosity: 0.5,
            persistence: 0.5,
            openness: 0.5,
            processingSpeed: 0.5,
            learningEfficiency: 0.5
        };

        this.updateUIMetrics();
    }

    getStatus() {
        return {
            version: this.version,
            initialized: this.isInitialized,
            processing: this.isProcessing,
            sessionCount: this.sessionData.length,
            eegMetrics: { ...this.eegMetrics },
            userTraits: { ...this.userTraits },
            lastOutcome: { ...this.learningOutcome }
        };
    }

    exportData() {
        return {
            version: this.version,
            timestamp: Date.now(),
            sessionData: this.sessionData,
            userTraits: this.userTraits,
            eegMetrics: this.eegMetrics,
            learningOutcome: this.learningOutcome
        };
    }
}

// Make it available globally
window.LIFEAlgorithmClient = LIFEAlgorithmClient;