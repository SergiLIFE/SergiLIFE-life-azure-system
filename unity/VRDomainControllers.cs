/*
L.I.F.E Platform - Domain-Specific Unity VR Controllers
Enhanced Unity VR implementations for Corporate, Healthcare, and Education domains

This Unity C# script provides specialized VR environment controllers for:
1. Corporate: Crisis Management Training (VR + EEG)
2. Healthcare: Stroke Rehabilitation (VR + Neuroplasticity) 
3. Education: Adaptive Learning (Real-Time, VR, EEG)

Copyright 2025 - Sergio Paya Benaully
*/

using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using Newtonsoft.Json;

namespace LIFEPlatform.DomainControllers
{
    // Corporate Domain: Crisis Management VR Controller
    [System.Serializable]
    public class CorporateVRSceneManager : MonoBehaviour
    {
        [Header("Corporate Crisis Management Settings")]
        public float stressThreshold = 0.7f;
        public float focusThreshold = 0.3f;
        public float difficultyAdjustmentRate = 0.2f;

        [Header("Scene Environment Controls")]
        public Light ambientLight;
        public GameObject[] stressIndicators;
        public GameObject[] focusEnhancers;
        public AudioSource backgroundAudio;

        [Header("Crisis Scenario Manager")]
        public CrisisScenarioManager scenarioManager;

        private float currentStressLevel = 0.5f;
        private float currentFocusLevel = 0.5f;
        private float crisisReadiness = 0.5f;

        void Start()
        {
            Debug.Log("🏢 Corporate Crisis Management VR Controller Initialized");
            InitializeCorporateEnvironment();
        }

        void InitializeCorporateEnvironment()
        {
            // Setup corporate boardroom/crisis center environment
            if (ambientLight == null)
                ambientLight = RenderSettings.sun;

            if (scenarioManager == null)
                scenarioManager = FindObjectOfType<CrisisScenarioManager>();

            // Set initial professional environment
            RenderSettings.ambientLight = Color.white;
            RenderSettings.fog = false;
        }

        public void UpdateSceneDifficulty(float stressLevel, float focusLevel, float decisionPressure)
        {
            currentStressLevel = stressLevel;
            currentFocusLevel = focusLevel;
            crisisReadiness = (focusLevel * 0.7f + (1 - stressLevel) * 0.3f);

            Debug.Log($"📊 Corporate Metrics - Stress: {stressLevel:F2}, Focus: {focusLevel:F2}, Crisis Readiness: {crisisReadiness:F2}");

            // High stress - reduce difficulty and add calming elements
            if (stressLevel > stressThreshold)
            {
                if (scenarioManager != null)
                    scenarioManager.AdjustDifficulty(-difficultyAdjustmentRate);

                // Calming green ambient lighting
                RenderSettings.ambientLight = Color.Lerp(Color.green, Color.red, stressLevel);

                // Activate stress reduction protocols
                ActivateStressReduction();

                // Reduce background noise/pressure
                if (backgroundAudio != null)
                    backgroundAudio.volume = Mathf.Lerp(0.8f, 0.3f, stressLevel);
            }
            // Low stress and high focus - increase challenge
            else if (stressLevel < focusThreshold && focusLevel > 0.6f)
            {
                if (scenarioManager != null)
                    scenarioManager.AdjustDifficulty(0.15f);

                // Energizing blue ambient lighting
                RenderSettings.ambientLight = Color.Lerp(Color.blue, Color.white, focusLevel);

                // Activate focus enhancement
                ActivateFocusEnhancement();

                // Increase scenario complexity
                if (backgroundAudio != null)
                    backgroundAudio.volume = 0.6f;
            }

            AdaptCrisisScenario();
        }

        void ActivateStressReduction()
        {
            // Show calming visual elements
            foreach (GameObject indicator in stressIndicators)
            {
                if (indicator != null)
                    indicator.SetActive(false);
            }

            // Activate breathing guide, reduce UI complexity
            StartCoroutine(ShowBreathingGuide());
        }

        void ActivateFocusEnhancement()
        {
            // Show focus enhancement elements
            foreach (GameObject enhancer in focusEnhancers)
            {
                if (enhancer != null)
                    enhancer.SetActive(true);
            }
        }

