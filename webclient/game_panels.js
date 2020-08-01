$('.panel-holder').draggable({
    containment: "#panel-container",
    //grid: [50, 50],
    handle: $('.panel-controls')
}).resizable({
    containment: "#panel-container",
    minWidth: 170,
    minHeight: 130,
    autoHide: true
});

function addGenericWindow(){
    $('#panel-container').append(divTemplate)
    $('.panel-holder').draggable({
        containment: "#panel-container",
        //grid: [50, 50],
        handle: $('.panel-controls')
    }).resizable({
        containment: "#panel-container",
        minWidth: 170,
        minHeight: 130,
        autoHide: true
    });
}
var divTemplate = `<div class="panel-holder" class="div-panel">
<div class="panel-controls">
<button class="remove-panel" onclick="$(this).parent().parent().remove();">X</button>
</div>
<div class="panel", style="background-color: aqua;"></div>
</div>`