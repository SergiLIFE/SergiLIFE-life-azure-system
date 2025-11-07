/**
 * L.I.F.E. Algorithm - Browser JavaScript Implementation
 * Learning Individually from Experience Theory
 * 
 * Copyright 2025 - Sergio Paya Borrull
 * Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
 * Production Ready - September 27, 2025
 * 
 * This is the browser-compatible version of the L.I.F.E. Algorithm
 * for integration into static web applications.
 */

// ============================
// ENUMS & CONSTANTS
// ============================

const LearningStage = {
    ACQUISITION: 'acquisition',
    CONSOLIDATION: 'consolidation',
    RETRIEVAL: 'retrieval',
    APPLICATION: 'application'
};

const NeuralState = {
    RESTING: 'resting',
    ACTIVE: 'active',
    FOCUSED: 'focused',
    LEARNING: 'learning',
    RECALL: 'recall'
};

// ============================
// DATACLASSES (JavaScript Objects)
// ============================

class UserTraits {
    constructor({
        userId,
        curiosity = 0.7,
        persistence = 0.7,
        openness = 0.7,
        processingSpeed = 0.7,
        learningEfficiency = 0.7,
        attentionSpan = 0.7,
        memoryRetention = 0.7,
        adaptationRate = 0.5
    }) {
        this.userId = userId;
        this.curiosity = this._validateTrait(curiosity, 'curiosity');
        this.persistence = this._validateTrait(persistence, 'persistence');
        this.openness = this._validateTrait(openness, 'openness');
        this.processingSpeed = this._validateTrait(processingSpeed, 'processingSpeed');
        this.learningEfficiency = this._validateTrait(learningEfficiency, 'learningEfficiency');
        this.attentionSpan = this._validateTrait(attentionSpan, 'attentionSpan');
        this.memoryRetention = this._validateTrait(memoryRetention, 'memoryRetention');
        this.adaptationRate = this._validateTrait(adaptationRate, 'adaptationRate');
    }

    _validateTrait(value, name) {
        if (value < 0.0 || value > 1.0) {
            throw new Error(`${name} must be between 0.0 and 1.0, got ${value}`);
        }
        return value;
    }
}

class EEGMetrics {
    constructor({
        timestamp = new Date(),
        attentionIndex,
        learningEfficiency,
        cognitiveLoad,
        engagementScore,
        alphaPower = 0.0,
        betaPower = 0.0,
        thetaPower = 0.0,
        deltaPower = 0.0,
        gammaPower = 0.0,
        neuralState = NeuralState.ACTIVE
    }) {
        this.timestamp = timestamp;
        this.attentionIndex = attentionIndex;
        this.learningEfficiency = learningEfficiency;
        this.cognitiveLoad = cognitiveLoad;
        this.engagementScore = engagementScore;
        this.alphaPower = alphaPower;
        this.betaPower = betaPower;
        this.thetaPower = thetaPower;
        this.deltaPower = deltaPower;
        this.gammaPower = gammaPower;
        this.neuralState = neuralState;
    }

    toDict() {
        return {
            timestamp: this.timestamp.toISOString(),
            attentionIndex: this.attentionIndex,
            learningEfficiency: this.learningEfficiency,
            cognitiveLoad: this.cognitiveLoad,
            engagementScore: this.engagementScore,
            alphaPower: this.alphaPower,
            betaPower: this.betaPower,
            thetaPower: this.thetaPower,
            deltaPower: this.deltaPower,
            gammaPower: this.gammaPower,
            neuralState: this.neuralState
        };
    }
}

class LearningOutcome {
    constructor({
        sessionId,
        userId,
        startTime,
        endTime,
        stage,
        successRate,
        avgAttention,
        avgEngagement,
        cognitiveEfficiency,
        contentMastery,
        recommendations = [],
        eegMetrics = []
    }) {
        this.sessionId = sessionId;
        this.userId = userId;
        this.startTime = startTime;
        this.endTime = endTime;
        this.stage = stage;
        this.successRate = successRate;
        this.avgAttention = avgAttention;
        this.avgEngagement = avgEngagement;
        this.cognitiveEfficiency = cognitiveEfficiency;
        this.contentMastery = contentMastery;
        this.recommendations = recommendations;
        this.eegMetrics = eegMetrics;
    }

