from database.meteo_dao import MeteoDao


class Model:
    def __init__(self):
        self.meteoDAO  = MeteoDao()

    def getSituazioni(self):
        return self.meteoDAO.get_all_situazioni()

    def getSituazioniMeseCitta(self, mese, citta):
        return self.meteoDAO.getSituazioneMeseCitta(mese, citta)

    def getSituazioneMese(self, mese):
        return self.meteoDAO.getSituazioneMese(mese)
