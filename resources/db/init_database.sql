
CREATE TABLE "user" (
    id UUID NOT NULL,
    name TEXT NOT NULL,
    login VARCHAR(100) NOT NULL UNIQUE,
    password TEXT NOT NULL,

    PRIMARY KEY (id)
);

CREATE TABLE workspace (
    id UUID NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMP NULL DEFAULT NULL,
    created_by UUID NOT NULL,
    updated_by UUID NOT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (created_by) REFERENCES "user"(id),
    FOREIGN KEY (updated_by) REFERENCES "user"(id)
);

CREATE TABLE workspace_has_user (
    workspace_id UUID NOT NULL,
    user_id UUID NOT NULL,

    PRIMARY KEY (workspace_id, user_id),
    FOREIGN KEY (workspace_id) REFERENCES workspace(id),
    FOREIGN KEY (user_id) REFERENCES "user"(id)
);

CREATE TABLE project (
    id UUID NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMP NULL DEFAULT NULL,
    created_by UUID NOT NULL,
    updated_by UUID NOT NULL,
    workspace_id UUID NOT NULL,
    budget FLOAT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (created_by) REFERENCES "user"(id),
    FOREIGN KEY (updated_by) REFERENCES "user"(id),
    FOREIGN KEY (workspace_id) REFERENCES workspace(id)
);

CREATE TABLE item (
    id UUID NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMP NULL DEFAULT NULL,
    created_by UUID NOT NULL,
    updated_by UUID NOT NULL,
    workspace_id UUID NOT NULL,
    unit_of_measurement TEXT NOT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (created_by) REFERENCES "user"(id),
    FOREIGN KEY (updated_by) REFERENCES "user"(id),
    FOREIGN KEY (workspace_id) REFERENCES workspace(id)
);

CREATE TABLE expense (
    id UUID NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMP NULL DEFAULT NULL,
    created_by UUID NOT NULL,
    updated_by UUID NOT NULL,
    workspace_id UUID NOT NULL,
    expense_type VARCHAR(100) NOT NULL,
    expense_class VARCHAR(100) NOT NULL,
    value FLOAT NOT NULL,
    notes TEXT NULL,
    project_id UUID NOT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (created_by) REFERENCES "user"(id),
    FOREIGN KEY (updated_by) REFERENCES "user"(id),
    FOREIGN KEY (workspace_id) REFERENCES workspace(id),
    FOREIGN KEY (project_id) REFERENCES project(id)
);

CREATE TABLE expense_has_item (
    expense_id UUID NOT NULL,
    item_id UUID NOT NULL,

    PRIMARY KEY (expense_id, item_id),
    FOREIGN KEY (expense_id) REFERENCES expense(id),
    FOREIGN KEY (item_id) REFERENCES item(id)
);

CREATE TABLE task (
    id UUID NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMP NULL DEFAULT NULL,
    created_by UUID NOT NULL,
    updated_by UUID NOT NULL,
    workspace_id UUID NOT NULL,
    planned_start_date TIMESTAMP NULL,
    planned_end_date TIMESTAMP NULL,
    actual_start_date TIMESTAMP NULL,
    actual_end_date TIMESTAMP NULL,
    status VARCHAR(100) NOT NULL,
    progress FLOAT NOT NULL,
    project_id UUID NOT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (created_by) REFERENCES "user"(id),
    FOREIGN KEY (updated_by) REFERENCES "user"(id),
    FOREIGN KEY (workspace_id) REFERENCES workspace(id),
    FOREIGN KEY (project_id) REFERENCES project(id)
);

CREATE TABLE task_history (
    id UUID NOT NULL,
    task_id UUID NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by UUID NOT NULL,
    progress FLOAT NOT NULL,
    notes TEXT NULL,
    status VARCHAR(100) NOT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (task_id) REFERENCES task(id),
    FOREIGN KEY (created_by) REFERENCES "user"(id)
);

CREATE TABLE file_document (
    id UUID NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMP NULL DEFAULT NULL,
    created_by UUID NOT NULL,
    updated_by UUID NOT NULL,
    workspace_id UUID NOT NULL,
    file_type VARCHAR(100) NOT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (created_by) REFERENCES "user"(id),
    FOREIGN KEY (updated_by) REFERENCES "user"(id),
    FOREIGN KEY (workspace_id) REFERENCES workspace(id)
);