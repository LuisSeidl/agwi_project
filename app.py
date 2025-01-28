import os
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template, jsonify, redirect, url_for, flash
from database import *
from collections import namedtuple
import secrets




app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


@app.route('/add_mitarbeiter', methods=['POST'])
def add_mitarbeiter():
    if request.method == 'POST':

        name = request.form.get('name')
        email = request.form.get('email')
        passwort = request.form.get('passwort')
        ort = request.form.get('ort')
        plz = request.form.get('plz')
        strasse = request.form.get('strasse')
        hausnummer = request.form.get('hausnummer')
        image = request.files.get('image')

        if not (name and email and passwort and ort and plz and strasse and hausnummer and image):
            flash("All fields are required","error")
            return redirect(url_for('zeige_mitarbeiter'))


        image_filename = secure_filename(image.filename)
        image_path = f"images/{image_filename}"
        image.save(os.path.join('static', 'images', image_filename))

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            insert_angestellter(
                name=name,
                email=email,
                passwort=passwort,
                ort=ort,
                plz=plz,
                strasse=strasse,
                hausnummer=hausnummer,
                image_data=image_path)
            flash("Mitarbeiter successfully added!", "success")
        except Exception as e:
            flash(f"An error occured: {e}", "error")
        finally:
            cursor.close()
            connection.close()

        return redirect(url_for('zeige_mitarbeiter'))

@app.route('/add_fahrzeug', methods=['POST'])
def add_fahrzeug():
    if request.method == 'POST':
        name = request.form.get('name')
        kategorie = request.form.get('kategorie')
        leistung = request.form.get('leistung')
        stunden = request.form.get('stunden')
        gps_daten = request.form.get('gps_daten')
        zustand = request.form.get('zustand')
        image = request.files.get('image')

        if not (name and kategorie and leistung and stunden and gps_daten and zustand and image):
            flash("All fields are required!", "error")
            return redirect(url_for('zeige_fahrzeuge'))

        image_filename = secure_filename(image.filename)
        image_path = f"images/{image_filename}"
        image.save(os.path.join('static', 'images', image_filename))

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            insert_fahrzeug(
                name=name,
                kategorie=kategorie,
                leistung=int(leistung),
                stunden=float(stunden),
                gps_daten=gps_daten,
                frei=True,
                zustand=zustand,
                service=None,
                image_data=image_path
            )
            flash("Fahrzeug successfully added!", "success")
        except Exception as e:
            flash(f"An error occurred: {e}", "error")
        finally:
            cursor.close()
            connection.close()

        return redirect(url_for('zeige_fahrzeuge'))

@app.route('/add_feld', methods=['POST'])
def add_feld():
    if request.method == 'POST':
        name = request.form['name']
        groesse = request.form.get('groesse')
        frucht = request.form.get('frucht')
        gps_daten = request.form.get('gps_daten')
        image = request.files.get('image')

        if not (name and groesse and frucht and gps_daten and image):
            flash("All fields are required!", "error")
            return redirect(url_for('zeige_felder'))

        image_filename = secure_filename(image.filename)
        image_path = f"images/{image_filename}"
        image.save(os.path.join('static', 'images', image_filename))

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            insert_feld(
                name=name,
                groesse=float(groesse),
                frucht=frucht,
                gps_daten=gps_daten,
                image_data=image_path
            )
            flash("Feld successfully added!", "success")
        except Exception as e:
            flash(f"An error occured: {e}", "error")
        finally:
            cursor.close()
            connection.close()

        return redirect(url_for('zeige_felder'))

@app.route('/add_auftrag', methods=['POST'])
def add_auftrag():
    data = request.get_json()

    angestellter_id = data['angestellter_id']
    arbeitsort_id = data['arbeitsort_id']
    arbeitsart_id = data['arbeitsart_id']
    zeit = data['zeit']
    fahrzeug_id = data['fahrzeug_id']

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        query = """
            INSERT INTO Auftrag (angestellter_id, arbeitsort_id, arbeitsart_id, fahrzeug_id, zeit, status)
            VALUES (%s, %s, %s, %s, %s, 'Unbearbeitet')
        """
        cursor.execute(query, (angestellter_id, arbeitsort_id, arbeitsart_id, fahrzeug_id, zeit))
        connection.commit()

        print("Auftrag successfully added!")

        return jsonify({"message": "Auftrag successfully added!"}), 200

    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
        return jsonify({"error": f"Ein Fehler ist aufgetreten: {str(e)}"}), 500
    finally:
        cursor.close()
        connection.close()



