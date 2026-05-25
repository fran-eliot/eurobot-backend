CREATE TABLE notifications (
    id_notification INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,

    title VARCHAR(255),
    message TEXT,

    is_read BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id_user)
);

CREATE TABLE audit_logs (
    id_log INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT,

    action VARCHAR(100),
    resource_type VARCHAR(100),
    resource_id INT,

    description TEXT,

    ip_address VARCHAR(100),
    user_agent TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id_user)
);

CREATE TABLE activity_feed (
    id_feed INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT,
    project_id INT,

    event_type VARCHAR(100),
    description TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id_user),
    FOREIGN KEY (project_id) REFERENCES projects(id_project)
);