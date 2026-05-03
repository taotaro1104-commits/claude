// タブ切り替え
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const tabId = btn.dataset.tab;
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    btn.classList.add('active');
    const target = document.getElementById('tab-' + tabId);
    if (target) target.classList.add('active');
  });
});

// モバイルナビゲーション
const navToggle = document.querySelector('.nav-toggle');
const navList = document.querySelector('.nav-list');
if (navToggle && navList) {
  navToggle.addEventListener('click', () => navList.classList.toggle('open'));
}

// スクロール時ヘッダーシャドウ
const header = document.querySelector('.site-header');
if (header) {
  window.addEventListener('scroll', () => {
    header.style.boxShadow = window.scrollY > 0 ? '0 2px 16px rgba(0,0,0,0.12)' : '0 2px 8px rgba(0,0,0,0.08)';
  });
}

// 楽天トラベル 都市タブ切り替え
document.querySelectorAll('.rakuten-tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const city = btn.dataset.city;
    document.querySelectorAll('.rakuten-tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.rakuten-city-panel').forEach(p => p.classList.remove('active'));
    btn.classList.add('active');
    const panel = document.getElementById('rakuten-' + city);
    if (panel) panel.classList.add('active');
  });
});
