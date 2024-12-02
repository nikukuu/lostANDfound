from flask import Blueprint, render_template, redirect, url_for, flash, session, request
import mysql.connector
from werkzeug.security import check_password_hash, generate_password_hash

admin_bp = Blueprint('admin', __name__, template_folder='../templates')

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='lost_and_found'
    )
    return connection

#----------------------------ADMIN---LOGIN----------------------------------------------------------------------------


@admin_bp.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Connect to the database
        connection = get_db_connection()
        cursor = connection.cursor()

        # Query the admin credentials
        cursor.execute("SELECT username, password FROM admin_info WHERE id = 1")
        admin = cursor.fetchone()  # Fetch the first row (since only one admin exists)
        cursor.close()
        connection.close()

        if admin and admin[0] == username and check_password_hash(admin[1], password):
            session['admin_logged_in'] = True  # Set a session variable
            return redirect(url_for('admin.admin_dashboard'))  # Redirect to the admin dashboard
        else:
            flash('Invalid username or password', 'danger')

    return render_template('admin_login.html')

@admin_bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('admin_login'))

@admin_bp.route('/admin_account', methods=['GET', 'POST'])
def admin_account():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    success_message = None
    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']

        # Validate inputs
        if len(new_username.strip()) == 0 or len(new_username) > 100:
            flash("Invalid username. Must be 1-100 characters.", 'danger')
        elif len(new_password.strip()) < 6:
            flash("Password must be at least 6 characters.", 'danger')
        else:
            # Update the credentials in the database
            hashed_password = generate_password_hash(new_password)
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE admin_info SET username = %s, password = %s WHERE id = 1",
                (new_username, hashed_password)
            )
            connection.commit()
            cursor.close()
            connection.close()

            success_message = "Admin credentials updated successfully!"

    return render_template('admin_account.html', success_message=success_message)


#--------------------------ADMIN---DASHBOARD--------------------------------------------


@admin_bp.route('/admin_dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM items WHERE status = 'pending'")
    pending_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM items WHERE status = 'published'")
    published_count = cursor.fetchone()[0]
    cursor.close()
    connection.close()

    return render_template(
        'admin_dashboard.html',
        pending_count=pending_count,
        published_count=published_count
    )


#---------------------ITEMS------------------------------------------------------------------------------


@admin_bp.route('/admin_items')
def admin_items():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch all items, ordering by date_created in descending order (latest first)
    cursor.execute("""
        SELECT id, date_found, item_name, description, status 
        FROM items 
        ORDER BY date_found DESC, id ASC
    """)
    items = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('admin_items.html', items=items)

@admin_bp.route('/admin/claims')
def admin_claims():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.admin_login'))

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, item_id, claimer_name, contact_info, status, message FROM claims")
    claims = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('admin_claims.html', claims=claims)

@admin_bp.route('/admin/confirm_claim/<int:claim_id>', methods=['POST'])
def confirm_claim(claim_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.admin_login'))

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Update claim status to 'confirmed'
        cursor.execute("UPDATE claims SET status = 'confirmed' WHERE id = %s", (claim_id,))
        connection.commit()
        flash('Claim confirmed successfully!', 'success')
    except Exception as e:
        connection.rollback()
        flash(f'Error confirming claim: {e}', 'danger')
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('admin.admin_claims'))

@admin_bp.route('/edit_item/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    connection = get_db_connection()
    cursor = connection.cursor()

    if request.method == 'POST':
        # Get updated details from the form
        item_name = request.form['name']  # Match form field with table field
        description = request.form['description']
        status = request.form['status']

        # Update the item in the database
        cursor.execute("""
            UPDATE items
            SET item_name = %s, description = %s, status = %s
            WHERE id = %s
        """, (item_name, description, status, item_id))
        connection.commit()

        cursor.close()
        connection.close()
        flash('Item updated successfully!', 'success')
        return redirect(url_for('admin.admin_items'))

    # For GET: Fetch the current details of the item
    cursor.execute("""
        SELECT id, item_name, description, status 
        FROM items 
        WHERE id = %s
    """, (item_id,))
    item = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template('edit_item.html', item=item)

@admin_bp.route('/delete_item/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Delete the item from the database
        cursor.execute("DELETE FROM items WHERE id = %s", (item_id,))
        connection.commit()

        flash('Item deleted successfully!', 'success')
    except Exception as e:
        connection.rollback()
        flash(f'Error deleting item: {e}', 'danger')
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('admin.admin_items'))