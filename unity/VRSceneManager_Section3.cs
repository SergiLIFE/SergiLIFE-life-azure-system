using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using Newtonsoft.Json;
using UnityEngine.Networking;

namespace LIFEPlatform.VR.Section3
{
    /// <summary>
    /// Advanced VR Scene Manager for Section 3 Multi-Domain Integration
    /// Handles dynamic difficulty adjustment across Corporate Training, Healthcare, Education domains
    /// Integrates with Ultimate L.I.F.E Algorithm for real-time neuroadaptive environments
    /// </summary>
    public class VRSceneManager : MonoBehaviour
    {
        [Header("L.I.F.E Platform Section 3 Configuration")]
        public string lifeApiEndpoint = "https://life-functions-app.azurewebsites.net/api/";
        public float difficultyUpdateInterval = 1.5f;
        public bool enableMultiDomainAdaptation = true;

        [Header("Domain-Specific Settings")]
        [Range(0.0f, 1.0f)]
        public float corporateTrainingDifficulty = 0.5f;
        [Range(0.0f, 1.0f)]
        public float healthcareRehabDifficulty = 0.3f;
        [Range(0.0f, 1.0f)]
        public float educationDifficulty = 0.6f;

        [Header("Neuroadaptive Thresholds")]
        [Range(0.0f, 1.0f)]
        public float stressThresholdHigh = 0.7f;
        [Range(0.0f, 1.0f)]
        public float stressThresholdLow = 0.3f;
        [Range(0.0f, 1.0f)]
        public float focusThresholdHigh = 0.8f;
        [Range(0.0f, 1.0f)]
        public float motorIntentThreshold = 0.6f;

        [Header("Scene Components")]
        public ScenarioManager scenarioManager;
        public GameObject[] corporateTrainingScenarios;
        public GameObject[] healthcareRehabScenarios;
        public GameObject[] educationScenarios;
        public ParticleSystem stressReductionEffects;
        public AudioSource biofeedbackAudio;
        public Light adaptiveEnvironmentLighting;

        // Private variables
        private CurrentDomain activeDomain = CurrentDomain.CorporateTraining;
        private float currentStressLevel = 0.3f;
        private float currentFocusLevel = 0.7f;
        private string currentMotorIntent = "rest";
        private Coroutine adaptationCoroutine;
        private Queue<BiometricData> biometricHistory;
        private Dictionary<string, float> domainDifficulties;

        // Data structures for Section 3 integration
        public enum CurrentDomain
        {
            CorporateTraining,
            Healthcare,
            Education,
            Technology,
            Finance
        }

        [System.Serializable]
        public class BiometricData
        {
            public float stress_level;
            public float focus_level;
            public float alpha_power;
            public float beta_power;
            public float theta_power;
            public float gamma_power;
            public string motor_intent;
            public float neuroplasticity_index;
            public string timestamp;
        }

        [System.Serializable]
        public class MultiDomainAdaptationRequest
        {
            public BiometricData biometrics;
            public CurrentDomain active_domain;
            public Dictionary<string, float> domain_difficulties;
            public bool enable_quantum_optimization;
            public bool enable_blockchain_tracking;
            public string session_id;
        }

        [System.Serializable]
        public class AdaptationResponse
        {
            public Dictionary<string, float> domain_adjustments;
            public bool activate_stress_reduction;
            public bool enhance_focus;
            public string recommended_scenario;
            public float learning_acceleration;
            public string[] immediate_actions;
            public bool mint_skill_nft;
        }

        void Start()
        {
            InitializeMultiDomainVR();
        }

