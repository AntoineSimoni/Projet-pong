from tkinter import *
from random import randrange
from time import *
X = 800 #taille de la fenetre en X
Y = 420 # taille de la fenetre en Y
SPEED = 8 #la vitesse de deplacement de la balle

COLOR = "white"
BGCOLOR = "black"

jeux = None
PLAY = False #est-ce qu'on est en train de jouer
JOUER = False

temps_start = 0
temps_fin = 0

class Pong : # la classe gerant la balle de pong
    def __init__(self): #le constructeur de la balle de pong
        self.tx = 10 # taille en X de la balle
        self.ty = 10 # taille en Y de la balle
        self.r1 = Raquette(30, Y/2-self.ty/2, "<z>","<s>") #on recup les deux raquettes pour plus tard check la hitbox
        self.r2 = Raquette(X-30, Y/2-self.ty/2, "<Up>","<Down>")
        self.dummy = randrange(0, 100) #une valeur aleatoire pour savoir vers qui va la balle
        self.J1 = 0
        self.J2 = 0
        self.x = X/2 - self.tx/2 #on place la balle au centre de l'ecran
        self.y = Y/2 - self.ty/2
        self.dx = 0 # on fixe le deplacement horizontal a 0, elle ira donc a plat et ne bougera pas
        if self.dummy < 50 : #si le dummy est < 50, la balle va a gauche sinon a droite
            self.dx = -1
        else :
            self.dx = 1

        self.dy = float(randrange(-100,100))/100 # on defini si la balle va monter ou descendre

        self.balle = terrain.create_rectangle(self.x, self.y, self.x + self.tx, self.y + self.ty, fill=COLORball)
				#on creer un rectangle qui va etre rempli avec une couleur
        self.deplacer()
				#on deplace la balle d'un cran
        tk.bind_all("<Return>", self.pause) #si return est press, met le jeu sur pause

    def pause(self, event): # met le jeu en pause ou non
        global PLAY
        if PLAY :
            PLAY = False
        else :
            PLAY = True

    def raffraichir(self): #on rafraichi la position de la bougie
        terrain.coords(self.balle, self.x, self.y, self.x+self.tx, self.y+self.ty)
        if self.J1 == point or self.J2 == point:
            menu_fin()

            
    def deplacer(self):
        global PLAY, x, y
        if PLAY :
            self.x += self.dx * SPEED #on deplace la balle sur dx, defini plus haut, a une vitesse donnée
            self.y += self.dy * SPEED #on deplace la balle sur dy, defini plus haut, a une vitesse donnée

            if self.y <= 0 or self.y >= Y-self.ty : #si on atteint un cote haut ou bas de l'ecran, on inverse la direction de dy
                self.dy =- self.dy
            if self.r1.y <= self.y + self.ty and self.r1.y + self.r1.ty >= self.y : #si on est entre le haut et le bas de la raquette 1
                if self.x <= self.r1.x + self.r1.tx and not self.x + self.tx <= self.r1.x: #si on touche sur l'axe X la raquette 1
                    self.dx =- self.dx #on inverse la direction de la balle sur X
                    self.dy = float(randrange(-100, 100))/100 #defini une nouvelle direction aleatoire sur Y

            if self.r2.y <= self.y + self.ty and self.r2.y + self.r2.ty >= self.y : #meme chose sur la raquette 2
                if self.x + self.tx >= self.r2.x and not self.x >= self.r2.x + self.r2.tx :
                    self.dx =- self.dx
                    self.dy = float(randrange(-100, 100))/100

            if self.x + self.tx < 0 : #si on touche la partie de droite de l'ecran (joueur 1 a perdu)
                self.x = X/2 - self.tx/2 #on reset la balle
                self.y = Y/2 - self.ty/2
                self.J2 += 1 #plus un point pour le J2
                self.dx =- self.dx  #on reset les directions 
                self.dy = float(randrange(-100, 100))/100
                self.r1.placer(30, Y/2-self.ty/2) #on replace les deux raquettes
                self.r2.placer(X-30, Y/2-self.ty/2)
                PLAY = False #on met le jeu en pause avant de redemarrer 


            if self.x+self.tx>X : #meme chose mais pour le joueur 2 qui a perdu
                self.x = X/2 - self.tx/2
                self.y = Y/2 - self.ty/2
                self.J1 += 1
                self.dx =- self.dx
                self.dy = float(randrange(-100, 100))/100
                self.r1.placer(30, Y/2-self.ty/2)
                self.r2.placer(X-30, Y/2-self.ty/2)
                PLAY = False

    

            tk.title("J1 : "+str(self.J1)+"/"+str(point)+"  |||  J2 : "+str(self.J2)+"/"+str(point)+"                                      Appuyez sur entrée pour Démarer/Mettre en pause") #on change le titre de la fenetre pour servir de score
            self.raffraichir() #on rafraichi l'ecran apres avoir bouger la balle

        tk.after(30, self.deplacer) #on refait le deplacement tout les 30 millisecondes

