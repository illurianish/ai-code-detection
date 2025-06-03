/**
 * AI Code Detection Bot - Frontend JavaScript
 * Handles user interactions, API communication, and result display
 */

// Config
const CONFIG = {
    API_BASE_URL: 'https://ai-code-detection.onrender.com',
    DEMO_MODE: false,
    MAX_FILE_SIZE: 1024 * 1024, // 1MB
    BACKEND_TIMEOUT: 5000,
    MIN_CODE_LENGTH: 10,
    MAX_CODE_LENGTH: 100000,
    SAMPLE_CODES: {
        python: `def fibonacci(n):
    """Generate the nth Fibonacci number."""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Example usage
result = fibonacci(10)
print(f"The 10th Fibonacci number is: {result}")`,
        
        javascript: `function reverseString(str) {
    // Convert string to array, reverse it, then join back
    return str.split('').reverse().join('');
}

// Example usage
const originalString = "Hello World";
const reversed = reverseString(originalString);
console.log("Original:", originalString);
console.log("Reversed:", reversed);`,

        java: `public class Calculator {
    public static void main(String[] args) {
        int result = add(5, 3);
        System.out.println("Result: " + result);
    }
    
    public static int add(int a, int b) {
        return a + b;
    }
}`,

        cpp: `#include <iostream>
using namespace std;

int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

int main() {
    int num = 5;
    cout << "Factorial of " << num << " is " << factorial(num) << endl;
    return 0;
}`,

        html: `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Website</title>
</head>
<body>
    <header>
        <h1>Welcome to My Website</h1>
    </header>
    <main>
        <p>This is a sample HTML document.</p>
        <button onclick="alert('Hello World!')">Click Me</button>
    </main>
</body>
</html>`,

        css: `.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    text-align: center;
    padding: 2rem;
    border-radius: 10px;
}

.button {
    background-color: #3498db;
    color: white;
    padding: 12px 24px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.button:hover {
    background-color: #2980b9;
    transform: translateY(-2px);
}`
    }
};

// DOM elements
const elements = {
    fileInput: document.getElementById('file-input'),
    fileName: document.getElementById('file-name'),
    languageSelect: document.getElementById('language-select'),
    codeInput: document.getElementById('code-input'),
    charCount: document.getElementById('char-count'),
    lineCount: document.getElementById('line-count'),
    analyzeBtn: document.getElementById('analyze-btn'),
    clearBtn: document.getElementById('clear-btn'),
    sampleBtn: document.getElementById('sample-btn'),
    resultsSection: document.getElementById('results-section'),
    loadingOverlay: document.getElementById('loading-overlay'),
    errorMessage: document.getElementById('error-message'),
    errorText: document.getElementById('error-text'),
    aboutModal: document.getElementById('about-modal')
};

let currentAnalysis = null;

function init() {
    setupEventListeners();
    updateInputStats();
    checkBackendStatus();
}

function setupEventListeners() {
    elements.fileInput.addEventListener('change', handleFileUpload);
    
    elements.codeInput.addEventListener('input', updateInputStats);
    elements.codeInput.addEventListener('paste', () => {
        setTimeout(updateInputStats, 10);
    });
    
    elements.analyzeBtn.addEventListener('click', analyzeCode);
    elements.clearBtn.addEventListener('click', clearInput);
    elements.sampleBtn.addEventListener('click', loadSampleCode);
    
    elements.languageSelect.addEventListener('change', updateLanguageHighlight);
    
    document.addEventListener('keydown', handleKeyboardShortcuts);
    
    elements.aboutModal.addEventListener('click', (e) => {
        if (e.target === elements.aboutModal) {
            hideAbout();
        }
    });
}

