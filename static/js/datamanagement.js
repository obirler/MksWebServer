$(document).ready(function()
{
    //Handle close modal action because we dont have
    //extra modals that needs to be handled at the same time
    //dont need to set two close buttons seperately since
    //the default function does the same
    sCaMSetDefaultCloseBtns();
    $("#stockCategoryModalActionButton").on("click", function(){
        //default action with custom listener. Because we need to
        //update the select element
        sCaMDefaultSubmitAction(stockCategoryModalListener);
    });
    $('#stockcategorycollapse').collapse('show');

    sSMSetDefaultCloseBtns();
    $("#stockSubcategoryModalActionButton").on("click", function(){
        //default action with custom listener. Because we need to
        //update the select element
        sSMDefaultSubmitAction(stockSubcategoryModalListener);
    });

    $("#stocksubcategorycategoryselect").change(function(){
        stockSubcategoryCategorySelectionChanged();
    });

    sTMSetDefaultCloseBtns();
    $("#stockTypeModalActionButton").on("click", function(){
        //default action with custom listener. Because we need to
        //update the select element
        sTMDefaultSubmitAction(stockTypeModalListener);
    });

    $("#stocktypecategoryselect").change(function(){
        stockTypeCategorySelectionChanged();
    });

    $("#stocktypesubcategoryselect").change(function(){
        stockTypeSubcategorySelectionChanged();
    });

    sCMSetDefaultCloseBtns();
    $("#stockColorModalActionButton").on("click", function(){
        //default action with custom listener. Because we need to
        //update the select element
        sCMDefaultSubmitAction(stockColorModalListener);
    });

    sPMSetDefaultCloseBtns();
    $("#stockPackageModalActionButton").on("click", function(){
        //default action with custom listener. Because we need to
        //update the select element
        sPMDefaultSubmitAction(stockPackageModalListener);
    });

    cMSetDefaultCloseBtns();
    $("#corporationModalActionButton").on("click", function(){
        //default action with custom listener. Because we need to
        //update the select element
        cMDefaultSubmitAction(corporationModalListener);
    });

    sUMSetDefaultCloseBtns();
    $("#stockUnitModalActionButton").on("click", function(){
        //default action with custom listener. Because we need to
        //update the select element
        sUMDefaultSubmitAction(stockUnitModalListener);
    });

    getDataTable('stockcategorytable');
    getDataTable('stocksubcategorytable');
    getDataTable('stocktypetable');
    getDataTable('stockcolortable');
    getDataTable('corporationtable');
    getDataTable('stockpackagetable');
    getDataTable('stockunittable');
});

function stockcategoryclicked()
{
    hideall();
    var categorybtn = document.getElementById('stockcategorycollapsebtn');
    addClass(categorybtn, 'active');
    $('#stockcategorycollapse').collapse('show');
}

function stocksubcategoryclicked()
{
    hideall();
    var subcategorybtn = document.getElementById('stocksubcategorycollapsebtn');
    addClass(subcategorybtn, 'active');
    $('#stocksubcategorycollapse').collapse('show');
    stockSubcategoryUpdateCategories();
    cleartable('stocksubcategorytable');
}

function stocktypeclicked()
{
    hideall();
    var typebtn = document.getElementById('stocktypecollapsebtn');
    addClass(typebtn, 'active');
    $('#stocktypecollapse').collapse('show');
    stockTypeUpdateCategories();
    cleartable('stocktypetable');
}

function stockcolorclicked()
{
    hideall();
    var colorbtn = document.getElementById('stockcolorcollapsebtn');
    addClass(colorbtn, 'active');
    $('#stockcolorcollapse').collapse('show');
}

function corporationclicked()
{
    hideall();
    var corporationbtn = document.getElementById('corporationcollapsebtn');
    addClass(corporationbtn, 'active');
    $('#corporationcollapse').collapse('show');
}

function stockpackageclicked()
{
    hideall();
    var packagebtn = document.getElementById('stockpackagecollapsebtn');
    addClass(packagebtn, 'active');
    $('#stockpackagecollapse').collapse('show');
}

function stockunitclicked()
{
    hideall();
    var unitbtn = document.getElementById('stockunitcollapsebtn');
    addClass(unitbtn, 'active');
    $('#stockunitcollapse').collapse('show');
}

function hideall()
{
    var categorybtn = document.getElementById('stockcategorycollapsebtn');
    var subcategorybtn = document.getElementById('stocksubcategorycollapsebtn');
    var typebtn = document.getElementById('stocktypecollapsebtn');
    var colorbtn = document.getElementById('stockcolorcollapsebtn');
    var corporationbtn = document.getElementById('corporationcollapsebtn');
    var packagebtn = document.getElementById('stockpackagecollapsebtn');
    var unitbtn = document.getElementById('stockunitcollapsebtn');

    removeClass(categorybtn, 'active');
    removeClass(subcategorybtn, 'active');
    removeClass(typebtn, 'active');
    removeClass(colorbtn, 'active');
    removeClass(corporationbtn, 'active');
    removeClass(packagebtn, 'active');
    removeClass(unitbtn, 'active');

    $('#stockcategorycollapse').collapse('hide');
    $('#stocksubcategorycollapse').collapse('hide');
    $('#stocktypecollapse').collapse('hide');
    $('#stockcolorcollapse').collapse('hide');
    $('#corporationcollapse').collapse('hide');
    $('#stockpackagecollapse').collapse('hide');
    $('#stockunitcollapse').collapse('hide');
}

