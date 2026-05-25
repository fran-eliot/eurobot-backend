CREATE TABLE projects (
    id_project INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    status ENUM('active', 'paused', 'completed') DEFAULT 'active',
    duration_type ENUM('1_year', '3_years', 'indefinite'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE project_members (
    id_member INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    user_id INT NOT NULL,
    contextual_role ENUM('coordinator', 'member') DEFAULT 'member',

    FOREIGN KEY (project_id) REFERENCES projects(id_project),
    FOREIGN KEY (user_id) REFERENCES users(id_user)
);

CREATE TABLE tasks (
    id_task INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status ENUM('todo', 'doing', 'done') DEFAULT 'todo',
    priority ENUM('low', 'medium', 'high') DEFAULT 'medium',
    due_date DATE,

    project_id INT NOT NULL,
    assigned_to INT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (project_id) REFERENCES projects(id_project),
    FOREIGN KEY (assigned_to) REFERENCES users(id_user)
);

CREATE TABLE activities (
    id_activity INT AUTO_INCREMENT PRIMARY KEY,
    task_id INT NOT NULL,
    user_id INT NOT NULL,

    activity_type VARCHAR(100),
    description TEXT,
    time_spent INT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (task_id) REFERENCES tasks(id_task),
    FOREIGN KEY (user_id) REFERENCES users(id_user)
);

CREATE TABLE attachments (
    id_attachment INT AUTO_INCREMENT PRIMARY KEY,

    activity_id INT NOT NULL,
    uploaded_by INT NOT NULL,

    original_filename VARCHAR(255),
    stored_filename VARCHAR(255),
    mime_type VARCHAR(100),
    file_size BIGINT,

    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (activity_id) REFERENCES activities(id_activity),
    FOREIGN KEY (uploaded_by) REFERENCES users(id_user)
);