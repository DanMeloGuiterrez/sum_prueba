document.addEventListener("DOMContentLoaded", function () {
    const chatButton = document.querySelector('.chatbox__button button');
    const chatBox = document.querySelector('.chatbox__support');
    const sendButton = document.querySelector('.send__button');
    const inputField = document.querySelector('.chatbox__footer input');
    const chatMessages = document.querySelector('.chatbox__messages div');

    // Abrir / cerrar chat
    chatButton.addEventListener('click', () => {
        chatBox.classList.toggle('chatbox--active');
    });

    // Enviar mensaje con botón
    sendButton.addEventListener('click', () => {
        sendMessage();
    });

    // Enviar con tecla Enter
    inputField.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // --- Función principal ---
    function sendMessage() {
        const msg = inputField.value.trim();
        if (msg === "") return;

        // Mostrar mensaje del usuario
        appendMessage('Tú', msg);
        inputField.value = '';

        // Enviar al servidor Flask
        fetch("/get", {
            method: "POST",
            body: new URLSearchParams({ msg: msg }),
            headers: { "Content-Type": "application/x-www-form-urlencoded" }
        })
        .then(res => res.json())
        .then(data => {
            appendMessage('Asistente IA', data.response);
        })
        .catch(() => {
            appendMessage('Asistente IA', "Error: No se pudo conectar con el servidor.");
        });
    }

    // --- Mostrar mensajes en el chat ---
    function appendMessage(sender, message) {
        const messageElem = document.createElement('p');
        messageElem.innerHTML = `<strong>${sender}:</strong> ${message}`;
        chatMessages.appendChild(messageElem);
        chatMessages.scrollTop = chatMessages.scrollHeight; // Auto-scroll
    }
});
