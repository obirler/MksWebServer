from sqlalchemy.exc import IntegrityError

from config import Base, engine, session, DbFilePath, DbFileFolder
import models
import os
import util
from sqlalchemy import and_, func


def init_db():
    """
    Initializes the database
    """
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    Base.metadata.create_all(bind=engine)


def firstTime():
    """
    Checks whether it is the first launch

    :return: True if it is first time, otherwise false
    :rtype: bool
    """
    if not os.path.exists(DbFileFolder):
        os.mkdir(DbFileFolder)

    if not os.path.exists(DbFilePath):
        init_db()
        return True
    else:
        return False


def addUser(username, name, surname, password, isadmin, commit=True):
    """
    Adds a user

    :param str username: Username of the user
    :param str name: Real name of the user
    :param str surname: Surname of the user
    :param str password: Password of the user
    :param bool isadmin: Whether user admin or not
    :param commit: If it should commit the changes
    :type commit: bool
    :return: 0 if the user added successfully, -1 otherwise
    :rtype: int
    :raises Exception: if the user can't be added to database
    """
    user = models.User(username, password, name, surname, isadmin)
    try:
        session.add(user, True)
        if commit:
            session.commit()
        return 0
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return -1


def getUser(id):
    """
    Gets the IncomingStockForm by given form id

    :param int id: User id
    :return: User with given id
    :rtype: models.User
    """
    user = session.query(models.User).get(id)
    return user


def getUserByUserName(username):
    try:
        user = session.query(models.User).filter_by(username=username).first()
        return user
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return None


def getAllUsers():
    """
    Gets all available Users

    :return: The list of all available Users
    :rtype: list[models.User]
    """
    users = session.query(models.User).all()
    return users


def getAllAdminIds():
    """
    Gets all available ids of admin Users

    :return: The list of all available ids of admin Users
    :rtype: list[int]
    """
    adminids = session.query(models.User.id).filter(models.User.isadmin == True).all()
    return adminids


def addDepotStock(typeid, colorid, quantity, commit=True):
    """
    Adds a DepotStock

    :param typeid: The id of StockType of this DepotStock
    :type typeid: int
    :param colorid: The id of StockColor of this DepotStock
    :type colorid: int
    :param quantity: The quantity of this DepotStock
    :type quantity: float
    :param commit: If it should commit the changes
    :type commit: bool
    :return: The DepotStock that is added
    :rtype: models.DepotStock
    """
    stock = models.DepotStock(stocktypeid=typeid, stockcolorid=colorid, quantity=quantity)
    try:
        session.add(stock, True)
        if commit:
            session.commit()
        return stock
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return None


def getDepotStock(id):
    """
    Gets DepotStock by given id
    :param id: The id of DepotStock
    :type id: int
    :return: The desired DepotStock
    :rtype: models.DepotStock
    """
    stock = session.query(models.DepotStock).get(id)
    return stock


def deleteDepotStock(id, commit=True):
    """
    Deletes DepotStock by id

    :param id: The id of DepotStock to be deleted
    :type id: int
    :param commit: If it should commit the changes
    :type commit: bool
    :return: The operation result: 0 if delete operation is successful otherwise -1
    :rtype: int
    """
    try:
        stock = session.query(models.DepotStock).get(id)
        session.delete(stock)
        if commit:
            session.commit()
        return 0
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return -1


def getDepotStockByTypeAndColor(typeid, colorid):
    """
    Gets DepotStock by given StockType and StockColor

    :param typeid: Id of StockType of this DepotStock
    :type typeid: int
    :param colorid: Id of StockColor of this DepotStock
    :type colorid: int
    :return: The desired DepotStock
    :rtype: models.DepotStock
    """
    stock = session.query(models.DepotStock).filter(and_(models.DepotStock.stocktypeid == typeid,
                                                         models.DepotStock.stockcolorid == colorid)).first()
    return stock


def getAllDepotStockIds():
    """
    Gets all available ids of DepotStocks

    :return: The list of all available ids of DepotStock
    :rtype: list[int]
    """
    ids = session.query(models.DepotStock.id).all()
    return ids


def getDepotAllStocks():
    """
    Gets all available DepotStocks

    :return: The list of all available DepotStocks
    :rtype: list[models.DepotStock]
    """
    stocks = session.query(models.DepotStock).all()
    return stocks


def handleDepotStockAdd(userid, stocktypeid, stockcolorid, quantity):
    return addStockBase(userid, stocktypeid, stockcolorid, None, None, quantity, None, None, True, False, True, True)


