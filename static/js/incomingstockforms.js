$(document).ready(function()
{
    $('.downloadBtn').click(function()
    {
        var formid = $(this).data('formid');
        window.open('/downloadincomingstockform/' + formid,'_blank');
    });

    $('.deleteBtn').click(function()
    {
        $('#stockFormDeleteModal').modal('show');
        var formid = $(this).data('formid');
        var modal = document.getElementById('stockFormDeleteModal');
        modal.dataset.id = formid;
    });

    getDataTable('stockformstable');
});

function openadvancedpdfmenu(formid)
{
    var pdfmodal = document.getElementById('pdfRowModal');
    pdfmodal.setAttribute('data-id', formid);
    $('#pdfRowModal').modal('show');
}

function downloadAdvanced()
{
    var rownumber = document.getElementById('rowinput').value;
    var formid = document.getElementById('pdfRowModal').dataset.id;
    $('#pdfRowModal').modal('hide');
    window.open('/downloadincomingstockform/' + formid + '/' + rownumber,'_blank');
}

function deleteForm()
{
    $('#stockFormDeleteModal').modal('hide');
    var modal = document.getElementById('stockFormDeleteModal');
    var formid = modal.dataset.id;
    var request = new XMLHttpRequest();
    request.open("DELETE", "/editincomingstockform/" + formid);
    request.setRequestHeader("Content-Type", "application/json");
    request.addEventListener("load", stockformdeleteListener);
    request.send("");
}

function stockformdeleteListener()
{
 var json = JSON.parse(this.responseText);

    if(json.responsecode === 0)
    {
        var table = document.getElementById('tablecontainer');
        table.style.display = "none";
        var success = document.getElementById('successalert');
        var successheading = document.getElementById('successheading');
        var successmessage = document.getElementById('successmessage');
        var successpostmessage = document.getElementById('successpostmessage');

        successheading.textContent  = json.heading;
        successmessage.textContent  = json.message;
        successpostmessage.textContent  = "Şimdi sayfa yenilenecektir";
        success.style.display = "block";

        setTimeout(() =>
        {
            window.location.replace("/incomingstockforms");
        }, 1250);
    }
    else if(json.responsecode === -1)
    {
         var danger = document.getElementById('dangeralert');
         danger.textContent  = json.message;
         danger.style.display = "block";
    }
}

function copyforminfoclicked(id)
{
    var request = new XMLHttpRequest();
    request.open("GET", "/copyincomingstockforminfo/" + id);
    request.setRequestHeader("Content-Type", "application/json");
    request.addEventListener("load", copyforminfolistener);
    request.send("");
}

function copyforminfolistener()
{
    var copyText = this.responseText;
    copyTextToClipboard(copyText);
}
function copyTextToClipboard(text) {
  if (!navigator.clipboard) {
    fallbackCopyTextToClipboard(text);
    return;
  }
  navigator.clipboard.writeText(text).then(function() {
    console.log('Async: Copying to clipboard was successful!');
  }, function(err) {
    console.error('Async: Could not copy text: ', err);
  });
}

function fallbackCopyTextToClipboard(text) {
  var textArea = document.createElement("textarea");
  textArea.value = text;

  // Avoid scrolling to bottom
  textArea.style.top = "0";
  textArea.style.left = "0";
  textArea.style.position = "fixed";

  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();

  try {
    var successful = document.execCommand('copy');
    var msg = successful ? 'successful' : 'unsuccessful';
    console.log('Fallback: Copying text command was ' + msg);
  } catch (err) {
    console.error('Fallback: Oops, unable to copy', err);
  }

  document.body.removeChild(textArea);
}


