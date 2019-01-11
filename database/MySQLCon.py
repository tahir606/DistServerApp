import pymysql.cursors


class MySQLCon:
    def __init__(self):
        print("In MySQL Constructor")

    def connectToDB(self):
        try:
            connection = pymysql.connect(host='localhost',
                                         user='crm',
                                         password='crm123!@#',
                                         db='dist_network',
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)
            return connection
        except Exception as e:
            print(e)

    def checkForSignUpRequests(self):
        connection = self.connectToDB()
        if connection is None:
            return
        try:
            # Check for new phones that have not been verified i.e 1) rows where OTAC are empty 2) Verified is False
            with connection.cursor() as cursor:
                # Read a single record
                sql = ("SELECT PHONE FROM otac_requests " +
                       " WHERE otac = '' " +
                       " AND VERIFIED = FALSE ")
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        finally:
            connection.close()

    def updateOTACwithPhone(self, otac, phone):
        connection = self.connectToDB()
        if connection is None:
            return
        try:
            with connection.cursor() as cursor:
                sql = ("UPDATE OTAC_REQUESTS " +
                       " SET OTAC = '%s' "
                       " WHERE PHONE = '%s'"
                       " AND OTAC = ''" % (otac, phone))
                cursor.execute(sql)
                connection.commit()
        except:
            connection.rollback()
        finally:
            connection.close()
