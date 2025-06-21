
CREATE TABLE tenants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role_id INT,
    tenant_id INT,
    FOREIGN KEY (role_id) REFERENCES roles(id),
    FOREIGN KEY (tenant_id) REFERENCES tenants(id)
);

CREATE TABLE properties (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    description TEXT,
    tenant_id INT,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id)
);

CREATE TABLE clients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    ndis_number VARCHAR(50),
    property_id INT,
    tenant_id INT,
    FOREIGN KEY (property_id) REFERENCES properties(id),
    FOREIGN KEY (tenant_id) REFERENCES tenants(id)
);

CREATE TABLE rosters (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT,
    support_worker VARCHAR(255),
    start_time DATETIME,
    end_time DATETIME,
    shiftcare_id VARCHAR(100),
    tenant_id INT,
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (tenant_id) REFERENCES tenants(id)
);

CREATE TABLE timesheets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    roster_id INT,
    hours_worked DECIMAL(5,2),
    notes TEXT,
    xero_timesheet_id VARCHAR(100),
    tenant_id INT,
    FOREIGN KEY (roster_id) REFERENCES rosters(id),
    FOREIGN KEY (tenant_id) REFERENCES tenants(id)
);

CREATE TABLE invoices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT,
    amount DECIMAL(10,2),
    status VARCHAR(50),
    xero_invoice_id VARCHAR(100),
    issued_date DATE,
    due_date DATE,
    tenant_id INT,
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (tenant_id) REFERENCES tenants(id)
);

CREATE TABLE audit_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action VARCHAR(255),
    entity VARCHAR(50),
    entity_id INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    details TEXT,
    tenant_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (tenant_id) REFERENCES tenants(id)
);

-- Default tenant, role, and admin user
INSERT INTO tenants (id, name) VALUES (1, 'DefaultTenant');
INSERT INTO roles (id, name) VALUES (1, 'admin'), (2, 'support_worker'), (3, 'manager');
-- password: password
INSERT INTO users (id, username, password_hash, role_id, tenant_id) VALUES (1, 'admin', '$2b$12$w1Q8Qw6Qw6Qw6Qw6Qw6QwOQw6Qw6Qw6Qw6Qw6Qw6Qw6Qw6Qw6Qw6', 1, 1);
