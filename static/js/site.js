document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector(".nav-toggle");
  const menu = document.querySelector(".nav-menu");
  if (toggle && menu) {
    toggle.addEventListener("click", () => {
      const open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      menu.classList.toggle("is-open", !open);
      document.body.classList.toggle("menu-open", !open);
    });
    menu.querySelectorAll("a").forEach(link => link.addEventListener("click", () => {
      toggle.setAttribute("aria-expanded", "false");
      menu.classList.remove("is-open");
      document.body.classList.remove("menu-open");
    }));
  }
  const year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();

  const revealItems = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    revealItems.forEach(item => observer.observe(item));
  } else revealItems.forEach(item => item.classList.add("visible"));

  const form = document.getElementById("contactForm");
  const status = document.getElementById("formStatus");
  if (form && status) {
    form.addEventListener("submit", event => {
      if (!form.checkValidity()) {
        event.preventDefault();
        status.textContent = "Please check the required fields and enter a valid email address.";
        status.classList.add("error");
        form.reportValidity();
      } else {
        status.textContent = "Sending your enquiry…";
        status.classList.remove("error");
      }
    });
  }
});
