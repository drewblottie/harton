var chars = [];
var locs = [];
var items = [];
var quests = [];
function loadHome()
{
    clearTables();
    hideTables();
}


function loadLocs(id)
{   
    loadHome();
    showLocsTable();
    showCharsTable();
    loadChars(id)
    $.getJSON('locations.json', function (data) {
    $.each(data.data, function(i, f) {
         if(f.location_id==id || f.id==id){
         var tblRow = "<tr>" + "<td>" + f.name + "</td>" +
         "<td>" + f.id + "</td>" + "<td>" + f.location_id + "</td>" + "<td><a href=" + f.urls.view + "> " +  f.urls.view + " </a></td>" 
         + "<td>" + "   " + "<button data-name=" + f.id +" onclick=loadLocs("+f.id+")>Select Location</button>" + "</td>" + "</tr>";
    $(tblRow).appendTo(".locstable tbody");}}
  );

 });
};




function loadChars(id)
{
    
    clearCharsTable();
    $.getJSON('treemap.json', function (data) {
        $.each(data.data, function(i, f) {
            if (f.parentid == id && f.type=="Character"){
                var tblRow = "<tr>" + "<td>" + f.name + "</td>" +
                "<td>" + f.name + "</td>" + "<td>" + f.name + "</td>" + "<td><a href=" + f.url + "> " +  f.url + " </a></td>" + "<td>" + f.is_dead + "</td>"
                 + "</tr>";
                $(tblRow).appendTo(".charstable tbody");
            }
        }
      );
 
    });
}






function loadQuests()
  { 
        loadHome();
        showQuestsTable();
        $.getJSON('quests.json', function (data) {
         $.each(data.data, function(i, f) {
              //if(f.name==qname)
              var tblRow = "<tr>" + "<td>" + f.name + "</td>" + "<td><a href=" + f.urls.view + "> " +  f.urls.view + " </a></td>" 
              + "<td>" + f.is_completed + "</td>" + "</tr>";
         $(tblRow).appendTo(".queststable tbody");}
       );
  
      });
    };

function loadItems()
  {   $.getJSON('items.json', function (data) {
         $.each(data.data, function(i, f) {
              //if(f.name==qname)
              var tblRow = "<tr>" + "<td>" + f.name + "</td>" +
              "<td>" + f.id + "</td>" + "<td>" + f.location_id + "</td>" + "<td><a href=" + f.urls.view + "> " +  f.urls.view + " </a></td>" + "<td>" + f.name + "</td>" + "<td>" + f.name + "</td>"
              + "<td>" + "   " + "<button onclick=deleteRow(this)>Delete</button>" + "</td>" + "</tr>";
         $(tblRow).appendTo(".itemstable tbody");}
       );
  
      });
    };


function clearTables()
{
    clearCharsTable()
    clearLocsTable()
    clearQuestsTable()
    clearItemsTable()
}    
    
function clearCharsTable()
{
    $(".charstable tbody tr").remove()
}
function clearLocsTable()
{
    $(".locstable tbody tr").remove()
}
function clearQuestsTable()
{
    $(".queststable tbody tr").remove()
}
function clearItemsTable()
{
    $(".itemstable tbody tr").remove()
}

function hideTables()
{
    hideCharsTable()
    hideLocsTable()
    hideQuestsTable()
    hideItemsTable()
}
function hideCharsTable()
{
    $(".charstable").hide()
    $(".CharHeader").hide()
}
function hideLocsTable()
{
    $(".locstable").hide()
    $(".LocHeader").hide()
    $(".getlocsbutton").hide()
}
function hideQuestsTable()
{
    $(".queststable").hide()
    $(".QuestHeader").hide()
}
function hideItemsTable()
{
    $(".itemstable").hide()
    $(".ItemHeader").hide()
}





function showTables()
{
    showCharsTable()
    showLocsTable()
    showQuestsTable()
    showItemsTable()
}
function showCharsTable()
{
    $(".charstable").show()
    $(".CharHeader").show()
}
function showLocsTable()
{
    $(".locstable").show()
    $(".LocHeader").show()
    $(".getlocsbutton").show()
}
function showQuestsTable()
{
    $(".queststable").show()
    $(".QuestHeader").show()
}
function showItemsTable()
{
    $(".itemstable").show()
    $(".ItemHeader").show()
}







function deleteRow(btndel) 
{
    
    $(btndel).closest("tr").remove();
    
}
function loadlocs()
{

}
