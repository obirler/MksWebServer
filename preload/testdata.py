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

    def preLoadTestData(self):
        self.preloadtestcorporation()
        self.preloadteststockrooms()
        self.preloadusers()
        self.preloadRandomTestEntries()

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

    def preloadRandomTestEntries(self):
        generator = preload.randomentrygenerator.RandomEntryGenerator()
        generator.addRandomCategories(30)
        generator.addDepotStockEntries(40)
        generator.addEntries(300)

