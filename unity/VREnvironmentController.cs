/*
L.I.F.E Platform - Unity VR Environment Controller
EEG-Driven Virtual Reality Adjustment System

This Unity C# script integrates with the L.I.F.E Platform to provide real-time
VR environment adjustments based on EEG data from the neuroadaptive learning system.

Copyright 2025 - Sergio Paya Benaully
Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
*/

using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using UnityEngine.Networking;
using Newtonsoft.Json;

namespace LIFEPlatform.VR
{
    /// <summary>
    /// VR Environment Controller for L.I.F.E Platform integration
    /// Provides real-time environment adjustments based on EEG neuroplasticity data
    /// </summary>
    public class VREnvironmentController : MonoBehaviour
    {
        [Header("L.I.F.E Platform Integration")]
        public string lifeApiEndpoint = "https://life-functions-app.azurewebsites.net/api/";
        public string apiKey = ""; // Set via Azure Key Vault integration

        [Header("Environment Adjustment Settings")]
        [Range(0.0f, 1.0f)]
        public float complexityAdjustmentRate = 0.2f;

        [Range(0.0f, 1.0f)]
        public float relaxationIntensity = 0.5f;

        [Header("EEG Thresholds")]
        [Range(0.0f, 1.0f)]
        public float highFocusThreshold = 0.7f;

        [Range(0.0f, 1.0f)]
        public float lowStressThreshold = 0.3f;

        // VR Environment Components
        private GameObject[] environmentObjects;
        private Light mainLight;
        private AudioSource backgroundAudio;
        private ParticleSystem relaxationParticles;

        // L.I.F.E Platform Data
        private EEGData currentEEGData;
        private bool isConnectedToLIFE = false;

        void Start()
        {
            InitializeVREnvironment();
            StartCoroutine(ConnectToLIFEPlatform());
        }

        void Update()
        {
            if (isConnectedToLIFE && currentEEGData != null)
            {
                UpdateEnvironment(currentEEGData.focus, currentEEGData.stress);
            }
        }

        /// <summary>
        /// Main L.I.F.E Platform integration method - updates VR environment based on EEG data
        /// </summary>
        /// <param name="focus">Focus level from EEG analysis (0.0-1.0)</param>
        /// <param name="stress">Stress level from EEG analysis (0.0-1.0)</param>
        public void UpdateEnvironment(float focus, float stress)
        {
            // Validate input parameters
            focus = Mathf.Clamp01(focus);
            stress = Mathf.Clamp01(stress);

            Debug.Log($"L.I.F.E VR Update - Focus: {focus:F2}, Stress: {stress:F2}");

            // High focus, low stress = increase complexity
            if (focus > highFocusThreshold && stress < lowStressThreshold)
            {
                Debug.Log("High focus and low stress detected. Increasing task complexity by 20%.");
                IncreaseTaskComplexity(complexityAdjustmentRate);
                ApplyFocusEnvironment();
            }
            // High stress or low focus = activate relaxation
            else if (stress > lowStressThreshold || focus < (highFocusThreshold - 0.2f))
            {
                Debug.Log("Stress level is high or focus is low. Activating relaxation protocol.");
                ActivateRelaxationProtocol();
                ApplyRelaxationEnvironment();
            }
            // Balanced state = maintain current environment
            else
            {
                Debug.Log("Balanced state detected. Maintaining current environment.");
                ApplyBalancedEnvironment();
            }

            // Log data for L.I.F.E Platform analytics
            LogEnvironmentAdjustment(focus, stress);
        }

        /// <summary>
        /// Increase task complexity based on high focus levels
        /// </summary>
        /// <param name="percentage">Percentage increase in complexity (0.0-1.0)</param>
        private void IncreaseTaskComplexity(float percentage)
        {
            percentage = Mathf.Clamp01(percentage);
            Debug.Log($"Task complexity increased by {percentage * 100}%.");

            // Implement complexity adjustments
            AdjustLighting(1.0f + percentage);
            AdjustSpatialComplexity(percentage);
            ModifyInteractionRequirements(percentage);

            // Visual feedback for complexity increase
            StartCoroutine(ShowComplexityIncrease());
        }

