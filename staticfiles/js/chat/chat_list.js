var searchInput = document.getElementById('name-input');
var suggestionsList = document.getElementById('suggestions');

// Get the users data from the json_script template variable
var usersData = JSON.parse(document.getElementById('users').textContent);
var current_user = document.getElementById('current-user').textContent;
var suggestions = usersData
    .filter(function (user) {
        return user.id != current_user;
    })
    .map(function (user) {
        return user.username;
    });

searchInput.addEventListener('input', function () {
    var searchValue = this.value.toLowerCase();
    var filteredSuggestions = getSuggestions(searchValue);

    renderSuggestions(filteredSuggestions);
});

function getSuggestions(searchValue) {
    return suggestions.filter(function (suggestion) {
        return suggestion.toLowerCase().startsWith(searchValue);
    });
}

function renderSuggestions(filteredSuggestions) {
    suggestionsList.innerHTML = '';

    filteredSuggestions.forEach(function (suggestion) {
        var li = document.createElement('li');
        li.textContent = suggestion;
        suggestionsList.appendChild(li);
    });

    if (filteredSuggestions.length > 0 && searchInput.value !== '') {
        suggestionsList.style.display = 'block';
    } else {
        suggestionsList.style.display = 'none';
    }
}

document.addEventListener('click', function (event) {
    if (!event.target.matches('#name-input')) {
        suggestionsList.style.display = 'none';
    }
});

suggestionsList.addEventListener('click', function (event) {
    if (event.target.matches('li')) {
        searchInput.value = event.target.textContent;
        suggestionsList.style.display = 'none';
    }
});

// Populating the chat lists
var chats = JSON.parse(document.getElementById('chats').textContent);
var chat_list = document.querySelector(".list");
if (chats.length) {
    chat_list.innerText = null;
    let new_div = document.createElement('div');
    new_div.classList.add('chat-item', 'my-1');
    chats.forEach((chat) => {
        let new_div = document.createElement('div');
        new_div.classList.add('chat-item', 'd-flex', 'align-items-center');
        let text = document.createElement('div');
        text.classList.add('ml-2');
        text.textContent = chat;
        new_div.appendChild(text);
        chat_list.appendChild(new_div);
    })
}

let chat_item = document.querySelectorAll(".chat-item");
chat_item.forEach(item=>{
    item.addEventListener('click', (event) => {
        let name = event.target.textContent;
        usersData.forEach(user => {
            if (name === user.username) {
                window.location.pathname = "/chat/" + user.id + "/";
            }
        });
    })
})