//////////////////////////////////////////////////////////////////
////////////////////////Stock Category////////////////////////////

function stockCategoryModalListener()
{
    var json = JSON.parse(this.responseText);

    switch(sCaMMode())
    {
      case "add":
        stockCategoryModalAddListener(json);
        break;
      case "update":
        stockCategoryModalUpdateListener(json);
        break;
      case "delete":
        stockCategoryModalDeleteListener(json);
        break;
      default:
        break;
    }
}

/* Stock Category Add Section*/
function openStockCategoryAddModalClicked()
{
    sCaMSetMode("add");

    $('#stockCategoryModal').modal('show');
}

function stockCategoryModalAddListener(json)
{
    if(json.responsecode === 0)
    {
        var table = getDataTable('stockcategorytable');
        table.row.add($(addStockCategoryEntryHtml(json.stockcategory.id, json.stockcategory.name)));
        table.draw();
        sCaMDefaultCloseActions();
    }
    else if(json.responsecode === -1)
    {
        sCaMShowAlert(json);
    }
}

function addStockCategoryEntryHtml(catid, catname)
{
    var rowid = 'stockcategory' + catid;
    var htmlstr = '<tr id="' + rowid +'">';
    htmlstr += '<td data-id="' + catid + '">' + catname + '</td>';
    htmlstr += '<td class="min">';
    htmlstr +=  '<div class="d-flex flex-nowrap">';
    htmlstr +=      '<button class="btn btn-primary" onclick="openStockCategoryUpdateModalClicked(\'' + catid + '\',\'' + catname + '\')" data-toggle="tooltip" title="Malzeme Kategorisini Değiştir">';
    htmlstr +=          '<i class="fas fa-external-link-alt"></i>';
    htmlstr +=      '</button>';
    htmlstr +=      '<span style="display: inline; width: 5px;"></span>';
    htmlstr +=      '<button class="btn btn-danger" onclick="openStockCategoryDeleteModalClicked(\'' + catid + '\',\'' + catname + '\')" data-toggle="tooltip" title="Malzeme Kategorisini Sil">';
    htmlstr +=          '<i class="fa fa-trash"></i>';
    htmlstr +=      '</button>';
    htmlstr +=  '</div>';
    htmlstr += '</td>';
    htmlstr += '</tr>';
    return htmlstr;
}

/* End Stock Category Add Section*/

/* Stock Category Update Section*/
function openStockCategoryUpdateModalClicked(id, name)
{
    sCaMSetMode("update");
    sCaMSetInfo(id, name);

    $('#stockCategoryModal').modal('show');
}

function stockCategoryModalUpdateListener(json)
{
    if(json.responsecode === 0)
    {
        updateStockCategoryEntry(json);

        sCaMDefaultCloseActions();
    }
    else if(json.responsecode === -1)
    {
        sCaMShowAlert(json);
    }
}

function updateStockCategoryEntry(json)
{
    var id = '#stockcategory' + json.stockcategory.id;
    var table = getDataTable('stockcategorytable');
    table.row(id).remove();
    table.row.add($(addStockCategoryEntryHtml(json.stockcategory.id, json.stockcategory.name)));
    table.draw();
}

/* End Stock Category Update Section*/

/* Stock Category Delete Section*/
function openStockCategoryDeleteModalClicked(id, name)
{
    sCaMSetMode("delete");
    sCaMSetInfo(id, name);

    $('#stockCategoryModal').modal('show');
}

function stockCategoryModalDeleteListener(json)
{
    if(json.responsecode === 0)
    {
        deleteStockCategoryEntry(json);

        sCaMDefaultCloseActions();
    }
    else if(json.responsecode === -1)
    {
        sCaMShowAlert(json);
    }
}

function deleteStockCategoryEntry(json)
{
    var id = '#stockcategory' + json.id;
    var table = getDataTable('stockcategorytable');
    table.row(id).remove();
    table.draw();
}

/* End Stock Category Delete Section*/

////////////////////////End Stock Category////////////////////////
//////////////////////////////////////////////////////////////////
/////////////////////////Stock Subcategory////////////////////////

function stockSubcategoryModalListener()
{
    var json = JSON.parse(this.responseText);

    switch(sSMMode())
    {
      case "add":
        stockSubcategoryModalAddListener(json);
        break;
      case "update":
        stockSubcategoryModalUpdateListener(json);
        break;
      case "delete":
        stockSubcategoryModalDeleteListener(json);
        break;
      default:
        break;
    }
}

function stockSubcategoryUpdateCategories()
{
    var request = new XMLHttpRequest();
    request.open("POST", "/getstockcategories");
    request.setRequestHeader("Content-Type", "application/json");
    request.addEventListener("load", stockSubcategoryCategoryReady);
    request.send("");
}