def handleDepotStockUpdate(id, userid, stocktypeid, stockcolorid, quantity):
    """
    Fake updates StockBase to sync changes to DepotStock

    :param id:
    :type id:
    :param userid:
    :type userid:
    :param stocktypeid:
    :type stocktypeid:
    :param stockcolorid:
    :type stockcolorid:
    :param quantity:
    :type quantity:
    :return: The StockBase
    :rtype: models.StockBase
    """
    depotstock = getDepotStock(id)

    if depotstock.stocktypeid != stocktypeid or depotstock.stockcolorid != stockcolorid:
        # The user changed the depot stock. So add a manual outgoing stockbase to delete old stock
        if addStockBase(userid, depotstock.stocktypeid, depotstock.stockcolorid, None, None, depotstock.quantity, None,
                        None, False, False, True, True) is None:
            return None
        # And add a new incoming manual stockbase with new values
        stock = addStockBase(userid, stocktypeid, stockcolorid, None, None, quantity, None, None, True, False, True,
                             True)
        return stock

    else:
        # The user only changed the quantity of the depot stock.
        stockqtty = float(depotstock.quantity)
        currentqtty = float(quantity)
        if currentqtty > stockqtty:
            # the user added some quantity, so this is incoming stockbase
            addedqtty = currentqtty - stockqtty
            stock = addStockBase(userid, stocktypeid, stockcolorid, None, None, addedqtty, None, None, True, False,
                                 True, True)
            return stock

        elif currentqtty < stockqtty:
            # the user removed some quantity, so this is outgoing stockbase
            removedqtty = stockqtty - currentqtty
            stock = addStockBase(userid, stocktypeid, stockcolorid, None, None, removedqtty, None, None, False, False,
                                 True, True)
            return stock


def handleDepotStockDelete(id, userid):
    # add an outcoming stockbase with the equal amount to set the depotstock zero
    depotstock = getDepotStock(id)
    try:
        if addStockBase(userid, depotstock.stocktypeid, depotstock.stockcolorid, depotstock.quantity, False, False,
                        True, True) is None:
            return -1
        return 0
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return -1


def addIncomingStockFormFromJson(user, json):
    """
    Adds an incoming StockForm by the given json file and adds StockBases according to json

    :param user: The User that adds this incoming StockForm, generally this is the current_user
    :type user: models.User
    :param json: The Json string that contains information about the form and stocks under the form
    :type json: dict
    :return: The operation result: 0 if add operation is successful otherwise -1
    :rtype: int
    """
    name = json['name']
    corporationid = json['corporationid']
    recorddate = json['recorddate']

    # There is no stock detail in incoming StockForm. So, we will give None parameter
    incomingstockform = addStockForm(name, user.id, corporationid, None, True, recorddate, True)

    try:
        for entry in json['incomingstocks']:
            stocktypeid = entry['stocktypeid']
            stockcolorid = entry['stockcolorid']
            stockpackageid = entry['stockpackageid']
            quantity = entry['quantity']
            packagequantity = entry['packagequantity']
            note = entry['stocknote']

            # Also process the stock to add or change depotstock, call with processstock=True
            if addStockBase(user.id, stocktypeid, stockcolorid, stockpackageid, incomingstockform.id, quantity,
                            packagequantity, note, True, True, True) is None:
                session.rollback()
                deleteStockForm(incomingstockform.id)
                return -1

        session.commit()
        if name == '':
            incomingstockform.name = 'Form ' + str(incomingstockform.id)
            session.commit()
        return 0
    except Exception as e:
        session.rollback()
        deleteStockForm(incomingstockform.id)
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return -1


def updateIncomingStockFormFromJson(formid, user, json):
    name = json['name']
    corporationid = json['corporationid']
    recorddate = json['recorddate']

    incomingform = getStockForm(formid)

    try:
        if name == '':
            incomingform.name = 'Form ' + str(incomingform.id)
        else:
            incomingform.name = name

        if updateStockForm(incomingform.id, user.id, name, corporationid, None, True, recorddate, False) is None:
            session.rollback()
            return -1

        stockbases = getStockBasesFromStockFormId(incomingform.id)

        for stockbase in stockbases:
            # Also process the deleted stocks for DepotStock
            if deleteStockBase(stockbase.id, True, True) < 0:
                session.rollback()
                return -1

        for entry in json['incomingstocks']:
            stocktypeid = entry['stocktypeid']
            stockcolorid = entry['stockcolorid']
            stockpackageid = entry['stockpackageid']
            quantity = entry['quantity']
            packagequantity = entry['packagequantity']
            note = entry['stocknote']

            # Also process the stock to add or change depotstock, call with processstock=True
            # Have to commit changes because we will have trouble if the same type of stock added
            if addStockBase(user.id, stocktypeid, stockcolorid, stockpackageid, incomingform.id, quantity,
                                packagequantity, note, True, True, True) is None:
                session.rollback()
                return -1

        session.commit()
        return 0

    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return -1


def getAllIncomingStockForms():
    """
    Gets all available incoming StockForms

    :return: The list of all available incoming StockForms
    :rtype: list[models.StockForm]
    """
    forms = session.query(models.StockForm).filter(models.StockForm.movetype == True).all()
    return forms


def processaddincomingstock(incomingstock, commit=True):
    """
    Processes the StockBase that was added

    :param incomingstock: The incoming StockBase that comes with incoming StockBase
    :type incomingstock: models.StockBase
    :param commit: If it should commit the changes
    :type commit: bool
    :return: The operation result: 0 if successful, -1 otherwise
    :rtype: int
    """
    depotstock = getDepotStockByTypeAndColor(incomingstock.stocktypeid, incomingstock.stockcolorid)
    if depotstock:
        stockqtty = float(depotstock.quantity)
        incominqtty = float(incomingstock.quantity)
        newquantity = stockqtty + incominqtty
        if float.is_integer(newquantity):
            depotstock.quantity = int(newquantity)
        else:
            depotstock.quantity = newquantity
        return 0
    else:
        if addDepotStock(incomingstock.stocktypeid, incomingstock.stockcolorid, incomingstock.quantity, commit) is None:
            return -1
        return 0


