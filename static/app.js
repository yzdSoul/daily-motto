/**
 * 每日格言 - 前端交互脚本
 */

// ===== Toast 提示 =====
function showToast(message) {
    let toast = document.getElementById('toast');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'toast';
        toast.className = 'toast';
        document.body.appendChild(toast);
    }
    toast.textContent = message || '已复制到剪贴板 📋';
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 2000);
}

// ===== 点击复制格言 =====
function copyQuote(element) {
    const cn = element.querySelector('.quote-cn')?.textContent || '';
    const en = element.querySelector('.quote-en')?.textContent || '';
    const author = element.querySelector('.quote-author')?.textContent || '';
    const text = `${cn}\n${en}\n${author}`;

    navigator.clipboard.writeText(text).then(() => {
        showToast('已复制到剪贴板 📋');
    }).catch(() => {
        // Fallback for older browsers
        const ta = document.createElement('textarea');
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
        showToast('已复制到剪贴板 📋');
    });
}

// ===== 刷新随机格言 =====
function refreshRandom() {
    const section = document.getElementById('random-section');
    const card = section.querySelector('.quote-card');

    // Add fade-out
    card.style.opacity = '0';
    card.style.transform = 'translateY(10px)';

    fetch('/api/random')
        .then(res => res.json())
        .then(data => {
            // Update content
            card.querySelector('.quote-cn').textContent = data.cn;
            card.querySelector('.quote-en').textContent = data.en;
            card.querySelector('.quote-author').textContent = '—— ' + data.author;
            card.querySelector('.quote-category').textContent = data.category;

            // Fade in
            card.style.transition = 'all 0.3s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        })
        .catch(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        });
}

// ===== 分类计数 =====
document.addEventListener('DOMContentLoaded', function() {
    // Load category counts
    const countSpans = document.querySelectorAll('[id^="count-"]');
    if (countSpans.length > 0) {
        fetch('/api/categories')
            .then(res => res.json())
            .then(data => {
                const categories = Object.keys(data.counts);
                countSpans.forEach((span, i) => {
                    if (i < categories.length) {
                        span.textContent = data.counts[categories[i]] + ' 条';
                    }
                });
            })
            .catch(() => {
                countSpans.forEach(span => span.textContent = '');
            });
    }

    // Add click handler for all quote cards
    document.querySelectorAll('.quote-card:not([onclick])').forEach(card => {
        card.addEventListener('click', () => copyQuote(card));
        card.title = '点击复制';
    });
});
