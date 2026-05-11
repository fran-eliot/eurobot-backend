/* =========================================================
   GLOBAL TOASTS
========================================================= */

window.showToast = function ({
    title = "Notificación",
    message = "",
    type = "primary",
    duration = 4000
}) {
    const container = document.getElementById("toast-container");

    if (!container) return;

    const toast = document.createElement("div");

    toast.classList.add(
        "app-toast",
        `app-toast-${type}`
    );

    toast.innerHTML = `
        <div class="app-toast-title">${title}</div>
        <div class="app-toast-body">${message}</div>
    `;

    container.prepend(toast);

    setTimeout(() => {
        toast.style.opacity = "0";
        toast.style.transform = "translateX(30px)";

        setTimeout(() => {
            toast.remove();
        }, 250);
    }, duration);
};