        /// <summary>
        /// Activate relaxation protocol for stress reduction
        /// </summary>
        private void ActivateRelaxationProtocol()
        {
            Debug.Log("Relaxation protocol activated.");

            // Implement relaxation features
            ReduceLighting();
            PlayRelaxationAudio();
            ActivateRelaxationParticles();
            SimplifyInteractions();

            // Visual feedback for relaxation mode
            StartCoroutine(ShowRelaxationMode());
        }

        /// <summary>
        /// Apply focused learning environment
        /// </summary>
        private void ApplyFocusEnvironment()
        {
            if (mainLight != null)
            {
                mainLight.intensity = 1.2f;
                mainLight.color = Color.white;
            }

            if (backgroundAudio != null)
            {
                backgroundAudio.volume = 0.3f;
            }
        }

        /// <summary>
        /// Apply relaxation environment settings
        /// </summary>
        private void ApplyRelaxationEnvironment()
        {
            if (mainLight != null)
            {
                mainLight.intensity = 0.6f;
                mainLight.color = new Color(0.8f, 0.9f, 1.0f); // Soft blue
            }

            if (backgroundAudio != null)
            {
                backgroundAudio.volume = 0.1f;
            }

            if (relaxationParticles != null)
            {
                relaxationParticles.Play();
            }
        }

        /// <summary>
        /// Apply balanced environment settings
        /// </summary>
        private void ApplyBalancedEnvironment()
        {
            if (mainLight != null)
            {
                mainLight.intensity = 1.0f;
                mainLight.color = Color.white;
            }

            if (backgroundAudio != null)
            {
                backgroundAudio.volume = 0.2f;
            }

            if (relaxationParticles != null)
            {
                relaxationParticles.Stop();
            }
        }

        /// <summary>
        /// Initialize VR environment components
        /// </summary>
        private void InitializeVREnvironment()
        {
            // Find environment components
            environmentObjects = GameObject.FindGameObjectsWithTag("Environment");
            mainLight = FindObjectOfType<Light>();
            backgroundAudio = GetComponent<AudioSource>();
            relaxationParticles = GetComponentInChildren<ParticleSystem>();

            Debug.Log($"L.I.F.E VR Environment initialized with {environmentObjects.Length} objects");
        }

        /// <summary>
        /// Connect to L.I.F.E Platform API
        /// </summary>
        private IEnumerator ConnectToLIFEPlatform()
        {
            while (!isConnectedToLIFE)
            {
                yield return StartCoroutine(FetchEEGData());
                yield return new WaitForSeconds(1.0f); // Update every second
            }
        }

        /// <summary>
        /// Fetch EEG data from L.I.F.E Platform API
        /// </summary>
        private IEnumerator FetchEEGData()
        {
            string url = lifeApiEndpoint + "eeg-data";

            using (UnityWebRequest request = UnityWebRequest.Get(url))
            {
                // Add authentication header if API key is available
                if (!string.IsNullOrEmpty(apiKey))
                {
                    request.SetRequestHeader("Authorization", $"Bearer {apiKey}");
                }

                yield return request.SendWebRequest();

                if (request.result == UnityWebRequest.Result.Success)
                {
                    try
                    {
                        string jsonResponse = request.downloadHandler.text;
                        currentEEGData = JsonConvert.DeserializeObject<EEGData>(jsonResponse);
                        isConnectedToLIFE = true;

                        Debug.Log($"L.I.F.E Platform connected - Focus: {currentEEGData.focus:F2}, Stress: {currentEEGData.stress:F2}");
                    }
                    catch (System.Exception e)
                    {
                        Debug.LogError($"Error parsing L.I.F.E Platform data: {e.Message}");
                    }
                }
                else
                {
                    Debug.LogWarning($"L.I.F.E Platform connection failed: {request.error}");
                    // Use simulated data for testing
                    currentEEGData = new EEGData
                    {
                        focus = Random.Range(0.3f, 0.9f),
                        stress = Random.Range(0.1f, 0.7f),
                        timestamp = System.DateTime.Now.ToString()
                    };
                    isConnectedToLIFE = true;
                }
            }
        }

