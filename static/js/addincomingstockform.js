$( document ).ready(function()
{
    sEMSetAction("incoming");
    $('#stockEntryModalActionButton').click(function()
    {
        stockEntryButtonSubmitAction();
    });
});

function openStockEntryModalForAdd()
{
    sEMOpenModal('add');
}

function openStockEntryModalForUpdate(id, stocktypeid, stockcolorid, stockunitid, stockquantity, stockpackageid, packagequantity, note)
{
    sEMSetInfoForUpdate(id, stocktypeid, stockcolorid, stockunitid, stockquantity, stockpackageid, packagequantity, note);
}

function openStockEntryModalForDelete(id, stocktypeid, stockcolorid, stockunitid, stockquantity, stockpackageid, packagequantity, note)
{
    sEMSetInfoForDelete(id, stocktypeid, stockcolorid, stockunitid, stockquantity, stockpackageid, packagequantity, note);
}

function stockEntryButtonSubmitAction()
{
    switch (sEMMode())
    {
        case "add":
            addstock();
            break;

        case "update":
            updatestock();
            break;

        case "delete":
            deletestock();
            break;
    }
}

function addstock()
{
    if(sEMCheckEntries())
    {
        var entryid = Date.now();

        var stocktype = document.getElementById('stocktype');
        var stockcolor = document.getElementById('stockcolor');
        var stockunit = document.getElementById('stockunit');
        var stockpackage = document.getElementById('stockpackage');
        var stockquantity = document.getElementById('stockquantity');
        var packagequantity = document.getElementById('packagequantity');
        var stocknote = document.getElementById('stocknote');

        var stocktypeid = getselecteddataid(stocktype.id);
        var stockcolorid = getselecteddataid(stockcolor.id);
        var stockunitid = getselecteddataid(stockunit.id);
        var stockpackageid = getselecteddataid(stockpackage.id);

        var tbodyRef = document.getElementById('stocktable').getElementsByTagName('tbody')[0];
        var newRow = tbodyRef.insertRow();

        var newCell = newRow.insertCell();
        newCell.style.verticalAlign= "middle";
        newCell.textContent = stocktype.options[stocktype.selectedIndex].textContent;
        newCell.setAttribute('data-id', stocktypeid);
        newCell.setAttribute('data-entryid', entryid);

        newCell = newRow.insertCell();
        newCell.style.verticalAlign= "middle";
        newCell.textContent = stockcolor.options[stockcolor.selectedIndex].textContent;
        newCell.setAttribute('data-id', stockcolorid);

        var precision = Number(stockunit.options[stockunit.selectedIndex].dataset.precision);
        var quantity = Number(stockquantity.value);

        newCell = newRow.insertCell();
        newCell.style.verticalAlign= "middle";
        newCell.textContent = quantity.toFixed(precision) + " " + stockunit.options[stockunit.selectedIndex].textContent;
        newCell.setAttribute('data-quantity', stockquantity.value);
        newCell.setAttribute('data-unitid', stockunitid);

        newCell = newRow.insertCell();
        newCell.style.verticalAlign= "middle";
        newCell.textContent = packagequantity.value + " " + stockpackage.options[stockpackage.selectedIndex].textContent;
        newCell.setAttribute('data-quantity', packagequantity.value);
        newCell.setAttribute('data-packageid', stockpackageid);

        newCell = newRow.insertCell();
        newCell.style.verticalAlign= "middle";
        newCell.textContent = stocknote.value;

        addStockEntryButtonGroup(entryid, newRow, stocktypeid, stockcolorid, stockunitid, stockquantity.value, stockpackageid, packagequantity.value, stocknote.value);

        sEMCloseModal();
    }
}

function updatestock()
{
    if(sEMCheckEntries())
    {
        var table = document.getElementById('stocktable');

        var stocktype = document.getElementById('stocktype');
        var stockcolor = document.getElementById('stockcolor');
        var stockunit = document.getElementById('stockunit');
        var stockpackage = document.getElementById('stockpackage');
        var stockquantity = document.getElementById('stockquantity');
        var packagequantity = document.getElementById('packagequantity');
        var stocknote = document.getElementById('stocknote');

        var stocktypeid = getselecteddataid(stocktype.id);
        var stockcolorid = getselecteddataid(stockcolor.id);
        var stockunitid = getselecteddataid(stockunit.id);
        var stockpackageid = getselecteddataid(stockpackage.id);


        //start i with 1 instead of 0 because we dont want to touch table header
        for (var i = 1; i < table.rows.length; i++)
        {
            if(table.rows[i].cells[0].dataset.entryid == sEMGetEntryId())
            {
                table.rows[i].cells[0].textContent = stocktype.options[stocktype.selectedIndex].textContent;
                table.rows[i].cells[0].setAttribute('data-id', stocktypeid);
                table.rows[i].cells[0].setAttribute('data-entryid', sEMGetEntryId());

                table.rows[i].cells[1].textContent = stockcolor.options[stockcolor.selectedIndex].textContent;
                table.rows[i].cells[1].setAttribute('data-id', stockcolorid);

                var precision = Number(stockunit.options[stockunit.selectedIndex].dataset.precision);
                var quantity = Number(stockquantity.value);

                table.rows[i].cells[2].textContent = quantity.toFixed(precision) + " " + stockunit.options[stockunit.selectedIndex].textContent;
                table.rows[i].cells[2].setAttribute('data-quantity', stockquantity.value);
                table.rows[i].cells[2].setAttribute('data-unitid', stockunitid);

                table.rows[i].cells[3].textContent = packagequantity.value + " " + stockpackage.options[stockpackage.selectedIndex].textContent;
                table.rows[i].cells[3].setAttribute('data-quantity', packagequantity.value);
                table.rows[i].cells[3].setAttribute('data-packageid', stockpackageid);

                table.rows[i].cells[4].textContent = stocknote.value;

                table.rows[i].deleteCell(5);

                addStockEntryButtonGroup(sEMGetEntryId(), table.rows[i], stocktypeid, stockcolorid, stockunitid, stockquantity.value, stockpackageid, packagequantity.value, stocknote.value);

                sEMCloseModal();
                break;
            }
        }

    }
}

