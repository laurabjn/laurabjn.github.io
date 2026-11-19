(() => {
  'use strict';

  const header = document.querySelector('.site-header');
  const toggle = document.getElementById('nav-toggle');
  const menu = document.getElementById('menu');

  /* ---------- Menu mobile ---------- */
  if (header && toggle && menu) {
    const setMenu = (open) => {
      toggle.setAttribute('aria-expanded', String(open));
      header.classList.toggle('is-open', open);
    };

    toggle.addEventListener('click', () => {
      setMenu(toggle.getAttribute('aria-expanded') !== 'true');
    });

    menu.addEventListener('click', (event) => {
      if (event.target.closest('a')) setMenu(false);
    });

    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && header.classList.contains('is-open')) {
        setMenu(false);
        toggle.focus();
      }
    });

    window.matchMedia('(min-width: 981px)').addEventListener('change', (event) => {
      if (event.matches) setMenu(false);
    });
  }

  /* ---------- Filet sous l'en-tête au défilement ---------- */
  const toTop = document.getElementById('to-top');
  if (header) {
    const onScroll = () => {
      header.classList.toggle('is-scrolled', window.scrollY > 8);
      // Le bouton flottant apparaît une fois le premier écran dépassé
      if (toTop) toTop.classList.toggle('is-visible', window.scrollY > window.innerHeight * 0.8);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ---------- Année du pied de page ---------- */
  const year = document.getElementById('annee');
  if (year) year.textContent = String(new Date().getFullYear());

  /* ---------- Copier l'adresse e-mail ---------- */
  const emailLink = document.getElementById('email-link');
  const copyBtn = document.getElementById('copy-email');
  const email = emailLink ? emailLink.textContent.trim() : '';

  if (emailLink && copyBtn) {
    const label = copyBtn.textContent;
    let timer;

    copyBtn.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(email);
        copyBtn.textContent = 'Adresse copiée';
      } catch (error) {
        // Presse-papiers indisponible : on sélectionne l'adresse pour une copie manuelle.
        const range = document.createRange();
        range.selectNodeContents(emailLink);
        const selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
        copyBtn.textContent = 'Sélectionnée, faites Ctrl+C';
      }
      clearTimeout(timer);
      timer = setTimeout(() => { copyBtn.textContent = label; }, 2500);
    });
  }

  /* ---------- Formulaire de contact ---------- */
  const form = document.getElementById('contact-form');
  const statusEl = document.getElementById('form-status');

  if (form && statusEl) {
    const submitBtn = form.querySelector('button[type="submit"]');

    const setStatus = (message, state) => {
      statusEl.textContent = message;
      if (state) statusEl.dataset.state = state;
      else delete statusEl.dataset.state;
    };

    /* Panneau de confirmation affiché à la place du formulaire après un envoi réussi */
    const success = document.getElementById('form-success');
    const successText = document.getElementById('form-success-text');
    const againBtn = document.getElementById('form-again');
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    const showSuccess = (data) => {
      const firstName = String(data.get('nom') || '').trim().split(/\s+/)[0];
      const replyTo = String(data.get('email') || '').trim();
      successText.textContent = `Merci${firstName ? ' ' + firstName : ''}, votre demande a bien été envoyée. `
        + `Je vous réponds sous 48 h ouvrées${replyTo ? ' à ' + replyTo : ''}.`;
      setStatus('');
      form.classList.add('is-sent');
      success.hidden = false;
      success.scrollIntoView({ behavior: reducedMotion ? 'auto' : 'smooth', block: 'center' });
      success.focus({ preventScroll: true });
    };

    if (success && againBtn) {
      againBtn.addEventListener('click', () => {
        success.hidden = true;
        form.classList.remove('is-sent');
        form.elements.nom.focus();
      });
    }

    /* Vérification anti-robot (Cloudflare Turnstile), active seulement si une clé de site est renseignée */
    const siteKey = (form.dataset.turnstileSitekey || '').trim();
    let turnstileId = null;
    const resetCaptcha = () => {
      if (window.turnstile && turnstileId !== null) window.turnstile.reset(turnstileId);
    };

    if (siteKey) {
      window.onTurnstileLoad = () => {
        const box = document.getElementById('captcha');
        const target = document.getElementById('turnstile');
        box.hidden = false;
        turnstileId = window.turnstile.render(target, {
          sitekey: siteKey,
          theme: 'dark',
          language: 'fr',
          size: target.offsetWidth < 300 ? 'compact' : 'flexible',
        });
      };
      // Le script Cloudflare ne se charge qu'à l'approche du formulaire, pour alléger l'arrivée sur la page
      let requested = false;
      const loadTurnstile = () => {
        if (requested) return;
        requested = true;
        const script = document.createElement('script');
        script.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit&onload=onTurnstileLoad';
        script.async = true;
        script.defer = true;
        document.head.appendChild(script);
      };
      if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
          if (entries.some((entry) => entry.isIntersecting)) {
            observer.disconnect();
            loadTurnstile();
          }
        }, { rootMargin: '600px 0px' });
        observer.observe(form);
      } else {
        loadTurnstile();
      }
      form.addEventListener('focusin', loadTurnstile, { once: true });
    }

    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      const data = new FormData(form);

      // Champ piège rempli : c'est un robot, on ignore l'envoi.
      if (data.get('_gotcha')) return;

      const endpoint = (form.dataset.endpoint || '').trim();

      if (endpoint && siteKey) {
        if (!window.turnstile || turnstileId === null) {
          setStatus(`La vérification anti-robot n'a pas pu se charger. Rechargez la page ou écrivez-moi directement à ${email}.`, 'error');
          return;
        }
        const token = window.turnstile.getResponse(turnstileId);
        if (!token) {
          setStatus("Merci de valider la vérification anti-robot avant d'envoyer votre message.", 'error');
          return;
        }
        data.set('cf-turnstile-response', token);
      }

      if (endpoint) {
        submitBtn.disabled = true;
        setStatus('Envoi en cours…');
        try {
          const response = await fetch(endpoint, {
            method: 'POST',
            body: data,
            headers: { Accept: 'application/json' },
          });
          if (!response.ok) throw new Error(`HTTP ${response.status}`);
          form.reset();
          if (success) showSuccess(data);
          else setStatus('Merci, votre demande a bien été envoyée. Je vous réponds sous 48 h ouvrées.', 'ok');
        } catch (error) {
          setStatus(`Le message n'a pas pu être envoyé. Réessayez dans un instant ou écrivez-moi à ${email}.`, 'error');
        } finally {
          submitBtn.disabled = false;
          resetCaptcha(); // un jeton Turnstile ne sert qu'une fois
        }
        return;
      }

      // Aucun service d'envoi configuré : on prépare l'e-mail dans la messagerie du visiteur.
      const subject = `Demande de projet : ${data.get('type')}`;
      const body = [
        `Nom : ${data.get('nom')}`,
        `E-mail : ${data.get('email')}`,
        `Profil : ${data.get('profil')}`,
        `Type de projet : ${data.get('type')}`,
        `Budget : ${data.get('budget') || 'Non précisé'}`,
        '',
        data.get('message'),
      ].join('\r\n');

      window.location.href = `mailto:${email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
      setStatus(`Votre messagerie devrait s'ouvrir avec le message prérempli. Si rien ne s'ouvre, écrivez-moi directement à ${email}.`);
    });
  }
})();
