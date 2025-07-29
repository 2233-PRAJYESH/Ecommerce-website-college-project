// Populating chat area with messages
const user2 = document.querySelector("#user2").textContent
var recepient = document.querySelector(".user-2")
recepient.textContent = user2.slice(1, user2.length - 1)
recepient = user2.slice(1, user2.length - 1)
const roomName = JSON.parse(document.getElementById('room-name').textContent);
var chat_area = document.querySelector(".chat-area")

if (roomName) {
    var chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/chat/'
        + roomName
        + '/'
    );

    chatSocket.onmessage = function (e) {
        const messages = JSON.parse(e.data);
        if (Array.isArray(messages)) {
            chat_area.innerHTML = null;
            messages.forEach((message) => {
                add_message_to_dom(message.message_content, message.sender, message.timestamp)
            })
        }
        else {
            add_message_to_dom(messages.message_content, messages.sender, messages.timestamp)
        }
    };

    chatSocket.onclose = function (e) {
        console.error('Chat socket closed unexpectedly');
    };

}

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function (e) {
    if (e.key === 'Enter') {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function (e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    messageInputDom.value = '';     // Clearing the input field after sending message
    let query_param = new URLSearchParams(document.location.search);
    if (query_param.size) {
        window.location = window.location.href.split('?')[0];
    }
};

function add_message_to_dom(message, sender, time) {
    var linkRegex = /(http[s]?:\/\/[^\s]+)/g;
    var containsLink = message.match(linkRegex);

    let new_div = document.createElement('div');
    new_div.classList.add('message', 'mx-2', 'mt-1');
    if (sender === recepient) {
        new_div.classList.add('align-self-start', 'receiver');
    }
    else {
        new_div.classList.add('align-self-end', 'sender');
    }
    let text = document.createElement('div');
    text.classList.add('m-2');
    let timeElement = document.createElement('p');
    timeElement.classList.add('text-right');
    timeElement.innerText = time.slice(11);
    timeElement.style = "font-size:x-small; margin:0 5px 0 0;"
    
    if (containsLink) {
        // Replace the link text with an <a> tag
        var replacedMessage = message.replace(linkRegex, '<a href="$1">$1</a>');
        text.innerHTML = replacedMessage;
    } else {
        // If no link found, render the message as normal text
        text.innerText = message;
    }
    // text.innerText = message;
    
    new_div.appendChild(text);
    new_div.appendChild(timeElement);
    chat_area.appendChild(new_div);
}

chat_item = document.querySelectorAll('.chat-item');
chat_item.forEach(item => {
    if (item.textContent == recepient) {
        item.style.backgroundColor = "#ddd";
    }
})

let query_param = new URLSearchParams(document.location.search);
if (query_param.size > 0) {
    let url = query_param.get('share');
    if (url) {
        let urlWithoutQS = window.location.origin + '/product/' + url;
        let message = "Check out this cool product! \n";
        document.querySelector('#chat-message-input').value = message + urlWithoutQS;
    }
    else {
        url = query_param.get('wishlist_id');
        urlWithoutQS = window.location.origin + '/wishlist/' + url;
        message = "Check out my wishlist! \n";
        document.querySelector('#chat-message-input').value = message + urlWithoutQS;
    }
}