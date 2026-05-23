'use strict';

// ── Diet colour map (Organic Nature Theme) ─────────────────────────────────
const DIET_META = {
  'Diabetic':      { color: '#b94040', gradient: 'linear-gradient(135deg,#b94040,#7f2020)', icon: '\u{1fa78}' },
  'Low Carb':      { color: '#c8813a', gradient: 'linear-gradient(135deg,#c8813a,#8a5520)', icon: '\u{1f951}' },
  'Heart Healthy': { color: '#c44f8a', gradient: 'linear-gradient(135deg,#c44f8a,#8a2560)', icon: '\u2764\ufe0f' },
  'High Protein':  { color: '#1a7a6e', gradient: 'linear-gradient(135deg,#1a7a6e,#0d4d44)', icon: '\u{1f4aa}' },
  'Balanced':      { color: '#2d6a4f', gradient: 'linear-gradient(135deg,#2d6a4f,#1b4332)', icon: '\u2696\ufe0f' },
};

// ── State ─────────────────────────────────────────────────────────────────
let chartInstance = null;
let currentChartMetric = 'accuracy';
let allMetrics = null;

// ── DOM helpers ───────────────────────────────────────────────────────────
const $ = id => document.getElementById(id);
const el = (tag, cls, html) => {
  const e = document.createElement(tag);
  if (cls)  e.className   = cls;
  if (html) e.innerHTML   = html;
  return e;
};

// ── BMI auto-calc ─────────────────────────────────────────────────────────
function updateBMI() {
  const h = parseFloat($('height').value);
  const w = parseFloat($('weight').value);
  const bmiField = $('bmi');
  const badge    = $('bmi-badge');
  if (!h || !w || h < 50 || w < 10) { bmiField.value = ''; badge.textContent = ''; return; }
  const bmi = w / ((h / 100) ** 2);
  bmiField.value = bmi.toFixed(2);
  let cat = '', col = '';
  if      (bmi < 18.5) { cat = '⚠️ Underweight';  col = '#c8813a'; }
  else if (bmi < 25)   { cat = '✅ Normal weight'; col = '#2d6a4f'; }
  else if (bmi < 30)   { cat = '⚠️ Overweight';    col = '#c8813a'; }
  else                 { cat = '🔴 Obese';           col = '#b94040'; }
  badge.innerHTML = `BMI: <strong>${bmi.toFixed(1)}</strong> — <span style="color:${col}">${cat}</span>`;
}
$('height').addEventListener('input', updateBMI);
$('weight').addEventListener('input', updateBMI);

// ── Toast ─────────────────────────────────────────────────────────────────
function showToast(msg, type = 'success') {
  const t = el('div', `toast ${type}`, (type === 'success' ? '✅ ' : '❌ ') + msg);
  document.body.appendChild(t);
  setTimeout(() => t.remove(), 4000);
}

// ── Loading overlay ───────────────────────────────────────────────────────
function setLoading(on) {
  const ov = $('loading-overlay');
  const spinner = $('btn-spinner');
  const btnText = $('btn-text');
  if (on) {
    ov.classList.add('show');
    if (spinner) spinner.style.display = 'block';
    if (btnText) btnText.textContent   = 'Analysing…';
  } else {
    ov.classList.remove('show');
    if (spinner) spinner.style.display = 'none';
    if (btnText) btnText.textContent   = '🌿 Predict My Diet';
  }
}

// ── Form submit ───────────────────────────────────────────────────────────
$('predict-form').addEventListener('submit', async function (e) {
  e.preventDefault();
  const fd   = new FormData(this);
  const data = {};
  for (const [k, v] of fd.entries()) data[k] = v;

  // Validation
  const required = ['Age','Gender','Height_cm','Weight_kg','BMI','Activity_Level','Sugar_Level','Cholesterol','Goal'];
  const missing = required.filter(k => !data[k]);
  if (missing.length) {
    showToast('Please fill all fields including Activity Level and Goal', 'error');
    return;
  }

  data.model = $('model-select').value;
  setLoading(true);

  try {
    const res  = await fetch('/api/predict', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(data),
    });
    const json = await res.json();
    if (!res.ok) throw new Error(json.error || 'Prediction failed');
    renderResult(json);
    showToast('Diet recommendation ready!', 'success');
    document.getElementById('result-panel').scrollIntoView({ behavior: 'smooth', block: 'start' });
  } catch (err) {
    showToast(err.message, 'error');
  } finally {
    setLoading(false);
  }
});

