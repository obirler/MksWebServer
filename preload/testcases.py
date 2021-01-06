import dbexecutor


class TestCases():
    adetid = None
    metreid = None
    kiloid = None

    def __init__(self, kiloid, metreid, adetid):
        self.kiloid = kiloid
        self.metreid = metreid
        self.adetid = adetid

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
