(function () {
  var t = document.querySelector('.nav-toggle'), n = document.getElementById('nav');
  if (t && n) t.addEventListener('click', function () {
    var o = n.classList.toggle('open'); t.setAttribute('aria-expanded', o);
  });
  // YouTube facade: swap the poster for the real player only on click.
  document.querySelectorAll('.video[data-yt]').forEach(function (v) {
    v.querySelector('a').addEventListener('click', function (e) {
      e.preventDefault();
      var f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + v.dataset.yt + '?autoplay=1&rel=0';
      f.allow = 'autoplay; encrypted-media; picture-in-picture'; f.allowFullscreen = true;
      f.title = 'TrekWest tour video';
      v.replaceChildren(f);
    });
  });
  // Respect reduced motion for the hero loop.
  if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.querySelectorAll('video[autoplay]').forEach(function (v) { v.pause(); v.removeAttribute('autoplay'); });
  }
})();