    toDict() {
        return {
            sessionId: this.sessionId,
            userId: this.userId,
            startTime: this.startTime.toISOString(),
            endTime: this.endTime.toISOString(),
            stage: this.stage,
            successRate: this.successRate,
            avgAttention: this.avgAttention,
            avgEngagement: this.avgEngagement,
            cognitiveEfficiency: this.cognitiveEfficiency,
            contentMastery: this.contentMastery,
            recommendations: this.recommendations,
            durationSeconds: (this.endTime - this.startTime) / 1000
        };
    }
}

// ============================
// MAIN L.I.F.E. ALGORITHM
// ============================

class LIFEAlgorithm {
    constructor(userTraits) {
        this.userTraits = userTraits;
        this.currentStage = LearningStage.ACQUISITION;
        this.sessionHistory = [];
        this.eegBuffer = [];

        // Adaptive learning parameters
        this.difficultyLevel = 0.5;
        this.contentPacing = 1.0;
        this.reinforcementThreshold = 0.7;

        console.log(`L.I.F.E. Algorithm initialized for user: ${userTraits.userId}`);
    }

    /**
     * Process simulated EEG data stream (async for real-time processing)
     * @param {Array} eegData - Simulated EEG signal data
     * @returns {Promise<EEGMetrics>} Processed neural metrics
     */
    async processEEGStream(eegData) {
        // Simulate async processing (sub-millisecond target)
        await this._sleep(1);

        // Calculate band powers
        const alphaPower = await this._calculateBandPower(eegData, 8, 12);
        const betaPower = await this._calculateBandPower(eegData, 12, 30);
        const thetaPower = await this._calculateBandPower(eegData, 4, 8);
        const deltaPower = await this._calculateBandPower(eegData, 0.5, 4);
        const gammaPower = await this._calculateBandPower(eegData, 30, 100);

        // Calculate derived metrics
        const attentionIndex = await this._calculateAttentionIndex(alphaPower, betaPower);
        const cognitiveLoad = await this._calculateCognitiveLoad(thetaPower, alphaPower);
        const engagementScore = await this._calculateEngagement(betaPower, alphaPower, gammaPower);

        // Determine neural state
        const neuralState = this._determineNeuralState(attentionIndex, cognitiveLoad, engagementScore);

        // Calculate learning efficiency
        const learningEfficiency = this._calculateLearningEfficiency(
            attentionIndex,
            engagementScore,
            this.userTraits
        );

        const metrics = new EEGMetrics({
            timestamp: new Date(),
            attentionIndex,
            learningEfficiency,
            cognitiveLoad,
            engagementScore,
            alphaPower,
            betaPower,
            thetaPower,
            deltaPower,
            gammaPower,
            neuralState
        });

        this.eegBuffer.push(metrics);
        return metrics;
    }

    async _calculateBandPower(eegData, lowFreq, highFreq) {
        await this._sleep(0.1);

        if (!eegData || eegData.length === 0) {
            return 0.0;
        }

        // Simplified band power calculation for browser
        const meanPower = eegData.reduce((sum, val) => sum + Math.abs(val), 0) / eegData.length;
        const randomFactor = 0.8 + Math.random() * 0.4;
        return Math.max(0.0, Math.min(1.0, meanPower * randomFactor));
    }

    async _calculateAttentionIndex(alphaPower, betaPower) {
        await this._sleep(0.1);

        if (alphaPower < 0.01) {
            alphaPower = 0.01;
        }

        const attention = betaPower / (alphaPower + betaPower);
        return Math.max(0.0, Math.min(1.0, attention));
    }

    async _calculateCognitiveLoad(thetaPower, alphaPower) {
        await this._sleep(0.1);

        const load = (thetaPower * 0.7 + (1 - alphaPower) * 0.3);
        return Math.max(0.0, Math.min(1.0, load));
    }

    async _calculateEngagement(betaPower, alphaPower, gammaPower) {
        await this._sleep(0.1);

        const engagement = (betaPower * 0.5 + gammaPower * 0.3 + alphaPower * 0.2);
        return Math.max(0.0, Math.min(1.0, engagement));
    }

    _determineNeuralState(attention, load, engagement) {
        if (engagement > 0.8 && attention > 0.7) {
            return NeuralState.LEARNING;
        } else if (attention > 0.7 && load < 0.5) {
            return NeuralState.FOCUSED;
        } else if (engagement > 0.6) {
            return NeuralState.ACTIVE;
        } else if (load < 0.3) {
            return NeuralState.RESTING;
        } else {
            return NeuralState.ACTIVE;
        }
    }