def processdeleteincomingstock(incomingstock, commit=True):
    """
    Processes the StockBase that was deleted

    :param incomingstock: The incoming StockBase
    :type incomingstock: models.StockBase
    """

    depotstock = getDepotStockByTypeAndColor(incomingstock.stocktypeid, incomingstock.stockcolorid)

    if depotstock:
        stockqtty = float(depotstock.quantity)
        incominqtty = float(incomingstock.quantity)
        newquantity = stockqtty - incominqtty
        if newquantity < 0:
            return -2
        elif newquantity == 0:
            if deleteDepotStock(depotstock.id, commit) < 0:
                return -1
            return 0
        else:
            if float.is_integer(newquantity):
                depotstock.quantity = int(newquantity)
            else:
                depotstock.quantity = newquantity
            return 0
    return 1


def addOutgoingStockFormFromJson(user, json):
    """
    Adds an OutgoingStockForm by the given json file and adds StockBases according to json

    :param user: The User that adds this IncomingStockForm, generally this is the current_user
    :type user: models.User
    :param json: The Json string that contains information about the form and stocks under the form
    :type json: dict
    :return: The operation result: 0 if add operation is successful otherwise -1
    :rtype: int
    """
    name = json['name']
    corporationid = json['corporationid']
    stockroomid = json['stockroomid']
    shipinfo = json['shipinfo']
    recorddate = json['recorddate']

    detail = addStockFormDetail(stockroomid, shipinfo, True)

    outgoingstockform = addStockForm(name, user.id, corporationid, detail.id, False, recorddate, True)

    try:
        for entry in json['outgoingstocks']:
            stocktypeid = entry['stocktypeid']
            stockcolorid = entry['stockcolorid']
            stockpackageid = entry['stockpackageid']
            quantity = entry['quantity']
            packagequantity = entry['packagequantity']
            note = entry['stocknote']

            # Also process the stock to add or change depotstock, call with processstock=True
            # TODO Don't just swallow the internal error codes. Implement a tuple mechanism to return multiple values
            # One of them the return class and the other is error code
            if addStockBase(user.id, stocktypeid, stockcolorid, stockpackageid, outgoingstockform.id, quantity,
                                packagequantity, note, False, True, True) is None:
                session.rollback()
                deleteStockForm(outgoingstockform.id)
                return -1

        session.commit()
        if name == '':
            outgoingstockform.name = 'Form ' + str(outgoingstockform.id)
            session.commit()
        return 0
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return -1


def updateOutgoingStockFormFromJson(formid, user, json):
    name = json['name']
    corporationid = json['corporationid']
    recorddate = json['recorddate']
    stockroomid = json['stockroomid']
    shipinfo = json['shipinfo']

    outgoingform = getStockForm(formid)

    try:
        if name == '':
            outgoingform.name = 'Form ' + str(outgoingform.id)
        else:
            outgoingform.name = name

        outgoingform.stockformdetail.stockroomid = stockroomid
        outgoingform.stockformdetail.shipinfo = shipinfo

        if updateStockForm(outgoingform.id, user.id, name, corporationid, outgoingform.stockformdetail.id, False,
                           recorddate, False) is None:
            session.rollback()
            return -1

        stockbases = getStockBasesFromStockFormId(outgoingform.id)

        for stockbase in stockbases:
            # Also process the deleted stocks for DepotStock
            if deleteStockBase(stockbase.id, True, True) < 0:
                session.rollback()
                return -1

        for entry in json['outgoingstocks']:
            stocktypeid = entry['stocktypeid']
            stockcolorid = entry['stockcolorid']
            stockpackageid = entry['stockpackageid']
            quantity = entry['quantity']
            packagequantity = entry['packagequantity']
            note = entry['stocknote']

            # Also process the stock to add or change depotstock, call with processstock=True
            if addStockBase(user.id, stocktypeid, stockcolorid, stockpackageid, outgoingform.id, quantity,
                                packagequantity, note, False, True, True) is None:
                session.rollback()
                return -1

        session.commit()
        return 0

    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return -1


def getAllOutgoingStockForms():
    """
    Gets all available outgoing StockForms

    :return: The list of all available outgoing StockForms
    :rtype: list[models.StockForm]
    """
    forms = session.query(models.StockForm).filter(models.StockForm.movetype == False).all()
    return forms


def processaddoutgoingstock(outgoingstock, commit=True):
    """
    Processes the StockBase that was added

    :param outgoingstock: The outgoing StockBase that comes with outgoingStockForm
    :type outgoingstock: models.StockBase
    :return: The operation result: 0 if process is successful, -2
    :rtype: int
    """
    stock = getDepotStockByTypeAndColor(outgoingstock.stocktypeid, outgoingstock.stockcolorid)
    if stock:
        stockqtty = float(stock.quantity)
        outcominqtty = float(outgoingstock.quantity)
        newquantity = stockqtty - outcominqtty
        if newquantity < 0:
            return -2
        elif newquantity == 0:
            if deleteDepotStock(stock.id, commit) < 0:
                return -1
            return 0
        else:
            if float.is_integer(newquantity):
                stock.quantity = int(newquantity)
            else:
                stock.quantity = newquantity
            return 0
    else:
        return -3


