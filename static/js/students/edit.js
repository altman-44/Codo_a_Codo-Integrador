document.addEventListener('DOMContentLoaded', () => {
    loadPutFormsAction()

    function loadPutFormsAction() {
        const forms = document.getElementsByClassName('edit-data-form')
        for (let form of forms) {
            form.addEventListener('submit', e => {
                e.preventDefault()
                ajaxPut(form.action, new FormData(form), response => {
                    try {
                        response = JSON.parse(response)
                        setMessageToShowAfterReloading(response['type'], response['message'])
                        window.location.href = response['redirect_url']
                    } catch (err) {
                        console.log('error', err)
                    }
                })
            })
        }
    }
})