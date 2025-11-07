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
        {\n            // Create adaptation request\n            VRAdaptationRequest request = new VRAdaptationRequest\n            {\n                eeg_data = eegData,\n                user_traits = GetUserTraits(),\n                session_id = System.Guid.NewGuid().ToString(),\n                enable_quantum_optimization = enableQuantumOptimization\n            };\n            \n            // Send request to L.I.F.E Platform API\n            yield return StartCoroutine(SendAdaptationRequest(request));\n        }\n        \n        /// <summary>\n        /// Send adaptation request to L.I.F.E Platform API\n        /// </summary>\n        private IEnumerator SendAdaptationRequest(VRAdaptationRequest request)\n        {\n            string jsonData = JsonConvert.SerializeObject(request);\n            \n            using (UnityWebRequest webRequest = new UnityWebRequest($\"{lifePlatformApiUrl}vr-adaptation\", \"POST\"))\n            {\n                byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(jsonData);\n                webRequest.uploadHandler = new UploadHandlerRaw(bodyRaw);\n                webRequest.downloadHandler = new DownloadHandlerBuffer();\n                webRequest.SetRequestHeader(\"Content-Type\", \"application/json\");\n                \n                yield return webRequest.SendWebRequest();\n                \n                if (webRequest.result == UnityWebRequest.Result.Success)\n                {\n                    string responseJson = webRequest.downloadHandler.text;\n                    VRAdaptationResponse response = JsonConvert.DeserializeObject<VRAdaptationResponse>(responseJson);\n                    \n                    // Apply adaptations\n                    ApplyVRAdaptations(response);\n                    \n                    Debug.Log($\"[L.I.F.E] VR Adaptation applied: Difficulty={response.difficulty_adjustment:F3}, Focus={response.focus_enhancement:F3}\");\n                }\n                else\n                {\n                    Debug.LogWarning($\"[L.I.F.E] API request failed: {webRequest.error}\");\n                    \n                    // Apply local fallback adaptation\n                    ApplyFallbackAdaptation(request.eeg_data);\n                }\n            }\n        }\n        \n        /// <summary>\n        /// Apply VR adaptations based on L.I.F.E Platform response\n        /// </summary>\n        private void ApplyVRAdaptations(VRAdaptationResponse response)\n        {\n            // Update difficulty level\n            float newDifficulty = Mathf.Clamp(response.difficulty_adjustment, 0.1f, 1.0f);\n            if (Mathf.Abs(newDifficulty - currentDifficulty) > 0.05f)\n            {\n                currentDifficulty = newDifficulty;\n                UpdateDifficultyLevel(currentDifficulty);\n                learningMetrics[\"adaptation_events\"]++;\n                \n                if (newDifficulty > currentDifficulty)\n                {\n                    learningMetrics[\"difficulty_increases\"]++;\n                }\n            }\n            \n            // Update relaxation mode\n            if (response.relaxation_mode != isRelaxationMode)\n            {\n                isRelaxationMode = response.relaxation_mode;\n                UpdateRelaxationMode(isRelaxationMode);\n                \n                if (isRelaxationMode)\n                {\n                    learningMetrics[\"stress_reductions\"]++;\n                }\n            }\n            \n            // Update focus enhancement\n            focusEnhancement = response.focus_enhancement;\n            UpdateFocusEnhancement(focusEnhancement);\n            \n            if (focusEnhancement > 0.1f)\n            {\n                learningMetrics[\"focus_improvements\"]++;\n            }\n            \n            // Process immediate actions\n            if (response.immediate_actions != null)\n            {\n                foreach (string action in response.immediate_actions)\n                {\n                    ProcessImmediateAction(action);\n                }\n            }\n            \n            // Apply learning acceleration\n            if (response.learning_acceleration > 1.0f)\n            {\n                ApplyLearningAcceleration(response.learning_acceleration);\n                learningMetrics[\"neuroplasticity_boosts\"]++;\n            }\n        }\n        \n        /// <summary>\n        /// Fallback adaptation when API is unavailable\n        /// </summary>\n        private void ApplyFallbackAdaptation(EEGMetrics eegData)\n        {\n            Debug.Log(\"[L.I.F.E] Applying fallback local adaptation\");\n            \n            // Local stress-based adaptation\n            if (eegData.stress_level > 0.6f)\n            {\n                // High stress - activate relaxation\n                isRelaxationMode = true;\n                UpdateRelaxationMode(true);\n                \n                // Reduce difficulty\n                currentDifficulty = Mathf.Max(0.1f, currentDifficulty - complexityAdjustmentRate);\n                UpdateDifficultyLevel(currentDifficulty);\n            }\n            \n            // Local focus-based adaptation\n            if (eegData.focus_level > highFocusThreshold && eegData.stress_level < lowStressThreshold)\n            {\n                // High focus, low stress - increase difficulty\n                currentDifficulty = Mathf.Min(1.0f, currentDifficulty + complexityAdjustmentRate);\n                UpdateDifficultyLevel(currentDifficulty);\n                \n                isRelaxationMode = false;\n                UpdateRelaxationMode(false);\n            }\n            \n            // Neuroplasticity-based enhancement\n            if (eegData.neuroplasticity_index > neuroplasticityThreshold)\n            {\n                focusEnhancement = 0.3f;\n                UpdateFocusEnhancement(focusEnhancement);\n                ApplyLearningAcceleration(learningAccelerationFactor);\n            }\n        }\n        \n        /// <summary>\n        /// Update VR environment difficulty level\n        /// </summary>\n        private void UpdateDifficultyLevel(float difficulty)\n        {\n            // Activate appropriate difficulty level objects\n            for (int i = 0; i < difficultyLevels.Length; i++)\n            {\n                float levelThreshold = (float)(i + 1) / difficultyLevels.Length;\n                difficultyLevels[i].SetActive(difficulty >= levelThreshold - 0.2f && difficulty <= levelThreshold + 0.2f);\n            }\n            \n            Debug.Log($\"[L.I.F.E] Difficulty updated to: {difficulty:F3}\");\n        }\n        \n        /// <summary>\n        /// Update relaxation mode effects\n        /// </summary>\n        private void UpdateRelaxationMode(bool enableRelaxation)\n        {\n            if (relaxationEffects != null)\n            {\n                if (enableRelaxation)\n                {\n                    relaxationEffects.Play();\n                    \n                    // Soft, warm lighting for relaxation\n                    if (environmentLighting != null)\n                    {\n                        environmentLighting.color = new Color(1.0f, 0.8f, 0.6f, 1.0f);\n                        environmentLighting.intensity = 0.7f;\n                    }\n                }\n                else\n                {\n                    relaxationEffects.Stop();\n                    \n                    // Normal lighting\n                    if (environmentLighting != null)\n                    {\n                        environmentLighting.color = Color.white;\n                        environmentLighting.intensity = 1.0f;\n                    }\n                }\n            }\n            \n            Debug.Log($\"[L.I.F.E] Relaxation mode: {(enableRelaxation ? \"ACTIVE\" : \"INACTIVE\")}\");\n        }\n        \n        /// <summary>\n        /// Update focus enhancement effects\n        /// </summary>\n        private void UpdateFocusEnhancement(float enhancement)\n        {\n            if (focusAudioFeedback != null)\n            {\n                focusAudioFeedback.volume = Mathf.Clamp01(enhancement);\n                \n                if (enhancement > 0.1f && !focusAudioFeedback.isPlaying)\n                {\n                    focusAudioFeedback.Play();\n                }\n                else if (enhancement <= 0.1f && focusAudioFeedback.isPlaying)\n                {\n                    focusAudioFeedback.Stop();\n                }\n            }\n            \n            // Visual focus indicators\n            if (enhancement > 0.2f)\n            {\n                // Add subtle visual focus cues (could be UI elements, particles, etc.)\n                Debug.Log($\"[L.I.F.E] Focus enhancement active: {enhancement:F3}\");\n            }\n        }\n        \n        /// <summary>\n        /// Process immediate actions from L.I.F.E Platform\n        /// </summary>\n        private void ProcessImmediateAction(string action)\n        {\n            switch (action.ToLower())\n            {\n                case \"activate relaxation protocol\":\n                    isRelaxationMode = true;\n                    UpdateRelaxationMode(true);\n                    Debug.Log(\"[L.I.F.E] Immediate action: Relaxation protocol activated\");\n                    break;\n                    \n                case \"increase task complexity by 20%\":\n                    currentDifficulty = Mathf.Min(1.0f, currentDifficulty + 0.2f);\n                    UpdateDifficultyLevel(currentDifficulty);\n                    Debug.Log(\"[L.I.F.E] Immediate action: Task complexity increased by 20%\");\n                    break;\n                    \n                case \"enhance learning acceleration\":\n                    ApplyLearningAcceleration(learningAccelerationFactor * 1.2f);\n                    Debug.Log(\"[L.I.F.E] Immediate action: Learning acceleration enhanced\");\n                    break;\n                    \n                default:\n                    Debug.Log($\"[L.I.F.E] Unknown immediate action: {action}\");\n                    break;\n            }\n        }\n        \n        /// <summary>\n        /// Apply learning acceleration effects\n        /// </summary>\n        private void ApplyLearningAcceleration(float accelerationFactor)\n        {\n            // Could modify time scale, animation speeds, feedback frequency, etc.\n            // For demo purposes, we'll just log and could trigger specific learning-enhancing effects\n            \n            Debug.Log($\"[L.I.F.E] Learning acceleration applied: {accelerationFactor:F2}x\");\n            \n            // Example: Increase feedback frequency\n            if (accelerationFactor > 1.5f)\n            {\n                // Could trigger more frequent positive feedback, faster transitions, etc.\n                StartCoroutine(TemporaryAccelerationEffects(5.0f)); // 5 second boost\n            }\n        }\n        \n        /// <summary>\n        /// Temporary acceleration effects\n        /// </summary>\n        private IEnumerator TemporaryAccelerationEffects(float duration)\n        {\n            float originalUpdateInterval = adaptationUpdateInterval;\n            adaptationUpdateInterval *= 0.5f; // Double the update frequency\n            \n            yield return new WaitForSeconds(duration);\n            \n            adaptationUpdateInterval = originalUpdateInterval;\n            Debug.Log(\"[L.I.F.E] Learning acceleration effects ended\");\n        }\n        \n        /// <summary>\n        /// Get current EEG data (simulated - replace with real EEG device integration)\n        /// </summary>\n        private EEGMetrics GetCurrentEEGData()\n        {\n            // Simulated EEG data - in production, this would come from actual EEG device\n            return new EEGMetrics\n            {\n                stress_level = Mathf.Sin(Time.time * 0.3f) * 0.3f + 0.4f, // Oscillating stress\n                focus_level = Mathf.Cos(Time.time * 0.2f) * 0.2f + 0.7f,   // Oscillating focus\n                neuroplasticity_index = Mathf.Sin(Time.time * 0.1f) * 0.2f + 0.6f,\n                hjorth_activity = Random.Range(0.3f, 0.8f),\n                hjorth_mobility = Random.Range(0.2f, 0.7f),\n                hjorth_complexity = Random.Range(0.4f, 0.9f),\n                quantum_features_count = Random.Range(32, 128),\n                timestamp = System.DateTime.Now.ToString(\"yyyy-MM-dd HH:mm:ss\")\n            };\n        }\n        \n        /// <summary>\n        /// Get user personality traits (simulated - would come from user profile)\n        /// </summary>\n        private float[] GetUserTraits()\n        {\n            // Simulated user traits: [curiosity, persistence, openness, processing_speed, learning_efficiency]\n            return new float[] { 0.7f, 0.6f, 0.8f, 0.5f, 0.9f };\n        }\n        \n        /// <summary>\n        /// Update learning metrics\n        /// </summary>\n        private void UpdateLearningMetrics()\n        {\n            learningMetrics[\"total_learning_time\"] += adaptationUpdateInterval;\n        }\n        \n        /// <summary>\n        /// Get current session statistics\n        /// </summary>\n        public Dictionary<string, float> GetSessionStatistics()\n        {\n            var stats = new Dictionary<string, float>(learningMetrics);\n            stats[\"current_difficulty\"] = currentDifficulty;\n            stats[\"focus_enhancement\"] = focusEnhancement;\n            stats[\"relaxation_active\"] = isRelaxationMode ? 1.0f : 0.0f;\n            stats[\"eeg_buffer_size\"] = eegHistoryBuffer.Count;\n            \n            return stats;\n        }\n        \n        /// <summary>\n        /// Manual trigger for testing adaptations\n        /// </summary>\n        [ContextMenu(\"Test High Stress Scenario\")]\n        public void TestHighStressScenario()\n        {\n            EEGMetrics testEEG = new EEGMetrics\n            {\n                stress_level = 0.8f,\n                focus_level = 0.3f,\n                neuroplasticity_index = 0.2f,\n                hjorth_activity = 0.9f,\n                hjorth_mobility = 0.7f,\n                hjorth_complexity = 0.4f,\n                quantum_features_count = 45\n            };\n            \n            StartCoroutine(ProcessVRAdaptation(testEEG));\n            Debug.Log(\"[L.I.F.E] Testing high stress scenario\");\n        }\n        \n        [ContextMenu(\"Test High Focus Scenario\")]\n        public void TestHighFocusScenario()\n        {\n            EEGMetrics testEEG = new EEGMetrics\n            {\n                stress_level = 0.2f,\n                focus_level = 0.9f,\n                neuroplasticity_index = 0.8f,\n                hjorth_activity = 0.6f,\n                hjorth_mobility = 0.8f,\n                hjorth_complexity = 0.9f,\n                quantum_features_count = 112\n            };\n            \n            StartCoroutine(ProcessVRAdaptation(testEEG));\n            Debug.Log(\"[L.I.F.E] Testing high focus scenario\");\n        }\n        \n        void OnDestroy()\n        {\n            if (adaptationCoroutine != null)\n            {\n                StopCoroutine(adaptationCoroutine);\n            }\n            \n            Debug.Log(\"[L.I.F.E] Unity Adaptive Learning Manager destroyed\");\n        }\n        \n        void OnGUI()\n        {\n            if (Application.isEditor)\n            {\n                // Debug GUI for development\n                GUILayout.BeginArea(new Rect(10, 10, 300, 200));\n                GUILayout.Label(\"L.I.F.E Platform - VR Adaptation\", GUI.skin.box);\n                GUILayout.Label($\"Difficulty: {currentDifficulty:F3}\");\n                GUILayout.Label($\"Relaxation: {(isRelaxationMode ? \"ACTIVE\" : \"INACTIVE\")}\");\n                GUILayout.Label($\"Focus Enhancement: {focusEnhancement:F3}\");\n                GUILayout.Label($\"EEG Buffer: {eegHistoryBuffer.Count}/20\");\n                GUILayout.Label($\"Adaptations: {learningMetrics[\"adaptation_events\"]}\");\n                GUILayout.EndArea();\n            }\n        }\n    }\n}"