// slides-connector-ext/content.js

let lastHash = '';
const baseUrl = 'http://127.0.0.1:8765';

function sendSlideChange(hash) {
    fetch(`${baseUrl}/slide-change?hash=${encodeURIComponent(hash)}`)
        .then(() => console.log('[Connector] sent', hash))
        .catch(err => console.error('[Connector] error', err));
}

function processHashChange() {
    const currentHash = window.location.hash;
    if (currentHash && currentHash.startsWith('#slide=') && currentHash !== lastHash) {
        lastHash = currentHash;
        sendSlideChange(currentHash);
    }
}

// Process slide changes every 500ms
setInterval(processHashChange, 500);

// Also listen for hashchange events
window.addEventListener('hashchange', processHashChange, false);