function deletestock()
{
    var table = document.getElementById('stocktable');

    for (var i = 1; i < table.rows.length; i++)
    {
        if(table.rows[i].cells[0].dataset.entryid == sEMGetEntryId())
        {
            table.deleteRow(i);
            sEMCloseModal();
            break;
        }
    }
}

function addStockEntryButtonGroup(entryid, newRow, stocktypeid, stockcolorid, stockunitid, stockquantity, stockpackageid, packagequantity, note)
{
    var newCell = newRow.insertCell();
    newCell.style.verticalAlign= "middle";
    var div = document.createElement('div');
    newCell.appendChild(div);
    addClass(div, "form-row");

    var button1 = document.createElement("button");
    addClass(button1, "btn");
    addClass(button1, "btn-primary");
    button1.setAttribute('data-toggle', 'tooltip');
    button1.setAttribute('title', 'Malzemeyi Değiştir');
    button1.setAttribute('onclick', "openStockEntryModalForUpdate('" + entryid + "','" + stocktypeid + "','"+ stockcolorid +"','" + stockunitid + "','" + stockquantity + "','" + stockpackageid + "','" + packagequantity + "','" + note + "')");

    div.appendChild(button1);
    var ielement1 = document.createElement('i');
    addClass(ielement1, "fas");
    addClass(ielement1, "fa-external-link-alt");
    button1.appendChild(ielement1);

    var button2 = document.createElement("button");
    addClass(button2, "btn");
    addClass(button2, "btn-danger");
    button2.setAttribute('data-toggle', 'tooltip');
    button2.setAttribute('title', 'Malzemeyi Sil');
    button2.setAttribute('onclick', "openStockEntryModalForDelete('" + entryid + "','"  + stocktypeid + "','"+ stockcolorid +"','" + stockunitid + "','" + stockquantity + "','" + stockpackageid+ "','" + packagequantity + "','" + note + "')");

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

function uploadform()
{
    var danger = document.getElementById('dangeralert');
    danger.style.display = "none";
    var success = document.getElementById('successalert');
    success.style.display = "none";

    var formname = document.getElementById('formnameid');
    var corporation = document.getElementById('corporation');

    var corporationid = getselecteddataid(corporation.id);
    if(corporationid < 0)
    {
        danger.textContent  = "Lütfen malzemenin geldiği yeri seçin!";
        danger.style.display = "block";
        return;
    }

    var recorddateinput = document.getElementById('recorddate');
    var recorddate = recorddateinput.value;

    var incoingstockform = {};
    incoingstockform.name = formname.value;
    incoingstockform.corporationid = corporationid;
    incoingstockform.incomingstocks = [];
    incoingstockform.recorddate = recorddate;
    var table = document.getElementById("stocktable");

    for (var i = 1; i < table.rows.length; i++)
    {
       var stockentry = {};
       stockentry["stocktypeid"] = table.rows[i].cells[0].dataset.id;
       stockentry["stockcolorid"] = table.rows[i].cells[1].dataset.id;
       stockentry["quantity"] = table.rows[i].cells[2].dataset.quantity;
       stockentry["packagequantity"] = table.rows[i].cells[3].dataset.quantity;
       stockentry["stockpackageid"] = table.rows[i].cells[3].dataset.packageid;
       stockentry["stocknote"] = table.rows[i].cells[4].textContent;
       incoingstockform.incomingstocks.push(stockentry);
    }

    var request = new XMLHttpRequest();
    request.open("POST", "/addincomingstockform");
    request.setRequestHeader("Content-Type", "application/json");
    request.addEventListener("load", stockformentryListener);
    var jsondata = JSON.stringify(incoingstockform);
    request.send(jsondata);
}

function stockformentryListener()
{
    var json = JSON.parse(this.responseText);
    if(json.responsecode === 0)
    {
        var success = document.getElementById('successalert');
        var successheading = document.getElementById('successheading');
        var successmessage = document.getElementById('successmessage');
        var successpostmessage = document.getElementById('successpostmessage');

        successheading.textContent  = json.heading;
        successmessage.textContent  = json.message;
        successpostmessage.textContent  = json.postmessage;
        success.style.display = "block";

        var table = document.getElementById("stocktable");

        document.getElementById('formnameid').value = "";
        document.getElementById('recorddate').value = "";
        resetselect('corporation');

        cleartable(table.id);
    }
    else
    {
         var danger = document.getElementById('dangeralert');
         danger.textContent  = json.message;
         danger.style.display = "block";
    }
}

function cleartable(id)
{
    var table = document.getElementById(id);

    while (table.rows.length > 1)
    {
        table.deleteRow(1);
    }
}

function getselecteddataid(id)
{
    var select = document.getElementById(id);

    for (var i = 0; i < select.options.length; i++)
    {
        opt = select.options[i];
        if ( opt.selected === true )
        {
            return Number(opt.dataset.id);
        }
    }
    return -1;
}

