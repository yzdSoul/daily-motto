# 可嵌入 Widget 实施计划

> **For Hermes:** Use `subagent-driven-development` skill to implement this plan task-by-task.

**Goal:** Add an iframe-embeddable daily motto widget with light/dark theme (auto-follow system + manual toggle) and a brand link back to the main site.

**Architecture:** A new Flask route `/widget` renders a standalone HTML template (no navbar, no footer, no layout chrome). The widget has its own CSS (light theme with CSS custom properties for dark mode toggle) and a small JS snippet for theme switching. Quote data comes from the existing `get_daily_quote()` function — no API changes needed.

**Tech Stack:** Flask (Jinja2), CSS custom properties, vanilla JS (prefers-color-scheme + localStorage)

**Conventions:**
- CSS custom properties for all colors (like existing `style.css`)
- Jinja2 template (like existing `templates/index.html`)
- Fetch daily quote via server-side render (not client-side API call) — simpler, no extra request
- No tests directory exists in this project; verification is browser-based

---

### Task 1: Create static/widget.css

**Objective:** Widget-specific stylesheet with light theme as default and CSS variables for dark mode override.

**Files:**
- Create: `static/widget.css`

**Complete code:**

```css
/* ===== Widget Styles ===== */
:root {
  /* Light theme (default) */
  --widget-bg: #ffffff;
  --widget-text: #1a1a2e;
  --widget-text-secondary: #6c6c8a;
  --widget-border: #e8e8f0;
  --widget-accent: #b8962e;
  --widget-shadow: 0 2px 16px rgba(0, 0, 0, 0.08);
  --widget-hover-bg: #f8f8fc;
}

/* Dark theme via prefers-color-scheme */
@media (prefers-color-scheme: dark) {
  :root {
    --widget-bg: #1a1a2e;
    --widget-text: #e8e8f0;
    --widget-text-secondary: #a0a0b8;
    --widget-border: #2a2a44;
    --widget-accent: #f0c040;
    --widget-shadow: 0 2px 16px rgba(0, 0, 0, 0.3);
    --widget-hover-bg: #16213e;
  }
}

/* Dark theme via manual toggle (class on html) */
html.dark {
  --widget-bg: #1a1a2e;
  --widget-text: #e8e8f0;
  --widget-text-secondary: #a0a0b8;
  --widget-border: #2a2a44;
  --widget-accent: #f0c040;
  --widget-shadow: 0 2px 16px rgba(0, 0, 0, 0.3);
  --widget-hover-bg: #16213e;
}

html.light {
  --widget-bg: #ffffff;
  --widget-text: #1a1a2e;
  --widget-text-secondary: #6c6c8a;
  --widget-border: #e8e8f0;
  --widget-accent: #b8962e;
  --widget-shadow: 0 2px 16px rgba(0, 0, 0, 0.08);
  --widget-hover-bg: #f8f8fc;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background: transparent;
  color: var(--widget-text);
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}

.widget-card {
  background: var(--widget-bg);
  border: 1px solid var(--widget-border);
  border-radius: 12px;
  padding: 20px 24px;
  box-shadow: var(--widget-shadow);
  position: relative;
  transition: background 0.3s ease, border-color 0.3s ease;
}

.widget-card:hover {
  background: var(--widget-hover-bg);
  border-color: var(--widget-accent);
}

.widget-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.widget-badge {
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 1px;
  color: var(--widget-accent);
  text-transform: uppercase;
  opacity: 0.8;
}

.theme-toggle {
  background: none;
  border: 1px solid var(--widget-border);
  border-radius: 50%;
  width: 28px;
  height: 28px;
  font-size: 0.85rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--widget-text-secondary);
  transition: all 0.2s;
  padding: 0;
  line-height: 1;
}

.theme-toggle:hover {
  border-color: var(--widget-accent);
  color: var(--widget-accent);
}

.quote-cn {
  font-family: 'Noto Serif SC', 'Songti SC', serif;
  font-size: 1.15rem;
  font-weight: 700;
  line-height: 1.6;
  margin-bottom: 8px;
  color: var(--widget-text);
}

.quote-en {
  font-size: 0.85rem;
  line-height: 1.5;
  color: var(--widget-text-secondary);
  font-style: italic;
}

.quote-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 12px;
  padding-top: 10px;
  border-top: 1px solid var(--widget-border);
}

.quote-author {
  font-family: 'Noto Serif SC', 'Songti SC', serif;
  font-size: 0.8rem;
  color: var(--widget-text-secondary);
}

.brand-link {
  font-size: 0.7rem;
  color: var(--widget-text-secondary);
  text-decoration: none;
  opacity: 0.6;
  transition: opacity 0.2s;
}

.brand-link:hover {
  opacity: 1;
  color: var(--widget-accent);
}
```

**Step 1:** Write the file to `static/widget.css`.

**Step 2:** Verify file exists and syntax looks correct.

**Step 3:** Commit
```bash
git add static/widget.css
git commit -m "feat: add widget stylesheet with light/dark theme support"
```

---

### Task 2: Create static/widget.js

**Objective:** Theme management — auto-detect system preference, respect manual override, persist choice across sessions.

**Files:**
- Create: `static/widget.js`

**Complete code:**

