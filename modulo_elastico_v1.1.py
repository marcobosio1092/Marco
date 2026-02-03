import sys
import os
import numpy as np
import math
import resources_rc
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QListWidget, QFileDialog,
    QMessageBox, QLabel, QTextEdit, QStackedWidget, QInputDialog,
    QTableWidget, QTableWidgetItem, QSizePolicy, QDialog, QComboBox
  
)
from PySide6.QtGui import QPixmap

from PySide6.QtCore import Qt

# Matplotlib per il grafico
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

Modulo_elastico = []
Delta_sforzo = []
Delta_epsilon1 = []
Delta_epsilon2 = []
Delta_epsilon3 = []
Delta_epsilon = []
SFOR = []
EPS1 = []
EPS2 = []
EPS3 = []
EPS = []
NEW_DIAM=[]
SU=[]
EU=[]


P_Modulo_elastico = []
P_Delta_sforzo = []
P_Delta_epsilon1 = []
P_Delta_epsilon2 = []
P_Delta_epsilon3 = []
P_Delta_epsilon = []
P_SFOR = []
P_EPS1 = []
P_EPS2 = []
P_EPS3 = []
P_EPS = []
P_NEW_DIAM=[]
P_SU=[]
P_EU=[]
P_FILE=[]


class Page1(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        layout = QVBoxLayout(self)

        # Percorso cartella
        top_layout = QHBoxLayout()
        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText("Inserisci o seleziona una cartella...")
        browse_btn = QPushButton("Sfoglia")
        ref_btn = QPushButton("Aggiorna")
        top_layout.addWidget(self.path_edit)
        top_layout.addWidget(browse_btn)
        top_layout.addWidget(ref_btn)
        # Lista file
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.MultiSelection)

        # Bottone processa
        bott_layout = QHBoxLayout()
        self.process_btn = QPushButton("Processa selezionati")
        self.sall = QPushButton("Seleziona tutti")
        self.dall = QPushButton("Deseleziona tutto")

        bott_layout.addWidget(self.sall)
        bott_layout.addWidget(self.dall)

        layout.addLayout(top_layout)
        layout.addWidget(self.file_list)
        layout.addLayout(bott_layout)
        layout.addWidget(self.process_btn)

        # Eventi
        browse_btn.clicked.connect(self.open_folder)
        ref_btn.clicked.connect(self.load_files)
        self.path_edit.returnPressed.connect(self.load_files)
        self.process_btn.clicked.connect(self.process_selected)
        self.sall.clicked.connect(self.selec_all)
        self.dall.clicked.connect(self.deselec_all)
     
    def open_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Seleziona una cartella")
        if folder:
            self.path_edit.setText(folder)
            self.load_files()

    def load_files(self):
        path = self.path_edit.text()
        self.file_list.clear()
        if not os.path.isdir(path):
            return
        for file in sorted(os.listdir(path)):
            self.file_list.addItem(file)

    def process_selected(self):
        selected_items = self.file_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Attenzione", "Seleziona almeno un file!")
            return

        selected_files = [item.text() for item in selected_items]
        global Modulo_elastico
        global Delta_sforzo
        global Delta_epsilon
        global Delta_epsilon1
        global Delta_epsilon2
        global Delta_epsilon3
        global SFOR
        global EPS
        global EPS1
        global EPS2
        global EPS3
        global NEW_DIAM
        global SU 
        global EU
        

        Modulo_elastico = [np.nan] * len(selected_files)  # lista della stessa lunghezza dei file
        Delta_sforzo = [np.nan] * len(selected_files)  # lista della stessa lunghezza dei file
        Delta_epsilon = [np.nan] * len(selected_files)  # lista della stessa lunghezza dei file
        Delta_epsilon1 = [np.nan] * len(selected_files)  # lista della stessa lunghezza dei file
        Delta_epsilon2 = [np.nan] * len(selected_files)  # lista della stessa lunghezza dei file
        Delta_epsilon3 = [np.nan] * len(selected_files)  # lista della stessa lunghezza dei file
        SU = [np.nan] * len(selected_files)  # lista della stessa lunghezza dei file
        EU = [np.nan] * len(selected_files)  # lista della stessa lunghezza dei file
        NEW_DIAM = [0] * len(selected_files)  # lista della stessa lunghezza dei file
        SFOR = [[] for _ in range(len(selected_files))]
        EPS = [[] for _ in range(len(selected_files))]
        EPS1 = [[] for _ in range(len(selected_files))]
        EPS2 = [[] for _ in range(len(selected_files))]
        EPS3 = [[] for _ in range(len(selected_files))]

        if any(not np.isnan(x) for x in P_Modulo_elastico):
            print('sono qui')
            for i, val in enumerate(P_FILE):
                if val in selected_files:
                    idx = selected_files.index(val)
                    Modulo_elastico [idx] = P_Modulo_elastico [i]
                    Delta_sforzo [idx] = P_Delta_sforzo [i]
                    Delta_epsilon1 [idx] = P_Delta_epsilon1 [i]
                    Delta_epsilon2 [idx] = P_Delta_epsilon2 [i]
                    Delta_epsilon3 [idx] = P_Delta_epsilon3 [i]
                    Delta_epsilon [idx] = P_Delta_epsilon [i]
                    SFOR [idx] = P_SFOR [i]
                    EPS1 [idx] = P_EPS1 [i]
                    EPS2 [idx] = P_EPS2 [i]
                    EPS3 [idx] = P_EPS3 [i]
                    EPS [idx] = P_EPS [i]
                    NEW_DIAM [idx] =P_NEW_DIAM [i]
                    SU [idx] =P_SU [i]
                    EU [idx] =P_EU [i]
   

        page2 = self.stack.widget(2)
        page2.start_processing(self.path_edit.text(), selected_files)
        self.stack.setCurrentIndex(2)  # vai alla pagina 2

    def selec_all(self):
        self.file_list.selectAll()
        
    def deselec_all(self):
        self.file_list.clearSelection()

def safe_float(x):
    try:
        return float(x)
    except ValueError:
        return np.nan


