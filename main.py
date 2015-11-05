import Tkinter as tk
import csv
import Image, ImageTk
import time
import tkMessageBox
import os, sys, shutil

#===============================================================================
# Aan te passen door Penningmeester AC
#===============================================================================
PRIJS_BIER = 0.70
PRIJS_TOSTI = 0.70
PRIJS_KOEK = 0.40
PRIJS_SNOEP = 0.60 
PRIJS_FRIS = 0.65
PRIJS_STERK = 1.00
PRIJS_WIJN = 0.85
PRIJS_SOEP = 0.50
PRIJS_CHIPS = 0.60

#===============================================================================
# Overige instellingen
#===============================================================================

VERSIE = "November 2015"
BUTTON_HEIGHT = 1
BUTTON_WIDTH = 15
WACHTWOORD = "Wachtwoord"
WACHTTIJD = 1000 #in miliseconden
debuggen = False

#===============================================================================
# Controleer of benodigde bestanden bestaan, stop anders direct en toon missende bestanden in errorlog.
#===============================================================================

try:
    missingfiles=[]
    for essentialfile in ['menslogo.png','Streeplijst_0000-00.csv']:
        if not os.path.isfile(essentialfile):
            missingfiles.append(essentialfile)
    if not missingfiles == []:
        raise IOError('404: Bestand(en) niet aanwezig. Zo kan ik toch niet werken...', missingfiles)
except IOError as err:
    sys.exit(err)


class MainApplication(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Streepsysteem Studievereniging Mens, versie %s" % (VERSIE))
        
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Fullscreen mogelijkheid
        self.fullscreenstate = True
        self.attributes("-fullscreen", self.fullscreenstate)
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.exit_fullscreen)
        
        if not debuggen:
            self.protocol("WM_DELETE_WINDOW", self.stop_programma)
        
        # Naam van de gebruiker
        self.content = ""

        self.frames = {}

        for F in (LoginScherm, StreepScherm, AdminScherm):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginScherm)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.voorbereiding()
        frame.tkraise()
        
    def toggle_fullscreen(self, event=None):
        self.fullscreenstate = not self.fullscreenstate
        self.attributes("-fullscreen", self.fullscreenstate)
        
    def exit_fullscreen(self, event=None):
        self.fullscreenstate = False
        self.attributes("-fullscreen", self.fullscreenstate)
        
    def stop_programma(self):        
        self.ww = tk.Entry(tk.Toplevel(), text="Wachtwoord")
        self.ww.pack()
        self.ww.bind('<Return>', self.controleer_einde)
        

    def controleer_einde(self, event=None):
        if self.ww.get()==WACHTWOORD:
            #self.destroy()
            tk.Tk.quit(self)
        else:
            tkMessageBox.showwarning("Wrong password", "The entered password is incorrect!")
        
