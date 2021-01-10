from flask import request, render_template, jsonify, send_file
from flask_login import login_required, current_user

import dbexecutor
import util
from config import app, AppRoot
from doctemplates.IncomingStockFormTemplate import IncomingStockFormTemplate
from doctemplates.OutgoingStockFormTemplate import OutgoingStockFormTemplate
from doctemplates.FormStockMovesTemplate import FormStockMovesTemplate


@app.route('/incomingstockforms', methods=['GET'])
@login_required
def incomingstockforms():
    if not current_user.isadmin:
        return render_template('autherror.html')

    if request.method == 'GET':
        forms = []
        incomingforms = dbexecutor.getAllIncomingStockForms()
        for incomingform in incomingforms:
            stockbasescount = dbexecutor.getStockBasesCountByStockFormId(incomingform.id)
            form = {}
            form['formid'] = incomingform.id
            form['name'] = incomingform.name
            form['userid'] = incomingform.userid
            form['username'] = incomingform.user.username
            form['corporationid'] = incomingform.corporationid
            form['corporationname'] = incomingform.corporation.name
            form['incomingstocksquantity'] = stockbasescount
            form['recorddate'] = incomingform.recorddate
            forms.append(form)

        return render_template("incomingstockforms.html", forms=forms)


@app.route('/addincomingstockform', methods=['GET', 'POST'])
@login_required
def addincomingstockform():
    if not current_user.isadmin:
        return render_template('autherror.html')

    if request.method == 'GET':
        stockcategories = dbexecutor.getAllStockCategory()
        stockcolors = dbexecutor.getAllStockColors()
        stockunits = dbexecutor.getAllStockUnits()
        stockpackages = dbexecutor.getAllStockPackages()
        corporations = dbexecutor.getAllCorporations()
        return render_template("addincomingstockform.html", stockcategories=stockcategories, stockcolors=stockcolors,
                               stockunits=stockunits, stockpackages=stockpackages, corporations=corporations)

    elif request.method == 'POST':
        req_data = request.get_json()
        if dbexecutor.addIncomingStockFormFromJson(current_user, req_data) != 0:
            return jsonify(responsecode=-1, message="Hata! Depo giriş verisi eklenemedi")

        return jsonify(responsecode=0, heading="Tebrikler!", message="Sisteme başarıyla depo girişi yaptınız.",
                       postmessage="Dilerseniz başka bir depo girişi daha yapabilirsiniz.")


@app.route('/editincomingstockform/<int:formid>', methods=['GET', 'PATCH', 'DELETE'])
@login_required
def editincomingstockform(formid):
    if not current_user.isadmin:
        return render_template('autherror.html')

    if request.method == 'GET':
        incomingform = dbexecutor.getStockForm(formid)
        form = {}
        form['name'] = incomingform.name
        form['formid'] = incomingform.id
        form['corporationid'] = incomingform.corporationid
        form['recorddate'] = util.htmldateTime(incomingform.recorddate)

        stockbases = dbexecutor.getStockBasesFromStockFormId(incomingform.id)
        incomingstocks = []

        i=0
        for stockbase in stockbases:
            entry = {}
            entry['stocktypename'] = stockbase.stocktype.name
            entry['stocktypeid'] = stockbase.stocktypeid
            entry['stockcolorname'] = stockbase.stockcolor.name
            entry['stockcolorid'] = stockbase.stockcolorid
            entry['stockunitid'] = stockbase.stocktype.stockunit.id
            entry['quantity'] = stockbase.quantity
            entry['quantitytext'] = stockbase.getQuantityText()
            entry['stockpackageid'] = stockbase.stockpackageid
            entry['packagequantity'] = stockbase.packagequantity
            entry['packagetext'] = stockbase.getPackageQuantityText()
            entry['note'] = stockbase.note
            entry['entryid'] = str(i)
            i += 1
            incomingstocks.append(entry)

        form['incomingstocks'] = incomingstocks

        stockcategories = dbexecutor.getAllStockCategory()
        stockcolors = dbexecutor.getAllStockColors()
        stockunits = dbexecutor.getAllStockUnits()
        stockpackages = dbexecutor.getAllStockPackages()
        corporations = dbexecutor.getAllCorporations()
        return render_template("editincomingstockform.html", form=form, stockcategories=stockcategories,
                               stockcolors=stockcolors, stockunits=stockunits, stockpackages=stockpackages,
                               corporations=corporations)

    elif request.method == 'PATCH':
        req_data = request.get_json()
        user = dbexecutor.getUser(current_user.id)
        if dbexecutor.updateIncomingStockFormFromJson(formid, user, req_data) != 0:
            return jsonify(responsecode=-1, message="Hata! Depo giriş verisi güncellenemedi")

        return jsonify(responsecode=0, heading="Tebrikler!", message="Depo giriş verisini başarıyla güncellediniz.",
                       postmessage="Şimdi depo giriş verileri sayfasına yönlendirileceksiniz")

    elif request.method == 'DELETE':
        incomingform = dbexecutor.getStockForm(formid)
        stockbases = dbexecutor.getStockBasesFromStockFormId(incomingform.id)

        for stockbase in stockbases:
            if dbexecutor.deleteStockBase(stockbase.id, False, True) < 0:
                dbexecutor.rollback()
                return jsonify(responsecode=-1, heading="Hata!",
                               message="Depo giriş verisi silinemedi")

        if dbexecutor.deleteStockForm(incomingform.id, False) < 0:
            dbexecutor.rollback()
            return jsonify(responsecode=-1, heading="Hata!",
                           message="Depo giriş verisi silinemedi")

        dbexecutor.commit()
        return jsonify(responsecode=0, heading="Tebrikler!", message="Depo giriş verisini başarıyla sildiniz.",
                       postmessage="Şimdi depo giriş verileri sayfasına yönlendirileceksiniz")


