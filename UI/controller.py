import flet as ft

from UI.view import View
from model.modello import Model


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
        mese = self._view.dd_mese.value

        if mese is None:
            self._view.create_alert("Attenzione! Selezionare un mese")
            return

        lista = self._model.calcola_sequenza(mese)
        situazioni = lista[0]
        costo = lista[1]

        self._view.lst_result.controls.append(ft.Text(f"La sequenza ottina ha costo {costo} ed è:"))

        for situazione in situazioni:
            localita = situazione.localita
            data = situazione.data
            umidita = situazione.umidita
            self._view.lst_result.controls.append(
                ft.Text(f"[{localita} - {data}] Umidità = {umidita}"))
            self._view.update_page()

    def read_mese(self, e):
        self._mese = int(e.control.value)
