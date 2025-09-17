const modalBody = document.querySelector('.modal-body');
const newGroup = document.getElementById('new-group');
const form = document.getElementsByClassName('form-wrapper')[0];
const current_user = document.getElementById('current-user').textContent.slice(1, -1);
var groupsData = JSON.parse(document.getElementById('groups').textContent);

const addModalBody = async () => {
    const usersResponse = await fetch('http://127.0.0.1:8000/chat/api/getusers/');
    const users = await usersResponse.json();
    group_name = '';
    
    users.forEach(user => {
        const checkbox = document.createElement('input');
        checkbox.classList.add('form-check-input');
        checkbox.type = 'checkbox';
        checkbox.name = 'users';
        checkbox.id = user.username;
        checkbox.value = user.username;
        if (user.username === current_user) {
            checkbox.setAttribute('checked', 'true');
            checkbox.setAttribute('disabled', 'true');
        }

        const label = document.createElement('label');
        label.setAttribute('for', user.username)
        label.textContent = user.username;
        label.classList.add('form-check-label');

        const div = document.createElement('div');
        div.classList.add('form-check');
        div.appendChild(checkbox);
        div.appendChild(label);
        
        form.appendChild(div);
    });

}

addModalBody();

// Send selected users to server to create group
function selectedUsers() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const checkboxes = document.querySelectorAll('input[name="users"]:checked');
    const users = Array.from(checkboxes).map(checkbox => checkbox.value);
    var group_name = document.querySelector("#group-name").value;
    fetch('http://127.0.0.1:8000/chat/api/creategroup/', {
        method: "POST",
        body: JSON.stringify({
            users: users,
            group_name: group_name
        }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    });
    document.getElementsByClassName('close')[0].click();
}

let chat_item = document.querySelectorAll(".chat-item");
chat_item.forEach(item=>{
    item.addEventListener('click', (event) => {
        let name = event.target.textContent.trim();
        groupsData.forEach(group => {
            if (name === group) {
                window.location.pathname = "/chat/group/chat/" + group + "/";
            }
        });
    })
})

const groupName = JSON.parse(document.getElementById('current-group').textContent);
var chat_area = document.querySelector(".chat-area");
let title = document.querySelector('#title');
title.innerText = groupName;

if (groupName) {
    var chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/chat/group/'
        + groupName
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

    let senderElement = document.createElement('p');
    senderElement.textContent = sender;
    senderElement.style = "font-size:x-small; margin:0 5px 0 0;"
    
    let new_div = document.createElement('div');
    new_div.classList.add('message', 'mx-2', 'mt-1');
    if (sender === current_user) {
        senderElement.classList.add('text-right');
        new_div.classList.add('align-self-end', 'sender');
    }
    else {
        senderElement.classList.add('text-left');
        new_div.classList.add('align-self-start', 'receiver');
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
    
    new_div.appendChild(senderElement);
    new_div.appendChild(text);
    new_div.appendChild(timeElement);
    chat_area.appendChild(new_div);
}

chat_item = document.querySelectorAll('.chat-item');
chat_item.forEach(item => {
    if (item.textContent.trim() == groupName) {
        item.style.backgroundColor = "#ddd";
    }
})