@app.route('/downloadincomingstockform/<int:formid>', methods=['GET'])
@login_required
def downloadincomingstockform(formid):
    if not current_user.isadmin:
        return render_template('autherror.html')

    form = dbexecutor.getStockForm(formid)
    formtemplate = IncomingStockFormTemplate(form, 18)
    pdfpath = formtemplate.generatePdf()
    print('sending pdf file in a blank tab')
    return send_file(pdfpath, mimetype="application/pdf", attachment_filename='form.pdf')


@app.route('/downloadincomingstockform/<int:formid>/<int:row>', methods=['GET'])
@login_required
def downloadincomingstockformadvanced(formid, row):
    if not current_user.isadmin:
        return render_template('autherror.html')

    form = dbexecutor.getStockForm(formid)
    formtemplate = IncomingStockFormTemplate(form, row)
    pdfpath = formtemplate.generatePdf()
    print('sending pdf file in a blank tab')
    return send_file(pdfpath, mimetype="application/pdf", attachment_filename='form.pdf')


@app.route('/copyincomingstockforminfo/<int:formid>', methods=['GET'])
@login_required
def copyincomingstockforminfo(formid):
    if not current_user.isadmin:
        return render_template('autherror.html')

    incomingform = dbexecutor.getStockForm(formid)
    stockbases = dbexecutor.getStockBasesFromStockFormId(incomingform.id)
    str = "Depo Girişi:\n"
    for stockbase in stockbases:
        str += "-" + stockbase.getQuantityText() + " " + stockbase.stocktype.name + " " + \
               stockbase.stockcolor.name + "\n"
    str += "\n"
    str += incomingform.corporation.name
    return str.upper()


@app.route('/addoutgoingstockform', methods=['GET', 'POST'])
@login_required
def addoutgoingstockform():
    if not current_user.isadmin:
        return render_template('autherror.html')

    if request.method == 'GET':
        stockcategories = dbexecutor.getAllStockCategory()
        stockcolors = dbexecutor.getAllStockColors()
        stockunits = dbexecutor.getAllStockUnits()
        stockpackages = dbexecutor.getAllStockPackages()
        corporations = dbexecutor.getAllCorporations()
        stockrooms = dbexecutor.getAllStockRooms()
        return render_template("addoutgoingstockform.html", stockcategories=stockcategories, stockcolors=stockcolors,
                               stockunits=stockunits, stockpackages=stockpackages, corporations=corporations,
                               stockrooms=stockrooms)

    elif request.method == 'POST':
        req_data = request.get_json()
        user = dbexecutor.getUser(current_user.id)
        result = dbexecutor.addOutgoingStockFormFromJson(user, req_data)
        if result != 0:
            if result == -1:
                return jsonify(responsecode=-1, message="Hata! Depo giriş verisi eklenemedi")
            elif result == -2:
                return jsonify(responsecode=-2, message="Hata! Depoda sevkiyat yapacak kadar malzeme yok!")
            elif result == -3:
                return jsonify(responsecode=-3, message="Hata! Depoda sevkiyat yapacak türden malzeme yok!")

        return jsonify(responsecode=0, heading="Tebrikler!", message="Sisteme başarıyla depo girişi yaptınız.",
                       postmessage="Dilerseniz başka bir depo girişi daha yapabilirsiniz.")