        void AdaptCrisisScenario()
        {
            if (scenarioManager != null)
            {
                if (crisisReadiness > 0.8f)
                {
                    scenarioManager.SetComplexity("expert_level");
                }
                else if (crisisReadiness < 0.4f)
                {
                    scenarioManager.SetComplexity("training_wheels");
                }
                else
                {
                    scenarioManager.SetComplexity("standard");
                }
            }
        }

        IEnumerator ShowBreathingGuide()
        {
            // Show breathing assistance for 30 seconds during high stress
            yield return new WaitForSeconds(30f);
        }
    }

    // Healthcare Domain: Rehabilitation VR Controller
    [System.Serializable]
    public class HealthcareRehabTaskManager : MonoBehaviour
    {
        [Header("Rehabilitation Settings")]
        public float successThreshold = 0.8f;
        public float difficultyThreshold = 0.4f;

        [Header("Rehabilitation Objects")]
        public GameObject targetObject;
        public GameObject[] obstacles;
        public Transform[] spawnPoints;

        [Header("Motor Intent Feedback")]
        public ParticleSystem successParticles;
        public AudioSource encouragementAudio;
        public AudioClip[] encouragementClips;

        [Header("Assistance Systems")]
        public LineRenderer guidanceLine;
        public GameObject[] assistanceObjects;

        private float currentSuccessRate = 0.5f;
        private bool motorIntentDetected = false;
        private float motorReadiness = 0.5f;

        void Start()
        {
            Debug.Log("🏥 Healthcare Rehabilitation VR Controller Initialized");
            InitializeRehabEnvironment();
        }

        void InitializeRehabEnvironment()
        {
            // Setup rehabilitation room environment
            RenderSettings.ambientLight = Color.white;

            if (targetObject == null)
                targetObject = GameObject.CreatePrimitive(PrimitiveType.Sphere);

            // Set initial moderate difficulty
            SetTargetSpeed(1.0f);
            SetObstacleCount(1);
        }

        public void AdjustTask(float successRate, bool intentDetected, float motorConfidence)
        {
            currentSuccessRate = successRate;
            motorIntentDetected = intentDetected;
            motorReadiness = motorConfidence;

            Debug.Log($"🧠 Rehabilitation Metrics - Success: {successRate:F2}, Intent: {intentDetected}, Motor Readiness: {motorConfidence:F2}");

            // High success rate - increase difficulty
            if (successRate > successThreshold)
            {
                // Increase target speed
                SetTargetSpeed(1.25f);

                // Add obstacles
                SetObstacleCount(2);

                // Reduce assistance
                SetAssistanceLevel("reduced");

                // Play achievement sound
                PlayEncouragement("challenge");

                Debug.Log("📈 Increasing rehabilitation difficulty");
            }
            // Low success rate - simplify task
            else if (successRate < difficultyThreshold)
            {
                // Decrease target speed
                SetTargetSpeed(0.75f);

                // Remove obstacles
                SetObstacleCount(0);

                // Increase assistance
                SetAssistanceLevel("high");

                // Play supportive sound
                PlayEncouragement("supportive");

                Debug.Log("📉 Simplifying rehabilitation task");
            }

            // Adjust based on motor intent detection
            AdaptToMotorIntent();
        }

        void SetTargetSpeed(float speed)
        {
            if (targetObject != null)
            {
                Rigidbody rb = targetObject.GetComponent<Rigidbody>();
                if (rb == null)
                    rb = targetObject.AddComponent<Rigidbody>();

                // Apply speed to movement script or animation
                TargetMover mover = targetObject.GetComponent<TargetMover>();
                if (mover != null)
                    mover.speed = speed;
            }
        }

        void SetObstacleCount(int count)
        {
            // Disable all obstacles first
            foreach (GameObject obstacle in obstacles)
            {
                if (obstacle != null)
                    obstacle.SetActive(false);
            }

            // Enable required number of obstacles
            for (int i = 0; i < count && i < obstacles.Length; i++)
            {
                if (obstacles[i] != null)
                    obstacles[i].SetActive(true);
            }
        }

        void SetAssistanceLevel(string level)
        {
            switch (level.ToLower())
            {
                case "high":
                case "maximum":
                    ShowAllAssistance();
                    break;
                case "reduced":
                case "minimal":
                    ShowMinimalAssistance();
                    break;
                default:
                    ShowStandardAssistance();
                    break;
            }
        }

