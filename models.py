from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, DateTime
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash
from datetime import datetime
from config import Base
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

    def changed(self):
        """
        Changes User class fields
        """
        self.changedate = turkishTimeNow()

    def __repr__(self):
        return "<User(id='%s', username='%s', name='%s', surname='%s', isadmin='%s', password='%s', " \
               "mockpassword='%s')>" % (self.id, self.username, self.name, self.surname, self.isadmin, self.password,
                                        self.mockpassword)


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

    category = relationship("StockCategory")

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

    stockunit = relationship("StockUnit")
    subcategory = relationship("StockSubcategory")

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
            'unitname': self.stockunit.name,
            'unitprecision': self.stockunit.precision,
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

    stocktype = relationship("StockType")
    stockcolor = relationship("StockColor")

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
            formattedqtty = round(qtty, int(self.stocktype.stockunit.precision))
        return str(formattedqtty) + ' ' + self.stocktype.stockunit.name

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
            formattedqtty = round(qtty, int(self.stocktype.stockunit.precision))
        return formattedqtty

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


class StockFormDetail(Base):
    __tablename__ = 'stockformdetail'
    id = Column(Integer, primary_key=True)
    stockroomid = Column(Integer, ForeignKey('stockroom.id'), nullable=False)
    shipinfo = Column(String(70))

    stockroom = relationship("StockRoom")

    def __init__(self, stockroomid=None, shipinfo=None):
        """
        Initializes a new instance of StockFormDetail class

        :param stockroomid: The StockRoom id of this StockFormDetail
        :type stockroomid: int
        :param shipinfo: The ship info of this StockFormDetail
        :type shipinfo: str
        """
        self.stockroomid = stockroomid
        self.shipinfo = shipinfo


class StockForm(Base):
    __tablename__ = 'stockform'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    userid = Column(Integer, ForeignKey('user.id'), nullable=False)
    corporationid = Column(Integer, ForeignKey('corporation.id'), nullable=False)
    stockformdetailid = Column(Integer, ForeignKey('stockformdetail.id'))
    movetype = Column(Boolean, default=True)
    recorddate = Column(DateTime, default=datetime.utcnow())
    createdate = Column(DateTime, default=datetime.utcnow())
    changedate = Column(DateTime, default=datetime.utcnow())

    user = relationship("User")
    corporation = relationship("Corporation")
    stockformdetail = relationship("StockFormDetail")

    def __init__(self, name=None, userid=None, corporationid=None, stockformdetailid=None, movetype=None,
                 recorddate=None):
        """
        Initializes a new instance of StockForm class

        :param name: The form name of this StockForm
        :type name: str
        :param userid: The User id of this StockForm
        :type userid: int
        :param corporationid: The Corporation id of this StockForm
        :type corporationid: int
        :param stockformdetailid: The StockFormDetail id of this StockForm
        :type stockformdetailid: int
        :param movetype: The move type of this StockForm. True for incoming stock form, False for outgoing stock form
        :type movetype: bool
        :param recorddate: The record date of this StockForm
        :type recorddate: datetime
        """
        self.name = name
        self.userid = userid
        self.corporationid = corporationid
        self.stockformdetailid = stockformdetailid
        self.movetype = movetype
        self.recorddate = recorddate
        self.createdate = turkishTimeNow()
        self.changedate = turkishTimeNow()

    def change(self, name=None, userid=None, corporationid=None, stockformdetailid=None, movetype=None,
               recorddate=None):
        """
        Changes StockForm class fields

        :param name: The form name of this StockForm
        :type name: str
        :param userid: The User id of this StockForm
        :type userid: int
        :param corporationid: The Corporation id of this StockForm
        :type corporationid: int
        :param stockformdetailid: The StockFormDetail id of this StockForm
        :type stockformdetailid: int
        :param movetype: The move type of this StockForm. True for incoming stock form, False for outgoing stock form
        :type movetype: bool
        :param recorddate: The record date of this StockForm
        :type recorddate: datetime
        """
        self.name = name
        self.userid = userid
        self.corporationid = corporationid
        self.stockformdetailid = stockformdetailid
        self.movetype = movetype
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
    stockpackageid = Column(Integer, ForeignKey('stockpackage.id'))
    stockformid = Column(Integer, ForeignKey('stockform.id'))
    quantity = Column(String(50))
    packagequantity = Column(String(50))
    note = Column(String(80))
    createdate = Column(DateTime, default=datetime.utcnow())
    actiontype = Column(Boolean, default=True)
    entrytype = Column(Boolean, default=True)

    user = relationship("User")
    stocktype = relationship("StockType")
    stockcolor = relationship("StockColor")
    stockpackage = relationship("StockPackage")
    stockform = relationship("StockForm")

    def __init__(self, userid=None, stocktypeid=None, stockcolorid=None, stockpackageid=None, stockformid=None,
                 quantity=None, packagequantity=None, note=None, actiontype=None, entrytype=None):
        """
        Initializes a new instance of StockBase class

        :param userid: The User id of this StockBase
        :type userid: int
        :param stocktypeid: The StockType id of this StockBase
        :type stocktypeid: int
        :param stockcolorid: The StockColor id of this StockBase
        :type stockcolorid: int
        :param stockpackageid: The StockPackage id of this StockBase
        :type stockpackageid: int
        :param stockformid: The StockColor id of this StockForm
        :type stockformid: int
        :param quantity: The quantity of this StockBase
        :type quantity: float
        :param packagequantity: The package quantity of this StockBase
        :type packagequantity: int
        :param note: The note about this StockBase
        :type note: str
        :param actiontype: The action type of this StockBase. True for incoming, False for outgoing
        :type actiontype: bool
        :param entrytype: The entry type of this StockBase. True for form entry, False for manual entry
        :type entrytype: bool
        """
        self.userid = userid
        self.stocktypeid = stocktypeid
        self.stockcolorid = stockcolorid
        self.stockpackageid = stockpackageid
        self.stockformid = stockformid
        self.quantity = quantity
        self.packagequantity = packagequantity
        self.note = note
        self.actiontype = actiontype
        self.entrytype = entrytype
        self.createdate = turkishTimeNow()

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
            formattedqtty = round(qtty, int(self.stocktype.stockunit.precision))
        return str(formattedqtty) + ' ' + self.stocktype.stockunit.name

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
            formattedqtty = round(qtty, int(self.stocktype.stockunit.precision))
        return formattedqtty

    def getPackageQuantityText(self):
        """
        Gets the package quantity text of this StockBase

        :return: The package quantity text of this StockBase
        :rtype: str
        """
        return str(self.packagequantity) + ' ' + self.stockpackage.name