        /// <summary>
        /// Initialize multi-domain VR system
        /// </summary>
        private void InitializeMultiDomainVR()
        {
            biometricHistory = new Queue<BiometricData>();
            domainDifficulties = new Dictionary<string, float>
            {
                {"corporate_training", corporateTrainingDifficulty},
                {"healthcare", healthcareRehabDifficulty},
                {"education", educationDifficulty},
                {"technology", 0.4f},
                {"finance", 0.5f}
            };

            // Initialize ScenarioManager if not assigned
            if (scenarioManager == null)
            {
                scenarioManager = FindObjectOfType<ScenarioManager>();
                if (scenarioManager == null)
                {
                    Debug.LogWarning("[L.I.F.E VR] ScenarioManager not found - creating mock implementation");
                    CreateMockScenarioManager();
                }
            }

            // Start the multi-domain adaptation cycle
            adaptationCoroutine = StartCoroutine(MultiDomainAdaptationCycle());

            Debug.Log("[L.I.F.E VR] Multi-Domain VR Scene Manager initialized");
            Debug.Log($"[L.I.F.E VR] Active Domain: {activeDomain}");
            Debug.Log($"[L.I.F.E VR] Multi-Domain Adaptation: {enableMultiDomainAdaptation}");
        }

        /// <summary>
        /// Create mock ScenarioManager for standalone operation
        /// </summary>
        private void CreateMockScenarioManager()
        {
            GameObject mockManager = new GameObject("MockScenarioManager");
            scenarioManager = mockManager.AddComponent<MockScenarioManager>();
        }

        /// <summary>
        /// Main multi-domain adaptation cycle
        /// </summary>
        private IEnumerator MultiDomainAdaptationCycle()
        {
            while (true)
            {
                yield return new WaitForSeconds(difficultyUpdateInterval);

                // Get current biometric data
                BiometricData currentBiometrics = GetCurrentBiometrics();

                // Add to history buffer
                biometricHistory.Enqueue(currentBiometrics);
                if (biometricHistory.Count > 30) // Keep last 30 readings
                {
                    biometricHistory.Dequeue();
                }

                // Process multi-domain adaptation
                yield return StartCoroutine(ProcessMultiDomainAdaptation(currentBiometrics));

                // Update current stress and focus levels
                currentStressLevel = currentBiometrics.stress_level;
                currentFocusLevel = currentBiometrics.focus_level;
                currentMotorIntent = currentBiometrics.motor_intent;
            }
        }

        /// <summary>
        /// Process multi-domain VR adaptation
        /// </summary>
        private IEnumerator ProcessMultiDomainAdaptation(BiometricData biometrics)
        {
            if (!enableMultiDomainAdaptation)
            {
                // Fallback to simple domain-specific adaptation
                ApplyDomainSpecificAdaptation(biometrics);
                yield break;
            }

            // Create multi-domain adaptation request
            MultiDomainAdaptationRequest request = new MultiDomainAdaptationRequest
            {
                biometrics = biometrics,
                active_domain = activeDomain,
                domain_difficulties = domainDifficulties,
                enable_quantum_optimization = true,
                enable_blockchain_tracking = true,
                session_id = System.Guid.NewGuid().ToString()
            };

            // Send to L.I.F.E Platform Ultimate API
            yield return StartCoroutine(SendMultiDomainRequest(request));
        }

        /// <summary>
        /// Send multi-domain adaptation request to L.I.F.E Ultimate API
        /// </summary>
        private IEnumerator SendMultiDomainRequest(MultiDomainAdaptationRequest request)
        {
            string jsonData = JsonConvert.SerializeObject(request);

            using (UnityWebRequest webRequest = new UnityWebRequest($"{lifeApiEndpoint}multi-domain-adaptation", "POST"))
            {
                byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(jsonData);
                webRequest.uploadHandler = new UploadHandlerRaw(bodyRaw);
                webRequest.downloadHandler = new DownloadHandlerBuffer();
                webRequest.SetRequestHeader("Content-Type", "application/json");
                webRequest.SetRequestHeader("X-L.I.F.E-Version", "Ultimate-v3.0");

                yield return webRequest.SendWebRequest();

                if (webRequest.result == UnityWebRequest.Result.Success)
                {
                    string responseJson = webRequest.downloadHandler.text;
                    AdaptationResponse response = JsonConvert.DeserializeObject<AdaptationResponse>(responseJson);

                    // Apply multi-domain adaptations
                    ApplyMultiDomainAdaptations(response);

                    Debug.Log($"[L.I.F.E VR] Multi-domain adaptation applied successfully");
                }
                else
                {
                    Debug.LogWarning($"[L.I.F.E VR] Multi-domain API request failed: {webRequest.error}");

                    // Fallback to local adaptation
                    ApplyDomainSpecificAdaptation(request.biometrics);
                }
            }
        }

