import random
import dbexecutor
import util
import string
from datetime import datetime
import time
import json


class RandomEntryGenerator():
    adminids = []
    unitids = []
    stocktypeids = []
    stockcolorids = []
    stockpackageids = []
    corporationids = []
    depotstockids = []
    stockroomids = []
    formnames = ['Random', 'Form', 'Name', '123', '12', 'A', 'Form1', 'Form2', 'Form3', 'Form4', 'Form5', 'Rnd',
                 'Entry']
    decriptions = ['Random', 'Desc', 'Açıklama', '123', '12', 'A', 'Desc1', 'Desc2', 'Desc3', 'Desc4', 'Desc5', 'Örnek',
                   'Entry', 'Girdi', 'Açıklama Örneği', 'Bir', 'Malzeme']
    shiinfos = ['', '', '', '', 'Kamyon', 'Otobüs', 'Otomobil', 'Kepçe', 'Buldozer', 'Uçak', 'Forklift']

    def __init__(self):
        self.loadids()
        random.seed(time.thread_time_ns())

    def loadids(self):
        self.adminids = dbexecutor.getAllAdminIds()
        self.unitids = dbexecutor.getAllStockUnitIds()
        self.stocktypeids = dbexecutor.getAllStockTypeIds()
        self.stockcolorids = dbexecutor.getAllStockColorIds()
        self.stockpackageids = dbexecutor.getAllStockPackageIds()
        self.corporationids = dbexecutor.getAllCorporationIds()
        self.depotstockids = dbexecutor.getAllDepotStockIds()
        self.stockroomids = dbexecutor.getAllStockRoomIds()

    def addEntries(self, number):
        rndsel = [1, 2, 3, 4]
        for i in range(number):
            t = time.time()
            tns = time.time_ns()
            tts = time.thread_time()
            ttns = time.thread_time_ns()
            p = time.process_time()
            pns = time.process_time()
            pc = time.perf_counter()
            pcns = time.perf_counter_ns()
            m = time.monotonic()
            mns = time.monotonic_ns()
            random.seed(t)
            print('t=' + str(t))
            print('tns=' + str(tns))
            print('tts=' + str(tts))
            print('ttns=' + str(ttns))
            print('p=' + str(p))
            print('pns=' + str(pns))
            print('pc=' + str(pc))
            print('pcns=' + str(pcns))
            print('m=' + str(m))
            print('mns=' + str(mns))
            sel = random.choice(rndsel)
            print('selection=' + str(sel))
            if sel == 1:
                self.addRandomDepotStock()
            elif sel == 2:
                self.addRandomIncomingStockForm()
            elif sel == 3:
                self.addRandomOutGoingStockForm()
            elif sel == 4:
                self.removeRandomDepotStock()

    def addDepotStockEntries(self, length):
        for i in range(length):
            self.addRandomDepotStock()

    def addRandomDepotStock(self):
        userid = self.getRandomAdminUser().id
        colorid = self.getRandomStockColor().id
        typeid = self.getRandomStockType().id
        depotstock = dbexecutor.getDepotStockByTypeAndColor(typeid, colorid)

        while depotstock is not None:
            colorid = self.getRandomStockColor().id
            typeid = self.getRandomStockType().id
            depotstock = dbexecutor.getDepotStockByTypeAndColor(typeid, colorid)

        dbexecutor.handleDepotStockAdd(userid, typeid, colorid, random.randint(1, 2000))

    def removeRandomDepotStock(self):
        userid = self.getRandomAdminUser().id
        colorid = self.getRandomStockColor().id
        typeid = self.getRandomStockType().id
        depotstock = dbexecutor.getDepotStockByTypeAndColor(typeid, colorid)

        while depotstock is None:
            colorid = self.getRandomStockColor().id
            typeid = self.getRandomStockType().id
            depotstock = dbexecutor.getDepotStockByTypeAndColor(typeid, colorid)

        dbexecutor.handleDepotStockUpdate(depotstock.id, userid, typeid, colorid,
                                          random.randint(1, int(depotstock.quantity)))

    def addRandomIncomingStockForm(self):
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

        user = self.getRandomAdminUser()
        dbexecutor.addIncomingStockFormFromJson(user, form)

    def addRandomOutGoingStockForm(self):
        form = {}
        form['name'] = self.getRandomFormName()
        form['corporationid'] = self.getRandomCorporation().id
        form['shipinfo'] = self.getRandomShipInfo()
        form['stockroomid'] = self.getRandomStockRoom().id
        dt = util.htmldateTime(self.getRandomTime())
        form['recorddate'] = dt

        rnd = random.randint(1, 6)
        outgoingstocks = []
        for i in range(0, rnd):
            colorid = self.getRandomStockColor().id
            typeid = self.getRandomStockType().id
            depotstock = dbexecutor.getDepotStockByTypeAndColor(typeid, colorid)

            while depotstock is None:
                colorid = self.getRandomStockColor().id
                typeid = self.getRandomStockType().id
                depotstock = dbexecutor.getDepotStockByTypeAndColor(typeid, colorid)

            outstock = {}
            outstock['stocktypeid'] = typeid
            outstock['stockcolorid'] = colorid
            outstock['stockpackageid'] = self.getRandomStockPackage().id

            qtty = random.randint(1, int(depotstock.quantity))
            outstock['quantity'] = qtty

            pqty = random.randint(1, 100)
            outstock['packagequantity'] = pqty
            outstock['stocknote'] = self.getRandomDescription()
            outgoingstocks.append(outstock)
        form['outgoingstocks'] = outgoingstocks

        user = self.getRandomAdminUser()
        dbexecutor.addOutgoingStockFormFromJson(user, form)

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

    def getRandomStockRoom(self):
        """
        Gets a random available StockRoom

        :return: The random available StockRoom
        :rtype: models.StockRoom
        """

        randid = random.choice(self.stockroomids)
        return dbexecutor.getStockRoom(randid)

    def getRandomFormName(self):
        """
        Gets a random form name

        :return: The random form name
        :rtype: str
        """

        lngth = random.randint(1, 9)
        strng = ''
        t = time.time()
        tns = time.time_ns()
        tts = time.thread_time()
        ttns = time.thread_time_ns()
        p = time.process_time()
        pns = time.process_time()
        pc = time.perf_counter()
        pcns = time.perf_counter_ns()
        m = time.monotonic()
        mns = time.monotonic_ns()
        print('t=' + str(t))
        print('tns=' + str(tns))
        print('tts=' + str(tts))
        print('ttns=' + str(ttns))
        print('p=' + str(p))
        print('pns=' + str(pns))
        print('pc=' + str(pc))
        print('pcns=' + str(pcns))
        print('m=' + str(m))
        print('mns=' + str(mns))
        random.seed(t)
        for i in range(lngth):
            strng += random.choice(self.formnames) + ' '
        return strng

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

    def getRandomShipInfo(self):
        """
        Gets a random shipinfo

        :return: The random shipinfo
        :rtype: str
        """

        citycode = random.randint(1, 81)
        rstr = self.getRandomString(3)

        postcode = random.randint(1, 100)

        return str(citycode) + rstr + str(postcode) + ' Araç ' + random.choice(self.shiinfos)

    def getRandomTime(self):

        start = datetime.strptime('14/05/1992 01:00 AM', '%d/%m/%Y %I:%M %p')
        end = datetime.strptime('06/01/2021 11:59 AM', '%d/%m/%Y %I:%M %p')
        rnd = util.randomDate(start, end)
        return rnd

    def getRandomString(self, length):
        # Random string with the combination of lower and upper case
        letters = string.ascii_letters

        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str
