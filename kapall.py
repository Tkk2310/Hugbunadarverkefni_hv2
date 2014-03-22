import pygame as pg
import random

class Spil:

    def __init__(self,sort, gildi, snyr):

        self.sort = sort
        self.gildi = gildi
        self.snyr_upp = snyr
        self.bakhlid = pg.image.load('bakhlid.png')
        self.spila_breidd = 72
        self.spila_haed = 96
        self.kantur_toppur = 0

        self.framhlid = self.fa_mitt_spil(self.sort, self.gildi)


    def snua(self):
        if self.snyr_upp == False:
            self.snyr_upp = True
        else:
            self.snyr_upp = False

    def fa_spil(self):
        return self.framhlid

    def fa_mitt_spil(self, sort, gildi):
        sortir = {'Lauf' : 0,'Spadi': 1 ,'Hjarta' : 2, 'Tigull' : 3, 'Auka' : 4}
        rod =  sortir[sort] * (self.spila_haed + self.kantur_toppur)
        dalkur = (gildi-1) * self.spila_breidd-1

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


class Geymsla:

    def tomur(self):
        return len(self.spil_i_lista)==0

    def setja_draug(self):
        if self.tomur():
            self.setja_a(Spil('Auka',6,True))
            self.draugur = True

    def taka_draug(self):
        if self.draugur and len(self.spil_i_lista) == 1:
            self.spil_i_lista = []
            self.draugur = False

    def draugur_lifandi(self):
        return self.draugur

    def setja_a(self, spil):
        if spil:
            if type(spil)==list:
                self.spil_i_lista += spil
            else:
                self.spil_i_lista.append(spil)

    def flytja(self, hnit):
        self.stadsetning = hnit



class Stokkur(Geymsla):

    def __init__(self, xHnit, yHnit):
        self.stadsetning = (xHnit, yHnit)
        self.spil_i_lista = []
        self.draugur = False

    def taka_af(self, spil):
        if not self.tomur():
            return [self.spil_i_lista.pop()]

    def teikna(self, skjar, mynd):
        if not self.tomur():
            efst = self.spil_i_lista[-1]
            if efst.hvernig_snyrdu():
                hnit = efst.fa_spil()
                kassi = pg.Rect(self.stadsetning[0], self.stadsetning[1],efst.breidd(), efst.haed())
                skjar.blit(mynd, kassi, (hnit[1], hnit[0], efst.breidd(), efst.haed()))
            else:
                kassi = pg.Rect(self.stadsetning[0], self.stadsetning[1],efst.breidd(), efst.haed())
                skjar.blit(efst.fa_bakhlid(), kassi)

    def athuga(self,hnit):
        if not self.tomur():
            efst = self.spil_i_lista[-1]
            kassi = pg.Rect(self.stadsetning[0], self.stadsetning[1],efst.breidd(), efst.haed())
            if kassi.collidepoint(hnit):
                return efst


class Bunki(Geymsla):

    def __init__(self, xhnit, yhnit):
        self.stadsetning = (xhnit, yhnit)
        self.spil_i_lista = []
        self.skekkja = 12
        self.draugur = False

    def taka_af(self, spil):
        if spil:
            hvar = self.spil_i_lista.index(spil)
            losun = self.spil_i_lista[hvar:]
            self.spil_i_lista = self.spil_i_lista[:hvar]
            return losun

    def teikna(self, skjar, mynd):
        if not self.tomur():
            yhnit = self.stadsetning[1]
            for i in self.spil_i_lista:
                if i.hvernig_snyrdu():
                    kassi = pg.Rect(self.stadsetning[0], yhnit , i.breidd(), i.haed())
                    yhnit += self.skekkja + (18-len(self.spil_i_lista))
                    hnit = i.fa_spil()
                    skjar.blit(mynd,kassi,(hnit[1], hnit[0], i.breidd(), i.haed()))
                else:
                    kassi = pg.Rect(self.stadsetning[0], yhnit , i.breidd(), i.haed())
                    yhnit += self.skekkja + (18-len(self.spil_i_lista))
                    hnit = i.fa_spil()
                    skjar.blit(i.fa_bakhlid(),kassi)

    def athuga(self,hnit):
        if not self.tomur():
            yhnit = self.stadsetning[1] + ((len(self.spil_i_lista)-1) * (self.skekkja + (18-len(self.spil_i_lista))))
            ofugt = self.spil_i_lista[::-1]
            for i in ofugt:
                kassi = pg.Rect(self.stadsetning[0], yhnit , i.breidd(), i.haed())
                yhnit -= self.skekkja + (18-len(self.spil_i_lista))
                if kassi.collidepoint(hnit):
                    return i
        return False

    def skila_fyrsta(self):
        if not self.tomur():
            return self.spil_i_lista[0]