function stockSubcategoryCategoryReady()
{
    var json = JSON.parse(this.responseText);
    var categories = json['categories'];
    clearselect('stocksubcategorycategoryselect')
    stockSubcategoryLoadCategory(categories);
}

function stockSubcategoryLoadCategory(categories)
{
    var stockcategoryselect = document.getElementById("stocksubcategorycategoryselect");
    for (i = 0; i < categories.length; i++)
    {
        var option = document.createElement("option");
        var name = categories[i].name;
        option.textContent = name;
        option.setAttribute('data-id', categories[i].id);
        stockcategoryselect.appendChild(option);
    }
}

function stockSubcategoryCategorySelectionChanged()
{
    var stockcategoryselect = document.getElementById("stocksubcategorycategoryselect");
    var catid = stockcategoryselect.options[stockcategoryselect.selectedIndex].dataset.id;

    var stockcategory = {};
    stockcategory.id = catid;
    var request = new XMLHttpRequest();
    request.open("POST", "/getstocksubcategories");
    request.setRequestHeader("Content-Type", "application/json");
    request.addEventListener("load", stockSubcategorySubcategoryReady);
    var jsondata = JSON.stringify(stockcategory);
    request.send(jsondata);
}

function stockSubcategorySubcategoryReady()
{
    var json = JSON.parse(this.responseText);
    var subcategories = json['subcategories'];
    cleartable('stocksubcategorytable');
    var table = getDataTable('stocksubcategorytable');
    for (i=0; i< subcategories.length; i++)
    {
        table.row.add($(addStockSubcategoryEntryHtml(subcategories[i].id, subcategories[i].name, subcategories[i].categoryid)));
    }
    table.draw();
}

/* Stock Subcategory Add Section*/
function openStockSubcategoryAddModalClicked()
{
    sSMSetMode("add");
    var stockcategoryselect = document.getElementById("stocksubcategorycategoryselect");
    var catid = stockcategoryselect.options[stockcategoryselect.selectedIndex].dataset.id;
    sSMSetInfo(catid, -1, '');
    $('#stockSubcategoryModal').modal('show');
}

function stockSubcategoryModalAddListener(json)
{
    if(json.responsecode === 0)
    {
        var table = getDataTable('stocksubcategorytable');
        table.row.add($(addStockSubcategoryEntryHtml(json.stocksubcategory.id, json.stocksubcategory.name, json.stocksubcategory.categoryid)));
        table.draw();
        sSMDefaultCloseActions();
    }
    else if(json.responsecode === -1)
    {
        sSMShowAlert(json);
    }
}


function addStockSubcategoryEntryHtml(subcatid, subcatname, catid)
{
    var rowid = 'stocksubcategory' + subcatid;
    var htmlstr = '<tr id="' + rowid +'">';
    htmlstr += '<td data-id="' + subcatid + '" data-categoryid="' + catid + '">' + subcatname + '</td>';
    htmlstr += '<td class="min">';
    htmlstr +=  '<div class="d-flex flex-nowrap">';
    htmlstr +=      '<button class="btn btn-primary" onclick="openStockSubcategoryUpdateModalClicked(\'' + subcatid + '\',\'' + subcatname + '\',\'' + catid + '\')" data-toggle="tooltip" title="Malzeme Alt Kategorisini Değiştir">';
    htmlstr +=          '<i class="fas fa-external-link-alt"></i>';
    htmlstr +=      '</button>';
    htmlstr +=      '<span style="display: inline; width: 5px;"></span>';
    htmlstr +=      '<button class="btn btn-danger" onclick="openStockSubcategoryDeleteModalClicked(\'' + subcatid + '\',\'' + subcatname + '\',\'' + catid + '\')" data-toggle="tooltip" title="Malzeme Kategorisini Sil">';
    htmlstr +=          '<i class="fa fa-trash"></i>';
    htmlstr +=      '</button>';
    htmlstr +=  '</div>';
    htmlstr += '</td>';
    htmlstr += '</tr>';
    return htmlstr;
}

/* End Stock Subcategory Add Section*/

/* Stock Subcategory Update Section*/
function openStockSubcategoryUpdateModalClicked(id, name, categoryid)
{
    sSMSetMode("update");
    sSMSetInfo(categoryid, id, name);

    $('#stockSubcategoryModal').modal('show');
}

function stockSubcategoryModalUpdateListener(json)
{
    if(json.responsecode === 0)
    {
        updateStockSubcategoryEntry(json);

        sSMDefaultCloseActions();
    }
    else if(json.responsecode === -1)
    {
        sSMShowAlert(json);
    }
}

function updateStockSubcategoryEntry(json)
{
    var id = '#stocksubcategory' + json.stocksubcategory.id;
    var table = getDataTable('stocksubcategorytable');
    table.row(id).remove();
    table.row.add($(addStockSubcategoryEntryHtml(json.stocksubcategory.id, json.stocksubcategory.name, json.stocksubcategory.categoryid)));
    table.draw();
}