// ── Render result ─────────────────────────────────────────────────────────
function renderResult(data) {
  const diet   = data.diet || 'Balanced';
  const meta   = DIET_META[diet] || DIET_META['Balanced'];
  const advice = data.advice || {};
  const conf   = data.confidence || 0;

  $('empty-state').style.display  = 'none';
  $('result-panel').style.display = 'block';

  // Header
  $('result-icon').textContent      = meta.icon;
  $('result-diet-name').textContent = diet;
  $('result-diet-name').style.background = meta.gradient;
  $('result-diet-name').style.webkitBackgroundClip = 'text';
  $('result-diet-name').style.webkitTextFillColor  = 'transparent';
  $('result-tagline').textContent   = advice.tagline || '';

  // Card border colour
  $('result-card').style.borderLeftColor = meta.color;

  // Gauge ring
  const gauge = $('gauge-ring');
  gauge.style.setProperty('--pct', conf);
  gauge.style.setProperty('--accent-color', meta.color);
  gauge.style.background = `conic-gradient(${meta.color} calc(${conf} * 1%), #e8f0e8 0%)`;
  $('result-confidence-pct').textContent = conf.toFixed(1) + '%';

  // Description
  $('result-description').textContent = advice.description || '';

  // Calories
  $('result-calories').innerHTML = `🔥 <strong>Recommended:</strong> ${advice.calories || '—'}`;

  // Key nutrients
  const nutBox = $('key-nutrients');
  nutBox.innerHTML = '';
  (advice.key_nutrients || []).forEach(n => {
    const span = el('span', 'tag', n);
    nutBox.appendChild(span);
  });

  // Probability bars
  const probContainer = $('prob-bars');
  probContainer.innerHTML = '';
  const probs = data.probabilities || {};
  const sorted = Object.entries(probs).sort((a, b) => b[1] - a[1]);
  sorted.forEach(([label, pct]) => {
    const m = DIET_META[label] || {};
    const row = el('div', 'prob-row');
    row.innerHTML = `
      <span class="prob-name">${m.icon || ''} ${label}</span>
      <div class="prob-bar-wrap">
        <div class="prob-bar-fill" style="width:0%;background:${m.color || '#2d6a4f'}"></div>
      </div>
      <span class="prob-val">${pct.toFixed(1)}%</span>`;
    probContainer.appendChild(row);
    setTimeout(() => row.querySelector('.prob-bar-fill').style.width = pct + '%', 50);
  });

  // Meal plan
  const mealGrid = $('meal-grid');
  mealGrid.innerHTML = '';
  const meals = advice.meal_plan || {};
  ['breakfast','lunch','dinner','snacks'].forEach(time => {
    if (!meals[time]) return;
    const item = el('div', 'meal-item');
    item.innerHTML = `<div class="meal-time">${time}</div><div class="meal-food">${meals[time]}</div>`;
    mealGrid.appendChild(item);
  });

  // Foods
  const eatList   = $('foods-eat');
  const avoidList = $('foods-avoid');
  eatList.innerHTML   = '';
  avoidList.innerHTML = '';
  (advice.foods_to_eat   || []).slice(0, 5).forEach(f => eatList.innerHTML   += `<li>${f}</li>`);
  (advice.foods_to_avoid || []).slice(0, 5).forEach(f => avoidList.innerHTML += `<li>${f}</li>`);
}

// ── Load model metrics & chart ────────────────────────────────────────────
async function loadModels() {
  try {
    const res     = await fetch('/api/models');
    allMetrics    = await res.json();
    renderModelCards(allMetrics);
    renderChart(allMetrics, currentChartMetric);
  } catch (e) {
    console.warn('Could not load model metrics:', e);
  }
}

const MODEL_LABELS = {
  logistic_regression: 'Logistic Reg.',
  decision_tree:       'Decision Tree',
  random_forest:       'Random Forest',
  xgboost:             'XGBoost',
  ann:                 'ANN (MLP)',
};

function renderModelCards(metrics) {
  const container = $('model-cards');
  if (!container) return;
  container.innerHTML = '';
  Object.entries(metrics).forEach(([name, m]) => {
    const card = el('div', 'model-stat-card');
    card.setAttribute('tabindex', '0');
    card.innerHTML = `
      <div class="model-name">${MODEL_LABELS[name] || name}</div>
      <div class="model-acc">${m.accuracy.toFixed(1)}%</div>
      <div class="model-acc-label">Accuracy</div>`;
    container.appendChild(card);
  });
}

// Organic green chart palette
const BAR_COLORS = ['#2d6a4f', '#52b788', '#74c69d', '#c8813a', '#b94040'];

