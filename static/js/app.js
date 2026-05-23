/* ═══════════════════════════════════════════════════════════════
   DietAI — app.js  |  SPA logic, API calls, Chart.js rendering
   ═══════════════════════════════════════════════════════════════ */

'use strict';

// ── Diet colour map (Organic Nature Theme) ─────────────────────────────────
const DIET_META = {
  'Diabetic':      { color: '#b94040', gradient: 'linear-gradient(135deg,#b94040,#7f2020)', icon: '\u{1fa78}' },
  'Low Carb':      { color: '#c8813a', gradient: 'linear-gradient(135deg,#c8813a,#8a5520)', icon: '\u{1f951}' },
  'Heart Healthy': { color: '#c44f8a', gradient: 'linear-gradient(135deg,#c44f8a,#8a2560)', icon: '\u2764\ufe0f' },
  'High Protein':  { color: '#1a7a6e', gradient: 'linear-gradient(135deg,#1a7a6e,#0d4d44)', icon: '\u{1f4aa}' },
  'Balanced':      { color: '#2d6a4f', gradient: 'linear-gradient(135deg,#2d6a4f,#1b4332)', icon: '\u2696\ufe0f' },
};

// ── State ────────────────────────────────────────────────────────────────────
let chartInstance = null;
let currentChartMetric = 'accuracy';

// ── DOM helpers ──────────────────────────────────────────────────────────────
const $ = id => document.getElementById(id);
const qs = sel => document.querySelector(sel);
const qsa = sel => [...document.querySelectorAll(sel)];
const show = el => { if (el) el.style.display = ''; };
const hide = el => { if (el) el.style.display = 'none'; };
const showFlex = el => { if (el) el.style.display = 'flex'; };

// ── Navigation active state on scroll ────────────────────────────────────────
const sections = ['hero', 'predict', 'models', 'diet-guide'];
const observer = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      qsa('.nav-links a').forEach(a => {
        a.classList.toggle('active', a.getAttribute('href') === `#${e.target.id}`);
      });
    }
  });
}, { threshold: 0.4 });

// ── Counter animation ─────────────────────────────────────────────────────────
function animateCount(el, target, duration = 1200, suffix = '') {
  const start = performance.now();
  const from   = 0;
  const update = t => {
    const elapsed = t - start;
    const progress = Math.min(elapsed / duration, 1);
    const ease = 1 - Math.pow(1 - progress, 3);
    el.textContent = Math.round(from + (target - from) * ease) + suffix;
    if (progress < 1) requestAnimationFrame(update);
  };
  requestAnimationFrame(update);
}

// ── BMI auto-calculation ──────────────────────────────────────────────────────
function calcBMI() {
  const h = parseFloat($('height').value);
  const w = parseFloat($('weight').value);
  const bmiEl  = $('bmi');
  const bmiMsg = $('bmi-msg');
  if (h > 0 && w > 0) {
    const bmi = w / Math.pow(h / 100, 2);
    bmiEl.value = bmi.toFixed(1);
    let cat = bmi < 18.5 ? '⬇ Underweight' : bmi < 25 ? '✔ Normal' : bmi < 30 ? '⚠ Overweight' : '⬆ Obese';
    bmiMsg.textContent = `BMI: ${bmi.toFixed(1)} — ${cat}`;
    bmiMsg.style.color = bmi < 18.5 ? '#06b6d4' : bmi < 25 ? '#10b981' : bmi < 30 ? '#f59e0b' : '#ef4444';
  }
}

// ── Toast ─────────────────────────────────────────────────────────────────────
function showToast(msg, type = 'error') {
  const old = qs('.toast');
  if (old) old.remove();
  const t = document.createElement('div');
  t.className = `toast ${type}`;
  t.innerHTML = `<span>${type === 'error' ? '⚠' : '✓'}</span><span>${msg}</span>`;
  document.body.appendChild(t);
  setTimeout(() => t.style.animation = 'slide-toast 0.4s ease reverse', 3200);
  setTimeout(() => t.remove(), 3600);
}

// ── Loading overlay ───────────────────────────────────────────────────────────
function setLoading(on, text = 'Running prediction…') {
  const ov = $('loading-overlay');
  ov.querySelector('.loader-text').textContent = text;
  ov.classList.toggle('show', on);
}

// ── Gauge ring ────────────────────────────────────────────────────────────────
function setGauge(pct, color) {
  const g = $('gauge-ring');
  g.style.setProperty('--pct', pct);
  g.style.setProperty('--accent-color', color);
  g.style.background = `conic-gradient(${color} ${pct}%, #1e293b 0%)`;
  $('gauge-pct').textContent = `${Math.round(pct)}%`;
}

