import pymysql.cursors


class MySQLCon:
    def __init__(self):
        print("In MySQL Constructor")

    def connectToDB(self):
        try:
            connection = pymysql.connect(host='192.168.100.24',
                                         user='crm',
                                         password='crm123!@#',
                                         db='dist_network',
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)
            return connection
        except Exception as e:
            print(e)
            raise e

    def checkForSignUpRequests(self):
        connection = self.connectToDB()
        if connection is None:
            return
        try:
            # Check for new phones that have not been verified i.e 1) rows where OTAC are empty 2) Verified is False
            with connection.cursor() as cursor:
                # Read a single record
                sql = ("SELECT NO, PHONE, EMAIL FROM otac_requests " +
                       " WHERE otac = ''"
                       " OR otac IS NULL " +
                       " AND VERIFIED = FALSE ")
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        except Exception as e:
            print(e)
            raise e
        finally:
            connection.close()

    def checkForSmsToBeSent(self):
        connection = self.connectToDB()
        if connection is None:
            return
        try:
            # Check for new messages to be sent from table SMS_OUT_LIST with the flag W
            with connection.cursor() as cursor:
                # Reading a single record
                sql = (" SELECT SNO, SPHONE, SBODY, SEMAIL, SUBJ " +
                       " FROM SMS_OUT_LIST " +
                       " WHERE FLAG = 'W' ")
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        except Exception as e:
            print(e)
            raise e
        finally:
            connection.close()

    def updateOTACwithPhone(self, otac, phone, id):
        print('otac: ' + otac + '\nphone: ' + phone + '\nno: ' + id)
        connection = self.connectToDB()
        if connection is None:
            return
        try:
            with connection.cursor() as cursor:
                sql = (("UPDATE OTAC_REQUESTS " +
                        " SET OTAC = '{0}' " +
                        " WHERE PHONE = '{1}' " +
                        " AND NO = '{2}' " +
                        " AND OTAC IS NULL").format(otac, phone, id))
                cursor.execute(sql)
                connection.commit()
        except Exception as e:
            connection.rollback()
            print('Exception in updateOTAC')
            print(e)
            raise e
        finally:
            connection.close()

    def updateSmsFlag(self, code):
        connection = self.connectToDB()
        if connection is None:
            return
        try:
            with connection.cursor() as cursor:
                sql = ("UPDATE SMS_OUT_LIST " +
                       " SET FLAG = 'S' "
                       " WHERE SNO = '%s'" % code)
                cursor.execute(sql)
                connection.commit()
        except Exception as e:
            connection.rollback()
            print(e)
            raise e
        finally:
            connection.close()
