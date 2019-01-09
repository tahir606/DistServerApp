import pymysql.cursors


class MySQLCon:
    def __init__(self):
        print("In MySQL Constructor")

    @staticmethod
    def connectToDatabase():
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                     user='crm',
                                     password='crm123!@#',
                                     db='dist_network',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            # with connection.cursor() as cursor:
            #     # Create a new record
            #     sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
            #     cursor.execute(sql, ('webmaster@python.org', 'very-secret'))
            #
            # # connection is not autocommit by default. So you must commit to save
            # # your changes.
            # connection.commit()

            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT * FROM `distributor_list` WHERE `dno`=%s"
                cursor.execute(sql, '1')
                result = cursor.fetchone()
                print(result)
        finally:
            connection.close()