@app.route('/editoutgoingstockform/<int:formid>', methods=['GET', 'PATCH', 'DELETE'])
@login_required
def editoutgoingstockform(formid):
    if not current_user.isadmin:
        return render_template('autherror.html')

    if request.method == 'GET':
        outgoingform = dbexecutor.getStockForm(formid)
        form = {}
        form['name'] = outgoingform.name
        form['formid'] = outgoingform.id
        form['stockroomid'] = outgoingform.stockformdetail.stockroom.id
        form['shipinfo'] = outgoingform.stockformdetail.shipinfo
        form['corporationid'] = outgoingform.corporationid
        form['recorddate'] = util.htmldateTime(outgoingform.recorddate)

        stockbases = dbexecutor.getStockBasesFromStockFormId(outgoingform.id)
        outgoingstocks = []

        i = 0
        for stockbase in stockbases:
            entry = {}
            entry['stocktypename'] = stockbase.stocktype.name
            entry['stocktypeid'] = stockbase.stocktypeid
            entry['stockcolorname'] = stockbase.stockcolor.name
            entry['stockcolorid'] = stockbase.stockcolorid
            entry['stockunitid'] = stockbase.stocktype.stockunit.id
            entry['quantity'] = stockbase.quantity
            entry['quantitytext'] = stockbase.getQuantityText()
            entry['stockpackageid'] = stockbase.stockpackageid
            entry['packagequantity'] = stockbase.packagequantity
            entry['packagetext'] = stockbase.getPackageQuantityText()
            entry['note'] = stockbase.note
            entry['entryid'] = str(i)
            i += 1
            outgoingstocks.append(entry)

        form['outgoingstocks'] = outgoingstocks

        stockcategories = dbexecutor.getAllStockCategory()
        stockcolors = dbexecutor.getAllStockColors()
        stockunits = dbexecutor.getAllStockUnits()
        stockpackages = dbexecutor.getAllStockPackages()
        corporations = dbexecutor.getAllCorporations()
        stockrooms = dbexecutor.getAllStockRooms()
        return render_template("editoutgoingstockform.html", form=form, stockcategories=stockcategories,
                               stockcolors=stockcolors, stockunits=stockunits, stockpackages=stockpackages,
                               corporations=corporations, stockrooms=stockrooms)

    elif request.method == 'PATCH':
        req_data = request.get_json()
        user = dbexecutor.getUser(current_user.id)
        if dbexecutor.updateOutgoingStockFormFromJson(formid, user, req_data) != 0:
            return jsonify(responsecode=-1, message="Hata! Ürün sevkiyat verisi güncellenemedi")

        return jsonify(responsecode=0, heading="Tebrikler!", message="Ürün sevkiyat verisini başarıyla güncellediniz.",
                       postmessage="Şimdi ürün sevkiyat verileri sayfasına yönlendirileceksiniz")

    elif request.method == 'DELETE':
        outgoingform = dbexecutor.getStockForm(formid)
        stockbases = dbexecutor.getStockBasesFromStockFormId(outgoingform.id)

        for stockbase in stockbases:
            if dbexecutor.deleteStockBase(stockbase.id, False, True) < 0:
                dbexecutor.rollback()
                return jsonify(responsecode=-1, heading="Hata!",
                               message="Ürün sevkiyat verisi silinemedi")

        if dbexecutor.deleteStockForm(outgoingform.id, False) < 0:
            dbexecutor.rollback()
            return jsonify(responsecode=-1, heading="Hata!",
                           message="Ürün sevkiyat verisi silinemedi")

        dbexecutor.commit()
        return jsonify(responsecode=0, heading="Tebrikler!", message="Ürün sevkiyat verisini başarıyla sildiniz.",
                       postmessage="Şimdi ürün sevkiyat verileri sayfasına yönlendirileceksiniz")