/* End Stock Subcategory Update Section*/

/* Stock Subcategory Delete Section*/
function openStockSubcategoryDeleteModalClicked(id, name, categoryid)
{
    sSMSetMode("delete");
    sSMSetInfo(categoryid, id, name);

    $('#stockSubcategoryModal').modal('show');
}

function stockSubcategoryModalDeleteListener(json)
{
    if(json.responsecode === 0)
    {
        deleteStockSubcategoryEntry(json);

        sSMDefaultCloseActions();
    }
    else if(json.responsecode === -1)
    {
        sSMShowAlert(json);
    }
}

function deleteStockSubcategoryEntry(json)
{
    var id = '#stocksubcategory' + json.id;
    var table = getDataTable('stocksubcategorytable');
    table.row(id).remove();
    table.draw();
}
/* End Stock Subcategory Delete Section*/

//////////////////////End Stock Subcategory///////////////////////
//////////////////////////////////////////////////////////////////
////////////////////////////Stock Type////////////////////////////

function stockTypeModalListener()
{
    var json = JSON.parse(this.responseText);

    switch(sTMMode())
    {
      case "add":
        stockTypeModalAddListener(json);
        break;
      case "update":
        stockTypeModalUpdateListener(json);
        break;
      case "delete":
        stockTypeModalDeleteListener(json);
        break;
      default:
        break;
    }
}

function stockTypeUpdateCategories()
{
    var request = new XMLHttpRequest();
    request.open("POST", "/getstockcategories");
    request.setRequestHeader("Content-Type", "application/json");
    request.addEventListener("load", stockTypeCategoryReady);
    request.send("");
}

function stockTypeCategoryReady()
{
    var json = JSON.parse(this.responseText);
    var categories = json['categories'];
    clearselect('stocktypecategoryselect');
    stockTypeLoadCategory(categories);
    clearselect('stocktypesubcategoryselect');
    cleartable('stocktypetable');
}

function stockTypeLoadCategory(categories)
{
    var stockcategoryselect = document.getElementById("stocktypecategoryselect");
    for (i = 0; i < categories.length; i++)
    {
        var option = document.createElement("option");
        var name = categories[i].name;
        option.textContent = name;
        option.setAttribute('data-id', categories[i].id);
        stockcategoryselect.appendChild(option);
    }
}

function stockTypeCategorySelectionChanged()
{
    var stockcategoryselect = document.getElementById("stocktypecategoryselect");
    var catid = stockcategoryselect.options[stockcategoryselect.selectedIndex].dataset.id;

    var stockcategory = {};
    stockcategory.id = catid;
    var request = new XMLHttpRequest();
    request.open("POST", "/getstocksubcategories");
    request.setRequestHeader("Content-Type", "application/json");
    request.addEventListener("load", stockTypeSubcategoryReady);
    var jsondata = JSON.stringify(stockcategory);
    request.send(jsondata);
}

function stockTypeSubcategoryReady()
{
    clearselect('stocktypesubcategoryselect');
    cleartable('stocktypetable');
    var json = JSON.parse(this.responseText);
    var subcategories = json['subcategories'];
    for (i=0; i< subcategories.length; i++)
    {
        stockTypeLoadSubcategory(subcategories);
    }
}

function stockTypeLoadSubcategory(categories)
{
    var stockcategoryselect = document.getElementById("stocktypesubcategoryselect");
    for (i = 0; i < categories.length; i++)
    {
        var option = document.createElement("option");
        var name = categories[i].name;
        option.textContent = name;
        option.setAttribute('data-id', categories[i].id);
        stockcategoryselect.appendChild(option);
    }
}

function stockTypeSubcategorySelectionChanged()
{
    var stocksubcategoryselect = document.getElementById("stocktypesubcategoryselect");
    var subcatid = stocksubcategoryselect.options[stocksubcategoryselect.selectedIndex].dataset.id;

    var stocktype = {};
    stocktype.id = subcatid;
    var request = new XMLHttpRequest();
    request.open("POST", "/getstocktypes");
    request.setRequestHeader("Content-Type", "application/json");
    request.addEventListener("load", stockTypeReady);
    var jsondata = JSON.stringify(stocktype);
    request.send(jsondata);
}

function stockTypeReady()
{
    cleartable('stocktypetable');
    var json = JSON.parse(this.responseText);
    var stocktypes = json['stocktypes'];
    var table = getDataTable('stocktypetable');
    for (i=0; i< stocktypes.length; i++)
    {
        table.row.add($(addStockTypeEntryHtml(stocktypes[i].id,stocktypes[i].name, stocktypes[i].unitid, stocktypes[i].unitname, stocktypes[i].subcategoryid)));
    }
    table.draw();
}

/* Stock Type Add Section*/
function openStockTypeAddModalClicked()
{
    sTMSetMode("add");
    var stocksubcategoryselect = document.getElementById("stocktypesubcategoryselect");
    var subcatid = stocksubcategoryselect.options[stocksubcategoryselect.selectedIndex].dataset.id;
    sTMSetInfo(-1, '', -1, subcatid);
    $('#stockTypeModal').modal('show');
}

