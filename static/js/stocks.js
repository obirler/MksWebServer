$( document ).ready(function()
{
    $('#depotStockEntryModalActionButton').click(function()
    {
        stockEntryButtonSubmitAction();
    });
});

function openStockEntryModalForAdd()
{
    dSEMOpenModal('add');
}

function openStockEntryModalForUpdate(id, stocktypeid, stockcolorid, stockunitid, stockquantity)
{
    dSEMSetInfoForUpdate(id, stocktypeid, stockcolorid, stockunitid, stockquantity);
}

function openStockEntryModalForDelete(id, stocktypeid, stockcolorid, stockunitid, stockquantity)
{
    dSEMSetInfoForDelete(id, stocktypeid, stockcolorid, stockunitid, stockquantity);
}

function stockEntryButtonSubmitAction()
{
    switch (dSEMMode())
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
    if(dSEMCheckEntries())
    {
        var stocktype = document.getElementById('stocktype');
        var stockcolor = document.getElementById('stockcolor');
        var stockquantity = document.getElementById('stockquantity');

        var stocktypeid = getselecteddataid(stocktype.id);
        var stockcolorid = getselecteddataid(stockcolor.id);

        var stock = {};
        stock.stocktypeid = stocktypeid;
        stock.stockcolorid = stockcolorid;
        stock.stockquantity = stockquantity.value;

        var request = new XMLHttpRequest();
        request.open("POST", "/stocks");
        request.setRequestHeader("Content-Type", "application/json");
        request.addEventListener("load", stockEntryListener);
        var jsondata = JSON.stringify(stock);
        request.send(jsondata);
        dSEMCloseModal();
    }
}

function updatestock()
{
    if(dSEMCheckEntries())
    {
       var stocktype = document.getElementById('stocktype');
        var stockcolor = document.getElementById('stockcolor');
        var stockquantity = document.getElementById('stockquantity');

        var stocktypeid = getselecteddataid(stocktype.id);
        var stockcolorid = getselecteddataid(stockcolor.id);

        var stockid = dSEMGetEntryId();
        var stock = {};
        stock.id = stockid;
        stock.stocktypeid = stocktypeid;
        stock.stockcolorid = stockcolorid;
        stock.stockquantity = stockquantity.value;

        var request = new XMLHttpRequest();
        request.open("PATCH", "/stocks");
        request.setRequestHeader("Content-Type", "application/json");
        request.addEventListener("load", stockEntryListener);
        var jsondata = JSON.stringify(stock);
        request.send(jsondata);
        dSEMCloseModal();
    }
}

function deletestock()
{
    if(dSEMCheckEntries())
    {
        var stockid = dSEMGetEntryId();
        var stock = {};
        stock.id = stockid;

        var request = new XMLHttpRequest();
        request.open("DELETE", "/stocks");
        request.setRequestHeader("Content-Type", "application/json");
        request.addEventListener("load", stockEntryListener);
        var jsondata = JSON.stringify(stock);
        request.send(jsondata);
        dSEMCloseModal();
    }
}

function stockEntryListener()
{
    var json = JSON.parse(this.responseText);
    var danger = document.getElementById('dangeralert');
    if(json.responsecode === 0)
    {
        danger.style.display = "none";

        var success = document.getElementById('successalert');
        var successheading = document.getElementById('successheading');
        var successmessage = document.getElementById('successmessage');
        var successpostmessage = document.getElementById('successpostmessage');

        successheading.textContent = json.heading;
        successmessage.textContent = json.message;
        successpostmessage.textContent = json.postmessage;
        success.style.display = "block";

        setTimeout(() =>
        {
            window.location.replace("/stocks");
        }, 1000);
    }
    else
    {
         danger.textContent  = json.message;
         danger.style.display = "block";
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