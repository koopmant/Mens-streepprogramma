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
WACHTWOORD = "Wachtwoord"
WACHTTIJD = 1000 #in miliseconden
debuggen = False

#===============================================================================
# Controleer of benodigde bestanden bestaan, stop anders direct en toon missende 
# bestanden in errorlog.
#===============================================================================

try:
    missingfiles=[]
    for essentialfile in ['Streeplijst_0000-00.csv','Images\\menslogo.png',\
                          'Images\\Bier.png','Images\\Fris.png','Images\\Snoep.png',\
                          'Images\\Koek.png','Images\\Tosti.png','Images\\Wijn.png',\
                          'Images\\Sterk.png','Images\\Soep.png','Images\\Chips.png']:
        if not os.path.isfile(essentialfile):
            missingfiles.append(essentialfile)
    if not missingfiles == []:
        raise IOError('---'+time.strftime("%Y-%m-%d - %H:%M:%S")+'--- Bestand(en) niet aanwezig. Zo kan ik toch niet werken...', missingfiles)
except IOError as err:
    sys.exit(err.args)

producten=[["Fris",PRIJS_FRIS],["Tosti",PRIJS_TOSTI],["Soep",PRIJS_SOEP],["Snoep",PRIJS_SNOEP],["Koek",PRIJS_KOEK],["Chips",PRIJS_CHIPS],["Bier",PRIJS_BIER],["Wijn",PRIJS_WIJN],["Sterk",PRIJS_STERK]]


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
        tk.Frame.configure(self,background = self.Achtergrondkleur)
        
        self.pack(side="top", fill="both", expand=True)
        # Invoer van eigen naam
        self.naam = tk.Entry(self, justify=tk.CENTER, font="Calibri, 20", bd=0)
        self.naam.pack(ipady=20, padx=100, pady=50)
        self.naam.bind("<Return>", self.check_name)
        
        # Informatie ruimte
        self.response = tk.Text(self, font="Calibri, 16", bd=0, width=25, height=4, bg=self.Achtergrondkleur, wrap=tk.WORD)
        self.response.tag_configure("center", justify='center')
        self.response.pack(padx=100)
        
        # Mens-logo
        ML = Image.open('Images\menslogo.png')
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
            self.response.insert(1.0, "\nNaam onbekend, probeer opnieuw.")
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
        # Mens-logo
        ML = Image.open('menslogo.png')
        achtergrond = ImageTk.PhotoImage(ML.resize((408,432), Image.ANTIALIAS))
        self.backlabel = tk.Label(self, bg=self.Achtergrondkleur, image= achtergrond)
        self.backlabel.image = achtergrond
        self.backlabel.pack(pady=50)
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
        self.lettertype = ("Calibri, 16")
        tk.Frame.configure(self,background = self.Achtergrondkleur)
        self.images = {}
        self.gestreept = {}
        self.buttons = {}
        for P in producten:
            self.images[P[0]] = ImageTk.PhotoImage(Image.open("Images\\"+P[0]+".png"))
            self.gestreept[P[0]] = 0
        
        self.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        for x in range(7):
            tk.Grid.columnconfigure(self, x, weight=1)
        
        for y in range(18):
            tk.Grid.rowconfigure(self, y, weight=1)
        
        action = lambda: self.doe_aankoop()
        self.stopknop = tk.Button(self, text = "Doe aankoop", command = action, font=self.lettertype).grid(row = 1, column = 2, sticky=tk.N+tk.S+tk.E+tk.W)
        self.tekst_naam = tk.Text(self, width=20, height = 2, bd=0, background = self.Achtergrondkleur, font=self.lettertype)
        self.tekst_naam.tag_configure("center", justify='center')
        self.tekst_naam.grid(row = 1, column = 5, sticky=tk.N+tk.S+tk.E+tk.W)
        self.tekst_consumptie = tk.Text(self, width=30, bd=0, bg=self.Achtergrondkleur, font=self.lettertype)
        self.tekst_consumptie.grid(row = 2, column = 5, rowspan = 2, sticky=tk.N+tk.S+tk.E+tk.W)
        self.tekst_nu_gestreept = tk.Text(self, width=30, height=10, bd=0, bg=self.Achtergrondkleur, font=self.lettertype)
        self.tekst_nu_gestreept.grid(row = 4, column = 5, sticky=tk.N+tk.S+tk.E+tk.W)
        
        self.euro = u"\u20AC"
                
        posrow=2; poscol=1
        for P in producten:
            action = lambda x = P[0]: self.nu_gestreept(x)
            tk.Button(self, image=self.images[P[0]], text="%s %.2f" %(self.euro, P[1]), compound="top", font=self.lettertype, bd=0, bg=self.Achtergrondkleur, command=action).grid(row=posrow, column=poscol)
            if poscol==3:
                poscol=1
                posrow+=1
            else:
                poscol+=1
    
    def voorbereiding(self):
        # Deze functie wordt opgeroepen voor het frame naar voren wordt gebracht.
        self.tekst_naam.insert(0.0, "\nHoi "+self.controller.content+"!")
        self.tekst_naam.tag_add("center", 0.0, "end")
        al_gestreept = "\n\nHuidige aantal consumpties:\n\n"
        for lid in leden.rij:
            if lid.naam == self.controller.content:
                for P in producten:
                    if lid.aantal[P[0]] > 0:
                        al_gestreept += P[0]+": \t\t%.0f \n" %(lid.aantal[P[0]])
                self.tekst_consumptie.insert(0.0, al_gestreept+"_______________________\nHuidig saldo \t\t%s %.2f" %(self.euro, lid.hoeveelheid_geld))
        
    def doe_aankoop(self):
        for lid in leden.rij:
            if lid.naam == self.controller.content:
                lid.hoeveelheid_geld += self.additief_saldo
                for P in producten:
                    lid.aantal[P[0]] += self.gestreept[P[0]]
                    self.gestreept[P[0]]=0
        self.controller.show_frame(LoginScherm)
        self.tekst_consumptie.delete(0.0, tk.END)
        self.tekst_nu_gestreept.delete(0.0, tk.END)
        self.tekst_naam.delete(0.0, tk.END)
        
    def nu_gestreept(self, artikel):
        self.gestreept[artikel]+=1
        self.tekst_nu_gestreept.delete(0.0, tk.END)
        self.additief_saldo=0
        nu_gestreept = ""
        for P in producten:
            if self.gestreept[P[0]] > 0:
                nu_gestreept += P[0]+": \t\t%.0f \n" %(self.gestreept[P[0]])
                self.additief_saldo += self.gestreept[P[0]]*P[1]
        for lid in leden.rij:
            if lid.naam == self.controller.content:
                nu_gestreept += "_______________________\nAdditief saldo \t\t%s %.2f\n\n_______________________\nNieuw saldo \t\t%s %.2f" %(self.euro, self.additief_saldo, self.euro, lid.hoeveelheid_geld+self.additief_saldo)
        self.tekst_nu_gestreept.insert(0.0, nu_gestreept)
        
    