class LoginScherm(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self,parent)
        self.Achtergrondkleur = "yellow"
        
        self.pack(side="top", fill="both", expand=True)
        # Invoer van eigen naam
        self.naam = tk.Entry(self, justify=tk.CENTER, font="Calibri, 20", bd=0)
        self.naam.pack(ipady=20, padx=100, pady=50)
        self.naam.bind("<Return>", self.check_name)
        
        # Informatie ruimte
        self.response = tk.Text(self, font="Calibri, 16", bd=0, width=25, height=4, bg=self.Achtergrondkleur, fg="black")
        self.response.tag_configure("center", justify='center')
        self.response.pack(padx=100)
        
        # Mens-logo
        ML = Image.open('menslogo.png')
        achtergrond = ImageTk.PhotoImage(ML.resize((408,432), Image.ANTIALIAS))
        self.backlabel = tk.Label(self, bg=self.Achtergrondkleur, image= achtergrond)
        self.backlabel.image = achtergrond
        self.backlabel.pack(pady=50)
        
    def voorbereiding(self):
        # Roep deze functie op voor het frame naar voren wordt gebracht.
        self.response.delete(1.0,tk.END)
        self.naam.delete(0, tk.END)
        self.naam.focus()
        
    def check_name(self, event):
        first_name = self.naam.get().title().strip()
        self.response.configure(bg=self.Achtergrondkleur, fg="black")
        if voornamen.count(first_name) == 0:
            self.response.delete(1.0,tk.END)
            self.response.insert(1.0, "Naam onbekend, \nprobeer opnieuw.")
            self.response.tag_add("center", 1.0, "end")
            self.response.configure(background = "red4", fg = "snow")            
        elif voornamen.count(first_name) == 1:
            for lid in leden.rij:
                if first_name == lid.voornaam:
                    vol_naam = "%s %s" %(lid.voornaam, lid.achternaam)
                    self.controller.content = vol_naam
                    self.login_succes()
        else:
            self.response.delete(1.0,tk.END)
            self.response.insert(1.0, "Kies uw naam")
            self.response.tag_add("center", 1.0, "end")
            self.backlabel.destroy()
            self.nu_rij = []
            self.btn_dict = {}
            for lid in leden.rij:
                if first_name == lid.voornaam:
                    vol_naam = "%s %s" %(lid.voornaam, lid.achternaam)
                    self.nu_rij.append(vol_naam)
            for person in self.nu_rij:
                action = lambda x = person: self.reg_naam(x)
                self.btn_dict[person] = tk.Button(self, width = 40, text = person, \
                                            command = action, bg = 'thistle2', activebackground = "thistle3")
                self.btn_dict[person].pack()
    
    def reg_naam(self,vol_naam):
        self.controller.content = vol_naam
        for person in self.nu_rij:
            self.btn_dict[person].destroy()
        self.login_succes()
        
    def login_succes(self):
        # Welkom
        self.response.delete(1.0,tk.END)
        self.response.insert(1.0, "Welkom \n%s!" % (self.controller.content))
        self.response.tag_add("center", 1.0, "end")
        self.update_idletasks()
        time.sleep(.1)
        
        self.controller.show_frame(StreepScherm)
        
