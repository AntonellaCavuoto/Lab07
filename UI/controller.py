import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        self._view.lst_result.controls.clear()
        mese = self._view.dd_mese.value

        if mese is None:
            self._view.create_alert("Attenzione! Selezionare un mese")
            return

        situazioni = self._model.getSituazioni()
        citta = []

        for s in situazioni:
            if not citta.__contains__(s.localita):
                citta.append(s.localita)

        citta.sort()

        for c in citta:
            somma = 0
            umidita = self._model.getSituazioniMeseCitta(mese, c)
            for u in umidita:
                somma += int(u[0])

            media = somma / len(umidita)
            self._view.lst_result.controls.append(ft.Text(f"{c}: {media}"))
            self._view.update_page()

    def handle_sequenza(self, e):
        self._view.lst_result.controls.clear()

        giorni_totali = 15
        max_citta = 6
        min_blocco = 3
        costo_cambio = 100

        miglior_sequenza=[]
        miglior_costo = float('inf')  # infinito

        mese = self._view.dd_mese.value

        if mese is None:
            self._view.create_alert("Attenzione! Selezionare un mese")
            return

        situazioni = self._model.getSituazioni()
        citta = []

        for s in situazioni:
            if not citta.__contains__(s.localita):
                citta.append(s.localita)

        situazioni_mese = self._model.getSituazioneMese(mese)

        # def esplora(giorno_corrente, sequenza, conta_citta, costo_attuale):
        #     global miglior_sequenza, miglior_costo
        #
        #     # il ciclo finisce quando abbiamo raggiunto tutti i giorni disponibili
        #     if giorno_corrente == giorni_totali:
        #         if costo_attuale < miglior_costo:
        #             miglior_costo = costo_attuale
        #             miglior_sequenza = sequenza[:] # copio la lista
        #         return
        #
        #     # se non finisco i giorni
        #     else:
        #         for city in citta:



    def read_mese(self, e):
        self._mese = int(e.control.value)