class Page2(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.layout = QVBoxLayout(self)

        # Etichetta file corrente
        self.label = QLabel("File corrente:")

        self.file_combo = QComboBox()
        self.file_combo.currentIndexChanged.connect(self.on_file_selected)


        self.riepilogo_btn = QPushButton("Vai al riepilogo")
        
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.label)
        top_layout.addWidget(self.file_combo)
        top_layout.addWidget(self.riepilogo_btn)

        self.riepilogo_btn.clicked.connect(self.vai_a_riepilogo)
        

        # Grafico principale
        self.figure = Figure(figsize=(5, 6))
        self.canvas = FigureCanvas(self.figure)

        # Bottoni Mostra grafico e Scegli punti
        self.choose_point = QPushButton("Processa dati")
        self.salva_grafico = QPushButton("Esporta in grafico come immagine")
        self.choose_point.clicked.connect(self.open_choose_window)
        self.salva_grafico.clicked.connect(lambda: self.salva_plot(self.figure))
        # Spazio risultati
        self.labelR = QLabel()
        html0 = f"""
        <table>
            <!-- RIGA DI INTESTAZIONE -->
            <tr>
                <td colspan="3" style="text-align:center; font-weight:bold; padding-bottom:10px;">
                    Valori di deformazione e sforzo
                </td>
            </tr>

            <!-- RIGHE DEI VALORI -->
            <tr>
                <!-- Prima riga -->
                <td>Δε<sub>1</sub>: - [μm/m]</td>
                <td></td>
                <td></td>
            </tr>
            <tr>
                <!-- Seconda riga: valore centrato nelle colonne 2 e 3 -->
                <td>Δε<sub>2</sub>: - [μm/m] </td>
                <td style="text-align:center;">Δε<sub>medio</sub>: - [μm/m] </td>
                <td style="text-align:center;">Δσ<sub>1</sub>: - [MPa] </td>
            </tr>
            <tr>
                <!-- Terza riga -->
                <td>Δε<sub>3</sub>: - [μm/m] </td>
                <td></td>
                <td></td>
            </tr>
        </table>
        """

        self.labelR.setText(html0)
        
        self.labelMODULO = QLabel("Il modulo elasitico del campione è:")
        
        self.labelMassimi = QLabel()
        html1 = f"""
        <table>
            <!-- RIGHE DEI VALORI -->
            <tr>
                <!-- Prima riga -->
                <td>Valori ultimi individuati:</td>

            </tr>
            <tr>
                <!-- Seconda riga: valore centrato nelle colonne 2 e 3 -->
                <td>ε<sub>u</sub>= - [μm/m]</td>
            </tr>
            <tr>
                <!-- Terza riga -->
                <td>σ<sub>u</sub>= - [MPa]</td>
            </tr>
        </table>
        """
        self.labelMassimi.setText(html1)

        R_layout = QHBoxLayout()
        R_layout.addWidget(self.labelR)
        R_layout.addWidget(self.labelMODULO)
        R_layout.addWidget(self.labelMassimi)


        # Bottoni navigazione
        self.next_btn = QPushButton("Successivo")
        self.back_btn = QPushButton("Torna indietro")
        self.back_home = QPushButton("Torna a seleziona file")
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.back_btn)
        btn_layout.addWidget(self.next_btn)
        btn_layout.addWidget(self.back_home)

        # Aggiunta al layout principale

        penultimo_layout = QHBoxLayout()
        penultimo_layout.addWidget(self.choose_point)
        penultimo_layout.addWidget(self.salva_grafico)
        


        self.layout.addLayout(top_layout)
        self.layout.addWidget(self.canvas)
        self.layout.addLayout(R_layout)
        self.layout.addLayout(penultimo_layout)
        self.layout.addLayout(btn_layout)

        # Eventi
        self.next_btn.clicked.connect(self.next_file)
        self.back_btn.clicked.connect(self.go_back)
        self.back_home.clicked.connect(self.go_home)

        # Variabili interne
        self.files = []
        self.folder = ""
        self.current_index = 0
        self.col1 = []
        self.col34 = []
        self.col56 = []
        self.col78 = []
        self.val_x = []
        self.val_y = []
    
    def on_file_selected(self, index):
        if index < 0 or index >= len(self.files):
            return

        if index == self.current_index:
            return

        self.reset_all()
        self.current_index = index
        self.process_file()

        # Se il file ha già dati, riplotta
        if (
            self.current_index < len(SFOR)
            and SFOR[self.current_index] is not None
            and len(SFOR[self.current_index]) > 0
        ):
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            self.richiama(ax)
            self.canvas.draw()

    def salva_plot(self, figure):
        """Salva il grafico corrente in formato JPEG."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Salva grafico",
            "",
            "JPEG Image (*.jpg *.jpeg)"
        )

        if not file_path:
            return

        if not (file_path.lower().endswith(".jpg") or file_path.lower().endswith(".jpeg")):
            file_path += ".jpg"

        try:
            figure.savefig(
                file_path,
                dpi=300,
                format="jpeg",
                bbox_inches="tight"
            )
            QMessageBox.information(
                self,
                "Salvataggio completato",
                f"Grafico salvato correttamente in:\n{file_path}"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Errore",
                f"Errore nel salvataggio del grafico:\n{e}"
            )    


    def start_processing(self, folder, files):
        self.folder = folder
        self.files = files
        self.current_index = 0

            # Popola la combo
        self.file_combo.blockSignals(True)
        self.file_combo.clear()
        self.file_combo.addItems(self.files)
        self.file_combo.setCurrentIndex(0)
        self.file_combo.blockSignals(False)

        self.col1 = []
        self.col34 = []
        self.col56 = []
        self.col78 = []
        if any(not np.isnan(x) for x in Modulo_elastico):
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            self.richiama(ax)
            self.canvas.draw()
        self.process_file()


        
    def process_file(self):
        if self.current_index < 0 or self.current_index >= len(self.files):
            return
        self.reset_labels()

        if self.file_combo.currentIndex() != self.current_index:
            self.file_combo.blockSignals(True)
            self.file_combo.setCurrentIndex(self.current_index)
            self.file_combo.blockSignals(False)
        
        # RESET dati del file corrente
        self.col1.clear()
        self.col34.clear()
        self.col56.clear()
        self.col78.clear()

        filename = self.files[self.current_index]
        full_path = os.path.join(self.folder, filename)
        self.label.setText(f"File corrente: {filename}")

        try:
            with open(full_path, "r") as f:
                lines = f.readlines()[100:]

            data = []
            for line in lines:
                if line.strip() == "":
                    continue
                numbers = [safe_float(x) for x in line.replace(",", " ").split()]
                data.append(numbers)
            data = np.array(data)

            # Salva i vettori
            self.col1.append(data[:, 0])

            if data.shape[1] >= 4:
                self.col34.append(np.nanmean(data[:, 2:4], axis=1))
            else:
                self.col34.append(np.full(len(data), np.nan))
            if data.shape[1] >= 6:
                self.col56.append(np.nanmean(data[:, 4:6], axis=1))
            else:
                self.col56.append(np.full(len(data), np.nan))

            
            if data.shape[1] >= 8:
                self.col78.append(np.nanmean(data[:, 6:8], axis=1))
            else:
                self.col78.append(np.full(len(data), np.nan))

        except Exception as e:
            QMessageBox.warning(self, "Errore", f"Impossibile leggere {filename}:\n{e}")

        if math.isnan(Modulo_elastico[self.current_index]):
            self.open_choose_window()

    def moving_average(self, x, window):
        x = np.asarray(x, dtype=float)

        # maschera dei valori validi
        valid = ~np.isnan(x)

        # se non ci sono dati validi → ritorna tutto NaN
        if not np.any(valid):
            return np.full_like(x, np.nan)

        # somma pesata ignorando i NaN
        weights = np.ones(window)

        x_filled = np.where(valid, x, 0.0)

        sum_x = np.convolve(x_filled, weights, mode='same')
        count = np.convolve(valid.astype(float), weights, mode='same')

        # evita divisioni per zero
        with np.errstate(invalid='ignore', divide='ignore'):
            ma = sum_x / count

        ma[count == 0] = np.nan
        return ma


 
    

    def update_plot(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        if not self.col1:
            self.canvas.draw()
            return

        # --- AREA PROVINO ---
        try:
            diametro = float(self.diam_input.text())
            area = math.pi * (diametro / 2) ** 2 / 1000 if diametro != 0 else 1
        except ValueError:
            area = 1

        # --- CONCATENA DATI ---
        col1  = np.concatenate(self.col1)
        col34 = np.concatenate(self.col34)
        col56 = np.concatenate(self.col56)
        col78 = np.concatenate(self.col78)

        # --- FINESTRA MEDIA MOBILE ---
        window = 100
        if len(col1) < window:
            window = max(1, len(col1) // 5)

        # --- MEDIA MOBILE (SOLO PER PLOT) ---
        col1_ma  = self.moving_average(col1, window)
        col34_ma = self.moving_average(col34, window)
        col56_ma = self.moving_average(col56, window)
        col78_ma = self.moving_average(col78, window)

        # --- GRANDEZZE FISICHE ---
        sforzo = col1_ma / (-area)
        E1 = col34_ma * -10000
        E2 = col56_ma * -10000
        E3 = col78_ma * -10000
        E  = (E1 + E2 + E3) / 3

        # --- SLICE FINO AL 5° PUNTO (SE ESISTE) ---
        if len(self.val_x) >= 5:
            nplot = min(self.val_x[-1] + 1, len(sforzo))
        else:
            nplot = 1

        EPS[self.current_index] = E[:nplot]
        SFOR[self.current_index] = sforzo[:nplot]
        EPS1[self.current_index] = E1[:nplot]
        EPS2[self.current_index] = E2[:nplot]
        EPS3[self.current_index] = E3[:nplot]
        
        s=SFOR[self.current_index]
        e=EPS[self.current_index]
        e1=EPS1[self.current_index]
        e2=EPS2[self.current_index]
        e3=EPS3[self.current_index]

        # --- PLOT ---
        ax.plot(e1,  s, label="E1", color=(205/255,)*3)
        ax.plot(e2,  s, label="E2", color=(55/255,)*3)
        ax.plot(e3,  s, label="E3", color=(105/255,)*3)
        ax.plot(e,  s, label="E media", color="red")

        ax.set_xlabel("Deformazioni [μm/m]")
        ax.set_ylabel("Sforzo [MPa]")
        ax.legend()
        ax.grid(True)
        self.canvas.draw()

    def richiama(self, ax):

        s = SFOR[self.current_index]
        e = EPS[self.current_index]
        e1 = EPS1[self.current_index]
        e2 = EPS2[self.current_index]
        e3 = EPS3[self.current_index]
        if s is None or len(s) == 0:
            # Nessun dato da plottare, esce subito
            return
        
        if not np.isnan(max(s)) and max(s) != 0:
            ax.plot(e1, s, label="E1", color=(205/255,)*3)
            ax.plot(e2, s, label="E2", color=(55/255,)*3)
            ax.plot(e3, s, label="E3", color=(105/255,)*3)
            ax.plot(e,  s, label="E media", color="red")

            ax.set_xlabel("Deformazioni [μm/m]")
            ax.set_ylabel("Sforzo [MPa]")
            ax.legend()
            ax.grid(True)

    def vai_a_riepilogo(self):
        global P_Modulo_elastico, P_Delta_sforzo
        global P_Delta_epsilon1, P_Delta_epsilon2, P_Delta_epsilon3
        global P_Delta_epsilon, P_SFOR
        global P_EPS1, P_EPS2, P_EPS3, P_EPS
        global P_NEW_DIAM, P_SU, P_EU, P_FILE
        P_Modulo_elastico = Modulo_elastico
        P_Delta_sforzo = Delta_sforzo
        P_Delta_epsilon1 = Delta_epsilon1
        P_Delta_epsilon2 = Delta_epsilon2
        P_Delta_epsilon3 = Delta_epsilon2
        P_Delta_epsilon = Delta_epsilon
        P_SFOR = SFOR
        P_EPS1 = EPS1
        P_EPS2 = EPS2
        P_EPS3 = EPS3
        P_EPS = EPS
        P_NEW_DIAM=NEW_DIAM
        P_SU=SU
        P_EU=EU
        P_FILE=self.files
        page3 = self.stack.widget(self.stack.count() - 1)
        page3.populate_table(self.files, NEW_DIAM,Delta_epsilon1,Delta_epsilon2,Delta_epsilon3,Delta_epsilon,Delta_sforzo,Modulo_elastico,EU,SU)
        self.stack.setCurrentWidget(page3)



    def next_file(self):
        self.file_combo.setCurrentIndex(self.current_index)
        if self.current_index >= len(self.files) - 1:
            msg = QMessageBox(self)  # 'self' è la finestra padre
            msg.setWindowTitle("Scelta")
            msg.setText("Hai provessato tutti i dati! Cosa vuoi fare?")
            msg.setIcon(QMessageBox.Question)

            # Aggiunta dei due pulsanti
            btn_ghome = msg.addButton("Torna alla home", QMessageBox.AcceptRole)
            btn_riepilogo = msg.addButton("Vai al riepilogo", QMessageBox.AcceptRole)
            
            btn_qui = msg.addButton("Rimani qui", QMessageBox.RejectRole)
            

            # Mostra il popup e aspetta la risposta
            msg.exec()

            # Controllo quale pulsante è stato premuto
            clicked = msg.clickedButton()
            if clicked == btn_qui:
                pass
                # Non fai nulla, il popup si chiude automaticamente
            elif clicked == btn_ghome:
                #self.stack.setCurrentIndex(1)  # esempio: vai alla pagina 1
                self.go_home()
            elif clicked == btn_riepilogo:
                global P_Modulo_elastico, P_Delta_sforzo
                global P_Delta_epsilon1, P_Delta_epsilon2, P_Delta_epsilon3
                global P_Delta_epsilon, P_SFOR
                global P_EPS1, P_EPS2, P_EPS3, P_EPS
                global P_NEW_DIAM, P_SU, P_EU, P_FILE
                
                P_Modulo_elastico = Modulo_elastico
                P_Delta_sforzo = Delta_sforzo
                P_Delta_epsilon1 = Delta_epsilon1
                P_Delta_epsilon2 = Delta_epsilon2
                P_Delta_epsilon3 = Delta_epsilon2
                P_Delta_epsilon = Delta_epsilon
                P_SFOR = SFOR
                P_EPS1 = EPS1
                P_EPS2 = EPS2
                P_EPS3 = EPS3
                P_EPS = EPS
                P_NEW_DIAM=NEW_DIAM
                P_SU=SU
                P_EU=EU
                P_FILE=self.files
                page3 = self.stack.widget(self.stack.count() - 1)
                page3.populate_table(self.files, NEW_DIAM,Delta_epsilon1,Delta_epsilon2,Delta_epsilon3,Delta_epsilon,Delta_sforzo,Modulo_elastico,EU,SU)
                self.stack.setCurrentWidget(page3)
            return
        
        
        self.reset_all()
        self.current_index += 1
        self.process_file()
        if (self.current_index < len(SFOR) and 
            SFOR[self.current_index] is not None and 
            len(SFOR[self.current_index]) > 0):
            
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            self.richiama(ax)   # PASSO AX qui
            self.canvas.draw()

    def reset_labels(self):
        # Reset della tabella dei valori
         if math.isnan(Modulo_elastico[self.current_index]):
 
            html0 = f"""
            <table>
                <tr>
                    <td colspan="3" style="text-align:center; font-weight:bold; padding-bottom:10px;">
                        Valori di deformazione e sforzo
                    </td>
                </tr>
                <tr>
                    <td>Δε<sub>1</sub>: - [μm/m]</td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <td>Δε<sub>2</sub>: - [μm/m]</td>
                    <td style="text-align:center;">Δε<sub>medio</sub>: - [μm/m]</td>
                    <td style="text-align:center;">Δσ<sub>1</sub>: - [MPa]</td>
                </tr>
                <tr>
                    <td>Δε<sub>3</sub>: - [μm/m]</td>
                    <td></td>
                    <td></td>
                </tr>
            </table>
            """
            self.labelR.setText(html0)

            # Reset QLabel modulo elastico
            self.labelMODULO.setText("Il modulo elastico del campione è:")    

            html1 = f"""
            <table>
                <!-- RIGHE DEI VALORI -->
                <tr>
                    <!-- Prima riga -->
                    <td>Valori ultimi individuati:</td>

                </tr>
                <tr>
                    <!-- Seconda riga: valore centrato nelle colonne 2 e 3 -->
                    <td>ε<sub>u</sub>= - [μm/m]</td>
                </tr>
                <tr>
                    <!-- Terza riga -->
                    <td>σ<sub>u</sub>= - [MPa]</td>
                </tr>
            </table>
            """
            self.labelMassimi.setText(html1)

         else:
            html0 = f"""
         <table>
            <tr>
                <td colspan="3" style="text-align:center; font-weight:bold; padding-bottom:10px;">
                    Valori di deformazione e sforzo
                </td>
            </tr>
            <tr>
                <td>Δε<sub>1</sub>: {Delta_epsilon1[self.current_index]:.2f} [μm/m]</td>
                <td></td>
                <td></td>
            </tr>
            <tr>
                <td>Δε<sub>2</sub>: {Delta_epsilon2[self.current_index]:.2f} [μm/m]</td>
                <td style="text-align:center;">Δε<sub>medio</sub>: {Delta_epsilon[self.current_index]:.2f} [μm/m]</td>
                <td style="text-align:center;">Δσ<sub>1</sub>: {Delta_sforzo[self.current_index]:.2f} [MPa]</td>
            </tr>
            <tr>
                <td>Δε<sub>3</sub>: {Delta_epsilon3[self.current_index]:.2f} [μm/m]</td>
                <td></td>
                <td></td>
            </tr>
        </table>
        """
            self.labelR.setText(html0)

            # Reset QLabel modulo elastico
            self.labelMODULO.setText(
            f"Il modulo elastico del campione è: {Modulo_elastico[self.current_index]:.2f} GPa"
            )


            html1 = f"""
            <table>
                <!-- RIGHE DEI VALORI -->
                <tr>
                    <!-- Prima riga -->
                    <td>Valori ultimi individuati:</td>

                </tr>
                <tr>
                    <!-- Seconda riga: valore centrato nelle colonne 2 e 3 -->
                    <td>ε<sub>u</sub>= {EU[self.current_index]:.2f} [μm/m]</td>
                </tr>
                <tr>
                    <!-- Terza riga -->
                    <td>σ<sub>u</sub>= {SU[self.current_index]:.2f} [MPa]</td>
                </tr>
            </table>
            """
            self.labelMassimi.setText(html1)



    def show_summary_popup(self):
        global Modulo_elastico

        testo = "Riepilogo Modulo Elastico per file selezionati:\n\n"
        for i, val in enumerate(Modulo_elastico):
            nome_file = self.files[i] if i < len(self.files) else "N/A"
            val_str = f"{val:.2f} GPa" if not np.isnan(val) else "NaN"
            testo += f"{i+1}. {nome_file}: {val_str}\n"

        QMessageBox.information(self, "Riepilogo Modulo Elastico", testo)

    def go_back(self):
        self.file_combo.setCurrentIndex(self.current_index)
        if self.current_index <= 0:
            QMessageBox.information(self, "Inizio", "Sei al primo file selezionato della lista, se vuoi selezionare altri file premi Torna a seleziona dati")
            return
        
        self.reset_all()
        self.current_index -= 1
        self.process_file()
        if (self.current_index < len(SFOR) and 
            SFOR[self.current_index] is not None and 
            len(SFOR[self.current_index]) > 0):
            
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            self.richiama(ax)   # PASSO AX qui
            self.canvas.draw()


    def go_home(self):
        global P_Modulo_elastico, P_Delta_sforzo
        global P_Delta_epsilon1, P_Delta_epsilon2, P_Delta_epsilon3
        global P_Delta_epsilon, P_SFOR
        global P_EPS1, P_EPS2, P_EPS3, P_EPS
        global P_NEW_DIAM, P_SU, P_EU, P_FILE
        
        P_Modulo_elastico = Modulo_elastico
        P_Delta_sforzo = Delta_sforzo
        P_Delta_epsilon1 = Delta_epsilon1
        P_Delta_epsilon2 = Delta_epsilon2
        P_Delta_epsilon3 = Delta_epsilon2
        P_Delta_epsilon = Delta_epsilon
        P_SFOR = SFOR
        P_EPS1 = EPS1
        P_EPS2 = EPS2
        P_EPS3 = EPS3
        P_EPS = EPS
        P_NEW_DIAM=NEW_DIAM
        P_SU=SU
        P_EU=EU
        P_FILE=self.files

        self.reset_all()
        self.stack.setCurrentIndex(1)



    def reset_all(self):
        # reset selezione punti
        self.val_x.clear()
        self.val_y.clear()
        self.selected_points = []

        # reset dati
        self.col1.clear()
        self.col34.clear()
        self.col56.clear()
        self.col78.clear()

        # reset grafico
        self.figure.clear()
        self.canvas.draw()     

    def open_choose_window(self):
        if not np.isnan(Modulo_elastico[self.current_index]) and Modulo_elastico[self.current_index] != 0:
            self.canc_valori()

    
        self.choose_window = QWidget()
        self.choose_window.setWindowTitle("Seleziona punti per la valutazione")
        self.choose_window.resize(1000, 600)

        main_layout = QHBoxLayout(self.choose_window)

        figure = Figure(figsize=(5, 6))
        canvas = FigureCanvas(figure)
        self.choose_canvas = canvas          # FIX 1
        self.ax = figure.add_subplot(111)
        main_layout.addWidget(canvas, stretch=3)

        def zoom(event):
            base_scale = 1.2  # fattore di zoom
            if event.inaxes != self.ax:
                return

            xdata = event.xdata
            ydata = event.ydata
            cur_xlim = self.ax.get_xlim()
            cur_ylim = self.ax.get_ylim()

            # calcola nuovi limiti
            scale_factor = base_scale if event.step > 0 else 1/base_scale
            x_left = xdata - (xdata - cur_xlim[0]) / scale_factor
            x_right = xdata + (cur_xlim[1] - xdata) / scale_factor
            y_bottom = ydata - (ydata - cur_ylim[0]) / scale_factor
            y_top = ydata + (cur_ylim[1] - ydata) / scale_factor

            self.ax.set_xlim([x_left, x_right])
            self.ax.set_ylim([y_bottom, y_top])
            self.choose_canvas.draw()

        # collega la funzione all'evento scroll
        self.choose_canvas.mpl_connect('scroll_event', zoom)

        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        new_diam = 0
        # Campo diametro provino
        diam_layout = QVBoxLayout()
        diam_label = QLabel("Diametro provino [mm]:")
        self.diam_input = QLineEdit()
        self.diam_input.editingFinished.connect(self.on_diameter_changed)
        diam_layout.addWidget(diam_label)
        diam_layout.addWidget(self.diam_input)

        right_layout.addLayout(diam_layout)

        self.info_label = QLabel("Punti selezionati:")
        right_layout.addWidget(self.info_label)

        self.canc = QPushButton("Cancella punti")
        right_layout.addWidget(self.canc)
        self.canc.clicked.connect(self.canc_valori)

        self.zoom = QPushButton("Resetta zoom")
        right_layout.addWidget(self.zoom)
        self.zoom.clicked.connect(self.res_zoom)

        # Bottone che mostra il modulo elastico
        self.show_checkbox = QCheckBox("Mostra valori ultimi del materiale:")
        right_layout.addWidget(self.show_checkbox )

        # Label che mostrerà il valore
        self.mod_label = QLabel("Sforzo ultimo:")
        right_layout.addWidget(self.mod_label)
        # Label che mostrerà il valore
        self.mod_label2 = QLabel("Deformazione ultima:")
        right_layout.addWidget(self.mod_label2)

        # Collegamento della spunta
        self.show_checkbox.stateChanged.connect(self.toggle_modulo)

        self.sec = QPushButton("Calcola e chiudi")
        right_layout.addWidget(self.sec)
        self.sec.clicked.connect(self.salva_chiudi)

        right_layout.addStretch(1)
        main_layout.addWidget(right_widget, stretch=1)

        self.selected_points = []


        if self.col1:
            y = np.concatenate(self.col1)
            window = 100
            if len(y) < window:
                window = max(1, len(y) // 5)
            y_ma  = self.moving_average(y, window)
            x = np.arange(len(y))



            self.line, = self.ax.plot(x, y_ma, color='blue', picker=1)
            self.ax.grid(True)

            def on_click(event):
                if event.inaxes != self.ax:
                    return
                if event.xdata is None or event.ydata is None:   # FIX 2
                    return

                idx = np.argmin((x - event.xdata) ** 2)
                val_y = y_ma[idx]
                point = (idx, val_y)

                if point not in self.selected_points:
                    self.selected_points.append(point)
                    self.val_x.append(idx)
                    self.val_y.append(val_y)

                punti_testo = "\n".join([f"({px},{py})" for px, py in self.selected_points])
                self.info_label.setText(f"Punti selezionati:\n{punti_testo}")

                self.ax.plot(idx, val_y, 'o', color='red', markersize=10)
                canvas.draw()

                self.update_plot()

                if self.show_checkbox.isChecked():
                    self.update_su_eu()

            figure.canvas.mpl_connect('button_press_event', on_click)

        self.choose_window.show()

        try:
            diametro_input = float(self.diam_input.text())
        except ValueError:
            diametro_input = 0  # se il campo non è numerico

        if diametro_input <= 0:
            # Apri finestra di input per inserire il diametro
            file_name = self.files[self.current_index]
            new_diam, ok = QInputDialog.getDouble(
                self.choose_window,                           # parent
                "Inserisci il diametro del campione",        # titolo fisso
                f"Stai processando il file: {file_name}\nInserire il diametro del campione [mm]:",  # testo su due righe
                100.0,                                       # valore di default
                0.01,                                        # min
                1000.0,                                      # max
                2                                            # decimali
            )
            if ok:
                # l'utente ha confermato un valore valido
                self.diam_input.setText(str(new_diam))
                self.diametro = new_diam
            else:
                # l'utente ha annullato → resta nella finestra
                self.choose_window.raise_()
                self.choose_window.activateWindow()
                return 

    def on_diameter_changed(self):
        try:
            diametro = float(self.diam_input.text())
            if diametro <= 0:
                return
        except ValueError:
            return

        # salva il nuovo diametro
        NEW_DIAM[self.current_index] = diametro

        # ricalcola sforzo e grafico
        self.update_plot()

        # ricalcola SU ed EU se abilitato
        if self.show_checkbox.isChecked():
            self.update_su_eu()

    def toggle_modulo(self, state):
        """Aggiorna la label solo se la checkbox è attiva"""
        if state == 2:  # Checkbox selezionata
            self.update_su_eu()
        else:
            self.mod_label.setText("Sforzo ultimo non calcolato")
            self.mod_label2.setText("Deformazione ultima non calcolata")
            SU[self.current_index] = np.nan
            EU[self.current_index] = np.nan

    def update_su_eu(self):
        """Calcola SU/EU solo se ci sono almeno 5 punti e SFOR/EPS sono validi"""
        if len(self.val_x) < 5:
            self.mod_label.setText("Sforzo ultimo non disponibile\nSeleziona almeno 5 punti")
            self.mod_label2.setText("Deformazione ultima non disponibile\nSeleziona almeno 5 punti")
            SU[self.current_index] = np.nan
            EU[self.current_index] = np.nan
            return

        current_sforzo = SFOR[self.current_index]
        current_eps = EPS[self.current_index]

        if current_sforzo is None or len(current_sforzo) == 0:
            self.mod_label.setText("Sforzo ultimo non disponibile")
            self.mod_label2.setText("Deformazione ultima non disponibile")
            SU[self.current_index] = np.nan
            EU[self.current_index] = np.nan
            return

        idx_max = np.argmax(np.abs(current_sforzo))
        SU[self.current_index] = current_sforzo[idx_max]
        EU[self.current_index] = current_eps[idx_max]

        self.mod_label.setText(f"Sforzo ultimo: {SU[self.current_index]:.2f} MPa")
        self.mod_label2.setText(f"Deformazione ultima: {EU[self.current_index]:.2f} μm/m")





    def res_zoom(self):
        self.ax.relim()       # ricalcola limiti dai dati
        self.ax.autoscale()   # applica limiti calcolati
        self.choose_canvas.draw()    


    def canc_valori(self):
        self.val_x.clear()
        self.val_y.clear()
        self.selected_points.clear()
        self.info_label.setText("Punti selezionati:")

        self.ax.clear()

        if self.col1:
            y = np.concatenate(self.col1)
            window = 100
            if len(y) < window:
                window = max(1, len(y) // 5)
            y_ma  = self.moving_average(y, window)
            x = np.arange(len(y))



            self.line, = self.ax.plot(x, y_ma, color='blue', picker=1)

        self.choose_canvas.draw() 
        self.update_plot() 
    
    
    def salva_chiudi(self):
        self.update_plot()

        

        
        try:
            diametro_input = float(self.diam_input.text())
        except ValueError:
            diametro_input = 0  # se il campo non è numerico

        if diametro_input <= 0:
            # Apri finestra di input per inserire il diametro
            new_diam, ok = QInputDialog.getDouble(
                self.choose_window,              # parent
                "Inserisci diametro",            # titolo
                "Inserire il diametro del campione [mm]:",  # label
                100.0,      # valore di default
                0.01,       # min
                1000.0,     # max
                2           # decimali
            )
            if ok:
                # l'utente ha confermato un valore valido
                self.diam_input.setText(str(new_diam))
                self.diametro = new_diam
            else:
                # l'utente ha annullato → resta nella finestra
                self.choose_window.raise_()
                self.choose_window.activateWindow()
                return

        if len(self.val_x) < 5:
            QMessageBox.warning(
                self.choose_window,   # <-- parent corretto
                "Attenzione",
                "Seleziona almeno 5 punti per calcolare!"
            )

            # Riporta la finestra in primo piano
            self.choose_window.raise_()
            self.choose_window.activateWindow()
            return

        # ✅ SOLO ORA puoi chiudere la finestra
        if hasattr(self, "choose_window") and self.choose_window is not None:
            self.choose_window.close()
            
        # Intervallo per Δε e Δσ (primi due punti -> low, secondi due punti -> high)
        start_idx = min(self.val_x[0], self.val_x[1])
        end_idx = max(self.val_x[0], self.val_x[1]) + 1

        start_idx2 = min(self.val_x[2], self.val_x[3])
        end_idx2 = max(self.val_x[2], self.val_x[3]) + 1

        # --- CONCATENA DATI ---
        col1  = np.concatenate(self.col1)
        col34 = np.concatenate(self.col34)
        col56 = np.concatenate(self.col56)
        col78 = np.concatenate(self.col78)

        # --- FINESTRA MEDIA MOBILE ---
        window = 100
        if len(col1) < window:
            window = max(1, len(col1) // 5)

        # --- MEDIA MOBILE (SOLO PER PLOT) ---
        col1_ma  = self.moving_average(col1, window)
        col34_ma = self.moving_average(col34, window)
        col56_ma = self.moving_average(col56, window)
        col78_ma = self.moving_average(col78, window)

        # --- GRANDEZZE FISICHE ---
        E1 = col34_ma * -10000
        E2 = col56_ma * -10000
        E3 = col78_ma * -10000
        E  = (E1 + E2 + E3) / 3

        self.delta_e1 = np.mean(E1[start_idx2:end_idx2])-np.mean(E1[start_idx:end_idx])
        self.delta_e2 = np.mean(E2[start_idx2:end_idx2])-np.mean(E2[start_idx:end_idx])
        self.delta_e3 = np.mean(E3[start_idx2:end_idx2])-np.mean(E3[start_idx:end_idx])
        self.delta_e = np.mean(E[start_idx2:end_idx2])-np.mean(E[start_idx:end_idx])

        # Calcolo sforzo Δσ1
        try:
            diametro = float(self.diam_input.text())
            area = math.pi * (diametro/2)**2 / 1000
        except ValueError:
            area = 1
        window = 100
        if len(col1) < window:
            window = max(1, len(col1) // 5)

        # --- MEDIA MOBILE (SOLO PER PLOT) ---
        col1_ma  = self.moving_average(col1, window)
        sforzo = col1_ma/(-area)
        self.delta_s = np.mean(sforzo[start_idx2:end_idx2])-np.mean(sforzo[start_idx:end_idx])

        # --- Aggiorna il vettore globale nella posizione del file corrente ---
        if self.delta_e != 0:
            Modulo_elastico[self.current_index] = self.delta_s / self.delta_e * 1000
            Delta_sforzo[self.current_index] = self.delta_s
            Delta_epsilon[self.current_index] = self.delta_e
            Delta_epsilon1[self.current_index] = self.delta_e1
            Delta_epsilon2[self.current_index] = self.delta_e2
            Delta_epsilon3[self.current_index] = self.delta_e3
        else:
            Modulo_elastico[self.current_index] = np.nan
            Delta_sforzo[self.current_index] = np.nan
            Delta_epsilon[self.current_index] = np.nan
            Delta_epsilon1[self.current_index] = np.nan
            Delta_epsilon2[self.current_index] = np.nan
            Delta_epsilon3[self.current_index] = np.nan

        NEW_DIAM[self.current_index] = float(self.diam_input.text())

        # Aggiorna tabella
        self.reset_labels()




from PySide6.QtWidgets import QCheckBox, QWidget

class IntroPage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)  # margini interni della finestra
        layout.setSpacing(10)  # spazio tra widget

        # --- Immagine ---
        self.image_label = QLabel()
        pixmap = QPixmap(":/logo.jpeg")
        self.image_label.setPixmap(pixmap)  # inizialmente originale
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label, stretch=1)  # stretch maggiore: occupa più spazio possibile

        # --- Testo di benvenuto ---
        label = QLabel("Procedura per il calcolo del modulo elastico con misure tramite DIC")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, stretch=0)  # stretch 0: spazio minimo

        # --- Bottone per iniziare ---
        start_btn = QPushButton("Inizia!")
        start_btn.setFixedHeight(40)  # altezza minima e costante
        layout.addWidget(start_btn, stretch=0)  # stretch 0: spazio minimo
        start_btn.clicked.connect(self.go_to_page1)

        # --- Rende l'immagine adattabile quando si ridimensiona la finestra ---
        self.image_label.setScaledContents(True)  # scala contenuto al widget
        self.image_label.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )  # permette di crescere con la finestra

    def go_to_page1(self):
        self.stack.setCurrentIndex(1)


class Page3(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        layout = QVBoxLayout(self)  # layout principale

        # Titolo
        label = QLabel("Riepilogo Modulo Elastico per file selezionati:")
        layout.addWidget(label)

        # Tabella + bottoni
        tb_layout = QHBoxLayout()  # ❌ rimosso 'self'

        self.table = QTableWidget()
        tb_layout.addWidget(self.table)

        bot_layout = QVBoxLayout()  # ❌ rimosso 'self'
        self.sall = QPushButton("Seleziona tutti")
        self.dall = QPushButton("Deseleziona tutto")
        self.exp = QPushButton("Esporta i dati selezionati della tabella")

        bot_layout.addWidget(self.sall)
        bot_layout.addWidget(self.dall)
        bot_layout.addWidget(self.exp)
        
        tb_layout.addLayout(bot_layout)
        layout.addLayout(tb_layout)

        # collegamenti bottoni
        self.sall.clicked.connect(self.select_all)
        self.dall.clicked.connect(self.deselect_all)
        self.exp.clicked.connect(self.export_selected_to_txt)

        # --- AREA PER IL GRAFICO ---
        self.figure = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        layout_btn = QHBoxLayout()
        plot_btn = QPushButton("Crea il grafico per i file selezionati")
        layout_btn.addWidget(plot_btn)
        plot_btn.clicked.connect(self.plot_selected_files)

        curve_btn = QPushButton("Visualizza curve σ-ε")
        layout_btn.addWidget(curve_btn)
        curve_btn.clicked.connect(self.open_curve_plot)

        layout.addLayout(layout_btn)

        # Bottone per tornare alla home
        layout_botton = QHBoxLayout()
        prc_btn = QPushButton("Torna ad analizza dati")
        layout_botton.addWidget(prc_btn)
        home_btn = QPushButton("Torna a seleziona file")
        layout_botton.addWidget(home_btn)
        layout.addLayout(layout_botton)
        home_btn.clicked.connect(self.go_home)
        prc_btn.clicked.connect(self.go_page2)

        # Lista dei checkbox
        self.checkboxes = []
        self.selected_indices = []

    def go_page2(self):
        self.stack.setCurrentIndex(2)

    def select_all(self):
        for chk in self.checkboxes:
            chk.setChecked(True)

    def deselect_all(self):
        for chk in self.checkboxes:
            chk.setChecked(False)


    def export_selected_to_txt(self):
        # Prendi gli indici delle righe selezionate tramite checkbox
        selected_indices = self.get_selected_positions()
        if not selected_indices:
            QMessageBox.warning(self, "Attenzione", "Seleziona almeno una riga da esportare!")
            return

        # Chiedi percorso di salvataggio
        file_path, _ = QFileDialog.getSaveFileName(self, "Salva TXT", "", "Text Files (*.txt)")
        if not file_path:
            return
        if not file_path.endswith(".txt"):
            file_path += ".txt"

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                # Scrivi intestazioni (escludendo ultima colonna checkbox)
                headers = [self.table.horizontalHeaderItem(c).text() for c in range(self.table.columnCount() - 1)]
                f.write("\t".join(headers) + "\n")

                # Scrivi i dati delle righe selezionate
                for idx in selected_indices:
                    row = []
                    for c in range(self.table.columnCount() - 1):  # escludo checkbox
                        item = self.table.item(idx, c)
                        row.append(item.text() if item else "")
                    f.write("\t".join(row) + "\n")

            QMessageBox.information(self, "Successo", f"Dati esportati correttamente in:\n{file_path}")

        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Impossibile esportare i dati:\n{e}")
    
    def reset_figure(self):
        """Pulisce la figura e prepara un canvas vuoto."""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_title("Seleziona dei file per visualizzare il grafico")
        ax.set_xlabel("File")
        ax.set_ylabel("Modulo Elastico [GPa]")
        ax.grid(True)
        self.canvas.draw()  
               
    def populate_table(self, files, NEW_DIAM, Delta_epsilon1, Delta_epsilon2, Delta_epsilon3,
                       Delta_epsilon, Delta_sforzo, Modulo_elastico,EU,SU):
        self.table.clear()
        self.reset_figure()
        self.checkboxes.clear()  # reset lista checkbox

        # Imposto colonne: 8 originali + 2 nuove
        self.table.setColumnCount(11)
        self.table.setHorizontalHeaderLabels([
            "File", "Diametro [mm]", "Δε1 [μm/m]", "Δε2 [μm/m]", "Δε3 [μm/m]",
            "Δεₘ [μm/m]", "Δσ [MPa]", "E [GPa]",
            "εᵤₘ [μm/m]", "σᵤ [MPa]","Esporta"
        ])
        self.table.setRowCount(len(files))

        for i, file in enumerate(files):
            self.table.setItem(i, 0, QTableWidgetItem(file))
            self.table.setItem(i, 1, QTableWidgetItem(f"{NEW_DIAM[i]:.2f}"))
            self.table.setItem(i, 2, QTableWidgetItem(f"{Delta_epsilon1[i]:.2f}" if not np.isnan(Delta_epsilon1[i]) else "NaN"))
            self.table.setItem(i, 3, QTableWidgetItem(f"{Delta_epsilon2[i]:.2f}" if not np.isnan(Delta_epsilon2[i]) else "NaN"))
            self.table.setItem(i, 4, QTableWidgetItem(f"{Delta_epsilon3[i]:.2f}" if not np.isnan(Delta_epsilon3[i]) else "NaN"))
            self.table.setItem(i, 5, QTableWidgetItem(f"{Delta_epsilon[i]:.2f}" if not np.isnan(Delta_epsilon[i]) else "NaN"))
            self.table.setItem(i, 6, QTableWidgetItem(f"{Delta_sforzo[i]:.2f}" if not np.isnan(Delta_sforzo[i]) else "NaN"))
            self.table.setItem(i, 7, QTableWidgetItem(f"{Modulo_elastico[i]:.2f}" if not np.isnan(Modulo_elastico[i]) else "NaN"))
            self.table.setItem(i, 8, QTableWidgetItem(f"{EU[i]:.2f}" if not np.isnan(EU[i]) else "NaN"))
            self.table.setItem(i, 9, QTableWidgetItem(f"{SU[i]:.2f}" if not np.isnan(SU[i]) else "NaN"))

            # --- Checkbox per selezione ---
            chk_widget = QWidget()
            chk = QCheckBox()
            chk_widget_layout = QVBoxLayout(chk_widget)
            chk_widget_layout.addWidget(chk)
            chk_widget_layout.setAlignment(Qt.AlignCenter)
            chk_widget_layout.setContentsMargins(0, 0, 0, 0)
            self.table.setCellWidget(i, 10, chk)
            self.checkboxes.append(chk)

            # Collego il checkbox a funzione che aggiorna colonna
            # chk.stateChanged.connect(lambda state, row=i: self.update_repeated_modulo(row))

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    # def update_repeated_modulo(self, row):
    #     if self.checkboxes[row].isChecked():
    #         val = self.table.item(row, 7).text()  # Modulo elastico originale
    #         self.table.setItem(row, 9, QTableWidgetItem(val))
    #     else:
    #         self.table.setItem(row, 9, QTableWidgetItem(""))

    def go_home(self):
        self.stack.setCurrentIndex(1)

    def get_selected_positions(self):
        """Restituisce una lista degli indici delle righe selezionate."""
        selected_indices = []
        for i, chk in enumerate(self.checkboxes):
            if chk.isChecked():
                selected_indices.append(i)
        return selected_indices

    def plot_selected_files(self):
        """Plot a barre dei moduli elastici dei file selezionati."""
        self.selected_indices = self.get_selected_positions()
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        if not self.selected_indices:
            ax.text(0.5, 0.5, "Nessun file selezionato", ha='center', va='center')
        else:
            valori_moduli = []
            etichette = []

            for idx in self.selected_indices:
                try:
                    val = float(self.table.item(idx, 7).text())  # colonna Modulo Elastico
                    valori_moduli.append(val)
                    etichette.append(str(idx + 1))  # 🔢 numero riga (1-based)
                except:
                    continue

            x = np.arange(len(valori_moduli))

            ax.bar(x, valori_moduli)
            ax.set_ylabel("Modulo Elastico [GPa]")
            ax.set_xlabel("Numero file (riga tabella)")
            ax.set_xticks(x)
            ax.set_xticklabels(etichette)
            ax.set_ylim(0.8 * min(valori_moduli), 1.2 * max(valori_moduli))
            ax.grid(True)
            ax.set_title("Numerazione riferita alla tabella (riga 1 → primo file)")
        self.canvas.draw()    



    def open_curve_plot(self):
        """Apri il grafico EPS vs SFOR in una finestra separata (PyQt6) con bottoni per esportare o chiudere."""
        selected_indices = self.get_selected_positions()
        if not selected_indices:
            return

        # Finestra separata
        dialog = QDialog(self)
        dialog.setWindowTitle("Curve σ-ε")
        dialog.resize(1200, 800) 
        
        layout = QVBoxLayout(dialog)

        # Canvas matplotlib
        fig = Figure(figsize=(5, 6))
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)
        ax = fig.add_subplot(111)

        # Plot dei file selezionati
        for idx in selected_indices:
            try:
                vx = np.array(EPS[idx])
                vy = np.array(SFOR[idx])
                nom = P_FILE[idx]

                if vx.size == 0 or vy.size == 0 or np.all(np.isnan(vx)) or np.all(np.isnan(vy)):
                    continue

                ax.plot(vx, vy, label=nom)
            except Exception as e:
                print(f"Errore nel plot del file {idx} ({nom}): {e}")
                continue

        ax.set_xlabel("Deformazioni [μm/m]")
        ax.set_ylabel("Sforzo [MPa]")
        ax.legend()
        ax.grid(True)
        canvas.draw()

        # --- Bottoni sotto il grafico ---
        btn_layout = QHBoxLayout()

        btn_close = QPushButton("Chiudi grafico")
        btn_close.clicked.connect(dialog.close)

        btn_export = QPushButton("Esporta valori della curva σ-ε")
        btn_save_plot = QPushButton("Salva grafico come immagine")
        btn_layout.addWidget(btn_export)
        btn_layout.addWidget(btn_save_plot)
        btn_layout.addWidget(btn_close)
        layout.addLayout(btn_layout)
        btn_save_plot.clicked.connect(lambda: self.salva_plot(fig))

        # --- Funzione di esportazione in TXT colonne affiancate ---
        def export_eps_sfor_columns():
            file_path, _ = QFileDialog.getSaveFileName(dialog, "Salva EPS e SFOR", "", "Text Files (*.txt)")
            if not file_path:
                return
            if not file_path.endswith(".txt"):
                file_path += ".txt"

            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    # Troviamo la lunghezza massima delle serie
                    max_len = max([len(EPS[idx]) for idx in selected_indices])

                    # Scriviamo intestazioni: una coppia EPS/SFOR per ogni file
                    header = []
                    for idx in selected_indices:
                        header.append(f"{P_FILE[idx]}_EPS")
                        header.append(f"{P_FILE[idx]}_SFOR")
                    f.write("\t".join(header) + "\n")

                    # Scriviamo i valori riga per riga, affiancati
                    for i in range(max_len):
                        row = []
                        for idx in selected_indices:
                            vx = EPS[idx]
                            vy = SFOR[idx]
                            # Se la serie è più corta, riempi con vuoto
                            row.append(f"{vx[i]:.6f}" if i < len(vx) else "")
                            row.append(f"{vy[i]:.6f}" if i < len(vy) else "")
                        f.write("\t".join(row) + "\n")

                QMessageBox.information(dialog, "Successo", f"Dati EPS e SFOR esportati in:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(dialog, "Errore", f"Impossibile esportare i dati:\n{e}")

        btn_export.clicked.connect(export_eps_sfor_columns)

        dialog.exec()


    def salva_plot(self, figure):
        """Salva il grafico corrente in formato JPEG."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Salva grafico",
            "",
            "JPEG Image (*.jpg *.jpeg)"
        )

        if not file_path:
            return

        if not (file_path.lower().endswith(".jpg") or file_path.lower().endswith(".jpeg")):
            file_path += ".jpg"

        try:
            figure.savefig(
                file_path,
                dpi=300,
                format="jpeg",
                bbox_inches="tight"
            )
            QMessageBox.information(
                self,
                "Salvataggio completato",
                f"Grafico salvato correttamente in:\n{file_path}"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Errore",
                f"Errore nel salvataggio del grafico:\n{e}"
            )    



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Procedurea per elaborazione dati delle prove di modulo con DIC")
        self.resize(1200, 800)

        layout = QVBoxLayout(self)
        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        self.intro_page = IntroPage(self.stack)
        self.page1 = Page1(self.stack)
        self.page2 = Page2(self.stack)
        self.page3 = Page3(self.stack)

        self.stack.addWidget(self.intro_page)
        self.stack.addWidget(self.page1)
        self.stack.addWidget(self.page2)
        self.stack.addWidget(self.page3)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
