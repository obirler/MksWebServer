$( document ).ready(function()
{
    $("#formStockFilterModalCloseBtn1").on("click", function(){
        $('#formStockFilterModal').modal('hide');
    });

    $("#formStockFilterModalCloseBtn2").on("click", function(){
        $('#formStockFilterModal').modal('hide');
    });

    $("#formStockFilterModalApply").on("click", function(){
        $('#formStockFilterModal').modal('hide');
        filterTable();
    });

    getDataTable();
});

function getDataTable()
{
    if ( $.fn.dataTable.isDataTable('#stockformstable'))
    {
        var table = $('#stockformstable').DataTable();
        return table;
    }
    else
    {
        var table = $('#stockformstable').DataTable(
        {
            language: {
                            "decimal":        ",",
                            "emptyTable":     "Tabloda herhangi bir veri mevcut değil",
                            "info":           "_TOTAL_ kayıttan _START_ - _END_ arasındaki kayıtlar gösteriliyor",
                            "infoEmpty":      "0 kayıttan 0 - 0 arasındaki kayıtlar gösteriliyor",
                            "infoFiltered":   "(_MAX_ kayıt içerisinden bulunan)",
                            "infoPostFix":    "",
                            "thousands":      "",
                            "lengthMenu":     "Sayfada _MENU_ kayıt göster",
                            "loadingRecords": "Yükleniyor...",
                            "processing":     "İşleniyor...",
                            "search":         "Ara:",
                            "zeroRecords":    "Eşleşen kayıt bulunamadı",
                            "paginate": {
                                "first":      "İlk",
                                "last":       "Son",
                                "next":       "Sonraki",
                                "previous":   "Önceki"
                            },
                            "aria": {
                                "sortAscending":  ": artan sütun sıralamasını aktifleştir",
                                "sortDescending": ": azalan sütun sıralamasını aktifleştir"
                            }
                     }
        });
        return table;
    }
}

function filterTable()
{
    clearfilterstack();
    var filtertable = document.getElementById('formStockFilterModalFilterTable');

    for (var line=1; line < filtertable.rows.length; line++)
    {
        var row = filtertable.rows[line];
        var cell = row.cells[1];
        var columnid = cell.dataset.columnid;
        var operatorid = cell.dataset.operatorid;
        var value1 = cell.dataset.value1;
        var value2 = cell.dataset.value2;
        addfilter(columnid, operatorid, value1, value2);
    }
    var table = getDataTable();
    table.draw();
}

function addfilter(columnid, operatorid, value1, value2)
{
    
    switch(columnid)
    {
        case "-1":
            break;
        case "1":
            operationfilter(operatorid, value1);
            break;
        case "2":
            stringcolumnfilter(1, operatorid, value1);
            break;
        case "3":
            stringcolumnfilter(2, operatorid, value1);
            break;
        case "4":
            numbercolumnfilter(3, operatorid, value1, value2);
            break;
        case "5":
            stringcolumnfilter(4, operatorid, value1);
            break;
        case "6":
            numbercolumnfilter(5, operatorid, value1, value2);
            break;
        case "7":
            stringcolumnfilter(6, operatorid, value1);
            break;
        case "8":
            stringcolumnfilter(7, operatorid, value1);
            break;
        case "9":
            stringcolumnfilter(8, operatorid, value1);
            break;
        case "10":
            stringcolumnfilter(9, operatorid, value1);
            break;
        case "11":
            stringcolumnfilter(10, operatorid, value1);
            break;
        case "12":
            stringcolumnfilter(11, operatorid, value1);
            break;
        case "13":
            stringcolumnfilter(12, operatorid, value1);
            break;
        case "14":
            stringcolumnfilter(13, operatorid, value1);
            break;
        case "15":
            datecolumnfilter(14, operatorid, value1, value2);
            break;
    }
}

function operationfilter(operatorid, value1)
{
    $.fn.dataTable.ext.search.push(
        function(settings, searchData, index, rowData, counter)
        {
            var table = document.getElementById("stockformstable");
            var row = table.rows[index];
            var cell = row.cells[0];
            var text = cell.dataset.title;
            if (typeof row == 'undefined')
            {
                return false;
            }
            switch(operatorid)
            {
                case "1":
                    return text === value1;
                case "2":
                    return text !== value1;
                case "3":
                    //case-insensitive search
                    return text.toLowerCase().includes(value1.toLowerCase());
                case "4":
                    return !text.toLowerCase().includes(value1.toLowerCase());
                case "5":
                    return text.toLowerCase().startsWith(value1.toLowerCase());
                case "6":
                    return !text.toLowerCase().startsWith(value1.toLowerCase());
                case "7":
                    return text.toLowerCase().endsWith(value1.toLowerCase());
                case "8":
                    return !text.toLowerCase().endsWith(value1.toLowerCase());
            }
            return false;
        }
    );
}

