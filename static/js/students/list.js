document.addEventListener('DOMContentLoaded', () => {
    loadDeleteFormsAction()

    function loadDeleteFormsAction() {
        const forms = document.getElementsByClassName('delete-student-form')
        for (form of forms) {
            form.addEventListener('submit', (e) => {
                e.preventDefault()
                ajaxDelete(form.action, function (response) {
                    try {
                        response = JSON.parse(response)
                        setMessageToShowAfterReloading(response['type'], response['message'])
                        window.location.href = response['redirect_url']
                    } catch (err) {
                        location.reload()
                    }
                })
            })
        }
    }
})