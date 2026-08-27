<div align="center">

# 🧠 DSA

### My Data Structures & Algorithms journey — auto-synced from LeetCode

*Every problem I solve on LeetCode lands here automatically. No copy-pasting, no manual commits.*

[![LeetCode](https://img.shields.io/badge/LeetCode-Aryanbhadani123-FFA116?style=for-the-badge&logo=leetcode&logoColor=white)](https://leetcode.com/u/Aryanbhadani123/)
[![Auto Sync](https://img.shields.io/badge/Sync-Automated-2ea44f?style=for-the-badge&logo=githubactions&logoColor=white)](../../actions/workflows/leetcode-sync.yml)
[![Language](https://img.shields.io/badge/Made%20with-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

</div>

---

## ✨ What this is

This repo is my living, breathing DSA logbook. A scheduled **GitHub Action**
checks LeetCode every few hours, finds any problems I've newly solved
(✅ Accepted submissions), and commits them here — solution code, title,
difficulty, and tags — all by itself.

No manual uploads. No "forgot to push my solution" days. Just solve on
LeetCode, and it shows up here.

```
        ┌────────────────┐        ┌──────────────────┐        ┌───────────────┐
        │   Solve on     │  ───▶  │   GitHub Action   │  ───▶  │   Auto-commit │
        │   LeetCode     │        │  runs every 6 hrs │        │   to this repo│
        └────────────────┘        └──────────────────┘        └───────────────┘
```

---

## 📂 Repo structure

```
DSA/
├── problems/
│   ├── 1-two-sum/
│   │   ├── README.md         → title, difficulty, tags, link
│   │   └── solution.py       → my accepted solution
│   ├── 200-number-of-islands/
│   │   ├── README.md
│   │   └── solution.cpp
│   └── ...
├── synced_submissions.json   → internal tracker (don't edit)
├── sync.py                   → the sync engine
├── SETUP.md                  → one-time setup guide
└── .github/workflows/
    └── leetcode-sync.yml     → the automation itself
```

---

## ⚙️ How it works

| Step | What happens |
|------|---------------|
| 🕐 | A GitHub Action wakes up every 6 hours (or on-demand) |
| 🔍 | It checks my LeetCode account for new **Accepted** submissions |
| 📥 | Pulls the problem title, difficulty, tags, and my actual code |
| 📁 | Writes it into a clean `problems/<id>-<name>/` folder |
| 🚀 | Commits and pushes — automatically |

Every language I solve in gets its own subfolder, so if I later revisit a
problem in a different language, both versions live side by side.

---

## 📊 Why I built this

Consistency is the whole game with DSA practice. This repo is my proof of
work — a public, timestamped, zero-effort record of every problem I grind
through, so my GitHub contribution graph and my LeetCode streak finally
tell the same story.

---

## 🛠️ Setup

Want to run something similar for your own LeetCode account? See
[`SETUP.md`](./SETUP.md) for the full one-time setup (takes about 5
minutes).

---

<div align="center">

*Built with 🧩 problems, ☕ patience, and a GitHub Action that never sleeps.*

</div>
