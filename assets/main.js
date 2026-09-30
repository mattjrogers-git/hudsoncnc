(function () {
  var t = document.querySelector('.menu-toggle'), n = document.getElementById('nav');
  if (t && n) t.addEventListener('click', function () {
    var o = n.classList.toggle('open'); t.setAttribute('aria-expanded', o ? 'true' : 'false');
  });

  // filter chips (projects + panels)
  document.querySelectorAll('[data-filter-group]').forEach(function (group) {
    var target = document.querySelector(group.getAttribute('data-filter-group'));
    group.addEventListener('click', function (e) {
      var b = e.target.closest('.chip'); if (!b) return;
      group.querySelectorAll('.chip').forEach(function (c) { c.setAttribute('aria-pressed', c === b ? 'true' : 'false'); });
      var f = b.getAttribute('data-f');
      target.querySelectorAll('[data-cat]').forEach(function (el) {
        el.hidden = !(f === 'all' || el.getAttribute('data-cat').split(' ').indexOf(f) > -1);
      });
    });
  });

  // lightbox
  document.addEventListener('click', function (e) {
    var img = e.target.closest('img[data-full]'); if (!img) return;
    var lb = document.createElement('div'); lb.className = 'lb'; lb.setAttribute('role', 'dialog'); lb.setAttribute('aria-label', img.alt || 'Photo');
    lb.innerHTML = '<button type="button">Close</button><img alt="">';
    lb.querySelector('img').src = img.getAttribute('data-full'); lb.querySelector('img').alt = img.alt;
    function close() { lb.remove(); document.removeEventListener('keydown', k); }
    function k(ev) { if (ev.key === 'Escape') close(); }
    lb.addEventListener('click', function (ev) { if (ev.target === lb || ev.target.tagName === 'BUTTON') close(); });
    document.addEventListener('keydown', k);
    document.body.appendChild(lb); lb.querySelector('button').focus();
  });

  // thumbnails swap main project image
  document.querySelectorAll('.thumbs img').forEach(function (th) {
    th.addEventListener('click', function (e) {
      e.stopPropagation();
      var card = th.closest('.proj'), main = card.querySelector('img.main');
      main.src = th.getAttribute('data-sm'); main.setAttribute('data-full', th.getAttribute('data-full')); main.alt = th.alt;
    });
  });

  // prefill design code from ?design= or #design-XX
  var code = null;
  try { code = new URLSearchParams(location.search).get('design'); } catch (e) {}
  var f = document.getElementById('q-design');
  if (f && code) f.value = code;
})();