function stockTypeModalAddListener(json)
{
    if(json.responsecode === 0)
    {
        var table = getDataTable('stocktypetable');
        table.row.add($(addStockTypeEntryHtml(json.stocktype.id, json.stocktype.name, json.stocktype.unitid, json.stocktype.unitname, json.stocktype.subcategoryid)));
        table.draw();
        sTMDefaultCloseActions();
    }
    else if(json.responsecode === -1)
    {
        sTMShowAlert(json);
    }
}

function addStockTypeEntryHtml(typeid, typename, unitid, unitname, subcatid)
{
    var rowid = 'stocktype' + typeid;
    var htmlstr = '<tr id="' + rowid +'">';
    htmlstr += '<td data-id="' + typeid + '">' + typename + '</td>';
    htmlstr += '<td data-unitid="' + unitid + '">' + unitname + '</td>';
    htmlstr += '<td class="min">';
    htmlstr +=  '<div class="d-flex flex-nowrap">';
    htmlstr +=      '<button class="btn btn-primary" onclick="openStockTypeUpdateModalClicked(\'' + typeid + '\',\'' + typename + '\',\'' + unitid + '\',\'' + subcatid + '\')" data-toggle="tooltip" title="Malzeme Cinsini Değiştir">';
    htmlstr +=          '<i class="fas fa-external-link-alt"></i>';
    htmlstr +=      '</button>';
    htmlstr +=      '<span style="display: inline; width: 5px;"></span>';
    htmlstr +=      '<button class="btn btn-danger" onclick="openStockTypeDeleteModalClicked (\'' + typeid + '\',\'' + typename + '\',\'' + unitid + '\',\'' + subcatid + '\')" data-toggle="tooltip" title="Malzeme Kategorisini Sil">';
    htmlstr +=          '<i class="fa fa-trash"></i>';
    htmlstr +=      '</button>';
    htmlstr +=  '</div>';
    htmlstr += '</td>';
    htmlstr += '</tr>';
    return htmlstr;
}

/* End Stock Type Add Section*/

/* Stock Type Update Section*/
function openStockTypeUpdateModalClicked(id, name, unitid, subcatid)
{
    sTMSetMode("update");
    sTMSetInfo(id, name, unitid, subcatid);

    $('#stockTypeModal').modal('show');
}

function stockTypeModalUpdateListener(json)
{
    if(json.responsecode === 0)
    {
        updateStockTypeEntry(json);

        sTMDefaultCloseActions();
    }
    else if(json.responsecode === -1)
    {
        sTMShowAlert(json);
    }
}

function updateStockTypeEntry(json)
{
    var id = '#stocktype' + json.stocktype.id;
    var table = getDataTable('stocktypetable');
    table.row(id).remove();
    table.row.add($(addStockTypeEntryHtml(json.stocktype.id, json.stocktype.name, json.stocktype.unitid, json.stocktype.unitname, json.stocktype.subcategoryid)));
    table.draw();
}

/* Stock Type Delete Section*/
function openStockTypeDeleteModalClicked(id, name, unitid, subcatid)
{
    sTMSetMode("delete");
    sTMSetInfo(id, name, unitid, subcatid);

    $('#stockTypeModal').modal('show');
}

function stockTypeModalDeleteListener(json)
{
    if(json.responsecode === 0)
    {
        deleteStockTypeEntry(json);

        sTMDefaultCloseActions();
    }
    else if(json.responsecode === -1)
    {
        sTMShowAlert(json);
    }
}

function deleteStockTypeEntry(json)
{
    var id = '#stocktype' + json.id;
    var table = getDataTable('stocktypetable');
    table.row(id).remove();
    table.draw();
}
/* End Stock Type Delete Section*/

////////////////////////End Stock Type////////////////////////////
//////////////////////////////////////////////////////////////////
//////////////////////////Stock Color/////////////////////////////

function stockColorModalListener()
{
    var json = JSON.parse(this.responseText);

    switch(sCMMode())
    {
      case "add":
        stockColorModalAddListener(json);
        break;
      case "update":
        stockColorModalUpdateListener(json);
        break;
      case "delete":
        stockColorModalDeleteListener(json);
        break;
      default:
        break;
    }
}

/* Stock Color Add Section*/
function openStockColorAddModalClicked()
{
    sCMSetMode("add");

    $('#stockColorModal').modal('show');
}

function stockColorModalAddListener(json)
{
    if(json.responsecode === 0)
    {
        var table = getDataTable('stockcolortable');
        table.row.add($(addStockColorEntryHtml(json.stockcolor.id, json.stockcolor.name)));
        table.draw();
        sCMDefaultCloseActions();
    }
    else if(json.responsecode === -1)
    {
        sCMShowAlert(json);
    }
}

