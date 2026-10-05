# ⚡ DevPulse AI SaaS (`devpulse-saas`)

> **Autonomous AI Code Security, Vulnerability Scanning & PR Bot Platform**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![SaaS](https://img.shields.io/badge/SaaS-Active-brightgreen.svg)]()
[![Python](https://img.shields.io/badge/backend-Flask-blue.svg)]()

`devpulse-saas` is a production-ready Web Application and SaaS platform for automated codebase security reviews, continuous vulnerability scanning, GitHub PR bot auto-reviews, and subscription tier management.

---

## ✨ SaaS Features

- ⚡ **Instant AI Security Playground**: Paste code snippets or GitHub repository URLs for immediate vulnerability analysis and security scoring.
- 📁 **Repository Health Dashboard**: Monitor security scores, open vulnerability findings, and active GitHub PR reviewer bots across all your projects.
- 💳 **Monetization & Subscription Management**: Built-in pricing tiers (Free, Pro $19/mo, Enterprise $49/mo) with simulated Stripe checkout and live API key generation.
- 🤖 **GitHub Webhook Listener**: Endpoint (`/api/webhook/github`) for automated Pull Request security review comments.

---

## 🚀 Running Locally

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Backend Server
```bash
python server.py
```

Open your browser at **`http://localhost:8080`** to view the live dashboard!

---

## 🌲 Repository Structure

```text
devpulse-saas/
├── public/
│   ├── index.html     # Glassmorphic SaaS Dashboard & Landing Page
│   ├── styles.css     # Modern Dark Mode CSS Design System
│   └── app.js         # Client-side API runner & modal handler
├── server.py          # Flask REST API & static server
├── requirements.txt   # Dependencies
└── README.md
```

---

## 📄 License

Distributed under the MIT License. Built by **Pravin Tamilan ([@apravint](https://github.com/apravint))**.