@app.route('/downloadoutgoingstockform/<int:formid>', methods=['GET'])
@login_required
def downloadoutgoingstockform(formid):
    if not current_user.isadmin:
        return render_template('autherror.html')

    form = dbexecutor.getStockForm(formid)
    formtemplate = OutgoingStockFormTemplate(form, 18)
    pdfpath = formtemplate.generatePdf()
    print('sending pdf file in a blank tab')
    return send_file(pdfpath, mimetype="application/pdf", attachment_filename='form.pdf')


@app.route('/downloadoutgoingstockform/<int:formid>/<int:row>', methods=['GET'])
@login_required
def downloadoutgoingstockformadvanced(formid, row):
    if not current_user.isadmin:
        return render_template('autherror.html')

    form = dbexecutor.getStockForm(formid)
    formtemplate = OutgoingStockFormTemplate(form, row)
    pdfpath = formtemplate.generatePdf()
    print('sending pdf file in a blank tab')
    return send_file(pdfpath, mimetype="application/pdf", attachment_filename='form.pdf')


@app.route('/copyoutgoingstockforminfo/<int:formid>', methods=['GET'])
@login_required
def copyoutgoingstockforminfo(formid):
    if not current_user.isadmin:
        return render_template('autherror.html')

    outgoingform = dbexecutor.getStockForm(formid)
    stockbases = dbexecutor.getStockBasesFromStockFormId(outgoingform.id)
    str = "Ürün Sevkiyatı:\n"
    for stockbase in stockbases:
        str += "-" + stockbase.getQuantityText() + " " + stockbase.stocktype.name + " " + \
               stockbase.stockcolor.name + "\n"
    str += "\n"
    str += outgoingform.corporation.name + "\n"
    str += outgoingform.stockformdetail.shipinfo
    return str.upper()


@app.route('/outgoingstockforms', methods=['GET'])
@login_required
def outgoingstockforms():
    if not current_user.isadmin:
        return render_template('autherror.html')

    if request.method == 'GET':
        forms = []
        outgoingforms = dbexecutor.getAllOutgoingStockForms()
        for outgoingform in outgoingforms:
            stockbasescount = dbexecutor.getStockBasesCountByStockFormId(outgoingform.id)
            form = {}
            form['formid'] = outgoingform.id
            form['name'] = outgoingform.name
            form['userid'] = outgoingform.userid
            form['username'] = outgoingform.user.username
            form['corporationid'] = outgoingform.corporationid
            form['corporationname'] = outgoingform.corporation.name
            form['outgoingstocksquantity'] = stockbasescount
            form['stockroom'] = outgoingform.stockformdetail.stockroom.name
            form['shipinfo'] = outgoingform.stockformdetail.shipinfo
            form['recorddate'] = outgoingform.recorddate
            forms.append(form)

        return render_template("outgoingstockforms.html", forms=forms)


@app.route('/stockcategory', methods=['POST', 'DELETE', 'PATCH'])
@login_required
def stockCategory():
    if not current_user.isadmin:
        return render_template('autherror.html')

    if request.method == 'POST':
        reqjson = request.get_json()
        name = reqjson['name']
        stockcategory = dbexecutor.addStockCategory(name)
        if stockcategory is None:
            return jsonify(responsecode=-1, message="Hata! Malzeme kategorisi verisi eklenemedi")
        return jsonify(responsecode=0, stockcategory=stockcategory.serialize())

    elif request.method == 'PATCH':
        reqjson = request.get_json()
        id = reqjson['id']
        newname = reqjson['name']
        stockcategory = dbexecutor.updateStockCategory(id, newname)
        if stockcategory is None:
            return jsonify(responsecode=-1, message="Hata! Malzeme kategorisi verisi değiştirilemedi")
        return jsonify(responsecode=0, stockcategory=stockcategory.serialize())

    elif request.method == 'DELETE':
        reqjson = request.get_json()
        id = reqjson['id']
        result = dbexecutor.deleteStockCategory(id)
        if result < 0:
            return jsonify(responsecode=-1, message="Hata! Malzeme kategorisi verisi silinemedi")
        return jsonify(responsecode=0, id=id)


