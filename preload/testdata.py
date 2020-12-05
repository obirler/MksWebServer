import dbexecutor
import json
from flask_login import current_user
from flask import jsonify
from preload import category


class TestData():

    def __init__(self):
        self.metre = -2
        self.kilo = -2

    def preLoadData(self):
        self.preloadMandotaryEntries()
        self.preloadTestEntries()

    def preloadMandotaryEntries(self):
        self.preloadstockunits()
        catload = category.CategoryLoad(self.adet.id, self.metre.id, self.kilo.id)
        catload.preloadCategories()
        # self.preloadTestCategories()

        self.preloadstockcolors()
        self.preloadstockpackage()
        self.preloadcorporation()
        self.preloadstockrooms()

    def preloadTestEntries(self):
        # self.preloadstockformtest()
        # self.preloadstockincomingaddoutgoingstockaddformtest()
        # self.preloadstockincomingaddoutgoingstockaddeditformtest()
        self.preloadaddeditdepotstock()
        self.preloadstockincomingaddeditoutgoingstockaddeditformtest()

    def preloadTestCategories(self):
        self.preloadTestCat1()
        self.preloadTestCat2()

    def preloadTestCat1(self):
        cat1 = dbexecutor.addStockCategory('Category 1')

        cat1sub1 = dbexecutor.addStockSubcategory('Cat 1 Sub 1', cat1.id)
        dbexecutor.addStockType('Type 1 Cat 1 Sub 1 ', self.metre.id, cat1sub1.id)
        dbexecutor.addStockType('Type 2 Cat 1 Sub 1 ', self.adet.id, cat1sub1.id)
        dbexecutor.addStockType('Type 3 Cat 1 Sub 1 ', self.kilo.id, cat1sub1.id)

        cat1sub2 = dbexecutor.addStockSubcategory('Cat 1 Sub 2', cat1.id)
        dbexecutor.addStockType('Type 1 Cat 1 Sub 2 ', self.metre.id, cat1sub2.id)
        dbexecutor.addStockType('Type 2 Cat 1 Sub 2 ', self.kilo.id, cat1sub2.id)

        cat1sub3 = dbexecutor.addStockSubcategory('Cat 1 Sub 3', cat1.id)
        dbexecutor.addStockType('Type 1 Cat 1 Sub 3 ', self.adet.id, cat1sub3.id)
        dbexecutor.addStockType('Type 2 Cat 1 Sub 3 ', self.kilo.id, cat1sub3.id)

    def preloadTestCat2(self):
        cat2 = dbexecutor.addStockCategory('Category 2')

        cat2sub1 = dbexecutor.addStockSubcategory('Cat 2 Sub 1', cat2.id)
        dbexecutor.addStockType('Type 1 Cat 2 Sub 1 ', self.metre.id, cat2sub1.id)
        dbexecutor.addStockType('Type 2 Cat 2 Sub 1 ', self.kilo.id, cat2sub1.id)
        dbexecutor.addStockType('Type 3 Cat 2 Sub 1 ', self.adet.id, cat2sub1.id)

        cat2sub2 = dbexecutor.addStockSubcategory('Cat 2 Sub 2', cat2.id)
        dbexecutor.addStockType('Type 1 Cat 2 Sub 2 ', self.kilo.id, cat2sub2.id)
        dbexecutor.addStockType('Type 2 Cat 2 Sub 2 ', self.adet.id, cat2sub2.id)

        cat2sub3 = dbexecutor.addStockSubcategory('Cat 2 Sub 3', cat2.id)
        dbexecutor.addStockType('Type 1 Cat 2 Sub 3 ', self.metre.id, cat2sub3.id)
        dbexecutor.addStockType('Type 2 Cat 2 Sub 3 ', self.adet.id, cat2sub3.id)

    def preloadstockunits(self):
        self.adet = dbexecutor.addStockUnit('Adet', 0)
        self.metre = dbexecutor.addStockUnit('Metre', 2)
        self.kilo = dbexecutor.addStockUnit('Kilogram', 1)

    def preloadstocktypes(self):
        '''
        dbexecutor.addStockType('Vinç Kablosu', 2)
        dbexecutor.addStockType('1070 Ti Ekran Kartı', 1)
        dbexecutor.addStockType('Bakır Kablo', 3)
        dbexecutor.addStockType('Ryzen 3600 İşlemci', 1)
        '''

    def preloadstockcolors(self):
        dbexecutor.addStockColor("Gri")
        dbexecutor.addStockColor("Sarı-Yeşil")
        dbexecutor.addStockColor("Lila")
        dbexecutor.addStockColor("Siyah")
        dbexecutor.addStockColor("Mavi")
        dbexecutor.addStockColor("Yeşil")
        dbexecutor.addStockColor("Beyaz")
        dbexecutor.addStockColor("Kahve")
        dbexecutor.addStockColor("Kımızı")
        dbexecutor.addStockColor("Mor")
        dbexecutor.addStockColor("Sarı")
        dbexecutor.addStockColor("Turuncu")

    def preloadstockpackage(self):
        dbexecutor.addStockPackage("Koli")
        dbexecutor.addStockPackage("Çuval")
        dbexecutor.addStockPackage("Torba")

    def preloadcorporation(self):
        dbexecutor.addCorporation("Mega Metal")
        dbexecutor.addCorporation("Er Bakır")
        dbexecutor.addCorporation("Deva Plastik")
        dbexecutor.addCorporation("Eker Motor")

    def preloadstockrooms(self):
        dbexecutor.addStockRoom("Şentaş")
        dbexecutor.addStockRoom("Günaydın")
        dbexecutor.addStockRoom("Özkan")
        dbexecutor.addStockRoom("K. A.")

    def preloadusers(self):
        dbexecutor.addUser('omer', 'Ömer', 'Birler', '1234', False)
        dbexecutor.addUser('yasar', 'Ali', 'Yaşar', '1234', False)
        dbexecutor.addUser('temiz', 'Yusuf', 'Temiz', '1234', False)

    def addincomingstockform(self):
        json1string = {
            "name": "Form1 test",
            "corporationid": 1,
            "recorddate": "",
            "incomingstocks":
            [
                {
                    "stocktypeid": 1,
                    "stockcolorid": 2,
                    "stockpackageid": 2,
                    "quantity": 10,
                    "packagequantity": 1,
                    "stocknote": "A test note about 1"
                },
                {
                    "stocktypeid": 2,
                    "stockcolorid": 1,
                    "stockpackageid": 1,
                    "quantity": 15,
                    "packagequantity": 1,
                    "stocknote": "A test note about 2"
                }
            ]
        }

        return json1string

    def editincomingstockform(self):
        json1string = {
            "name": "Form1 test",
            "corporationid": 1,
            "recorddate": "",
            "incomingstocks":
            [
                {
                    "stocktypeid": 1,
                    "stockcolorid": 2,
                    "stockpackageid": 2,
                    "quantity": 15,
                    "packagequantity": 1,
                    "stocknote": "A test note about 1"
                }
            ]
        }

        return json1string

    def editincomingstockform2(self):
        json1string = {
            "name": "Form1 test",
            "corporationid": 1,
            "recorddate": "",
            "incomingstocks":
            [
                {
                    "stocktypeid": 1,
                    "stockcolorid": 2,
                    "stockpackageid": 2,
                    "quantity": 20,
                    "packagequantity": 1,
                    "stocknote": "A test note about 1"
                },
                {
                    "stocktypeid": 2,
                    "stockcolorid": 1,
                    "stockpackageid": 1,
                    "quantity": 13,
                    "packagequantity": 1,
                    "stocknote": "A test note about 2"
                }
            ]
        }

        return json1string

    def addoutgoingstockform(self):
        json1string = {
            "name": "Form1 test",
            "corporationid": 1,
            "shipinfo": "34 abc 123",
            "stockroomid": 1,
            "recorddate": "",
            "outgoingstocks":
            [
                {
                    "stocktypeid": 1,
                    "stockcolorid": 2,
                    "stockpackageid": 2,
                    "quantity": 3,
                    "packagequantity": 1,
                    "stocknote": "A test note about 1"
                },
                {
                    "stocktypeid": 2,
                    "stockcolorid": 1,
                    "stockpackageid": 1,
                    "quantity": 5,
                    "packagequantity": 1,
                    "stocknote": "A test note about 2"
                }
            ]
        }

        return json1string

    def editoutgoingstockform(self):
        json1string = {
            "name": "Form1 test",
            "corporationid": 1,
            "shipinfo": "34 abc 123",
            "stockroomid": 1,
            "recorddate": "",
            "outgoingstocks":
            [
                {
                    "stocktypeid": 1,
                    "stockcolorid": 2,
                    "stockpackageid": 2,
                    "quantity": 3,
                    "packagequantity": 1,
                    "stocknote": "A test note about 1"
                }
            ]
        }

        return json1string

    def preloadincomingstockaddeditformtest(self):
        user = dbexecutor.getUser(1)
        json1 = self.addincomingstockform()
        dbexecutor.addIncomingStockFormFromJson(user, json1)

        json2 = self.editincomingstockform()
        dbexecutor.updateIncomingStockFormFromJson(1, user, json2)

    def preloadstockincomingaddoutgoingstockaddformtest(self):
        user = dbexecutor.getUser(1)
        json1 = self.addincomingstockform()
        dbexecutor.addIncomingStockFormFromJson(user, json1)

        json2 = self.addoutgoingstockform()
        dbexecutor.addOutgoingStockFormFromJson(user, json2)

    def preloadstockincomingaddoutgoingstockaddeditformtest(self):
        user = dbexecutor.getUser(1)
        json1 = self.addincomingstockform()
        dbexecutor.addIncomingStockFormFromJson(user, json1)

        json2 = self.addoutgoingstockform()
        dbexecutor.addOutgoingStockFormFromJson(user, json2)

        json3 = self.editoutgoingstockform()
        dbexecutor.updateOutgoingStockFormFromJson(1, user, json3)

    def preloadstockincomingaddeditoutgoingstockaddeditformtest(self):
        user = dbexecutor.getUser(1)
        json1 = self.addincomingstockform()
        dbexecutor.addIncomingStockFormFromJson(user, json1)

        json2 = self.editincomingstockform2()
        dbexecutor.updateIncomingStockFormFromJson(1, user, json2)

        json3 = self.addoutgoingstockform()
        dbexecutor.addOutgoingStockFormFromJson(user, json3)

        json4 = self.editoutgoingstockform()
        dbexecutor.updateOutgoingStockFormFromJson(1, user, json4)

    def preloadaddeditdepotstock(self):
        user = dbexecutor.getUser(1)
        dbexecutor.handleDepotStockAdd(user.id, 1, 2, 10)
        dbexecutor.handleDepotStockAdd(user.id, 2, 1, 5)

        dbexecutor.handleDepotStockUpdate(1, user.id, 1, 2, 20)
        dbexecutor.handleDepotStockUpdate(2, user.id, 2, 1, 10)