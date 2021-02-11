import mysql.connector
import os

from dotenv import load_dotenv

load_dotenv()

mydb = mysql.connector.connect(
    host=os.getenv("HOST"),
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD"),
    database=os.getenv("DATABASE"))


def user_exists(id):
    cursor = mydb.cursor()
    cursor.execute("SELECT COUNT(*) FROM Userdata WHERE ID = (%s)", (id,))
    data = cursor.fetchone()[0]
    if data == 0:
        return False
    elif data == 1:
        return True
    cursor.close


def create_table():
    cursor = mydb.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Userdata (ID VARCHAR(100), PUUID VARCHAR(100), Name VARCHAR(100), Tag VARCHAR("
        "100), Role VARCHAR(100))")
    mydb.commit()
    cursor.close


def insert_userdata(id, valPUUID, valName, valTag, rank):
    cursor = mydb.cursor()
    if not user_exists(id):
        qry = "INSERT INTO Userdata (ID, PUUID, Name, Tag, Role) VALUES (%s, %s, %s, %s, %s)"
        val = (id, valPUUID, valName, valTag, rank.name)
        cursor.execute(qry, val)
        mydb.commit()
        return True
    else:
        return False
    cursor.close


def update_rank(id, rank):
    cursor = mydb.cursor()
    if user_exists(id):
        qry = "UPDATE Userdata SET Role = %s WHERE ID = %s"
        val = (rank.name, id)
        cursor.execute(qry, val)
        mydb.commit()
    cursor.close


def update_name(id, name):
    cursor = mydb.cursor()
    if user_exists(id):
        qry = "UPDATE Userdata SET Name = %s WHERE ID = %s"
        val = (name, id)
        cursor.execute(qry, val)
        mydb.commit()
    cursor.close


def update_tag(id, tag):
    cursor = mydb.cursor()
    if user_exists(id):
        qry = "UPDATE Userdata SET Tag = %s WHERE ID = %s"
        val = (tag, id)
        cursor.execute(qry, val)
        mydb.commit()
    cursor.close


def get_puuid(id):
    cursor = mydb.cursor()

    cursor.execute("SELECT PUUID FROM Userdata WHERE ID = (%s)", (id,))
    result = cursor.fetchone()[0]

    return result
    cursor.close


def get_name(id):
    cursor = mydb.cursor()
    if user_exists(id):
        cursor.execute("SELECT Name FROM Userdata WHERE ID = (%s)", (id,))
        result = cursor.fetchone()[0]

        return result
    cursor.close


def get_rank(id):
    cursor = mydb.cursor()
    if user_exists(id):
        cursor.execute("SELECT Role FROM Userdata WHERE ID = (%s)", (id,))
        result = cursor.fetchone()[0]

        return result
    cursor.close


def delete_user(id):
    cursor = mydb.cursor()
    if user_exists(id):
        cursor.execute("DELETE FROM Userdata WHERE ID = (%s)", (id,))
        mydb.commit()
        print("User with ID " + str(id) + " deleted")
    cursor.close
