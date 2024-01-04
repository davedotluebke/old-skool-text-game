// display the page once Javascript access has been confirmed
document.getElementsByClassName('content')[0].classList.remove('hidden');

// cookie handling

function setCookie(cname, cvalue, exminutes) {
    var d = new Date();
    d.setTime(d.getTime() + (exminutes*60*1000));
    var expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return undefined;
}

// header and info section

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

// valid modes: plain, old-school, blue
var modes = ['plain', 'old-school', 'blue'];
var modeIdx = 0;
var currentMode = getCookie('mode');

function setMode(newMode) {
    for (var i = 0; i < modes.length; i++) {
        if (modes[i] == newMode) {
            // add the new mode to the background
            document.getElementsByClassName('background')[0].classList.add(modes[i]);
            document.getElementsByClassName('header')[0].classList.add(modes[i]);
            if (newMode == 'old-school') {
                document.getElementsByClassName('inputLine')[0].style = 'caret-shape: block';
            }
            modeIdx = i;
            setCookie('mode', newMode, 60*24*7*4);
        } else {
            // remove the old mode from the background
            document.getElementsByClassName('background')[0].classList.remove(modes[i]);
            document.getElementsByClassName('header')[0].classList.remove(modes[i]);
        }
    }
}

setMode(currentMode);

// console section
var converter = new showdown.Converter({simpleLineBreaks: true});
converter.setFlavor('github');
var cmd_history = [''];
var current_cmd = 0;
var state = 'MAKE_CONNECTION';
var ws = undefined;

window.onkeydown = function(e) {
    var key = e.key;
    if (document.activeElement != document.getElementsByClassName('inputLine')[0]) {
        // to not mess around with the file editing software
        return;
    }
    /*if (key == 'Tab') {
        document.getElementsByClassName('inputLine')[0].focus();
        e.preventDefault();
    } else */ if (key == 'Enter') {
        if (state != 'SEND_PASSWORD') {
            cmd_history[cmd_history.length-1] = document.getElementsByClassName('inputLine')[0].value;
            cmd_history.push('')
            current_cmd = cmd_history.length - 1;
        }
        sendLine()
        document.getElementsByClassName("inputLine")[0].value = cmd_history[current_cmd];
        e.preventDefault();
    } else if (key == 'ArrowUp') {
        if (current_cmd > 0) {
            cmd_history[current_cmd] = document.getElementsByClassName('inputLine')[0].value;
            current_cmd--;
            document.getElementsByClassName('inputLine')[0].value = cmd_history[current_cmd];
            e.preventDefault();
        }
    } else if (key == 'ArrowDown') {
        if (current_cmd < cmd_history.length - 1) {
            cmd_history[current_cmd] = document.getElementsByClassName('inputLine')[0].value;
            current_cmd ++;
            document.getElementsByClassName('inputLine')[0].value = cmd_history[current_cmd];
            e.preventDefault();
        }
    } else if (key == 'Escape') {
        modeIdx++;
        if (modeIdx >= modes.length) {
            modeIdx = 0;
        }
        setMode(modes[modeIdx])
        e.preventDefault();
    }
}

function receiveMessage(event) {
    var messagesOutput = document.getElementsByClassName('messageOutput')[0]
    var message = document.createElement('div')
    if (state == 'PLAY_GAME') {
        var msg = event.data;
        msg = JSON.parse(msg);
        if (msg['type'] == 'file') {
            receiveFile(msg['data'], msg['behaviour'], msg['filename']);
            return;
        }
        message.innerHTML = converter.makeHtml(msg['data']);
    }
    if (state == 'MAKE_CONNECTION') {
        message.innerHTML = event;
    }
    if (message.innerHTML.indexOf('--#quit') > -1) {
        message.innerHTML = message.innerHTML.replace('--#quit', 'Disconnected from server.')
        state = 'MAKE_CONNECTION';
        ws.close();
    }
    if (message.innerHTML.indexOf('--#password') > -1) {
        message.innerHTML = message.innerHTML.replace('--#password', 'password')
        state = 'SEND_PASSWORD';
        document.getElementsByClassName('inputLine')[0].type = 'password';
    }
    if (message.innerHTML.indexOf('--#upload') > -1) {
        message.innerHTML = message.innerHTML.replace('--#upload', 'upload')
        uploadFiles();
    }
    messagesOutput.appendChild(message);
    window.scrollTo(0,document.body.scrollHeight);
}

function encryptAndSend(message, type, filename) {
    if (type == undefined) {
        type = "command";
    }
    var data_dict = {"type": type, "data": message};
    if (filename != undefined) {
        data_dict['filename'] = filename;
    }
    var data = JSON.stringify(data_dict);
    try {
        ws.send(data);
    } catch {
        state = 'MAKE_CONNECTION';
        receiveMessage("Your connection was interrupted.")
    }
}