        void ShowAllAssistance()
        {
            // Show guidance line
            if (guidanceLine != null)
                guidanceLine.enabled = true;

            // Activate all assistance objects
            foreach (GameObject assist in assistanceObjects)
            {
                if (assist != null)
                    assist.SetActive(true);
            }
        }

        void ShowMinimalAssistance()
        {
            // Hide guidance line
            if (guidanceLine != null)
                guidanceLine.enabled = false;

            // Deactivate most assistance objects
            for (int i = 0; i < assistanceObjects.Length; i++)
            {
                if (assistanceObjects[i] != null)
                    assistanceObjects[i].SetActive(i == 0); // Keep only first one
            }
        }

        void ShowStandardAssistance()
        {
            // Show moderate assistance
            if (guidanceLine != null)
                guidanceLine.enabled = true;

            // Show half the assistance objects
            for (int i = 0; i < assistanceObjects.Length; i++)
            {
                if (assistanceObjects[i] != null)
                    assistanceObjects[i].SetActive(i % 2 == 0);
            }
        }

        void AdaptToMotorIntent()
        {
            if (motorIntentDetected && motorReadiness > 0.8f)
            {
                // High motor readiness - expert level tasks
                SetAssistanceLevel("minimal");
                PlayEncouragement("achievement");

                // Show success particles
                if (successParticles != null)
                    successParticles.Play();
            }
            else if (!motorIntentDetected || motorReadiness < 0.3f)
            {
                // Low motor readiness - maximum assistance
                SetAssistanceLevel("maximum");
                PlayEncouragement("motivation");
            }
        }

        void PlayEncouragement(string type)
        {
            if (encouragementAudio != null && encouragementClips.Length > 0)
            {
                AudioClip clipToPlay = encouragementClips[0]; // Default

                // Select appropriate encouragement clip based on type
                // This would be expanded with specific clips for each type
                encouragementAudio.clip = clipToPlay;
                encouragementAudio.Play();
            }
        }

        public void RemoveObstacles(int count)
        {
            int activeCount = 0;
            foreach (GameObject obstacle in obstacles)
            {
                if (obstacle != null && obstacle.activeSelf)
                {
                    if (activeCount < count)
                    {
                        obstacle.SetActive(false);
                        activeCount++;
                    }
                }
            }
        }
    }

    // Education Domain: Adaptive Learning VR Controller
    [System.Serializable]
    public class VRAcademicController : MonoBehaviour
    {
        [Header("Educational Settings")]
        public float focusThreshold = 0.8f;
        public float stressThreshold = 0.5f;
        public float difficultyAdjustmentRate = 0.15f;

        [Header("Learning Environment")]
        public GameObject[] lessonObjects;
        public GameObject calmingScene;
        public ParticleSystem focusParticles;
        public AudioSource ambientAudio;

        [Header("Adaptive UI Elements")]
        public Canvas mainUI;
        public GameObject[] complexityIndicators;
        public GameObject breakSuggestionUI;

        private float currentFocus = 0.5f;
        private float currentStress = 0.3f;
        private float attentionScore = 0.5f;
        private float learningReadiness = 0.5f;

        void Start()
        {
            Debug.Log("🎓 Educational Adaptive Learning VR Controller Initialized");
            InitializeEducationalEnvironment();
        }

        void InitializeEducationalEnvironment()
        {
            // Setup educational classroom/lab environment
            RenderSettings.ambientLight = Color.white;
            RenderSettings.fog = false;

            // Initialize UI elements
            if (breakSuggestionUI != null)
                breakSuggestionUI.SetActive(false);
        }

        public void AdjustLesson(float focus, float stress, float attentionLevel, float cognitiveLoad)
        {
            currentFocus = focus;
            currentStress = stress;
            attentionScore = attentionLevel;
            learningReadiness = attentionLevel * (1 - Mathf.Min(cognitiveLoad, 0.7f));

            Debug.Log($"📚 Educational Metrics - Focus: {focus:F2}, Stress: {stress:F2}, Attention: {attentionLevel:F2}, Learning Readiness: {learningReadiness:F2}");

            // High focus and low cognitive load - increase challenge
            if (focus > focusThreshold && cognitiveLoad < 0.6f)
            {
                IncreaseTaskDifficulty(difficultyAdjustmentRate);
                SetEnvironment("challenging");
                SetInteractionMode("advanced");
                SetFeedbackFrequency("reduced");

                Debug.Log("📈 Increasing lesson difficulty - student is focused");
            }
            // Low focus - simplify and engage
            else if (attentionLevel < 0.5f)
            {
                DecreaseTaskDifficulty(0.1f);
                SetEnvironment("engaging");
                SetInteractionMode("guided");
                SetFeedbackFrequency("high");

                Debug.Log("📉 Simplifying lesson - improving engagement");
            }

            // High stress - activate calming protocols
            if (stress > stressThreshold)
            {
                ActivateCalmScene();
                SuggestBreak();

                Debug.Log("😌 Activating calming protocols - high stress detected");
            }

            AdaptToLearningReadiness();
        }