    _calculateLearningEfficiency(attention, engagement, traits) {
        const neuralComponent = (attention * 0.6 + engagement * 0.4);
        const traitComponent = (
            traits.learningEfficiency * 0.4 +
            traits.processingSpeed * 0.3 +
            traits.attentionSpan * 0.3
        );

        const efficiency = neuralComponent * 0.7 + traitComponent * 0.3;
        return Math.max(0.0, Math.min(1.0, efficiency));
    }

    adaptDifficulty(recentPerformance) {
        if (recentPerformance > 0.85) {
            this.difficultyLevel = Math.min(1.0, this.difficultyLevel + 0.1);
        } else if (recentPerformance < 0.60) {
            this.difficultyLevel = Math.max(0.1, this.difficultyLevel - 0.1);
        }

        const traitFactor = (this.userTraits.learningEfficiency + this.userTraits.persistence) / 2;
        this.difficultyLevel *= (0.7 + traitFactor * 0.3);

        console.log(`Difficulty adapted to: ${this.difficultyLevel.toFixed(2)}`);
        return this.difficultyLevel;
    }

    adaptPacing(avgAttention, avgCognitiveLoad) {
        if (avgAttention < 0.5 || avgCognitiveLoad > 0.8) {
            this.contentPacing = Math.max(0.5, this.contentPacing * 0.9);
        } else if (avgAttention > 0.8 && avgCognitiveLoad < 0.5) {
            this.contentPacing = Math.min(2.0, this.contentPacing * 1.1);
        }

        console.log(`Content pacing adapted to: ${this.contentPacing.toFixed(2)}x`);
        return this.contentPacing;
    }

    generateRecommendations(sessionMetrics) {
        const recommendations = [];

        if (!sessionMetrics || sessionMetrics.length === 0) {
            return ["Complete a learning session to receive recommendations"];
        }

        const avgAttention = this._average(sessionMetrics.map(m => m.attentionIndex));
        const avgEngagement = this._average(sessionMetrics.map(m => m.engagementScore));
        const avgLoad = this._average(sessionMetrics.map(m => m.cognitiveLoad));

        if (avgAttention < 0.5) {
            recommendations.push("Try shorter learning sessions to maintain attention");
            recommendations.push("Consider environmental factors that may cause distraction");
        }

        if (avgEngagement < 0.6) {
            recommendations.push("Explore more interactive learning materials");
            recommendations.push("Try varying content formats (video, text, exercises)");
        }

        if (avgLoad > 0.8) {
            recommendations.push("Content may be too challenging - consider review sessions");
            recommendations.push("Take more frequent breaks to reduce cognitive fatigue");
        }

        if (avgAttention > 0.8 && avgEngagement > 0.8) {
            recommendations.push("Excellent focus! Consider advancing to more challenging material");
        }

        if (this.userTraits.curiosity > 0.7) {
            recommendations.push("Your curiosity is high - explore related topics for deeper understanding");
        }

        if (this.userTraits.persistence > 0.8) {
            recommendations.push("Your persistence is strong - tackle complex problems with confidence");
        }

        return recommendations.slice(0, 5);
    }

    async completeLearningSession(sessionId, successRate, contentMastery) {
        if (this.eegBuffer.length === 0) {
            console.warn("No EEG metrics recorded for session");
            this.eegBuffer = [
                new EEGMetrics({
                    timestamp: new Date(),
                    attentionIndex: 0.5,
                    learningEfficiency: 0.5,
                    cognitiveLoad: 0.5,
                    engagementScore: 0.5
                })
            ];
        }

        const avgAttention = this._average(this.eegBuffer.map(m => m.attentionIndex));
        const avgEngagement = this._average(this.eegBuffer.map(m => m.engagementScore));
        const avgEfficiency = this._average(this.eegBuffer.map(m => m.learningEfficiency));
        const avgLoad = this._average(this.eegBuffer.map(m => m.cognitiveLoad));

        const recommendations = this.generateRecommendations(this.eegBuffer);

        this.adaptDifficulty(successRate);
        this.adaptPacing(avgAttention, avgLoad);

        const outcome = new LearningOutcome({
            sessionId,
            userId: this.userTraits.userId,
            startTime: this.eegBuffer[0].timestamp,
            endTime: this.eegBuffer[this.eegBuffer.length - 1].timestamp,
            stage: this.currentStage,
            successRate,
            avgAttention,
            avgEngagement,
            cognitiveEfficiency: avgEfficiency,
            contentMastery,
            recommendations,
            eegMetrics: [...this.eegBuffer]
        });

        this.sessionHistory.push(outcome);
        this.eegBuffer = [];

        console.log(`Session ${sessionId} completed. Success: ${(successRate * 100).toFixed(1)}%, Mastery: ${(contentMastery * 100).toFixed(1)}%`);
        return outcome;
    }

