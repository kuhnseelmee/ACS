
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from db import get_db
from audit import log_audit
from auth import role_required

bp = Blueprint('api', __name__)

def get_tenant_id():
    return get_jwt()['tenant_id']

def get_user_id():
    return get_jwt_identity()

# Properties CRUD
@bp.route('/properties', methods=['GET', 'POST'])
@jwt_required()
def properties():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    tenant_id = get_tenant_id()
    if request.method == 'POST':
        data = request.json
        cursor.execute("INSERT INTO properties (name, address, description, tenant_id) VALUES (%s, %s, %s, %s)",
                       (data['name'], data.get('address', ''), data.get('description', ''), tenant_id))
        db.commit()
        prop_id = cursor.lastrowid
        log_audit(get_user_id(), 'create', 'property', prop_id, str(data), tenant_id)
        return jsonify({'status': 'created', 'id': prop_id}), 201
    cursor.execute("SELECT * FROM properties WHERE tenant_id=%s", (tenant_id,))
    return jsonify(cursor.fetchall())

@bp.route('/properties/<int:property_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def property_detail(property_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    tenant_id = get_tenant_id()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM properties WHERE id=%s AND tenant_id=%s", (property_id, tenant_id))
        return jsonify(cursor.fetchone())
    elif request.method == 'PUT':
        data = request.json
        cursor.execute("UPDATE properties SET name=%s, address=%s, description=%s WHERE id=%s AND tenant_id=%s",
                       (data['name'], data.get('address', ''), data.get('description', ''), property_id, tenant_id))
        db.commit()
        log_audit(get_user_id(), 'update', 'property', property_id, str(data), tenant_id)
        return jsonify({'status': 'updated'})
    elif request.method == 'DELETE':
        cursor.execute("DELETE FROM properties WHERE id=%s AND tenant_id=%s", (property_id, tenant_id))
        db.commit()
        log_audit(get_user_id(), 'delete', 'property', property_id, '', tenant_id)
        return jsonify({'status': 'deleted'})

# Clients CRUD
@bp.route('/clients', methods=['GET', 'POST'])
@jwt_required()
def clients():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    tenant_id = get_tenant_id()
    if request.method == 'POST':
        data = request.json
        cursor.execute("INSERT INTO clients (name, email, phone, ndis_number, property_id, tenant_id) VALUES (%s, %s, %s, %s, %s, %s)",
                       (data['name'], data.get('email', ''), data.get('phone', ''), data.get('ndis_number', ''), data.get('property_id'), tenant_id))
        db.commit()
        client_id = cursor.lastrowid
        log_audit(get_user_id(), 'create', 'client', client_id, str(data), tenant_id)
        return jsonify({'status': 'created', 'id': client_id}), 201
    cursor.execute("SELECT * FROM clients WHERE tenant_id=%s", (tenant_id,))
    return jsonify(cursor.fetchall())

@bp.route('/clients/<int:client_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def client_detail(client_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    tenant_id = get_tenant_id()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM clients WHERE id=%s AND tenant_id=%s", (client_id, tenant_id))
        return jsonify(cursor.fetchone())
    elif request.method == 'PUT':
        data = request.json
        cursor.execute("UPDATE clients SET name=%s, email=%s, phone=%s, ndis_number=%s, property_id=%s WHERE id=%s AND tenant_id=%s",
                       (data['name'], data.get('email', ''), data.get('phone', ''), data.get('ndis_number', ''), data.get('property_id'), client_id, tenant_id))
        db.commit()
        log_audit(get_user_id(), 'update', 'client', client_id, str(data), tenant_id)
        return jsonify({'status': 'updated'})
    elif request.method == 'DELETE':
        cursor.execute("DELETE FROM clients WHERE id=%s AND tenant_id=%s", (client_id, tenant_id))
        db.commit()
        log_audit(get_user_id(), 'delete', 'client', client_id, '', tenant_id)
        return jsonify({'status': 'deleted'})

# Rosters CRUD
@bp.route('/rosters', methods=['GET', 'POST'])
@jwt_required()
def rosters():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    tenant_id = get_tenant_id()
    if request.method == 'POST':
        data = request.json
        cursor.execute("INSERT INTO rosters (client_id, support_worker, start_time, end_time, shiftcare_id, tenant_id) VALUES (%s, %s, %s, %s, %s, %s)",
                       (data['client_id'], data.get('support_worker', ''), data.get('start_time'), data.get('end_time'), data.get('shiftcare_id', ''), tenant_id))
        db.commit()
        roster_id = cursor.lastrowid
        log_audit(get_user_id(), 'create', 'roster', roster_id, str(data), tenant_id)
        return jsonify({'status': 'created', 'id': roster_id}), 201
    cursor.execute("SELECT * FROM rosters WHERE tenant_id=%s", (tenant_id,))
    return jsonify(cursor.fetchall())

@bp.route('/rosters/<int:roster_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def roster_detail(roster_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    tenant_id = get_tenant_id()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM rosters WHERE id=%s AND tenant_id=%s", (roster_id, tenant_id))
        return jsonify(cursor.fetchone())
    elif request.method == 'PUT':
        data = request.json
        cursor.execute("UPDATE rosters SET client_id=%s, support_worker=%s, start_time=%s, end_time=%s, shiftcare_id=%s WHERE id=%s AND tenant_id=%s",
                       (data['client_id'], data.get('support_worker', ''), data.get('start_time'), data.get('end_time'), data.get('shiftcare_id', ''), roster_id, tenant_id))
        db.commit()
        log_audit(get_user_id(), 'update', 'roster', roster_id, str(data), tenant_id)
        return jsonify({'status': 'updated'})
    elif request.method == 'DELETE':
        cursor.execute("DELETE FROM rosters WHERE id=%s AND tenant_id=%s", (roster_id, tenant_id))
        db.commit()
        log_audit(get_user_id(), 'delete', 'roster', roster_id, '', tenant_id)
        return jsonify({'status': 'deleted'})

# Timesheets CRUD
@bp.route('/timesheets', methods=['GET', 'POST'])
@jwt_required()
def timesheets():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    tenant_id = get_tenant_id()
    if request.method == 'POST':
        data = request.json
        cursor.execute("INSERT INTO timesheets (roster_id, hours_worked, notes, xero_timesheet_id, tenant_id) VALUES (%s, %s, %s, %s, %s)",
                       (data['roster_id'], data.get('hours_worked', 0), data.get('notes', ''), data.get('xero_timesheet_id', ''), tenant_id))
        db.commit()
        timesheet_id = cursor.lastrowid
        log_audit(get_user_id(), 'create', 'timesheet', timesheet_id, str(data), tenant_id)
        return jsonify({'status': 'created', 'id': timesheet_id}), 201
    cursor.execute("SELECT * FROM timesheets WHERE tenant_id=%s", (tenant_id,))
    return jsonify(cursor.fetchall())

@bp.route('/timesheets/<int:timesheet_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def timesheet_detail(timesheet_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    tenant_id = get_tenant_id()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM timesheets WHERE id=%s AND tenant_id=%s", (timesheet_id, tenant_id))
        return jsonify(cursor.fetchone())
    elif request.method == 'PUT':
        data = request.json
        cursor.execute("UPDATE timesheets SET roster_id=%s, hours_worked=%s, notes=%s, xero_timesheet_id=%s WHERE id=%s AND tenant_id=%s",
                       (data['roster_id'], data.get('hours_worked', 0), data.get('notes', ''), data.get('xero_timesheet_id', ''), timesheet_id, tenant_id))
        db.commit()
        log_audit(get_user_id(), 'update', 'timesheet', timesheet_id, str(data), tenant_id)
        return jsonify({'status': 'updated'})
    elif request.method == 'DELETE':
        cursor.execute("DELETE FROM timesheets WHERE id=%s AND tenant_id=%s", (timesheet_id, tenant_id))
        db.commit()
        log_audit(get_user_id(), 'delete', 'timesheet', timesheet_id, '', tenant_id)
        return jsonify({'status': 'deleted'})

# Invoices CRUD
@bp.route('/invoices', methods=['GET', 'POST'])
@jwt_required()
def invoices():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    tenant_id = get_tenant_id()
    if request.method == 'POST':
        data = request.json
        cursor.execute("INSERT INTO invoices (client_id, amount, status, xero_invoice_id, issued_date, due_date, tenant_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (data['client_id'], data.get('amount', 0), data.get('status', ''), data.get('xero_invoice_id', ''), data.get('issued_date'), data.get('due_date'), tenant_id))
        db.commit()
        invoice_id = cursor.lastrowid
        log_audit(get_user_id(), 'create', 'invoice', invoice_id, str(data), tenant_id)
        return jsonify({'status': 'created', 'id': invoice_id}), 201
    cursor.execute("SELECT * FROM invoices WHERE tenant_id=%s", (tenant_id,))
    return jsonify(cursor.fetchall())

@bp.route('/invoices/<int:invoice_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def invoice_detail(invoice_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    tenant_id = get_tenant_id()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM invoices WHERE id=%s AND tenant_id=%s", (invoice_id, tenant_id))
        return jsonify(cursor.fetchone())
    elif request.method == 'PUT':
        data = request.json
        cursor.execute("UPDATE invoices SET client_id=%s, amount=%s, status=%s, xero_invoice_id=%s, issued_date=%s, due_date=%s WHERE id=%s AND tenant_id=%s",
                       (data['client_id'], data.get('amount', 0), data.get('status', ''), data.get('xero_invoice_id', ''), data.get('issued_date'), data.get('due_date'), invoice_id, tenant_id))
        db.commit()
        log_audit(get_user_id(), 'update', 'invoice', invoice_id, str(data), tenant_id)
        return jsonify({'status': 'updated'})
    elif request.method == 'DELETE':
        cursor.execute("DELETE FROM invoices WHERE id=%s AND tenant_id=%s", (invoice_id, tenant_id))
        db.commit()
        log_audit(get_user_id(), 'delete', 'invoice', invoice_id, '', tenant_id)
        return jsonify({'status': 'deleted'})

# Audit log endpoint (admin only)
@bp.route('/audit', methods=['GET'])
@jwt_required()
@role_required('admin')
def audit_logs():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    tenant_id = get_tenant_id()
    cursor.execute("SELECT * FROM audit_logs WHERE tenant_id=%s ORDER BY timestamp DESC LIMIT 100", (tenant_id,))
    return jsonify(cursor.fetchall())
