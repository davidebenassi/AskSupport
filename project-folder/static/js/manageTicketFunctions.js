function openChatModal(ticketId, ticketTitle, ticketDescription, canWrite) {
       
    document.getElementById('modalTicketTitle').textContent = ticketTitle;
    document.getElementById('modalTicketDesc').textContent = ticketDescription;
    document.getElementById('chatTicketId').value = ticketId;

    // AJAX request to get messages //
    fetch(`/tickets/${ticketId}/messages/`)
        .then(response => response.json())
        .then(data => {
            const chatMessages = document.getElementById('chatMessages');
            chatMessages.innerHTML = ''; 

            data.messages.forEach(message => {
                const messageElement = document.createElement('div');
                messageElement.classList.add('mb-2');
                messageElement.innerHTML = `<strong>${message.sender__username}</strong> <small>(${formatDate(message.timestamp)})</small>: ${message.content}`;
                chatMessages.appendChild(messageElement);
            });

            chatMessages.scrollTop = chatMessages.scrollHeight;

            const chatForm = document.getElementById('chatForm');
            if (canWrite) {
                chatForm.style.display = 'block';

                chatForm.addEventListener('submit', function(event) {
                    event.preventDefault();

                    const formData = new FormData(this);

                    fetch(`/tickets/${ticketId}/send_message/`, {
                        method: 'POST',
                        body: formData
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            updateChatMessages(ticketId);
                            document.getElementById('chatMessageContent').value = '';                                
                        }
                    });
                });
            } 
            else {
                chatForm.style.display = 'none';
            }   

            // Open modal //
            const chatModal = new bootstrap.Modal(document.getElementById('chatModal'));
            chatModal.show();
        });
}

function updateChatMessages(ticketId) {
    fetch(`/tickets/${ticketId}/messages/`)
        .then(response => response.json())
        .then(data => {
            const chatMessages = document.getElementById('chatMessages');
            chatMessages.innerHTML = '';

            data.messages.forEach(message => {
                const messageElement = document.createElement('div');
                messageElement.classList.add('mb-2');
                messageElement.innerHTML = `<strong>${message.sender__username}</strong> <small>(${formatDate(message.timestamp)})</small>: ${message.content}`;
                chatMessages.appendChild(messageElement);
            });

            // Scrolla alla fine dei messaggi
            chatMessages.scrollTop = chatMessages.scrollHeight;
        })
        .catch(error => {
            console.error('Error fetching messages:', error);
        });
}

function submitCloseForm(ticketId) {
    var reason = prompt("Please enter the close reason:");
    if (reason !== null && reason.trim() !== "") {
        document.getElementById('close-reason-' + ticketId).value = reason;
        document.getElementById('close-ticket-form-' + ticketId).submit();
    } else {
        alert("You must provide a reason to close the ticket.");
    }
}