@app.route('/stocksubcategory', methods=['POST', 'DELETE', 'PATCH'])
@login_required
def stockSubcategory():
    if not current_user.isadmin:
        return render_template('autherror.html')

    if request.method == 'POST':
        reqjson = request.get_json()
        name = reqjson['name']
        categoryid = reqjson['categoryid']
        stocksubcategory = dbexecutor.addStockSubcategory(name, categoryid)
        if stocksubcategory is None:
            return jsonify(responsecode=-1, message="Hata! Malzeme alt kategorisi verisi eklenemedi")
        return jsonify(responsecode=0, stocksubcategory=stocksubcategory.serialize())

    elif request.method == 'PATCH':
        reqjson = request.get_json()
        id = reqjson['id']
        newname = reqjson['name']
        newcategoryid = reqjson['categoryid']
        stocksubcategory = dbexecutor.updateStockSubcategory(id, newname, newcategoryid)
        if stocksubcategory is None:
            return jsonify(responsecode=-1, message="Hata! Malzeme alt kategorisi verisi değiştirilemedi")
        return jsonify(responsecode=0, stocksubcategory=stocksubcategory.serialize())

    elif request.method == 'DELETE':
        reqjson = request.get_json()
        id = reqjson['id']
        result = dbexecutor.deleteStockSubcategory(id)
        if result < 0:
            return jsonify(responsecode=-1, message="Hata! Malzeme alt kategorisi verisi silinemedi")
        return jsonify(responsecode=0, id=id)


@app.route('/stocktype', methods=['POST', 'DELETE', 'PATCH'])
@login_required
def stockType():
    if not current_user.isadmin:
        return render_template('autherror.html')

    if request.method == 'POST':
        reqjson = request.get_json()
        name = reqjson['name']
        unitid = reqjson['unitid']
        subcategoryid = reqjson['subcategoryid']
        stocktype = dbexecutor.addStockType(name, unitid, subcategoryid)
        if stocktype is None:
            return jsonify(responsecode=-1, message="Hata! Malzeme cinsi verisi eklenemedi")
        return jsonify(responsecode=0, stocktype=stocktype.serialize())

    elif request.method == 'PATCH':
        reqjson = request.get_json()
        id = reqjson['id']
        newname = reqjson['name']
        newunitid = reqjson['unitid']
        newsubcategoryid = reqjson['subcategoryid']
        stocktype = dbexecutor.updateStockType(id, newname, newunitid, newsubcategoryid)
        if stocktype is None:
            return jsonify(responsecode=-1, message="Hata! Malzeme cinsi verisi değiştirilemedi")
        return jsonify(responsecode=0, stocktype=stocktype.serialize())

    elif request.method == 'DELETE':
        reqjson = request.get_json()
        id = reqjson['id']
        result = dbexecutor.deleteStockType(id)
        if result < 0:
            return jsonify(responsecode=-1, message="Hata! Malzeme cinsi verisi silinemedi")
        return jsonify(responsecode=0, id=id)


@app.route('/stockcolor', methods=['POST', 'DELETE', 'PATCH'])
@login_required
def stockColor():
    if not current_user.isadmin:
        return render_template('autherror.html')

    if request.method == 'POST':
        reqjson = request.get_json()
        name = reqjson['name']
        stockcolor = dbexecutor.addStockColor(name)
        if stockcolor is None:
            return jsonify(responsecode=-1, message="Hata! Malzeme rengi verisi eklenemedi")
        return jsonify(responsecode=0, stockcolor=stockcolor.serialize())

    elif request.method == 'PATCH':
        reqjson = request.get_json()
        id = reqjson['id']
        newname = reqjson['name']
        stockcolor = dbexecutor.updateStockColor(id, newname)
        if stockcolor is None:
            return jsonify(responsecode=-1, message="Hata! Malzeme rengi verisi değiştirilemedi")
        return jsonify(responsecode=0, stockcolor=stockcolor.serialize())

    elif request.method == 'DELETE':
        reqjson = request.get_json()
        id = reqjson['id']
        result = dbexecutor.deleteStockColor(id)
        if result < 0:
            return jsonify(responsecode=-1, message="Hata! Malzeme rengi verisi silinemedi")
        return jsonify(responsecode=0, id=id)


