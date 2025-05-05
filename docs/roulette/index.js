const wheel = document.querySelector('.wheel');
const btn = document.querySelector('button');

let current = 0;

btn.addEventListener('click', function() {
  const rotate = Math.floor(Math.random() * 360) + 720;
  const angle = current + rotate;

  wheel.style.transform = `rotate(${angle}deg)`;

  current = angle;

  btn.disabled = true;
  wheel.addEventListener('transitionend', () => {
    btn.disabled = false;
  }, { once: true });
});
