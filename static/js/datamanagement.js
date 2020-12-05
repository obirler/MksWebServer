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

function addStockCategoryTableButtonGroup(row, json)
{
    var newCell = row.insertCell();
    var div = document.createElement('div');
    newCell.appendChild(div);
    addClass(div, "form-row");

    var button1 = document.createElement("button");
    addClass(button1, "btn");
    addClass(button1, "btn-primary");
    button1.setAttribute('data-toggle', 'tooltip');
    button1.setAttribute('title', 'Malzeme Kategorisini Değiştir');
    button1.setAttribute('onclick', "openStockCategoryUpdateModalClicked('" + json.stockcategory.id + "','"+ json.stockcategory.name + "')");

    div.appendChild(button1);
    var ielement1 = document.createElement('i');
    addClass(ielement1, "fas");
    addClass(ielement1, "fa-external-link-alt");
    button1.appendChild(ielement1);

    var button2 = document.createElement("button");
    addClass(button2, "btn");
    addClass(button2, "btn-danger");
    button2.setAttribute('data-toggle', 'tooltip');
    button2.setAttribute('title', 'Malzeme Kategorisini Sil');
    button2.setAttribute('onclick', "openStockCategoryDeleteModalClicked('" + json.stockcategory.id + "','"+ json.stockcategory.name + "')");

    var span = document.createElement("span");
    span.style.display = "inline";
    span.style.width = "5px";
    div.appendChild(span);

    div.appendChild(button2);
    var ielement2 = document.createElement('i');
    addClass(ielement2, "fas");
    addClass(ielement2, "fa-trash");
    button2.appendChild(ielement2);
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
        addStockCategoryEntry(json);

        sCaMDefaultCloseActions();
    }
    else if(json.responsecode === -1)
    {
        sCaMShowAlert(json);
    }
}

function addStockCategoryEntry(json)
{
    var tbodyRef = document.getElementById('stockcategorytable').getElementsByTagName('tbody')[0];

    var newRow = tbodyRef.insertRow();
    var newCell = newRow.insertCell();
    newCell.textContent = json.stockcategory.name;
    newCell.style.verticalAlign= "middle";
    newCell.setAttribute('data-id', json.stockcategory.id);

    addStockCategoryTableButtonGroup(newRow, json);
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
    var table = document.getElementById("stockcategorytable");

    //start i with 1 instead of 0 because we dont want to touch table header
    for (var i = 1; i < table.rows.length; i++)
    {
        if(table.rows[i].cells[0].dataset.id == json.stockcategory.id)
        {
            table.rows[i].cells[0].textContent = json.stockcategory.name;
            table.rows[i].deleteCell(1);

            addStockCategoryTableButtonGroup(table.rows[i], json);
            break;
        }
    }
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
    var table = document.getElementById("stockcategorytable");

    //start i with 1 instead of 0 because we dont want to touch table header
    for (var i = 1; i < table.rows.length; i++)
    {
        if(table.rows[i].cells[0].dataset.id == json.id)
        {
            table.deleteRow(i);
            break;
        }
    }
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

function addStockSubcategoryTableButtonGroupWrapper(row, subcatid, subcatname, catid)
{
        var newCell = row.insertCell();
    var div = document.createElement('div');
    newCell.appendChild(div);
    addClass(div, "form-row");

    var button1 = document.createElement("button");
    addClass(button1, "btn");
    addClass(button1, "btn-primary");
    button1.setAttribute('data-toggle', 'tooltip');
    button1.setAttribute('title', 'Malzeme Alt Kategorisini Değiştir');
    button1.setAttribute('onclick', "openStockSubcategoryUpdateModalClicked('" + subcatid + "','"+ subcatname +"','" + catid + "')");

    div.appendChild(button1);
    var ielement1 = document.createElement('i');
    addClass(ielement1, "fas");
    addClass(ielement1, "fa-external-link-alt");
    button1.appendChild(ielement1);

    var button2 = document.createElement("button");
    addClass(button2, "btn");
    addClass(button2, "btn-danger");
    button2.setAttribute('data-toggle', 'tooltip');
    button2.setAttribute('title', 'Malzeme Alt Kategorisini Sil');
    button2.setAttribute('onclick', "openStockSubcategoryDeleteModalClicked('" + subcatid + "','"+ subcatname +"','" + catid + "')");

    var span = document.createElement("span");
    span.style.display = "inline";
    span.style.width = "5px";
    div.appendChild(span);

    div.appendChild(button2);
    var ielement2 = document.createElement('i');
    addClass(ielement2, "fas");
    addClass(ielement2, "fa-trash");
    button2.appendChild(ielement2);
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
    for (i=0; i< subcategories.length; i++)
    {
        addStockSubcategoryEntry(subcategories[i].id, subcategories[i].name, subcategories[i].categoryid);
    }
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
        addStockSubcategoryEntryFromJson(json);

        sSMDefaultCloseActions();
    }
    else if(json.responsecode === -1)
    {
        sSMShowAlert(json);
    }
}