        /// <summary>
        /// Apply multi-domain adaptations from L.I.F.E Ultimate response
        /// </summary>
        private void ApplyMultiDomainAdaptations(AdaptationResponse response)
        {
            // Update domain difficulties
            foreach (var adjustment in response.domain_adjustments)
            {
                if (domainDifficulties.ContainsKey(adjustment.Key))
                {
                    domainDifficulties[adjustment.Key] = Mathf.Clamp01(adjustment.Value);
                    Debug.Log($"[L.I.F.E VR] {adjustment.Key} difficulty updated to {adjustment.Value:F3}");
                }
            }

            // Apply current domain difficulty
            string currentDomainKey = activeDomain.ToString().ToLower().Replace("corporatetraining", "corporate_training");
            if (domainDifficulties.ContainsKey(currentDomainKey))
            {
                UpdateSceneDifficulty(domainDifficulties[currentDomainKey]);
            }

            // Handle stress reduction
            if (response.activate_stress_reduction)
            {
                ActivateStressReduction();
            }

            // Handle focus enhancement
            if (response.enhance_focus)
            {
                EnhanceFocus();
            }

            // Switch scenario if recommended
            if (!string.IsNullOrEmpty(response.recommended_scenario))
            {
                SwitchToScenario(response.recommended_scenario);
            }

            // Apply learning acceleration
            if (response.learning_acceleration > 1.0f)
            {
                ApplyLearningAcceleration(response.learning_acceleration);
            }

            // Process immediate actions
            if (response.immediate_actions != null)
            {
                foreach (string action in response.immediate_actions)
                {
                    ProcessImmediateAction(action);
                }
            }

            // Handle NFT minting
            if (response.mint_skill_nft)
            {
                Debug.Log("[L.I.F.E VR] Skill mastery detected - NFT minting recommended");
                ShowSkillMasteryNotification();
            }
        }

        /// <summary>
        /// Apply domain-specific adaptation (fallback)
        /// </summary>
        private void ApplyDomainSpecificAdaptation(BiometricData biometrics)
        {
            Debug.Log("[L.I.F.E VR] Applying domain-specific fallback adaptation");

            switch (activeDomain)
            {
                case CurrentDomain.CorporateTraining:
                    ApplyCorporateTrainingAdaptation(biometrics);
                    break;

                case CurrentDomain.Healthcare:
                    ApplyHealthcareAdaptation(biometrics);
                    break;

                case CurrentDomain.Education:
                    ApplyEducationAdaptation(biometrics);
                    break;

                case CurrentDomain.Technology:
                    ApplyTechnologyAdaptation(biometrics);
                    break;

                case CurrentDomain.Finance:
                    ApplyFinanceAdaptation(biometrics);
                    break;
            }
        }

        /// <summary>
        /// Corporate Training domain adaptation
        /// </summary>
        private void ApplyCorporateTrainingAdaptation(BiometricData biometrics)
        {
            // Stress-based difficulty adjustment for corporate training
            if (biometrics.stress_level > stressThresholdHigh)
            {
                // High stress - reduce difficulty and activate relaxation
                corporateTrainingDifficulty = Mathf.Max(0.1f, corporateTrainingDifficulty - 0.2f);
                UpdateSceneDifficulty(corporateTrainingDifficulty);
                ActivateStressReduction();

                Debug.Log("[L.I.F.E VR] Corporate Training: High stress detected - reducing difficulty");
            }
            else if (biometrics.stress_level < stressThresholdLow && biometrics.focus_level > focusThresholdHigh)
            {
                // Low stress, high focus - increase difficulty
                corporateTrainingDifficulty = Mathf.Min(1.0f, corporateTrainingDifficulty + 0.15f);
                UpdateSceneDifficulty(corporateTrainingDifficulty);

                Debug.Log("[L.I.F.E VR] Corporate Training: Optimal state - increasing difficulty");
            }
        }

