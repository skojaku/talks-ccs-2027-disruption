(function () {
  var K = 1280, cleanup = [], busy = false;
  var TR = '{"name":"fade","duration":"1.1s","builtinFallback":true}';
  function sleep(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }
  function sec(n) { return document.getElementById(String(n)); }
  function named(s, name) {
    var els = s.querySelectorAll('[style*="view-transition-name"]');
    for (var i = 0; i < els.length; i++) {
      var m = (els[i].getAttribute('style') || '').match(/view-transition-name:\s*(\w+)/);
      if (m && m[1] === name) return els[i];
    }
    return null;
  }
  function rectOf(el, s) {
    var r = el.getBoundingClientRect(), sr = s.getBoundingClientRect(), k = K / sr.width;
    return { x: (r.left - sr.left) * k, y: (r.top - sr.top) * k, w: r.width * k, h: r.height * k };
  }
  function reset() { while (cleanup.length) { try { cleanup.pop()(); } catch (e) {} } }
  function apply(slideNo, otherNo, name, rect) {
    var s = sec(slideNo), el = named(s, name);
    if (!el) {
      var src = named(sec(otherNo), name);
      if (!src) return false;
      el = src.cloneNode(true);
      (s.querySelector('.stage') || s).appendChild(el);
      cleanup.push(function () { el.remove(); });
    }
    var cur = rectOf(el, s);
    var prev = { t: el.style.translate, sc: el.style.scale, o: el.style.transformOrigin };
    var hasT = /transform\s*:/.test(el.getAttribute('style') || '');
    var sc = cur.w > 1 ? rect.w / cur.w : 1;
    if (Math.abs(sc - 1) > 0.02 && !hasT) { el.style.transformOrigin = '50% 50%'; el.style.scale = String(sc); }
    el.style.translate = ((rect.x + rect.w / 2) - (cur.x + cur.w / 2)) + 'px ' + ((rect.y + rect.h / 2) - (cur.y + cur.h / 2)) + 'px';
    cleanup.push(function () { el.style.translate = prev.t; el.style.scale = prev.sc; el.style.transformOrigin = prev.o; });
    return true;
  }
  function key(shift) {
    document.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowRight', shiftKey: !!shift, bubbles: true, cancelable: true }));
  }
  function say(o) { try { parent.postMessage(o, '*'); } catch (e) {} }
  async function play(msg) {
    if (busy) return;
    busy = true;
    try {
      reset();
      var N = msg.from, svt = document.startViewTransition;
      document.startViewTransition = function (cb) { cb(); var p = Promise.resolve(); return { finished: p, ready: p, updateCallbackDone: p, skipTransition: function () {} }; };
      location.hash = '#' + N;
      await sleep(350);
      document.startViewTransition = svt;
      var sN = sec(N);
      if (msg.edits && msg.edits.length) {
        msg.edits.forEach(function (e) { if (e.mode === 'to') apply(N + 1, N, e.name, e.rect); else apply(N, N + 1, e.name, e.rect); });
      }
      if (!sN.hasAttribute('data-transition')) sN.setAttribute('data-transition', TR);
      say({ type: 'mm-state', phase: 'before' });
      await sleep(700);
      var frags = sN.querySelectorAll('[data-marpit-fragment]').length;
      if (frags) { key(true); await sleep(300); }
      say({ type: 'mm-state', phase: 'playing' });
      key(true);
      await sleep(1500);
      say({ type: 'mm-state', phase: 'done' });
    } catch (e) { say({ type: 'mm-state', phase: 'error', message: String(e) }); }
    busy = false;
  }
  window.addEventListener('message', function (ev) {
    var m = ev.data;
    if (ev.source !== parent || !m || m.type !== 'mm-play') return;
    play(m);
  });
  window.addEventListener('load', function () { setTimeout(function () { say({ type: 'mm-ready' }); }, 300); });
})();
