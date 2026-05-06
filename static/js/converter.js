// Converter functionality

// Set example question
function setQuestion(question) {
    document.getElementById('questionInput').value = question;
    document.getElementById('questionInput').focus();
}

// Clear all inputs and results
function clearAll() {
    document.getElementById('questionInput').value = '';
    hideAllSections();
}

// Hide all result sections
function hideAllSections() {
    document.getElementById('loadingSpinner').classList.add('d-none');
    document.getElementById('sqlResultSection').classList.add('d-none');
    document.getElementById('resultsSection').classList.add('d-none');
    document.getElementById('errorSection').classList.add('d-none');
}

// Show error message
function showError(message) {
    hideAllSections();
    document.getElementById('errorMessage').textContent = message;
    document.getElementById('errorSection').classList.remove('d-none');
}

// Hide error message
function hideError() {
    document.getElementById('errorSection').classList.add('d-none');
}

// Copy SQL query to clipboard
function copySQLQuery() {
    const sqlText = document.getElementById('sqlOutput').textContent;
    navigator.clipboard.writeText(sqlText).then(() => {
        // Show success feedback
        const btn = event.target.closest('button');
        const originalHTML = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-check me-1"></i>Copied!';
        btn.classList.remove('btn-light');
        btn.classList.add('btn-success');
        
        setTimeout(() => {
            btn.innerHTML = originalHTML;
            btn.classList.remove('btn-success');
            btn.classList.add('btn-light');
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy:', err);
        alert('Failed to copy SQL query');
    });
}

// Convert text to SQL
async function convertToSQL() {
    const question = document.getElementById('questionInput').value.trim();
    
    // Validation
    if (!question) {
        showError('Please enter a question');
        return;
    }
    
    // Disable button and show loading
    const convertBtn = document.getElementById('convertBtn');
    const originalBtnHTML = convertBtn.innerHTML;
    convertBtn.disabled = true;
    convertBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Converting...';
    
    hideAllSections();
    document.getElementById('loadingSpinner').classList.remove('d-none');
    
    try {
        // Make API request
        const response = await fetch('/convert', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question: question })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to convert query');
        }
        
        // Hide loading
        document.getElementById('loadingSpinner').classList.add('d-none');
        
        // Display SQL query
        displaySQLQuery(data.sql);
        
        // Display results
        if (data.result.success) {
            displayResults(data.result);
        } else {
            showError('Query executed but returned an error: ' + data.result.error);
        }
        
    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'An error occurred while processing your request');
    } finally {
        // Re-enable button
        convertBtn.disabled = false;
        convertBtn.innerHTML = originalBtnHTML;
    }
}

// Display SQL query with syntax highlighting
function displaySQLQuery(sql) {
    const sqlOutput = document.getElementById('sqlOutput');
    sqlOutput.textContent = sql;
    
    // Trigger Prism.js highlighting
    if (typeof Prism !== 'undefined') {
        Prism.highlightElement(sqlOutput);
    }
    
    document.getElementById('sqlResultSection').classList.remove('d-none');
    
    // Smooth scroll to results
    setTimeout(() => {
        document.getElementById('sqlResultSection').scrollIntoView({ 
            behavior: 'smooth', 
            block: 'nearest' 
        });
    }, 100);
}

// Display query results in table
function displayResults(result) {
    const { columns, data } = result;
    
    // Create table header
    const headerRow = document.getElementById('resultsHeader');
    headerRow.innerHTML = '';
    columns.forEach(col => {
        const th = document.createElement('th');
        th.textContent = col;
        headerRow.appendChild(th);
    });
    
    // Create table body
    const tbody = document.getElementById('resultsBody');
    tbody.innerHTML = '';
    
    if (data.length === 0) {
        const tr = document.createElement('tr');
        const td = document.createElement('td');
        td.colSpan = columns.length;
        td.textContent = 'No results found';
        td.className = 'text-center text-muted py-4';
        tr.appendChild(td);
        tbody.appendChild(tr);
    } else {
        data.forEach((row, index) => {
            const tr = document.createElement('tr');
            tr.style.animationDelay = `${index * 0.05}s`;
            tr.style.animation = 'fadeIn 0.3s ease forwards';
            
            row.forEach(cell => {
                const td = document.createElement('td');
                td.textContent = cell !== null ? cell : 'NULL';
                if (cell === null) {
                    td.className = 'text-muted';
                }
                tr.appendChild(td);
            });
            
            tbody.appendChild(tr);
        });
    }
    
    // Update row count
    document.getElementById('rowCount').textContent = data.length;
    
    // Show results section
    document.getElementById('resultsSection').classList.remove('d-none');
    
    // Smooth scroll to results
    setTimeout(() => {
        document.getElementById('resultsSection').scrollIntoView({ 
            behavior: 'smooth', 
            block: 'nearest' 
        });
    }, 200);
}

