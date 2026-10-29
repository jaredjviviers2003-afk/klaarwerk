// Frame-accurate animation: render(t) sets every element's state for time t (seconds).
const clamp = (x) => Math.max(0, Math.min(1, x));
const easeOut = (x) => 1 - Math.pow(1 - x, 3);
const easeInOut = (x) => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
const back = (x) => { const c1 = 1.5, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };
window.custom = window.custom || (() => {});
function render(t) {
  document.querySelectorAll('[data-in]').forEach(el => {
    const tin = +el.dataset.in, tout = el.dataset.out ? +el.dataset.out : 1e9;
    const din = el.dataset.din ? +el.dataset.din : 0.5, dout = el.dataset.dout ? +el.dataset.dout : 0.35;
    const pi = clamp((t - tin) / din), po = clamp((t - tout) / dout);
    const fx = el.dataset.fx || 'up';
    const ei = fx === 'pop' ? back(pi) : easeOut(pi), eo = easeInOut(po);
    let tr = '';
    if (fx === 'up') tr = `translateY(${(1 - ei) * 70 - eo * 50}px)`;
    else if (fx === 'left') tr = `translateX(${(1 - ei) * -120 + eo * 80}px)`;
    else if (fx === 'right') tr = `translateX(${(1 - ei) * 120 - eo * 80}px)`;
    else if (fx === 'pop') tr = `scale(${0.6 + 0.4 * ei - eo * 0.1})`;
    else if (fx === 'rise') tr = `translateY(${(1 - ei) * 500 - eo * 200}px)`;
    el.style.opacity = fx === 'none' ? (t >= tin && t < tout ? 1 : 0) : Math.min(pi * 1.4, 1) * (1 - po);
    el.style.transform = (el.dataset.base || '') + ' ' + tr;
  });
  window.custom(t);
}
window.render = render;
