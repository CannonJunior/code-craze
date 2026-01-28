/**
 * API utility for communicating with Code Craze backend.
 *
 * Provides methods for all API endpoints.
 */

const API_BASE = window.location.origin + '/api';

/**
 * Helper function to make API requests.
 *
 * @param {string} endpoint - API endpoint path
 * @param {object} options - Fetch options
 * @returns {Promise} Response data
 */
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;

    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    const config = { ...defaultOptions, ...options };

    try {
        const response = await fetch(url, config);

        if (!response.ok) {
            throw new Error(`API error: ${response.status} ${response.statusText}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
}

/**
 * API methods organized by category.
 */
const API = {
    // ========================================================================
    // Info & Health
    // ========================================================================

    /**
     * Get application information.
     */
    getInfo: async () => {
        return await apiRequest('/info');
    },

    /**
     * Health check.
     */
    health: async () => {
        return await apiRequest('/health', { baseUrl: window.location.origin });
    },

    // ========================================================================
    // Competencies
    // ========================================================================

    /**
     * Get user's competency dashboard.
     */
    getCompetencies: async () => {
        return await apiRequest('/competencies');
    },

    /**
     * Get detailed competency for a specific topic.
     *
     * @param {string} topicId - Topic identifier
     */
    getTopicCompetency: async (topicId) => {
        return await apiRequest(`/competencies/${topicId}`);
    },

    /**
     * Get personalized recommendations.
     */
    getRecommendations: async () => {
        return await apiRequest('/recommendations');
    },

    // ========================================================================
    // Practice Sessions
    // ========================================================================

    /**
     * Start a new practice session.
     *
     * @param {string} mode - Practice mode (balanced, weak_focus, review, competition)
     * @param {Array} topicFilter - Optional topic filter
     * @param {number} difficulty - Optional difficulty level
     */
    startPractice: async (mode = 'balanced', topicFilter = null, difficulty = null) => {
        return await apiRequest('/practice/start', {
            method: 'POST',
            body: JSON.stringify({
                mode,
                topic_filter: topicFilter,
                difficulty,
            }),
        });
    },

    /**
     * Get next question in practice session.
     *
     * @param {string} sessionId - Practice session ID
     * @param {string} mode - Practice mode
     */
    getNextQuestion: async (sessionId, mode = 'balanced') => {
        return await apiRequest(`/practice/next?session_id=${sessionId}&mode=${mode}`);
    },

    /**
     * Submit an answer and get explanation.
     *
     * @param {number} questionId - Question ID
     * @param {number} selectedAnswer - Index of selected answer
     * @param {number} timeSpentMs - Time spent in milliseconds
     * @param {number} hintsUsed - Number of hints used
     */
    submitAnswer: async (questionId, selectedAnswer, timeSpentMs, hintsUsed = 0) => {
        return await apiRequest('/practice/submit', {
            method: 'POST',
            body: JSON.stringify({
                question_id: questionId,
                selected_answer: selectedAnswer,
                time_spent_ms: timeSpentMs,
                hints_used: hintsUsed,
            }),
        });
    },

    // ========================================================================
    // User Preferences
    // ========================================================================

    /**
     * Get user preferences.
     */
    getPreferences: async () => {
        return await apiRequest('/preferences');
    },

    /**
     * Update user preferences.
     *
     * @param {object} preferences - Preference updates
     */
    updatePreferences: async (preferences) => {
        return await apiRequest('/preferences', {
            method: 'PUT',
            body: JSON.stringify(preferences),
        });
    },

    // ========================================================================
    // Progress
    // ========================================================================

    /**
     * Get user's learning progress.
     */
    getProgress: async () => {
        return await apiRequest('/progress');
    },

    // ========================================================================
    // Authentication (placeholder)
    // ========================================================================

    /**
     * Get current user.
     */
    getCurrentUser: async () => {
        return await apiRequest('/users/me');
    },
};

// Make API available globally
window.CodeCrazeAPI = API;
