document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".js-confirm-form").forEach(form => {
        form.addEventListener("submit", async (e) => {
            e.preventDefault();

            const confirmed = await confirmAction({
                title: form.dataset.confirmTitle || "¿Confirmar acción?",
                text: form.dataset.confirmText || "Esta acción no se puede deshacer.",
                confirmText: form.dataset.confirmButton || "Sí, continuar",
                cancelText: "Cancelar",
                icon: form.dataset.confirmIcon || "warning",
            });

            if (confirmed) {
                form.submit();
            }
        });
    });
});