from sqlalchemy.exc import IntegrityError

from config import Base, engine, session, DbFilePath
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


def updateUser(id, username, name, surname, password, isadmin, commit=True):
    try:
        user = getUser(id)
        user.change(username, password, name, surname, password, isadmin)
        if commit:
            session.commit()
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return None


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


def getDepotAllStocks():
    """
    Gets all available DepotStocks

    :return: The list of all available DepotStocks
    :rtype: list[models.DepotStock]
    """
    stocks = session.query(models.DepotStock).all()
    return stocks


def handleDepotStockAdd(userid, stocktypeid, stockcolorid, quantity):
    return addStockBase(userid, stocktypeid, stockcolorid, quantity, True, False, True, True)


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
        if addStockBase(userid, depotstock.stocktypeid, depotstock.stockcolorid, depotstock.quantity, False, False,
                        True, True) is None:
            return None
        # And add a new incoming manual stockbase with nuw values
        stock = addStockBase(userid, stocktypeid, stockcolorid, quantity, True, False, True, True)
        return stock

    else:
        # The user only changed the quantity of the depot stock.
        stockqtty = float(depotstock.quantity)
        currentqtty = float(quantity)
        if currentqtty > stockqtty:
            # the user added some quantity, so this is incoming stockbase
            addedqtty = currentqtty - stockqtty
            stock = addStockBase(userid, stocktypeid, stockcolorid, addedqtty, True, False, True, True)
            return stock

        elif currentqtty < stockqtty:
            # the user removed some quantity, so this is outgoing stockbase
            removedqtty = stockqtty - currentqtty
            stock = addStockBase(userid, stocktypeid, stockcolorid, removedqtty, False, False, True, True)
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


def addIncomingStockForm(name, stockformid, commit=True):
    """
    Adds an IncomingStockForm

    :param name: The name of the IncomingStockForm
    :type name: str
    :param stockformid: The id of StockForm of this IncomingStockForm
    :type stockformid: int
    :param commit: If it should commit the changes
    :type commit: bool
    :return: The IncomingStockForm that is added
    :rtype: models.IncomingStockForm
    """
    form = models.IncomingStockForm(name, stockformid)
    try:
        session.add(form, True)
        if commit:
            session.commit()
        return form
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return -1


def addIncomingStockFormFromJson(user, json):
    """
    Adds an IncomingStockForm by the given json file and adds StockBases according to json

    :param user: The User that adds this IncomingStockForm, generally this is the current_user
    :type user: models.User
    :param json: The Json string that contains information about the form and stocks under the form
    :type json: dict
    :return: The operation result: 0 if add operation is successful otherwise -1
    :rtype: int
    """
    name = json['name']
    corporationid = json['corporationid']
    recorddate = json['recorddate']

    stockform = addStockForm(user.id, corporationid, recorddate, True)

    try:
        incomingform = addIncomingStockForm(name, stockform.id, False)
        for entry in json['incomingstocks']:
            stocktypeid = entry['stocktypeid']
            stockcolorid = entry['stockcolorid']
            stockpackageid = entry['stockpackageid']
            quantity = entry['quantity']
            packagequantity = entry['packagequantity']
            note = entry['stocknote']

            # Also process the stock to add or change depotstock, call with processstock=True
            if addFormStockBase(user.id, stockform.id, stocktypeid, stockcolorid, stockpackageid, quantity,
                                packagequantity, note, True, True, True) is None:
                session.rollback()
                return -1

        session.commit()
        if name == '':
            incomingform.name = 'Form ' + str(incomingform.id)
            session.commit()
        return 0
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return -1


