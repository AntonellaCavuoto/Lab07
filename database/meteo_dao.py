from collections import defaultdict

from database.DB_connect import DBConnect
from model import situazione
from model.situazione import Situazione


class MeteoDao():

    @staticmethod
    def get_all_situazioni():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, s.Data, s.Umidita
                        FROM situazione s 
                        ORDER BY s.Data ASC"""
            cursor.execute(query)
            for row in cursor:
                s = situazione.Situazione(row["Localita"],
                                          row["Data"],
                                          row["Umidita"])
                result.append(s)

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getSituazioneMeseCitta(mese, citta):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor()
            query = """SELECT s.Umidita 
                       FROM situazione s 
                       WHERE month(s.`Data`) = %s and
                       s.Localita = %s """

            cursor.execute(query, (mese, citta))

            for row in cursor:
                result.append(row)

            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def getSituazioneMese(mese):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, s.`Data`, s.Umidita 
                               FROM situazione s 
                               WHERE month(s.`Data`) = %s  and 
                               day(s.`Data`) <= 15
                               ORDER BY s.Data ASC"""

            cursor.execute(query, (mese,))

            for row in cursor:
                result.append(Situazione(row["Localita"],
                                         row["Data"],
                                         row["Umidita"]))

            cursor.close()
            cnx.close()

        return result


if __name__ == "__main__":
    myDao = MeteoDao()
    lista = (myDao.getSituazioneMese("2"))
    print(lista)

