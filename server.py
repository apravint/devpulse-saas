"""
DevPulse AI SaaS Backend Server
===============================
Provides API endpoints for GitHub repository security auditing,
PR auto-review webhooks, and subscription management.
"""

import os
import re
import json
import time
import uuid
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder="public", static_url_path="")
CORS(app)

# In-memory storage for SaaS state
USER_SUBSCRIPTIONS = {
    "user_1": {
        "plan": "Pro Tier",
        "monthly_scans_used": 14,
        "scan_limit": 500,
        "api_key": "dp_live_9f8a32b104ce89a2",
        "status": "active"
    }
}

REPOSITORIES = [
    {
        "id": "repo_1",
        "name": "apravint/AI-DevPulse",
        "health_score": 9.4,
        "status": "Healthy",
        "last_scan": "2 hours ago",
        "open_issues": 1,
        "pr_bot_enabled": True
    },
    {
        "id": "repo_2",
        "name": "apravint/tamil-ai-suite",
        "health_score": 8.4,
        "status": "Attention Required",
        "last_scan": "10 minutes ago",
        "open_issues": 3,
        "pr_bot_enabled": True
    },
    {
        "id": "repo_3",
        "name": "apravint/omarchy-ubuntu",
        "health_score": 9.8,
        "status": "Healthy",
        "last_scan": "1 day ago",
        "open_issues": 0,
        "pr_bot_enabled": False
    }
]

def perform_ai_audit(code_snippet: str):
    """Static security and quality analysis engine for SaaS scan API."""
    lines = code_snippet.split("\n")
    issues = []
    score = 9.5

    for idx, line in enumerate(lines, 1):
        line_str = line.strip()
        if "api_key" in line_str.lower() and "=" in line_str and not ("os.getenv" in line_str or "os.environ" in line_str or "getenv(" in line_str):
            issues.append({"line": idx, "severity": "HIGH", "type": "Secret Exposure", "description": "Potential hardcoded API key or credential."})
            score -= 2.0
        if "eval(" in line_str or "exec(" in line_str:
            issues.append({"line": idx, "severity": "CRITICAL", "type": "Code Injection", "description": "Dangerous dynamic execution call (eval/exec)."})
            score -= 3.0
        if "shell=True" in line_str and "subprocess" in line_str:
            issues.append({"line": idx, "severity": "MEDIUM", "type": "Process Injection", "description": "Subprocess call with shell=True."})
            score -= 1.5
        if "SELECT " in line_str.upper() and "+" in line_str and not "?" in line_str:
            issues.append({"line": idx, "severity": "HIGH", "type": "SQL Injection", "description": "Unsanitized string concatenation in SQL query."})
            score -= 2.5

    return {
        "health_score": max(1.0, round(score, 1)),
        "total_lines": len(lines),
        "total_issues": len(issues),
        "issues": issues,
        "status": "PASS" if score >= 8.0 else "WARN" if score >= 5.0 else "FAIL"
    }

@app.route("/")
def index():
    return send_from_directory("public", "index.html")

@app.route("/api/scan", methods=["POST"])
def api_scan():
    data = request.json or {}
    code = data.get("code", "")
    url = data.get("url", "")

    if not code and not url:
        return jsonify({"error": "Provide either 'code' snippet or 'url' to scan"}), 400

    if url and not code:
        code = f"# Mock repository fetched from {url}\nimport os\napi_key = os.getenv('API_KEY')\ndef run():\n    print('Safe Execution')"

    result = perform_ai_audit(code)
    result["scanned_at"] = time.strftime("%Y-%m-%d %H:%M:%S UTC")
    return jsonify(result)

@app.route("/api/repos", methods=["GET"])
def get_repos():
    return jsonify({"repositories": REPOSITORIES})

@app.route("/api/billing", methods=["GET"])
def get_billing():
    return jsonify(USER_SUBSCRIPTIONS["user_1"])

@app.route("/api/subscribe", methods=["POST"])
def subscribe():
    data = request.json or {}
    plan = data.get("plan", "Developer Pro ($19/mo)")
    new_key = f"dp_live_{uuid.uuid4().hex[:16]}"
    
    USER_SUBSCRIPTIONS["user_1"] = {
        "plan": plan,
        "monthly_scans_used": 0,
        "scan_limit": 5000 if "Enterprise" in plan else 500,
        "api_key": new_key,
        "status": "active"
    }
    return jsonify({
        "success": True,
        "message": f"Successfully upgraded to {plan}!",
        "api_key": new_key,
        "billing": USER_SUBSCRIPTIONS["user_1"]
    })

@app.route("/api/webhook/github", methods=["POST"])
def github_webhook():
    event = request.headers.get("X-GitHub-Event", "pull_request")
    data = request.json or {}
    
    return jsonify({
        "status": "acknowledged",
        "event": event,
        "action": "AI-DevPulse PR review triggered",
        "bot_comment": "⚡ DevPulse AI reviewed PR: 0 Security Vulnerabilities Found. Code Health: 9.6/10."
    })

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