        void IncreaseTaskDifficulty(float percentage)
        {
            // Increase complexity of learning objects
            for (int i = 0; i < lessonObjects.Length; i++)
            {
                if (lessonObjects[i] != null)
                {
                    LessonComplexity complexity = lessonObjects[i].GetComponent<LessonComplexity>();
                    if (complexity != null)
                        complexity.IncreaseDifficulty(percentage);
                }
            }

            // Show complexity indicators
            ShowComplexityIndicators(Mathf.CeilToInt(percentage * 10));
        }

        void DecreaseTaskDifficulty(float percentage)
        {
            // Decrease complexity of learning objects
            for (int i = 0; i < lessonObjects.Length; i++)
            {
                if (lessonObjects[i] != null)
                {
                    LessonComplexity complexity = lessonObjects[i].GetComponent<LessonComplexity>();
                    if (complexity != null)
                        complexity.DecreaseDifficulty(percentage);
                }
            }

            // Reduce complexity indicators
            ShowComplexityIndicators(Mathf.FloorToInt((1 - percentage) * 10));
        }

        void ActivateCalmScene()
        {
            if (calmingScene != null)
            {
                calmingScene.SetActive(true);

                // Fade in calming environment over 2 seconds
                StartCoroutine(FadeToCalmingScene());
            }

            // Reduce ambient audio volume
            if (ambientAudio != null)
                ambientAudio.volume = 0.3f;
        }

        void SuggestBreak()
        {
            if (breakSuggestionUI != null)
            {
                breakSuggestionUI.SetActive(true);

                // Auto-hide after 10 seconds
                StartCoroutine(HideBreakSuggestion());
            }
        }

        void SetEnvironment(string environmentType)
        {
            switch (environmentType.ToLower())
            {
                case "challenging":
                    RenderSettings.ambientLight = Color.blue * 1.2f;
                    if (focusParticles != null)
                        focusParticles.Play();
                    break;

                case "engaging":
                    RenderSettings.ambientLight = Color.yellow * 1.1f;
                    SetLessonVisualization("interactive");
                    break;

                case "peaceful":
                    RenderSettings.ambientLight = Color.green * 0.8f;
                    ActivateCalmScene();
                    break;

                default:
                    RenderSettings.ambientLight = Color.white;
                    break;
            }
        }

        void SetInteractionMode(string mode)
        {
            switch (mode.ToLower())
            {
                case "advanced":
                    // Enable advanced interaction tools
                    EnableAdvancedTools();
                    break;

                case "guided":
                    // Show step-by-step guidance
                    EnableGuidedMode();
                    break;

                case "exploratory":
                    // Enable free exploration
                    EnableExploratoryMode();
                    break;

                case "supportive":
                    // Maximum assistance mode
                    EnableSupportiveMode();
                    break;
            }
        }

        void SetFeedbackFrequency(string frequency)
        {
            float feedbackRate;
            switch (frequency.ToLower())
            {
                case "high":
                    feedbackRate = 0.5f; // Every 0.5 seconds
                    break;
                case "reduced":
                    feedbackRate = 3.0f; // Every 3 seconds
                    break;
                default:
                    feedbackRate = 1.5f; // Every 1.5 seconds
                    break;
            }

            // Apply feedback rate to lesson system
            StartCoroutine(ProvideFeedback(feedbackRate));
        }

        void AdaptToLearningReadiness()
        {
            if (learningReadiness > 0.8f)
            {
                SetInteractionMode("exploratory");
                Debug.Log("🚀 High learning readiness - enabling exploration mode");
            }
            else if (learningReadiness < 0.3f)
            {
                SetInteractionMode("supportive");
                Debug.Log("🤝 Low learning readiness - enabling support mode");
            }
        }

