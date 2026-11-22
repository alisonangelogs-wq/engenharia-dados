CREATE TABLE IF NOT EXISTS registros_jornada (
    employee_id VARCHAR(20) NOT NULL,
    work_date DATE NOT NULL,
    check_in TIME NOT NULL,
    lunch_out TIME NOT NULL,
    lunch_in TIME NOT NULL,
    check_out TIME NOT NULL,
    work_hours NUMERIC(5,2) NOT NULL,
    source_row INTEGER,
    loaded_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (employee_id, work_date)
);

CREATE TABLE IF NOT EXISTS registros_rejeitados (
    id BIGSERIAL PRIMARY KEY,
    employee_id VARCHAR(20),
    work_date DATE,
    source_row INTEGER NOT NULL,
    rejection_reason TEXT NOT NULL,
    raw_record JSONB NOT NULL,
    processed_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