@app.route('/stockpackage', methods=['POST', 'DELETE', 'PATCH'])
@login_required
def stockPackage():
    if not current_user.isadmin:
        return render_template('autherror.html')

    if request.method == 'POST':
        reqjson = request.get_json()
        name = reqjson['name']
        stockpackage = dbexecutor.addStockPackage(name)
        if stockpackage is None:
            return jsonify(responsecode=-1, message="Hata! Ambalaj verisi eklenemedi")
        return jsonify(responsecode=0, stockpackage=stockpackage.serialize())

    elif request.method == 'PATCH':
        reqjson = request.get_json()
        id = reqjson['id']
        newname = reqjson['name']
        stockpackage = dbexecutor.updateStockPackage(id, newname)
        if stockpackage is None:
            return jsonify(responsecode=-1, message="Hata! Ambalaj verisi değiştirilemedi")
        return jsonify(responsecode=0, stockpackage=stockpackage.serialize())

    elif request.method == 'DELETE':
        reqjson = request.get_json()
        id = reqjson['id']
        result = dbexecutor.deleteStockPackage(id)
        if result < 0:
            return jsonify(responsecode=-1, message="Hata! Ambalaj verisi silinemedi")
        return jsonify(responsecode=0, id=id)


@app.route('/corporation', methods=['POST', 'DELETE', 'PATCH'])
@login_required
def corporation():
    if not current_user.isadmin:
        return render_template('autherror.html')

    if request.method == 'POST':
        reqjson = request.get_json()
        name = reqjson['name']
        corporation = dbexecutor.addCorporation(name)
        if corporation is None:
            return jsonify(responsecode=-1, message="Hata! Şirket verisi eklenemedi")
        return jsonify(responsecode=0, corporation=corporation.serialize())

    elif request.method == 'PATCH':
        reqjson = request.get_json()
        id = reqjson['id']
        newname = reqjson['name']
        corporation = dbexecutor.updateCorporation(id, newname)
        if corporation is None:
            return jsonify(responsecode=-1, message="Hata! Şirket verisi değiştirilemedi")
        return jsonify(responsecode=0, corporation=corporation.serialize())

    elif request.method == 'DELETE':
        reqjson = request.get_json()
        id = reqjson['id']
        result = dbexecutor.deleteCorporation(id)
        if result < 0:
            return jsonify(responsecode=-1, message="Hata! Şirket verisi silinemedi")
        return jsonify(responsecode=0, id=id)


@app.route('/stockunit', methods=['POST', 'DELETE', 'PATCH'])
@login_required
def stockUnit():
    if not current_user.isadmin:
        return render_template('autherror.html')

    if request.method == 'POST':
        reqjson = request.get_json()
        name = reqjson['name']
        precision = reqjson['precision']
        stockunit = dbexecutor.addStockUnit(name, precision)
        if stockunit is None:
            return jsonify(responsecode=-1, message="Hata! Malzeme birimi verisi eklenemedi")
        return jsonify(responsecode=0, stockunit=stockunit.serialize())

    elif request.method == 'PATCH':
        reqjson = request.get_json()
        id = reqjson['id']
        newname = reqjson['name']
        newprecision = reqjson['precision']
        stockunit = dbexecutor.updateStockUnit(id, newname, newprecision)
        if stockunit is None:
            return jsonify(responsecode=-1, message="Hata! Malzeme birimi verisi değiştirilemedi")
        return jsonify(responsecode=0, stockunit=stockunit.serialize())

    elif request.method == 'DELETE':
        reqjson = request.get_json()
        id = reqjson['id']
        result = dbexecutor.deleteStockUnit(id)
        if result < 0:
            return jsonify(responsecode=-1, message="Hata! Malzeme birimi verisi silinemedi")
        return jsonify(responsecode=0, id=id)


