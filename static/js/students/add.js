const ORIGIN_VALUE_TO_ACTIVATE_RECOMMENDED_BY = 'recomendado por un conocido'

document.addEventListener('DOMContentLoaded', () => {
    loadDefaultValues()
    loadEvents()
})

function loadDefaultValues() {
    const entryDateInput = document.querySelector('#entryDate')
    entryDateInput.value = new Date().valueAsDate = new Date().toISOString().substring(0,10)
}

function loadEvents() {
    loadStudentOriginInputOnKeyPress()
    loadAddStudentContactCheck()
}

function loadStudentOriginInputOnKeyPress() {
    const originInput = document.querySelector('#origin')
    originInput.onkeyup = () => {
        const recommendedByContainer = document.querySelector('#input-group-recommendedBy')
        if (originInput.value.toLowerCase() == ORIGIN_VALUE_TO_ACTIVATE_RECOMMENDED_BY) {
            recommendedByContainer.style.display = 'flex'
        } else {
            recommendedByContainer.style.display = 'none'
        }
    }
}

function loadAddStudentContactCheck() {
    const check = document.querySelector('#addStudentContactBtn')
    check.addEventListener('click', () => {
        const valuesContainer = document.querySelector('#add-student-contacts-values')
        const inputGroupContainers = valuesContainer.querySelectorAll('.add-student-contact-input-group-container')
        
        const contactNumber = inputGroupContainers.length + 1

        const newAddStudentContactContainer = document.createElement('div')
        const newInputGroupsContainer = document.createElement('div')

        newAddStudentContactContainer.classList.add('add-student-contact-container')
        newInputGroupsContainer.classList.add('add-student-contact-input-group-container', 'col-10')

        const firstInputId = 'contact-name-' + contactNumber
        const newInputGroups = [
            createInputGroup('Nombre del contacto', firstInputId, 'text'),
            createInputGroup('Relación con el alumno', 'contact-relationship-' + contactNumber, 'text'),
            createInputGroup('Celular', 'contact-phone-' + contactNumber, 'number')
        ]
        newInputGroups.forEach(inputGroup => newInputGroupsContainer.appendChild(inputGroup))

        const newActionsContainer = document.createElement('div')
        const newBtnDelete = document.createElement('button')

        newActionsContainer.classList.add('add-student-contact-actions-container', 'col-2')
        newBtnDelete.type = 'button'
        newBtnDelete.innerText = 'Eliminar'
        newBtnDelete.classList.add('btn', 'btn-danger')
        newBtnDelete.onclick = () => {
            valuesContainer.removeChild(newAddStudentContactContainer)
        }
        newActionsContainer.appendChild(newBtnDelete)

        newAddStudentContactContainer.appendChild(newInputGroupsContainer)
        newAddStudentContactContainer.appendChild(newActionsContainer)
        valuesContainer.prepend(newAddStudentContactContainer)
        newInputGroups[0].querySelector('#' + firstInputId).focus()
    })

    function createInputGroup(labelText, inputId, inputType='text') {
        const newInputGroup = document.createElement('div')
        const newInputGroupPrepend = document.createElement('div')
        const newInputGroupText = document.createElement('span')
        const newLabel = document.createElement('label')
        const newInput = document.createElement('input')
        newInputGroup.classList.add('input-group')
        newInputGroupPrepend.classList.add('input-group-prepend')
        newInputGroupText.classList.add('input-group-text')
        
        newLabel.innerText = labelText
        newLabel.htmlFor = inputId
        newInput.id = inputId
        newInput.type = inputType
        newInput.classList.add('form-control')
        
        newInputGroupText.appendChild(newLabel)
        newInputGroupPrepend.appendChild(newInputGroupText)
        newInputGroup.appendChild(newInputGroupPrepend)
        newInputGroup.appendChild(newInput)
        return newInputGroup
    }
}