def processdeleteoutgoingstock(outgoingstock, commit=True):
    """
    Processes the StockBase that was added

    :param outgoingstock: The outgoing StockBase that comes with outgoingStockForm
    :type outgoingstock: models.StockBase
    :return: The operation result: 0 if process is successful, -1 if there is general error, -2 if stock is not enough
    :rtype: int
    """
    stock = getDepotStockByTypeAndColor(outgoingstock.stocktypeid, outgoingstock.stockcolorid)
    if stock:
        stockqtty = float(stock.quantity)
        outcominqtty = float(outgoingstock.quantity)
        newquantity = stockqtty + outcominqtty
        if newquantity < 0:
            return -2
        elif newquantity == 0:
            if deleteDepotStock(stock.id, commit) < 0:
                return -1
            return 0
        else:
            stock.quantity = newquantity
            return 0
    else:
        return -3


def addStockUnit(name, precision, commit=True):
    """
    Adds a StockUnit

    :param name: The name of the StockUnit
    :type name: str
    :param precision: The precision ıf the StockUnit
    :type precision: int
    :param commit: If it should commit the changes
    :type commit: bool
    :return: The StockUnit that is added
    :rtype: models.StockUnit
    """
    unit = models.StockUnit(name, precision)
    try:
        session.add(unit, True)
        if commit:
            session.commit()
        return unit
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return None


def getStockUnit(id):
    """
    Gets StockUnit by given id

    :param id: Id of the StockUnit
    :type id: int
    :return: The desired StockUnit
    :rtype: models.StockUnit
    """
    try:
        unit = session.query(models.StockUnit).get(id)
        return unit
    except Exception as e:
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return None


def updateStockUnit(id, newname, newprecision, commit=True):
    """
    Updates the StockUnit

    :param id: Id of the StockUnit to be updated
    :type id: int
    :param newname: New name of the StockUnit
    :type newname: str
    :param newprecision: New precision of the StockUnit
    :type newprecision: int
    :param commit: If it should commit the changes
    :type commit: bool
    :return: The StockUnit that is updated
    :rtype: models.StockUnit
    """
    try:
        unit = getStockUnit(id)
        unit.name = newname
        unit.precision = newprecision
        if commit:
            session.commit()
        return unit
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return None


def deleteStockUnit(id, commit=True):
    """
    Deletes the StockUnit

    :param id: The of the StockUnit to be deleted
    :type id: int
    :param commit: If it should commit the changes
    :type commit: bool
    :return: The operation result: 0 if delete is successful, otherwise -1
    :rtype: int
    """
    try:
        unit = session.query(models.StockUnit).get(id)
        session.delete(unit)
        if commit:
            session.commit()
        return 0
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return -1


def getAllStockUnitIds():
    """
    Gets all available ids of StockUnits

    :return: The list of all available ids of StockUnit
    :rtype: list[int]
    """
    ids = session.query(models.StockUnit.id).all()
    return ids


def getAllStockUnits():
    """
    Gets all available StockUnits
    :return: The list of all available StockUnits
    :rtype: list[models.StockUnit]
    """
    units = session.query(models.StockUnit).all()
    return units


def addStockType(name, unitid, subcategoryid, commit=True):
    """
    Adds a StockType

    :param name: The name of the StockType
    :type name: str
    :param unitid: The unit id of the StockType
    :type unitid: int
    :param subcategoryid: The subcategory id of the StockType
    :type subcategoryid: int
    :param commit: If it should commit the changes
    :type commit: bool
    :return: The StockType that is added
    :rtype: models.StockType
    """
    type = models.StockType(name, unitid, subcategoryid)
    try:
        session.add(type, True)
        if commit:
            session.commit()
        return type
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return None


def getStockType(id):
    """
    Gets StockType by given id

    :param id: Id of the StockType
    :type id: int
    :return: The desired StockType
    :rtype: models.StockType
    """
    try:
        type = session.query(models.StockType).get(id)
        return type
    except Exception as e:
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return None


def updateStockType(id, newname, newunitid, newsubcategoryid, commit=True):
    """
    Updates the StockType

    :param id: Id of the StockType to be updated
    :type id: int
    :param newname: New name of the StockType
    :type newname: str
    :param newunitid: New unit id of the StockType
    :type newunitid: int
    :param newsubcategoryid: New subcategory id of the StockType
    :type newsubcategoryid: int
    :param commit: If it should commit the changes
    :type commit: bool
    :return: The StockType that is updated
    :rtype: models.StockType
    """
    try:
        stocktype = getStockType(id)
        stocktype.name = newname
        stocktype.unitid = newunitid
        stocktype.subcategoryid = newsubcategoryid
        if commit:
            session.commit()
        return stocktype
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return None


def deleteStockType(id, commit=True):
    """
    Deletes the StockType

    :param id: The of the StockType to be deleted
    :type id: int
    :param commit: If it should commit the changes
    :type commit: bool
    :return: The operation result: 0 if delete is successful, otherwise -1
    :rtype: int
    """
    try:
        type = session.query(models.StockType).get(id)
        session.delete(type)
        if commit:
            session.commit()
        return 0
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return -1


