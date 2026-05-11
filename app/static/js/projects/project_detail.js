/* =========================================================
   PROJECT DETAIL PAGE
   Kanban + Realtime + Activity Feed
========================================================= */

/* =========================================================
   CONFIG
========================================================= */

const CURRENT_USER_ID = window.APP_CONFIG.currentUserId;
const PROJECT_ID = window.APP_CONFIG.projectId;


/* =========================================================
   INIT
========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    initKanban();
    initStatusButtons();
    refreshKanbanUI();
    renderUsers([]);
    connectWebSocket();

});


/* =========================================================
   KANBAN DRAG & DROP
========================================================= */

function initKanban() {

    let draggedTask = null;

    document.querySelectorAll(".kanban-task").forEach(task => {

        task.addEventListener("dragstart", (e) => {

            if (task.getAttribute("draggable") !== "true") return;

            draggedTask = task;

            e.dataTransfer.setData(
                "taskId",
                task.dataset.taskId
            );

            task.classList.add("loading");
        });

        task.addEventListener("dragend", () => {
            task.classList.remove("loading");
        });

    });

    document.querySelectorAll(".kanban-column").forEach(column => {

        column.addEventListener("dragover", e => {
            e.preventDefault();
            column.classList.add("drag-over");
        });

        column.addEventListener("dragleave", () => {
            column.classList.remove("drag-over");
        });

        column.addEventListener("drop", async (e) => {

            e.preventDefault();

            column.classList.remove("drag-over");

            const taskId = e.dataTransfer.getData("taskId");
            const newStatus = column.dataset.status;

            if (!taskId || !newStatus) return;

            await changeTaskStatus(taskId, newStatus);

        });

    });

}


/* =========================================================
   STATUS BUTTONS
========================================================= */

function initStatusButtons() {
    document.addEventListener("click", async (event) => {
        const button = event.target.closest(".js-change-status");

        if (!button) return;

        event.preventDefault();
        event.stopPropagation();

        const taskId = button.dataset.taskId;
        const newStatus = button.dataset.nextStatus;

        if (!taskId || !newStatus) return;

        await changeTaskStatus(taskId, newStatus);
    });
}

/* =========================================================
   COMMON TASK STATUS UPDATE
========================================================= */

async function changeTaskStatus(taskId, newStatus) {

    const taskElement = document.querySelector(
        `.kanban-task[data-task-id='${taskId}']`
    );

    const targetColumn = document.querySelector(
        `.kanban-column[data-status='${newStatus}']`
    );

    const originColumn = taskElement?.closest(".kanban-column");

    if (!taskElement || !targetColumn) return;

    // evitar mover a la misma columna
    if (originColumn === targetColumn) return;

    // optimistic UI
    targetColumn.appendChild(taskElement);

    taskElement.classList.add("loading");

    try {

        const response = await fetch(
            `/tasks/${taskId}/status`,
            {
                method: "POST",
                headers: {
                    "Content-Type":
                        "application/x-www-form-urlencoded"
                },
                body: `new_status=${newStatus}`
            }
        );

        if (!response.ok) {
            throw new Error();
        }

        taskElement.classList.remove("loading");
        taskElement.classList.add("success");

        updateTaskCardAction(taskElement, newStatus);

        refreshKanbanUI();

        setTimeout(() => {
            taskElement.classList.remove("success");
        }, 800);

    } catch (error) {

        // rollback
        if (originColumn) {
            originColumn.appendChild(taskElement);
        }

        refreshKanbanUI();

        taskElement.classList.remove("loading");
        taskElement.classList.add("error");

        setTimeout(() => {
            taskElement.classList.remove("error");
        }, 1200);

        alert("Error al actualizar estado");

    }

}


/* =========================================================
   UPDATE TASK CARD BUTTON / STYLE
========================================================= */

function updateTaskCardAction(taskElement, status) {

    // eliminar botón previo
    const oldButton = taskElement.querySelector(
        ".js-change-status"
    );

    if (oldButton) {
        oldButton.remove();
    }

    // reset visual
    const title = taskElement.querySelector("strong");

    if (title) {
        title.classList.remove("text-muted");
        title.style.textDecoration = "none";
    }

    // TODO
    if (status === "todo") {

        taskElement.insertAdjacentHTML(
            "beforeend",
            `
            <button type="button"
                    class="btn btn-sm btn-outline-primary mt-2 btn-block js-change-status"
                    data-task-id="${taskElement.dataset.taskId}"
                    data-next-status="doing">
                Empezar
            </button>
            `
        );

    }

    // DOING
    if (status === "doing") {

        taskElement.insertAdjacentHTML(
            "beforeend",
            `
            <button type="button"
                    class="btn btn-sm btn-success mt-2 btn-block js-change-status"
                    data-task-id="${taskElement.dataset.taskId}"
                    data-next-status="done">
                Finalizar
            </button>
            `
        );

    }

    // DONE
    if (status === "done") {

        if (title) {
            title.classList.add("text-muted");
            title.style.textDecoration = "line-through";
        }

    }


}


