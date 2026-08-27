# ⚡ Setup Guide

One-time setup to get the auto-sync running on your `DSA` repo. Takes about
5 minutes.

---

### 1. Add the files to your repo
Upload these into your `DSA` GitHub repo, keeping this exact structure:

```
DSA/
├── sync.py
├── requirements.txt
├── README.md
├── SETUP.md
└── .github/
    └── workflows/
        └── leetcode-sync.yml
```

> ⚠️ `leetcode-sync.yml` **must** live inside `.github/workflows/` — GitHub
> only looks for workflows in that exact folder.

---

### 2. Log in to LeetCode
Go to [leetcode.com](https://leetcode.com) and make sure you're signed in
to your account.

---

### 3. Grab your session cookies
Open DevTools (`F12`) → **Application** tab (Chrome) or **Storage** tab
(Firefox) → **Cookies** → `https://leetcode.com`, and copy the values of:

- `LEETCODE_SESSION`
- `csrftoken`

🔒 **Treat these like passwords.** Never paste them into a file or commit —
they go into GitHub Secrets only (next step).

---

### 4. Add them as GitHub Secrets
In your repo: **Settings → Secrets and variables → Actions → New
repository secret**

| Secret name | Value |
|---|---|
| `LEETCODE_SESSION` | the `LEETCODE_SESSION` cookie value |
| `LEETCODE_CSRF_TOKEN` | the `csrftoken` cookie value |

---

### 5. Test it
Go to the **Actions** tab → **Sync LeetCode Submissions** → **Run
workflow**. Check the logs — you should see lines like:

```
Synced: 1-two-sum (Python3)
Done. 1 new solution(s) synced.
```

---

### 6. Sit back
From here it runs on its own every 6 hours. Solve a problem on LeetCode,
and within a few hours it'll show up in `problems/` with no action needed
from you.

---

## 🔁 If it ever stops working

LeetCode session cookies expire every few weeks/months. If the Action
starts failing with an auth error, just repeat **steps 2–4** with fresh
cookie values.

## 🕒 Changing the sync frequency

Edit the cron line in `.github/workflows/leetcode-sync.yml`:

```yaml
schedule:
  - cron: "0 */6 * * *"   # every 6 hours — change as you like
```

[crontab.guru](https://crontab.guru) is handy for building custom schedules.
