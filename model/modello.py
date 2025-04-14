import copy
import math

from database.meteo_dao import MeteoDao


class Model:
    def __init__(self):
        self.meteoDAO = MeteoDao()
        self.n_soluzioni = 0
        self.costo_ottimo = -1
        self.soluzione_ottima= []

    def getSituazioni(self):
        return self.meteoDAO.get_all_situazioni()

    def getSituazioniMeseCitta(self, mese, citta):
        return self.meteoDAO.getSituazioneMeseCitta(mese, citta)

    def getSituazioneMese(self, mese):
        return self.meteoDAO.getSituazioneMese(mese)

    def calcola_sequenza(self, mese):
        situazioni = self.getSituazioneMese(mese)
        self.n_soluzioni = 0
        self.costo_ottimo = -1
        self.soluzione_ottima = []
        self._ricorsione([], situazioni)
        return self.soluzione_ottima, self.costo_ottimo

    def trova_possibili_step(self, parziale, lista_situazioni):
        giorno = len(parziale) + 1  # se parziale ha lunghezza uno, cerco il giorno due
        candidati = []
        for situazione in lista_situazioni:
            if situazione.data.day == giorno:
                candidati.append(situazione)
        return candidati

    def is_admissible(self, candidate, parziale):
        # vincolo sui 6 giorni
        # conto quante volte il candidato è in parziale
        counter = 0
        for situazione in parziale:
            if situazione.localita == candidate.localita:
                counter += 1
        if counter >= 6:
            return False  # non posso aggiungere di nuovo la città

        # vincolo sulla permanenza => 3 giorni consecutivi
        # controllo le ultime tre situazioni del mio vettore
        # se sono tutte uguali non faccio niente
        # se non lo sono devo inserire l'ultima città
        # può esserci un caso particolare: se la lunghezza è < di 3 so già che la città da mettere
        # deve essere uguale alla città iniziale

        if len(parziale) == 0:
            return True

        # => lunghezza di parziale < 3
        if len(parziale) < 3:
            if candidate.localita != parziale[0].localita:
                return False  # non posso aggiungerlo

        else:
            # => le tre situazioni precedenti non sono tutte uguali
            if parziale[-3].localita != parziale[-2].localita or parziale[-3].localita != parziale[-1].localita or parziale[-2].localita != parziale[-1].localita:
                # se le tre citta non sono uguali (basta un solo caso)
                if parziale[-1].localita != candidate.localita:
                    return False

        # altrimenti ok
        return True

    def calcola_costo(self, parziale):
        costo = 0
        # => costo umidita
        for situazione in parziale:
            costo += situazione.umidita

        # => costo su spostamenti
        for i in range(len(parziale)):
            # se i due giorni precedenti non sono stato nella stessa citta in cui sono ora pago 100
            if i >= 2 and (parziale[i-1].localita != parziale[i].localita or
                           parziale[i-2].localita != parziale[i].localita):
                costo += 100

        return costo

    def _ricorsione(self, parziale, lista_situazioni):
        # condizione terminale
        if len(parziale) == 15:  # la lista è piena
            self.n_soluzioni += 1
            costo = self.calcola_costo(parziale)
            if self.costo_ottimo == -1 or self.costo_ottimo > costo:  # aggiorna costo e soluzioni ottime
                self.costo_ottimo = costo
                self.soluzione_ottima = copy.deepcopy(parziale)
            # print(f"Costo = {costo} ||| {parziale}")
            # print(parziale)
        # condizione ricorsiva
        else:
            # cercare le città per il giorno che mi serve
            candidates = self.trova_possibili_step(parziale, lista_situazioni)
            # se parziale ha lunghezza uno trovo le soluzioni del secondo giorno e così via

            # provo ad aggiungere una di queste città e vado avanti
            for candidate in candidates:
                # verifica vincoli
                if self.is_admissible(candidate, parziale):
                    parziale.append(candidate)
                    # ricorsione
                    self._ricorsione(parziale, lista_situazioni)
                    # backtracking
                    parziale.pop()


if __name__ == "__main__":
    myModel = Model()
    print(myModel.calcola_sequenza(2))
    # print(myModel.n_soluzioni)