def getAllStockTypes():
    """
    Gets all available StockTypes

    :return: The list of all available StockType
    :rtype: list[models.StockType]
    """
    types = session.query(models.StockType).all()
    return types


def getAllStockTypeIds():
    """
    Gets all available ids of StockType

    :return: The list of all available ids of StockType
    :rtype: list[int]
    """
    ids = session.query(models.StockType.id).all()
    return ids


def getAllStockTypesByStockSubcategory(categoryid):
    """
    Gets all available StockTypes by subcategory

    :param categoryid: The subcategory id
    :type categoryid: int
    :return: The list of desired StockTypes
    :rtype: list[models.StockType]
    """
    types = session.query(models.StockType).filter(models.StockType.subcategoryid == categoryid).all()
    return types


def addStockColor(name, commit=True):
    """
    Adds a StockColor

    :param name: The name of the StockColor
    :type name: str
    :param commit: If it should commit the changes
    :type commit: bool
    :return: The StockColor that is added
    :rtype: models.StockColor
    """
    color = models.StockColor(name)
    try:
        session.add(color, True)
        if commit:
            session.commit()
        return color
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return None


def getStockColor(id):
    """
    Gets StockColor by given id

    :param id: Id of the StockColor
    :type id: int
    :return: The desired StockColor
    :rtype: models.StockColor
    """
    try:
        color = session.query(models.StockColor).get(id)
        return color
    except Exception as e:
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return None


def updateStockColor(id, newname, commit=True):
    """
    Updates the StockColor
    :param id:Id of the StockColor to be updated
    :type id: int
    :param newname: New name of the StockColor
    :type newname: str
    :param commit: If it should commit the changes
    :type commit: bool
    :return: The StockColor that is updated
    :rtype: models.StockColor
    """
    try:
        stockcolor = getStockColor(id)
        stockcolor.name = newname
        if commit:
            session.commit()
        return stockcolor
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return None


def deleteStockColor(id, commit=True):
    """
    Deletes the StockColor

    :param id: The of the StockColor to be deleted
    :type id: int
    :param commit: If it should commit the changes
    :type commit: bool
    :return: The operation result: 0 if delete is successful, otherwise -1
    :rtype: int
    """
    try:
        color = session.query(models.StockColor).get(id)
        session.delete(color)
        if commit:
            session.commit()
        return 0
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return -1


def getAllStockColors():
    """
    Gets all available StockColors

    :return: The list of all available StockColor
    :rtype: list[models.StockColor]
    """
    colors = session.query(models.StockColor).all()
    return colors


def getAllStockColorIds():
    """
    Gets all available ids of StockColor

    :return: The list of all available ids of StockColor
    :rtype: list[int]
    """
    ids = session.query(models.StockColor.id).all()
    return ids


def addStockPackage(name, commit=True):
    """
    Adds a StockPackage

    :param name: The name of the StockPackage
    :type name: str
    :param commit: If it should commit the changes
    :type commit: bool
    :return: The StockPackage that is added
    :rtype: models.StockPackage
    """
    package = models.StockPackage(name)
    try:
        session.add(package, True)
        if commit:
            session.commit()
        return package
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return None


def getStockPackage(id):
    """
    Gets StockPackage by given id

    :param id: Id of the StockPackage
    :type id: int
    :return: The desired StockPackage
    :rtype: models.StockPackage
    """
    try:
        package = session.query(models.StockPackage).get(id)
        return package
    except Exception as e:
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return None


def updateStockPackage(id, newname, commit=True):
    """
    Updates the StockPackage
    :param id:Id of the StockPackage to be updated
    :type id: int
    :param newname: New name of the StockPackage
    :type newname: str
    :param commit: If it should commit the changes
    :type commit: bool
    :return: The StockPackage that is updated
    :rtype: models.StockPackage
    """
    try:
        stockpackage = getStockPackage(id)
        stockpackage.name = newname
        if commit:
            session.commit()
        return stockpackage
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return None


def deleteStockPackage(id, commit=True):
    """
    Deletes the StockPackage

    :param id: The of the StockPackage to be deleted
    :type id: int
    :param commit: If it should commit the changes
    :type commit: bool
    :return: The operation result: 0 if delete is successful, otherwise -1
    :rtype: int
    """
    try:
        stockpackage = session.query(models.StockPackage).get(id)
        session.delete(stockpackage)
        if commit:
            session.commit()
        return 0
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return -1


def getAllStockPackages():
    """
    Gets all available StockPackages

    :return: The list of all available StockPackage
    :rtype: list[models.StockPackage]
    """
    packages = session.query(models.StockPackage).all()
    return packages


def getAllStockPackageIds():
    """
    Gets all available ids of StockPackage

    :return: The list of all available ids of StockPackage
    :rtype: list[int]
    """
    ids = session.query(models.StockPackage.id).all()
    return ids


def addCorporation(name, commit=True):
    """
    Adds a Corporation

    :param name: The name of the Corporation
    :type name: str
    :param commit: If it should commit the changes
    :type commit: bool
    :return: The Corporation that is added
    :rtype: models.Corporation
    """
    corporation = models.Corporation(name)
    try:
        session.add(corporation, True)
        if commit:
            session.commit()
        return corporation
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return None