// ── Render result panel ───────────────────────────────────────────────────────
function renderResult(data) {
  const { diet, confidence, probabilities, advice } = data;
  const meta = DIET_META[diet] || { color: '#7c3aed', gradient: 'linear-gradient(135deg,#7c3aed,#06b6d4)', icon: '🥗' };

  // Header
  $('result-icon').textContent = meta.icon;
  $('result-diet-name').textContent  = diet;
  $('result-diet-name').style.color  = meta.color;
  $('result-tagline').textContent    = advice?.tagline || '';

  // Gauge
  setGauge(confidence, meta.color);

  // Description
  $('result-description').textContent = advice?.description || '';

  // Calorie
  $('result-calories').innerHTML = `<span>🔥</span> Recommended intake: <strong>${advice?.calories || '—'}</strong>`;

  // Probability bars
  const probWrap = $('prob-bars');
  probWrap.innerHTML = '';
  Object.entries(probabilities)
    .sort((a, b) => b[1] - a[1])
    .forEach(([label, val]) => {
      const m = DIET_META[label] || {};
      probWrap.innerHTML += `
        <div class="prob-row">
          <span class="prob-name">${m.icon || ''} ${label}</span>
          <div class="prob-bar-wrap">
            <div class="prob-bar-fill" style="width:0%;background:${m.color || '#7c3aed'}" data-target="${val}"></div>
          </div>
          <span class="prob-val">${val.toFixed(1)}%</span>
        </div>`;
    });
  // Animate bars after paint
  setTimeout(() => {
    probWrap.querySelectorAll('.prob-bar-fill').forEach(el => {
      el.style.width = el.dataset.target + '%';
    });
  }, 50);

  // Meal plan
  const mp = advice?.meal_plan || {};
  $('meal-breakfast').textContent = mp.breakfast || '—';
  $('meal-lunch').textContent     = mp.lunch     || '—';
  $('meal-dinner').textContent    = mp.dinner    || '—';
  $('meal-snacks').textContent    = mp.snacks    || '—';

  // Foods
  const eat   = advice?.foods_to_eat   || [];
  const avoid = advice?.foods_to_avoid || [];
  $('foods-eat').innerHTML   = eat.slice(0,4).map(f => `<li>${f}</li>`).join('');
  $('foods-avoid').innerHTML = avoid.slice(0,4).map(f => `<li>${f}</li>`).join('');

  // Key nutrients
  const kn = advice?.key_nutrients || [];
  $('key-nutrients').innerHTML = kn.map(n => `<span class="tag">${n}</span>`).join('');

  // Show panel
  const panel = $('result-panel');
  panel.style.display = 'block';
  panel.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ── Form submit ───────────────────────────────────────────────────────────────
async function handlePredict(e) {
  e.preventDefault();
  const btn = $('predict-btn');
  btn.disabled = true;
  $('btn-spinner').style.display = 'inline-block';
  $('btn-text').textContent = 'Predicting…';
  setLoading(true);

  const payload = {
    Age:            parseFloat($('age').value),
    Gender:         parseFloat(qs('input[name="gender"]:checked')?.value ?? 0),
    Height_cm:      parseFloat($('height').value),
    Weight_kg:      parseFloat($('weight').value),
    BMI:            parseFloat($('bmi').value),
    Activity_Level: parseFloat($('activity').value),
    Sugar_Level:    parseFloat($('sugar').value),
    Cholesterol:    parseFloat($('cholesterol').value),
    Goal:           parseFloat($('goal').value),
    model:          $('model-select').value,
  };

  // Validate
  const invalid = Object.entries(payload)
    .filter(([k, v]) => k !== 'model' && (isNaN(v) || v === ''))
    .map(([k]) => k);
  if (invalid.length) {
    showToast(`Please fill in: ${invalid.join(', ')}`);
    btn.disabled = false;
    $('btn-spinner').style.display = 'none';
    $('btn-text').textContent = 'Get Diet Recommendation';
    setLoading(false);
    return;
  }

  try {
    const res  = await fetch('/api/predict', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(payload),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Server error');
    renderResult(data);
    showToast('Recommendation ready!', 'success');
  } catch (err) {
    showToast(err.message || 'Prediction failed');
  } finally {
    btn.disabled = false;
    $('btn-spinner').style.display = 'none';
    $('btn-text').textContent = 'Get Diet Recommendation';
    setLoading(false);
  }
}

// ── Chart.js model comparison ────────────────────────────────────────────────
const MODEL_LABELS = {
  logistic_regression: 'Logistic Regression',
  decision_tree:       'Decision Tree',
  random_forest:       'Random Forest',
  xgboost:             'XGBoost',
  ann:                 'ANN',
};
// Organic green chart palette
const BAR_COLORS = ['#2d6a4f','#52b788','#74c69d','#c8813a','#b94040'];

function renderChart(metrics, metricKey) {
  const names  = Object.keys(metrics);
  const values = names.map(n => metrics[n][metricKey]);
  const canvas = $('metrics-chart');
  if (!canvas) return;

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
          bodyColor: '#3a5c3a',
          padding: 10,
          boxShadow: '0 4px 12px rgba(27,67,50,0.1)',
        },
      },
      scales: {
        x: {
          grid: { color: 'rgba(45,106,79,0.06)' },
          ticks: { color: '#3a5c3a', font: { size: 12, family: 'Inter' } },
        },
        y: {
          grid: { color: 'rgba(45,106,79,0.06)' },
          ticks: { color: '#3a5c3a', callback: v => v + '%', font: { family: 'Inter' } },
          min: 0, max: 105,
        },
      },
      animation: { duration: 900, easing: 'easeOutQuart' },
    },
  });
}

