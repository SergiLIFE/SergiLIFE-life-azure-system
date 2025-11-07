using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System.Threading.Tasks;
using Newtonsoft.Json;
using UnityEngine.Networking;

namespace LIFEPlatform.VR
{
    /// <summary>
    /// Unity Adaptive Learning Manager with quantum-neural integration
    /// Provides real-time VR environment adaptation based on EEG neuroplasticity
    /// and quantum-optimized learning parameters
    /// </summary>
    public class UnityAdaptiveLearningManager : MonoBehaviour
    {
        [Header("L.I.F.E Platform Configuration")]
        public string lifePlatformApiUrl = "https://life-functions-app.azurewebsites.net/api/";
        public float adaptationUpdateInterval = 2.0f;
        public bool enableQuantumOptimization = true;

        [Header("EEG Thresholds")]
        [Range(0.0f, 1.0f)]
        public float highFocusThreshold = 0.7f;
        [Range(0.0f, 1.0f)]
        public float lowStressThreshold = 0.3f;
        [Range(0.0f, 1.0f)]
        public float neuroplasticityThreshold = 0.5f;

        [Header("Adaptation Parameters")]
        [Range(0.1f, 0.5f)]
        public float complexityAdjustmentRate = 0.2f;
        [Range(0.1f, 2.0f)]
        public float learningAccelerationFactor = 1.5f;

        [Header("VR Environment References")]
        public GameObject[] difficultyLevels;
        public ParticleSystem relaxationEffects;
        public AudioSource focusAudioFeedback;
        public Light environmentLighting;

        // Private variables
        private float currentDifficulty = 0.5f;
        private bool isRelaxationMode = false;
        private float focusEnhancement = 0.0f;
        private Coroutine adaptationCoroutine;
        private Queue<EEGMetrics> eegHistoryBuffer;
        private Dictionary<string, float> learningMetrics;

        // EEG and adaptation data structures
        [System.Serializable]
        public class EEGMetrics
        {
            public float stress_level;
            public float focus_level;
            public float neuroplasticity_index;
            public float hjorth_activity;
            public float hjorth_mobility;
            public float hjorth_complexity;
            public int quantum_features_count;
            public string timestamp;
        }

        [System.Serializable]
        public class VRAdaptationRequest
        {
            public EEGMetrics eeg_data;
            public float[] user_traits;
            public string session_id;
            public bool enable_quantum_optimization;
        }

        [System.Serializable]
        public class VRAdaptationResponse
        {
            public float difficulty_adjustment;
            public bool relaxation_mode;
            public float focus_enhancement;
            public float stress_reduction_factor;
            public float learning_acceleration;
            public string[] immediate_actions;
            public Dictionary<string, object> session_adjustments;
        }

        void Start()
        {
            InitializeAdaptiveLearning();
        }

        /// <summary>
        /// Initialize the adaptive learning system
        /// </summary>
        private void InitializeAdaptiveLearning()
        {
            eegHistoryBuffer = new Queue<EEGMetrics>();
            learningMetrics = new Dictionary<string, float>
            {
                {"total_learning_time", 0f},
                {"adaptation_events", 0f},
                {"focus_improvements", 0f},
                {"stress_reductions", 0f},
                {"difficulty_increases", 0f},
                {"neuroplasticity_boosts", 0f}
            };

            // Start the adaptive learning cycle
            adaptationCoroutine = StartCoroutine(AdaptiveLearningCycle());

            Debug.Log("[L.I.F.E] Unity Adaptive Learning Manager initialized");
            Debug.Log($"[L.I.F.E] API Endpoint: {lifePlatformApiUrl}");
            Debug.Log($"[L.I.F.E] Quantum Optimization: {enableQuantumOptimization}");
        }

        /// <summary>
        /// Main adaptive learning cycle - continuously monitors and adapts VR environment
        /// </summary>
        private IEnumerator AdaptiveLearningCycle()
        {
            while (true)
            {
                yield return new WaitForSeconds(adaptationUpdateInterval);

                // Get current EEG data (simulated for demo - replace with real EEG integration)
                EEGMetrics currentEEG = GetCurrentEEGData();

                // Add to history buffer
                eegHistoryBuffer.Enqueue(currentEEG);
                if (eegHistoryBuffer.Count > 20) // Keep last 20 readings
                {
                    eegHistoryBuffer.Dequeue();
                }

                // Process adaptation
                yield return StartCoroutine(ProcessVRAdaptation(currentEEG));

                // Update learning metrics
                UpdateLearningMetrics();
            }
        }