function addStockColorEntryHtml(colorid, colorname)
{
    var rowid = 'stockcolor' + colorid;
    var htmlstr = '<tr id="' + rowid +'">';
    htmlstr += '<td data-id="' + colorid + '">' + colorname + '</td>';
    htmlstr += '<td class="min">';
    htmlstr +=  '<div class="d-flex flex-nowrap">';
    htmlstr +=      '<button class="btn btn-primary" onclick="openStockColorUpdateModalClicked(\'' + colorid + '\',\'' + colorname + '\')" data-toggle="tooltip" title="Malzeme Rengini Değiştir">';
    htmlstr +=          '<i class="fas fa-external-link-alt"></i>';
    htmlstr +=      '</button>';
    htmlstr +=      '<span style="display: inline; width: 5px;"></span>';
    htmlstr +=      '<button class="btn btn-danger" onclick="openStockColorDeleteModalClicked(\'' + colorid + '\',\'' + colorname + '\')" data-toggle="tooltip" title="Malzeme Rengini Sil">';
    htmlstr +=          '<i class="fa fa-trash"></i>';
    htmlstr +=      '</button>';
    htmlstr +=  '</div>';
    htmlstr += '</td>';
    htmlstr += '</tr>';
    return htmlstr;
}

/* End Stock Color Add Section*/

/* Stock Color Update Section*/
function openStockColorUpdateModalClicked(id, name)
{
    sCMSetMode("update");
    sCMSetInfo(id, name);

    $('#stockColorModal').modal('show');
}

function stockColorModalUpdateListener(json)
{
    if(json.responsecode === 0)
    {
        updateStockColorEntry(json);

        sCMDefaultCloseActions();
    }
    else if(json.responsecode === -1)
    {
        sCMShowAlert(json);
    }
}

function updateStockColorEntry(json)
{
    var id = '#stockcolor' + json.stockcolor.id;
    var table = getDataTable('stockcolortable');
    table.row(id).remove();
    table.row.add($(addStockColorEntryHtml(json.stockcolor.id, json.stockcolor.name)));
    table.draw();
}

/* End Stock Color Update Section*/

/* Stock Color Delete Section*/
function openStockColorDeleteModalClicked(id, name)
{
    sCMSetMode("delete");
    sCMSetInfo(id, name);

    $('#stockColorModal').modal('show');
}

function stockColorModalDeleteListener(json)
{
    if(json.responsecode === 0)
    {
        deleteStockColorEntry(json);

        sCMDefaultCloseActions();
    }
    else if(json.responsecode === -1)
    {
        sCMShowAlert(json);
    }
}

function deleteStockColorEntry(json)
{
    var id = '#stockcolor' + json.id;
    var table = getDataTable('stockcolortable');
    table.row(id).remove();
    table.draw();
}
/* End Stock Color Delete Section*/

////////////////////////End Stock Color///////////////////////////
//////////////////////////////////////////////////////////////////
////////////////////////Stock Package/////////////////////////////

function stockPackageModalListener()
{
    var json = JSON.parse(this.responseText);

    switch(sPMMode())
    {
      case "add":
        stockPackageModalAddListener(json);
        break;
      case "update":
        stockPackageModalUpdateListener(json);
        break;
      case "delete":
        stockPackageModalDeleteListener(json);
        break;
      default:
        break;
    }
}

/* Stock Package Add Section*/
function openStockPackageAddModalClicked()
{
    sPMSetMode("add");

    $('#stockPackageModal').modal('show');
}

function stockPackageModalAddListener(json)
{
    if(json.responsecode === 0)
    {
        var table = getDataTable('stockpackagetable');
        table.row.add($(addStockPackageEntryHtml(json.stockpackage.id, json.stockpackage.name)));
        table.draw();

        sPMDefaultCloseActions();
    }
    else if(json.responsecode === -1)
    {
        sPMShowAlert(json);
    }
}

function addStockPackageEntryHtml(packageid, packagename)
{
    var rowid = 'stockpackage' + packageid;
    var htmlstr = '<tr id="' + rowid +'">';
    htmlstr += '<td data-id="' + packageid + '">' + packagename + '</td>';
    htmlstr += '<td class="min">';
    htmlstr +=  '<div class="d-flex flex-nowrap">';
    htmlstr +=      '<button class="btn btn-primary" onclick="openStockPackageUpdateModalClicked(\'' + packageid + '\',\'' + packagename + '\')" data-toggle="tooltip" title="Malzeme Rengini Değiştir">';
    htmlstr +=          '<i class="fas fa-external-link-alt"></i>';
    htmlstr +=      '</button>';
    htmlstr +=      '<span style="display: inline; width: 5px;"></span>';
    htmlstr +=      '<button class="btn btn-danger" onclick="openStockPackageDeleteModalClicked(\'' + packageid + '\',\'' + packagename + '\')" data-toggle="tooltip" title="Malzeme Rengini Sil">';
    htmlstr +=          '<i class="fa fa-trash"></i>';
    htmlstr +=      '</button>';
    htmlstr +=  '</div>';
    htmlstr += '</td>';
    htmlstr += '</tr>';
    return htmlstr;
}

/* End Stock Package Add Section*/

/* Stock Package Update Section*/
function openStockPackageUpdateModalClicked(id, name)
{
    sPMSetMode("update");
    sPMSetInfo(id, name);

    $('#stockPackageModal').modal('show');
}