function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    if (file.size > CONFIG.MAX_FILE_SIZE) {
        showError(`File too large. Maximum size is ${CONFIG.MAX_FILE_SIZE / 1024 / 1024}MB`);
        event.target.value = '';
        return;
    }
    
    const extension = file.name.split('.').pop().toLowerCase();
    const languageMap = {
        'py': 'python',
        'java': 'java',
        'cpp': 'cpp',
        'cc': 'cpp',
        'cxx': 'cpp',
        'c++': 'cpp',
        'c': 'cpp',
        'html': 'html',
        'htm': 'html',
        'css': 'css',
        'js': 'javascript',
        'jsx': 'javascript',
        'ts': 'typescript',
        'tsx': 'typescript'
    };
    
    if (languageMap[extension]) {
        elements.languageSelect.value = languageMap[extension];
        updateLanguageHighlight();
    } else {
        showError('Unsupported file type');
        event.target.value = '';
        return;
    }
    
    const reader = new FileReader();
    reader.onload = (e) => {
        const content = e.target.result;
        if (content.length > CONFIG.MAX_CODE_LENGTH) {
            showError(`Code too long. Maximum length is ${CONFIG.MAX_CODE_LENGTH / 1024}KB`);
            event.target.value = '';
            return;
        }
        elements.codeInput.value = content;
        updateInputStats();
        elements.fileName.textContent = file.name;
    };
    reader.onerror = (error) => {
        showError(`Error reading file: ${error.message}`);
        event.target.value = '';
    };
    reader.readAsText(file);
}

function updateInputStats() {
    const code = elements.codeInput.value;
    const charCount = code.length;
    const lineCount = code.split('\n').length;
    
    elements.charCount.textContent = `${charCount.toLocaleString()} characters`;
    elements.lineCount.textContent = `${lineCount.toLocaleString()} lines`;
    
    elements.analyzeBtn.disabled = code.trim().length < CONFIG.MIN_CODE_LENGTH;
}

function loadSampleCode() {
    const language = elements.languageSelect.value;
    const sampleCode = CONFIG.SAMPLE_CODES[language] || CONFIG.SAMPLE_CODES.python;
    
    elements.codeInput.value = sampleCode;
    updateInputStats();
    elements.fileName.textContent = 'Sample code loaded';
}

function clearInput() {
    elements.codeInput.value = '';
    elements.fileInput.value = '';
    elements.fileName.textContent = 'No file selected';
    hideResults();
    updateInputStats();
}

function updateLanguageHighlight() {
    const language = elements.languageSelect.value;
    console.log(`Language changed to: ${language}`);
}

function handleKeyboardShortcuts(event) {
    if (event.ctrlKey || event.metaKey) {
        switch (event.key) {
            case 'Enter':
                event.preventDefault();
                if (!elements.analyzeBtn.disabled) {
                    analyzeCode();
                }
                break;
            case 'l':
                event.preventDefault();
                loadSampleCode();
                break;
            case 'k':
                event.preventDefault();
                clearInput();
                break;
        }
    }
}

async function checkBackendStatus() {
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), CONFIG.BACKEND_TIMEOUT);
        
        const response = await fetch(`${CONFIG.API_BASE_URL}/health`, {
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        if (!response.ok) {
            throw new Error(`Backend returned status ${response.status}`);
        }
        console.log('Backend is available');
    } catch (error) {
        const message = error.name === 'AbortError' 
            ? 'Backend connection timed out'
            : `Backend not available: ${error.message}`;
        console.warn(message);
        showError('Backend server is not available. Using demo mode.');
    }
}

