$(document).ready(function() {
    const senderID = document.getElementById('senderId').value;
    loadChatUsers(senderID); // Načtení seznamu chatů
});

function loadChatUsers(senderId) {
    $.get(`/api/chat-users/${senderId}`, function(users) {
        const chatList = document.getElementById('chatList');
        chatList.innerHTML = ''; // Clear existing list
        users.forEach(user => {
            if (user.UserID !== parseInt(senderId)) { // Ensure not to include the sender's own chat
                const userItem = document.createElement('li');
                userItem.className = 'list-group-item list-group-item-action';
                userItem.setAttribute('data-recipient-id', user.UserID); // Store recipient ID
                userItem.textContent = user.FirstName + ' ' + user.LastName;
                userItem.onclick = function() {
                    selectChat(user.UserID);
                };
                chatList.appendChild(userItem);
            }
        });
        // Automatically select the first chat if available
        if (chatList.firstChild) {
            chatList.firstChild.click();
        }
    }).fail(function(jqXHR, textStatus, errorThrown) {
        console.error('Failed to load chat users:', textStatus, errorThrown);
    });
}

function selectChat(recipientId) {
    const senderId = document.getElementById('senderId').value;
    document.getElementById('recipientId').value = recipientId;
    loadMessages(senderId, recipientId);
}

function loadMessages(senderId, recipientId) {
    console.log("Loading messages from " + senderId + " to " + recipientId);
    $.get(`/api/messages/${senderId}/${recipientId}`, function(messages) {
        const messagesContainer = document.getElementById('messagesContainer');
        messagesContainer.innerHTML = '';
        messages.forEach(msg => {
            const msgElement = document.createElement('div');
            msgElement.textContent = `${msg.FirstName} ${msg.LastName}: ${msg.MessageText}`;
            messagesContainer.appendChild(msgElement);
        });
    }).fail(function(jqXHR, textStatus, errorThrown) {
        console.error('Error loading messages:', textStatus, errorThrown);
    });
}

function sendMessage() {
    const senderId = document.getElementById('senderId').value;
    const recipientId = document.getElementById('recipientId').value;
    const message = document.getElementById('messageInput').value;
    if (!message.trim()) {
        alert('Please enter a message.');
        return;
    }
    $.post('/api/send-message', { sender_id: senderId, recipient_id: recipientId, text: message }, function(response) {
        if (response.success) {
            document.getElementById('messageInput').value = '';
            loadMessages(senderId, recipientId);
        } else {
            alert('Error sending message: ' + response.message);
        }
    }).fail(function(jqXHR, textStatus, errorThrown) {
        console.log('AJAX call failed: ' + textStatus + ', ' + errorThrown);
    });
}
