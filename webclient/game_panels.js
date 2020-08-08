var heightLock;

window.onload = function(e) {
    heightLock = document.getElementsByClassName("initial-column")[0].offsetHeight;
}

function calibrateWindowing() {
    $('.column').sortable({
        containment: ".panel-container",
        connectWith: ".column",
        //grid: [50, 50],
        handle: $('.panel-controls'),
        stack: $('.panel-holder'),
    });
    $('.column').resizable({
        containment: ".panel-container",
        minWidth: 170,
        minHeight: heightLock,
        handles: "e",
        start: function (event, ui) {
            // just remember the total width of self + neighbor
            var widthArray = [];
            var nextElement = ui.element;
            var widthSoFar = ui.originalSize.width;
            var elemLoopNum = nextElement.nextAll().length;
            for (var i = 0; i < elemLoopNum; i++) {
                nextElement = nextElement.next();
                widthSoFar = widthSoFar + nextElement.outerWidth();
                widthArray.push(widthSoFar);
            }
            this.widthsWithNeighbors = widthArray;
        },
        resize: function (event, ui) {
            // then simply subtract it!
            var widthIndex = 0;
            var elem = ui.element.next();
            while (elem.nextAll().length > 0 && elem.outerWidth() <= 170) {
                widthIndex += 1;
                elem = elem.next();
            }
            var prevElemWidths = ui.size.width + 170*widthIndex;
            if (elem.nextAll().length <= 0 && this.widthsWithNeighbors[widthIndex] - prevElemWidths <= 170) {
                ui.element.width(this.widthsWithNeighbors[widthIndex] - (ui.element.nextAll().length)*170);
                elem.width(170); //this.widthsWithNeighbors[widthIndex] - (ui.size.width + 170*widthIndex));
            }
            else {
                elem.width(this.widthsWithNeighbors[widthIndex] - prevElemWidths);
            }
        },
        stop: function(event, ui) {
            // clean up, is this needed?
            delete this.widthsWithNeighbors;
        }
    });
}

function resetColumnSize() {
    for (var i = 0; i < document.getElementsByClassName("column").length; i++) {
        delete document.getElementsByClassName("column").i.style.width;
    }
}

function addGenericWindow(){
    try {
        $('.initial-column').append(`<div class="panel-holder div-panel">
        <div class="panel-controls">
        <button class="remove-panel" onclick="$(this).parent().parent().remove();">X</button>
        </div>
        <iframe class="panel" src="${$("#windowType").val()}"></div>
        </div>`);
        calibrateWindowing();
    } catch (err) {
        console.log('Invalid option:', $("#windowType").val());
    }
}