class Reglur:
    pass


class Leikur:
    def __init__(self):
        self.undirbua()
        self.leikhringur()

    def undirbua(self):
        pg.init()
        self.spilandi = True
        self.halda_nidri = False
        self.klukka = pg.time.Clock()
        self.gluggi = pg.display.set_mode((800,500))
        self.gluggi.fill((0,0,0))
        self.mynd = pg.image.load('mynd.png').convert()
        self.utbytta_spilum()

    def utbytta_spilum(self):
        spil = [Spil(tegund,numer, False) for tegund in ['Hjarta','Spadi','Tigull','Lauf'] for numer in range(1,14)]
        random.shuffle(spil)
        self.bunkar = (
                Bunki(10,130),
                Bunki(110,130),
                Bunki(210,130),
                Bunki(310,130),
                Bunki(410,130),
                Bunki(510,130),
                Bunki(610,130)
                )
        self.stokkar = (
                Stokkur(10,10),
                Stokkur(110,10),
                Stokkur(310,10),
                Stokkur(410,10),
                Stokkur(510,10),
                Stokkur(610,10)
                )
        for i in range(1,7):
            for j in range(i):
                self.bunkar[i].setja_a(spil.pop())
        for k in self.bunkar:
            snu = spil.pop()
            snu.snua()
            k.setja_a(snu)
        self.stokkar[0].setja_a(spil)
        for l in self.stokkar:
            l.setja_draug()
        self.hond = Bunki(0,0)

    def teikna_stokka(self):
        for stk in self.stokkar:
            stk.teikna(self.gluggi, self.mynd)
        for bnk in self.bunkar:
            bnk.teikna(self.gluggi, self.mynd)
        self.hond.teikna(self.gluggi, self.mynd)

    def samskipti(self):
        mus = pg.mouse.get_pos()
        for atburdur in pg.event.get():
            if atburdur.type == pg.MOUSEBUTTONDOWN:
                self.halda_nidri = True
                self.laga_hond()
            if atburdur.type == pg.MOUSEBUTTONUP:
                self.halda_nidri = False
            self.hond.flytja((mus[0]-36,mus[1]-10))
            if atburdur.type == pg.KEYDOWN and atburdur.key == pg.K_ESCAPE:
                self.spilandi = False

    def laga_hond(self):
        if self.hond.tomur():
            self.setja_a_hond()
        else:
            self.taka_af_hond()

    def setja_a_hond(self):
        bos,spil = self.mus_yfir_spili()
        if bos and not bos.draugur_lifandi():
            mitt = bos.taka_af(spil)
            self.hond.setja_a(mitt)
            bos.setja_draug()

    def taka_af_hond(self):
        bos,spil = self.mus_yfir_spili()
        if bos:
            bos.taka_draug()
            fyrsta = self.hond.skila_fyrsta()
            spil = self.hond.taka_af(fyrsta)
            bos.setja_a(spil)

    def mus_yfir_spili(self):
        for stk in self.stokkar:
            spil = stk.athuga(pg.mouse.get_pos())
            if spil:
                return stk,spil
        for bnk in self.bunkar:
            spil = bnk.athuga(pg.mouse.get_pos())
            if spil:
                return bnk,spil
        return False,False

    def leikhringur(self):
        while self.spilandi:
            self.gluggi.fill((0,255,0))
            self.teikna_stokka()
            self.samskipti()
            self.klukka.tick(200)
            pg.display.flip()

if __name__ == '__main__':
    Leikur()