function addStockSubcategoryEntry(subcatid, subcatname, catid)
{
    var tbodyRef = document.getElementById('stocksubcategorytable').getElementsByTagName('tbody')[0];

    var newRow = tbodyRef.insertRow();
    var newCell = newRow.insertCell();
    newCell.textContent = subcatname;
    newCell.style.verticalAlign= "middle";
    newCell.setAttribute('data-id', subcatid);
    newCell.setAttribute('data-categoryid', catid);

    addStockSubcategoryTableButtonGroupWrapper(newRow, subcatid, subcatname, catid);
}

function addStockSubcategoryEntryFromJson(json)
{
    var tbodyRef = document.getElementById('stocksubcategorytable').getElementsByTagName('tbody')[0];

    var newRow = tbodyRef.insertRow();
    var newCell = newRow.insertCell();
    newCell.textContent = json.stocksubcategory.name;
    newCell.style.verticalAlign= "middle";
    newCell.setAttribute('data-id', json.stocksubcategory.id);
    newCell.setAttribute('data-categoryid', json.stocksubcategory.categoryid);

    addStockSubcategoryTableButtonGroupWrapper(newRow, json.stocksubcategory.id, json.stocksubcategory.name, json.stocksubcategory.categoryid);
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
    var table = document.getElementById("stocksubcategorytable");

    //start i with 1 instead of 0 because we dont want to touch table header
    for (var i = 1; i < table.rows.length; i++)
    {
        if(table.rows[i].cells[0].dataset.id == json.stocksubcategory.id)
        {
            table.rows[i].cells[0].textContent = json.stocksubcategory.name;
            table.rows[i].cells[0].setAttribute('data-id', json.stocksubcategory.id);
            table.rows[i].cells[0].setAttribute('data-categoryid', json.stocksubcategory.categoryid);
            table.rows[i].deleteCell(1);

            addStockSubcategoryTableButtonGroupWrapper(table.rows[i], json.stocksubcategory.id, json.stocksubcategory.name, json.stocksubcategory.categoryid)
            break;
        }
    }
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
    var table = document.getElementById("stocksubcategorytable");

    //start i with 1 instead of 0 because we dont want to touch table header
    for (var i = 1; i < table.rows.length; i++)
    {
        if(table.rows[i].cells[0].dataset.id == json.id)
        {
            table.deleteRow(i);
            break;
        }
    }
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

function addStockTypeTableButtonGroup(row, typeid, typename, unitid, subcatid)
{
    var newCell = row.insertCell();
    var div = document.createElement('div');
    newCell.appendChild(div);
    addClass(div, "form-row");

    var button1 = document.createElement("button");
    addClass(button1, "btn");
    addClass(button1, "btn-primary");
    button1.setAttribute('data-toggle', 'tooltip');
    button1.setAttribute('title', 'Malzeme Cinsini Değiştir');
    button1.setAttribute('onclick', "openStockTypeUpdateModalClicked('" + typeid + "','"+ typename +"','" + unitid + "','" + subcatid + "')");

    div.appendChild(button1);
    var ielement1 = document.createElement('i');
    addClass(ielement1, "fas");
    addClass(ielement1, "fa-external-link-alt");
    button1.appendChild(ielement1);

    var button2 = document.createElement("button");
    addClass(button2, "btn");
    addClass(button2, "btn-danger");
    button2.setAttribute('data-toggle', 'tooltip');
    button2.setAttribute('title', 'Malzeme Cinsini Sil');
    button2.setAttribute('onclick', "openStockTypeDeleteModalClicked('" + typeid + "','"+ typename +"','" + unitid + "','" + subcatid + "')");

    var span = document.createElement("span");
    span.style.display = "inline";
    span.style.width = "5px";
    div.appendChild(span);

    div.appendChild(button2);
    var ielement2 = document.createElement('i');
    addClass(ielement2, "fas");
    addClass(ielement2, "fa-trash");
    button2.appendChild(ielement2);
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
    for (i=0; i< stocktypes.length; i++)
    {
        addStockTypeEntry(stocktypes[i].id,stocktypes[i].name, stocktypes[i].unitid, stocktypes[i].unitname, stocktypes[i].subcategoryid);
    }
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
        addStockTypeEntryFromJson(json);

        sTMDefaultCloseActions();
    }
    else if(json.responsecode === -1)
    {
        sTMShowAlert(json);
    }
}