@app.route('/stocks', methods=['GET', 'POST', 'PATCH', 'DELETE'])
@login_required
def stocks():
    if not current_user.isadmin:
        return render_template('autherror.html')

    if request.method == 'GET':
        stocks = dbexecutor.getDepotAllStocks()
        stockcategories = dbexecutor.getAllStockCategory()
        stockcolors = dbexecutor.getAllStockColors()
        stockunits = dbexecutor.getAllStockUnits()
        return render_template("stocks.html", stocks=stocks, stockcategories=stockcategories, stockcolors=stockcolors,
                               stockunits=stockunits)

    elif request.method == 'POST':
        reqjson = request.get_json()
        user = dbexecutor.getUser(current_user.id)
        stocktypeid = reqjson['stocktypeid']
        stockcolorid = reqjson['stockcolorid']
        quantity = reqjson['stockquantity']
        # Add incoming manual stock
        if dbexecutor.handleDepotStockAdd(user.id, stocktypeid, stockcolorid, quantity) is None:
            return jsonify(responsecode=-1, message="Hata! Malzeme girişi eklenemedi")

        return jsonify(responsecode=0, heading="Tebrikler!", message="Başarıyla depoya malzeme girişi yaptınız.",
                       postmessage="Şimdi sayfa yenilenecektir.")

    elif request.method == 'PATCH':
        reqjson = request.get_json()
        user = dbexecutor.getUser(current_user.id)
        id = reqjson['id']
        stocktypeid = reqjson['stocktypeid']
        stockcolorid = reqjson['stockcolorid']
        quantity = reqjson['stockquantity']

        if dbexecutor.handleDepotStockUpdate(id, user.id, stocktypeid, stockcolorid, quantity) is None:
            return jsonify(responsecode=-1, message="Hata! Malzeme girişi değiştirilemedi")

        return jsonify(responsecode=0, heading="Tebrikler!", message="Başarıyla depo malzemesini değiştirdiniz.",
                       postmessage="Şimdi sayfa yenilenecektir.")

    elif request.method == 'DELETE':
        reqjson = request.get_json()
        user = dbexecutor.getUser(current_user.id)
        id = reqjson['id']
        if dbexecutor.handleDepotStockDelete(id, user.id) < 0:
            return jsonify(responsecode=-1, message="Hata! Malzeme silinemedi")

        return jsonify(responsecode=0, heading="Tebrikler!", message="Başarıyla depo malzemesini sildiniz.",
                       postmessage="Şimdi sayfa yenilenecektir.")


@app.route('/datamanagement', methods=['GET'])
@login_required
def datamanagement():
    if not current_user.isadmin:
        return render_template('autherror.html')

    stockcategories = dbexecutor.getAllStockCategory()
    stocktypes = dbexecutor.getAllStockTypes()
    stockcolors = dbexecutor.getAllStockColors()
    corporations = dbexecutor.getAllCorporations()
    stockpackages = dbexecutor.getAllStockPackages()
    stockunits = dbexecutor.getAllStockUnits()
    return render_template("datamanagement.html", stockcategories=stockcategories, stocktypes=stocktypes,
                           stockcolors=stockcolors, corporations=corporations, stockpackages=stockpackages,
                           stockunits=stockunits)


@app.route('/getstockcategories', methods=['POST'])
@login_required
def getStockCategories():
    if not current_user.isadmin:
        return render_template('autherror.html')

    categories = dbexecutor.getAllStockCategory()
    return jsonify(categories=[category.serialize() for category in categories])


@app.route('/getstocksubcategories', methods=['POST'])
@login_required
def getStockSubCategoriesByStockCategory():
    if not current_user.isadmin:
        return render_template('autherror.html')

    reqjson = request.get_json()
    catid = reqjson['id']
    subcategories = dbexecutor.getAllStockSubcategoryByStockCategory(catid)
    return jsonify(subcategories=[category.serialize() for category in subcategories])


@app.route('/getstocktypes', methods=['POST'])
@login_required
def getStockTypes():
    if not current_user.isadmin:
        return render_template('autherror.html')

    reqjson = request.get_json()
    catid = reqjson['id']
    stocktypes = dbexecutor.getAllStockTypesByStockSubcategory(catid)

    return jsonify(stocktypes=[stocktype.serialize() for stocktype in stocktypes])


@app.route('/stockmoves', methods=['GET'])
@login_required
def stockMoves():
    if not current_user.isadmin:
        return render_template('autherror.html')

    stockbases = dbexecutor.getAllStockBases()

    bases = []

    for stockbase in stockbases:
        base = {}
        base['userid'] = stockbase.userid
        base['username'] = stockbase.user.name
        base['stockcolorid'] = stockbase.stockcolorid
        base['stockcolorname'] = stockbase.stockcolor.name
        base['stocktypeid'] = stockbase.stocktypeid
        base['stocktypename'] = stockbase.stocktype.name
        base['quantity'] = stockbase.getQuantityText()
        base['createdate'] = stockbase.createdate
        base['action'] = stockbase.actiontype
        base['entry'] = stockbase.entrytype
        if stockbase.entrytype:
            base['entrytype'] = 'Form Girdisi'
            base['packagequantitytext'] = stockbase.getPackageQuantityText()
            base['note'] = stockbase.note
            base['formid'] = stockbase.stockformid
            base['formname'] = stockbase.stockform.name
            if stockbase.actiontype:
                base['actiontype'] = 'Depo Giriş Formu'

            else:
                base['actiontype'] = 'Ürün Sevkiyat Formu'

        else:
            base['entrytype'] = 'Depo Girdisi'
            base['packagequantitytext'] = '-'
            base['note'] = '-'
            base['formid'] = '-'
            base['formname'] = '-'
            if stockbase.actiontype:
                base['actiontype'] = 'Depo Girişi'
            else:
                base['actiontype'] = 'Depo Çıkışı'
        bases.append(base)

    return render_template("stockmoves.html", bases=bases)


