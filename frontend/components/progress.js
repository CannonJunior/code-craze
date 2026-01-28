/**
 * Progress component for tracking learning journey.
 */

// Load progress when progress view is activated
document.getElementById('nav-progress')?.addEventListener('click', async () => {
    await loadProgress();
});

/**
 * Load and display progress data.
 */
async function loadProgress() {
    try {
        const data = await CodeCrazeAPI.getProgress();

        // Update stats
        updateProgressStats(data);

        // Display levels
        if (data.levels && data.levels.length > 0) {
            displayLevels(data.levels);
        }
    } catch (error) {
        console.error('Failed to load progress:', error);
    }
}

/**
 * Update progress statistics.
 *
 * @param {object} data - Progress data
 */
function updateProgressStats(data) {
    // Total points
    const pointsElement = document.querySelector('.progress-overview .stat-card:nth-child(1) .stat-value');
    if (pointsElement) {
        pointsElement.textContent = `${data.total_points || 0} VP`;
    }

    // Badges earned
    const badgesElement = document.querySelector('.progress-overview .stat-card:nth-child(2) .stat-value');
    if (badgesElement) {
        badgesElement.textContent = `${data.badges_earned || 0} / 30`;
    }

    // Current level
    const levelElement = document.querySelector('.progress-overview .stat-card:nth-child(3) .stat-value');
    if (levelElement) {
        levelElement.textContent = `Level ${data.current_level || 0}`;
    }
}

/**
 * Display learning levels.
 *
 * @param {Array} levels - Array of level progress objects
 */
function displayLevels(levels) {
    const container = document.querySelector('.levels-container');
    if (!container) return;

    container.innerHTML = '<h3>Learning Levels</h3>';

    // Level names for Code Craze
    const levelNames = [
        'Level 0: Getting Started',
        'Level 1: Karel Basics',
        'Level 2: Functions & Control',
        'Level 3: AI Fundamentals',
        'Level 4: Machine Learning',
        'Level 5: Cryptography Basics',
        'Level 6: Encryption Methods',
        'Level 7: Python Fundamentals',
        'Level 8: Python Advanced',
        'Level 9: Quantum Computing',
        'Level 10: Competition Ready'
    ];

    levels.forEach((level, index) => {
        const levelCard = createLevelCard(level, levelNames[level.level] || `Level ${level.level}`);
        container.appendChild(levelCard);
    });
}

/**
 * Create a level progress card.
 *
 * @param {object} level - Level progress data
 * @param {string} name - Level name
 * @returns {HTMLElement} Card element
 */
function createLevelCard(level, name) {
    const card = document.createElement('div');
    card.className = 'level-card';
    card.style.cssText = 'margin-bottom: 1rem; padding: 1rem; background-color: var(--light-gray); border-radius: 8px;';

    const statusIcon = getStatusIcon(level.status);
    const scoreDisplay = level.score !== null ? `${level.score.toFixed(0)}%` : '--';

    card.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h4>${statusIcon} ${name}</h4>
                <p style="color: #666; font-size: 0.9rem;">Status: ${level.status}</p>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 1.5rem; font-weight: bold; color: var(--primary-blue);">
                    ${scoreDisplay}
                </div>
                <div style="font-size: 0.8rem; color: #666;">
                    ${level.status === 'completed' ? 'Completed' : 'Not completed'}
                </div>
            </div>
        </div>
    `;

    return card;
}

/**
 * Get status icon.
 *
 * @param {string} status - Level status
 * @returns {string} Icon
 */
function getStatusIcon(status) {
    const icons = {
        'locked': '🔒',
        'in_progress': '📝',
        'completed': '✅'
    };
    return icons[status] || '❓';
}

// Export functions
window.ProgressComponent = {
    loadProgress,
    updateProgressStats,
    displayLevels
};
