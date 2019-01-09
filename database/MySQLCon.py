import pymysql.cursors


class MySQLCon:
    def __init__(self):
        print("In MySQL Constructor")
        self.connection = pymysql.connect(host='localhost',
                                          user='crm',
                                          password='crm123!@#',
                                          db='dist_network',
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)

    def checkForSignUpRequests(self):
        try:
            # Check for new phones that have not been verified i.e 1) rows where OTAC are empty 2) Verified is False
            with self.connection.cursor() as cursor:
                # Read a single record
                sql = ("SELECT PHONE, OTAC, VERIFIED FROM otac_requests " +
                       " WHERE otac = '' " +
                       " AND VERIFIED = FALSE ")
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        finally:
            self.connection.close()