@app.route('/formstockmoves', methods=['GET'])
@login_required
def formStockMoves():
    if not current_user.isadmin:
        return render_template('autherror.html')

    timevar = util.time_me()
    stockbases = dbexecutor.getAllStockBases()
    util.time_me(timevar)

    timevar = util.time_me()
    bases = []

    for stockbase in stockbases:
        if stockbase.entrytype:
            base = {}
            base['baseid'] = stockbase.id
            base['userid'] = stockbase.userid
            base['username'] = stockbase.user.name
            base['stockcolorid'] = stockbase.stockcolorid
            base['stockcolorname'] = stockbase.stockcolor.name
            base['stocktypeid'] = stockbase.stocktypeid
            base['stocktypename'] = stockbase.stocktype.name
            base['quantity'] = stockbase.getFormattedQuantity()
            base['quantityunit'] = stockbase.stocktype.stockunit.name
            base['createdate'] = stockbase.createdate
            base['action'] = stockbase.actiontype

            base['corporationid'] = stockbase.stockform.corporationid
            base['corporationname'] = stockbase.stockform.corporation.name
            base['recorddate'] = stockbase.stockform.recorddate

            base['packagequantity'] = stockbase.packagequantity
            base['packagequantityunit'] = stockbase.stockpackage.name
            base['note'] = stockbase.note
            if stockbase.actiontype:
                base['actiontype'] = 'Depo Giriş Formu'
                base['formid'] = stockbase.stockform.id
                base['formname'] = stockbase.stockform.name
                base['stockroomid'] = '-1'
                base['stockroomname'] = '-'
                base['shipinfo'] = '-'

            else:
                base['actiontype'] = 'Ürün Sevkiyat Formu'
                base['formid'] = stockbase.stockform.id
                base['formname'] = stockbase.stockform.name
                base['stockroomid'] = stockbase.stockform.stockformdetail.stockroom.id
                base['stockroomname'] = stockbase.stockform.stockformdetail.stockroom.name
                base['shipinfo'] = stockbase.stockform.stockformdetail.shipinfo

            bases.append(base)
    util.time_me(timevar)
    return render_template("formstockmoves.html", bases=bases)


@app.route('/downloadformstockmoves', methods=['POST'])
@login_required
def downloadFilteredFormStockMoves():
    if not current_user.isadmin:
        return render_template('autherror.html')

    reqjson = request.get_json()
    entries = reqjson['entries']
    columns = reqjson['columns']
    title = reqjson['title']
    try:
        formtemplate = FormStockMovesTemplate(entries, columns, title)
        formtemplate.generatePdf()
        return jsonify(responsecode=0)
    except Exception as e:
        if hasattr(e, 'message'):
            message = e.message
        else:
            message = 'Hata'
        return jsonify(responsecode=-1, message=message)


@app.route('/getfilteredformstockmovesdoc', methods=['GET'])
@login_required
def getFilteredFormStockMovesDoc():
    if not current_user.isadmin:
        return render_template('autherror.html')

    pdfpath = AppRoot + '/static/data/form.pdf'
    return send_file(pdfpath, mimetype="application/pdf", attachment_filename='form.pdf')


@app.route('/getstockcategoriesbystocktypeid', methods=['POST'])
@login_required
def getStockCategoriesByStockTypeId():
    if not current_user.isadmin:
        return render_template('autherror.html')

    reqjson = request.get_json()
    typeid = reqjson['id']
    stocktype = dbexecutor.getStockType(typeid)
    subcat = stocktype.subcategory
    cat = subcat.category
    subcategories = dbexecutor.getAllStockSubcategoryByStockCategory(cat.id)
    stocktypes = dbexecutor.getAllStockTypesByStockSubcategory(subcat.id)
    return jsonify(categoryid=cat.id, subcategoryid=subcat.id, stocktypeid=typeid,
                   subcategories=[sub.serialize() for sub in subcategories],
                   stocktypes=[type.serialize() for type in stocktypes])