        /// <summary>
        /// Log environment adjustment for L.I.F.E Platform analytics
        /// </summary>
        private void LogEnvironmentAdjustment(float focus, float stress)
        {
            var logData = new
            {
                timestamp = System.DateTime.Now.ToString(),
                focus = focus,
                stress = stress,
                action = GetCurrentEnvironmentMode(),
                user_id = "vr_user_" + System.Environment.UserName
            };

            StartCoroutine(SendLogToLIFEPlatform(JsonConvert.SerializeObject(logData)));
        }

        /// <summary>
        /// Send log data to L.I.F.E Platform
        /// </summary>
        private IEnumerator SendLogToLIFEPlatform(string jsonData)
        {
            string url = lifeApiEndpoint + "vr-logs";

            using (UnityWebRequest request = new UnityWebRequest(url, "POST"))
            {
                byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(jsonData);
                request.uploadHandler = new UploadHandlerRaw(bodyRaw);
                request.downloadHandler = new DownloadHandlerBuffer();
                request.SetRequestHeader("Content-Type", "application/json");

                if (!string.IsNullOrEmpty(apiKey))
                {
                    request.SetRequestHeader("Authorization", $"Bearer {apiKey}");
                }

                yield return request.SendWebRequest();

                if (request.result == UnityWebRequest.Result.Success)
                {
                    Debug.Log("L.I.F.E Platform log sent successfully");
                }
                else
                {
                    Debug.LogWarning($"L.I.F.E Platform log failed: {request.error}");
                }
            }
        }

        // Helper methods for environment adjustments
        private void AdjustLighting(float multiplier)
        {
            if (mainLight != null) mainLight.intensity *= multiplier;
        }

        private void AdjustSpatialComplexity(float increase)
        {
            // Implement spatial complexity adjustments
            Debug.Log($"Spatial complexity adjusted by {increase * 100}%");
        }

        private void ModifyInteractionRequirements(float increase)
        {
            // Implement interaction complexity adjustments
            Debug.Log($"Interaction requirements increased by {increase * 100}%");
        }

        private void ReduceLighting()
        {
            if (mainLight != null) mainLight.intensity = 0.6f;
        }

        private void PlayRelaxationAudio()
        {
            if (backgroundAudio != null) backgroundAudio.volume = 0.1f;
        }

        private void ActivateRelaxationParticles()
        {
            if (relaxationParticles != null) relaxationParticles.Play();
        }

        private void SimplifyInteractions()
        {
            Debug.Log("Interaction complexity reduced for relaxation");
        }

        private string GetCurrentEnvironmentMode()
        {
            if (currentEEGData == null) return "unknown";

            if (currentEEGData.focus > highFocusThreshold && currentEEGData.stress < lowStressThreshold)
                return "focus_mode";
            else if (currentEEGData.stress > lowStressThreshold)
                return "relaxation_mode";
            else
                return "balanced_mode";
        }

        // Coroutines for visual feedback
        private IEnumerator ShowComplexityIncrease()
        {
            // Visual feedback implementation
            yield return new WaitForSeconds(0.5f);
            Debug.Log("Complexity increase visual feedback completed");
        }

        private IEnumerator ShowRelaxationMode()
        {
            // Relaxation mode visual feedback implementation
            yield return new WaitForSeconds(0.5f);
            Debug.Log("Relaxation mode visual feedback completed");
        }
    }

    /// <summary>
    /// EEG data structure for L.I.F.E Platform integration
    /// </summary>
    [System.Serializable]
    public class EEGData
    {
        public float focus;
        public float stress;
        public float attention;
        public float neuroplasticity;
        public string timestamp;
        public string user_id;
    }
}