class Raquette :
    def __init__(self, x, y, haut,bas):
        self.x = x
        self.y = y
        self.tx = 10
        self.ty = 50
        self.vitesse = 10
        self.haut = haut
        self.bas = bas
        self.ra = terrain.create_rectangle(self.x, self.y, self.x+self.tx, self.y+self.ty, fill=COLORraq)
        tk.bind_all(self.haut, self.monter)
        tk.bind_all(self.bas, self.descendre)

    def monter(self, event): #la fonction pour monter
        self.deplacer(-self.vitesse) #on se deplace de - la vitesse, probablement vers le haut)
    def descendre(self, event): #la fonction pour descendre
        self.deplacer(self.vitesse) #on se deplace de + la vitesse, pour descendre)



    def deplacer (self, dy): #fonction deplacer
        if PLAY : #si play est actif
            self.y += dy # tu deplaces le player de dy (qu'il soit positif ou negatif)
            if self.y < 0: #si le nouveau self.y est inferieur a 0, on est sorti de la fenetre)
                self.y = 0 #on le remet donc dans la fenetre
            if self.y > Y - self.ty: # si a l'inverse on sort de l'autre cote
                self.y = Y - self.ty #on le remet dans le bon endroit
            self.raffraichir() #on rafraichi l'ecran pour deplacer visuellement le joueur


    def placer(self, x, y):
        self.x = x
        self.y = y
        terrain.coords(self.ra, self.x, self.y, self.x + self.tx, self.y + self.ty)


    def raffraichir(self):
        terrain.coords(self.ra, self.x, self.y, self.x + self.tx, self.y + self.ty)

def jeu():
    global tk, terrain, jeux, COLORraq, COLORball
    if COLORsraq == 0:
        COLORraq = "white"
    if COLORsraq == 1:
        COLORraq = "red"
    if COLORsraq == 2:
        COLORraq = "green"
    if COLORsraq == 3:
        COLORraq = "purple"

    if COLORsball == 0:
        COLORball = "white"
    if COLORsball == 1:
        COLORball = "red"
    if COLORsball == 2:
        COLORball = "green"
    if COLORsball == 3:
        COLORball = "purple"


    tk = Tk()
    tk.focus_force()
    tk.resizable(width=False, height=False)
    terrain = Canvas(tk, bg=BGCOLOR, height=Y, width=X)
    terrain.pack()
    jeux = Pong()
    tk.title("J1 : "+str(jeux.J1)+"/"+str(point)+"  |||  J2 : "+str(jeux.J2)+"/"+str(point)+"                                      Appuyez sur entrée pour Démarer/Mettre en pause")
    tk.mainloop()

