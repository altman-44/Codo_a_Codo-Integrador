document.addEventListener('DOMContentLoaded', () => {
    setInitialStyles()
    showMessageAfterReloading()

    function setInitialStyles() {
        const header = document.getElementsByTagName('header')[0]
        const main = document.getElementsByTagName('main')[0]
        main.style.minHeight = window.innerHeight - header.clientHeight + 'px'
    }

    function showMessageAfterReloading() {
        reloadingMessageType = sessionStorage.getItem('reloading_message_type')
        reloadingMessageText = sessionStorage.getItem('reloading_message_text')
        if (reloadingMessageType && reloadingMessageText) {
            showAlertMessage(reloadingMessageType, reloadingMessageText)
        }
        sessionStorage.removeItem('reloading_message_type')
        sessionStorage.removeItem('reloading_message_text')
    }
})

function setMessageToShowAfterReloading(type, message) {
    sessionStorage.setItem(
        'reloading_message_type',
        type
    )
    sessionStorage.setItem(
        'reloading_message_text',
        message
    )
}

function showAlertMessage(type, message) {
    const alertsContainer = document.getElementById('alert-messages-container')
    const alert = document.createElement('div')
    alert.classList.add('alert', `alert-${getAlertClassByMessageType(type)}`, 'text-center')
    const buttonClose = getAlertCloseButton()
    const messageElement = document.createElement('p')
    messageElement.innerText = message
    alert.appendChild(buttonClose)
    alert.appendChild(messageElement)
    alertsContainer.appendChild(alert)

    function getAlertClassByMessageType(type) {
        return type == 'error'
            ? 'danger'
            : type == 'success'
            ? 'success'
            : type == 'warning'
            ? 'warning'
            : 'info'
    }

    function getAlertCloseButton() {
        const buttonClose = document.createElement('button')
        buttonClose.classList.add('close')
        buttonClose.dataset['dismiss'] = 'alert'
        buttonClose.ariaLabel = 'Close'
        const span = document.createElement('span')
        span.ariaHidden = 'true'
        span.innerHTML = '&times;'
        buttonClose.appendChild(span)
        return buttonClose
    }
}

function ajaxDelete(url, cb) {
    xhr = new XMLHttpRequest()
    xhr.open('DELETE', url, true)
    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            cb(this.responseText)
        }
    }
    xhr.send()
}

function ajaxPut(url, formData, cb) {
    xhr = new XMLHttpRequest()
    xhr.open('PUT', url, true)
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            cb(this.responseText)
        }
    }
    xhr.send(formData)
}