import pymysql

def connect_to_database():
    try:
        db = pymysql.connect(
            host="*****",
            user="root",
            password="*******",
            database="CRIMINALDB"
        )
        print("Connected to MySQL server")
        return db
    except pymysql.Error as e:
        print("Failed to connect to MySQL server:", e)
        return None

def disconnect_from_database(db):
    if db:
        db.close()
        print("Connection closed")

def insert_data(data):
    row_id = 0
    db = connect_to_database()
    if not db:
        return row_id  # Return 0 if unable to connect to the database

    try:
        with db.cursor() as cursor:
            query = "INSERT INTO criminaldata (Name, `Father's Name`, `Mother's Name`, Gender, DOB, `Blood Group`, `Identification Mark`, Nationality, Religion, `Crimes Done`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (
                data["Name"], data["Father's Name"], data["Mother's Name"], data["Gender"],
                data["DOB(yyyy-mm-dd)"], data["Blood Group"], data["Identification Mark"],
                data["Nationality"], data["Religion"], data["Crimes Done"]
            ))
            db.commit()
            row_id = cursor.lastrowid
            print("Data stored on row %d" % row_id)
    except pymysql.Error as e:
        db.rollback()
        print("Data insertion failed:", e)
        row_id = 0  # Set row_id to 0 in case of an error
    finally:
        disconnect_from_database(db)
    return row_id


def retrieve_data(name):
    id = None
    crim_data = None
    db = connect_to_database()
    if not db:
        return id, crim_data  # Return None if unable to connect to the database

    try:
        with db.cursor() as cursor:
            query = "SELECT * FROM criminaldata WHERE name=%s"
            cursor.execute(query, (name,))
            result = cursor.fetchone()
            if result:
                id = result[0]
                crim_data = {
                    "ID": result[0],
                    "Name": result[1],
                    "Father's Name": result[2],
                    "Mother's Name": result[3],
                    "Gender": result[4],
                    "DOB(yyyy-mm-dd)": result[5],
                    "Blood Group": result[6],
                    "Identification Mark": result[7],
                    "Nationality": result[8],
                    "Religion": result[9],
                    "Crimes Done": result[10]
                }

                print("Data retrieved")
            else:
                print("No data found for name:", name)
    except pymysql.Error as e:
        print("Error: Unable to fetch data:", e)
    finally:
        disconnect_from_database(db)
    return id, crim_data

def deleteData():
    return None


def updateData():
    return None

def fetch_all_criminal_data():
    criminal_records = []

    db = connect_to_database()
    if not db:
        return criminal_records  # Return an empty list if unable to connect to the database

    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM criminaldata")
            rows = cursor.fetchall()
            for row in rows:
                # Inside fetch_all_criminal_data() function
                # Inside fetch_all_criminal_data() function
                record = {
                    "id": row[0],
                    "name": row[1],
                    "father_name": row[2],
                    "mother_name": row[3],
                    "gender": row[4],
                    "dob": row[5],
                    "blood_group": row[6],
                    "identification_mark": row[7],
                    "nationality": row[8],
                    "religion": row[9],
                    "Crimes Done": row[10]  # Update to "Crimes Done"
                }

                criminal_records.append(record)
    except pymysql.Error as e:
        print("Error: Unable to fetch criminal data from database:", e)
    finally:
        disconnect_from_database(db)

    return criminal_records

# You can similarly define functions for other database operations

if __name__ == "__main__":
    # You can use this section for testing your functions
    pass

import pymysql

def deleteData(id):
    try:
        # Connect to the database
        db = connect_to_database()
        cursor = db.cursor()

        # Execute the delete query
        query = "DELETE FROM criminaldata WHERE id=%s"
        cursor.execute(query, (id,))
        db.commit()
        print("Data with ID %d deleted successfully." % id)
        return True  # Return True indicating successful deletion
    except Exception as e:
        db.rollback()
        print("Error: Unable to delete data")
        print("Exception:", e)
        return False  # Return False indicating deletion failure
    finally:
        db.close()