@app.route('/')
def index():
    connection = get_db_connection()
    cursor = connection.cursor()

    Auftrag = namedtuple('Auftrag',
                         ['id', 'angestellter_name', 'arbeitsort_gps', 'arbeitsart_name', 'fahrzeug_name', 'status',
                          'zeit'])

    cursor.execute("""
        SELECT a.id, ang.name AS angestellter_name, f.gps_daten AS arbeitsort_gps, ar.name AS arbeitsart_name, fa.name AS fahrzeug_name, a.status, a.zeit
        FROM Auftrag a 
        JOIN Angestellter ang ON a.angestellter_id = ang.id 
        JOIN Feld f ON a.arbeitsort_id = f.id 
        JOIN Arbeitsart ar ON a.arbeitsart_id = ar.id 
        JOIN Fahrzeug fa ON a.fahrzeug_id = fa.id;
    """)
    auftraege = []

    for row in cursor.fetchall():
        auftrag = Auftrag(*row)
        if auftrag.zeit:
            formatted_date = auftrag.zeit.strftime('%d-%m-%Y')
            formatted_time = auftrag.zeit.strftime('%H:%M')
        else:
            formatted_date = None
            formatted_time = None

        auftraege.append({
            'id': auftrag.id,
            'angestellter_name': auftrag.angestellter_name,
            'arbeitsort_gps': auftrag.arbeitsort_gps,
            'arbeitsart_name': auftrag.arbeitsart_name,
            'fahrzeug_name': auftrag.fahrzeug_name,
            'status': auftrag.status,
            'zeit': auftrag.zeit,
            'formatted_date': formatted_date,
            'formatted_time': formatted_time
        })

    cursor.execute("SELECT id, name FROM Angestellter")
    angestellte = cursor.fetchall()

    cursor.execute("SELECT id, gps_daten FROM Feld")
    arbeitsorte = cursor.fetchall()

    cursor.execute("SELECT id, name FROM Arbeitsart")
    arbeitsarten = cursor.fetchall()

    cursor.execute("SELECT id, name FROM Fahrzeug")
    fahrzeuge = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('smartfarm.html', auftraege=auftraege, angestellte=angestellte, arbeitsorte=arbeitsorte,
                           arbeitsarten=arbeitsarten, fahrzeuge=fahrzeuge)

@app.route('/update_status/<int:auftrag_id>', methods=['POST'])
def update_status(auftrag_id):
    new_status = request.json.get('status')
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE Auftrag SET status = %s WHERE id = %s", (new_status, auftrag_id))
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify(success=True)
    except Exception as e:
        print(f"Error updating status: {e}")
        return jsonify(success=False)