        /// <summary>
        /// Process VR adaptation based on EEG data and quantum optimization
        /// </summary>
        private IEnumerator ProcessVRAdaptation(EEGMetrics eegData)
        {
            // Create adaptation request
            VRAdaptationRequest request = new VRAdaptationRequest
            {
                eeg_data = eegData,
                user_traits = GetUserTraits(),
                session_id = System.Guid.NewGuid().ToString(),
                enable_quantum_optimization = enableQuantumOptimization
            };

            // Send request to L.I.F.E Platform API
            yield return StartCoroutine(SendAdaptationRequest(request));
        }

        /// <summary>
        /// Send adaptation request to L.I.F.E Platform API
        /// </summary>
        private IEnumerator SendAdaptationRequest(VRAdaptationRequest request)
        {
            string jsonData = JsonConvert.SerializeObject(request);

            using (UnityWebRequest webRequest = new UnityWebRequest($"{lifePlatformApiUrl}vr-adaptation", "POST"))
            {
                byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(jsonData);
                webRequest.uploadHandler = new UploadHandlerRaw(bodyRaw);
                webRequest.downloadHandler = new DownloadHandlerBuffer();
                webRequest.SetRequestHeader("Content-Type", "application/json");

                yield return webRequest.SendWebRequest();

                if (webRequest.result == UnityWebRequest.Result.Success)
                {
                    string responseJson = webRequest.downloadHandler.text;
                    VRAdaptationResponse response = JsonConvert.DeserializeObject<VRAdaptationResponse>(responseJson);

                    // Apply adaptations
                    ApplyVRAdaptations(response);

                    Debug.Log($"[L.I.F.E] VR Adaptation applied: Difficulty={response.difficulty_adjustment:F3}, Focus={response.focus_enhancement:F3}");
                }
                else
                {
                    Debug.LogWarning($"[L.I.F.E] API request failed: {webRequest.error}");

                    // Apply local fallback adaptation
                    ApplyFallbackAdaptation(request.eeg_data);
                }
            }
        }

        /// <summary>
        /// Apply VR adaptations based on L.I.F.E Platform response
        /// </summary>
        private void ApplyVRAdaptations(VRAdaptationResponse response)
        {
            // Update difficulty level
            float newDifficulty = Mathf.Clamp(response.difficulty_adjustment, 0.1f, 1.0f);
            if (Mathf.Abs(newDifficulty - currentDifficulty) > 0.05f)
            {
                currentDifficulty = newDifficulty;
                UpdateDifficultyLevel(currentDifficulty);
                learningMetrics["adaptation_events"]++;

                if (newDifficulty > currentDifficulty)
                {
                    learningMetrics["difficulty_increases"]++;
                }
            }

            // Update relaxation mode
            if (response.relaxation_mode != isRelaxationMode)
            {
                isRelaxationMode = response.relaxation_mode;
                UpdateRelaxationMode(isRelaxationMode);

                if (isRelaxationMode)
                {
                    learningMetrics["stress_reductions"]++;
                }
            }

            // Update focus enhancement
            focusEnhancement = response.focus_enhancement;
            UpdateFocusEnhancement(focusEnhancement);

            if (focusEnhancement > 0.1f)
            {
                learningMetrics["focus_improvements"]++;
            }

            // Process immediate actions
            if (response.immediate_actions != null)
            {
                foreach (string action in response.immediate_actions)
                {
                    ProcessImmediateAction(action);
                }
            }

            // Apply learning acceleration
            if (response.learning_acceleration > 1.0f)
            {
                ApplyLearningAcceleration(response.learning_acceleration);
                learningMetrics["neuroplasticity_boosts"]++;
            }
        }

        /// <summary>
        /// Fallback adaptation when API is unavailable
        /// </summary>
        private void ApplyFallbackAdaptation(EEGMetrics eegData)
        {
            Debug.Log("[L.I.F.E] Applying fallback local adaptation");

            // Local stress-based adaptation
            if (eegData.stress_level > 0.6f)
            {
                // High stress - activate relaxation
                isRelaxationMode = true;
                UpdateRelaxationMode(true);

                // Reduce difficulty
                currentDifficulty = Mathf.Max(0.1f, currentDifficulty - complexityAdjustmentRate);
                UpdateDifficultyLevel(currentDifficulty);
            }

            // Local focus-based adaptation
            if (eegData.focus_level > highFocusThreshold && eegData.stress_level < lowStressThreshold)
            {
                // High focus, low stress - increase difficulty
                currentDifficulty = Mathf.Min(1.0f, currentDifficulty + complexityAdjustmentRate);
                UpdateDifficultyLevel(currentDifficulty);

                isRelaxationMode = false;
                UpdateRelaxationMode(false);
            }

            // Neuroplasticity-based enhancement
            if (eegData.neuroplasticity_index > neuroplasticityThreshold)
            {
                focusEnhancement = 0.3f;
                UpdateFocusEnhancement(focusEnhancement);
                ApplyLearningAcceleration(learningAccelerationFactor);
            }
        }

