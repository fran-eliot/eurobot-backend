/* =========================================================
   REALTIME USER NOTIFICATIONS
========================================================= */

document.addEventListener("DOMContentLoaded", () => {
    connectNotificationsWebSocket();
});


function connectNotificationsWebSocket() {
    const protocol =
        window.location.protocol === "https:"
            ? "wss"
            : "ws";

    const socket = new WebSocket(
        `${protocol}://${window.location.host}/ws/notifications`
    );

    // =====================================================
    // KEEPALIVE
    // =====================================================

    socket.onopen = function() {

        console.log("Notifications WS conectado");

        setInterval(() => {

            if (socket.readyState === WebSocket.OPEN) {
                socket.send("ping");
            }

        }, 30000);
    };

    socket.onmessage = function(event) {

        const data = JSON.parse(event.data);

        if (data.type === "notification") {

            prependNotification(data.notification);

            incrementNotificationCount();

            if (window.showToast) {

                showToast({
                    title: data.notification.title,
                    message: data.notification.message,
                    type: "primary"
                });
            }
        }
    };

    socket.onclose = function() {

        console.warn(
            "Notifications WS desconectado. Reintentando..."
        );

        setTimeout(
            connectNotificationsWebSocket,
            3000
        );
    };
}


function prependNotification(notification) {
    const list = document.getElementById("notification-list");

    if (!list) return;

    const empty = list.querySelector(".dropdown-item.text-muted");

    if (empty) {
        empty.remove();
    }

    const item = document.createElement("a");

    item.href = `/notifications/${notification.id_notification}/open`;

    item.classList.add(
        "dropdown-item",
        "notification-item",
        "notification-unread"
    );

    item.dataset.notificationId = notification.id_notification;

    item.innerHTML = `
        <div class="d-flex flex-column">
            <strong class="small">
                ${notification.title}
            </strong>

            <span class="small text-muted">
                ${notification.message}
            </span>

            <small class="text-muted">
                ${formatNotificationDate(notification.created_at)}
            </small>
        </div>
    `;

    list.prepend(document.createElement("div")).classList.add("dropdown-divider");
    list.prepend(item);
}


function incrementNotificationCount() {
    const counter = document.getElementById("notification-count");

    if (!counter) return;

    const current = Number(counter.textContent || 0);
    const next = current + 1;

    counter.textContent = next;
    counter.style.display = "inline-block";
}


function formatNotificationDate(value) {
    if (!value) return "";

    const date = new Date(value);

    return date.toLocaleString([], {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit"
    });
}