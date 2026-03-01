# NEMORA Website (GitHub Pages Ready)

This is a fully static, premium multi-page website built to match the NEMORA brand rules:
- Dark luxury base (deep navy / charcoal)
- Refined gold accents
- High-contrast minimalism
- Uses the provided NEMORA logo image as-is (no recreation of the wordmark)

## Files
- `index.html` — Home
- `services.html` — Services
- `work.html` — Portfolio + case studies
- `about.html` — About
- `contact.html` — Contact (mailto fallback form)
- `styles.css` / `main.js` — shared styling + scroll animations
- `assets/nemora-logo.png` — uploaded logo (used exactly as provided)

## Publish on GitHub Pages
1. Create a new GitHub repo (public or private).
2. Upload all files and folders from this project into the repo root.
3. In GitHub: **Settings → Pages**
   - Source: **Deploy from a branch**
   - Branch: **main** (or `master`) and folder: **/ (root)**
4. Save. Your site will be live at the URL GitHub provides.

## Contact form inbox
The contact form opens the visitor's email client using `mailto:` for maximum compatibility on static hosting.
Update the destination email by editing:

- `contact.html` → `<form ... data-to="hello@nemora.agency">`

Replace with your real inbox.


## Image credits (concept studies)
Public images used on the Work pages:
- “No 1 Hyde Park, London” — Wikimedia Commons (CC BY 2.0)
- “Battersea Power station redevelopment Dec 2020” — Wikimedia Commons (CC BY-SA 2.0)
- “Canary Wharf Skyline” — Wikimedia Commons (Public Domain)
- “The Ritz London Exterior medium res” — Wikimedia Commons (CC BY-SA 4.0)
