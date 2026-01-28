/**
 * Practice component for interactive learning.
 */

// Practice session state
let currentSession = null;
let currentQuestion = null;
let selectedAnswer = null;
let startTime = null;
let currentMode = 'balanced';

// Quick action buttons
document.getElementById('start-balanced')?.addEventListener('click', () => startPracticeMode('balanced'));
document.getElementById('start-weak-focus')?.addEventListener('click', () => startPracticeMode('weak_focus'));
document.getElementById('start-review')?.addEventListener('click', () => startPracticeMode('review'));
document.getElementById('start-competition')?.addEventListener('click', () => startPracticeMode('competition'));

/**
 * Start practice session with specified mode.
 *
 * @param {string} mode - Practice mode
 */
async function startPracticeMode(mode) {
    try {
        // Save current mode
        currentMode = mode;

        // Switch to practice view
        document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
        document.getElementById('view-practice').classList.add('active');

        document.querySelectorAll('.nav-button').forEach(b => b.classList.remove('active'));
        document.getElementById('nav-practice').classList.add('active');

        // Start session
        const session = await CodeCrazeAPI.startPractice(mode);
        currentSession = session;

        // Update UI
        updatePracticeModeLabel(mode);

        // Load first question
        if (session.question) {
            displayQuestion(session.question);
        } else {
            showMessage('No questions available yet. Check back later!');
        }
    } catch (error) {
        console.error('Failed to start practice:', error);
        showMessage('Error starting practice session. Please try again.');
    }
}

/**
 * Update practice mode label.
 *
 * @param {string} mode - Practice mode
 */
function updatePracticeModeLabel(mode) {
    const labels = {
        'balanced': '🎯 Balanced Practice',
        'weak_focus': '⚠️ Weak Area Focus',
        'review': '🔄 Review Mode',
        'competition': '🏆 Competition Simulation'
    };

    const label = document.getElementById('practice-mode-label');
    if (label) {
        label.textContent = labels[mode] || 'Practice Mode';
    }
}

/**
 * Display a question.
 *
 * @param {object} question - Question object
 */
function displayQuestion(question) {
    currentQuestion = question;
    selectedAnswer = null;
    startTime = Date.now();

    // Update context
    const context = document.getElementById('practice-context');
    if (context && question.practice_context) {
        context.textContent = question.practice_context;
    }

    // Update question text
    const content = document.getElementById('question-content');
    if (content) {
        content.innerHTML = `<p><strong>Q:</strong> ${question.question_text}</p>`;
    }

    // Display code snippet if present
    const codeSnippet = document.getElementById('code-snippet');
    if (codeSnippet) {
        if (question.code_snippet) {
            codeSnippet.classList.remove('hidden');
            codeSnippet.innerHTML = `<pre><code>${escapeHtml(question.code_snippet)}</code></pre>`;
        } else {
            codeSnippet.classList.add('hidden');
            codeSnippet.innerHTML = '';
        }
    }

    // Display answers
    displayAnswers(question.answers);

    // Reset UI state
    document.getElementById('explanation-container')?.classList.add('hidden');
    document.getElementById('btn-submit')?.classList.remove('hidden');
    document.getElementById('btn-next')?.classList.add('hidden');
}

/**
 * Escape HTML to prevent XSS.
 *
 * @param {string} text - Text to escape
 * @returns {string} Escaped text
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Display answer options.
 *
 * @param {Array} answers - Array of answer objects
 */
function displayAnswers(answers) {
    const container = document.getElementById('answers-container');
    if (!container) return;

    container.innerHTML = '';

    answers.forEach((answer, index) => {
        const option = document.createElement('div');
        option.className = 'answer-option';
        option.textContent = answer.text;
        option.dataset.index = index;

        option.addEventListener('click', () => selectAnswer(index));

        container.appendChild(option);
    });
}

/**
 * Select an answer.
 *
 * @param {number} index - Answer index
 */
function selectAnswer(index) {
    selectedAnswer = index;

    // Update UI
    document.querySelectorAll('.answer-option').forEach((option, i) => {
        if (i === index) {
            option.classList.add('selected');
        } else {
            option.classList.remove('selected');
        }
    });
}

/**
 * Submit answer button handler.
 */
document.getElementById('btn-submit')?.addEventListener('click', async () => {
    if (selectedAnswer === null) {
        alert('Please select an answer first!');
        return;
    }

    if (!currentQuestion) {
        return;
    }

    const timeSpent = Date.now() - startTime;

    try {
        // Submit answer to API
        const result = await CodeCrazeAPI.submitAnswer(
            currentQuestion.id,
            selectedAnswer,
            timeSpent,
            0 // hints used
        );

        // Display result
        displayResult(result);

    } catch (error) {
        console.error('Failed to submit answer:', error);
        showMessage('Error submitting answer. Please try again.');
    }
});

/**
 * Display answer result and explanation.
 *
 * @param {object} result - Result object from API
 */
function displayResult(result) {
    // Mark answers as correct/incorrect
    document.querySelectorAll('.answer-option').forEach((option, index) => {
        option.style.pointerEvents = 'none'; // Disable clicking

        if (index === result.correct_answer) {
            option.classList.add('correct');
        }
        if (index === result.selected_answer && index !== result.correct_answer) {
            option.classList.add('incorrect');
        }
    });

    // Display explanation
    const explContainer = document.getElementById('explanation-container');
    if (explContainer) {
        explContainer.classList.remove('hidden');
        explContainer.innerHTML = formatExplanation(result.explanation);
    }

    // Update buttons
    document.getElementById('btn-submit')?.classList.add('hidden');
    document.getElementById('btn-next')?.classList.remove('hidden');
}

/**
 * Format explanation HTML.
 *
 * @param {object} explanation - Explanation object
 * @returns {string} HTML string
 */
function formatExplanation(explanation) {
    let html = '<h4>Explanation</h4>';

    if (explanation.your_answer) {
        html += `<p><strong>Your answer:</strong> ${explanation.your_answer.text}</p>`;
        if (explanation.your_answer.why_wrong) {
            html += `<p>${explanation.your_answer.why_wrong}</p>`;
        }
    }

    if (explanation.correct_answer) {
        html += `<p><strong>Correct answer:</strong> ${explanation.correct_answer.text}</p>`;
        if (explanation.correct_answer.why_right) {
            html += `<p>${explanation.correct_answer.why_right}</p>`;
        }
    }

    if (explanation.solution_steps && explanation.solution_steps.length > 0) {
        html += '<h5>Step-by-step solution:</h5><ol>';
        explanation.solution_steps.forEach(step => {
            html += `<li>${step}</li>`;
        });
        html += '</ol>';
    }

    return html;
}

/**
 * Next question button handler.
 */
document.getElementById('btn-next')?.addEventListener('click', async () => {
    try {
        // Get next question
        const response = await CodeCrazeAPI.getNextQuestion(currentSession?.session_id || 'temp', currentMode);

        if (response.question) {
            displayQuestion(response.question);
        } else {
            showMessage('No more questions available. Great work!');
        }
    } catch (error) {
        console.error('Failed to get next question:', error);
        showMessage('Error loading next question. Please try again.');
    }
});

/**
 * Show message in question area.
 *
 * @param {string} message - Message to display
 */
function showMessage(message) {
    const content = document.getElementById('question-content');
    if (content) {
        content.innerHTML = `<p>${message}</p>`;
    }
}

// Export functions
window.PracticeComponent = {
    startPracticeMode,
    displayQuestion,
    selectAnswer
};
