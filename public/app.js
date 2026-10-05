// DevPulse AI SaaS Client-Side Application Logic

document.addEventListener('DOMContentLoaded', () => {
  fetchRepos();
  fetchBillingInfo();

  // Code Scanner Handler
  const btnScan = document.getElementById('btn-scan');
  const txtCode = document.getElementById('code-input');
  const resultsContainer = document.getElementById('audit-results');

  if (btnScan) {
    btnScan.addEventListener('click', async () => {
      const code = txtCode.value.trim();
      if (!code) {
        alert('Please paste a code snippet to run audit.');
        return;
      }

      btnScan.innerHTML = '⚡ Scanning Codebase...';
      btnScan.disabled = true;

      try {
        const resp = await fetch('/api/scan', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ code })
        });
        const data = await resp.json();
        renderAuditResults(data);
      } catch (err) {
        alert('Scan failed: ' + err.message);
      } finally {
        btnScan.innerHTML = '⚡ Run Instant AI Audit';
        btnScan.disabled = false;
      }
    });
  }
});

async function fetchRepos() {
  const tbody = document.getElementById('repo-table-body');
  if (!tbody) return;

  try {
    const resp = await fetch('/api/repos');
    const data = await resp.json();
    tbody.innerHTML = '';

    data.repositories.forEach(repo => {
      const tr = document.createElement('tr');
      const scoreClass = repo.health_score >= 9.0 ? 'score-high' : 'score-med';
      
      tr.innerHTML = `
        <td><strong style="color: #fff;">${repo.name}</strong></td>
        <td><span class="score-badge ${scoreClass}">${repo.health_score}/10</span></td>
        <td><span style="color: ${repo.open_issues === 0 ? '#10b981' : '#f59e0b'};">${repo.open_issues} Findings</span></td>
        <td>${repo.last_scan}</td>
        <td>
          <button class="btn-outline" style="padding: 0.3rem 0.8rem; font-size: 0.8rem;" onclick="triggerRepoScan('${repo.name}')">
            Re-scan Repo
          </button>
        </td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    console.error('Error fetching repos:', err);
  }
}

async function fetchBillingInfo() {
  try {
    const resp = await fetch('/api/billing');
    const data = await resp.json();

    const planBadge = document.getElementById('user-plan-badge');
    const apiKeyInput = document.getElementById('user-api-key');

    if (planBadge) planBadge.innerText = data.plan;
    if (apiKeyInput) apiKeyInput.value = data.api_key;
  } catch (err) {
    console.error('Error fetching billing info:', err);
  }
}

function renderAuditResults(data) {
  const container = document.getElementById('audit-results');
  container.style.display = 'block';

  const scoreClass = data.health_score >= 8.5 ? 'score-high' : data.health_score >= 6.0 ? 'score-med' : 'score-low';

  let issuesHtml = '';
  if (data.issues.length === 0) {
    issuesHtml = '<p style="color: #10b981;">✔ No security vulnerabilities or static code defects detected!</p>';
  } else {
    issuesHtml = '<ul style="list-style: none; padding: 0;">';
    data.issues.forEach(issue => {
      issuesHtml += `
        <li style="background: rgba(239, 68, 68, 0.1); border-left: 4px solid #ef4444; margin-bottom: 0.5rem; padding: 0.75rem; border-radius: 4px;">
          <strong style="color: #ef4444;">[${issue.severity}] Line ${issue.line}: ${issue.type}</strong>
          <p style="color: #cbd5e1; font-size: 0.9rem; margin-top: 0.2rem;">${issue.description}</p>
        </li>
      `;
    });
    issuesHtml += '</ul>';
  }

  container.innerHTML = `
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
      <h3 style="color: #fff;">Audit Summary Report</h3>
      <span class="score-badge ${scoreClass}">Health Index: ${data.health_score} / 10.0</span>
    </div>
    <p style="color: var(--text-secondary); margin-bottom: 1rem;">
      Audited <strong>${data.total_lines} lines</strong> • Status: <strong>${data.status}</strong> • Scanned at: ${data.scanned_at}
    </p>
    ${issuesHtml}
  `;
}

function triggerRepoScan(repoName) {
  alert(`⚡ Triggered autonomous AI audit scan on repository: ${repoName}`);
}

function openCheckoutModal(planName) {
  const modal = document.getElementById('checkout-modal');
  document.getElementById('modal-plan-name').innerText = planName;
  modal.classList.add('active');
}

function closeModal() {
  document.getElementById('checkout-modal').classList.remove('active');
}

async function confirmSubscription() {
  const planName = document.getElementById('modal-plan-name').innerText;
  try {
    const resp = await fetch('/api/subscribe', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ plan: planName })
    });
    const data = await resp.json();
    alert(`🎉 ${data.message}\nYour Live API Key: ${data.api_key}`);
    closeModal();
    fetchBillingInfo();
  } catch (err) {
    alert('Subscription failed: ' + err.message);
  }
}
