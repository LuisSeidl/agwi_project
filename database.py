import mariadb


def get_db_connection():
    try:
        connection = mariadb.connect(
            user="sel47223",
            password="sel47223",
            host="hera.hs-regensburg.de",
            database="sel47223",

        )
        return connection
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return None


#Next Functions are for inserting the Geschaeftsobjekte into my Database

def insert_fahrzeug(name, kategorie, leistung, stunden, gps_daten, frei, zustand, service, image_data):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """
        INSERT INTO Fahrzeug (name, kategorie, leistung, stunden, gps_daten, frei, zustand, service, image)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (name, kategorie, leistung, stunden, gps_daten, frei, zustand, service, image_data)
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()


def insert_feld(name, groesse, frucht, gps_daten, image_data):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO Feld (name, groesse, frucht, gps_daten, image)
        VALUES (%s, %s, %s, %s, %s)
    """
    values = (name, groesse, frucht, gps_daten, image_data)

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()


def insert_angestellter(name, email, passwort, ort, plz, strasse, hausnummer, image_data):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO Angestellter (name, email, passwort, ort, plz, strasse, hausnummer, image)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (name, email, passwort, ort, plz, strasse, hausnummer, image_data)
    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()


def insert_arbeitsart(name, zeitfaktor):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = """INSERT INTO Arbeitsart (name, zeitfaktor) VALUES (%s, %s)"""
    values = (name, zeitfaktor)
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()


def insert_auftrag(connection, cursor, angestellter_name, arbeitsort_gps, arbeitsart_name, fahrzeug_name):

    cursor.execute("SELECT id FROM Angestellter WHERE name = %s", (angestellter_name,))
    angestellter_id = cursor.fetchone()
    if angestellter_id:
        angestellter_id = angestellter_id[0]
    else:
        print("Angestellter not found!")
        return

    cursor.execute("SELECT id FROM Feld WHERE gps_daten = %s", (arbeitsort_gps,))
    arbeitsort_id = cursor.fetchone()
    if arbeitsort_id:
        arbeitsort_id = arbeitsort_id[0]
    else:
        print("Feld not found!")
        return

    cursor.execute("SELECT id FROM Arbeitsart WHERE name = %s", (arbeitsart_name,))
    arbeitsart_id = cursor.fetchone()
    if arbeitsart_id:
        arbeitsart_id = arbeitsart_id[0]
    else:
        print("Arbeitsart not found!")
        return

    cursor.execute("SELECT id FROM Fahrzeug WHERE name = %s", (fahrzeug_name,))
    fahrzeug_id = cursor.fetchone()
    if fahrzeug_id:
        fahrzeug_id = fahrzeug_id[0]
    else:
        print("Fahrzeug not found!")
        return

    query = """
        INSERT INTO Auftrag (angestellter_id, arbeitsort_id, arbeitsart_id, fahrzeug_id, status)
        VALUES (%s, %s, %s, %s, 'Unbearbeitet')
    """
    values = (angestellter_id, arbeitsort_id, arbeitsart_id, fahrzeug_id)
    cursor.execute(query, values)
    connection.commit()

    print("Auftrag successfully added!")


