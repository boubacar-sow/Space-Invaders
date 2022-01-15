"""
@authors: Boubacar Sow, Saleh Hassan Salah

"""
import json #Pour la gestion des scores
import tkinter as tk
import tkinter.messagebox as tkMessageBox
from tkinter import *

class Score(object):
    """Classe score permettant de stocker le score assocjé à un joueur"""
    def __init__(self, nom, points):
        """Construction de notre classe"""
        self.nom = nom
        self.points = points
    #Définition des méthodes d'accès
    def _get_nom(self):
        return self.nom
    def _get_points(self):
        return self.points
    def _set_nom(self, autre):
        self.nom = autre
    def _set_points(self, autre):
        self.points = autre
    def __str__(self):
        return self.nom + "[" + str(self.points) 
    #Définition des méthodes d'accès aux fichiers
    def toFile(self, fichier):
        f = open(fichier, "w")
        f.write(str(self.points))
        f.close()
    @classmethod
    def fromFile(cls, fichier):
        with open(fichier, "r") as f:
            texte = f.read()
            print(texte)
class Resultat(object):
    """Classe qui permet de stocker defférents scores"""
    def __init__(self):
        """Définition de notre classe"""
        self.liste_score = []
    #Méthodes d'accès à la classe Resultat
    def _get_liste_score(self):
        return self.liste_score
    def ajout(self, element):
        self.liste_score.append(element)
    def __str__(self):
        chaine = str(self.liste_score[0])
        for e in self.liste_score[1:]:
            chaine = chaine + "," + str(e)
        return chaine
    #Définition des méthodes d'accès aux fichiers pour la classe Résultat
    def toFile(self, fichier):
        f = open(fichier, "w")
        tmp = []
        for l in self.liste_score:
            d = {}
            d["nom"] = l.nom
            d["points"] = l.points
            tmp.append(d)
        json.dump(tmp, f)
        f.close
    @classmethod
    def fromFile(cls, fichier):
        f = open(fichier, "r")
        tmp = json.load(f)
        liste = []
        for d in tmp:
            s=Score(d["nom"], d["points"])
            liste.append(d)
        sco = Resultat()
        sco.liste_score = liste
        f.close()
        return sco
class Fleet(object):
    """Classe caractérisant une flotte d'aliens qui bouge """
    def __init__(self):
        """Construction de notre classe"""
        self.width = 800
        self.height = 600
        self.aliens_lines = 5
        self.aliens_columns = 7
        self.aliens_inner_gap = 20
        self.alien_x_delta = 5
        self.alien_y_delta = 15
        fleet_size = self.aliens_lines * self.aliens_columns
        self.aliens_fleet = [None] * fleet_size
    #Définition de accesseurs
    def _get_width(self):
        return self.width
    def _get_height(self):
        return self.height
    def install_in(self, canvas):
        """Fonction permettant l'installation de la flotte d'aliens"""
        self.x=50  
        self.y=50
        self.alien = Alien()
        self.canvas = canvas
        tmp = 0
        for i in range(0, self.aliens_lines):
            for j in range(0, self.aliens_columns):
                self.aliens_fleet[tmp] = self.alien.install_in(self.canvas, self.x, self.y)
                tmp+=1
                self.x += self.aliens_inner_gap + 70
            self.x = 50
            self.y += self.aliens_inner_gap+30
    def move_in(self, canvas):
        """Fonction permettant le déplacement de la flotte d'aliens"""
        if len(self.aliens_fleet) !=0:
            all_rect_ids= self.canvas.find_withtag("alien")
            x1,y1,x2,y2 = self.canvas.bbox("alien")
            if x2>=788: 
                self.alien_x_delta=-self.alien_x_delta #On change le sens de déplacement
                dy = self.alien_y_delta
            elif x1<=0:
                self.alien_x_delta=-self.alien_x_delta #On change encore le sens de déplacement
                dy = self.alien_y_delta
            else:       
                dy=0 #Sinon on ne change pas position sur l'axe y
            for i in range(0,len(all_rect_ids)):
                self.alien.move_in(self.canvas,all_rect_ids[i],self.alien_x_delta,dy)
    def manage_touched_aliens_by(self, canvas, defender):
        """Fonction qui dirige l'operation de tir de bullet"""
        self.canvas=canvas
        self.defender=defender
        for i in range(0, len(self.defender.fired_bullets)):
            continuer = 1 #Variable servant de booléen       
            xb1,yb1,xb2,yb2=self.canvas.bbox(self.defender.fired_bullets[i]) 
            for j in range(len(self.aliens_fleet)):
                if self.aliens_fleet[j] != None: #On verifie si l'alien est vivant ou existe
                    xa1,ya1,xa2,ya2=self.canvas.bbox(self.aliens_fleet[j])
                    if (xb1>=xa1 or xb2>=xa1) and (xb1<=xa2 or xb2<=xa2) and yb1<=ya2 and yb1>=ya1:
                        self.alien.touched_by(self.canvas,self.defender.fired_bullets[i])
                        canvas.delete(self.defender.fired_bullets[i])#On supprime l'image du bullet bullet tiré
                        canvas.delete(self.aliens_fleet[j])#On supprime l'alien
                        self.alien.alive = False
                        del self.defender.fired_bullets[i]  #on supprime le bullet 
                        del self.aliens_fleet[j] #On supprime l'alien
                        continuer = 0
                        break
            if continuer==0:
                break       
                    
