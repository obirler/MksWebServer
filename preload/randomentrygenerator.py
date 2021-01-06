import random
import dbexecutor
import util
from datetime import datetime
import json


class RandomEntryGenerator():
    adminids = []
    unitids = []
    stocktypeids = []
    stockcolorids = []
    stockpackageids = []
    corporationids = []
    formnames = ['Random', 'Form', 'Name', '123', '12', 'A', 'Form1', 'Form2', 'Form3', 'Form4', 'Form5', 'Rnd',
                 'Entry']
    decriptions = ['Random', 'Desc', 'Açıklama', '123', '12', 'A', 'Desc1', 'Desc2', 'Desc3', 'Desc4', 'Desc5', 'Örnek',
                   'Entry', 'Girdi', 'Açıklama Örneği', 'Bir', 'Malzeme']

    def __init__(self, adminids, unitids, stocktypeids, stockcolorids, stockpackageids, corporationids):
        self.adminids = adminids
        self.unitids = unitids
        self.stocktypeids = stocktypeids
        self.stockcolorids = stockcolorids
        self.stockpackageids = stockpackageids
        self.corporationids = corporationids

    def getRandomIncomingStockForm(self):
        form = {}
        form['name'] = self.getRandomFormName()
        form['corporationid'] = self.getRandomCorporation().id
        dt = util.htmldateTime(self.getRandomTime())
        form['recorddate'] = dt
        rnd = random.randint(1, 6)
        incomingstocks = []
        for i in range(0, rnd):
            incstock = {}
            incstock['stocktypeid'] = self.getRandomStockType().id
            incstock['stockcolorid'] = self.getRandomStockColor().id
            incstock['stockpackageid'] = self.getRandomStockPackage().id
            qtty = random.randint(1, 2000)
            incstock['quantity'] = qtty
            pqty = random.randint(1, 100)
            incstock['packagequantity'] = pqty
            incstock['stocknote'] = self.getRandomDescription()
            incomingstocks.append(incstock)
        form['incomingstocks'] = incomingstocks
        return form

    def getRandomAdminUser(self):
        """
        Gets a random available admin User

        :return: The random available admin User
        :rtype: models.User
        """
        randid = random.choice(self.adminids)
        return dbexecutor.getUser(randid)

    def getRandomStockType(self):
        """
        Gets a random available StockType

        :return: The random available StockType
        :rtype: models.StockType
        """
        randid = random.choice(self.stocktypeids)
        return dbexecutor.getStockType(randid)

    def getRandomStockColor(self):
        """
        Gets a random available StockColor

        :return: The random available StockColor
        :rtype: models.StockColor
        """
        randid = random.choice(self.stockcolorids)
        return dbexecutor.getStockColor(randid)

    def getRandomStockPackage(self):
        """
        Gets a random available StockPackage

        :return: The random available StockPackage
        :rtype: models.StockPackage
        """
        randid = random.choice(self.stockpackageids)
        return dbexecutor.getStockPackage(randid)

    def getRandomCorporation(self):
        """
        Gets a random available Corporation

        :return: The random available Corporation
        :rtype: models.Corporation
        """
        randid = random.choice(self.corporationids)
        return dbexecutor.getCorporation(randid)

    def getRandomFormName(self):
        """
        Gets a random form name

        :return: The random form name
        :rtype: str
        """
        lngth = random.randint(1, 9)
        str = ''
        for i in range(lngth):
            str += random.choice(self.formnames) + ' '
        return str

    def getRandomDescription(self):
        """
        Gets a random description

        :return: The random description
        :rtype: str
        """
        lngth = random.randint(1, 9)
        str = ''
        for i in range(lngth):
            str += random.choice(self.decriptions) + ' '
        return str

    def getRandomTime(self):
        start = datetime.strptime('14/05/1992 01:00 AM', '%d/%m/%Y %I:%M %p')
        end = datetime.strptime('06/01/2021 11:59 AM', '%d/%m/%Y %I:%M %p')
        rnd = util.randomDate(start, end)
        return rnd
