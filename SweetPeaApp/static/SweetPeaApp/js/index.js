  const toggle = document.querySelector(".nav-toggle");
  const nav = document.querySelector(".dropdown-nav");


toggle.addEventListener("click", (e) => {
  e.stopPropagation();
  nav.classList.toggle("open");
});

// Close nav when clicking outside
document.addEventListener("click", (e) => {
  if (nav.classList.contains("open") && !nav.contains(e.target)) {
    nav.classList.remove("open");
  }
});

// Optional: close on menu link click
document.querySelectorAll(".nav-list a").forEach(link => {
  link.addEventListener("click", () => nav.classList.remove("open"));
});
    
    // Helper: send a GA4 event if gtag is ready
const gaEvent = (name, params = {}) => window.gtag && gtag('event', name, params);

// A) “Get in Touch” button clicks
document.querySelectorAll('.form-button').forEach(btn => {
  btn.addEventListener('click', () => gaEvent('get_in_touch_click', { location: 'card_section' }));
});

  function openModal(id) {
    document.getElementById(id).style.display = 'flex';
  }

  function closeModal(id) {
    document.getElementById(id).style.display = 'none';
  }

  // Close modal when clicking outside
  window.onclick = function (event) {
    const modals = document.querySelectorAll('.modal');
    modals.forEach((modal) => {
      if (event.target === modal) modal.style.display = 'none';
    });
  };


// C) Enquiry form submit attempt (Web3Forms)
const form = document.querySelector('form[action="https://api.web3forms.com/submit"]');
if (form) {
  form.addEventListener('submit', () => gaEvent('form_submit_attempt'));
}

// Enable debug only on localhost
if (window.location.hostname === "localhost") {
  gtag('config', 'G-3TVNTPGJME', { debug_mode: true });
}

(function () {
  // Run after the DOM is ready so all elements are queryable
  document.addEventListener('DOMContentLoaded', function () {

    // Grab references to the elements we'll be working with
    const form = document.getElementById('enquiry-form');
    const modal = document.getElementById('enquiry-success-modal');
    const errorBox = document.getElementById('form-error-message');

    // If any of these are missing, bail silently — page might not have a form
    if (!form || !modal || !errorBox) {
      return;
    }

    const closeBtn = modal.querySelector('.success-modal__close');
    const backdrop = modal.querySelector('.success-modal__backdrop');

    // How long the modal stays open before auto-dismissing (in milliseconds)
    const AUTO_DISMISS_MS = 6000;

    // Track the auto-dismiss timer so we can cancel it if the user closes manually
    let autoDismissTimer = null;

    /**
     * Show the success modal and start the auto-dismiss countdown.
     */
    function showModal() {
      modal.hidden = false;

      // Set focus on the close button so keyboard users can dismiss it easily
      if (closeBtn) {
        closeBtn.focus();
      }

      // Start the auto-dismiss timer
      autoDismissTimer = setTimeout(hideModal, AUTO_DISMISS_MS);

      // Fire the GA4 conversion event (only if gtag is loaded — i.e. user accepted cookies)
      if (typeof gtag === 'function') {
        gtag('event', 'form_submit', {
          'form_name': 'enquiry',
          'form_destination': 'web3forms'
        });
      }
    }

    /**
     * Hide the modal and cancel the auto-dismiss timer.
     */
    function hideModal() {
      modal.hidden = true;

      if (autoDismissTimer) {
        clearTimeout(autoDismissTimer);
        autoDismissTimer = null;
      }
    }

    /**
     * Show the inline error message under the form.
     */
    function showError() {
      errorBox.hidden = false;

      // Scroll the error into view so the user notices it
      errorBox.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    /**
     * Hide the error message (called when the user retries).
     */
    function hideError() {
      errorBox.hidden = true;
    }

    /**
     * Handle the form submission. Prevents the default redirect and
     * posts the data to Web3Forms via fetch() instead.
     */
    form.addEventListener('submit', async function (event) {
      // Stop the browser from doing its default form post + redirect
      event.preventDefault();

      // Hide any previous error before retrying
      hideError();

      // Find the submit button so we can disable it during the request
      const submitBtn = form.querySelector('button[type="submit"]');
      const originalLabel = submitBtn ? submitBtn.textContent : '';

      // Disable the button to prevent double-submission, and update the label
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = 'Sending...';
      }

      try {
        // Build the payload from the form's current values
        const formData = new FormData(form);

        // Web3Forms accepts FormData directly — no need to convert to JSON
        const response = await fetch(form.action, {
          method: 'POST',
          body: formData,
          headers: {
            // Tells Web3Forms we expect a JSON response (so they don't redirect)
            'Accept': 'application/json'
          }
        });

        const result = await response.json();

        // Web3Forms returns { success: true, ... } on success
        if (response.ok && result.success) {
          // Clear the form so the user can't accidentally re-submit the same data
          form.reset();

          // Show the success modal
          showModal();
        } else {
          // The request reached Web3Forms but the submission was rejected
          // (e.g. honeypot triggered, invalid access key, spam detected)
          console.warn('Web3Forms rejected submission:', result);
          showError();
        }
      } catch (err) {
        // Network failure, CORS error, or Web3Forms is down
        console.error('Form submission failed:', err);
        showError();
      } finally {
        // Always re-enable the submit button so the user can try again if needed
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.textContent = originalLabel;
        }
      }
    });

    // Wire up the manual close button
    if (closeBtn) {
      closeBtn.addEventListener('click', hideModal);
    }

    // Allow clicking the backdrop to close the modal too
    if (backdrop) {
      backdrop.addEventListener('click', hideModal);
    }

    // Allow the Escape key to close the modal (accessibility convention)
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && !modal.hidden) {
        hideModal();
      }
    });
  });
})();