        void ShowComplexityIndicators(int level)
        {
            for (int i = 0; i < complexityIndicators.Length; i++)
            {
                if (complexityIndicators[i] != null)
                    complexityIndicators[i].SetActive(i < level);
            }
        }

        void SetLessonVisualization(string type)
        {
            // Implement different visualization modes for lessons
            foreach (GameObject lesson in lessonObjects)
            {
                if (lesson != null)
                {
                    LessonVisualizer visualizer = lesson.GetComponent<LessonVisualizer>();
                    if (visualizer != null)
                        visualizer.SetVisualizationType(type);
                }
            }
        }

        void EnableAdvancedTools()
        {
            // Enable advanced learning tools and interfaces
        }

        void EnableGuidedMode()
        {
            // Show step-by-step guidance and hints
        }

        void EnableExploratoryMode()
        {
            // Enable free exploration and discovery learning
        }

        void EnableSupportiveMode()
        {
            // Maximum assistance and scaffolding
        }

        IEnumerator FadeToCalmingScene()
        {
            float fadeTime = 2.0f;
            float elapsed = 0f;

            while (elapsed < fadeTime)
            {
                elapsed += Time.deltaTime;
                float alpha = elapsed / fadeTime;

                // Implement fade logic here
                yield return null;
            }
        }

        IEnumerator HideBreakSuggestion()
        {
            yield return new WaitForSeconds(10f);
            if (breakSuggestionUI != null)
                breakSuggestionUI.SetActive(false);
        }

        IEnumerator ProvideFeedback(float interval)
        {
            while (true)
            {
                yield return new WaitForSeconds(interval);

                // Provide appropriate feedback based on current state
                ProvideLearningFeedback();
            }
        }

        void ProvideLearningFeedback()
        {
            // Implement learning feedback logic
            if (currentFocus > 0.7f)
            {
                // Positive reinforcement
                ShowPositiveFeedback();
            }
            else if (currentFocus < 0.4f)
            {
                // Encouraging feedback
                ShowEncouragingFeedback();
            }
        }

        void ShowPositiveFeedback()
        {
            // Show positive visual/audio feedback
            if (focusParticles != null)
                focusParticles.Play();
        }

        void ShowEncouragingFeedback()
        {
            // Show encouraging feedback to improve focus
        }
    }

    // Supporting Classes

    public class CrisisScenarioManager : MonoBehaviour
    {
        public float currentDifficulty = 0.5f;
        public string currentComplexity = "standard";

        public void AdjustDifficulty(float adjustment)
        {
            currentDifficulty = Mathf.Clamp01(currentDifficulty + adjustment);
            Debug.Log($"Crisis scenario difficulty adjusted to: {currentDifficulty:F2}");
        }

        public void SetComplexity(string complexity)
        {
            currentComplexity = complexity;
            Debug.Log($"Crisis scenario complexity set to: {complexity}");

            // Implement complexity adjustments based on type
            switch (complexity.ToLower())
            {
                case "expert_level":
                    // Highest complexity scenarios
                    break;
                case "training_wheels":
                    // Simplified, guided scenarios
                    break;
                default:
                    // Standard complexity
                    break;
            }
        }
    }

    public class TargetMover : MonoBehaviour
    {
        public float speed = 1.0f;

        void Update()
        {
            // Simple movement implementation
            transform.Translate(Vector3.forward * speed * Time.deltaTime);
        }
    }

    public class LessonComplexity : MonoBehaviour
    {
        public float currentComplexity = 0.5f;

        public void IncreaseDifficulty(float percentage)
        {
            currentComplexity = Mathf.Clamp01(currentComplexity + percentage);
            ApplyComplexityChanges();
        }

        public void DecreaseDifficulty(float percentage)
        {
            currentComplexity = Mathf.Clamp01(currentComplexity - percentage);
            ApplyComplexityChanges();
        }

        void ApplyComplexityChanges()
        {
            // Implement visual/interactive complexity changes
            transform.localScale = Vector3.one * (0.8f + currentComplexity * 0.4f);
        }
    }

    public class LessonVisualizer : MonoBehaviour
    {
        public void SetVisualizationType(string type)
        {
            // Implement different lesson visualization modes
            switch (type.ToLower())
            {
                case "interactive":
                    // Enable interactive elements
                    break;
                case "visual":
                    // Emphasize visual components
                    break;
                case "hands_on":
                    // Enable hands-on manipulation
                    break;
                default:
                    // Standard visualization
                    break;
            }
        }
    }
}