def getCorporation(id):
    """
    Gets Corporation by given id

    :param id: Id of the Corporation
    :type id: int
    :return: The desired Corporation
    :rtype: models.Corporation
    """
    try:
        corporation = session.query(models.Corporation).get(id)
        return corporation
    except Exception as e:
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return None


def updateCorporation(id, newname, commit=True):
    """
    Updates the Corporation
    :param id:Id of the Corporation to be updated
    :type id: int
    :param newname: New name of the Corporation
    :type newname: str
    :param commit: If it should commit the changes
    :type commit: bool
    :return: The Corporation that is updated
    :rtype: models.Corporation
    """
    try:
        corporation = getCorporation(id)
        corporation.name = newname
        if commit:
            session.commit()
        return corporation
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return None


def deleteCorporation(id, commit=True):
    """
    Deletes the Corporation

    :param id: The of the Corporation to be deleted
    :type id: int
    :param commit: If it should commit the changes
    :type commit: bool
    :return: The operation result: 0 if delete is successful, otherwise -1
    :rtype: int
    """
    try:
        corporation = session.query(models.Corporation).get(id)
        session.delete(corporation)
        if commit:
            session.commit()
        return 0
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return -1


def getAllCorporations():
    """
    Gets all available Corporations

    :return: The list of all available Corporation
    :rtype: list[models.Corporation]
    """
    corporations = session.query(models.Corporation).all()
    return corporations


def getAllCorporationIds():
    """
    Gets all available ids of Corporation

    :return: The list of all available ids of Corporation
    :rtype: list[int]
    """
    ids = session.query(models.Corporation.id).all()
    return ids


def addStockCategory(name, commit=True):
    """
    Adds a StockCategory

    :param name: The name of the StockCategory
    :type name: str
    :param commit: If it should commit the changes
    :type commit: bool
    :return: The StockCategory that is added
    :rtype: models.StockCategory
    """
    category = models.StockCategory(name)
    try:
        session.add(category, True)
        if commit:
            session.commit()
        return category
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return None


def getStockCategory(id):
    """
    Gets StockCategory by given id

    :param id: Id of the StockCategory
    :type id: int
    :return: The desired StockCategory
    :rtype: models.StockCategory
    """
    try:
        category = session.query(models.StockCategory).get(id)
        return category
    except Exception as e:
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return None


def updateStockCategory(id, newname, commit=True):
    """
    Updates the StockCategory
    :param id:Id of the StockCategory to be updated
    :type id: int
    :param newname: New name of the StockCategory
    :type newname: str
    :param commit: If it should commit the changes
    :type commit: bool
    :return: The StockCategory that is updated
    :rtype: models.StockCategory
    """
    try:
        category = getStockCategory(id)
        category.name = newname
        if commit:
            session.commit()
        return category
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return None


def deleteStockCategory(id, commit=True):
    """
    Deletes the StockCategory

    :param id: The of the StockCategory to be deleted
    :type id: int
    :param commit: If it should commit the changes
    :type commit: bool
    :return: The operation result: 0 if delete is successful, otherwise -1
    :rtype: int
    """
    try:
        category = getStockCategory(id)
        session.delete(category)
        session.flush()
        if commit:
            session.commit()
        return 0

    except IntegrityError as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return -1

    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return -1


def getAllStockCategory():
    """
    Gets all available StockCategorys

    :return: The list of all available StockCategory
    :rtype: list[models.StockCategory]
    """
    categories = session.query(models.StockCategory).all()
    return categories


def addStockSubcategory(name, categoryid, commit=True):
    """
    Adds a StockSubcategory

    :param name: The name of the StockSubcategory
    :type name: str
    :param name: The StockCategory id of the StockSubcategory
    :type name: str
    :param commit: If it should commit the changes
    :type commit: bool
    :return: The StockSubcategory that is added
    :rtype: models.StockSubcategory
    """
    category = models.StockSubcategory(name, categoryid)
    try:
        session.add(category, True)
        if commit:
            session.commit()
        return category
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return None


def getStockSubcategory(id):
    """
    Gets StockSubcategory by given id

    :param id: Id of the StockSubcategory
    :type id: int
    :return: The desired StockSubcategory
    :rtype: models.StockSubcategory
    """
    try:
        category = session.query(models.StockSubcategory).get(id)
        return category
    except Exception as e:
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return None


def updateStockSubcategory(id, newname, newcategoryid, commit=True):
    """
    Updates the StockSubcategory
    :param id:Id of the StockSubcategory to be updated
    :type id: int
    :param newname: New name of the StockSubcategory
    :type newname: str
    :param newname: The new StockCategory id of the StockSubcategory
    :type newname: int
    :param commit: If it should commit the changes
    :type commit: bool
    :return: The StockSubcategory that is updated
    :rtype: models.StockSubcategory
    """
    try:
        category = getStockSubcategory(id)
        category.name = newname
        category.categoryid = newcategoryid
        if commit:
            session.commit()
        return category
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return None