def updateIncomingStockFormFromJson(formid, user, json):
    name = json['name']
    corporationid = json['corporationid']
    recorddate = json['recorddate']

    incomingform = getIncomingStockForm(formid)
    stockform = getStockForm(incomingform.stockformid)

    try:
        if name == '':
            incomingform.name = 'Form ' + str(incomingform.id)
        else:
            incomingform.name = name

        if updateStockForm(stockform.id, user.id, corporationid, recorddate, False) is None:
            session.rollback()
            return -1

        stockbases = getFormStockBasesByStockFormId(stockform.id)
        for stockbase in stockbases:
            # Also process the deleted stocks for DepotStock
            if deleteFormStockBase(stockbase.id, True, True) < 0:
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
            #Have to commit changes because we will have trouble if the same type of stock added
            if addFormStockBase(user.id, stockform.id, stocktypeid, stockcolorid, stockpackageid, quantity,
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


def deleteIncomingStockForm(formid, commit=True):
    incomingform = getIncomingStockForm(formid)

    try:
        session.delete(incomingform)
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


def getIncomingStockForm(formid):
    """
    Gets the IncomingStockForm by given form id

    :param formid: Id of IncomingStockForm
    :type formid: int
    :return: The desired IncomingStockForm
    :rtype: models.IncomingStockForm
    """
    form = session.query(models.IncomingStockForm).get(formid)
    return form


def getIncomingStockFormByStockFormId(stockformid):
    """
    Gets IncomingStockForm by StockForm id
    :param stockformid: StockForm id of IncomingStockForm
    :type stockformid: int
    :return: The desired IncomingStockForm
    :rtype: models.IncomingStockForm
    """
    incomingstockform = session.query(models.IncomingStockForm).filter_by(stockformid=stockformid).first()
    return incomingstockform


def getAllIncomingStockForms():
    """
    Gets all available IncomingStockForms

    :return: The list of all available IncomingStockForms
    :rtype: list[models.IncomingStockForm]
    """
    forms = session.query(models.IncomingStockForm).all()
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


def addOutgoingStockForm(name, stockformid, stockroomid, shipifo, commit=True):
    """
    Adds an OutgoingStockForm

    :param name: The name of the OutgoingStockForm
    :type name: str
    :param stockformid: The id of StockForm of this OutgoingStockForm
    :type stockformid: int
    :param stockroomid: The id of StockRoom of this OutgoingStockForm
    :type stockroomid: int
    :param shipifo: The shipping information about this OutgoingStockForm
    :type shipifo: str
    :param commit: If it should commit the changes
    :type commit: bool
    :return: The OutgoingStockForm that is added
    :rtype: models.OutgoingStockForm
    """
    form = models.OutgoingStockForm(name, stockformid, stockroomid, shipifo)
    try:
        session.add(form, True)
        if commit:
            session.commit()
        return form
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return -1


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

    stockform = addStockForm(user.id, corporationid, recorddate, True)

    try:
        outgoingform = addOutgoingStockForm(name, stockform.id, stockroomid, shipinfo, False)
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
            if addFormStockBase(user.id, stockform.id, stocktypeid, stockcolorid, stockpackageid, quantity,
                                packagequantity, note, False, True, True) is None:
                session.rollback()
                return -1

        session.commit()
        if name == '':
            outgoingform.name = 'Form ' + str(outgoingform.id)
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

    outgoingform = getOutgoingStockForm(formid)
    stockform = getStockForm(outgoingform.stockformid)

    try:
        if name == '':
            outgoingform.name = 'Form ' + str(outgoingform.id)
        else:
            outgoingform.name = name

        outgoingform.stockroomid = stockroomid
        outgoingform.shipinfo = shipinfo

        if updateStockForm(stockform.id, user.id, corporationid, recorddate, False) is None:
            session.rollback()
            return -1

        stockbases = getFormStockBasesByStockFormId(stockform.id)
        for stockbase in stockbases:
            # Also process the deleted stocks for DepotStock
            if deleteFormStockBase(stockbase.id, True, True) < 0:
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
            if addFormStockBase(user.id, stockform.id, stocktypeid, stockcolorid, stockpackageid, quantity,
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


def deleteOutgoingStockForm(formid, commit=True):
    outgoingform = getOutgoingStockForm(formid)

    try:
        session.delete(outgoingform)
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


def getOutgoingStockForm(formid):
    """
    Gets the OutgoingStockForm by given form id

    :param formid: Id of OutgoingStockForm
    :type formid: int
    :return: The desired OutgoingStockForm
    :rtype: models.OutgoingStockForm
    """
    form = session.query(models.OutgoingStockForm).get(formid)
    return form


def getOutgoingStockFormByStockFormId(stockformid):
    """
    Gets OutgoingStockForm by StockForm id
    :param stockformid: StockForm id of OutgoingStockForm
    :type stockformid: int
    :return: The desired OutgoingStockForm
    :rtype: models.OutgoingStockForm
    """
    outgoingstockform = session.query(models.OutgoingStockForm).filter_by(stockformid=stockformid).first()
    return outgoingstockform


def getAllOutgoingStockForms():
    """
    Gets all available OutgoingStockForm

    :return: The list of all available OutgoingStockForm
    :rtype: list[models.OutgoingStockForm]
    """
    forms = session.query(models.OutgoingStockForm).all()
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


def addStockForm(userid, corporationid, recorddate, commit=True):
    """
    Adds a StockForm

    :param userid: User id of the StockForm
    :type userid: int
    :param corporationid: Corporation id of StockForm
    :type corporationid: int
    :param recorddate: The date of record of the StockForm
    :type recorddate: datetime
    :return: The StockForm that is added
    :rtype: models.StockForm
    """
    if recorddate == '':
        pydatetime = util.turkishTimeNow()
    else:
        pydatetime = util.pythonDateTime(recorddate)
    stockform = models.StockForm(userid, corporationid, pydatetime)
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


def updateStockForm(id, newuserid, newcorporationid, newrecorddate, commit=True):
    """
    Updates the StockForm
    :param id: Id of the StockForm to be updated
    :type id: int
    :param newuserid: New User id of the StockForm
    :type newuserid: int
    :param newcorporationid: New Corporation id of the StockForm
    :type newcorporationid: int
    :param newrecorddate: New record date of the StockForm
    :type newrecorddate: datetime
    :param commit: If it should commit the changes
    :type commit: bool
    :return: The StockForm that is updated
    :rtype: models.StockForm
    """
    try:
        stockform = getStockForm(id)
        stockform.userid = newuserid
        stockform.corporationid = newcorporationid
        if newrecorddate == '':
            pydatetime = util.turkishTimeNow()
        else:
            pydatetime = util.pythonDateTime(newrecorddate)
        stockform.recorddate = pydatetime
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


def addFormStockBase(userid, stockformid, stocktypeid, stockcolorid, stockpackageid, quantity, packagequantity, note,
                     type, commit=True, processstock=True):
    """
    Adds a FormStockBase

    :param stockformid: StockForm id of the FormStockBase
    :type stockformid: int
    :param stocktypeid: StockType id of the FormStockBase
    :type stocktypeid: int
    :param stockcolorid: StockColor id of the FormStockBase
    :type stockcolorid: int
    :param stockpackageid: FormStockPackage id of the StockBase
    :type stockpackageid: int
    :param quantity: Quantity of the FormStockBase
    :type quantity: float
    :param packagequantity: StockPackage quantity id of the FormStockBase
    :type packagequantity: int
    :param note: Note about FormStockBase
    :type note: str
    :param type: The type of the FormStockBase. True for incoming, False for outgoing
    :type type: bool
    :param commit: If it should commit the changes
    :type commit: bool
    :param processstock: If it should process the FormStockBase that is added for DepotStock
    :type processstock: bool
    :return: The FormStockBase that is added
    :rtype: models.FormStockBase
    """
    try:
        # Have to commit to get the id
        stockbase = addStockBase(userid, stocktypeid, stockcolorid, quantity, type, True, True, processstock)

        if stockbase is None:
            session.rollback()
            return None

        formstockbase = models.FormStockBase(stockformid, stockbase.id, stockpackageid, packagequantity, note, type)

        session.add(formstockbase, True)

        if commit:
            session.commit()
        return stockbase
    except Exception as e:
        session.rollback()
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return None


def getFormStockBase(id):
    """
    Gets StockBase by given id

    :param id: Id of the StockBase
    :type id: int
    :return: The desired StockBase
    :rtype: models.FormStockBase
    """

    try:
        stockbase = session.query(models.FormStockBase).get(id)
        return stockbase
    except Exception as e:
        if hasattr(e, 'message'):
            print('Exception: ' + e.message)
        else:
            print(e)
        return None


def getFormStockBasesByStockFormId(stockformid):
    """
    Gets StockBases by given StockForm id

    :param stockformid: Id of the StockForm of StockBases
    :type stockformid: int
    :return: All StockBases whose StockForm id is give
    :rtype: list[models.FormStockBase]
    """
    stockbases = session.query(models.FormStockBase).filter(models.FormStockBase.stockformid == stockformid).all()
    return stockbases


def getFormStockBasesCountByStockFormId(stockformid):
    """
    Gets StockBases by given StockForm id

    :param stockformid: Id of the StockForm of StockBases
    :type stockformid: int
    :return: All StockBases whose StockForm id is give
    :rtype: list[models.FormStockBase]
    """
    query = session.query(models.FormStockBase).filter(models.FormStockBase.stockformid == stockformid)
    query = query.with_entities(func.count())
    return query.scalar()


def getFormStockBasesByStockBaseId(stockbaseid):
    """
    Gets StockBase by given StockBase id

    :param stockformid: Id of the StockForm of StockBase
    :type stockformid: int
    :return: FormStockBases whose StockForm id is give
    :rtype: models.FormStockBase
    """
    formstockbase = session.query(models.FormStockBase).filter_by(stockbaseid=stockbaseid).first()
    return formstockbase


def deleteFormStockBase(id, commit=True, processstock=True):
    """
    Deletes the StockBase

    :param id: The of the StockBase to be deleted
    :type id: int
    :param commit: If it should commit the changes
    :type commit: bool
    :return: The operation result: 0 if delete is successful, otherwise -1
    :rtype: int
    """
    try:
        formstockbase = getFormStockBase(id)
        stockbase = getStockBase(formstockbase.stockbaseid)

        if deleteStockBase(stockbase.id, commit, processstock) < 0:
            session.rollback()
            return -1

        session.delete(formstockbase)
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


def addStockBase(userid, stocktypeid, stockcolorid, quantity, actiontype, entrytype, commit=True, processstock=True):
    """
    Adds a FormStockBase

    :param userid: User id of the StockBase
    :type userid: int
    :param stocktypeid: StockType id of the StockBase
    :type stocktypeid: int
    :param stockcolorid: StockColor id of the StockBase
    :type stockcolorid: int
    :param quantity: Quantity of the StockBase
    :type quantity: float
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
    base = models.StockBase(userid, stocktypeid, stockcolorid, quantity, actiontype, entrytype)
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
    Gets al lavailable StockBases

    :param id: Id of StockBase
    :type id: int
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


def commit():
    """
    Commits database changes
    """
    session.commit()


def rollback():
    session.rollback()