class StreepScherm(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.Achtergrondkleur = "medium spring green"
        
        self.grid()
        ML = Image.open('menslogo.png')
        achtergrond = ImageTk.PhotoImage(ML.resize((408,432), Image.ANTIALIAS))
        self.backlabel = tk.Label(self, bg=self.Achtergrondkleur, image= achtergrond)
        self.backlabel.image = achtergrond
        self.backlabel.grid(row= 100, column = 100)
        self.tekst_naam = tk.Text(self, width=40, height = 2, wrap = tk.WORD, background = self.Achtergrondkleur)
        self.tekst_naam.grid(row = 3, column = 0, sticky = tk.W, columnspan = 2)
        self.stopknop = tk.Button(self, text = "Afsluiten", command = self.controller.stop_programma, bg = 'red4', fg = "snow", \
                               activebackground = "red4", activeforeground = "snow")
        self.stopknop.grid(row = 0, column = 2, sticky = tk.E)
        euro = u"\u20AC"
        a = u"\u00E0"
        text1 = "%s %s " %(a, euro)
        self.lijst_wat2 = ["Fris", "Bier", "Tosti", "Snoep", "Koek", "Wijn", "Sterke drank", "Soep", "Chips"]
        self.lijst_wat3 = ["Fris", "Tosti", "Snoep", "Koek", "Soep", "Chips"]
        self.alg_lib = {"Fris": [PRIJS_FRIS, "Fris "+text1+"%.2f" %(PRIJS_FRIS), 'salmon', 'dark salmon'], \
                        "Bier": [PRIJS_BIER, "Bier "+text1+"%.2f" %(PRIJS_BIER),'OliveDrab1', 'OliveDrab3'], \
                        "Tosti": [PRIJS_TOSTI,  "Tosti "+text1+"%.2f" %(PRIJS_TOSTI), 'yellow', 'yellow3'], \
                        "Snoep": [PRIJS_SNOEP, "Snoep "+text1+"%0.2f" %PRIJS_SNOEP, 'orange red', "OrangeRed3"], \
                        "Koek": [PRIJS_KOEK, "Koek "+text1+"%.2f" %(PRIJS_KOEK), 'MediumPurple1', "MediumPurple3"], \
                        "Wijn": [PRIJS_WIJN, "Wijn "+text1+"%.2f" %PRIJS_WIJN,'spring green', "SpringGreen3"],\
                        "Sterke drank": [PRIJS_STERK, "Sterke drank "+text1+"%.2f" %PRIJS_STERK, 'sky blue', "SkyBlue3"],\
                        "Soep": [PRIJS_SOEP, "Soep "+text1+"%.2f" %PRIJS_SOEP, 'maroon1', "maroon2"],\
                        "Chips": [PRIJS_CHIPS, "Chips "+text1+"%.2f" %PRIJS_CHIPS, 'gray70', "gray60"]}
        self.bestelling = tk.Text(self, width = 40, height = 1, wrap = tk.WORD)
        self.bestelling.delete(0.0, tk.END)  
        self.bestelling.grid(row = 50, column = 0, columnspan = 2, sticky = tk.W)
    
    def voorbereiding(self):
        # Deze functie wordt opgeroepen voor het frame naar voren wordt gebracht.
        self.tekst_naam.delete(1.0, tk.END)
        message = "Geregistreerd als "+self.controller.content+", kies uw consumptie. \n"
        self.tekst_naam.insert(0.0, message)
        self.tekst_naam.configure(background = "green2", fg = "black")
        if self.controller.content in minderjarigen:
            self.lijst_wat = self.lijst_wat3
        else:
            self.lijst_wat = self.lijst_wat2
        pos = 0
        self.lib_knop = {}
        for artikel in self.lijst_wat:
            action = lambda x = artikel: self.doe_aankoop(x)
            self.lib_knop[artikel] = tk.Button(self, width = BUTTON_WIDTH, height = BUTTON_HEIGHT, text = self.alg_lib[artikel][1], \
                           bg = self.alg_lib[artikel][2], activebackground = self.alg_lib[artikel][3], command = action)
            self.lib_knop[artikel].grid(row = 4+pos, column = 0, sticky = tk.W)
            pos += 1
        self.verkeerd = tk.Button(self, width = BUTTON_WIDTH, height = 2*BUTTON_HEIGHT, text = "Ik heb \nverkeerd gestreept.", \
                               bg = "medium sea green", activebackground = "dark sea green", command=self.verkeerd_streep)
        self.verkeerd.grid(row = 4+pos+1, column = 0, sticky = tk.W)
        self.nu_gestreept()
        self.al_gestreept = []
        self.bestelling.delete(1.0, tk.END)
        self.bestelling.configure(bg = self.Achtergrondkleur)
        
    def verkeerd_streep(self):
        self.verkeerd.destroy()
        for artikel in self.lijst_wat:
            self.lib_knop[artikel].destroy()
        for lid in leden.rij:
            if lid.naam == self.controller.content:
                if lid.aantal_bier+lid.aantal_chips+lid.aantal_fris+lid.aantal_koekjes==0+lid.aantal_snoep+lid.aantal_soep+lid.aantal_sterke_drank+lid.aantal_tosti+lid.aantal_wijn==0:
                    self.doorgaan = tk.Button(self, width = BUTTON_WIDTH, height = 10*BUTTON_HEIGHT, text = "U hebt nog niets gestreepd deze maand. Neem contact op met AC of Bestuur om fouten in de voorgaande maand te wijzigen.", bg = "pale green", \
                                        activebackground = "spring green", wraplength=BUTTON_WIDTH*6,command = self.na_fout) 
                    self.doorgaan.grid(row = 6, column = 0, sticky = tk.W) 
                else: 
                    if lid.aantal_bier > 0:
                        self.al_gestreept.append("Bier")
                    if lid.aantal_chips > 0:
                        self.al_gestreept.append("Chips")
                    if lid.aantal_fris > 0:
                        self.al_gestreept.append("Fris")                    
                    if lid.aantal_koekjes > 0:
                        self.al_gestreept.append("Koek")
                    if lid.aantal_snoep > 0:
                        self.al_gestreept.append("Snoep")                    
                    if lid.aantal_soep > 0:
                        self.al_gestreept.append("Soep")                    
                    if lid.aantal_sterke_drank > 0:
                        self.al_gestreept.append("Sterke drank")                    
                    if lid.aantal_tosti >= 1:
                        self.al_gestreept.append("Tosti")                    
                    if lid.aantal_wijn >= 1:
                        self.al_gestreept.append("Wijn")     
                    pos = 0
                    self.lib_knop2 = {}
                    for artikel in self.al_gestreept:
                        action = lambda x = artikel: self.streep_weg(x)
                        self.lib_knop2[artikel] = tk.Button(self, width = BUTTON_WIDTH, height = BUTTON_HEIGHT, text = self.alg_lib[artikel][1],\
                                            bg = self.alg_lib[artikel][2], activebackground = self.alg_lib[artikel][3], command = action)
                        self.lib_knop2[artikel].grid(row = 4+pos, column = 0, sticky = tk.W)
                        pos += 1

    def na_fout(self):
        self.doorgaan.destroy()
        self.tekst3.destroy()
        self.na_bestelling()

    def streep_weg(self, artikel):
        wat_prijs = self.alg_lib[artikel][0]
        for lid in leden.rij:
            if lid.naam == self.controller.content:
                if artikel == "Fris":
                    lid.aantal_fris -= 1
                elif artikel == "Bier":
                    lid.aantal_bier -= 1
                elif artikel == "Chips":
                    lid.aantal_chips -= 1
                elif artikel == "Koekjes":
                    lid.aantal_koekjes -= 1 
                elif artikel == "Snoep":
                    lid.aantal_snoep -= 1
                elif artikel == "Tosti":
                    lid.aantal_tosti -= 1
                elif artikel == "Soep":
                    lid.aantal_soep -= 1
                elif artikel == "Sterke drank":
                    lid.aantal_sterke_drank -= 1
                elif artikel == "Wijn":
                    lid.aantal_wijn -= 1
                lid.hoeveelheid_geld -= wat_prijs
        self.bestelling = tk.Text(self, width = 40, height = 1, wrap = tk.WORD)
        self.bestelling.delete(0.0, tk.END)  
        self.bestelling.grid(row = 50, column = 0, columnspan = 2, sticky = tk.W)
        message = "Uw annulering is geregistreerd."
        self.bestelling.insert(0.0, message)
        self.bestelling.configure(bg = "green2")
        tk.Frame.after(self, WACHTTIJD, self.na_bestelling)
                    
    def doe_aankoop(self, artikel):
        wat_prijs = self.alg_lib[artikel][0]
        for lid in leden.rij:
            if lid.naam == self.controller.content:
                if artikel == "Fris":
                    lid.aantal_fris += 1
                elif artikel == "Bier":
                    lid.aantal_bier += 1
                elif artikel == "Chips":
                    lid.aantal_chips += 1
                elif artikel == "Koekjes":
                    lid.aantal_koekjes += 1 
                elif artikel == "Snoep":
                    lid.aantal_snoep += 1
                elif artikel == "Tosti":
                    lid.aantal_tosti += 1
                elif artikel == "Soep":
                    lid.aantal_soep += 1
                elif artikel == "Sterke drank":
                    lid.aantal_sterke_drank += 1
                elif artikel == "Wijn":
                    lid.aantal_wijn += 1
                lid.hoeveelheid_geld += wat_prijs
        self.gestreepd_artikel = artikel
        self.registreer_aankoop()
        
    def registreer_aankoop(self):
        message = "Uw bestelling is geregistreerd."
        self.bestelling.insert(0.0, message)
        self.bestelling.configure(bg = "green2")
        tk.Frame.after(self, WACHTTIJD, self.na_bestelling)
        self.opzien = tk.Text(self, bg = self.Achtergrondkleur, width = 100, height = 50)
        self.tijd = str()
        self.opzien.insert(1.0, self.tijd+":\t"+str(self.gestreepd_artikel)+"\n")
        
    def na_bestelling(self):
        self.controller.show_frame(LoginScherm)
        
    def nu_gestreept(self):
        for lid in leden.rij:
            if lid.naam == self.controller.content: 
                nu_gestreept2 = "Huidige aantal consumpties: \nFris: \t\t%.0f \nBier: \t\t%.0f \nTosti: \t\t%.0f \nSnoep: \t\t%.0f\
                \nKoek: \t\t%.0f \nWijn: \t\t%.0f \nSterke drank:  \t%.0f \nSoep: \t\t%.0f \nChips:\t\t%.0f \nDit komt totaal op %.2f euro." \
                %(lid.aantal_fris, lid.aantal_bier, lid.aantal_tosti, lid.aantal_snoep, lid.aantal_koekjes, lid.aantal_wijn, \
                  lid.aantal_sterke_drank, lid.aantal_soep, lid.aantal_chips, lid.hoeveelheid_geld)
                self.tekst3 = tk.Label(self, text = nu_gestreept2, bg = self.Achtergrondkleur, justify = tk.LEFT)
                self.tekst3.grid(row = 4, column = 1, rowspan = 9, sticky = tk.S)
    


class AdminScherm(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)

    def voorbereiding(self):
        # Deze functie wordt opgeroepen voor het frame naar voren wordt gebracht.
        pass
        
class Lid():
    def __init__(self, naam, fris, tosti, bier, sterke_drank, wijn, koekjes, snoep, soep, chips, geld, geboortedatum):
        name = naam.split()
        self.voornaam = name[0]
        self.achternaam = ' '.join(name[1:len(name)])
        self.naam = str(naam)
        self.aantal_fris = int(fris)
        self.aantal_tosti = int(tosti)
        self.aantal_bier = int(bier)
        self.aantal_sterke_drank = int(sterke_drank)
        self.aantal_wijn = int(wijn)
        self.aantal_snoep = int(snoep)
        self.aantal_koekjes = int(koekjes)
        self.aantal_soep = int(soep)
        self.aantal_chips = int(chips)
        self.hoeveelheid_geld = float(geld)
        self.geboortedatum = geboortedatum


        
class LedenLijst():
    def __init__(self):
        self.rij = []
        
    def add(self, lid):
        self.rij.append(lid)
        


def check_minderjarig(row):
    lid = row[11].split("-")
    dag = int(lid[0])
    maand = int(lid[1])
    jaar = int(lid[2])
    nu_jaar = int(time.strftime("%Y"))
    nu_maand = int(time.strftime("%m"))
    nu_dag = int(time.strftime("%d"))
    meerderjarig = False
    if (jaar+18) > nu_jaar:
        meerderjarig = True
    if (jaar+18) == nu_jaar:
        if maand > nu_maand:
            meerderjarig = True
        elif maand == nu_maand:
            if dag > nu_dag:
                meerderjarig = True
    return meerderjarig

maandlijstbestand = 'Streeplijst_'+time.strftime("%Y-%m")+'.csv'

# Als de lijst van deze maand nog niet bestaat, maak deze dan aan
if not os.path.isfile(maandlijstbestand):
    shutil.copyfile('Streeplijst_0000-00.csv', maandlijstbestand)

with open(maandlijstbestand, 'rb') as csvfile:
    file_now = csv.reader(csvfile, delimiter = ';')
    leden = LedenLijst()
    namen = []
    minderjarigen = []
    voornamen = []
    for row in file_now:
        if row[0] != 'Naam' and row[0] != 'Totaal' and row[0]!='Omzet' and row[0]!="Voorraad":
            lid = Lid(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11])
            leden.add(lid)
            namen.append(row[0])
            voornamen.append(row[0].split()[0])
            if check_minderjarig(row):
                minderjarigen.append(row[0])
        elif row[0] == 'Totaal':
            totaal_fris = int(row[1])
            totaal_tosti = int(row[2])
            totaal_bier = int(row[3])
            totaal_sterk = int(row[4])
            totaal_wijn = int(row[5])
            totaal_koek = int(row[6])
            totaal_snoep = int(row[7])
            totaal_soep = int(row[8])
            totaal_chips = int(row[9])
            totaal_geld = float(row[10])
        elif row[0] == 'Omzet':
            omzet_fris = float(row[1])
            omzet_tosti = float(row[2])
            omzet_bier = float(row[3])
            omzet_sterk = float(row[4])
            omzet_wijn = float(row[5])
            omzet_koek = float(row[6])
            omzet_snoep = float(row[7])
            omzet_soep = float(row[8])
            omzet_chips = float(row[9])
            totaal_omzet = float(row[10])
    
    
    root = MainApplication()
    root.mainloop()
    
    
    with open(maandlijstbestand+'temp', 'wb') as csvfile2:
        file_now2 = csv.writer(csvfile2, delimiter = ';')
        file_now2.writerow(['Naam', 'Fris', 'Tosti', 'Bier', 'Sterke drank', 'Wijn', 'Koek', 'Snoep', 'Soep', 'Chips', 'Geld', 'Geboortedatum'])    
        for row in leden.rij:
            volled_naam = "%s %s" %(row.voornaam, row.achternaam)
            file_now2.writerow([volled_naam, row.aantal_fris, row.aantal_tosti, row.aantal_bier, row.aantal_sterke_drank, \
                row.aantal_wijn, row.aantal_koekjes, row.aantal_snoep, row.aantal_soep, row.aantal_chips, row.hoeveelheid_geld, row.geboortedatum])
            totaal_fris += row.aantal_fris
            totaal_tosti += row.aantal_tosti
            totaal_bier += row.aantal_bier
            totaal_geld += row.hoeveelheid_geld
            totaal_koek += row.aantal_koekjes
            totaal_sterk += row.aantal_sterke_drank
            totaal_wijn += row.aantal_wijn
            totaal_snoep += row.aantal_snoep
            totaal_chips += row.aantal_chips
            totaal_soep += row.aantal_soep
        file_now2.writerow(['Totaal', totaal_fris, totaal_tosti, totaal_bier, totaal_sterk, totaal_wijn, totaal_koek, \
                            totaal_snoep, totaal_soep, totaal_chips, totaal_geld, " "])
        omzet_fris = totaal_fris*PRIJS_FRIS
        omzet_bier = totaal_bier*PRIJS_BIER
        omzet_chips = totaal_chips*PRIJS_CHIPS
        omzet_koek = totaal_koek*PRIJS_KOEK
        omzet_snoep = totaal_snoep*PRIJS_SNOEP
        omzet_soep = totaal_soep*PRIJS_SOEP
        omzet_sterk = totaal_sterk*PRIJS_STERK
        omzet_tosti = totaal_tosti*PRIJS_TOSTI
        omzet_wijn = totaal_wijn*PRIJS_WIJN
        totaal_omzet = omzet_bier+omzet_chips+omzet_fris+omzet_koek+omzet_snoep+omzet_soep+omzet_sterk+omzet_tosti+omzet_wijn
        file_now2.writerow(['Omzet', omzet_fris, omzet_tosti, omzet_bier, omzet_sterk, omzet_wijn, omzet_koek, omzet_snoep, omzet_soep,\
                            omzet_chips, totaal_omzet, " "])
    
shutil.copyfile(maandlijstbestand+'temp', maandlijstbestand)
os.remove(maandlijstbestand+'temp')
                