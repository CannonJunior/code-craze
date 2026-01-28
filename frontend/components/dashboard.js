/**
 * Dashboard component for competency visualization.
 */

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', async () => {
    await loadDashboard();
});

/**
 * Load and display competency dashboard.
 */
async function loadDashboard() {
    try {
        // Get competencies from API
        const data = await CodeCrazeAPI.getCompetencies();

        // Update readiness score
        updateReadinessScore(data.competition_readiness || 0);

        // Update competency cards
        if (data.competencies && data.competencies.length > 0) {
            displayCompetencies(data.competencies);
        }

        // Update recommendations
        if (data.recommendations && data.recommendations.length > 0) {
            displayRecommendations(data.recommendations);
        }
    } catch (error) {
        console.error('Failed to load dashboard:', error);
    }
}

/**
 * Update competition readiness score display.
 *
 * @param {number} score - Readiness score (0-100)
 */
function updateReadinessScore(score) {
    const scoreElement = document.querySelector('.readiness-value');
    if (scoreElement) {
        scoreElement.textContent = `${score}%`;

        // Color code based on readiness
        if (score >= 80) {
            scoreElement.style.color = 'var(--success-green)';
        } else if (score >= 60) {
            scoreElement.style.color = 'var(--secondary-purple)';
        } else {
            scoreElement.style.color = 'var(--warning-red)';
        }
    }
}

/**
 * Display competency cards.
 *
 * @param {Array} competencies - Array of competency objects
 */
function displayCompetencies(competencies) {
    const grid = document.querySelector('.competency-grid');
    if (!grid) return;

    // Clear existing cards
    grid.innerHTML = '';

    // Create card for each competency
    competencies.forEach(comp => {
        const card = createCompetencyCard(comp);
        grid.appendChild(card);
    });
}

/**
 * Create a competency card element.
 *
 * @param {object} comp - Competency data
 * @returns {HTMLElement} Card element
 */
function createCompetencyCard(comp) {
    const card = document.createElement('div');
    card.className = 'competency-card';

    const accuracy = (comp.accuracy * 100).toFixed(0);
    const masteryPercent = getMasteryPercent(comp.mastery_level);

    card.innerHTML = `
        <h4>${comp.topic_name}</h4>
        <div class="mastery-bar">
            <div class="mastery-fill" style="width: ${masteryPercent}%"></div>
        </div>
        <div class="competency-stats">
            <span>Accuracy: ${accuracy}%</span>
            <span class="trend">${getTrendIcon(comp.trend)}</span>
        </div>
    `;

    return card;
}

/**
 * Get mastery level as percentage.
 *
 * @param {string} level - Mastery level
 * @returns {number} Percentage
 */
function getMasteryPercent(level) {
    const levels = {
        'novice': 20,
        'developing': 40,
        'proficient': 60,
        'expert': 80,
        'master': 100
    };
    return levels[level] || 0;
}

/**
 * Get trend icon.
 *
 * @param {string} trend - Trend (improving, stable, declining)
 * @returns {string} Icon
 */
function getTrendIcon(trend) {
    const icons = {
        'improving': '↗',
        'stable': '→',
        'declining': '↘'
    };
    return icons[trend] || '→';
}

/**
 * Display recommendations.
 *
 * @param {Array} recommendations - Array of recommendation strings
 */
function displayRecommendations(recommendations) {
    const list = document.getElementById('recommendations-list');
    if (!list) return;

    list.innerHTML = '';

    recommendations.forEach(rec => {
        const li = document.createElement('li');
        li.textContent = rec;
        list.appendChild(li);
    });
}

// Export functions for use in other scripts
window.DashboardComponent = {
    loadDashboard,
    updateReadinessScore,
    displayCompetencies,
    displayRecommendations
};