def deleteStockSubcategory(id, commit=True):
    """
    Deletes the StockSubcategory

    :param id: The of the StockSubcategory to be deleted
    :type id: int
    :param commit: If it should commit the changes
    :type commit: bool
    :return: The operation result: 0 if delete is successful, otherwise -1
    :rtype: int
    """
    try:
        category = getStockSubcategory(id)
        session.delete(category)
        if commit:
            session.commit()
        return 0
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return -1


def getAllStockSubcategory():
    """
    Gets all available StockSubcategorys

    :return: The list of all available StockSubcategory
    :rtype: list[models.StockSubcategory]
    """
    categories = session.query(models.StockSubcategory).all()
    return categories


def getAllStockSubcategoryByStockCategory(categoryid):
    """
    Gets all available StockSubcategorys under given StockCategory

    :param categoryid: The is of StockCategory
    :type categoryid: int
    :return: The list of all available StockSubcategorys under StockCategory
    :rtype: list[models.StockCategory]
    """
    categories = session.query(models.StockSubcategory).filter(models.StockSubcategory.categoryid == categoryid).all()
    return categories


def addStockForm(name, userid, corporationid, stockformdetailid, movetype, recorddate, commit=True):
    """
    Adds a StockForm

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
    :return: The StockForm that is added
    :rtype: models.StockForm
    """
    if recorddate == '':
        pydatetime = util.turkishTimeNow()
    else:
        pydatetime = util.pythonDateTime(recorddate)
    stockform = models.StockForm(name, userid, corporationid, stockformdetailid, movetype, pydatetime)
    try:
        session.add(stockform, True)
        if commit:
            session.commit()
        return stockform
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return None


def getStockForm(id):
    """
    Gets StockForm by given id

    :param id: Id of the StockForm
    :type id: int
    :return: The desired StockForm
    :rtype: models.StockForm
    """

    try:
        stockform = session.query(models.StockForm).get(id)
        return stockform
    except Exception as e:
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return None


def updateStockForm(id, name, userid, corporationid, stockformdetailid, movetype, recorddate, commit=True):
    """
    Updates the StockForm
    :param id: Id of the StockForm to be updated
    :type id: int
    :param name: The new form name of this StockForm
    :type name: str
    :param userid: The new User id of this StockForm
    :type userid: int
    :param corporationid: The new Corporation id of this StockForm
    :type corporationid: int
    :param stockformdetailid: The new StockFormDetail id of this StockForm
    :type stockformdetailid: int
    :param movetype: The new move type of this StockForm. True for incoming stock form, False for outgoing stock form
    :type movetype: bool
    :param recorddate: The new record date of this StockForm
    :type recorddate: datetime
    :return: The StockForm that is updated
    :rtype: models.StockForm
    """
    try:
        stockform = getStockForm(id)
        if recorddate == '':
            pydatetime = util.turkishTimeNow()
        else:
            pydatetime = util.pythonDateTime(recorddate)

        stockform.change(name, userid, corporationid, stockformdetailid, movetype, pydatetime)
        if commit:
            session.commit()
        return stockform
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return None


def deleteStockForm(id, commit=True):
    """
    Deletes the StockForm

    :param id: The of the StockForm to be deleted
    :type id: int
    :param commit: If it should commit the changes
    :type commit: bool
    :return: The operation result: 0 if delete is successful, otherwise -1
    :rtype: int
    """
    try:
        unit = session.query(models.StockForm).get(id)
        session.delete(unit)
        if commit:
            session.commit()
        return 0
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return -1


def addStockBase(userid, stocktypeid, stockcolorid, stockpackageid, stockformid, quantity, packagequantity, note,
                 actiontype, entrytype, commit=True, processstock=True):
    """
    Adds a FormStockBase

    :param userid: User id of the StockBase
    :type userid: int
    :param stocktypeid: StockType id of the StockBase
    :type stocktypeid: int
    :param stockcolorid: StockColor id of the StockBase
    :type stockcolorid: int
    :param stockpackageid: StockPackage id of the StockBase
    :type stockpackageid: int
    :param stockformid: StockForm id of the StockBase
    :type stockformid: int
    :param quantity: Quantity of the StockBase
    :type quantity: float
    :param packagequantity: The package quantity of this StockBase
    :type packagequantity: int
    :param note: The note about this StockBase
    :type note: str
    :param actiontype: The action type of the StockBase. True for incoming, False for outgoing
    :type actiontype: bool
    :param entrytype: The entry type of the StockBase. True for form entry, False for manual entry
    :type entrytype: bool
    :param commit: If it should commit the changes
    :type commit: bool
    :param processstock: If it should process the StockBase that is added for DepotStock
    :type processstock: bool
    :return: The StockBase that is added
    :rtype: models.StockBase
    """
    base = models.StockBase(userid, stocktypeid, stockcolorid, stockpackageid, stockformid, quantity, packagequantity,
                            note, actiontype, entrytype)
    try:
        session.add(base, True)

        if commit:
            session.commit()

        if processstock:
            if actiontype:
                processaddincomingstock(base, commit)
            else:
                processaddoutgoingstock(base, commit)

        return base
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return None


def getStockBase(id):
    """
    Gets StockBase by id

    :param id: Id of StockBase
    :type id: int
    :return: The desired StockBase
    :rtype: models.StockBase
    """
    try:
        base = session.query(models.StockBase).get(id)
        return base
    except Exception as e:
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return None


