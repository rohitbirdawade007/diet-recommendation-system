// DietAI SPA - initial
// ── Keyboard shortcut: Ctrl+Enter submits prediction form ──────────────────
document.addEventListener('keydown', function(e) {
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
    var form = document.getElementById('predict-form');
    if (form) form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
  }
});

// ── Smooth scroll polyfill for older browsers ──────────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(function(a) {
  a.addEventListener('click', function(e) {
    var target = document.querySelector(a.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

// ── IntersectionObserver for lazy chart loading ────────────────────────────
(function() {
  var modelsSection = document.getElementById('models');
  if (!modelsSection || !window.IntersectionObserver) return;
  var observed = false;
  var observer = new IntersectionObserver(function(entries) {
    if (entries[0].isIntersecting && !observed) {
      observed = true;
      loadModels();   // fetch and render chart only when visible
    }
  }, { threshold: 0.1 });
  observer.observe(modelsSection);
})();

// ── Copy result to clipboard ───────────────────────────────────────────────
function copyResultToClipboard() {
  var diet = document.getElementById('result-diet-name');
  var conf = document.getElementById('result-confidence-pct');
  if (!diet || !conf) return;
  var text = 'DietAI Result: ' + diet.textContent + ' (' + conf.textContent + ' confidence)';
  navigator.clipboard && navigator.clipboard.writeText(text).then(function() {
    showToast('Result copied to clipboard!', 'success');
  });
}