function addStockTypeEntry(typeid, typename, unitid, unitname, subcatid)
{
    var tbodyRef = document.getElementById('stocktypetable').getElementsByTagName('tbody')[0];

    var newRow = tbodyRef.insertRow();
    var newCell = newRow.insertCell();
    newCell.textContent = typename;
    newCell.style.verticalAlign= "middle";
    newCell.setAttribute('data-id', typeid);

    newCell = newRow.insertCell();
    newCell.textContent = unitname;
    newCell.style.verticalAlign= "middle";
    newCell.setAttribute('data-unitid', unitid);
    addStockTypeTableButtonGroup(newRow, typeid, typename, unitid, subcatid);
}

function addStockTypeEntryFromJson(json)
{
    var tbodyRef = document.getElementById('stocktypetable').getElementsByTagName('tbody')[0];

    var newRow = tbodyRef.insertRow();
    var newCell = newRow.insertCell();
    newCell.textContent = json.stocktype.name;
    newCell.style.verticalAlign= "middle";
    newCell.setAttribute('data-id', json.stocktype.id);

    newCell = newRow.insertCell();
    newCell.textContent = json.stocktype.unitname;
    newCell.style.verticalAlign= "middle";
    newCell.setAttribute('data-unitid', json.stocktype.unitid);

    addStockTypeTableButtonGroup(newRow, json);
}

/* End Stock Type Add Section*/

/* Stock Type Update Section*/
function openStockTypeUpdateModalClicked(id, name, unitid, subcatid)
{
    console.log('clicked' +Math.random());
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
    var table = document.getElementById("stocktypetable");

    //start i with 1 instead of 0 because we dont want to touch table header
    for (var i = 1; i < table.rows.length; i++)
    {
        if(table.rows[i].cells[0].dataset.id == json.stocktype.id)
        {
            table.rows[i].cells[0].textContent = json.stocktype.name;
            table.rows[i].cells[1].textContent = json.stocktype.unitname;
            table.rows[i].cells[1].setAttribute('data-unitid', json.stocktype.unitid);
            table.rows[i].deleteCell(2);

            addStockTypeTableButtonGroup(table.rows[i], json);
            break;
        }
    }
}
/* End Stock Type Update Section*/

/* Stock Type Delete Section*/
function openStockTypeDeleteModalClicked(id, name, unitid, subcatid)
{
    console.log('clicked' +Math.random());
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
    var table = document.getElementById("stocktypetable");

    //start i with 1 instead of 0 because we dont want to touch table header
    for (var i = 1; i < table.rows.length; i++)
    {
        if(table.rows[i].cells[0].dataset.id == json.id)
        {
            table.deleteRow(i);
            break;
        }
    }
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

function addStockColorTableButtonGroup(row, json)
{
    var newCell = row.insertCell();
    var div = document.createElement('div');
    newCell.appendChild(div);
    addClass(div, "form-row");

    var button1 = document.createElement("button");
    addClass(button1, "btn");
    addClass(button1, "btn-primary");
    button1.setAttribute('data-toggle', 'tooltip');
    button1.setAttribute('title', 'Malzeme Rengini Değiştir');
    button1.setAttribute('onclick', "openStockColorUpdateModalClicked('" + json.stockcolor.id + "','"+ json.stockcolor.name + "')");

    div.appendChild(button1);
    var ielement1 = document.createElement('i');
    addClass(ielement1, "fas");
    addClass(ielement1, "fa-external-link-alt");
    button1.appendChild(ielement1);

    var button2 = document.createElement("button");
    addClass(button2, "btn");
    addClass(button2, "btn-danger");
    button2.setAttribute('data-toggle', 'tooltip');
    button2.setAttribute('title', 'Malzeme Rengini Sil');
    button2.setAttribute('onclick', "openStockColorDeleteModalClicked('" + json.stockcolor.id + "','"+ json.stockcolor.name + "')");

    var span = document.createElement("span");
    span.style.display = "inline";
    span.style.width = "5px";
    div.appendChild(span);

    div.appendChild(button2);
    var ielement2 = document.createElement('i');
    addClass(ielement2, "fas");
    addClass(ielement2, "fa-trash");
    button2.appendChild(ielement2);
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
        addStockColorEntry(json);

        sCMDefaultCloseActions();
    }
    else if(json.responsecode === -1)
    {
        sCMShowAlert(json);
    }
}