async function analyzeCode() {
    const code = elements.codeInput.value.trim();
    const language = elements.languageSelect.value;
    
    if (code.length < CONFIG.MIN_CODE_LENGTH) {
        showError('Please enter at least 10 characters of code');
        return;
    }
    
    showLoading();
    hideError();
    
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/detect`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                code: code,
                language: language
            })
        });
        
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.error) {
            throw new Error(result.error);
        }
        
        currentAnalysis = result;
        displayResults(result);
        
    } catch (error) {
        console.error('Analysis error:', error);
        
        // fallback to demo mode
        if (error.message.includes('fetch')) {
            const demoResult = generateDemoResult(code, language);
            currentAnalysis = demoResult;
            displayResults(demoResult);
            showError('Using demo mode - backend unavailable', 3000);
        } else {
            showError(`Analysis failed: ${error.message}`);
        }
    } finally {
        hideLoading();
    }
}

/**
 * Generate a demo result when backend is unavailable
 */
function generateDemoResult(code, language) {
    const lines = code.split('\n').length;
    const chars = code.length;
    const hasComments = /\/\/|#|\/\*|\*\//.test(code);
    const hasFunctions = /function|def |func |fn |sub /.test(code);
    
    const aiIndicators = [
        code.includes('result'),
        code.includes('data'),
        hasComments && code.match(/\/\/|#/g)?.length > lines * 0.3,
        code.includes('Example usage'),
        code.includes('This function'),
        /\b(generate|create|build|process|handle)\b/i.test(code)
    ];
    
    const aiScore = aiIndicators.filter(Boolean).length / aiIndicators.length;
    const isAI = aiScore > 0.4;
    const confidence = isAI ? 0.6 + (aiScore * 0.3) : 0.7 - (aiScore * 0.3);
    
    return {
        prediction: isAI ? "AI" : "Human",
        confidence: confidence,
        is_ai_generated: isAI,
        ai_probability: isAI ? confidence : 1 - confidence,
        human_probability: isAI ? 1 - confidence : confidence,
        features: {
            lines_of_code: lines,
            comment_ratio: hasComments ? 0.3 : 0.1,
            avg_line_length: chars / lines,
            complexity_score: hasFunctions ? lines / 10 : lines / 20
        },
        analysis: {
            lines_of_code: lines,
            comment_ratio: hasComments ? 0.3 : 0.1,
            avg_line_length: Math.round(chars / lines),
            complexity_score: Math.round(hasFunctions ? lines / 10 : lines / 20)
        },
        reasons: isAI ? [
            `Demo mode: ${Math.round(confidence * 100)}% confidence in AI authorship`,
            "Contains common AI patterns in variable naming",
            "Formatting consistency suggests automated generation"
        ] : [
            `Demo mode: ${Math.round(confidence * 100)}% confidence in human authorship`,
            "Natural code structure suggests human writing",
            "Lacks typical AI generation patterns"
        ]
    };
}

/**
 * Display analysis results
 */
function displayResults(result) {
    elements.resultsSection.style.display = 'block';
    elements.resultsSection.scrollIntoView({ behavior: 'smooth' });
    
    const resultBadge = document.getElementById('result-badge');
    const resultIcon = document.getElementById('result-icon');
    const resultText = document.getElementById('result-text');
    
    resultBadge.className = `result-badge ${result.prediction.toLowerCase()}`;
    resultIcon.className = result.is_ai_generated ? 'fas fa-robot result-icon' : 'fas fa-user result-icon';
    resultText.textContent = result.is_ai_generated ? 'AI Generated' : 'Human Written';
    
    const confidenceValue = document.getElementById('confidence-value');
    const confidenceFill = document.getElementById('confidence-fill');
    
    const confidencePercent = Math.round(result.confidence * 100);
    confidenceValue.textContent = `${confidencePercent}%`;
    confidenceFill.style.width = `${confidencePercent}%`;
    
    const aiProb = result.ai_probability || 0;
    const humanProb = result.human_probability || 0;
    
    document.getElementById('ai-probability').textContent = `${Math.round(aiProb * 100)}%`;
    document.getElementById('human-probability').textContent = `${Math.round(humanProb * 100)}%`;
    document.getElementById('lines-of-code').textContent = result.analysis.lines_of_code || 0;
    document.getElementById('complexity-score').textContent = result.analysis.complexity_score || 0;
    
    const reasoningList = document.getElementById('reasoning-list');
    reasoningList.innerHTML = '';
    (result.reasons || []).forEach(reason => {
        const li = document.createElement('li');
        li.textContent = reason;
        reasoningList.appendChild(li);
    });
    
    const featuresGrid = document.getElementById('features-grid');
    featuresGrid.innerHTML = '';
    
    const enhancedFeatures = [
        {
            name: 'Code Structure',
            items: [
                { label: 'Lines of Code', value: result.analysis.lines_of_code || 0, format: 'number' },
                { label: 'Functions', value: result.features?.function_count || 0, format: 'number' },
                { label: 'Complexity Score', value: result.analysis.complexity_score || 0, format: 'number' },
                { label: 'Avg Line Length', value: result.analysis.avg_line_length || 0, format: 'decimal' }
            ]
        },
        {
            name: 'Style Analysis',
            items: [
                { label: 'Comment Ratio', value: result.analysis.comment_ratio || 0, format: 'percentage' },
                { label: 'Indentation Consistency', value: result.features?.indentation_consistency || 0, format: 'percentage' },
                { label: 'Perfect Formatting Score', value: result.features?.perfect_formatting_score || 0, format: 'percentage' },
                { label: 'Blank Line Ratio', value: result.features?.blank_line_ratio || 0, format: 'percentage' }
            ]
        },
        {
            name: 'AI Patterns',
            items: [
                { label: 'AI Variable Names', value: result.features?.ai_variable_names || 0, format: 'number' },
                { label: 'AI Function Names', value: result.features?.ai_function_names || 0, format: 'number' },
                { label: 'Generic Name Ratio', value: result.features?.generic_name_ratio || 0, format: 'percentage' },
                { label: 'AI Comment Patterns', value: result.features?.ai_comment_patterns || 0, format: 'number' }
            ]
        }
    ];
    
    enhancedFeatures.forEach(category => {
        const categoryHeader = document.createElement('div');
        categoryHeader.className = 'feature-category-header';
        categoryHeader.innerHTML = `<h4>${category.name}</h4>`;
        featuresGrid.appendChild(categoryHeader);
        
        category.items.forEach(item => {
            const featureItem = document.createElement('div');
            featureItem.className = 'feature-item';
            
            let formattedValue;
            switch (item.format) {
                case 'percentage':
                    formattedValue = `${(item.value * 100).toFixed(1)}%`;
                    break;
                case 'decimal':
                    formattedValue = item.value.toFixed(1);
                    break;
                case 'number':
                default:
                    formattedValue = Math.round(item.value);
                    break;
            }
            
            featureItem.innerHTML = `
                <span class="feature-name">${item.label}</span>
                <span class="feature-value">${formattedValue}</span>
            `;
            featuresGrid.appendChild(featureItem);
        });
    });
}

/**
 * Hide results section
 */
function hideResults() {
    elements.resultsSection.style.display = 'none';
    currentAnalysis = null;
}

/**
 * Show loading overlay
 */
function showLoading() {
    elements.loadingOverlay.classList.add('show');
    elements.analyzeBtn.disabled = true;
}

/**
 * Hide loading overlay
 */
function hideLoading() {
    elements.loadingOverlay.classList.remove('show');
    updateInputStats();
}

/**
 * Show error message
 */
function showError(message, duration = 5000) {
    elements.errorText.textContent = message;
    elements.errorMessage.style.display = 'flex';
    
    if (duration > 0) {
        setTimeout(hideError, duration);
    }
}

/**
 * Hide error message
 */
function hideError() {
    elements.errorMessage.style.display = 'none';
}

/**
 * Show about modal
 */
function showAbout() {
    elements.aboutModal.classList.add('show');
}

/**
 * Hide about modal
 */
function hideAbout() {
    elements.aboutModal.classList.remove('show');
}

/**
 * Copy results to clipboard
 */
function copyResults() {
    if (!currentAnalysis) return;
    
    const resultText = `
AI Code Detection Results
========================
Prediction: ${currentAnalysis.prediction}
Confidence: ${Math.round(currentAnalysis.confidence * 100)}%
AI Probability: ${Math.round(currentAnalysis.ai_probability * 100)}%
Human Probability: ${Math.round(currentAnalysis.human_probability * 100)}%

Analysis:
- Lines of Code: ${currentAnalysis.analysis.lines_of_code}
- Comment Ratio: ${currentAnalysis.analysis.comment_ratio.toFixed(2)}
- Avg Line Length: ${currentAnalysis.analysis.avg_line_length.toFixed(1)}
- Complexity Score: ${currentAnalysis.analysis.complexity_score}

Reasoning:
${currentAnalysis.reasons.map(reason => `- ${reason}`).join('\n')}
    `.trim();
    
    navigator.clipboard.writeText(resultText).then(() => {
        showError('Results copied to clipboard!', 2000);
    }).catch(() => {
        showError('Failed to copy results');
    });
}

/**
 * Export results as JSON
 */
function exportResults() {
    if (!currentAnalysis) return;
    
    const dataStr = JSON.stringify(currentAnalysis, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = 'ai-detection-results.json';
    link.click();
    
    URL.revokeObjectURL(url);
}

// Initialize when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

// Expose functions globally for HTML onclick handlers
window.showAbout = showAbout;
window.hideAbout = hideAbout;
window.hideError = hideError;
window.copyResults = copyResults;
window.exportResults = exportResults; 