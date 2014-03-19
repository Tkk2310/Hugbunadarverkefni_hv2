import pygame as pg
import sys


class Spil:

    def __init__(self,sort, gildi, snyr):

        self.sort = sort
        self.gildi = gildi
        self.snyr_upp = snyr
        self.bakhlid = pg.image.load('bakhlid.png')
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

    def skila_spili(self):
        return (self.sort,self.gildi)

    def hvernig_snyrdu(self):
        return self.snyr_upp

    def fa_bakhlid(self):
        return self.bakhlid





class Stokkur:

    def __init__(self, xHnit, yHnit):
        self.stadsetning = (xHnit, yHnit)
        self.spil_i_stokk = []

    def setja_a(self, spil):
        if type(spil)==list:
            self.spil_i_stokk += spil
        else:
            self.spil_i_stokk.append(spil)

    def taka_efsta(self):
        if not self.tomur():
            return [self.spil_i_stokk.pop()]

    def teikna(self, skjar, mynd):
        if not self.tomur():
            efst = self.spil_i_stokk[-1]
            if efst.hvernig_snyrdu():
                hnit = efst.fa_spil()
                kassi = pg.Rect(self.stadsetning[0], self.stadsetning[1],efst.breidd(), efst.haed())
                skjar.blit(mynd, kassi, (hnit[1], hnit[0], efst.breidd(), efst.haed()))
            else:
                kassi = pg.Rect(self.stadsetning[0], self.stadsetning[1],efst.breidd(), efst.haed())
                skjar.blit(efst.fa_bakhlid(), kassi)

    def athuga(self,hnit):
        if not self.tomur():
            efst = self.spil_i_stokk[-1]
            kassi = pg.Rect(self.stadsetning[0], self.stadsetning[1],efst.breidd(), efst.haed())
            if kassi.collidepoint(hnit):
                return efst


    def tomur(self):
        return len(self.spil_i_stokk) == 0

    def flytja(self, hnit):
        self.stadsetning = hnit

    def stadur(self):
        return self.stadsetning

class bunki:

    def __init__(self, xhnit, yhnit):
        self.stadsetning = (xhnit, yhnit)
        self.spil_i_bunka = []
        self.skekkja = 10

    def setja_a(self, spil):
        if spil:
            if type(spil)==list:
                self.spil_i_bunka += spil
            else:
                self.spil_i_bunka.append(spil)

    def taka_af(self, spil):
        if spil:
            hvar = self.spil_i_bunka.index(spil)
            losun = self.spil_i_bunka[hvar:]
            self.spil_i_bunka = self.spil_i_bunka[:hvar]
            return losun

    def tomur(self):
        return len(self.spil_i_bunka) == 0

    def teikna(self, skjar, mynd):
        if not self.tomur():
            yhnit = self.stadsetning[0]
            for i in self.spil_i_bunka:
                if i.hvernig_snyrdu():
                    kassi = pg.Rect(self.stadsetning[1], yhnit , i.breidd(), i.haed())
                    yhnit += self.skekkja + (18-len(self.spil_i_bunka))
                    hnit = i.fa_spil()
                    skjar.blit(mynd,kassi,(hnit[1], hnit[0], i.breidd(), i.haed()))
                else:
                    kassi = pg.Rect(self.stadsetning[1], yhnit , i.breidd(), i.haed())
                    yhnit += self.skekkja + (18-len(self.spil_i_bunka))
                    hnit = i.fa_spil()
                    skjar.blit(i.fa_bakhlid(),kassi)


    def athuga(self,hnit):
        if not self.tomur():
            yhnit = self.stadsetning[0] + ((len(self.spil_i_bunka)-1) * (self.skekkja + (18-len(self.spil_i_bunka))))
            ofugt = self.spil_i_bunka[::-1]
            for i in ofugt:
                kassi = pg.Rect(self.stadsetning[1], yhnit , i.breidd(), i.haed()) 
                yhnit -= self.skekkja + (18-len(self.spil_i_bunka))
                if kassi.collidepoint(hnit):
                    return i

        return False


    
    def stadur(self):
        return self.stadsetning




pg.init()

size = width, height = 1200, 640
black = 0, 0, 0
screen = pg.display.set_mode(size)
mynd = pg.image.load("Spil.png")

s1 = Stokkur(300,100)

s2 = Stokkur(500,100)

b = bunki(100,700)
b2 = bunki(100,800)

prufa = pg.Rect(500,500,100,100)

for i in range(13):
    s = Spil('Hjarta', i+1, True)
    s1.setja_a(s)


def s1_s2():
    spil = s1.taka_efsta()
    spil[0].snua()
    s2.setja_a(spil)

def s2_s1():
    spil = s2.taka_efsta()
    spil[0].snua()
    s1.setja_a(spil)

faera = True 

while 1:
    for event in pg.event.get():
        if event.type == pg.QUIT: 
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            spil = s1.athuga(pg.mouse.get_pos())
            temp = s1.taka_efsta()
            temp[0].snua()
            b2.setja_a(temp)
#            if faera:
#                s1_s2()
#                if s1.tomur():
#                    faera = False
#            else:
#                s2_s1()
#                if s2.tomur():
#                    faera = True

        elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            spil = s1.taka_efsta()
            spil[0].snua()
            b.setja_a(spil)

        elif event.type == pg.KEYDOWN and event.key == pg.K_a:
            spil = b.athuga((750,250))
            temp = b.taka_af(spil)
            b2.setja_a(temp)
            


    screen.fill(black)
    s1.teikna(screen, mynd)
    s2.teikna(screen, mynd)
    b.teikna(screen,mynd)
    b2.teikna(screen,mynd)
    pg.display.flip()