function stringcolumnfilter(colid, operatorid, value1)
{
    value1 = value1.toString();
    $.fn.dataTable.ext.search.push(
        function(settings, searchData, index, rowData, counter)
        {
            var text = searchData[colid];
            if (typeof text == 'undefined')
            {
                return false;
            }
            switch(operatorid)
            {
                case "1":
                    return text === value1;
                case "2":
                    return text !== value1;
                case "3":
                    //case-insensitive search
                    return text.toLowerCase().includes(value1.toLowerCase());
                case "4":
                    //case-insensitive search
                    return !text.toLowerCase().includes(value1.toLowerCase());
                case "5":
                    return text.toLowerCase().startsWith(value1.toLowerCase());
                case "6":
                    return !text.toLowerCase().startsWith(value1.toLowerCase());
                case "7":
                    return text.toLowerCase().endsWith(value1.toLowerCase());
                case "8":
                    return !text.toLowerCase().endsWith(value1.toLowerCase());
            }
            return false;
        }
    );
}

function numbercolumnfilter(colid, operatorid, value1, value2)
{
    value1 = parseFloat(value1);
    value2 = parseFloat(value2);
    $.fn.dataTable.ext.search.push(
        function(settings, searchData, index, rowData, counter)
        {
            var number = parseFloat(searchData[colid]);
            if (typeof number == 'undefined')
            {
                return false;
            }

            switch(operatorid)
            {
                case "1":
                    return number === value1;
                case "2":
                    return number !== value1;
                case "3":
                    //case-insensitive search
                    return number.toString().toLowerCase().includes(value1.toLowerCase());
                case "4":
                    //case-insensitive search
                    return !number.toString().toLowerCase().includes(value1.toLowerCase());
                case "5":
                    return number.toString().toLowerCase().startsWith(value1.toLowerCase());
                case "6":
                    return !number.toString().toLowerCase().startsWith(value1.toLowerCase());
                case "7":
                    return number.toString().toLowerCase().endsWith(value1.toLowerCase());
                case "8":
                    return !number.toString().toLowerCase().endsWith(value1.toLowerCase());
                case "9":
                    return number > value1;
                case "10":
                    return number >= value1;
                case "11":
                    return number < value1;
                case "12":
                    return number <= value1;
                case "13":
                    return number > value1 && number < value2;
                case "14":
                    return number <= value1 || number >= value2;
            }
            return false;
        }
    );
}

function datecolumnfilter(colid, operatorid, value1, value2)
{
    $.fn.dataTable.ext.search.push(
        function(settings, searchData, index, rowData, counter)
        {
            var datestr = searchData[colid];
            if (typeof datestr == 'undefined')
            {
                return false;
            }
            switch(operatorid)
            {
                case "1":
                    value1 = new Date(value1);
                    return getDateTimeFromTableString(datestr).getTime() === value1.getTime();
                case "2":
                    value1 = new Date(value1);
                    return getDateTimeFromTableString(datestr).getTime() !== value1.getTime();
                case "3":
                    //case-insensitive search
                    return datestr.toLowerCase().includes(value1.toString().toLowerCase());
                case "4":
                    //case-insensitive search
                    return !datestr.toLowerCase().includes(value1.toString().toLowerCase());
                case "5":
                    return datestr.toLowerCase().startsWith(value1.toString().toLowerCase());
                case "6":
                    return !datestr.toLowerCase().startsWith(value1.toString().toLowerCase());
                case "7":
                    return datestr.toLowerCase().endsWith(value1.toString().toLowerCase());
                case "8":
                    return !datestr.toLowerCase().endsWith(value1.toString().toLowerCase());
                case "9":
                    value1 = new Date(value1);
                    return getDateTimeFromTableString(datestr).getTime() > value1.getTime();
                case "10":
                    value1 = new Date(value1);
                    return getDateTimeFromTableString(datestr) >= value1.getTime();
                case "11":
                    value1 = new Date(value1);
                    return getDateTimeFromTableString(datestr).getTime() < value1.getTime();
                case "12":
                    value1 = new Date(value1);
                    return getDateTimeFromTableString(datestr).getTime() <= value1.getTime();
                case "13":
                    value1 = new Date(value1);
                    value2 = new Date(value2);
                    return getDateTimeFromTableString(datestr).getTime() > value1.getTime() && getDateTimeFromTableString(datestr).getTime() < value2.getTime();
                case "14":
                    value1 = new Date(value1);
                    value2 = new Date(value2);
                    return getDateTimeFromTableString(datestr).getTime() <= value1.getTime() || getDateTimeFromTableString(datestr).getTime() >= value2.getTime();
            }
            return false;
        }
    );
}

function getDateTimeFromTableString(str)
{
    var dtparts = str.split(" ");
    var datepart = dtparts[0];
    var timepart = dtparts[1];

    var dparts = datepart.split("-");
    var date = parseInt(dparts[0]);
    var month = parseInt(dparts[1]);
    var year = parseInt(dparts[2]);

    var tparts = timepart.split(":");
    var hour = parseInt(tparts[0]);
    var minute = parseInt(tparts[1]);
    var second = parseInt(tparts[2]);

    var datetime = new Date(year, month-1, date, hour, minute, second, 0);
    return datetime;
}

function clearfilterstack()
{
    while($.fn.dataTable.ext.search.length > 0)
    {
        $.fn.dataTable.ext.search.pop();
    }
}
