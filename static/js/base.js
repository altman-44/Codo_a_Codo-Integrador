document.addEventListener('DOMContentLoaded', () => {
    setInitialStyles()

    function setInitialStyles() {
        const header = document.getElementsByTagName('header')[0]
        const main = document.getElementsByTagName('main')[0]
        main.style.minHeight = (window.innerHeight - header.clientHeight) + 'px'
    }
})

function ajaxDelete(url, formData, cb) {
    xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            cb(this.responseText)
        }
    }
    xhr.open('DELETE', url)
    xhr.send(formData)
}