        /// <summary>
        /// Update VR environment difficulty level
        /// </summary>
        private void UpdateDifficultyLevel(float difficulty)
        {
            // Activate appropriate difficulty level objects
            for (int i = 0; i < difficultyLevels.Length; i++)
            {
                float levelThreshold = (float)(i + 1) / difficultyLevels.Length;
                difficultyLevels[i].SetActive(difficulty >= levelThreshold - 0.2f && difficulty <= levelThreshold + 0.2f);
            }

            Debug.Log($"[L.I.F.E] Difficulty updated to: {difficulty:F3}");
        }

        /// <summary>
        /// Update relaxation mode effects
        /// </summary>
        private void UpdateRelaxationMode(bool enableRelaxation)
        {
            if (relaxationEffects != null)
            {
                if (enableRelaxation)
                {
                    relaxationEffects.Play();

                    // Soft, warm lighting for relaxation
                    if (environmentLighting != null)
                    {
                        environmentLighting.color = new Color(1.0f, 0.8f, 0.6f, 1.0f);
                        environmentLighting.intensity = 0.7f;
                    }
                }
                else
                {
                    relaxationEffects.Stop();

                    // Normal lighting
                    if (environmentLighting != null)
                    {
                        environmentLighting.color = Color.white;
                        environmentLighting.intensity = 1.0f;
                    }
                }
            }

            Debug.Log($"[L.I.F.E] Relaxation mode: {(enableRelaxation ? "ACTIVE" : "INACTIVE")}");
        }

        /// <summary>
        /// Update focus enhancement effects
        /// </summary>
        private void UpdateFocusEnhancement(float enhancement)
        {
            if (focusAudioFeedback != null)
            {
                focusAudioFeedback.volume = Mathf.Clamp01(enhancement);

                if (enhancement > 0.1f && !focusAudioFeedback.isPlaying)
                {
                    focusAudioFeedback.Play();
                }
                else if (enhancement <= 0.1f && focusAudioFeedback.isPlaying)
                {
                    focusAudioFeedback.Stop();
                }
            }

            // Visual focus indicators
            if (enhancement > 0.2f)
            {
                // Add subtle visual focus cues (could be UI elements, particles, etc.)
                Debug.Log($"[L.I.F.E] Focus enhancement active: {enhancement:F3}");
            }
        }

        /// <summary>
        /// Process immediate actions from L.I.F.E Platform
        /// </summary>
        private void ProcessImmediateAction(string action)
        {
            switch (action.ToLower())
            {
                case "activate relaxation protocol":
                    isRelaxationMode = true;
                    UpdateRelaxationMode(true);
                    Debug.Log("[L.I.F.E] Immediate action: Relaxation protocol activated");
                    break;

                case "increase task complexity by 20%":
                    currentDifficulty = Mathf.Min(1.0f, currentDifficulty + 0.2f);
                    UpdateDifficultyLevel(currentDifficulty);
                    Debug.Log("[L.I.F.E] Immediate action: Task complexity increased by 20%");
                    break;

                case "enhance learning acceleration":
                    ApplyLearningAcceleration(learningAccelerationFactor * 1.2f);
                    Debug.Log("[L.I.F.E] Immediate action: Learning acceleration enhanced");
                    break;

                default:
                    Debug.Log($"[L.I.F.E] Unknown immediate action: {action}");
                    break;
            }
        }

        /// <summary>
        /// Apply learning acceleration effects
        /// </summary>
        private void ApplyLearningAcceleration(float accelerationFactor)
        {
            // Could modify time scale, animation speeds, feedback frequency, etc.
            // For demo purposes, we'll just log and could trigger specific learning-enhancing effects

            Debug.Log($"[L.I.F.E] Learning acceleration applied: {accelerationFactor:F2}x");

            // Example: Increase feedback frequency
            if (accelerationFactor > 1.5f)
            {
                // Could trigger more frequent positive feedback, faster transitions, etc.
                StartCoroutine(TemporaryAccelerationEffects(5.0f)); // 5 second boost
            }
        }

