/* =========================================================
   DASHBOARD REALTIME
   Global activity feed via WebSocket
========================================================= */

document.addEventListener("DOMContentLoaded", () => {
    connectDashboardWebSocket();
});


function connectDashboardWebSocket() {
    const protocol =
        window.location.protocol === "https:"
            ? "wss"
            : "ws";

    const socket = new WebSocket(
        `${protocol}://${window.location.host}/ws/dashboard`
    );

    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);

        console.log("Dashboard WS event:", data);

        const activity = data.activity || data;

        if (
            data.type === "dashboard_feed_event" ||
            activity.event_type
        ) {
            prependDashboardFeedEvent(activity);

            showToast({
                title: "Actividad reciente",
                message: stripHtml(activity.message),
                type: "primary"
            });
        }
    };

    socket.onclose = function() {
        console.warn("Dashboard WS desconectado. Reintentando...");
        setTimeout(connectDashboardWebSocket, 2500);
    };
}


function prependDashboardFeedEvent(activity) {
    if (!activity) return;

    const list = document.getElementById("dashboard-feed-list");
    if (!list) return;

    if (activity.feed_id) {
        const existing = list.querySelector(
            `[data-feed-id='${activity.feed_id}']`
        );

        if (existing) return;
    }

    const emptyState = list.querySelector(".dashboard-feed-empty");

    if (emptyState) {
        emptyState.remove();
    }

    const item = document.createElement("div");

    item.classList.add(
        "px-3",
        "py-3",
        "border-bottom",
        "activity-item",
        "activity-item-new"
    );

    if (activity.feed_id) {
        item.dataset.feedId = activity.feed_id;
    }

    item.innerHTML = `
        <div class="small mb-1">
            ${activity.message}
        </div>

        <div class="text-muted small">
            ${formatDashboardDate(activity.created_at)}
        </div>
    `;

    list.prepend(item);

    limitDashboardFeedItems(list, 8);

    setTimeout(() => {
        item.classList.remove("activity-item-new");
    }, 1800);
}


function limitDashboardFeedItems(list, maxItems) {
    const items = list.querySelectorAll(".activity-item");

    if (items.length <= maxItems) return;

    items.forEach((item, index) => {
        if (index >= maxItems) {
            item.remove();
        }
    });
}


function formatDashboardDate(value) {
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

function stripHtml(html) {
    const div = document.createElement("div");
    div.innerHTML = html;
    return div.textContent || div.innerText || "";
}