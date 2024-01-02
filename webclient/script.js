// display the page once Javascript access has been confirmed
document.getElementsByClassName('content')[0].classList.remove('hidden')

function toggleSection(sectionClass) {
    // toggle the visibility of a section
    if (document.getElementsByClassName(sectionClass)[0].classList.contains('hidden')) {
        document.getElementsByClassName(sectionClass)[0].classList.remove('hidden');
        document.getElementsByClassName(sectionClass + 'ToggleButton')[0].innerHTML = "Hide " + sectionClass.charAt(0).toUpperCase() + sectionClass.slice(1);
    } else {
        document.getElementsByClassName(sectionClass)[0].classList.add('hidden');
        document.getElementsByClassName(sectionClass + 'ToggleButton')[0].innerHTML = "Show " + sectionClass.charAt(0).toUpperCase() + sectionClass.slice(1);
    }
}
function setMode(newMode) {
    // valid modes: plain, old-school
    var modes = ['plain', 'old-school', 'blue'];
    for (var i = 0; i < modes.length; i++) {
        if (modes[i] == newMode) {
            // add the new mode to the background
            document.getElementsByClassName('background')[0].classList.add(modes[i]);
        } else {
            // remove the old mode from the background
            document.getElementsByClassName('background')[0].classList.remove(modes[i]);
        }
    }
}