        /// <summary>
        /// Healthcare domain adaptation (rehabilitation focus)
        /// </summary>
        private void ApplyHealthcareAdaptation(BiometricData biometrics)
        {
            // Motor intent-based adaptation for healthcare
            if (!string.IsNullOrEmpty(biometrics.motor_intent) && biometrics.motor_intent != "rest")
            {
                // Motor intent detected - adjust scenario accordingly
                if (biometrics.motor_intent == "left_hand" || biometrics.motor_intent == "right_hand")
                {
                    SwitchToScenario("hand_rehabilitation");
                    Debug.Log($"[L.I.F.E VR] Healthcare: {biometrics.motor_intent} intent - activating hand rehab");
                }
                else if (biometrics.motor_intent == "feet")
                {
                    SwitchToScenario("mobility_training");
                    Debug.Log("[L.I.F.E VR] Healthcare: Feet movement intent - activating mobility training");
                }
            }

            // Gradual difficulty progression for rehabilitation
            if (biometrics.focus_level > 0.7f && biometrics.stress_level < 0.4f)
            {
                healthcareRehabDifficulty = Mathf.Min(0.8f, healthcareRehabDifficulty + 0.05f);
                UpdateSceneDifficulty(healthcareRehabDifficulty);
            }
        }

        /// <summary>
        /// Education domain adaptation
        /// </summary>
        private void ApplyEducationAdaptation(BiometricData biometrics)
        {
            // Neuroplasticity-based adaptation for education
            if (biometrics.neuroplasticity_index > 0.7f)
            {
                // High neuroplasticity - accelerate learning
                ApplyLearningAcceleration(1.5f);
                educationDifficulty = Mathf.Min(1.0f, educationDifficulty + 0.1f);

                Debug.Log("[L.I.F.E VR] Education: High neuroplasticity - accelerating learning");
            }
            else if (biometrics.neuroplasticity_index < 0.3f)
            {
                // Low neuroplasticity - provide more support
                educationDifficulty = Mathf.Max(0.2f, educationDifficulty - 0.1f);
                EnhanceFocus();

                Debug.Log("[L.I.F.E VR] Education: Low neuroplasticity - providing support");
            }

            UpdateSceneDifficulty(educationDifficulty);
        }

        /// <summary>
        /// Technology domain adaptation
        /// </summary>
        private void ApplyTechnologyAdaptation(BiometricData biometrics)
        {
            // Quantum-inspired adaptation for technology training
            float quantumComplexity = (biometrics.alpha_power + biometrics.gamma_power) / 2.0f;

            if (quantumComplexity > 0.6f && biometrics.focus_level > 0.7f)
            {
                // High quantum processing capability
                domainDifficulties["technology"] = Mathf.Min(1.0f, domainDifficulties["technology"] + 0.2f);
                Debug.Log("[L.I.F.E VR] Technology: High quantum processing - increasing complexity");
            }

            UpdateSceneDifficulty(domainDifficulties["technology"]);
        }

        /// <summary>
        /// Finance domain adaptation
        /// </summary>
        private void ApplyFinanceAdaptation(BiometricData biometrics)
        {
            // Risk assessment based adaptation for finance
            float riskTolerance = biometrics.beta_power / (biometrics.alpha_power + 1e-6f);

            if (riskTolerance > 1.5f)
            {
                // High risk tolerance - present more complex scenarios
                domainDifficulties["finance"] = Mathf.Min(0.9f, domainDifficulties["finance"] + 0.15f);
                Debug.Log("[L.I.F.E VR] Finance: High risk tolerance - increasing scenario complexity");
            }
            else if (riskTolerance < 0.5f)
            {
                // Low risk tolerance - present conservative scenarios
                domainDifficulties["finance"] = Mathf.Max(0.2f, domainDifficulties["finance"] - 0.1f);
                Debug.Log("[L.I.F.E VR] Finance: Low risk tolerance - conservative scenarios");
            }

            UpdateSceneDifficulty(domainDifficulties["finance"]);
        }