function stockPackageModalUpdateListener(json)
{
    if(json.responsecode === 0)
    {
        updateStockPackageEntry(json);

        sPMDefaultCloseActions();
    }
    else if(json.responsecode === -1)
    {
        sPMShowAlert(json);
    }
}

function updateStockPackageEntry(json)
{
    var id = '#stockpackage' + json.stockpackage.id;
    var table = getDataTable('stockpackagetable');
    table.row(id).remove();
    table.row.add($(addStockPackageEntryHtml(json.stockpackage.id, json.stockpackage.name)));
    table.draw();
}

/* End Stock Package Update Section*/

/* Stock Package Delete Section*/
function openStockPackageDeleteModalClicked(id, name)
{
    sPMSetMode("delete");
    sPMSetInfo(id, name);

    $('#stockPackageModal').modal('show');
}

function stockPackageModalDeleteListener(json)
{
    if(json.responsecode === 0)
    {
        deleteStockPackageEntry(json);

        sPMDefaultCloseActions();
    }
    else if(json.responsecode === -1)
    {
        sPMShowAlert(json);
    }
}

function deleteStockPackageEntry(json)
{
    var id = '#stockpackage' + json.id;
    var table = getDataTable('stockpackagetable');
    table.row(id).remove();
    table.draw();
}

/* End Stock Package Delete Section*/

////////////////////////End Stock Package//////////////////////////
///////////////////////////////////////////////////////////////////
///////////////////////////Corporation/////////////////////////////

function corporationModalListener()
{
    var json = JSON.parse(this.responseText);

    switch(cMMode())
    {
      case "add":
        corporationModalAddListener(json);
        break;
      case "update":
        corporationModalUpdateListener(json);
        break;
      case "delete":
        corporationModalDeleteListener(json);
        break;
      default:
        break;
    }
}

/* Corporation Add Section*/
function openCorporationAddModalClicked()
{
    cMSetMode("add");

    $('#corporationModal').modal('show');
}

function corporationModalAddListener(json)
{
    if(json.responsecode === 0)
    {
        var table = getDataTable('corporationtable');
        table.row.add($(addCorporationEntryHtml(json.corporation.id, json.corporation.name)));
        table.draw();

        cMDefaultCloseActions();
    }
    else if(json.responsecode === -1)
    {
        cMShowAlert(json);
    }
}

function addCorporationEntryHtml(corporationid, corporationname)
{
    var rowid = 'corporation' + corporationid;
    var htmlstr = '<tr id="' + rowid +'">';
    htmlstr += '<td data-id="' + corporationid + '">' + corporationname + '</td>';
    htmlstr += '<td class="min">';
    htmlstr +=  '<div class="d-flex flex-nowrap">';
    htmlstr +=      '<button class="btn btn-primary" onclick="openCorporationUpdateModalClicked(\'' + corporationid + '\',\'' + corporationname + '\')" data-toggle="tooltip" title="Malzeme Rengini Değiştir">';
    htmlstr +=          '<i class="fas fa-external-link-alt"></i>';
    htmlstr +=      '</button>';
    htmlstr +=      '<span style="display: inline; width: 5px;"></span>';
    htmlstr +=      '<button class="btn btn-danger" onclick="openCorporationDeleteModalClicked(\'' + corporationid + '\',\'' + corporationname + '\')" data-toggle="tooltip" title="Malzeme Rengini Sil">';
    htmlstr +=          '<i class="fa fa-trash"></i>';
    htmlstr +=      '</button>';
    htmlstr +=  '</div>';
    htmlstr += '</td>';
    htmlstr += '</tr>';
    return htmlstr;
}

/* End Corporation Add Section*/

/* Corporation Update Section*/
function openCorporationUpdateModalClicked(id, name)
{
    cMSetMode("update");
    cMSetInfo(id, name);

    $('#corporationModal').modal('show');
}

function corporationModalUpdateListener(json)
{
    if(json.responsecode === 0)
    {
        updateCorporationEntry(json);

        cMDefaultCloseActions();
    }
    else if(json.responsecode === -1)
    {
        cMShowAlert(json);
    }
}

function updateCorporationEntry(json)
{
    var id = '#corporation' + json.corporation.id;
    var table = getDataTable('corporationtable');
    table.row(id).remove();
    table.row.add($(addCorporationEntryHtml(json.corporation.id, json.corporation.name)));
    table.draw();
}
/* End Corporation Update Section*/

/* Corporation Delete Section*/
function openCorporationDeleteModalClicked(id, name)
{
    cMSetMode("delete");
    cMSetInfo(id, name);

    $('#corporationModal').modal('show');
}

function corporationModalDeleteListener(json)
{
    if(json.responsecode === 0)
    {
        deleteCorporationEntry(json);

        cMDefaultCloseActions();
    }
    else if(json.responsecode === -1)
    {
        cMShowAlert(json);
    }
}

function deleteCorporationEntry(json)
{
    var id = '#corporation' + json.id;
    var table = getDataTable('corporationtable');
    table.row(id).remove();
    table.draw();
}

/* End Corporation Delete Section*/

