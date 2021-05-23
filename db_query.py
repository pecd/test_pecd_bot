import mysql.connector
import config_data

def db_credentials():
    credentials = mysql.connector.connect(
            host=config_data.db_config['host'],
            user=config_data.db_config['user'],
            passwd=config_data.db_config['passwd'],
            database=config_data.db_config['database']
        )

    return credentials

def db_connect():

    try:
        db = db_credentials()
        if db.is_connected():
            print('Connected to MySQL BD')
        db.close()

    except mysql.connector.Error as error_message:
        print(error_message)

def db_table_rec_check(user_id):

    try:
        db = db_credentials()
        output = ''
        if db.is_connected():
            mycursor = db.cursor()

            query = 'SELECT user_id FROM messages WHERE user_id = ' + str(user_id)

            mycursor.execute(query)

            for x in mycursor:
                output += str(x[0])

        db.close()
        if output != '':
            return True
        else:
            return False

    except mysql.connector.Error as error_message:
        print(error_message)


def db_input_message(user_id, user_name, user_message):

    try:
        db = db_credentials()
        if db.is_connected():
            print(db_table_rec_check(user_id))
            if db_table_rec_check(user_id):
                mycursor = db.cursor()

                query = f'UPDATE messages SET message_datetime = CURRENT_TIMESTAMP(), user_message = "{str(user_message)}" WHERE user_id = {user_id}'

                mycursor.execute(query)
                db.commit()

            else:
                mycursor = db.cursor()

                query = 'INSERT INTO messages (user_id, user_name, user_message) VALUES(%s,%s,%s)'
                values = (user_id, user_name, user_message)

                mycursor.execute(query, values)
                db.commit()
        db.close()

    except mysql.connector.Error as error_message:
        print(error_message)

def db_output_message(user_id):

    try:
        db = db_credentials()
        output = ''
        if db.is_connected():
            mycursor = db.cursor()

            query = 'SELECT user_message FROM messages WHERE user_id = ' + str(user_id)

            mycursor.execute(query)

            for x in mycursor:
                output += str(x[0])

        db.close()

        return output

    except mysql.connector.Error as error_message:
        print(error_message)