        /// <summary>
        /// Update scene difficulty using ScenarioManager
        /// </summary>
        public void UpdateSceneDifficulty(float stressLevel)
        {
            if (scenarioManager != null)
            {
                if (stressLevel > stressThresholdHigh)
                {
                    scenarioManager.AdjustDifficulty(-0.2f);
                    Debug.Log($"[L.I.F.E VR] Difficulty decreased due to high stress: {stressLevel:F3}");
                }
                else if (stressLevel < stressThresholdLow)
                {
                    scenarioManager.AdjustDifficulty(0.15f);
                    Debug.Log($"[L.I.F.E VR] Difficulty increased due to low stress: {stressLevel:F3}");
                }
            }
        }

        /// <summary>
        /// Activate stress reduction protocols
        /// </summary>
        private void ActivateStressReduction()
        {
            if (stressReductionEffects != null)
            {
                stressReductionEffects.Play();
            }

            if (adaptiveEnvironmentLighting != null)
            {
                // Soft, warm lighting for stress reduction
                adaptiveEnvironmentLighting.color = new Color(0.8f, 0.9f, 1.0f, 1.0f);
                adaptiveEnvironmentLighting.intensity = 0.6f;
            }

            if (biofeedbackAudio != null)
            {
                // Play calming audio feedback
                biofeedbackAudio.pitch = 0.8f;
                if (!biofeedbackAudio.isPlaying)
                {
                    biofeedbackAudio.Play();
                }
            }

            Debug.Log("[L.I.F.E VR] Stress reduction protocols activated");
        }

        /// <summary>
        /// Enhance focus and attention
        /// </summary>
        private void EnhanceFocus()
        {
            if (adaptiveEnvironmentLighting != null)
            {
                // Bright, focused lighting for attention enhancement
                adaptiveEnvironmentLighting.color = Color.white;
                adaptiveEnvironmentLighting.intensity = 1.2f;
            }

            if (biofeedbackAudio != null)
            {
                // Play focus-enhancing audio
                biofeedbackAudio.pitch = 1.2f;
                biofeedbackAudio.volume = 0.7f;
            }

            Debug.Log("[L.I.F.E VR] Focus enhancement activated");
        }

        /// <summary>
        /// Switch to specific scenario
        /// </summary>
        private void SwitchToScenario(string scenarioName)
        {
            Debug.Log($"[L.I.F.E VR] Switching to scenario: {scenarioName}");

            // Deactivate all scenarios first
            DeactivateAllScenarios();

            // Activate specific scenario based on name and domain
            switch (scenarioName.ToLower())
            {
                case "hand_rehabilitation":
                    ActivateScenarioSet(healthcareRehabScenarios, 0);
                    break;

                case "mobility_training":
                    ActivateScenarioSet(healthcareRehabScenarios, 1);
                    break;

                case "corporate_presentation":
                    ActivateScenarioSet(corporateTrainingScenarios, 0);
                    break;

                case "team_collaboration":
                    ActivateScenarioSet(corporateTrainingScenarios, 1);
                    break;

                case "interactive_learning":
                    ActivateScenarioSet(educationScenarios, 0);
                    break;

                case "skill_assessment":
                    ActivateScenarioSet(educationScenarios, 1);
                    break;

                default:
                    Debug.LogWarning($"[L.I.F.E VR] Unknown scenario: {scenarioName}");
                    break;
            }
        }