function addStockColorEntry(json)
{
    var tbodyRef = document.getElementById('stockcolortable').getElementsByTagName('tbody')[0];

    var newRow = tbodyRef.insertRow();
    var newCell = newRow.insertCell();
    newCell.textContent = json.stockcolor.name;
    newCell.style.verticalAlign= "middle";
    newCell.setAttribute('data-id', json.stockcolor.id);

    addStockColorTableButtonGroup(newRow, json);
}
/* End Stock Color Add Section*/

/* Stock Color Update Section*/
function openStockColorUpdateModalClicked(id, name)
{
    console.log('clicked' +Math.random());
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
    var table = document.getElementById("stockcolortable");

    //start i with 1 instead of 0 because we dont want to touch table header
    for (var i = 1; i < table.rows.length; i++)
    {
        if(table.rows[i].cells[0].dataset.id == json.stockcolor.id)
        {
            table.rows[i].cells[0].textContent = json.stockcolor.name;
            table.rows[i].deleteCell(1);

            addStockColorTableButtonGroup(table.rows[i], json);
            break;
        }
    }
}
/* End Stock Color Update Section*/

/* Stock Color Delete Section*/
function openStockColorDeleteModalClicked(id, name)
{
    console.log('clicked' +Math.random());
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
    var table = document.getElementById("stockcolortable");

    //start i with 1 instead of 0 because we dont want to touch table header
    for (var i = 1; i < table.rows.length; i++)
    {
        if(table.rows[i].cells[0].dataset.id == json.id)
        {
            table.deleteRow(i);
            break;
        }
    }
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

function addStockPackageTableButtonGroup(row, json)
{
    var newCell = row.insertCell();
    var div = document.createElement('div');
    newCell.appendChild(div);
    addClass(div, "form-row");

    var button1 = document.createElement("button");
    addClass(button1, "btn");
    addClass(button1, "btn-primary");
    button1.setAttribute('data-toggle', 'tooltip');
    button1.setAttribute('title', 'Ambalaj Tipini Değiştir');
    button1.setAttribute('onclick', "openStockPackageUpdateModalClicked('" + json.stockpackage.id + "','"+ json.stockpackage.name + "')");

    div.appendChild(button1);
    var ielement1 = document.createElement('i');
    addClass(ielement1, "fas");
    addClass(ielement1, "fa-external-link-alt");
    button1.appendChild(ielement1);

    var button2 = document.createElement("button");
    addClass(button2, "btn");
    addClass(button2, "btn-danger");
    button2.setAttribute('data-toggle', 'tooltip');
    button2.setAttribute('title', 'Ambalaj Tipini Sil');
    button2.setAttribute('onclick', "openStockPackageDeleteModalClicked('" + json.stockpackage.id + "','"+ json.stockpackage.name + "')");

    var span = document.createElement("span");
    span.style.display = "inline";
    span.style.width = "5px";
    div.appendChild(span);

    div.appendChild(button2);
    var ielement2 = document.createElement('i');
    addClass(ielement2, "fas");
    addClass(ielement2, "fa-trash");
    button2.appendChild(ielement2);
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
        addStockPackageEntry(json);

        sPMDefaultCloseActions();
    }
    else if(json.responsecode === -1)
    {
        sPMShowAlert(json);
    }
}

