import dbexecutor


class RealData():
    adetid = None
    metreid = None
    kiloid = None

    def __init__(self):
        self.kiloid = -1
        self.metreid = -1
        self.adetid = -1

    def preloadRealData(self):
        self.preloadBaseData()
        self.preloadcorporation()
        self.preloadstockrooms()
        self.preloadCategories()

    def preloadBaseData(self):
        self.preloadstockunits()
        self.preloadstockcolors()
        self.preloadstockpackage()

    def preloadstockunits(self):
        adet = dbexecutor.addStockUnit('Adet', 0)
        self.adetid = adet.id
        metre = dbexecutor.addStockUnit('Metre', 2)
        self.metreid = metre.id
        kilo = dbexecutor.addStockUnit('Kilogram', 1)
        self.kiloid = kilo.id

    def preloadstockcolors(self):
        dbexecutor.addStockColor("Gri")
        dbexecutor.addStockColor("Sarı-Yeşil")
        dbexecutor.addStockColor("Lila")
        dbexecutor.addStockColor("Siyah")
        dbexecutor.addStockColor("Mavi")
        dbexecutor.addStockColor("Yeşil")
        dbexecutor.addStockColor("Beyaz")
        dbexecutor.addStockColor("Kahve")
        dbexecutor.addStockColor("Kırmızı")
        dbexecutor.addStockColor("Mor")
        dbexecutor.addStockColor("Sarı")
        dbexecutor.addStockColor("Turuncu")
        dbexecutor.addStockColor("Kahve-Mavi")

    def preloadstockpackage(self):
        dbexecutor.addStockPackage("Koli")
        dbexecutor.addStockPackage("Çuval")
        dbexecutor.addStockPackage("Torba")
        dbexecutor.addStockPackage("Kangal")
        dbexecutor.addStockPackage("Makara")

    def preloadcorporation(self):
        dbexecutor.addCorporation("Mega Metal")
        dbexecutor.addCorporation("Er Bakır")
        dbexecutor.addCorporation("Deva Plastik")
        dbexecutor.addCorporation("Eker Motor")
        dbexecutor.addCorporation("Ürün Sarfı")

    def preloadstockrooms(self):
        dbexecutor.addStockRoom("Şentaş")
        dbexecutor.addStockRoom("Günaydın")
        dbexecutor.addStockRoom("Özkan")
        dbexecutor.addStockRoom("K. A.")

    '''
        Category Section
    '''
    def preloadCategories(self):
        self.preloadImalat()
        self.preloadMegaMetal()
        self.preloadErBakir()
        self.preloadEkerMotor()
        self.preloadClindasMotor()

    def preloadImalat(self):
        imalat = dbexecutor.addStockCategory('İMALAT')
        self.preloadImalatNya(imalat.id)
        self.preloadImalatHffrNya(imalat.id)
        self.preloadImalatNyaf(imalat.id)
        self.preloadImalatHffrNyaf(imalat.id)
        self.preloadImalatDigital(imalat.id)
        self.preloadImalatHffrDigital(imalat.id)
        self.preloadImalatTtrDigital(imalat.id)
        self.preloadImalatLivy(imalat.id)
        self.preloadImalatLicyca(imalat.id)
        self.preloadImalatLicyc(imalat.id)
        self.preloadImalatKumandaKablosu(imalat.id)
        self.preloadImalatYuvarlakBukumlu(imalat.id)
        self.preloadImalatNhmxmh(imalat.id)
        self.preloadImalatSoyslcyjb(imalat.id)
        self.preloadImalatDahiliTlfKablosu(imalat.id)
        self.preloadImalatN2xhfe180(imalat.id)
        self.preloadImalatTtrDigital(imalat.id)
        self.preloadImalat6awg(imalat.id)
        self.preloadImalatCambusBukum(imalat.id)
        self.preloadImalatOzelKablo(imalat.id)
        self.preloadImalatAsansorKablosu(imalat.id)
        self.preloadImalatHffrAsansorKablosu(imalat.id)
        self.preloadImalatVincKablosu(imalat.id)
        self.preloadImalatHffrYassiVincKablosu(imalat.id)

    def preloadImalatNya(self, imalatid):
        nya = dbexecutor.addStockSubcategory('NYA', imalatid)
        dbexecutor.addStockType('0,80 mm2 NYA KABLO', self.metreid, nya.id)
        dbexecutor.addStockType('4 mm2 NYA KABLO', self.metreid, nya.id)
        dbexecutor.addStockType('6 mm2 NYA KABLO', self.metreid, nya.id)

    def preloadImalatHffrNya(self, imalatid):
        hffrnya = dbexecutor.addStockSubcategory('HFFR NYA', imalatid)
        dbexecutor.addStockType('HFFR 0,80 mm2 NYA KABLO', self.metreid, hffrnya.id)
        dbexecutor.addStockType('HFFR 4 mm2 NYA KABLO', self.metreid, hffrnya.id)
        dbexecutor.addStockType('HFFR 6 mm2 NYA KABLO', self.metreid, hffrnya.id)

    def preloadImalatNyaf(self, imalatid):
        nyaf = dbexecutor.addStockSubcategory('NYAF', imalatid)
        dbexecutor.addStockType('0,50 mm2 NYAF KABLO', self.metreid, nyaf.id)
        dbexecutor.addStockType('0,75 mm2 NYAF KABLO', self.metreid, nyaf.id)
        dbexecutor.addStockType('1 mm2 NYAF KABLO', self.metreid, nyaf.id)
        dbexecutor.addStockType('1,5 mm2 NYAF KABLO', self.metreid, nyaf.id)
        dbexecutor.addStockType('2,5 mm2 NYAF KABLO', self.metreid, nyaf.id)
        dbexecutor.addStockType('4 mm2 NYAF KABLO', self.metreid, nyaf.id)
        dbexecutor.addStockType('6 mm2 NYAF KABLO', self.metreid, nyaf.id)

    def preloadImalatHffrNyaf(self, imalatid):
        hffrnyaf = dbexecutor.addStockSubcategory('HFFR NYAF', imalatid)
        dbexecutor.addStockType('HFFR 0,50 mm2 NYAF KABLO', self.metreid, hffrnyaf.id)
        dbexecutor.addStockType('HFFR 0,75 mm2 NYAF KABLO', self.metreid, hffrnyaf.id)
        dbexecutor.addStockType('HFFR 1 mm2 NYAF KABLO', self.metreid, hffrnyaf.id)
        dbexecutor.addStockType('HFFR 1,5 mm2 NYAF KABLO', self.metreid, hffrnyaf.id)
        dbexecutor.addStockType('HFFR 2,5 mm2 NYAF KABLO', self.metreid, hffrnyaf.id)
        dbexecutor.addStockType('HFFR 4 mm2 NYAF KABLO', self.metreid, hffrnyaf.id)
        dbexecutor.addStockType('HFFR 6 mm2 NYAF KABLO', self.metreid, hffrnyaf.id)

    def preloadImalatDigital(self, imalatid):
        dijital = dbexecutor.addStockSubcategory('DİJİTAL KABLO', imalatid)
        dbexecutor.addStockType('DT-18 DİJİTAL KABLO', self.metreid, dijital.id)
        dbexecutor.addStockType('DT-16 DİJİTAL KABLO', self.metreid, dijital.id)
        dbexecutor.addStockType('DT-13 DİJİTAL KABLO 13*0,22mm', self.metreid, dijital.id)

    def preloadImalatHffrDigital(self, imalatid):
        hffrdijital = dbexecutor.addStockSubcategory('HFFR DİJİTAL KABLO', imalatid)
        dbexecutor.addStockType('HFFR - DT-13 DİJİTAL KABLO', self.metreid, hffrdijital.id)

    def preloadImalatTtrDigital(self, imalatid):
        ttr = dbexecutor.addStockSubcategory('TTR KABLO', imalatid)
        dbexecutor.addStockType('2*0,75 TTR KABLO', self.metreid, ttr.id)
        dbexecutor.addStockType('3*0,75 TTR KABLO', self.metreid, ttr.id)
        dbexecutor.addStockType('5*0,75 TTR KABLO', self.metreid, ttr.id)
        dbexecutor.addStockType('3*1 TTR KABLO', self.metreid, ttr.id)
        dbexecutor.addStockType('2X1 TTR KABLO', self.metreid, ttr.id)
        dbexecutor.addStockType('2*1,5 TTR TTR KABLO', self.metreid, ttr.id)
        dbexecutor.addStockType('4*1,5 TTR KABLO', self.metreid, ttr.id)
        dbexecutor.addStockType('2X2,5 TTR KABLO', self.metreid, ttr.id)
        dbexecutor.addStockType('5X1,5 TTR KABLO', self.metreid, ttr.id)
        dbexecutor.addStockType('5G2,5 TTR KABLO', self.metreid, ttr.id)
        dbexecutor.addStockType('4*0,75 TTR KABLO', self.metreid, ttr.id)
        dbexecutor.addStockType('4*1 TTR KABLO', self.metreid, ttr.id)
        dbexecutor.addStockType('4*2,5 TTR KABLO', self.metreid, ttr.id)
        dbexecutor.addStockType('4*4 TTR KABLO', self.metreid, ttr.id)
        dbexecutor.addStockType('5*4 TTR KABLO', self.metreid, ttr.id)
        dbexecutor.addStockType('7*0,50 TTR KABLO', self.metreid, ttr.id)
        dbexecutor.addStockType('2*1,25 TTR', self.metreid, ttr.id)

    def preloadImalatLivy(self, imalatid):
        livy = dbexecutor.addStockSubcategory('LIYY', imalatid)
        dbexecutor.addStockType('2*0,50 LIYY', self.metreid, livy.id)
        dbexecutor.addStockType('3G0,50 LIYY', self.metreid, livy.id)
        dbexecutor.addStockType('4*0,50 LIYY', self.metreid, livy.id)

    def preloadImalatLicyca(self, imalatid):
        livy = dbexecutor.addStockSubcategory('LIYCY-A', imalatid)
        dbexecutor.addStockType('4*2,5 mm LIYCY-A KABLO', self.metreid, livy.id)

    def preloadImalatLicyc(self, imalatid):
        livy = dbexecutor.addStockSubcategory('LIYCY', imalatid)
        dbexecutor.addStockType('4*4 LIYCY KABLO', self.metreid, livy.id)
        dbexecutor.addStockType('4*6 LIYCY KABLO', self.metreid, livy.id)

    def preloadImalatKumandaKablosu(self, imalatid):
        sub = dbexecutor.addStockSubcategory('KUMANDA KABLOSU', imalatid)
        dbexecutor.addStockType('6*0,50mm KUMANDA KABLOSU', self.metreid, sub.id)

    def preloadImalatYuvarlakBukumlu(self, imalatid):
        sub = dbexecutor.addStockSubcategory('YUVARLAK BÜKÜMLÜ YSLY-JZ', imalatid)
        dbexecutor.addStockType('10*0,75 YUVARLAK BÜKÜMLÜ YSLY-JZ GRİ KABLO', self.metreid, sub.id)
        dbexecutor.addStockType('15*0,75 YSLY-JZ KABLO', self.metreid, sub.id)

    def preloadImalatNhmxmh(self, imalatid):
        sub = dbexecutor.addStockSubcategory('NHXMH', imalatid)
        dbexecutor.addStockType('4*6 NHXMH', self.metreid, sub.id)
        dbexecutor.addStockType('4*4 mm2 NHXMH KABLO', self.metreid, sub.id)

    def preloadImalatSoyslcyjb(self, imalatid):
        sub = dbexecutor.addStockSubcategory('SO-YSLCY-JB', imalatid)
        dbexecutor.addStockType('3G 10+6 mm2 SO-YSLCY-JB', self.metreid, sub.id)

    def preloadImalatDahiliTlfKablosu(self, imalatid):
        sub = dbexecutor.addStockSubcategory('Dahili Tlf kablosu', imalatid)
        dbexecutor.addStockType('2*2*0,5+0,5 Dahili Tlf kablosu', self.metreid, sub.id)

    def preloadImalatN2xhfe180(self, imalatid):
        sub = dbexecutor.addStockSubcategory('N2XH FE-180', imalatid)
        dbexecutor.addStockType('N2XH FE-180 4*6 KABLO', self.metreid, sub.id)

    def preloadImalat6awg(self, imalatid):
        sub = dbexecutor.addStockSubcategory('6AWG', imalatid)
        dbexecutor.addStockType('6AWG 6*014 mm2', self.metreid, sub.id)

    def preloadImalatCambusBukum(self, imalatid):
        sub = dbexecutor.addStockSubcategory('CAMBUS BÜKÜM', imalatid)
        dbexecutor.addStockType('2X0,75mm CAMBUS BÜKÜM SİYAH-KIRMIZI', self.metreid, sub.id)
        dbexecutor.addStockType('2X0,75mm CAMBUS BÜKÜM KAHVE-GRİ', self.metreid, sub.id)

    def preloadImalatOzelKablo(self, imalatid):
        sub = dbexecutor.addStockSubcategory('ÖZEL KABLO', imalatid)
        dbexecutor.addStockType('4X2,5 + 8X1 mm2 ÖZEL', self.metreid, sub.id)
        dbexecutor.addStockType('2*CAT6E+12*0,75 HFFR YASSI KABLO', self.metreid, sub.id)
        dbexecutor.addStockType('HFFR 2*CAT6E+2*1 LIYCY+6*0,75 LYCY YASSI KABLO', self.metreid, sub.id)
        dbexecutor.addStockType('HFFR 2*CAT6E+2*1 LIYCY+4*0,75 LYCY YASSI KABLO', self.metreid, sub.id)
        dbexecutor.addStockType('Z-H05V-K PE 1*0,22 mm2', self.metreid, sub.id)

    def preloadImalatAsansorKablosu(self, imalatid):
        sub = dbexecutor.addStockSubcategory('ASANSÖR KABLOSU', imalatid)
        dbexecutor.addStockType('8 X 0,75 mm2', self.metreid, sub.id)
        dbexecutor.addStockType('12 X 0,75 mm2', self.metreid, sub.id)
        dbexecutor.addStockType('16 X 0,75 mm2', self.metreid, sub.id)
        dbexecutor.addStockType('18 X 0,75 mm2', self.metreid, sub.id)
        dbexecutor.addStockType('20 X 0,75 mm2', self.metreid, sub.id)
        dbexecutor.addStockType('24 X 0,75 mm2', self.metreid, sub.id)
        dbexecutor.addStockType('28 X 0,75 mm2', self.metreid, sub.id)
        dbexecutor.addStockType('30 X 0,75 mm2', self.metreid, sub.id)
        dbexecutor.addStockType('36 X 0,75 mm2', self.metreid, sub.id)
        dbexecutor.addStockType('42 X 0,75 mm2', self.metreid, sub.id)
        dbexecutor.addStockType('12 X 0,75 mm2 + Çelik Halat', self.metreid, sub.id)
        dbexecutor.addStockType('24 X 0,75 mm2 Yüksek Hızlı', self.metreid, sub.id)
        dbexecutor.addStockType('18 G 0,75 mm2 + 2 x 0,50 mm2', self.metreid, sub.id)
        dbexecutor.addStockType('28 G 0,75 mm2 + 2 x 0,25 m2', self.metreid, sub.id)
        dbexecutor.addStockType('28 G 0,75 mm2 + 2 x 0,22 m2', self.metreid, sub.id)
        dbexecutor.addStockType('4 x CAT6e YASSI DATA LAN KABLO', self.metreid, sub.id)
        dbexecutor.addStockType('28 G 0,75 mm2 + 4 x 2 x 0,34 mm2', self.metreid, sub.id)
        dbexecutor.addStockType('24 G 0,75 mm2 + 3 x 4 x 0,50 mm2', self.metreid, sub.id)
        dbexecutor.addStockType('24 G 0,75 mm2 + 3 x 4 x 0,34 mm2', self.metreid, sub.id)
        dbexecutor.addStockType('24 G 0,75 mm2 + 3 x 4 x 0,22 mm2', self.metreid, sub.id)
        dbexecutor.addStockType('24 G 0,75 mm2 + 3 x 4 x 0,25 mm2', self.metreid, sub.id)
        dbexecutor.addStockType('50 Nakil ', self.metreid, sub.id)
        dbexecutor.addStockType('24 G 0,75 mm2 + CCTV', self.metreid, sub.id)
        dbexecutor.addStockType('12 X 0,75 mm2 + Çelik Halat + Yüksek Hızlı', self.metreid, sub.id)
        dbexecutor.addStockType('24 X 0,75 mm2 + Çelik Halat + Yüksek Hızlı', self.metreid, sub.id)
        dbexecutor.addStockType('12 G 0,75 mm2 + CCTV', self.metreid, sub.id)
        dbexecutor.addStockType('28 G 0,75 mm2 + 2 x 2 x 0,25 mm2', self.metreid, sub.id)
        dbexecutor.addStockType('28 G 0,75 mm2 + 2 x 2 x 0,50 mm2 D3', self.metreid, sub.id)
        dbexecutor.addStockType('16x0,75mm2 + 2x2x0,50 mm2', self.metreid, sub.id)

    def preloadImalatHffrAsansorKablosu(self, imalatid):
        sub = dbexecutor.addStockSubcategory('HFFR ASANSÖR KABLOSU', imalatid)
        dbexecutor.addStockType('HFFR - 24 X 0,75 mm2 + Çelik Halat', self.metreid, sub.id)
        dbexecutor.addStockType('HFFR - 12 X 0,75 mm2 + Çelik Halat', self.metreid, sub.id)
        dbexecutor.addStockType('HFFR - 12 X 0,75 mm2', self.metreid, sub.id)
        dbexecutor.addStockType('HFFR - 24 X 0,75 mm2', self.metreid, sub.id)
        dbexecutor.addStockType('HFFR - 28 G 0,75 mm2 + 2 x 2 x 0,25 m2', self.metreid, sub.id)
        dbexecutor.addStockType('HFFR - 28 G 0,75 mm2 + 2 x 0,25 m2', self.metreid, sub.id)

    def preloadImalatVincKablosu(self, imalatid):
        sub = dbexecutor.addStockSubcategory('VİNÇ KABLOSU', imalatid)
        dbexecutor.addStockType('12 X 1,5 YASSI VİNÇ KAB.', self.metreid, sub.id)
        dbexecutor.addStockType('5 X 2,5 YASSI VİNÇ KAB.', self.metreid, sub.id)
        dbexecutor.addStockType('5 X 1,5 YASSI VİNÇ KAB.', self.metreid, sub.id)
        dbexecutor.addStockType('7 X 1,5 YASSI VİNÇ KAB.', self.metreid, sub.id)
        dbexecutor.addStockType('4 X 4 YASSI VİNÇ KAB.', self.metreid, sub.id)
        dbexecutor.addStockType('16 X 1,5 YASSI VİNÇ KAB.', self.metreid, sub.id)
        dbexecutor.addStockType('10 X 1,5 YASSI VİNÇ KAB.', self.metreid, sub.id)
        dbexecutor.addStockType('4 X 2,5 YASSI VİNÇ KAB.', self.metreid, sub.id)
        dbexecutor.addStockType('5 X 4 YASSI VİNÇ KAB.', self.metreid, sub.id)
        dbexecutor.addStockType('4 X 6 YASSI VİNÇ KAB.', self.metreid, sub.id)
        dbexecutor.addStockType('4 X 10 YASSI VİNÇ KAB.', self.metreid, sub.id)
        dbexecutor.addStockType('5 X 6 YASSI VİNÇ KAB.', self.metreid, sub.id)

    def preloadImalatHffrYassiVincKablosu(self, imalatid):
        sub = dbexecutor.addStockSubcategory('HFFR YASSI VİNÇ KABLOSU', imalatid)

    def preloadMegaMetal(self):
        mm = dbexecutor.addStockCategory('MEGA METAL')
        self.preloadMegaMetalBakir(mm.id)

    def preloadMegaMetalBakir(self, id):
        bakir = dbexecutor.addStockSubcategory('BAKIR', id)
        dbexecutor.addStockType('0,14 mm2 (7X0,160) BAKIR', self.metreid, bakir.id)
        dbexecutor.addStockType('0,22 mm2 (7X0,190) BAKIR', self.metreid, bakir.id)
        dbexecutor.addStockType('0,25 mm2 (7X0,210) BAKIR', self.metreid, bakir.id)
        dbexecutor.addStockType('0,50 mm2 (16X0,190) BAKIR', self.metreid, bakir.id)
        dbexecutor.addStockType('0,75 mm2 (24X0,190) BAKIR', self.metreid, bakir.id)
        dbexecutor.addStockType('1 mm2 (32X0,190) BAKIR', self.metreid, bakir.id)
        dbexecutor.addStockType('1,5 mm2 (29X0,250) BAKIR', self.metreid, bakir.id)
        dbexecutor.addStockType('2,5 mm2 (48X0,250) BAKIR', self.metreid, bakir.id)
        dbexecutor.addStockType('4 mm2 (54X0,300) BAKIR', self.metreid, bakir.id)
        dbexecutor.addStockType('6 mm2 (76X0,300) BAKIR', self.metreid, bakir.id)

    def preloadErBakir(self):
        eb = dbexecutor.addStockCategory('ER BAKIR')
        self.preloadErBakirBakir(eb.id)

    def preloadErBakirBakir(self, id):
        bakir = dbexecutor.addStockSubcategory('BAKIR', id)
        dbexecutor.addStockType('0,14 mm2 (7X0,160) BAKIR', self.metreid, bakir.id)
        dbexecutor.addStockType('0,22 mm2 (7X0,190) BAKIR', self.metreid, bakir.id)
        dbexecutor.addStockType('0,25 mm2 (7X0,210) BAKIR', self.metreid, bakir.id)
        dbexecutor.addStockType('0,50 mm2 (16X0,190) BAKIR', self.metreid, bakir.id)
        dbexecutor.addStockType('0,75 mm2 (24X0,190) BAKIR', self.metreid, bakir.id)
        dbexecutor.addStockType('1 mm2 (32X0,190) BAKIR', self.metreid, bakir.id)
        dbexecutor.addStockType('1,5 mm2 (29X0,250) BAKIR', self.metreid, bakir.id)
        dbexecutor.addStockType('2,5 mm2 (48X0,250) BAKIR', self.metreid, bakir.id)
        dbexecutor.addStockType('4 mm2 (54X0,300) BAKIR', self.metreid, bakir.id)
        dbexecutor.addStockType('6 mm2 (76X0,300) BAKIR', self.metreid, bakir.id)

    def preloadDevaPlastik(self):
        dp = dbexecutor.addStockCategory('DEVA PLASTİK')
        self.preloadDevaPlastikPvc(dp.id)

    def preloadDevaPlastikPvc(self, id):
        pvc = dbexecutor.addStockSubcategory('DEVA PLASTİK PVC', id)
        dbexecutor.addStockType('DEVA DP-1/65 KILIF SİYAH PVC GRANÜL', self.metreid, pvc.id)
        dbexecutor.addStockType('DEVA DP 1-40 NYAF NATUREL PVC GRANÜL', self.metreid, pvc.id)
        dbexecutor.addStockType('DEVA DP-90 PARLAK SİYAH', self.metreid, pvc.id)
        dbexecutor.addStockType('DEVA DP-2/75 SİYAH', self.metreid, pvc.id)

    def preloadEkerMotor(self):
        em = dbexecutor.addStockCategory('EKER MOTOR')
        self.preloadEkerMotor55kw(em.id)
        self.preloadEkerMotor4kw(em.id)
        self.preloadEkerMotorDislisiz(em.id)
        self.preloadEkerMotor75kw(em.id)
        self.preloadEkerMotor9kw(em.id)
        self.preloadEkerMotor11kw(em.id)
        self.preloadEkerMotor15kw(em.id)

    def preloadEkerMotor55kw(self, id):
        kw55 = dbexecutor.addStockSubcategory('5,5 kW', id)
        dbexecutor.addStockType('320kg 1,6mt/sn 5,5kW', self.adetid, kw55.id)
        dbexecutor.addStockType('450kg 0,63mt/sn 5,5kw', self.adetid, kw55.id)
        dbexecutor.addStockType('480kg 1mt/sn 5,5kw', self.adetid, kw55.id)
        dbexecutor.addStockType('480kg 1-0,24mt/sn 5,5kw', self.adetid, kw55.id)
        dbexecutor.addStockType('480kg 1mt/sn 5,5kw çift hız', self.adetid, kw55.id)
        dbexecutor.addStockType('630kg 1,6mt/sn 5,5kw', self.adetid, kw55.id)
        dbexecutor.addStockType('630kg 1mt/sn 5,5kw', self.adetid, kw55.id)

    def preloadEkerMotor4kw(self, id):
        kw4 = dbexecutor.addStockSubcategory('4 kW', id)
        dbexecutor.addStockType('480kg 0,63mt/sn 4kw', self.adetid, kw4.id)
        dbexecutor.addStockType('400kg 1mt/sn 4kw', self.adetid, kw4.id)

    def preloadEkerMotorDislisiz(self, id):
        dislisiz = dbexecutor.addStockSubcategory('DİŞLİSİZ', id)
        dbexecutor.addStockType('480kg 1mt/sn Dişlisiz', self.adetid, dislisiz.id)
        dbexecutor.addStockType('630kg 1mt/sn Dişlisiz', self.adetid, dislisiz.id)
        dbexecutor.addStockType('630kg 1,6mt/sn Dişlisiz', self.adetid, dislisiz.id)
        dbexecutor.addStockType('1300kg 1.0mt/sn dişlisiz', self.adetid, dislisiz.id)
        dbexecutor.addStockType('800kg dişlisiz 1mt/sn', self.adetid, dislisiz.id)
        dbexecutor.addStockType('800kg dişlisiz 1,6mt/sn', self.adetid, dislisiz.id)

    def preloadEkerMotor75kw(self, id):
        kw75 = dbexecutor.addStockSubcategory('7,5 kW', id)
        dbexecutor.addStockType('630kg 1,6mt/sn 7,5kw', self.adetid, kw75.id)
        dbexecutor.addStockType('630kg 1,00mt/sn 7,5 kw ÇİFTHIZ', self.adetid, kw75.id)
        dbexecutor.addStockType('800kg 1mt/sn 7,5kw', self.adetid, kw75.id)
        dbexecutor.addStockType('Stronglite 800 kg 1mt/sn 7,5kw', self.adetid, kw75.id)

    def preloadEkerMotor9kw(self, id):
        kw9 = dbexecutor.addStockSubcategory('9 kW', id)
        dbexecutor.addStockType('630kg 2,00 mt/sn 9kw ', self.adetid, kw9.id)
        dbexecutor.addStockType('1000 kg 1m/sn 9 kw', self.adetid, kw9.id)
        dbexecutor.addStockType('1250kg 1m/sn 9kw', self.adetid, kw9.id)
        dbexecutor.addStockType('800kg 1,2mt/sn 9kw', self.adetid, kw9.id)
        dbexecutor.addStockType('1250 kg 1.00mt/sn 9 kw 2/1 ASKI', self.adetid, kw9.id)
        dbexecutor.addStockType('800kg 1,6mt/sn 9kw', self.adetid, kw9.id)
        dbexecutor.addStockType('1250 kg 1.00mt/sn 9 kw 2/1 ASKI', self.adetid, kw9.id)

    def preloadEkerMotor11kw(self, id):
        kw11 = dbexecutor.addStockSubcategory('11 kW', id)
        dbexecutor.addStockType('800kg 2.00mt/sn 11kw', self.adetid, kw11.id)
        dbexecutor.addStockType('1000kg 1,6mt/sn 11kw', self.adetid, kw11.id)
        dbexecutor.addStockType('1300kg 1m/sn 11kw', self.adetid, kw11.id)
        dbexecutor.addStockType('1250 kg 1.6mt/sn 11 kw 2/1 ASKI', self.adetid, kw11.id)

    def preloadEkerMotor15kw(self, id):
        kw15 = dbexecutor.addStockSubcategory('15 kW', id)
        dbexecutor.addStockType('1300kg 1,6m/sn 15kw', self.adetid, kw15.id)
        dbexecutor.addStockType('STP-1.6m/sn 1250 KG WVF 15 KW', self.adetid, kw15.id)

    def preloadClindasMotor(self):
        cm = dbexecutor.addStockCategory('CLİNDAS MOTOR')

        kw55 = dbexecutor.addStockSubcategory('5,5 kW', cm.id)
        dbexecutor.addStockType('630kg 1mt/sn 5,5kw clindas TC5', self.adetid, kw55.id)

        kw5 = dbexecutor.addStockSubcategory('4 kW', cm.id)

        dislisiz = dbexecutor.addStockSubcategory('DİŞLİSİZ', cm.id)

        kw75 = dbexecutor.addStockSubcategory('7,5 kW', cm.id)
        dbexecutor.addStockType('800kg 1mt/sn 7,5kw clindas', self.adetid, kw75.id)
        dbexecutor.addStockType('800kg 1mt/sn 7,5kw clindas EC -7', self.adetid, kw75.id)

        kw9 = dbexecutor.addStockSubcategory('9 kW', cm.id)
