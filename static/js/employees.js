document.addEventListener('DOMContentLoaded', () => {
    loadDeleteFormsAction()

    function loadDeleteFormsAction() {
        const forms = document.getElementsByClassName('delete-employee-form')
        console.log(forms)
        for (form of forms) {
            console.log(form)
            form.addEventListener('submit', e => {
                e.preventDefault()
                ajaxDelete(form.action, null, document.innerHTML)
            })
        }
    }
})