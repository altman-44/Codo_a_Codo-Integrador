document.addEventListener('DOMContentLoaded', () => {
    setInitialStyles()

    function setInitialStyles() {
        const header = document.getElementsByTagName('header')[0]
        const main = document.getElementsByTagName('main')[0]
        main.style.minHeight = (window.innerHeight - header.clientHeight) + 'px'
    }
})