// Handle Enter key in textarea
document.addEventListener('DOMContentLoaded', function() {
    const questionInput = document.getElementById('questionInput');
    
    if (questionInput) {
        questionInput.addEventListener('keydown', function(e) {
            // Ctrl+Enter or Cmd+Enter to convert
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                e.preventDefault();
                convertToSQL();
            }
        });
    }
});

// Add fade-in animation for table rows
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);

// Show keyboard shortcut hint
document.addEventListener('DOMContentLoaded', function() {
    const questionInput = document.getElementById('questionInput');
    if (questionInput) {
        const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0;
        const shortcut = isMac ? 'Cmd+Enter' : 'Ctrl+Enter';
        
        const hint = document.createElement('small');
        hint.className = 'text-muted d-block mt-1';
        hint.innerHTML = `<i class="fas fa-keyboard me-1"></i>Press ${shortcut} to convert quickly`;
        
        const formText = questionInput.closest('.mb-3').querySelector('.form-text');
        if (formText) {
            formText.appendChild(document.createElement('br'));
            formText.appendChild(hint);
        }
    }
});

// ─────────────────────────────────────────────
// VOICE INPUT FEATURE
// Uses the Web Speech API (SpeechRecognition).
// No backend changes required.
// ─────────────────────────────────────────────

let recognition = null;
let isListening = false;

function initSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        return null;
    }

    const rec = new SpeechRecognition();
    rec.lang = 'en-US';
    rec.interimResults = true;   // show partial results live in the textarea
    rec.maxAlternatives = 1;
    rec.continuous = false;      // stop after natural pause

    rec.onstart = () => {
        isListening = true;
        setVoiceUI('listening');
    };

    rec.onresult = (event) => {
        let interimTranscript = '';
        let finalTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
                finalTranscript += transcript;
            } else {
                interimTranscript += transcript;
            }
        }

        const input = document.getElementById('questionInput');
        if (finalTranscript) {
            // Append final text, trimming extra whitespace
            input.value = (input.value + ' ' + finalTranscript).trim();
            setVoiceUI('done');
        } else {
            // Show interim result as placeholder hint
            setVoiceUI('listening', `Hearing: "${interimTranscript}"`);
        }
    };

    rec.onerror = (event) => {
        let msg = 'Voice error';
        if (event.error === 'not-allowed') msg = 'Microphone access denied';
        else if (event.error === 'no-speech') msg = 'No speech detected';
        else if (event.error === 'network') msg = 'Network error';
        setVoiceUI('error', msg);
        isListening = false;
    };

    rec.onend = () => {
        isListening = false;
        // If UI still says listening (no result came), reset
        setTimeout(() => setVoiceUI('idle'), 1500);
    };

    return rec;
}

function toggleVoiceInput() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        alert('Your browser does not support voice input.\nPlease use Chrome, Edge, or Safari.');
        return;
    }

    if (isListening) {
        // Stop recording
        if (recognition) recognition.stop();
        isListening = false;
        setVoiceUI('idle');
        return;
    }

    // Start recording
    recognition = initSpeechRecognition();
    if (recognition) {
        try {
            recognition.start();
        } catch (e) {
            // Already started — ignore
        }
    }
}

function setVoiceUI(state, customText) {
    const btn      = document.getElementById('voiceBtn');
    const icon     = document.getElementById('voiceIcon');
    const badge    = document.getElementById('voiceStatus');
    const badgeTxt = document.getElementById('voiceStatusText');

    // Reset classes
    btn.className = 'btn btn-lg';
    icon.className = 'fas';

    switch (state) {
        case 'listening':
            btn.classList.add('btn-danger');
            icon.classList.add('fa-microphone-slash');
            badge.classList.remove('d-none');
            badgeTxt.textContent = customText || 'Listening… speak now';
            break;

        case 'done':
            btn.classList.add('btn-success');
            icon.classList.add('fa-microphone');
            badge.classList.remove('d-none');
            badgeTxt.textContent = '✓ Got it! Tap mic to speak again';
            setTimeout(() => badge.classList.add('d-none'), 2500);
            // Auto-convert after a short pause
            setTimeout(() => {
                const q = document.getElementById('questionInput').value.trim();
                if (q) convertToSQL();
            }, 800);
            break;

        case 'error':
            btn.classList.add('btn-outline-danger');
            icon.classList.add('fa-microphone');
            badge.classList.remove('d-none');
            badgeTxt.textContent = customText || 'Error — try again';
            setTimeout(() => badge.classList.add('d-none'), 3000);
            break;

        default: // idle
            btn.classList.add('btn-outline-danger');
            icon.classList.add('fa-microphone');
            badge.classList.add('d-none');
            break;
    }
}

// Inject blinking dot animation
(function addVoiceStyles() {
    const s = document.createElement('style');
    s.textContent = `
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50%       { opacity: 0.2; }
        }
        .blink-dot { animation: blink 1s infinite; }
        #voiceBtn { transition: all 0.2s ease; min-width: 52px; }
    `;
    document.head.appendChild(s);
})();