def getAllStockBases():
    """
    Gets all available StockBases

    :return: The list of all available StockBases
    :rtype: list[models.StockBase]
    """
    try:
        base = session.query(models.StockBase).all()
        return base
    except Exception as e:
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return None


def getStockBasesFromStockFormId(stockformid):
    """
    Gets all available StockBases under given StockForm

    :param stockformid: The is of StockForm
    :type stockformid: int
    :return: The list of all available StockBases under StockForm
    :rtype: list[models.StockBase]
    """
    stockbases = session.query(models.StockBase).filter(models.StockBase.stockformid == stockformid).all()
    return stockbases


def deleteStockBase(id, commit=True, processstock=True):
    base = getStockBase(id)
    actiontype = base.actiontype

    try:
        if processstock:
            if actiontype:
                if processdeleteincomingstock(base, commit) < 0:
                    return -1
            else:
                if processdeleteoutgoingstock(base, commit) < 0:
                    return -1
        session.delete(base)
        return 0

    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return -1


def getStockBasesCountByStockFormId(stockformid):
    """
    Gets StockBases count by given StockForm id

    :param stockformid: Id of the StockForm of StockBases
    :type stockformid: int
    :return: The count of all StockBases whose StockForm id is given
    :rtype: int
    """
    query = session.query(models.StockBase).filter(models.StockBase.stockformid == stockformid)
    query = query.with_entities(func.count())
    return query.scalar()


def addStockRoom(name, commit=True):
    """
    Adds a StockRoom

    :param name: The name of the StockRoom
    :type name: str
    :param commit: If it should commit the changes
    :type commit: bool
    :return: The StockRoom that is added
    :rtype: models.StockRoom
    """
    room = models.StockRoom(name)
    try:
        session.add(room, True)
        if commit:
            session.commit()
        return room
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return None


def getStockRoom(id):
    """
    Gets StockRoom by given id

    :param id: Id of the StockRoom
    :type id: int
    :return: The desired StockRoom
    :rtype: models.StockRoom
    """
    try:
        room = session.query(models.StockRoom).get(id)
        return room
    except Exception as e:
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return None


def updateStockRoom(id, newname, commit=True):
    """
    Updates the StockRoom
    :param id:Id of the StockRoom to be updated
    :type id: int
    :param newname: New name of the StockRoom
    :type newname: str
    :param commit: If it should commit the changes
    :type commit: bool
    :return: The StockRoom that is updated
    :rtype: models.StockRoom
    """
    try:
        stockroom = getStockRoom(id)
        stockroom.name = newname
        if commit:
            session.commit()
        return stockroom
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return None


def deleteStockRoom(id, commit=True):
    """
    Deletes the StockRoom

    :param id: The of the StockRoom to be deleted
    :type id: int
    :param commit: If it should commit the changes
    :type commit: bool
    :return: The operation result: 0 if delete is successful, otherwise -1
    :rtype: int
    """
    try:
        stockroom = session.query(models.StockColor).get(id)
        session.delete(stockroom)
        if commit:
            session.commit()
        return 0
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return -1


def getAllStockRooms():
    """
    Gets all available StockRooms

    :return: The list of all available StockRoom
    :rtype: list[models.StockRoom]
    """
    stockrooms = session.query(models.StockRoom).all()
    return stockrooms


def getAllStockRoomIds():
    """
    Gets all available ids of StockRoom

    :return: The list of all available ids of StockRoom
    :rtype: list[int]
    """
    ids = session.query(models.StockRoom.id).all()
    return ids


def addStockFormDetail(stockroomid, shipinfo, commit):
    """
    Adds a StockFormDetail

    :param stockroomid: The id of StockRoom of this StockFormDetail
    :type stockroomid: id
    :param shipinfo: The ship info opf this StockFormDetail
    :type shipinfo: str
    :param commit: If it should commit the changes
    :type commit: bool
    :return: The StockFormDetail that is added
    :rtype: models.StockFormDetail
    """
    detail = models.StockFormDetail(stockroomid, shipinfo)
    try:
        session.add(detail, True)
        if commit:
            session.commit()
        return detail
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return None


def updateStockFormDetail(id, stockroomid, shipinfo, commit=True):
    """
    Updates the StockFormDetail

    :param id:Id of the StockFormDetail to be updated
    :type id: int
    :param stockroomid: New id of StockRoom of this StockFormDetail
    :type stockroomid: int
    :param shipinfo: New ship info of this StockFormDetail
    :type shipinfo: str
    :param commit: If it should commit the changes
    :type commit: bool
    :return: The StockFormDetail that is updated
    :rtype: models.StockFormDetail
    """
    try:
        detail = getStockFormDetail(id)
        detail.stockroomid = stockroomid
        detail.shipinfo = shipinfo
        if commit:
            session.commit()
        return detail
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return None


def getStockFormDetail(id):
    """
    Gets StockFormDetail by given id

    :param id: Id of the StockFormDetail
    :type id: int
    :return: The desired StockFormDetail
    :rtype: models.StockFormDetail
    """
    try:
        detail = session.query(models.StockFormDetail).get(id)
        return detail
    except Exception as e:
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return None


def commit():
    """
    Commits database changes
    """
    session.commit()


def rollback():
    session.rollback()