@app.route('/get_auftrag/<int:auftrag_id>', methods=['GET'])
def get_auftrag(auftrag_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
        SELECT angestellter_id, arbeitsort_id, arbeitsart_id, fahrzeug_id, zeit
        FROM Auftrag
        WHERE id = %s
    """
    cursor.execute(query, (auftrag_id,))
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    if row:
        zeit_iso = row[4].isoformat() if row[4] else None
        return jsonify({
            'angestellter_id': row[0],
            'arbeitsort_id': row[1],
            'arbeitsart_id': row[2],
            'fahrzeug_id': row[3],
            'zeit': zeit_iso
        })
    else:
        return jsonify({"error": "Auftrag not found"}), 404


@app.route('/update_auftrag/<int:auftrag_id>', methods=['POST'])
def update_auftrag(auftrag_id):
    data = request.json
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
        UPDATE Auftrag
        SET angestellter_id = %s, arbeitsort_id = %s, arbeitsart_id = %s, fahrzeug_id = %s, zeit = %s
        WHERE id = %s
    """
    try:
        cursor.execute(query, (data['angestellter_id'], data['arbeitsort_id'], data['arbeitsart_id'],
                               data['fahrzeug_id'], data['zeit'], auftrag_id))
        connection.commit()
        return jsonify({"success": True})
    except Exception as e:
        connection.rollback()
        return jsonify({"success": False, "error": str(e)})
    finally:
        cursor.close()
        connection.close()

@app.route('/delete_auftrag/<int:auftrag_id>', methods=['DELETE'])
def delete_auftrag(auftrag_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM Auftrag WHERE id = %s", (auftrag_id,))
        connection.commit()
        return jsonify({"success": True})
    except Exception as e:
        connection.rollback()
        return jsonify({"success": False, "error": str(e)})
    finally:
        cursor.close()
        connection.close()



@app.route('/fuhrpark')
def zeige_fahrzeuge():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, kategorie, leistung, gps_daten, frei, zustand, service, image FROM Fahrzeug")
    fahrzeuge = cursor.fetchall()

    fahrzeuge_list = []

    for fahrzeug in fahrzeuge:
        image_path = fahrzeug[8]


        fahrzeug_data = {
            'id': fahrzeug[0],
            'name': fahrzeug[1],
            'kategorie': fahrzeug[2],
            'leistung': fahrzeug[3],
            'gps_daten': fahrzeug[4],
            'frei': fahrzeug[5],
            'zustand': fahrzeug[6],
            'service': fahrzeug[7],
            'image': image_path
        }
        fahrzeuge_list.append(fahrzeug_data)

    cursor.close()
    connection.close()

    return render_template('Fuhrpark.html', fahrzeuge=fahrzeuge_list)

@app.route('/get_fahrzeug/<int:fahrzeug_id>', methods=['GET'])
def get_fahrzeug(fahrzeug_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Fahrzeug WHERE id = %s", (fahrzeug_id,))
    fahrzeug = cursor.fetchone()
    cursor.close()
    connection.close()
    if fahrzeug:
        return jsonify(fahrzeug)
    return jsonify({"error": "Fahrzeug not found"}), 404

@app.route('/update_fahrzeug/<int:fahrzeug_id>', methods=['POST'])
def update_fahrzeug(fahrzeug_id):
    data = request.json
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
        UPDATE Fahrzeug
        SET name = %s, kategorie = %s, leistung = %s, stunden = %s, gps_daten = %s, zustand = %s
        WHERE id = %s
    """
    cursor.execute(query, (data['name'], data['kategorie'], data['leistung'], data['stunden'], data['gps_daten'], data['zustand'], fahrzeug_id))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Fahrzeug erfolgreich geändert!"})

@app.route('/delete_fahrzeug/<int:fahrzeug_id>', methods=['DELETE'])
def delete_fahrzeug(fahrzeug_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Fahrzeug WHERE id = %s", (fahrzeug_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Fahrzeug erfolgreich gelöscht!"})



@app.route('/mitarbeiter')
def zeige_mitarbeiter():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, email, ort, plz, strasse, hausnummer, image FROM Angestellter")
    mitarbeiter = cursor.fetchall()


    mitarbeiter_list = []
    for mitarbeiter in mitarbeiter:
        image_path = mitarbeiter[7]

        mitarbeiter_data = {
            'id': mitarbeiter[0],
            'name': mitarbeiter[1],
            'email': mitarbeiter[2],
            'ort': mitarbeiter[3],
            'plz': mitarbeiter[4],
            'strasse': mitarbeiter[5],
            'hausnummer': mitarbeiter[6],
            'image': image_path
        }
        mitarbeiter_list.append(mitarbeiter_data)

    cursor.close()
    connection.close()

    return render_template('Mitarbeiter.html', mitarbeiter=mitarbeiter_list)

@app.route('/get_mitarbeiter/<int:mitarbeiter_id>', methods=['GET'])
def get_mitarbeiter(mitarbeiter_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Angestellter WHERE id = %s", (mitarbeiter_id,))
    mitarbeiter = cursor.fetchone()
    cursor.close()
    connection.close()
    if mitarbeiter:
        return jsonify(mitarbeiter)
    return jsonify({"error": "Mitarbeiter not found"}), 404

@app.route('/update_mitarbeiter/<int:mitarbeiter_id>', methods=['POST'])
def update_mitarbeiter(mitarbeiter_id):
    data = request.json
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
        UPDATE Angestellter
        SET name = %s, email = %s, ort = %s, plz = %s, strasse = %s, hausnummer = %s
        WHERE id = %s
    """
    cursor.execute(query, (data['name'], data['email'], data['ort'], data['plz'], data['strasse'], data['hausnummer'], mitarbeiter_id))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Mitarbeiter erfolgreich geändert!"})

@app.route('/delete_mitarbeiter/<int:mitarbeiter_id>', methods=['DELETE'])
def delete_mitarbeiter(mitarbeiter_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Angestellter WHERE id = %s", (mitarbeiter_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Mitarbeiter erfolgreich gelöscht!"})



@app.route('/felder')
def zeige_felder():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, groesse, frucht, gps_daten, image FROM Feld")
    felder = cursor.fetchall()


    felder_list = []
    for feld in felder:
        image_path = feld[4]

        feld_data = {
            'id': feld[0],
            'groesse': feld[1],
            'frucht': feld[2],
            'gps_daten': feld[3],
            'image': image_path
        }
        felder_list.append(feld_data)

    cursor.close()
    connection.close()

    return render_template('felder.html', felder=felder_list)

@app.route('/get_feld/<int:feld_id>', methods=['GET'])
def get_feld(feld_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Feld WHERE id = %s", (feld_id,))
    feld = cursor.fetchone()
    cursor.close()
    connection.close()
    if feld:
        return jsonify(feld)
    return jsonify({"error": "Feld not found"}), 404

@app.route('/update_feld/<int:feld_id>', methods=['POST'])
def update_feld(feld_id):
    data = request.json
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
        UPDATE Feld
        SET groesse = %s, frucht = %s, gps_daten = %s
        WHERE id = %s
    """
    cursor.execute(query, (data['groesse'], data['frucht'], data['gps_daten'],feld_id))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Feld erfolgreich geändert!"})

@app.route('/delete_feld/<int:feld_id>', methods=['DELETE'])
def delete_feld(feld_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Feld WHERE id = %s", (feld_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Feld erfolgreich gelöscht!"})



@app.route('/register')
def zeige_register():
    return render_template('register.html')
@app.route('/settings')
def zeige_settings():
    return render_template('settings.html')

if __name__ == '__main__':
    app.run(debug=True)