def menu_fin():
    global temps_fin
    PLAY = False
    tk.unbind_all("<Return>")
    temps_fin = time()
    win = Tk()
    temps =  int(temps_fin - temps_start)
    minutes = int(temps/60)
    secondes = int(temps%60)
    def rejouer():
        global temps_fin, temps_start
        win.destroy()
        jeux.J1 = 0
        jeux.J2 = 0
        temps_fin = 0
        temps_start = 0
        temps_start = time()
        tk.bind_all("<Return>", jeux.pause)

    if jeux.J1 == point :
        lab = Label(win, text="J1 WIN ! Il y a "+str(jeux.J1)+" à "+str(jeux.J2)+" pour J1"+" en "+str(minutes)+" min "+str(secondes)+" sec ")
        lab.grid(row=1,column=1,columnspan=2,padx=10,pady=10)
        fin_rejouer = Button(win,text="Rejouer",command=rejouer)
        fin_rejouer.grid(row=2,column=2,padx=10,pady=10)
    
    if jeux.J2 == point :
        lab = Label(win, text="J2 WIN ! Il y a "+str(jeux.J2)+" à "+str(jeux.J1)+" pour J2"+" en "+str(minutes)+" min "+str(secondes)+" sec ")
        lab.grid(row=1,column=1,columnspan=2,padx=10,pady=10)
        fin_rejouer = Button(win,text="Rejouer",command=rejouer)
        fin_rejouer.grid(row=2,column=2,padx=10,pady=10)


def menu_principal():
    def jouer():
        menu.destroy()
        parametre()
    menu = Tk()
    menu.title("Pong")
    menu.focus_force()
    titre = Label (menu, text="Pong Game", width=10)
    titre.grid(row=1, column=3, padx=10, pady=10)
    but_quitter = Button(menu,text="Quitter", command=menu.destroy)
    but_quitter.grid(row=2,column=3,padx=10,pady=10)
    but_play = Button(menu,text="Jouer", command=jouer)
    but_play.grid(row=2,column=1,padx=10,pady=10)
    menu.mainloop()

def parametre():
    def precedent1():
        parametre.destroy()
        menu_principal()
        
    def suivant1():
        global temps_start
        parametre.destroy()
        temps_start = time()
        jeu()

    def valider():
        global point, SPEED, COLORsraq, COLORsball
        point = score.get()
        SPEED = vitesse.get()
        COLORsraq = couleurraq.get()
        COLORsball = couleurball.get()

    parametre = Tk()
    parametre.title("Parametre")
    parametre.focus_force()
    titre = Label(parametre,text="Paramètre de la partie :")
    titre.grid(row=1,column=1,columnspan=2,padx=10,pady=10)

    nbr_pts_gag = Label(parametre,text="Nombre de points pour gagner :")
    nbr_pts_gag.grid(row=2,column=1,padx=5,pady=5)
    score = IntVar()
    ligne_text = Entry(parametre, textvariable=score,width=5)
    ligne_text.grid(row=2,column=2,padx=10)

    VITESSE = Label(parametre, text="Vitesse de la balle :")
    VITESSE.grid(row=3, column=1, padx=5, pady=5)
    vitesse = IntVar()
    VITESSE = Entry(parametre, textvariable= vitesse, width = 5)
    VITESSE.grid(row=3, column=2, padx=10)

    COULEURraq = Label (parametre,text="Couleur raquette : 0=blanc, 1=rouge , 2=vert, 3=violet ")
    COULEURraq.grid(row=4, column=1,padx=5,pady=5)
    couleurraq = IntVar()
    COULEURraq = Entry(parametre, textvariable=couleurraq,width=5)
    COULEURraq.grid(row=4, column=2, padx=10)

    COULEURball = Label (parametre,text="Couleur balle : 0=blanc, 1=rouge , 2=vert, 3=violet ")
    COULEURball.grid(row=5, column=1,padx=5,pady=5)
    couleurball = IntVar()
    COULEURball = Entry(parametre, textvariable=couleurball,width=5)
    COULEURball.grid(row=5, column=2, padx=10)
    


    btn_valider = Button(parametre,text="Appliquer",command=valider)
    btn_valider.grid(row=2,column=3,rowspan=2)

    precedent1_1 = Button(parametre,text="Précédent",command=precedent1)
    precedent1_1.grid(row=4,column=0,padx=10,pady=10)
    suivant1 = Button(parametre,text="Suivant",command=suivant1)
    suivant1.grid(row=4,column=4,padx=10,pady=10)

    parametre.mainloop()

    

menu_principal()