```javascript
/**
 * Widget Theme Manager
 * - Auto-detect system color scheme via prefers-color-scheme
 * - Manual toggle button to override
 * - Persist choice in localStorage
 */
(function() {
  const STORAGE_KEY = 'widget-theme';

  function getSystemTheme() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function getSavedTheme() {
    return localStorage.getItem(STORAGE_KEY);
  }

  function applyTheme(theme) {
    const html = document.documentElement;
    html.classList.remove('light', 'dark');
    html.classList.add(theme);
  }

  function setTheme(theme) {
    applyTheme(theme);
    localStorage.setItem(STORAGE_KEY, theme);
  }

  function toggleTheme() {
    const current = document.documentElement.classList.contains('dark') ? 'dark' : 'light';
    setTheme(current === 'dark' ? 'light' : 'dark');
  }

  // Initialize
  const saved = getSavedTheme();
  if (saved) {
    applyTheme(saved);
  } else {
    applyTheme(getSystemTheme());
  }

  // Listen for system theme changes (only when no saved override)
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
    if (!getSavedTheme()) {
      applyTheme(e.matches ? 'dark' : 'light');
    }
  });

  // Expose toggle function for the button
  window.widgetToggleTheme = toggleTheme;
})();
```

**Step 1:** Write the file to `static/widget.js`.

**Step 2:** Verify file syntax.

**Step 3:** Commit
```bash
git add static/widget.js
git commit -m "feat: add widget theme manager JS"
```

---

### Task 3: Create templates/widget.html

**Objective:** Standalone widget template — no navbar, no footer, just the quote card with theme toggle button and brand link.

**Files:**
- Create: `templates/widget.html`

**Complete code:**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>每日格言 · 每日一帖</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='widget.css') }}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
</head>
<body>
  <div class="widget-card">
    <div class="widget-header">
      <span class="widget-badge">Daily Motto · {{ today }}</span>
      <button class="theme-toggle" onclick="widgetToggleTheme()" title="切换主题">🌓</button>
    </div>

    <div class="quote-cn">{{ quote.cn }}</div>
    <div class="quote-en">{{ quote.en }}</div>

    <div class="quote-footer">
      <span class="quote-author">—— {{ quote.author }}</span>
      <a href="https://yzdsoul-daily-motto.hf.space" class="brand-link" target="_blank" rel="noopener">📜 每日格言</a>
    </div>
  </div>

  <script src="{{ url_for('static', filename='widget.js') }}"></script>
</body>
</html>
```

**Step 1:** Write the file to `templates/widget.html`.

**Step 2:** Verify file looks correct.

**Step 3:** Commit
```bash
git add templates/widget.html
git commit -m "feat: add widget template with daily quote and theme toggle"
```

---

### Task 4: Add /widget route to app.py

**Objective:** New Flask route that renders the widget template with daily quote data.

**Files:**
- Modify: `app.py` (insert after the `/api/categories` route, before `if __name__`)

**Step 1:** Read the current `app.py` to confirm no changes. Then add the route.

Insert this code at line 108 (before `if __name__ == "__main__":`):

```python
# ========== Widget ==========

@app.route("/widget")
def widget():
    """可嵌入 Widget - 每日格言卡片"""
    daily = get_daily_quote()
    return render_template("widget.html",
                         quote=daily,
                         today=date.today().isoformat())
```

**Step 2:** Verify by running `python app.py` (or `flask run`) and visiting `/widget` in browser.

**Step 3:** Commit
```bash
git add app.py
git commit -m "feat: add /widget route for embeddable daily motto card"
```

---

### Task 5: Verify in Browser

**Objective:** Confirm the widget renders correctly, theme switching works, and it's embeddable via iframe.

**Step 1:** Start the dev server
```bash
cd ~/projects/daily-motto-web
python app.py
```

**Step 2:** Open `http://localhost:5000/widget` in a browser. Verify:
- [ ] Quote card renders with Chinese text, English text, and author
- [ ] Date badge shows today's date
- [ ] Theme toggle button (🌓) is visible
- [ ] "每日格言" brand link is visible at bottom-right

**Step 3:** Test theme switching
- [ ] Toggle button switches between light and dark themes
- [ 】Theme persists after page refresh (localStorage)
- [ ] Open DevTools → toggle `prefers-color-scheme` emulation → theme follows system preference when no saved override

**Step 4:** Test iframe embedding
Create a simple HTML file for testing:
```html
<!DOCTYPE html>
<html>
<body style="background:#f0f0f0; padding:40px;">
  <h2>我的网站</h2>
  <p>下面是一个每日格言 Widget：</p>
  <iframe src="http://localhost:5000/widget"
          width="100%" height="180"
          frameborder="0"
          style="max-width:500px; border-radius:12px;">
  </iframe>
</body>
</html>
```
- [ ] Widget renders inside iframe
- [ ] No CORS errors in console
- [ ] Widget is 180px tall (no scrolling inside iframe)

**Step 5:** Clean up — kill the dev server.

**Step 6:** Commit final tweaks if any.

---

## Rollback

If something goes wrong, revert all changes:
```bash
git log --oneline -10
# Find the commits from this feature
git revert HEAD~4..HEAD  # Revert all 4-5 widget commits
```

## Verification Checklist

- [ ] `/widget` route renders a standalone HTML page
- [ ] Widget inherits no styles from the main site's navbar/footer
- [ ] Default theme is light
- [ ] Auto-follows system dark mode via `prefers-color-scheme`
- [ ] Manual toggle (🌓 button) overrides system preference
- [ ] Theme persists in localStorage across page loads
- [ ] System theme change (while no saved override) updates live
- [ ] Daily quote matches what's shown on the main site's homepage
- [ ] Brand link ("📜 每日格言") points to the live site
- [ ] iframe embed works with `frameborder="0"` at 180px height