function openWebSocket(ip_address, port) {
    if (port == undefined) {
        port = "443";
    }
    setTimeout(receiveMessage,1,"Trying to connect to " + ip_address + "...");
    if (port == "443") {
        ws = new WebSocket("wss://" + ip_address + ":"+port+"/")
    } else {
        ws = new WebSocket("ws://" + ip_address + ":"+port+"/")
    }
    ws.binaryType = "arraybuffer";
    ws.onopen = function (event) {
        receiveMessage("Successfully connected to " + ip_address);
        if (port != "443") {
            receiveMessage("<b class='urgent'>Warning! This is an insecure connection! Do not send any passwords or credit cards or it may be stolen by attackers!</b>")
        }
        state = 'PLAY_GAME';
        ws.send('Connected!')
    };
    ws.onerror = function (event) {
        if (port === "443") {
            openWebSocket(ip_address, "9124");
        }
        else {
            setTimeout(receiveMessage,1,"No server was found at " + ip_address);
        }
    };
    // What to do when receiving a message
    ws.onmessage = receiveMessage;
}

function handleInput(user_input) {
    if (user_input.length == 0) {
        openWebSocket('server.firefile.us');
    } else if (user_input.split(":").length == 2) {
        openWebSocket(user_input.split(":")[0], user_input.split(":")[1]);
    } else {
        openWebSocket(user_input);
    }
}

// What to do when sending a message
function sendLine () {
    var user_input = document.getElementsByClassName("inputLine")[0].value,
        messages = document.getElementsByClassName('messageOutput')[0],
        message = document.createElement('div'),
        contentBlock = document.createElement('b');
    if (state != 'SEND_PASSWORD') {
        var content = document.createTextNode("> " + user_input);
    }
    else {
        var content = document.createTextNode("> ******");
    }
    if (state == 'PLAY_GAME') {
        encryptAndSend(user_input + '\n');
    }
    if (state == 'SEND_PASSWORD') {
        var hashed_key = new sjcl.hash.sha256();
        hashed_key.update(user_input);
        key_to_send = JSON.stringify(hashed_key);
        encryptAndSend(key_to_send);
        user_input = '';
        document.getElementsByClassName('inputLine')[0].type = 'text';
        state = 'PLAY_GAME';
    }
    if (state == 'MAKE_CONNECTION') {
        handleInput(user_input);
    }
    contentBlock.appendChild(content);
    message.appendChild(contentBlock);
    messages.appendChild(message);
    window.scrollTo(0,document.body.scrollHeight);
}

// handling file editing

var codeMirrorSettingsObj = {
    mode: "python",
    theme: "solarized dark",
    lineNumbers: true,
    autofocus: true
};
var codeEditor;

function displayEditor() {
    codeEditor = CodeMirror.fromTextArea(document.getElementsByClassName("codeEditorTextArea")[0], codeMirrorSettingsObj);
    codeEditor.setSize("100%", "100%");
    codeEditor.refresh();
}

displayEditor();

function fillEditor(fileContents, filename) {
    // first, check if something is already open, and if so, save it
    if (codeEditor.getDoc().getValue() != '') {
        saveCode();
    }
    codeEditor.getDoc().setValue(fileContents);
    document.getElementsByClassName('filename')[0].value = filename;
    if (document.getElementsByClassName('editor')[0].classList.contains('hidden')) {
        toggleSection('editor');
    }
    codeEditor.focus();

}

function saveCode() {
    encryptAndSend(codeEditor.getValue(), 'file', document.getElementsByClassName("filename")[0].value);
}

function receiveFile(file_contents, behaviour, filename) {
    if (filename === undefined) {
        filename = 'gamefile.py'
    }
    if (behaviour) {
        fillEditor(file_contents, filename);
        return;
    }
    var binaryData = [];
    binaryData.push(file_contents);
    const url = window.URL.createObjectURL(new Blob(binaryData, {type: "application/zip"}));
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    // TODO: the filename you want
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
}

function uploadFiles() {
    document.getElementsByClassName('fileInput').onchange = sendFile;
    document.getElementsByClassName('fileInput').click();
}

function sendFile() {
    var file = document.getElementsByClassName('fileInput')[0].files[0];
    if (file) {
        var reader = new FileReader();
        reader.fileName = file.name;
        reader.onload = function(e) {
            fileText = e.target.result;
            encryptAndSend(fileText, "file", e.target.fileName);
        }
        reader.readAsText(file);
    }
}

function startDefaultGame() {
    document.getElementsByClassName("inputLine")[0].value = "server.firefile.us";
    sendLine();
    document.getElementsByClassName("inputLine")[0].value = cmd_history[current_cmd];
    document.getElementsByClassName("defaultGameButton")[0].classList.add("hidden");
    document.getElementsByClassName("inputLine")[0].focus();
}

// final prep work

document.getElementsByClassName('inputLine')[0].focus();
toggleSection('editor');
window.scrollTo(0,0);
