document.getElementById('send-button').addEventListener('click', handleFileUpload);
document.getElementById('refresh-button').addEventListener('click', clear);

function handleFileUpload() {
    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];

    if (file) {
        const formData = new FormData();
        formData.append('file', file);
        fetch('http://127.0.0.1:5000/parse-email', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    console.log(data)
                    appendEmail(data.response);
                }
            })
            .catch(error => console.error('Error:', error));

        fetch('http://127.0.0.1:5000/upload-email', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    appendMessage('bot', data.response);
                    switchToChatInput();
                }
            })
            .catch(error => console.error('Error:', error));
    }
}

function appendMessage(sender, message) {
    const chatMessages = document.getElementById('chat-messages');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender);
    const contentElement = document.createElement('div');
    contentElement.classList.add('content');
    if (message['ACTION'] === "CREATE_MEETING") {
        contentElement.innerHTML = prepareHtmlForMeeting(message)
    } else if (message['ACTION'] === "ANSWER_MAIL") {
        contentElement.innerHTML = prepareHtmlForAnswer(message)
    } else if (message['ACTION'] === "READ_MAIL") {
        contentElement.innerHTML = prepareHtmlForRead(message)
    } else if (message['ACTION'] === "USER_ACTION_NEEDED") {
        contentElement.innerHTML = prepareHtmlForAction(message)
    } else {

        contentElement.textContent = message;
    }
    messageElement.appendChild(contentElement);
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function appendEmail(email_content) {
    const chatMessages = document.getElementById('chat-messages');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', 'user');
    const contentElement = document.createElement('div');
    contentElement.classList.add('content');
    contentElement.innerHTML = `
        <div style="font-family: Arial, sans-serif; line-height: 1.6;">
            <h2>Email</h2>
            <p><strong>Betreff:</strong> ${email_content.Subject}</p>
            <p><strong>Datum:</strong> ${email_content.Date}</p>
            <p><strong>From:</strong> ${email_content.From}</p>
            <p><strong>To:</strong> ${email_content.To}</p>
            <p><strong>Content:</strong> ${email_content.Body}</p>
        </div>
    `;
    messageElement.appendChild(contentElement);
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function prepareHtmlForRead(message) {
    const content = message['CONTENT'].map(item => `<p>${item}</p>`).join('');
    return `
        <div style="font-family: Arial, sans-serif; line-height: 1.6;">
            <h2>Zusammenfassung der Mail</h2>
            <div>${content}</div>
        </div>
    `;
}

function prepareHtmlForAction(message) {
    const content = message['CONTENT'].map(item => `<p>${item}</p>`).join('');
    return `
        <div style="font-family: Arial, sans-serif; line-height: 1.6;">
            <h2>Folgende Aktion sind notwendig:</h2>
            <div>${content}</div>
        </div>
    `;
}

function prepareHtmlForMeeting(message) {
    const content = message['CONTENT'];
    const startDate = new Date(`${content.Datum}T${content.Uhrzeit}:00`);
    const endDate = new Date(startDate.getTime() + 60 * 60 * 1000); // add one hour

    const formatDate = (date) => {
        const year = date.getUTCFullYear().toString().padStart(4, '0');
        const month = (date.getUTCMonth() + 1).toString().padStart(2, '0');
        const day = date.getUTCDate().toString().padStart(2, '0');
        const hours = date.getUTCHours().toString().padStart(2, '0');
        const minutes = date.getUTCMinutes().toString().padStart(2, '0');
        const seconds = date.getUTCSeconds().toString().padStart(2, '0');
        return `${year}${month}${day}T${hours}${minutes}${seconds}Z`;
    };

    const startDateTime = formatDate(startDate);
    const endDateTime = formatDate(endDate);
    const icsContent = `
        BEGIN:VCALENDAR
        VERSION:2.0
        PRODID:-//Your Organization//Your Product//EN
        CALSCALE:GREGORIAN
        BEGIN:VEVENT
        UID:${new Date().getTime()}@yourdomain.com
        SUMMARY:${content.Betreff}
        DTSTART:${startDateTime}
        DTEND:${endDateTime}
        LOCATION:${content.Ort}
        DESCRIPTION:${content.Beschreibung}
        STATUS:CONFIRMED
        SEQUENCE:0
        TRANSP:OPAQUE
        END:VEVENT
        END:VCALENDAR
            `;

    const encodedIcsContent = encodeURIComponent(icsContent);
    const dataUri = `data:text/calendar;charset=utf-8,${encodedIcsContent}`;

    return `
        <div style="font-family: Arial, sans-serif; line-height: 1.6;">
            <h2>Neue Terminbuchung</h2>
            <p><strong>Betreff:</strong> ${content.Betreff}</p>
            <p><strong>Datum:</strong> ${content.Datum}</p>
            <p><strong>Uhrzeit:</strong> ${content.Uhrzeit}</p>
            <p><strong>Ort:</strong> ${content.Ort}</p>
            <p><strong>Beschreibung:</strong> ${content.Beschreibung}</p>
            <a href="${dataUri}" target="_blank" style="display: inline-block; margin-top: 20px; padding: 10px 15px; background-color: #007BFF; color: #fff; text-decoration: none; border-radius: 5px;">Termin öffnen</a>
        </div>
    `;
}

function prepareHtmlForAnswer(message) {
    const content = message['CONTENT'];

    return `
        <div style="font-family: Arial, sans-serif; line-height: 1.6;">
            <p><strong>Antwort:</strong> ${content.email_response}</p>
            <p><strong>Offene Fragen:</strong> ${content.questions}</p>
        </div>
    `;
}

function switchToChatInput() {
    document.getElementById('file-input').style.display = 'none';
    document.getElementById('message-input').style.display = 'block';
    document.getElementById('send-button').removeEventListener('click', handleFileUpload);
    document.getElementById('send-button').addEventListener('click', sendMessage);
    document.getElementById('message-input').addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
}

function sendMessage() {
    const input = document.getElementById('message-input');
    const message = input.value.trim();

    if (message !== '') {
        appendMessage('user', message);
        input.value = '';

        fetch('http://127.0.0.1:5000/send-message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({message: message})
        })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    appendMessage('bot', data.response);
                }
            })
            .catch(error => console.error('Error:', error));
    }
}

function clear() {
    fetch('http://127.0.0.1:5000/clear', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: {}
    })
    document.getElementById('file-input').value = '';
    document.getElementById('chat-messages').innerHTML = "";
    document.getElementById('file-input').style.display = 'block';
    document.getElementById('message-input').style.display = 'none';
    document.getElementById('send-button').addEventListener('click', handleFileUpload);
    document.getElementById('send-button').removeEventListener('click', sendMessage);
    document.getElementById('message-input').removeEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
}