        /// <summary>
        /// Deactivate all scenario sets
        /// </summary>
        private void DeactivateAllScenarios()
        {
            DeactivateScenarioSet(corporateTrainingScenarios);
            DeactivateScenarioSet(healthcareRehabScenarios);
            DeactivateScenarioSet(educationScenarios);
        }

        /// <summary>
        /// Activate specific scenario from set
        /// </summary>
        private void ActivateScenarioSet(GameObject[] scenarios, int index)
        {
            if (scenarios != null && index >= 0 && index < scenarios.Length)
            {
                if (scenarios[index] != null)
                {
                    scenarios[index].SetActive(true);
                    Debug.Log($"[L.I.F.E VR] Activated scenario {index} from set");
                }
            }
        }

        /// <summary>
        /// Deactivate entire scenario set
        /// </summary>
        private void DeactivateScenarioSet(GameObject[] scenarios)
        {
            if (scenarios != null)
            {
                foreach (GameObject scenario in scenarios)
                {
                    if (scenario != null)
                    {
                        scenario.SetActive(false);
                    }
                }
            }
        }

        /// <summary>
        /// Apply learning acceleration effects
        /// </summary>
        private void ApplyLearningAcceleration(float accelerationFactor)
        {
            Debug.Log($"[L.I.F.E VR] Learning acceleration applied: {accelerationFactor:F2}x");

            // Increase update frequency during acceleration
            if (accelerationFactor > 1.3f)
            {
                StartCoroutine(TemporaryAcceleration(accelerationFactor, 10.0f));
            }
        }

        /// <summary>
        /// Temporary learning acceleration effects
        /// </summary>
        private IEnumerator TemporaryAcceleration(float factor, float duration)
        {
            float originalInterval = difficultyUpdateInterval;
            difficultyUpdateInterval /= factor;

            Debug.Log($"[L.I.F.E VR] Temporary acceleration: {factor:F2}x for {duration} seconds");

            yield return new WaitForSeconds(duration);

            difficultyUpdateInterval = originalInterval;
            Debug.Log("[L.I.F.E VR] Learning acceleration ended");
        }

        /// <summary>
        /// Process immediate actions from L.I.F.E Ultimate
        /// </summary>
        private void ProcessImmediateAction(string action)
        {
            switch (action.ToLower())
            {
                case "switch_to_healthcare":
                    SwitchDomain(CurrentDomain.Healthcare);
                    break;

                case "switch_to_corporate":
                    SwitchDomain(CurrentDomain.CorporateTraining);
                    break;

                case "switch_to_education":
                    SwitchDomain(CurrentDomain.Education);
                    break;

                case "activate_quantum_mode":
                    SwitchDomain(CurrentDomain.Technology);
                    break;

                case "enable_blockchain_tracking":
                    SwitchDomain(CurrentDomain.Finance);
                    break;

                case "emergency_stress_reduction":
                    ActivateStressReduction();
                    UpdateSceneDifficulty(0.2f); // Very low difficulty
                    break;

                default:
                    Debug.Log($"[L.I.F.E VR] Unknown immediate action: {action}");
                    break;
            }
        }

        /// <summary>
        /// Switch active domain
        /// </summary>
        public void SwitchDomain(CurrentDomain newDomain)
        {
            if (activeDomain != newDomain)
            {
                activeDomain = newDomain;
                Debug.Log($"[L.I.F.E VR] Switched to domain: {newDomain}");

                // Apply domain-specific settings
                ApplyDomainSettings(newDomain);
            }
        }

