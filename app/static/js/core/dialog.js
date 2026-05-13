window.showSuccess = function (title, text = "") {
    Swal.fire({
        icon: "success",
        title,
        text,
        confirmButtonColor: "#3085d6"
    });
};

window.showError = function (title, text = "") {
    Swal.fire({
        icon: "error",
        title,
        text,
        confirmButtonColor: "#d33"
    });
};

window.showWarning = function (title, text = "") {
    Swal.fire({
        icon: "warning",
        title,
        text,
        confirmButtonColor: "#f39c12"
    });
};

window.confirmAction = async function ({
    title = "¿Estás seguro?",
    text = "",
    confirmText = "Sí",
    cancelText = "Cancelar",
    icon = "warning"
} = {}) {

    const result = await Swal.fire({
        title,
        text,
        icon,
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#6c757d",
        confirmButtonText: confirmText,
        cancelButtonText: cancelText,
        reverseButtons: true
    });

    return result.isConfirmed;
};