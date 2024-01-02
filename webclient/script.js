function setMode(newMode) {
    // valid modes: plain, old-school
    var modes = ['plain', 'old-school']
    for (var i = 0; i < modes.length; i++) {
        if (modes[i] == newMode) {
            // add the new mode to the background
            document.getElementsByClassName('background')[0].classList.add(modes[i])
        } else {
            // remove the old mode from the background
            document.getElementsByClassName('background')[0].classList.remove(modes[i])
        }
    }
}