function addStockPackageEntry(json)
{
    var tbodyRef = document.getElementById('stockpackagetable').getElementsByTagName('tbody')[0];

    var newRow = tbodyRef.insertRow();
    var newCell = newRow.insertCell();
    newCell.textContent = json.stockpackage.name;
    newCell.style.verticalAlign= "middle";
    newCell.setAttribute('data-id', json.stockpackage.id);

    addStockPackageTableButtonGroup(newRow, json);
}
/* End Stock Package Add Section*/

/* Stock Package Update Section*/
function openStockPackageUpdateModalClicked(id, name)
{
    console.log('clicked' +Math.random());
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
    var table = document.getElementById("stockpackagetable");

    //start i with 1 instead of 0 because we dont want to touch table header
    for (var i = 1; i < table.rows.length; i++)
    {
        if(table.rows[i].cells[0].dataset.id == json.stockpackage.id)
        {
            table.rows[i].cells[0].textContent = json.stockpackage.name;
            table.rows[i].deleteCell(1);

            addStockPackageTableButtonGroup(table.rows[i], json);
            break;
        }
    }
}
/* End Stock Package Update Section*/

/* Stock Package Delete Section*/
function openStockPackageDeleteModalClicked(id, name)
{
    console.log('clicked' +Math.random());
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
    var table = document.getElementById("stockpackagetable");

    //start i with 1 instead of 0 because we dont want to touch table header
    for (var i = 1; i < table.rows.length; i++)
    {
        if(table.rows[i].cells[0].dataset.id == json.id)
        {
            table.deleteRow(i);
            break;
        }
    }
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

function addCorporationTableButtonGroup(row, json)
{
    var newCell = row.insertCell();
    var div = document.createElement('div');
    newCell.appendChild(div);
    addClass(div, "form-row");

    var button1 = document.createElement("button");
    addClass(button1, "btn");
    addClass(button1, "btn-primary");
    button1.setAttribute('data-toggle', 'tooltip');
    button1.setAttribute('title', 'Şirketi Değiştir');
    button1.setAttribute('onclick', "openCorporationUpdateModalClicked('" + json.corporation.id + "','"+ json.corporation.name + "')");

    div.appendChild(button1);
    var ielement1 = document.createElement('i');
    addClass(ielement1, "fas");
    addClass(ielement1, "fa-external-link-alt");
    button1.appendChild(ielement1);

    var button2 = document.createElement("button");
    addClass(button2, "btn");
    addClass(button2, "btn-danger");
    button2.setAttribute('data-toggle', 'tooltip');
    button2.setAttribute('title', 'Şirketi Sil');
    button2.setAttribute('onclick', "openCorporationDeleteModalClicked('" + json.corporation.id + "','"+ json.corporation.name + "')");

    var span = document.createElement("span");
    span.style.display = "inline";
    span.style.width = "5px";
    div.appendChild(span);

    div.appendChild(button2);
    var ielement2 = document.createElement('i');
    addClass(ielement2, "fas");
    addClass(ielement2, "fa-trash");
    button2.appendChild(ielement2);
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
        addCorporationEntry(json);

        cMDefaultCloseActions();
    }
    else if(json.responsecode === -1)
    {
        cMShowAlert(json);
    }
}

function addCorporationEntry(json)
{
    var tbodyRef = document.getElementById('corporationtable').getElementsByTagName('tbody')[0];

    var newRow = tbodyRef.insertRow();
    var newCell = newRow.insertCell();
    newCell.textContent = json.corporation.name;
    newCell.style.verticalAlign= "middle";
    newCell.setAttribute('data-id', json.corporation.id);

    addCorporationTableButtonGroup(newRow, json);
}
/* End Corporation Add Section*/

/* Corporation Update Section*/
function openCorporationUpdateModalClicked(id, name)
{
    console.log('clicked' +Math.random());
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
    var table = document.getElementById("corporationtable");

    //start i with 1 instead of 0 because we dont want to touch table header
    for (var i = 1; i < table.rows.length; i++)
    {
        if(table.rows[i].cells[0].dataset.id == json.corporation.id)
        {
            table.rows[i].cells[0].textContent = json.corporation.name;
            table.rows[i].deleteCell(1);

            addCorporationTableButtonGroup(table.rows[i], json);
            break;
        }
    }
}
/* End Corporation Update Section*/