class AdminScherm(tk.Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.Achtergrondkleur = "deep sky blue"
        tk.Frame.configure(self,background = self.Achtergrondkleur)

    def voorbereiding(self):
        # Deze functie wordt opgeroepen voor het frame naar voren wordt gebracht.
        pass
        
class Lid():
    def __init__(self, naam, fris, tosti, bier, sterk, wijn, koek, snoep, soep, chips, geld, geboortedatum):
        name = naam.split()
        self.voornaam = name[0]
        self.achternaam = ' '.join(name[1:len(name)])
        self.naam = str(naam)
        self.aantal={}
        self.aantal["Fris"] = int(fris)
        self.aantal["Tosti"] = int(tosti)
        self.aantal["Bier"] = int(bier)
        self.aantal["Sterk"] = int(sterk)
        self.aantal["Wijn"] = int(wijn)
        self.aantal["Snoep"] = int(snoep)
        self.aantal["Koek"] = int(koek)
        self.aantal["Soep"] = int(soep)
        self.aantal["Chips"] = int(chips)
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
            file_now2.writerow([volled_naam, row.aantal["Fris"], row.aantal["Tosti"], row.aantal["Bier"], row.aantal["Sterk"], \
                row.aantal["Wijn"], row.aantal["Koek"], row.aantal["Snoep"], row.aantal["Soep"], row.aantal["Chips"], row.hoeveelheid_geld, row.geboortedatum])
            totaal_fris += row.aantal["Fris"]
            totaal_tosti += row.aantal["Tosti"]
            totaal_bier += row.aantal["Bier"]
            totaal_koek += row.aantal["Koek"]
            totaal_sterk += row.aantal["Sterk"]
            totaal_wijn += row.aantal["Wijn"]
            totaal_snoep += row.aantal["Snoep"]
            totaal_chips += row.aantal["Chips"]
            totaal_soep += row.aantal["Soep"]
            totaal_geld += row.hoeveelheid_geld
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
                