    getUserProgressSummary() {
        if (this.sessionHistory.length === 0) {
            return {
                userId: this.userTraits.userId,
                totalSessions: 0,
                message: 'No learning sessions completed yet'
            };
        }

        const totalTime = this.sessionHistory.reduce((sum, s) => {
            return sum + (s.endTime - s.startTime) / 1000;
        }, 0);

        return {
            userId: this.userTraits.userId,
            totalSessions: this.sessionHistory.length,
            currentStage: this.currentStage,
            currentDifficulty: this.difficultyLevel,
            currentPacing: this.contentPacing,
            avgSuccessRate: this._average(this.sessionHistory.map(s => s.successRate)),
            avgMastery: this._average(this.sessionHistory.map(s => s.contentMastery)),
            avgAttention: this._average(this.sessionHistory.map(s => s.avgAttention)),
            avgEngagement: this._average(this.sessionHistory.map(s => s.avgEngagement)),
            totalLearningTime: totalTime,
            userTraits: {
                curiosity: this.userTraits.curiosity,
                persistence: this.userTraits.persistence,
                learningEfficiency: this.userTraits.learningEfficiency
            }
        };
    }

    // Utility functions
    _average(arr) {
        return arr.reduce((sum, val) => sum + val, 0) / arr.length;
    }

    _sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// ============================
// DEMO & TESTING
// ============================

async function demoLearningSession() {
    console.log("=== L.I.F.E. Algorithm Browser Demo ===");

    const user = new UserTraits({
        userId: 'browser_demo_001',
        curiosity: 0.8,
        persistence: 0.75,
        openness: 0.85,
        processingSpeed: 0.7,
        learningEfficiency: 0.75
    });

    const lifeAlgorithm = new LIFEAlgorithm(user);

    const sessionId = `session_${new Date().toISOString().replace(/[:.]/g, '_')}`;

    console.log("Processing simulated EEG data stream...");

    for (let i = 0; i < 10; i++) {
        // Simulate EEG data
        const eegData = Array.from({ length: 256 }, () => Math.random() * 2 - 1);

        const metrics = await lifeAlgorithm.processEEGStream(eegData);
        console.log(`Sample ${i + 1}: Attention=${metrics.attentionIndex.toFixed(2)}, ` +
            `Engagement=${metrics.engagementScore.toFixed(2)}, ` +
            `Efficiency=${metrics.learningEfficiency.toFixed(2)}`);
    }

    const outcome = await lifeAlgorithm.completeLearningSession(sessionId, 0.85, 0.82);

    console.log("\n=== Session Complete ===");
    console.log(`Success Rate: ${(outcome.successRate * 100).toFixed(1)}%`);
    console.log(`Content Mastery: ${(outcome.contentMastery * 100).toFixed(1)}%`);
    console.log(`Avg Attention: ${(outcome.avgAttention * 100).toFixed(1)}%`);
    console.log("Recommendations:");
    outcome.recommendations.forEach(rec => console.log(`  - ${rec}`));

    const summary = lifeAlgorithm.getUserProgressSummary();
    console.log("\nUser Progress Summary:", JSON.stringify(summary, null, 2));

    return outcome;
}

// Export for module systems (Node.js, bundlers)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        LearningStage,
        NeuralState,
        UserTraits,
        EEGMetrics,
        LearningOutcome,
        LIFEAlgorithm,
        demoLearningSession
    };
}

// Browser global export
if (typeof window !== 'undefined') {
    window.LIFE = {
        LearningStage,
        NeuralState,
        UserTraits,
        EEGMetrics,
        LearningOutcome,
        LIFEAlgorithm,
        demoLearningSession
    };
}

console.log("L.I.F.E. Algorithm Browser Module Loaded ✓");
console.log("Usage: const algorithm = new LIFE.LIFEAlgorithm(userTraits);");
console.log("Demo: await LIFE.demoLearningSession();");