/* Corporation Delete Section*/
function openCorporationDeleteModalClicked(id, name)
{
    console.log('clicked' +Math.random());
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
    var table = document.getElementById("corporationtable");

    //start i with 1 instead of 0 because we dont want to touch table header
    for (var i = 1; i < table.rows.length; i++)
    {
        if(table.rows[i].cells[0].dataset.id == json.id)
        {
            table.deleteRow(i);
            break;
        }
    }
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

function addStockUnitTableButtonGroup(row, json)
{
    var newCell = row.insertCell();
    var div = document.createElement('div');
    newCell.appendChild(div);
    addClass(div, "form-row");

    var button1 = document.createElement("button");
    addClass(button1, "btn");
    addClass(button1, "btn-primary");
    button1.setAttribute('data-toggle', 'tooltip');
    button1.setAttribute('title', 'Malzeme Birimini Değiştir');
    button1.setAttribute('onclick', "openStockUnitUpdateModalClicked('" + json.stockunit.id + "','"+ json.stockunit.name +"','" + json.stockunit.precision + "')");

    div.appendChild(button1);
    var ielement1 = document.createElement('i');
    addClass(ielement1, "fas");
    addClass(ielement1, "fa-external-link-alt");
    button1.appendChild(ielement1);

    var button2 = document.createElement("button");
    addClass(button2, "btn");
    addClass(button2, "btn-danger");
    button2.setAttribute('data-toggle', 'tooltip');
    button2.setAttribute('title', 'Malzeme Birimini Sil');
    button2.setAttribute('onclick', "openStockUnitDeleteModalClicked('" + json.stockunit.id + "','"+ json.stockunit.name +"','" + json.stockunit.precision + "')");

    var span = document.createElement("span");
    span.style.display = "inline";
    span.style.width = "5px";
    div.appendChild(span);

    div.appendChild(button2);
    var ielement2 = document.createElement('i');
    addClass(ielement2, "fas");
    addClass(ielement2, "fa-trash");
    button2.appendChild(ielement2);
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
        addStockUnitEntry(json);

        sUMDefaultCloseActions();
    }
    else if(json.responsecode === -1)
    {
        sUMShowAlert(json);
    }
}

function addStockUnitEntry(json)
{
    var tbodyRef = document.getElementById('stockunittable').getElementsByTagName('tbody')[0];

    var newRow = tbodyRef.insertRow();
    var newCell = newRow.insertCell();
    newCell.textContent = json.stockunit.name;
    newCell.style.verticalAlign= "middle";
    newCell.setAttribute('data-id', json.stockunit.id);

    newCell = newRow.insertCell();
    newCell.textContent = json.stockunit.precision;
    newCell.style.verticalAlign= "middle";
    newCell.setAttribute('data-precision', json.stockunit.precision);

    addStockUnitTableButtonGroup(newRow, json);
}
/* End Stock Unit Add Section*/

/* Stock Unit Update Section*/
function openStockUnitUpdateModalClicked(id, name, precision)
{
    console.log('clicked' +Math.random());
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
    var table = document.getElementById("stockunittable");

    //start i with 1 instead of 0 because we dont want to touch table header
    for (var i = 1; i < table.rows.length; i++)
    {
        if(table.rows[i].cells[0].dataset.id == json.stockunit.id)
        {
            table.rows[i].cells[0].textContent = json.stockunit.name;
            table.rows[i].cells[1].textContent = json.stockunit.precision;
            table.rows[i].cells[1].setAttribute('data-precision', json.stockunit.precision);
            table.rows[i].deleteCell(2);

            addStockUnitTableButtonGroup(table.rows[i], json);
            break;
        }
    }
}
/* End Stock Unit Update Section*/

/* Stock Unit Delete Section*/
function openStockUnitDeleteModalClicked(id, name, precision)
{
    console.log('clicked' +Math.random());
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
    var table = document.getElementById("stockunittable");

    //start i with 1 instead of 0 because we dont want to touch table header
    for (var i = 1; i < table.rows.length; i++)
    {
        if(table.rows[i].cells[0].dataset.id == json.id)
        {
            table.deleteRow(i);
            break;
        }
    }
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
    var table = document.getElementById(id);
    while (table.rows.length > 1)
    {
        table.deleteRow(1);
    }
}