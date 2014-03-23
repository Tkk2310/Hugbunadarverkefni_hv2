import pygame as pg
import random

class Spil:

    def __init__(self,sort, gildi, snyr):
        self.sort = sort
        self.gildi = gildi
        self.snyr_upp = snyr
        self.spila_breidd = 71
        self.spila_haed = 96
        self.heimili = False
        self.bakhlid = self.fa_mitt_spil('Auka', 1)
        self.framhlid = self.fa_mitt_spil(self.sort, self.gildi)

    def hvar_attu_heima(self):
        return self.heimili

    def nytt_heimili(self,geymsla):
        self.heimili = geymsla

    def snua(self):
        if self.snyr_upp == False:
            self.snyr_upp = True
        else:
            self.snyr_upp = False
        return self

    def fa_spil(self):
        if self.snyr_upp:
            return self.framhlid
        else:
            return self.bakhlid

    def fa_mitt_spil(self, sort, gildi):
        sortir = {'Lauf' : 0,'Spadi': 1 ,'Hjarta' : 2, 'Tigull' : 3, 'Auka' : 4}
        rod =  sortir[sort] * self.spila_haed
        dalkur = (gildi-1) * self.spila_breidd + (gildi-1)
        return (rod,dalkur)

    def breidd(self):
        return self.spila_breidd

    def haed(self):
        return self.spila_haed

    def skila_spili(self):
        return (self.sort,self.gildi)

    def hvernig_snyrdu(self):
        return self.snyr_upp


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

    def skila_fremsta(self):
        if not self.tomur():
            return self.spil_i_lista[-1]


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
            hnit = efst.fa_spil()
            kassi = pg.Rect(self.stadsetning[0], self.stadsetning[1],efst.breidd(), efst.haed())
            skjar.blit(mynd, kassi, (hnit[1], hnit[0], efst.breidd(), efst.haed()))

    def athuga(self,hnit):
        if not self.tomur():
            efst = self.spil_i_lista[-1]
            kassi = pg.Rect(self.stadsetning[0], self.stadsetning[1],efst.breidd(), efst.haed())
            if kassi.collidepoint(hnit):
                return efst

    def snyr_efst_upp(self):
        return True


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
                kassi = pg.Rect(self.stadsetning[0], yhnit , i.breidd(), i.haed())
                yhnit += self.skekkja + (18-len(self.spil_i_lista))
                hnit = i.fa_spil()
                skjar.blit(mynd,kassi,(hnit[1], hnit[0], i.breidd(), i.haed()))

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

    def skila_aftasta(self):
        if not self.tomur():
            return self.spil_i_lista[0]

    def snyr_efst_upp(self):
        return self.spil_i_lista[-1].hvernig_snyrdu()

    def snua_efsta(self):
        self.spil_i_lista[-1].snua()

    def fjoldi_spila(self):
        return len(self.spil_i_lista)


class Reglur:

    def klikka(self):
        geymsla,spil = self.mus_yfir_spili()
        if not geymsla: return
        if self.hond.tomur():
            if geymsla == self.stokkar[0]:
                self.draga_nytt_spil()
            elif not geymsla.snyr_efst_upp():
                geymsla.snua_efsta()
            else:
                self.setja_a_hond(geymsla,spil)
        else:
            if geymsla == self.stokkar[0]:
                return
            if (geymsla == self.stokkar[1] and
                self.hond.skila_aftasta().hvar_attu_heima() == self.stokkar[1]):
                    self.taka_af_hond(geymsla)
                    return
            if geymsla == self.stokkar[1]:
                return
            if geymsla == self.hond.skila_aftasta().hvar_attu_heima():
                self.taka_af_hond(geymsla)
                return
            self.logleg_faersla(geymsla)

    def logleg_faersla(self,geymsla):
        aftast = self.hond.skila_aftasta().skila_spili()
        fremst = geymsla.skila_fremsta().skila_spili()
        if geymsla.draugur_lifandi() and aftast[1] == 13 and geymsla in self.bunkar:
            self.taka_af_hond(geymsla)
        if not self.litur(aftast[0]) == self.litur(fremst[0]):
            if aftast[1]+1 == fremst[1]:
                self.taka_af_hond(geymsla)
        if geymsla in self.stokkar[2:]:
            self.sigur_stokkar(geymsla)

    def sigur_stokkar(self, geymsla):
        spil = self.hond.skila_aftasta().skila_spili()
        if geymsla.draugur_lifandi() and spil[1] == 1:
            self.taka_af_hond(geymsla)
        elif self.hond.fjoldi_spila() == 1:
            spil_i_bunka = geymsla.skila_fremsta().skila_spili()
            if spil_i_bunka[0] == spil[0] and spil_i_bunka[1]+1 == spil[1]:
                self.taka_af_hond(geymsla)
        self.leikur_buinn()

    def leikur_buinn(self):
        for i in self.stokkar[2:]:
            if i.draugur_lifandi():
                return
            if not i.skila_fremsta().skila_spili()[1] == 13:
                return
        print('jei')

    def litur(self,sort):
        if sort == 'Hjarta' or sort == 'Tigull':
            return 'Rautt'
        else:
            return 'Svart'

    def draga_nytt_spil(self):
        if not self.stokkar[0].draugur_lifandi():
            if self.stokkar[1].draugur_lifandi():
                self.stokkar[1].taka_draug()
            self.stokkar[1].setja_a(self.stokkar[0].taka_af(None)[0].snua())
            if self.stokkar[0].tomur():
                self.stokkar[0].setja_draug()
        else:
            self.stokkar[0].taka_draug()
            while not self.stokkar[1].tomur():
                self.stokkar[0].setja_a(self.stokkar[1].taka_af(None)[0].snua())
            self.stokkar[1].setja_draug()

    def setja_a_hond(self,geymsla,spil):
        if geymsla and not geymsla.draugur_lifandi():
            mitt = geymsla.taka_af(spil)
            mitt[0].nytt_heimili(geymsla)
            self.hond.setja_a(mitt)
            geymsla.setja_draug()

    def taka_af_hond(self,geymsla):
        if geymsla:
            geymsla.taka_draug()
            aftasta = self.hond.skila_aftasta()
            aftasta.nytt_heimili(False)
            spil = self.hond.taka_af(aftasta)
            geymsla.setja_a(spil)

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


class Leikur(Reglur):

    def __init__(self):
        self.undirbua()
        self.leikhringur()

    def undirbua(self):
        pg.init()
        pg.display.set_caption('awesome-souce')
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
                self.klikka()
            self.hond.flytja((mus[0]-36,mus[1]-10))
            if (atburdur.type == pg.KEYDOWN and
                atburdur.key == pg.K_ESCAPE or
                atburdur.type == pg.QUIT):
                    self.spilandi = False

    def leikhringur(self):
        while self.spilandi:
            self.gluggi.fill((0,150,0))
            self.teikna_stokka()
            self.samskipti()
            self.klukka.tick(200)
            pg.display.flip()

if __name__ == '__main__':
    Leikur()