function updateModelCards(metrics) {
  const grid = $('models-grid');
  if (!grid) return;
  grid.innerHTML = Object.entries(metrics).map(([name, m]) => `
    <div class="model-stat-card" data-model="${name}">
      <div class="model-name">${MODEL_LABELS[name]}</div>
      <div class="model-acc">${m.accuracy}</div>
      <div class="model-acc-label">Accuracy %</div>
    </div>`).join('');
}

async function loadModels() {
  try {
    const res = await fetch('/api/models');
    if (!res.ok) throw new Error('Metrics not ready');
    const metrics = await res.json();
    updateModelCards(metrics);
    renderChart(metrics, currentChartMetric);

    // Chart tab clicks
    qsa('.chart-tab').forEach(tab => {
      tab.addEventListener('click', () => {
        qsa('.chart-tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        currentChartMetric = tab.dataset.metric;
        renderChart(metrics, currentChartMetric);
      });
    });
  } catch {
    const grid = $('models-grid');
    if (grid) grid.innerHTML = '<p style="color:var(--text-muted);grid-column:1/-1">Train models first: <code>python src/train_models.py && python src/evaluate.py</code></p>';
  }
}

// ── Diet Guide ────────────────────────────────────────────────────────────────
async function loadDietGuide() {
  try {
    const res  = await fetch('/api/diets');
    const data = await res.json();
    const grid = $('diet-guide-grid');
    if (!grid) return;

    grid.innerHTML = Object.entries(data).map(([label, info]) => `
      <div class="diet-card">
        <div class="diet-card-banner" style="background:${info.gradient}"></div>
        <div class="diet-card-body">
          <div class="diet-card-header">
            <div class="diet-card-icon" style="background:${info.color}22">${info.icon}</div>
            <div>
              <div class="diet-card-title">${label}</div>
              <span class="tag diet-card-tag" style="color:${info.color};border-color:${info.color}44;background:${info.color}15">${info.calories}</span>
            </div>
          </div>
          <p class="diet-card-desc">${info.description}</p>
          <div class="diet-foods-wrap">
            <div class="diet-foods-col eat">
              <h5>✓ Eat More</h5>
              <ul>${info.foods_to_eat.slice(0,4).map(f => `<li>${f}</li>`).join('')}</ul>
            </div>
            <div class="diet-foods-col avoid">
              <h5>✕ Avoid</h5>
              <ul>${info.foods_to_avoid.slice(0,4).map(f => `<li>${f}</li>`).join('')}</ul>
            </div>
          </div>
        </div>
      </div>`).join('');
  } catch {
    console.warn('Could not load diet guide');
  }
}

// ── Hero stats from /api/stats ────────────────────────────────────────────────
async function loadStats() {
  try {
    const res  = await fetch('/api/stats');
    const data = await res.json();
    const pEl  = $('stat-patients');
    const fEl  = $('stat-features');
    const mEl  = $('stat-models');
    if (pEl) animateCount(pEl, data.total_patients);
    if (fEl) animateCount(fEl, data.features);
    if (mEl) animateCount(mEl, data.models_available.length);
  } catch { /* silent */ }
}

// ── Init ──────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  // Observe sections for nav highlighting
  sections.forEach(id => {
    const el = $(id);
    if (el) observer.observe(el);
  });

  // BMI auto-calc
  $('height')?.addEventListener('input', calcBMI);
  $('weight')?.addEventListener('input', calcBMI);

  // Form submit
  $('predict-form')?.addEventListener('submit', handlePredict);

  // Load data
  loadStats();
  loadModels();
  loadDietGuide();

  // Scroll → show nav shadow
  window.addEventListener('scroll', () => {
    const nav = $('navbar');
    if (nav) nav.style.background = window.scrollY > 20
      ? 'rgba(7,7,17,0.95)' : 'rgba(7,7,17,0.75)';
  });
});