        /// <summary>
        /// Temporary acceleration effects
        /// </summary>
        private IEnumerator TemporaryAccelerationEffects(float duration)
        {
            float originalUpdateInterval = adaptationUpdateInterval;
            adaptationUpdateInterval *= 0.5f; // Double the update frequency

            yield return new WaitForSeconds(duration);

            adaptationUpdateInterval = originalUpdateInterval;
            Debug.Log("[L.I.F.E] Learning acceleration effects ended");
        }

        /// <summary>
        /// Get current EEG data (simulated - replace with real EEG device integration)
        /// </summary>
        private EEGMetrics GetCurrentEEGData()
        {
            // Simulated EEG data - in production, this would come from actual EEG device
            return new EEGMetrics
            {
                stress_level = Mathf.Sin(Time.time * 0.3f) * 0.3f + 0.4f, // Oscillating stress
                focus_level = Mathf.Cos(Time.time * 0.2f) * 0.2f + 0.7f,   // Oscillating focus
                neuroplasticity_index = Mathf.Sin(Time.time * 0.1f) * 0.2f + 0.6f,
                hjorth_activity = Random.Range(0.3f, 0.8f),
                hjorth_mobility = Random.Range(0.2f, 0.7f),
                hjorth_complexity = Random.Range(0.4f, 0.9f),
                quantum_features_count = Random.Range(32, 128),
                timestamp = System.DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss")
            };
        }

        /// <summary>
        /// Get user personality traits (simulated - would come from user profile)
        /// </summary>
        private float[] GetUserTraits()
        {
            // Simulated user traits: [curiosity, persistence, openness, processing_speed, learning_efficiency]
            return new float[] { 0.7f, 0.6f, 0.8f, 0.5f, 0.9f };
        }

        /// <summary>
        /// Update learning metrics
        /// </summary>
        private void UpdateLearningMetrics()
        {
            learningMetrics["total_learning_time"] += adaptationUpdateInterval;
        }

        /// <summary>
        /// Get current session statistics
        /// </summary>
        public Dictionary<string, float> GetSessionStatistics()
        {
            var stats = new Dictionary<string, float>(learningMetrics);
            stats["current_difficulty"] = currentDifficulty;
            stats["focus_enhancement"] = focusEnhancement;
            stats["relaxation_active"] = isRelaxationMode ? 1.0f : 0.0f;
            stats["eeg_buffer_size"] = eegHistoryBuffer.Count;

            return stats;
        }

        /// <summary>
        /// Manual trigger for testing adaptations
        /// </summary>
        [ContextMenu("Test High Stress Scenario")]
        public void TestHighStressScenario()
        {
            EEGMetrics testEEG = new EEGMetrics
            {
                stress_level = 0.8f,
                focus_level = 0.3f,
                neuroplasticity_index = 0.2f,
                hjorth_activity = 0.9f,
                hjorth_mobility = 0.7f,
                hjorth_complexity = 0.4f,
                quantum_features_count = 45
            };

            StartCoroutine(ProcessVRAdaptation(testEEG));
            Debug.Log("[L.I.F.E] Testing high stress scenario");
        }

        [ContextMenu("Test High Focus Scenario")]
        public void TestHighFocusScenario()
        {
            EEGMetrics testEEG = new EEGMetrics
            {
                stress_level = 0.2f,
                focus_level = 0.9f,
                neuroplasticity_index = 0.8f,
                hjorth_activity = 0.6f,
                hjorth_mobility = 0.8f,
                hjorth_complexity = 0.9f,
                quantum_features_count = 112
            };

            StartCoroutine(ProcessVRAdaptation(testEEG));
            Debug.Log("[L.I.F.E] Testing high focus scenario");
        }

        void OnDestroy()
        {
            if (adaptationCoroutine != null)
            {
                StopCoroutine(adaptationCoroutine);
            }

            Debug.Log("[L.I.F.E] Unity Adaptive Learning Manager destroyed");
        }

        void OnGUI()
        {
            if (Application.isEditor)
            {
                // Debug GUI for development
                GUILayout.BeginArea(new Rect(10, 10, 300, 200));
                GUILayout.Label("L.I.F.E Platform - VR Adaptation", GUI.skin.box);
                GUILayout.Label($"Difficulty: {currentDifficulty:F3}");
                GUILayout.Label($"Relaxation: {(isRelaxationMode ? "ACTIVE" : "INACTIVE")}");
                GUILayout.Label($"Focus Enhancement: {focusEnhancement:F3}");
                GUILayout.Label($"EEG Buffer: {eegHistoryBuffer.Count}/20");
                GUILayout.Label($"Adaptations: {learningMetrics["adaptation_events"]}");
                GUILayout.EndArea();
            }
        }
    }
}