        /// <summary>
        /// Apply domain-specific settings
        /// </summary>
        private void ApplyDomainSettings(CurrentDomain domain)
        {
            switch (domain)
            {
                case CurrentDomain.CorporateTraining:
                    // Activate corporate scenarios
                    DeactivateAllScenarios();
                    if (corporateTrainingScenarios != null && corporateTrainingScenarios.Length > 0)
                    {
                        ActivateScenarioSet(corporateTrainingScenarios, 0);
                    }
                    break;

                case CurrentDomain.Healthcare:
                    // Activate healthcare scenarios
                    DeactivateAllScenarios();
                    if (healthcareRehabScenarios != null && healthcareRehabScenarios.Length > 0)
                    {
                        ActivateScenarioSet(healthcareRehabScenarios, 0);
                    }
                    break;

                case CurrentDomain.Education:
                    // Activate education scenarios
                    DeactivateAllScenarios();
                    if (educationScenarios != null && educationScenarios.Length > 0)
                    {
                        ActivateScenarioSet(educationScenarios, 0);
                    }
                    break;

                case CurrentDomain.Technology:
                    // Technology domain settings (quantum-inspired)
                    if (adaptiveEnvironmentLighting != null)
                    {
                        adaptiveEnvironmentLighting.color = new Color(0.5f, 0.8f, 1.0f);
                    }
                    break;

                case CurrentDomain.Finance:
                    // Finance domain settings (blockchain-focused)
                    if (adaptiveEnvironmentLighting != null)
                    {
                        adaptiveEnvironmentLighting.color = new Color(1.0f, 0.8f, 0.2f);
                    }
                    break;
            }
        }

        /// <summary>
        /// Show skill mastery notification for NFT minting
        /// </summary>
        private void ShowSkillMasteryNotification()
        {
            Debug.Log("[L.I.F.E VR] 🎉 SKILL MASTERY ACHIEVED! NFT certification available.");

            // In production, would show UI notification for NFT minting
            // For now, just log the achievement
            StartCoroutine(DisplayMasteryEffect());
        }

        /// <summary>
        /// Display visual effects for skill mastery
        /// </summary>
        private IEnumerator DisplayMasteryEffect()
        {
            // Golden lighting effect for achievement
            if (adaptiveEnvironmentLighting != null)
            {
                Color originalColor = adaptiveEnvironmentLighting.color;
                float originalIntensity = adaptiveEnvironmentLighting.intensity;

                // Golden celebration effect
                adaptiveEnvironmentLighting.color = new Color(1.0f, 0.8f, 0.2f);
                adaptiveEnvironmentLighting.intensity = 1.5f;

                yield return new WaitForSeconds(3.0f);

                // Restore original lighting
                adaptiveEnvironmentLighting.color = originalColor;
                adaptiveEnvironmentLighting.intensity = originalIntensity;
            }

            Debug.Log("[L.I.F.E VR] Skill mastery celebration completed");
        }

        /// <summary>
        /// Get current biometric data (simulated - replace with real EEG integration)
        /// </summary>
        private BiometricData GetCurrentBiometrics()
        {
            // Simulate realistic biometric data with domain-specific variations
            float baseStress = 0.4f;
            float baseFocus = 0.6f;

            // Domain-specific adjustments
            switch (activeDomain)
            {
                case CurrentDomain.CorporateTraining:
                    baseStress += Mathf.Sin(Time.time * 0.2f) * 0.2f;
                    baseFocus += Mathf.Cos(Time.time * 0.3f) * 0.15f;
                    break;

                case CurrentDomain.Healthcare:
                    baseStress = Mathf.Max(0.1f, baseStress - 0.1f); // Lower stress for rehabilitation
                    baseFocus += 0.1f; // Higher focus for therapy
                    break;

                case CurrentDomain.Education:
                    baseFocus += Mathf.Sin(Time.time * 0.4f) * 0.2f; // Varying focus during learning
                    break;
            }

            return new BiometricData
            {
                stress_level = Mathf.Clamp01(baseStress),
                focus_level = Mathf.Clamp01(baseFocus),
                alpha_power = Random.Range(0.3f, 0.8f),
                beta_power = Random.Range(0.2f, 0.7f),
                theta_power = Random.Range(0.1f, 0.5f),
                gamma_power = Random.Range(0.1f, 0.4f),
                motor_intent = GetSimulatedMotorIntent(),
                neuroplasticity_index = Random.Range(0.3f, 0.9f),
                timestamp = System.DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss")
            };
        }

