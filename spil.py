import pygame as pg
import sys


class Spil:

    def __init__(self,sort, gildi, snyr):

        self.sort = sort
        self.gildi = gildi
        self.snyr_upp = snyr
        self.bakhlid = None
        self.spila_breidd = 73
        self.spila_haed = 95
        self.kantur_toppur = 3

        self.framhlid = self.fa_mitt_spil(self.sort, self.gildi)


    def snua(self):
        if self.snyr_upp == False:
            self.snyr_upp = True
        else:
            self.snyr_upp = False

    def fa_spil(self):
        return self.framhlid

    def fa_mitt_spil(self, sort, gildi):
        sortir = {'Lauf' : 0,'Spadi': 1 ,'Hjarta' : 2, 'Tigull' : 3}
        rod =  sortir[sort] * (self.spila_haed + self.kantur_toppur)
        dalkur = (gildi-1) * self.spila_breidd

        return (rod,dalkur)

    def breidd(self):
        return self.spila_breidd

    def haed(self):
        return self.spila_haed




class Stokkur:

    def __init__(self, xHnit, yHnit):
        self.stadsetning = (xHnit, yHnit)
        self.spil_i_stokk = []

    def baeta_vid(self, spil):
        self.spil_i_stokk.append(spil)

    def taka_efsta(self):
        return self.spil_i_stokk.pop()

    def teikna(self, skjar, mynd):
        if not self.tomur():
            efst = self.spil_i_stokk[-1]
            hnit = efst.fa_spil()
            kassi = pg.Rect(self.stadsetning[0], self.stadsetning[1],efst.breidd(), efst.haed())
            skjar.blit(mynd, self.stadsetning, (hnit[1], hnit[0], efst.breidd(), efst.haed()))

    def tomur(self):
        return len(self.spil_i_stokk) == 0

    def flytja(self, hnit):
        self.stadsetning = hnit

    def stadur(self):
        return self.stadsetning

class bunki:

    def __init__(self, xhnit, yhnit):
        self.stadsetning = (xhnit, yhnit)
        self.skekkja = 30
        self.spil_i_bunka = []

    def setja_a_bunka(self, spil):
        self.spil_i_bunka.append(spil)

    def tomur(self):
        return len(self.spil_i_bunka) == 0

    def teikna(self, skjar, mynd):
        if not self.tomur():
            yhnit = self.stadsetning[0]
            for i in self.spil_i_bunka:
                kassi = pg.Rect(self.stadsetning[1], yhnit , i.breidd(), i.haed())
                yhnit += self.skekkja
                hnit = i.fa_spil()
                skjar.blit(mynd,kassi,(hnit[1], hnit[0], i.breidd(), i.haed()))











pg.init()

size = width, height = 1200, 640
black = 0, 0, 0
screen = pg.display.set_mode(size)
mynd = pg.image.load("Spil.png")

s1 = Stokkur(300,100)

s2 = Stokkur(500,100)

b = bunki(300,200)

spil1 = Spil('Hjarta', 1, True)
spil3 = Spil('Hjarta', 2, True)
spil2 = Spil('Spadi', 1, True)
spil4 = Spil('Tigull', 13, True)


s1.baeta_vid(spil1)
s1.baeta_vid(spil3)

s2.baeta_vid(spil4)
s2.baeta_vid(spil2)

def s1_s2():
    spil = s1.taka_efsta()
    s2.baeta_vid(spil)

def s2_s1():
    spil = s2.taka_efsta()
    s1.baeta_vid(spil)

faera = True

while 1:
    for event in pg.event.get():
        if event.type == pg.QUIT: 
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            if faera:
                s1_s2()
                if s1.tomur():
                    faera = False
            else:
                s2_s1()
                if s2.tomur():
                    faera = True
        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            spil = s1.taka_efsta()
            b.setja_a_bunka(spil)
            #h = s2.stadur()
            #s2.flytja((h[0]+20, h[1]+100))
            
            


    screen.fill(black)
    s1.teikna(screen, mynd)
    s2.teikna(screen, mynd)
    b.teikna(screen,mynd)

    pg.display.flip()