/* =========================================================
   WEBSOCKET CONNECTION
========================================================= */

function connectWebSocket() {

    const protocol =
        window.location.protocol === "https:"
            ? "wss"
            : "ws";

    const socket = new WebSocket(
        `${protocol}://${window.location.host}/ws/projects/${PROJECT_ID}`
    );

    socket.onmessage = function(event) {

        const data = JSON.parse(event.data);

        // usuarios online
        if (data.type === "users_online") {
            renderUsers(data.users);
        }

        // tarea movida realtime
        if (data.type === "task_updated") {
            moveTaskRealtime(
                data.task_id,
                data.status
            );
        }

        // auditoría realtime
        if (data.type === "audit") {
            appendAuditToTimeline(data);
        }

        // feed realtime
        if (data.type === "feed_event") {
            prependFeedEvent(data.activity);
        }

    };

    socket.onclose = function() {

        console.warn(
            "WebSocket desconectado. Reintentando..."
        );

        setTimeout(connectWebSocket, 2000);

    };

}


/* =========================================================
   REALTIME TASK MOVE
========================================================= */

function moveTaskRealtime(taskId, status) {

    const task = document.querySelector(
        `.kanban-task[data-task-id='${taskId}']`
    );

    const column = document.querySelector(
        `.kanban-column[data-status='${status}']`
    );

    if (!task || !column) return;

    // evitar mover si ya está
    if (task.parentElement !== column) {
        column.appendChild(task);
    }

    updateTaskCardAction(task, status);

    refreshKanbanUI();

}


/* =========================================================
   ONLINE USERS
========================================================= */

function renderUsers(users) {

    const container = document.getElementById("online-users-list");

    if (!container) return;

    const counter = document.getElementById("online-users-count");

    if (counter) {
        counter.textContent = users ? users.length : 0;
    }

    container.innerHTML = "";

    if (!users || users.length === 0) {
        container.innerHTML = `
            <div class="text-muted small">
                No hay usuarios conectados.
            </div>
        `;
        return;
    }

    users.forEach(user => {

        const el = document.createElement("div");

        el.classList.add("online-user");

        el.innerHTML = `
            <span class="online-dot"></span>
            <span>${user.name}</span>
        `;

        container.appendChild(el);

    });
}


/* =========================================================
   AUDIT TIMELINE REALTIME
========================================================= */

function appendAuditToTimeline(data) {

    if (data.user_id === CURRENT_USER_ID) return;

    const timeline = document.querySelector(".timeline");

    if (!timeline) return;

    const date = new Date(data.created_at);

    const dayKey = date.toISOString().split("T")[0];

    const time = date.toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit"
    });

    let label = timeline.querySelector(
        `.time-label[data-date="${dayKey}"]`
    );

    // crear label si no existe
    if (!label) {

        const labelDiv = document.createElement("div");

        labelDiv.classList.add("time-label");

        labelDiv.setAttribute("data-date", dayKey);

        labelDiv.innerHTML = `
            <span class="bg-secondary">
                ${getDayLabel(date)}
            </span>
        `;

        timeline.prepend(labelDiv);

        label = labelDiv;
    }

    // item timeline
    const item = document.createElement("div");

    item.innerHTML = `
        <i class="fas ${getAuditIcon(data.action)} ${getAuditColor(data.action)}"></i>

        <div class="timeline-item highlight">

            <span class="time">
                <i class="fas fa-clock"></i>
                ${time}
            </span>

            <h3 class="timeline-header">
                <strong>${data.user}</strong>
            </h3>

            <div class="timeline-body">
                ${data.description}
            </div>

        </div>
    `;

    label.insertAdjacentElement(
        "afterend",
        item
    );

    setTimeout(() => {

        item.querySelector(".timeline-item")
            .classList.remove("highlight");

    }, 2000);

}


/* =========================================================
   ACTIVITY FEED REALTIME
========================================================= */