        /// <summary>
        /// Get simulated motor intent for healthcare domain
        /// </summary>
        private string GetSimulatedMotorIntent()
        {
            if (activeDomain != CurrentDomain.Healthcare)
            {
                return "rest";
            }

            string[] intents = { "rest", "left_hand", "right_hand", "feet", "tongue" };
            float intentProbability = Random.Range(0f, 1f);

            if (intentProbability < 0.6f)
            {
                return "rest";
            }
            else
            {
                return intents[Random.Range(1, intents.Length)];
            }
        }

        /// <summary>
        /// Public methods for external control
        /// </summary>
        [ContextMenu("Test Corporate Training Mode")]
        public void TestCorporateTrainingMode()
        {
            SwitchDomain(CurrentDomain.CorporateTraining);
            BiometricData testData = new BiometricData
            {
                stress_level = 0.8f,
                focus_level = 0.3f,
                neuroplasticity_index = 0.4f
            };
            ApplyCorporateTrainingAdaptation(testData);
        }

        [ContextMenu("Test Healthcare Mode")]
        public void TestHealthcareMode()
        {
            SwitchDomain(CurrentDomain.Healthcare);
            BiometricData testData = new BiometricData
            {
                stress_level = 0.2f,
                focus_level = 0.8f,
                motor_intent = "right_hand"
            };
            ApplyHealthcareAdaptation(testData);
        }

        [ContextMenu("Test Education Mode")]
        public void TestEducationMode()
        {
            SwitchDomain(CurrentDomain.Education);
            BiometricData testData = new BiometricData
            {
                stress_level = 0.4f,
                focus_level = 0.7f,
                neuroplasticity_index = 0.8f
            };
            ApplyEducationAdaptation(testData);
        }

        void OnDestroy()
        {
            if (adaptationCoroutine != null)
            {
                StopCoroutine(adaptationCoroutine);
            }

            Debug.Log("[L.I.F.E VR] Multi-Domain VR Scene Manager destroyed");
        }

        void OnGUI()
        {
            if (Application.isEditor)
            {
                // Debug GUI for development
                GUILayout.BeginArea(new Rect(10, 10, 350, 300));
                GUILayout.Label("L.I.F.E Platform - Multi-Domain VR", GUI.skin.box);
                GUILayout.Label($"Active Domain: {activeDomain}");
                GUILayout.Label($"Stress Level: {currentStressLevel:F3}");
                GUILayout.Label($"Focus Level: {currentFocusLevel:F3}");
                GUILayout.Label($"Motor Intent: {currentMotorIntent}");
                GUILayout.Label($"Biometric History: {biometricHistory.Count}/30");

                GUILayout.Space(10);
                GUILayout.Label("Domain Difficulties:", EditorStyles.boldLabel);
                foreach (var domain in domainDifficulties)
                {
                    GUILayout.Label($"  {domain.Key}: {domain.Value:F3}");
                }

                GUILayout.EndArea();
            }
        }
    }

    /// <summary>
    /// Mock ScenarioManager for standalone operation
    /// </summary>
    public class MockScenarioManager : MonoBehaviour
    {
        public void AdjustDifficulty(float adjustment)
        {
            Debug.Log($"[Mock ScenarioManager] Difficulty adjusted by {adjustment:F3}");
        }
    }

    /// <summary>
    /// Real ScenarioManager interface (implement as needed)
    /// </summary>
    public class ScenarioManager : MonoBehaviour
    {
        public static ScenarioManager Instance { get; private set; }

        void Awake()
        {
            if (Instance == null)
            {
                Instance = this;
                DontDestroyOnLoad(gameObject);
            }
            else
            {
                Destroy(gameObject);
            }
        }

        public virtual void AdjustDifficulty(float adjustment)
        {
            // Implement difficulty adjustment logic
            Debug.Log($"[ScenarioManager] Difficulty adjusted by {adjustment:F3}");
        }
    }
}