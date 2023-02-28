import csv
import mysql.connector

RESULT = []

class Weight:
    def __init__(self, first_name, date, weight):
        self.first_name = first_name
        self.date = date
        self.weight = weight

def populate_db():
    # Open a connection to the db
    cnx = mysql.connector.connect(user='root',
                                       port=3306,
                                       password='hcmfjkz14y91',
                                       host='192.168.1.183',
                                       database='weight_tracker')
    cursor = cnx.cursor()
    
    # Read the CSV file and insert its contents into the db
    with open('weight_data.csv') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            user_id = row[0]
            measured_at = row[1]
            weight = row[2]
            query = f"INSERT INTO user_weight (user_id, measured_at, weight) VALUES ({user_id}, str_to_date('{measured_at}', '%Y-%m-%dT%H:%i:%s.%fZ'), {weight})"
            print(query)
            cursor.execute(query)
            
    # Commit the changes and close the database connection
    cnx.commit()
    cursor.close()
    cnx.close()

def athlete_weights():
    RESULT = []

    with open('weight_data.csv') as fn:
        fr = csv.reader(fn)
        next(fr)
        RESULT = list(fr)
    
    return RESULT

def add_weight(weight):
    with open('weight_data.csv', mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(weight)

def remove_weight(weight):
    with open('weight_data.csv', mode="r") as file:
        reader = csv.reader(file)
        rows = [row for row in reader if row != weight]

    with open('weight_data.csv', mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

def change_weight(weight_before, weight_after):
    with open('weight_data.csv', mode="r") as file:
        reader = csv.reader(file)
        rows = []
        for row in reader:
            if int(row[1] == weight_before[1] and row[2] == weight_before[2]):
                row[2] = str(weight_after[2])
            rows.append(row)

    with open('weight_data.csv', mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

def change_date(date_before, date_after):
    with open('weight_data.csv', mode="r") as file:
        reader = csv.reader(file)
        rows = []
        for row in reader:
            if int(row[1] == date_before[1] and row[2] == date_before[2]):
                row[1] = str(date_after[1])
            rows.append(row)

    with open('weight_data.csv', mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)
        
#populate_db()