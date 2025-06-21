
from db import get_db

def log_audit(user_id, action, entity, entity_id, details, tenant_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO audit_logs (user_id, action, entity, entity_id, details, tenant_id) VALUES (%s, %s, %s, %s, %s, %s)",
        (user_id, action, entity, entity_id, details, tenant_id)
    )
    db.commit()