////////////////////////End Corporation//////////////////////////
/////////////////////////////////////////////////////////////////
///////////////////////////Stock Unit////////////////////////////

function stockUnitModalListener()
{
    var json = JSON.parse(this.responseText);

    switch(sUMMode())
    {
      case "add":
        stockUnitModalAddListener(json);
        break;
      case "update":
        stockUnitModalUpdateListener(json);
        break;
      case "delete":
        stockUnitModalDeleteListener(json);
        break;
      default:
        break;
    }
}

/* Stock Unit Add Section*/
function openStockUnitAddModalClicked()
{
    sUMSetMode("add");

    $('#stockUnitModal').modal('show');
}

function stockUnitModalAddListener(json)
{
    if(json.responsecode === 0)
    {
        var table = getDataTable('stockunittable');
        table.row.add($(addStockUnitEntryHtml(json.stockunit.id, json.stockunit.name)));
        table.draw();

        sUMDefaultCloseActions();
    }
    else if(json.responsecode === -1)
    {
        sUMShowAlert(json);
    }
}

function addStockUnitEntryHtml(unitid, unitname)
{
    var rowid = 'stockunit' + unitid;
    var htmlstr = '<tr id="' + rowid +'">';
    htmlstr += '<td data-id="' + unitid + '">' + unitname + '</td>';
    htmlstr += '<td class="min">';
    htmlstr +=  '<div class="d-flex flex-nowrap">';
    htmlstr +=      '<button class="btn btn-primary" onclick="openStockUnitUpdateModalClicked(\'' + unitid + '\',\'' + unitname + '\')" data-toggle="tooltip" title="Malzeme Rengini Değiştir">';
    htmlstr +=          '<i class="fas fa-external-link-alt"></i>';
    htmlstr +=      '</button>';
    htmlstr +=      '<span style="display: inline; width: 5px;"></span>';
    htmlstr +=      '<button class="btn btn-danger" onclick="openStockUnitDeleteModalClicked(\'' + unitid + '\',\'' + unitname + '\')" data-toggle="tooltip" title="Malzeme Rengini Sil">';
    htmlstr +=          '<i class="fa fa-trash"></i>';
    htmlstr +=      '</button>';
    htmlstr +=  '</div>';
    htmlstr += '</td>';
    htmlstr += '</tr>';
    return htmlstr;
}

/* End Stock Unit Add Section*/

/* Stock Unit Update Section*/
function openStockUnitUpdateModalClicked(id, name, precision)
{
    sUMSetMode("update");
    sUMSetInfo(id, name, precision);

    $('#stockUnitModal').modal('show');
}

function stockUnitModalUpdateListener(json)
{
    if(json.responsecode === 0)
    {
        updateStockUnitEntry(json);

        sUMDefaultCloseActions();
    }
    else if(json.responsecode === -1)
    {
        sUMShowAlert(json);
    }
}

function updateStockUnitEntry(json)
{
    var id = '#stockunit' + json.stockunit.id;
    var table = getDataTable('stockunittable');
    table.row(id).remove();
    table.row.add($(addStockUnitEntryHtml(json.stockunit.id, json.stockunit.name)));
    table.draw();
}
/* End Stock Unit Update Section*/

/* Stock Unit Delete Section*/
function openStockUnitDeleteModalClicked(id, name, precision)
{
    sUMSetMode("delete");
    sUMSetInfo(id, name, precision);

    $('#stockUnitModal').modal('show');
}

function stockUnitModalDeleteListener(json)
{
    if(json.responsecode === 0)
    {
        deleteStockUnitEntry(json);

        sUMDefaultCloseActions();
    }
    else if(json.responsecode === -1)
    {
        sUMShowAlert(json);
    }
}

function deleteStockUnitEntry(json)
{
    var id = '#stockunit' + json.id;
    var table = getDataTable('stockunittable');
    table.row(id).remove();
    table.draw();
}
/* End Stock Unit Delete Section*/

////////////////////////End Stock Unit///////////////////////////
/////////////////////////////////////////////////////////////////

function hasClass(el, className)
{
    if (el.classList)
        return el.classList.contains(className);
    return !!el.className.match(new RegExp('(\\s|^)' + className + '(\\s|$)'));
}

function addClass(el, className)
{
    if (el.classList)
        el.classList.add(className)
    else if (!hasClass(el, className))
        el.className += " " + className;
}

function removeClass(el, className)
{
    if (el.classList)
        el.classList.remove(className)
    else if (hasClass(el, className))
    {
        var reg = new RegExp('(\\s|^)' + className + '(\\s|$)');
        el.className = el.className.replace(reg, ' ');
    }
}

function clearselect(id)
{
    var selectinput = document.getElementById(id);
    var option = selectinput.options[1];
    while(typeof option != 'undefined')
    {
        selectinput.removeChild(option);
        option = selectinput.options[1];
    }
}

function resetselect(id)
{
    var select = document.getElementById(id);
    select.selectedIndex = 0;
}

function cleartable(id)
{
    var table = getDataTable(id);
    table.clear()
    table.draw();
}