def update_data(id, new_data):
    try:
        # Connect to the database
        db = connect_to_database()

        cursor = db.cursor()
        query = """
            UPDATE criminaldata
            SET name=%s, father_name=%s, mother_name=%s, gender=%s, dob=%s,
                blood_group=%s, identification_mark=%s, nationality=%s, religion=%s, crimes_done=%s
            WHERE id=%s
        """
        cursor.execute(query, (
            id,
            new_data["Name"], new_data["Father's Name"], new_data["Mother's Name"],
            new_data["Gender"], new_data["DOB"], new_data["Blood Group"],
            new_data["Identification Mark"], new_data["Nationality"], new_data["Religion"],
            new_data["Crimes Done"]
        ))
        db.commit()
        print("Data with ID %s updated successfully." % str(id))
        return True
    except Exception as e:
        db.rollback()
        print("Error: Unable to update data:", e)
        return False
    finally:
        db.close()

# Remaining code...



import pymysql
def create_criminaldata_table():
    try:
        # Connect to MySQL
        db = pymysql.connect(
            host="localhost",
            user="root",
            password="mysql369963",
            database="CRIMINALDB"
        )
        cursor = db.cursor()
        print("Database connected")

        # SQL statement to create the criminaldata table
        create_table_query = """
            CREATE TABLE IF NOT EXISTS criminaldata (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                father_name VARCHAR(255),
                mother_name VARCHAR(255),
                gender VARCHAR(10),
                dob DATE,
                blood_group VARCHAR(10),
                identification_mark VARCHAR(255),
                nationality VARCHAR(50),
                religion VARCHAR(50),
                crimes_done VARCHAR(255)  -- Add this column definition
            )
        """

        cursor.execute(create_table_query)
        db.commit()
        print("Table 'criminaldata' created successfully.")

    except pymysql.Error as e:
        print("Error creating table:", e)

    finally:
        if db:
            db.close()
            print("Connection closed")


# Call the function to create the criminaldata table
create_criminaldata_table()
def modifyTableSchema():
    try:
        # Connect to MySQL
        db = pymysql.connect(
            host="localhost",
            user="root",
            password="*******",
            database="*******"
        )
        cursor = db.cursor()
        print("Database connected")

        # Alter table schema to change dob to DATE and crimes_done to VARCHAR(255)
        alter_query = """
            ALTER TABLE criminaldata 
            MODIFY COLUMN dob DATE,
            MODIFY COLUMN crimes_done VARCHAR(255);
        """
        cursor.execute(alter_query)
        db.commit()
        print("Table schema modified successfully.")
    except pymysql.Error as e:
        print("Error modifying table schema:", e)
    finally:
        if db:
            db.close()
            print("Connection closed")

# Call the function to modify the table schema
modifyTableSchema()



def display_all_names():
    db = connect_to_database()
    if not db:
        return  # Return if unable to connect to the database

    try:
        with db.cursor() as cursor:
            query = "SELECT name FROM criminaldata"
            cursor.execute(query)
            results = cursor.fetchall()
            print("List of names:")
            for result in results:
                print(result[0])
    except pymysql.Error as e:
        print("Error: Unable to fetch names:", e)
    finally:
        disconnect_from_database(db)


def fetch_officers():
    conn = connect_to_database()
    if not conn:
        return []

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM officers")
            officers = cursor.fetchall()
            return officers
    except pymysql.Error as e:
        print("Error fetching officers:", e)
        return []
    finally:
        if conn:
            conn.close()

def fetch_officer_info(officer_id):
    conn = connect_to_database()
    if not conn:
        return None

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM officers WHERE id = %s", (officer_id,))
            officer_info = cursor.fetchone()
            return officer_info
    except pymysql.Error as e:
        print("Error fetching officer info:", e)
        return None
    finally:
        if conn:
            conn.close()


def fetchAllData():
    return None
