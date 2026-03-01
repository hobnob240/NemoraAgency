/* NEMORA — lightweight enhancements (no frameworks) */
(() => {
  const $ = (s, r=document) => r.querySelector(s);
  const $$ = (s, r=document) => Array.from(r.querySelectorAll(s));

  // Mobile menu toggle
  const closeMenu = () => {
    if (!menuBtn || !menuPanel) return;
    menuBtn.setAttribute("aria-expanded", "false");
    menuPanel.hidden = true;
  };

  const menuBtn = $("#menuBtn");
  const menuPanel = $("#menuPanel");
  if (menuBtn && menuPanel) {
    menuBtn.addEventListener("click", () => {
      const open = menuBtn.getAttribute("aria-expanded") === "true";
      menuBtn.setAttribute("aria-expanded", String(!open));
      menuPanel.hidden = open;
    });

    // Close menu when a link is clicked (mobile)
    menuPanel.addEventListener("click", (e) => {
      const a = e.target.closest("a");
      if (a) closeMenu();
    });

    // Close menu if resized to desktop
    window.addEventListener("resize", () => {
      if (window.innerWidth > 720) closeMenu();
    }, { passive: true });

  }

  // Scroll reveal
  const revealEls = $$(".reveal");
  if (revealEls.length) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) e.target.classList.add("in");
      });
    }, { threshold: 0.12 });
    revealEls.forEach(el => io.observe(el));
  }

  // Parallax (subtle)
  const parallaxEls = $$(".parallax");
  if (parallaxEls.length) {
    let ticking = false;
    const onScroll = () => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(() => {
        const y = window.scrollY || 0;
        parallaxEls.forEach(el => {
          const speed = Number(el.dataset.speed || 0.08);
          const offset = Math.max(-26, Math.min(26, (y * speed)));
          el.style.setProperty("--par", `${offset}px`);
        });
        ticking = false;
      });
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  // Set current nav link
  const path = (location.pathname.split("/").pop() || "index.html").toLowerCase();
  $$('a[data-nav]').forEach(a => {
    const href = (a.getAttribute("href") || "").toLowerCase();
    if (href === path) a.setAttribute("aria-current", "page");
  });

  // Contact form (mailto fallback)
  const form = $("#contactForm");
  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const fd = new FormData(form);
      const name = (fd.get("name") || "").toString().trim();
      const email = (fd.get("email") || "").toString().trim();
      const company = (fd.get("company") || "").toString().trim();
      const message = (fd.get("message") || "").toString().trim();

      const subject = encodeURIComponent(`NEMORA enquiry${company ? " — " + company : ""}`);
      const body = encodeURIComponent(
        `Name: ${name}\nEmail: ${email}\nCompany: ${company}\n\nMessage:\n${message}\n`
      );

      // Replace with your actual inbox when ready
      const to = form.dataset.to || "hello@nemora.agency";
      window.location.href = `mailto:${to}?subject=${subject}&body=${body}`;
    });
  }
})();