function renderChart(metrics, metricKey) {
  const canvas = $('model-chart');
  if (!canvas) return;
  const names  = Object.keys(metrics);
  const values = names.map(n => metrics[n][metricKey] || 0);

  if (chartInstance) chartInstance.destroy();
  chartInstance = new Chart(canvas, {
    type: 'bar',
    data: {
      labels: names.map(n => MODEL_LABELS[n] || n),
      datasets: [{
        label: metricKey.replace('_', ' ').toUpperCase(),
        data: values,
        backgroundColor: BAR_COLORS,
        borderRadius: 8,
        borderSkipped: false,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: { label: ctx => ` ${ctx.parsed.y.toFixed(2)}%` },
          backgroundColor: '#ffffff',
          borderColor: 'rgba(45,106,79,0.2)',
          borderWidth: 1,
          titleColor: '#1a2e1a',
          bodyColor:  '#3a5c3a',
          padding: 10,
        },
      },
      scales: {
        x: {
          grid:  { color: 'rgba(45,106,79,0.06)' },
          ticks: { color: '#3a5c3a', font: { size: 12, family: 'Inter' } },
        },
        y: {
          grid:  { color: 'rgba(45,106,79,0.06)' },
          ticks: { color: '#3a5c3a', callback: v => v + '%', font: { family: 'Inter' } },
          min: 0, max: 105,
        },
      },
      animation: { duration: 900, easing: 'easeOutQuart' },
    },
  });
}

// Chart tab switching
document.querySelectorAll('.chart-tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.chart-tab').forEach(t => { t.classList.remove('active'); t.setAttribute('aria-selected','false'); });
    tab.classList.add('active');
    tab.setAttribute('aria-selected', 'true');
    currentChartMetric = tab.dataset.metric;
    if (allMetrics) renderChart(allMetrics, currentChartMetric);
  });
});

// ── Load diet guide cards ─────────────────────────────────────────────────
async function loadDietGuide() {
  try {
    const res   = await fetch('/api/diets');
    const diets = await res.json();
    const grid  = $('diet-cards-grid');
    if (!grid) return;
    grid.innerHTML = '';
    Object.entries(diets).forEach(([name, d]) => {
      const meta = DIET_META[name] || { color: '#2d6a4f', gradient: 'linear-gradient(135deg,#2d6a4f,#1b4332)', icon: '🥗' };
      const card = el('div', 'diet-card');
      const eat   = (d.foods_to_eat   || []).slice(0, 4).map(f => `<li>${f}</li>`).join('');
      const avoid = (d.foods_to_avoid || []).slice(0, 4).map(f => `<li>${f}</li>`).join('');
      card.innerHTML = `
        <div class="diet-card-banner" style="background:${meta.gradient}"></div>
        <div class="diet-card-body">
          <div class="diet-card-header">
            <div class="diet-card-icon" style="background:${meta.color}22">${meta.icon}</div>
            <div>
              <div class="diet-card-title">${name}</div>
              <div class="diet-card-tag tag">${d.tagline || ''}</div>
            </div>
          </div>
          <p class="diet-card-desc">${d.description || ''}</p>
          <div class="diet-card-cal">🔥 <strong>${d.calories || '—'}</strong></div>
          <div class="diet-foods-wrap">
            <div class="diet-foods-col eat"><h5>✅ Eat</h5><ul>${eat}</ul></div>
            <div class="diet-foods-col avoid"><h5>❌ Avoid</h5><ul>${avoid}</ul></div>
          </div>
        </div>`;
      grid.appendChild(card);
    });
  } catch (e) {
    console.warn('Could not load diet guide:', e);
  }
}

// ── Load hero stats ───────────────────────────────────────────────────────
async function loadStats() {
  try {
    const res  = await fetch('/api/stats');
    const data = await res.json();
    if ($('stat-patients')) $('stat-patients').textContent = (data.total_patients || 1000).toLocaleString() + '+';
    if ($('stat-models'))   $('stat-models').textContent   = data.diet_classes || 5;
    if ($('stat-accuracy')) $('stat-accuracy').textContent = (data.best_accuracy || 100) + '%';
  } catch (e) { /* use defaults */ }
}

// ── IntersectionObserver: lazy-load chart ─────────────────────────────────
(function () {
  const section = $('models');
  if (!section || !window.IntersectionObserver) { loadModels(); return; }
  let loaded = false;
  new IntersectionObserver(entries => {
    if (entries[0].isIntersecting && !loaded) { loaded = true; loadModels(); }
  }, { threshold: 0.1 }).observe(section);
})();

// ── Smooth scroll for nav anchor links ───────────────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if (target) { e.preventDefault(); target.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
  });
});

// ── Keyboard shortcut: Ctrl+Enter submits form ────────────────────────────
document.addEventListener('keydown', e => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
    const form = $('predict-form');
    if (form) form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
  }
});

// ── Copy result to clipboard ──────────────────────────────────────────────
function copyResultToClipboard() {
  const diet = $('result-diet-name');
  const conf = $('result-confidence-pct');
  if (!diet || !conf) return;
  const text = `DietAI Result: ${diet.textContent} (${conf.textContent} confidence)`;
  navigator.clipboard && navigator.clipboard.writeText(text).then(() => showToast('Result copied!', 'success'));
}

// ── Init ──────────────────────────────────────────────────────────────────
loadStats();
loadDietGuide();