function prependFeedEvent(activity) {

    if (!activity) return;

    // evitar duplicados
    if (activity.feed_id) {

        const existing = document.querySelector(
            `[data-feed-id='${activity.feed_id}']`
        );

        if (existing) return;

    }

    const list = document.getElementById(
        "project-feed-list"
    );

    if (!list) return;

    const emptyState = list.querySelector(
        ".project-feed-empty"
    );

    if (emptyState) {
        emptyState.remove();
    }

    const item = document.createElement("div");

    item.classList.add(
        "feed-item",
        "feed-new"
    );

    if (activity.feed_id) {
        item.dataset.feedId = activity.feed_id;
    }

    item.innerHTML = `
        <div class="feed-icon ${getFeedColor(activity.event_type)}">
            <i class="fas ${getFeedIcon(activity.event_type)}"></i>
        </div>

        <div class="feed-content">

            <div class="feed-message">
                ${activity.message}
            </div>

            <div class="feed-date">
                <i class="far fa-clock mr-1"></i>
                ${formatFeedDate(activity.created_at)}
            </div>

        </div>
    `;

    list.prepend(item);

    setTimeout(() => {
        item.classList.remove("feed-new");
    }, 1800);

}

/* =========================================================
   KANBAN UI COUNTERS / EMPTY STATES
========================================================= */

function refreshKanbanUI() {

    document.querySelectorAll(".kanban-column").forEach(column => {

        const status = column.dataset.status;

        const tasks = column.querySelectorAll(".kanban-task");

        const count = tasks.length;

        updateKanbanCount(status, count);

        updateKanbanEmptyState(column, count);

    });

}

function updateKanbanCount(status, count) {

    const counter = document.querySelector(
        `.kanban-count[data-count-status='${status}']`
    );

    if (!counter) return;

    counter.textContent = count;

}

function updateKanbanEmptyState(column, count) {

    let empty = column.querySelector(".kanban-empty");

    if (count === 0) {

        if (!empty) {
            empty = document.createElement("div");

            empty.classList.add("kanban-empty");

            empty.innerHTML = `
                <i class="fas fa-inbox"></i>
                <span>Sin tareas</span>
            `;

            column.appendChild(empty);
        }

        return;
    }

    if (empty) {
        empty.remove();
    }

}

/* =========================================================
   HELPERS
========================================================= */

function getDayLabel(date) {

    const today = new Date();

    const yesterday = new Date();

    yesterday.setDate(today.getDate() - 1);

    const d = date.toDateString();

    if (d === today.toDateString()) return "Hoy";

    if (d === yesterday.toDateString()) return "Ayer";

    return date.toLocaleDateString();

}

function getAuditIcon(action) {

    const map = {
        "CREATE_TASK": "fa-plus-circle",
        "UPDATE_TASK": "fa-edit",
        "DELETE_TASK": "fa-trash",
        "TASK_STATUS_CHANGE": "fa-tasks"
    };

    return map[action] || "fa-info-circle";

}

function getAuditColor(action) {

    if (action.includes("DELETE")) {
        return "bg-danger";
    }

    if (action.includes("CREATE")) {
        return "bg-success";
    }

    if (action.includes("STATUS")) {
        return "bg-warning";
    }

    return "bg-primary";

}

function getFeedIcon(eventType) {

    const map = {

        TASK_CREATED: "fa-plus-circle",
        TASK_UPDATED: "fa-pen",
        TASK_DELETED: "fa-trash",
        TASK_STATUS_CHANGED: "fa-exchange-alt",

        ACTIVITY_CREATED: "fa-layer-group",
        ACTIVITY_UPDATED: "fa-pen-to-square",
        ACTIVITY_DELETED: "fa-trash",

        PROJECT_CREATED: "fa-diagram-project",
        PROJECT_UPDATED: "fa-diagram-project",
        PROJECT_DELETED: "fa-trash",

        MEMBER_JOINED: "fa-user-plus",
        MEMBER_REMOVED: "fa-user-minus"

    };

    return map[eventType] || "fa-info-circle";

}

function getFeedColor(eventType) {

    if (!eventType) {
        return "bg-secondary";
    }

    if (
        eventType.includes("DELETED") ||
        eventType.includes("REMOVED")
    ) {
        return "bg-danger";
    }

    if (
        eventType.includes("CREATED") ||
        eventType.includes("JOINED")
    ) {
        return "bg-success";
    }

    if (eventType.includes("STATUS")) {
        return "bg-warning";
    }

    if (eventType.includes("UPDATED")) {
        return "bg-primary";
    }

    return "bg-secondary";

}

function formatFeedDate(value) {

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