import dbexecutor
import models
import preload.randomentrygenerator
import json

class TestData():
    adetid = None
    metreid = None
    kiloid = None
    adminids = []
    unitids = []
    stocktypeids = []
    stockcolorids = []
    stockpackageids = []
    corporationids = []

    def __init__(self, kiloid, metreid, adetid):
        self.kiloid = kiloid
        self.metreid = metreid
        self.adetid = adetid

    def loadids(self):
        self.adminids = dbexecutor.getAllAdminIds()
        self.unitids = dbexecutor.getAllStockUnitIds()
        self.stocktypeids = dbexecutor.getAllStockTypeIds()
        self.stockcolorids = dbexecutor.getAllStockColorIds()
        self.stockpackageids = dbexecutor.getAllStockPackageIds()
        self.corporationids = dbexecutor.getAllCorporationIds()

    def preLoadTestData(self):
        self.preloadtestcorporation()
        self.preloadteststockrooms()
        self.preloadusers()
        self.preloadTestCategories()
        self.loadids()
        self.preloadTestIncomingStockForm()

    def preloadTestCategories(self):
        self.preloadTestCat1()
        self.preloadTestCat2()

    def preloadTestCat1(self):
        cat1 = dbexecutor.addStockCategory('Category 1')

        cat1sub1 = dbexecutor.addStockSubcategory('Cat 1 Sub 1', cat1.id)
        dbexecutor.addStockType('Type 1 Cat 1 Sub 1 ', self.metreid, cat1sub1.id)
        dbexecutor.addStockType('Type 2 Cat 1 Sub 1 ', self.adetid, cat1sub1.id)
        dbexecutor.addStockType('Type 3 Cat 1 Sub 1 ', self.kiloid, cat1sub1.id)

        cat1sub2 = dbexecutor.addStockSubcategory('Cat 1 Sub 2', cat1.id)
        dbexecutor.addStockType('Type 1 Cat 1 Sub 2 ', self.metreid, cat1sub2.id)
        dbexecutor.addStockType('Type 2 Cat 1 Sub 2 ', self.kiloid, cat1sub2.id)

        cat1sub3 = dbexecutor.addStockSubcategory('Cat 1 Sub 3', cat1.id)
        dbexecutor.addStockType('Type 1 Cat 1 Sub 3 ', self.adetid, cat1sub3.id)
        dbexecutor.addStockType('Type 2 Cat 1 Sub 3 ', self.kiloid, cat1sub3.id)

    def preloadTestCat2(self):
        cat2 = dbexecutor.addStockCategory('Category 2')

        cat2sub1 = dbexecutor.addStockSubcategory('Cat 2 Sub 1', cat2.id)
        dbexecutor.addStockType('Type 1 Cat 2 Sub 1 ', self.metreid, cat2sub1.id)
        dbexecutor.addStockType('Type 2 Cat 2 Sub 1 ', self.kiloid, cat2sub1.id)
        dbexecutor.addStockType('Type 3 Cat 2 Sub 1 ', self.adetid, cat2sub1.id)

        cat2sub2 = dbexecutor.addStockSubcategory('Cat 2 Sub 2', cat2.id)
        dbexecutor.addStockType('Type 1 Cat 2 Sub 2 ', self.kiloid, cat2sub2.id)
        dbexecutor.addStockType('Type 2 Cat 2 Sub 2 ', self.adetid, cat2sub2.id)

        cat2sub3 = dbexecutor.addStockSubcategory('Cat 2 Sub 3', cat2.id)
        dbexecutor.addStockType('Type 1 Cat 2 Sub 3 ', self.metreid, cat2sub3.id)
        dbexecutor.addStockType('Type 2 Cat 2 Sub 3 ', self.adetid, cat2sub3.id)

    def preloadtestcorporation(self):
        dbexecutor.addCorporation("Ferrous Corp")
        dbexecutor.addCorporation("Mikkei Combine")
        dbexecutor.addCorporation("CoreLactic Industries")
        dbexecutor.addCorporation("Dwarf Star Technologies")
        dbexecutor.addCorporation("Traugott Corp")
        dbexecutor.addCorporation("Transfer Transit")
        dbexecutor.addCorporation("Volkov-Rusi")

    def preloadteststockrooms(self):
        dbexecutor.addStockRoom("EOS-7")
        dbexecutor.addStockRoom("Regulus-12")
        dbexecutor.addStockRoom("Hyperion-8")
        dbexecutor.addStockRoom("Hyadum-12")
        dbexecutor.addStockRoom("Eridani-6")
        dbexecutor.addStockRoom("Lankarn Nebula")

    def preloadusers(self):
        dbexecutor.addUser('omer', 'Ömer', 'Birler', '1234', True)
        dbexecutor.addUser('plin', 'Portia', 'Lin', '1234', True)
        dbexecutor.addUser('mossd', 'Derrick', 'Moss', '1234', False)
        dbexecutor.addUser('emilyk', 'Emily', 'Kolburn', '1234', True)
        dbexecutor.addUser('kalv', 'Kal', 'Varrick', '1234', False)
        dbexecutor.addUser('boonem', 'Marcus', 'Boone', '1234', True)
        dbexecutor.addUser('ryot', 'Ryo', 'Tetsuda', '1234', False)
        dbexecutor.addUser('harpern', 'Nyx', 'Harper', '1234', True)

    def preloadTestIncomingStockForm(self):
        generator = preload.randomentrygenerator.RandomEntryGenerator(self.adminids, self.unitids, self.stocktypeids,
                                                                      self.stockcolorids, self.stockpackageids,
                                                                      self.corporationids)
        for i in range(100):
            user = generator.getRandomAdminUser()
            jsn = generator.getRandomIncomingStockForm()
            dbexecutor.addIncomingStockFormFromJson(user, jsn)

    def preloadincomingdepotstock(self):
        return ""

    def preLoadFormEntries(self):
        return ""