class Alien(object):
    """Classe permettant de définir un alien"""
    def __init__(self):
        """Construction de notre classe"""
        self.id = None
        self.alive = True
        self.alien = PhotoImage(file="alien.gif")
        self.explosion = PhotoImage(file="explosion.gif")
    def install_in(self, canvas, x, y):
        """Fonction permettant de créer et d'installer un alien"""
        self.id = canvas.create_image(x, y, image=self.alien, tags="alien")
        return self.id
    def move_in(self, canvas, alien, dx, dy):
        """Fonction qui assure le déplacement de l'alien"""
        self.id = alien
        canvas.move(self.id, dx, dy)
    def touched_by(self, canvas, projectile):
        """Fonction qui permet de créer une explosion"""
        x1, y1, x2, y2=canvas.bbox(projectile)
        explosion=canvas.create_image(x1+(x2-x1)/2, y1+(y2-y1)/2, image= self.explosion, tags="explosion")
        canvas.after(100, canvas.delete, explosion)
class Bullet(object):
    """Classe caractérisant un bullet"""
    def __init__ (self, shooter):
        """Construction de notre classe"""
        self.radius = 5
        self.color = 'red'
        self.speed = 8
        self.id = None
        self.shooter = shooter
        self.x = Defender()._get_x()
        self.y = Defender()._get_y()
    #Définition des accesseurs et des mutateurs
    def _get_id(self):
        return self.id 
    def _get_x(self):
        return self.x
    def _get_y(self):
        return self.y
    def _set_id(self, autre):
        self.id = autre
    def _set_x(self, autre):
        self.x = autre
    def _set_y(self, autre):
        self.y = autre
    def install_in(self, canvas):
        """Fonction permettant de créer le bullet"""
        r=self.radius
        self.id = canvas.create_oval(self.x, self.y, self.x+r, self.y+r, fill=self.color)
        return self.id
    def move_in(self,canvas,balle):
        self.id=balle
        canvas.move(self.id, 0, -self.speed)        
        
class Defender(object):
    """Classe permettant de concevoir le defender"""
    def __init__(self):
        """Construction de notre classe"""
        self.root = tk.Tk()
        self.width = 20
        self.height = 20
        self.move_delta = 20
        self.id = None
        self.max_fired_bullets = 8
        self.player = tk.PhotoImage(file="alien.gif")
        self.fired_bullets = []
        self.canvas_height = Fleet()._get_height()
        self.canvas_width = Fleet()._get_width()
        self.x = self.canvas_width//2 - self.width//2
        self.y = self.canvas_height - self.height
    #Définition des accesseurs et des mutateurs
    def _get_id(self):
        return self.id
    def _get_x(self):
        return self.x
    def _get_y(self):
        return self.y
    def _set_x(self, autre):
        self.x = autre
    def _set_y(self, autre):
        self.y = autre
    def install_in(self, canvas):
        """Création et installation d'un defender"""
        self.canvas=canvas
        self.rect_id = canvas.create_rectangle(self.x,self.y, self.x+self.width, self.y+self.width, fill="white")
        canvas.pack()
    def move_in(self, canvas, dx):
        """Fonction permettant de gérer le mouvement du defender"""
        canvas.move(self.rect_id, dx, 0)
    def keypress(self, event):
        """Fonction qui gère le mouvement du defender en fonction de la touche appuyée"""
        if event.keysym == 'Left':
           if self.x > self.move_delta:
               self.x-=self.move_delta
               self.move_in(self.canvas, -self.move_delta) 
        if event.keysym == 'Right':
            if self.x + self.move_delta < self.canvas_width:
                self.x += self.move_delta
                self.move_in(self.canvas, self.move_delta)
        if event.keysym == 'space':
            self.id = 1
            self.bullet = Bullet(self.id)
            self.bullet.x = self.x
            self.bullet.y = self.y
            self.fire(self.canvas)
    def fire(self, canvas):
        if len(self.fired_bullets) < self.max_fired_bullets:     
            self.bullet.id = self.bullet.install_in(self.canvas)    
            self.fired_bullets.append(self.bullet.id)  
    def move_bullet(self, canvas):
        for i in range(0,len(self.fired_bullets)):
            x1,y1,x2,y2 = self.canvas.bbox(self.fired_bullets[i])
            if y1<0:    
                canvas.delete(self.fired_bullets[i])    
                del self.fired_bullets[i]   
                break
            else:
                self.bullet.move_in(self.canvas,self.fired_bullets[i])

class Game(object):
    """Classe qui caractérise le jeu, qui installe la flotte d'aliens et le defender"""
    def __init__(self, frame):
        """Construction de notre classe"""
        width = 800
        height = 600
        self.frame = frame
        self.canvas = tk.Canvas(self.frame, width = width, 
                                                      height = height, bg='black')
        self.canvas.pack(side="top", fill="both", expand = True)
        self.defender = Defender()
        self.fleet = Fleet()
        self.defender.install_in(self.canvas)
        self.fleet.install_in(self.canvas)
    def move_bullets(self):
        if self.defender._get_id() == 1: 
            self.defender.move_bullet(self.canvas)
    def move_aliens_fleet(self):
        self.fleet.move_in(self.canvas)
    def start_animation(self):
        self.animation()
    def animation(self):
        self.move_bullets()
        self.move_aliens_fleet()
        self.fleet.manage_touched_aliens_by(self.canvas,self.defender)
        self.canvas.after(100,self.animation)
   
    

class SpaceInvaders(object):
    '''
    Main Game class
    '''
    def __init__(self):
        """Construction de notre classe"""
        self.root = tk.Tk()
        self.root.title("Space Invaders")
        width=800
        height=600
        self.frame=tk.Frame(self.root,width=width, height=height,bg="green")
        self.frame.pack(side="top", fill="both")
        self.game = Game(self.frame)
    def play(self):
        """Fonction qui actionne le jeu"""
        self.game.start_animation()
        self.root.bind("<Key>", self.game.defender.keypress)
        self.root.mainloop()
SpaceInvaders().play()
        