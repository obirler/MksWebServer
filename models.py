from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, DateTime
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash
from datetime import datetime
from config import Base
import dbexecutor
from util import turkishTimeNow


class User(UserMixin, Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    name = Column(String(50))
    surname = Column(String(50))
    isadmin = Column(Boolean, default=False)
    createdate = Column(DateTime, default=datetime.utcnow())
    changedate = Column(DateTime, default=datetime.utcnow())
    password = Column(String(100))
    mockpassword = Column(String(70))

    def __init__(self, username=None, password=None, name=None, surname=None, isadmin=False):
        """
        Initializes a new instance of User class

        :param username: The user name of the User
        :type username: str
        :param password: The password of the User
        :type password: str
        :param name: The name of the User
        :type name: str
        :param surname: The surname of the User
        :type surname: str
        :param isadmin: Whether the user is admin or not
        :type isadmin: bool
        """
        self.username = username
        self.setPassword(password)
        self.name = name
        self.surname = surname
        self.isadmin = isadmin
        self.createdate = turkishTimeNow()
        self.changedate = turkishTimeNow()

    def setPassword(self, password):
        """
        Sets the password of the User

        :param password: The password of the User
        :type password: str
        """
        hashed_password = generate_password_hash(password, method='sha256')
        self.password = hashed_password
        i = 0
        mockpass = ''
        while i < len(password):
            mockpass = mockpass + '*'
            i += 1
        self.mockpassword = mockpass

    def getFullName(self):
        """
        Gets the full name of the User
        :return: The full name of the User
        :rtype: str
        """
        return self.name + ' ' + self.surname

    def get_id(self):
        """
        Returns the id to satisfy Flask-Login's requirements.

        :return: The id of the User
        :rtype: int
        """
        return self.id

    def change(self, username=None, password=None, name=None, surname=None, isadmin=False):
        """
        Changes User class fields

        :param username: The new user name of the User
        :type username: str
        :param password: The new password of the User
        :type password: str
        :param name: The new name of the User
        :type name: str
        :param surname: The new surname of the User
        :type surname: str
        :param isadmin: Whether the User is admin or not
        :type isadmin: bool
        """
        self.username = username
        self.setPassword(password)
        self.name = name
        self.surname = surname
        self.isadmin = isadmin
        self.changedate = turkishTimeNow()

    def __repr__(self):
        return "<User(id='%s', username='%s', name='%s', surname='%s', isadmin='%s', password='%s', mockpassword='%s')>" % (
            self.id, self.username, self.name, self.surname, self.isadmin, self.password, self.mockpassword)


class StockCategory(Base):
    __tablename__ = 'stockcategory'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

    def __init__(self, name=None):
        """
        Initializes a new instance of StockCategory class

        :param name: The name of the StockCategory
        :type name: str
        """
        self.name = name

    def serialize(self):
        """
        Serializes the class
        :return: The dictionary of all fields
        :rtype: dict
        """
        return {
            'id': self.id,
            'name': self.name
        }

    def __repr__(self):
        return "<StockCategory(id='%s', name='%s')>" % (self.id, self.name)


class StockSubcategory(Base):
    __tablename__ = 'stocksubcategory'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    categoryid = Column(Integer, ForeignKey(StockCategory.id, ondelete='RESTRICT'), nullable=False)

    def __init__(self, name=None, categoryid=None):
        """
        Initializes a new instance of StockSubcategory class

        :param name: The name of the StockSubcategory
        :type name: str
        :param categoryid: The id of StockCategory of the StockSubcategory
        :type categoryid: int
        """
        self.name = name
        self.categoryid = categoryid

    def getStockCategory(self):
        """
        Gets StockCategory of this StockSubcategory
        :return: StockCategory of this StockSubcategory
        :rtype: StockCategory
        """
        cat = dbexecutor.getStockCategory(self.categoryid)
        return cat

    def serialize(self):
        """
        Serializes the class
        :return: The dictionary of all fields
        :rtype: dict
        """
        return {
            'id': self.id,
            'name': self.name,
            'categoryid': self.categoryid
        }

    def __repr__(self):
        return "<StockSubcategory(id='%s', name='%s', categoryid='%s')>" % (self.id, self.name, self.categoryid)


class StockUnit(Base):
    __tablename__ = 'stockunit'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    precision = Column(Integer)

    def __init__(self, name=None, precision=None):
        """
        Initializes a new instance of StockUnit class

        :param name: The name of the StockUnit
        :type name: str
        :param precision: The precision of the StockUnit
        :type precision: int
        """
        self.name = name
        self.precision = precision

    def serialize(self):
        """
        Serializes the class
        :return: The dictionary of all fields
        :rtype: dict
        """
        return {
            'id': self.id,
            'name': self.name,
            'precision': self.precision,
            'precisionlist': '[0,1,2,3,4,5]'
        }

    def __repr__(self):
        return "<StockUnit(id='%s', name='%s', precision='%s')>" % (self.id, self.name, self.precision)


class StockType(Base, object):
    __tablename__ = 'stocktype'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    unitid = Column(Integer, ForeignKey('stockunit.id'), nullable=False)
    subcategoryid = Column(Integer, ForeignKey('stocksubcategory.id'), nullable=False)

    def __init__(self, name=None, unitid=None, subcategoryid=None):
        """
        Initializes a new instance of StockType class

        :param name: The name of the StockType
        :type name: str
        :param unitid: The StockUnit id of the StockType
        :type unitid: int
        :param subcategoryid: The StockSubcategory id of the StockType
        :type subcategoryid: int
        """
        self.name = name
        self.unitid = unitid
        self.subcategoryid = subcategoryid

    def getUnitName(self):
        """
        Gets the name of StockUnit of this StockType

        :return: The name of StockUnit
        :rtype: str
        """
        unit = dbexecutor.getStockUnit(self.unitid)
        if unit is not None:
            return unit.name
        else:
            return None

    def getUnitPrecision(self):
        """
        Gets the precisiom of StockUnit of this StockType

        :return: The precisiom of StockUnit
        :rtype: int
        """
        unit = dbexecutor.getStockUnit(self.unitid)
        if unit is not None:
            return unit.precision
        else:
            return None

    def getStockSubcategory(self):
        """
        Gets StockCategory of the StockType
        :return: StockCategory of the StockType
        :rtype: StockSubcategory
        """
        subcat = dbexecutor.getStockSubcategory(self.subcategoryid)
        return subcat

    def serialize(self):
        """
        Serializes the class
        :return: The dictionary of all fields
        :rtype: dict
        """
        return {
            'id': self.id,
            'name': self.name,
            'unitid': self.unitid,
            'unitname': self.getUnitName(),
            'unitprecision': self.getUnitPrecision(),
            'subcategoryid': self.subcategoryid
        }

    def __repr__(self):
        return "<StockType(id='%s', name='%s', subcategoryid='%s')>" % (self.id, self.name, self.subcategoryid)


class StockColor(Base):
    __tablename__ = 'stockcolor'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

    def __init__(self, name=None):
        """
        Initializes a new instance of StockColor class

        :param name: The name of StockColor
        :type name: str
        """
        self.name = name

    def serialize(self):
        """
        Serializes the class
        :return: The dictionary of all fields
        :rtype: dict
        """
        return {
            'id': self.id,
            'name': self.name
        }

    def __repr__(self):
        return "<StockColor(id='%s', name='%s')>" % (self.id, self.name)


class StockPackage(Base):
    __tablename__ = 'stockpackage'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

    def __init__(self, name=None):
        """
        Initializes a new instance of StockPackage class

        :param name: The name of StockPackage
        :type name: str
        """
        self.name = name

    def serialize(self):
        """
        Serializes the class
        :return: The dictionary of all fields
        :rtype: dict
        """
        return {
            'id': self.id,
            'name': self.name
        }

    def __repr__(self):
        return "<StockPackage(id='%s', name='%s')>" % (self.id, self.name)


class Corporation(Base):
    __tablename__ = 'corporation'
    id = Column(Integer, primary_key=True)
    name = Column(String(70), unique=True)

    def __init__(self, name=None):
        """
        Initializes a new instance of Corporation class

        :param name: The name of Corporation
        :type name: str
        """
        self.name = name

    def serialize(self):
        """
        Serializes the class

        :return: The dictionary of all fields
        :rtype: dict
        """
        return {
            'id': self.id,
            'name': self.name
        }

    def __repr__(self):
        return "<Corporation(id='%s', name='%s')>" % (self.id, self.name)


class StockRoom(Base):
    __tablename__ = 'stockroom'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

    def __init__(self, name=None):
        """
        Initializes a new instance of StockRoom class

        :param name: The name of StockRoom
        :type name: str
        """
        self.name = name

    def serialize(self):
        """
         Serializes the class

         :return: The dictionary of all fields
         :rtype: dict
         """
        return {
            'id': self.id,
            'name': self.name
        }

    def __repr__(self):
        return "<StockRoom(id='%s', name='%s')>" % (self.id, self.name)


class DepotStock(Base):
    __tablename__ = 'depotstock'
    id = Column(Integer, primary_key=True)
    stocktypeid = Column(Integer, ForeignKey('stocktype.id'), nullable=False)
    stockcolorid = Column(Integer, ForeignKey('stockcolor.id'), nullable=False)
    quantity = Column(String(50))
    createdate = Column(DateTime, default=datetime.utcnow())
    changedate = Column(DateTime, default=datetime.utcnow())

    def __init__(self, stocktypeid=None, stockcolorid=None, quantity=None):
        """
        Initializes a new instance of DepotStock class

        :param stocktypeid: The id of StockType of this DepotStock
        :type stocktypeid: int
        :param stockcolorid: The id of StockColor of this DepotStock
        :type stockcolorid: int
        :param quantity: The quantity of this DepotStock
        :type quantity: float
        """
        self.stocktypeid = stocktypeid
        self.stockcolorid = stockcolorid
        self.quantity = quantity
        self.createdate = turkishTimeNow()
        self.changedate = turkishTimeNow()

    def getStockTypeName(self):
        """
        Gets the name of the StockType of this DepotStock

        :return: The name of the StockType
        :rtype: str
        """
        type = dbexecutor.getStockType(self.stocktypeid)
        if type is not None:
            return type.name
        else:
            return None

    def getStockColorName(self):
        """
        Gets the name of the StockColor of this DepotStock
        :return: The name of the StockColor
        :rtype: str
        """
        color = dbexecutor.getStockColor(self.stockcolorid)
        if color is not None:
            return color.name
        else:
            return None

    def getStockUnitName(self):
        """
        Gets the name of the StockUnit of this DepotStock

        :return: The name of the StockUnit
        :rtype: str
        """
        type = dbexecutor.getStockType(self.stocktypeid)
        if type is not None:

            return type.getUnitName()
        else:
            return None

    def getQuantityText(self):
        """
        Gets the quantity text of this DepotStock
        :return: The quantity text
        :rtype: str
        """
        qtty = float(self.quantity)
        if float.is_integer(qtty):
            formattedqtty = int(qtty)
        else:
            formattedqtty = round(qtty, int(dbexecutor.getStockType(self.stocktypeid).getUnitPrecision()))
        return str(formattedqtty) + ' ' + self.getStockUnitName()

    def getFormattedQuantity(self):
        """
        Gets the formatted quantity of this StockBase

        :return: The formatted quantity of this StockBase
        :rtype: float
        """
        qtty = float(self.quantity)
        if float.is_integer(qtty):
            formattedqtty = int(qtty)
        else:
            formattedqtty = round(qtty, int(dbexecutor.getStockType(self.stocktypeid).getUnitPrecision()))
        return formattedqtty

    def getStockUnitId(self):
        """
        Gets the id of the StockUnit of this DepotStock

        :return: Id of the StockUnit
        :rtype: int
        """
        type = dbexecutor.getStockType(self.stocktypeid)
        if type is not None:

            return type.unitid
        else:
            return None

    def change(self, stocktypeid, stockcolorid, quantity):
        """
        Changes DepotStock class fields

        :param stocktypeid: The new id of StockType
        :type stocktypeid: int
        :param stockcolorid: The new id of StockColor
        :type stockcolorid: int
        :param quantity: The quantity
        :type quantity: float
        """
        self.stocktypeid = stocktypeid
        self.stockcolorid = stockcolorid
        self.quantity = quantity
        self.changedate = turkishTimeNow()

    def __repr__(self):
        return "<Stock(id='%s', stocktypeid='%s', stockcolorid='%s', quantity='%s')>" % (
            self.id, self.stocktypeid, self.stockcolorid, self.quantity)


class StockForm(Base):
    __tablename__ = 'stockform'
    id = Column(Integer, primary_key=True)
    userid = Column(Integer, ForeignKey('user.id'), nullable=False)
    corporationid = Column(Integer, ForeignKey('corporation.id'), nullable=False)
    createdate = Column(DateTime, default=datetime.utcnow())
    changedate = Column(DateTime, default=datetime.utcnow())
    recorddate = Column(DateTime, default=datetime.utcnow())

    def __init__(self, userid=None, corporationid=None, recorddate=None):
        """
        Initializes a new instance of StockForm class

        :param userid: The User id of this StockForm
        :type userid: int
        :param corporationid: The Corporation id of this StockForm
        :type corporationid: int
        :param recorddate: The record date of this StockForm
        :type recorddate: datetime
        """
        self.userid = userid
        self.corporationid = corporationid
        self.recorddate = recorddate
        self.createdate = turkishTimeNow()
        self.changedate = turkishTimeNow()

    def getCorporationName(self):
        """
        Gets the name of Corporation of this StockForm

        :return: The name of Corporation of this StockForm
        :rtype: str
        """
        return dbexecutor.getCorporation(self.corporationid).name

    def getUserName(self):
        """
        Gets the name of User of this StockForm

        :return: The name of User of this StockForm
        :rtype: str
        """
        return dbexecutor.getUser(self.userid).username

    def change(self, userid, corporationid, recorddate):
        """
        Changes StockForm class fields

        :param userid: The new id of User of this StockForm
        :type userid: int
        :param corporationid: The new id of Corporation of this StockForm
        :type corporationid: int
        :param recorddate: The new record date of this StockForm
        :type recorddate: datetime
        """
        self.userid = userid
        self.corporationid = corporationid
        self.recorddate = recorddate
        self.changedate = turkishTimeNow()

    def __repr__(self):
        return "<StockForm(id='%s', userid='%s', corporationid='%s', createdate='%s', changedate='%s', " \
               "recorddate='%s')>" % (
                   self.id, self.userid, self.corporationid, self.createdate, self.changedate, self.recorddate)


class StockBase(Base):
    __tablename__ = 'stockbase'
    id = Column(Integer, primary_key=True)
    userid = Column(Integer, ForeignKey('user.id'), nullable=False)
    stocktypeid = Column(Integer, ForeignKey('stocktype.id'), nullable=False)
    stockcolorid = Column(Integer, ForeignKey('stockcolor.id'), nullable=False)
    quantity = Column(String(50))
    createdate = Column(DateTime, default=datetime.utcnow())
    actiontype = Column(Boolean, default=True)
    entrytype = Column(Boolean, default=True)

    def __init__(self, userid=None, stocktypeid=None, stockcolorid=None, quantity=None,
                 actiontype=None, entrytype=None):
        """
        Initializes a new instance of StockBase class

        :param userid: The User id of this StockBase
        :type userid: int
        :param stocktypeid: The StockType id of this StockBase
        :type stocktypeid: int
        :param stockcolorid: The StockColor id of this StockBase
        :type stockcolorid: int
        :param quantity: The quantity of this StockBase
        :type quantity: float
        :param actiontype: The action type of this StockBase. True for incoming, False for outgoing
        :type actiontype: bool
        :param entrytype: The entry type of this StockBase. True for form entry, False for manual entry
        :type entrytype: bool
        """
        self.userid = userid
        self.stocktypeid = stocktypeid
        self.stockcolorid = stockcolorid
        self.quantity = quantity
        self.actiontype = actiontype
        self.entrytype = entrytype
        self.createdate = turkishTimeNow()

    def getUserName(self):
        """
        Gets the Username of this StockBase
        :return: The Username of this StockBase
        :rtype: str
        """
        return dbexecutor.getUser(self.userid).username

    def getStockTypeName(self):
        """
        Gets the name of the StockType of this StockBase

        :return: The name of the StockType
        :rtype: str
        """
        return dbexecutor.getStockType(self.stocktypeid).name

    def getStockColorName(self):
        """
        Gets the name of the StockColor of this StockBase

        :return: The name of the StockColor
        :rtype: str
        """
        return dbexecutor.getStockColor(self.stockcolorid).name

    def getQuantityText(self):
        """
        Gets the quantity text of this StockBase

        :return: The quantity text of this StockBase
        :rtype: str
        """
        qtty = float(self.quantity)
        if float.is_integer(qtty):
            formattedqtty = int(qtty)
        else:
            formattedqtty = round(qtty, int(dbexecutor.getStockType(self.stocktypeid).getUnitPrecision()))
        return str(formattedqtty) + ' ' + self.getStockUnitName()

    def getFormattedQuantity(self):
        """
        Gets the formatted quantity of this StockBase

        :return: The formatted quantity of this StockBase
        :rtype: float
        """
        qtty = float(self.quantity)
        if float.is_integer(qtty):
            formattedqtty = int(qtty)
        else:
            formattedqtty = round(qtty, int(dbexecutor.getStockType(self.stocktypeid).getUnitPrecision()))
        return formattedqtty

    def getStockUnitName(self):
        """
        Gets the name of the StockUnit of this StockBase

        :return: The name of the StockUnit
        :rtype: str
        """
        return dbexecutor.getStockType(self.stocktypeid).getUnitName()


class FormStockBase(Base):
    __tablename__ = 'formstockbase'
    id = Column(Integer, primary_key=True)
    stockformid = Column(Integer, ForeignKey('stockform.id'), nullable=False)
    stockbaseid = Column(Integer, ForeignKey('stockbase.id'), nullable=False)
    stockpackageid = Column(Integer, ForeignKey('stockpackage.id'), nullable=False)
    packagequantity = Column(String(50))
    note = Column(String(80))
    type = Column(Boolean, default=True)

    def __init__(self, stockformid=None, stockbaseid=None, stockpackageid=None, packagequantity=None, note=None,
                 type=None):
        """
        Initializes a new instance of FormStockBase class

        :param stockformid:  The StockForm id of this FormStockBase
        :type stockformid: int
        :param stockbaseid: The StockBase id of this FormStockBase
        :type stockbaseid: int
        :param stockpackageid: The StockPackage id of this StockBase
        :type stockpackageid: int
        :param packagequantity: The package quantity of this StockBase
        :type packagequantity: int
        :param note: The note about this StockBase
        :type note: str
        :param type: The type of the StockBase. True for incoming, False for outgoing
        :type type: bool
        """
        self.stockformid = stockformid
        self.stockbaseid = stockbaseid
        self.stockpackageid = stockpackageid
        self.packagequantity = packagequantity
        self.note = note
        self.type = type

    def getStockBase(self):
        """
        Return StockBase of this FormStockBase
        :return: The StockBase
        :rtype: StockBase
        """
        return dbexecutor.getStockBase(self.stockbaseid)

    def getStockTypeName(self):
        """
        Gets the name of the StockType of this StockBase

        :return: The name of the StockType
        :rtype: str
        """
        stockbase = dbexecutor.getStockBase(self.stockbaseid)
        return dbexecutor.getStockType(stockbase.stocktypeid).name

    def getStockColorName(self):
        """
        Gets the name of the StockColor of this StockBase

        :return: The name of the StockColor
        :rtype: str
        """
        stockbase = dbexecutor.getStockBase(self.stockbaseid)
        return dbexecutor.getStockColor(stockbase.stockcolorid).name

    def getStockPackageName(self):
        """
        Gets the name of the StockPackage of this StockBase

        :return: The name of the StockPackage
        :rtype: str
        """
        return dbexecutor.getStockPackage(self.stockpackageid).name

    def getStockUnitName(self):
        """
        Gets the name of the StockUnit of this StockBase

        :return: The name of the StockUnit
        :rtype: str
        """
        stockbase = dbexecutor.getStockBase(self.stockbaseid)
        return dbexecutor.getStockType(stockbase.stocktypeid).getUnitName()

    def getStockUnitId(self):
        """
        Gets the id of StockUnit of this StockBase

        :return: The id of StockUnit
        :rtype: int
        """
        stockbase = dbexecutor.getStockBase(self.stockbaseid)
        return dbexecutor.getStockType(stockbase.stockcolorid).unitid

    def getUnitPrecision(self):
        """
        Gets the precision of the StockUnit of this StockBase

        :return: The precision of the StockUnit
        :rtype: int
        """
        stockbase = dbexecutor.getStockBase(self.stockbaseid)
        return dbexecutor.getStockType(stockbase.stockcolorid).getUnitPrecision()

    def getQuantityText(self):
        """
        Gets the quantity text of this StockBase

        :return: The quantity text of this StockBase
        :rtype: str
        """
        stockbase = dbexecutor.getStockBase(self.stockbaseid)
        qtty = float(stockbase.quantity)
        if float.is_integer(qtty):
            formattedqtty = int(qtty)
        else:
            formattedqtty = round(qtty, int(dbexecutor.getStockType(stockbase.stocktypeid).getUnitPrecision()))
        return str(formattedqtty) + ' ' + self.getStockUnitName()

    def getPackageQuantityText(self):
        """
        Gets the package quantity text of this StockBase

        :return: The package quantity text of this StockBase
        :rtype: str
        """
        return str(self.packagequantity) + ' ' + self.getStockPackageName()


    def __repr__(self):
        return "<FormStockBase(id='%s', stockformid='%s', stockbaseid='%s', stockpackageid='%s', " \
               "packagequantity='%s', note='%s', type='%s')>" % (
                   self.id, self.stockformid, self.stockbaseid, self.stockpackageid,
                   self.packagequantity, self.note, self.type)


class IncomingStockForm(Base):
    __tablename__ = 'incomingstockform'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    stockformid = Column(Integer, ForeignKey('stockform.id'), nullable=False)

    def __init__(self, name=None, stockformid=None):
        """
        Initializes a new instance of IncomingStockForm class

        :param name: The name of this IncomingStockForm
        :type name: str
        :param stockformid: The id of StockForm of this IncomingStockForm
        :type stockformid: int
        """
        self.name = name
        self.stockformid = stockformid

    def getCorporationName(self):
        """
        Gets the name of Corporation of this IncomingStockForm
        :return: The name of Corporation of this IncomingStockForm
        :rtype: str
        """
        return dbexecutor.getStockForm(self.stockformid).getCorporationName()

    def getStockForm(self):
        """
        Return the StockForm of this IncomingStockForm
        :return: The StockForm
        :rtype: StockForm
        """
        return dbexecutor.getStockForm(self.stockformid)

    def __repr__(self):
        return "<IncomingStockForm(id='%s', name='%s', stockformid='%s')>" % (
            self.id, self.name, self.stockformid)


class OutgoingStockForm(Base):
    __tablename__ = 'outgoingstockform'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    stockformid = Column(Integer, ForeignKey('stockform.id'), nullable=False)
    stockroomid = Column(Integer, ForeignKey('stockroom.id'), nullable=False)
    shipinfo = Column(String(70))

    def __init__(self, name=None, stockformid=None, stockroomid=None, shipinfo=None):
        """
        Initializes a new instance of OutgoingStockForm class

        :param name: The name of this OutgoingStockForm
        :type name: str
        :param stockformid: The id of StockForm of this OutgoingStockForm
        :type stockformid: int
        :param stockroomid: The id of StockRoom of this OutgoingStockForm
        :type stockroomid: int
        :param shipinfo: The shipping information about this OutgoingStockForm
        :type shipinfo: str
        """
        self.name = name
        self.stockformid = stockformid
        self.stockroomid = stockroomid
        self.shipinfo = shipinfo

    def getCorporationName(self):
        """
        Gets the name of Corporation of this OutgoingStockForm

        :return: The name of Corporation of this OutgoingStockForm
        :rtype: str
        """
        return dbexecutor.getStockForm(self.stockformid).getCorporationName()

    def getStockForm(self):
        """
        Return the StockForm of this IncomingStockForm
        :return: The StockForm
        :rtype: StockForm
        """
        return dbexecutor.getStockForm(self.stockformid)

    def getStockroomName(self):
        """
        Gets the name of StockRoom of this OutgoingStockForm

        :return: The name of StockRoom of this OutgoingStockForm
        :rtype: str
        """
        return dbexecutor.getStockRoom(self.stockroomid).name

    def __repr__(self):
        return "<OutgoingStockForm(id='%s', name='%s', stockformid='%s', stockroomid='%s', shipinfo='%s')>" % (
            self.id, self.name, self.stockformid, self.stockroomid, self.shipinfo)
