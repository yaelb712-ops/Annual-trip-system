const SERVER = 'http://127.0.0.1:5000'

let teacherId = ''
let teacherClass = ''

async function login() {
    teacherId = document.getElementById('teacherId').value

    const response = await fetch(`${SERVER}/teachers/id/${teacherId}`, { headers: { 'teacherId': teacherId } })

    if (response.ok) {
        const data = await response.json()
        teacherClass = data.classN
        document.getElementById('loginTeacher').style.display = 'none'
        document.getElementById('mainSection').style.display = 'block'
    }

    else {
        document.getElementById('loginError').style.display = 'block'

    }
}

function showTab(tab) {
    document.getElementById('studentsTab').style.display = 'none'
    document.getElementById('teachersTab').style.display = 'none'
    document.getElementById(tab + 'Tab').style.display = 'block'
}

async function getAllStudents() {
    const response = await fetch(`${SERVER}/students`, {
        headers: { 'teacherId': teacherId }
    })
    const data = await response.json()
    displayResults(data.students, 'studentsResult')
}

async function getMyClass() {
    const response = await fetch(`${SERVER}/students/class/${teacherClass}`, {
        headers: { 'teacherId': teacherId }
    })
    const data = await response.json()
    displayResults(data.students, 'studentsResult')

}

async function getStudent() {
    const id = document.getElementById('searchStudentId').value
    const response = await fetch(`${SERVER}/students/id/${id}`, {
        headers: { 'teacherId': teacherId }
    })
    const data = await response.json()
    displayResults([data], 'studentsResult')

}

async function getAllTeachers() {
    const response = await fetch(`${SERVER}/teachers`, {
        headers: { 'teacherId': teacherId }
    })
    const data = await response.json()
    displayResults(data.teachers, 'teachersResult')

}

async function getTeacher() {
    const id = document.getElementById('searchTeacherId').value
    const response = await fetch(`${SERVER}/teachers/id/${id}`, {
        headers: { 'teacherId': teacherId }
    })
    const data = await response.json()
    displayResults([data], 'teachersResult')

}

function displayResults(items, containerId) {
    const container = document.getElementById(containerId)
    container.innerHTML = ''
    items.forEach(element => {
        container.innerHTML += `
        <p>${element.firstName} ${element.lastName} |ת"ז: ${element.identityNumber}| כיתה: ${element.classN}`
    })

}

document.getElementById('studentForm').addEventListener('submit', async function (e) {
    e.preventDefault()

    const newStudent = {
        firstName: document.getElementById('studentFirstName').value,
        lastName: document.getElementById('studentLastName').value,
        identityNumber: document.getElementById('studentId').value,
        classN: teacherClass
    }

    if (newStudent.studentFirstName = '') {
        alert('insert first name')
        return
    }
    if (newStudent.studentLastName = '') {
        alert('insert last name')
        return
    }
    if (newStudent.identityNumber.length !== 9) {
        alert('identityNumber must be 9 numbers')
        return
    }
    if (newStudent.studentClass = '') {
        alert('insert class number')
        return
    }


    const response = await fetch(`${SERVER}/students`, {
        method: 'POST',
        headers: {
            'teacherId': teacherId,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(newStudent)
    })

    if (response.ok) {
        alert('student added!')
        document.getElementById('studentForm').reset()
    } else {
        alert('error during adding student')
    }
})

document.getElementById('teacherForm').addEventListener('submit', async function (e) {
    e.preventDefault()

    const newTeacher = {
        firstName: document.getElementById('teacherFirstName').value,
        lastName: document.getElementById('teacherLastName').value,
        identityNumber: document.getElementById('teacherIdentity').value,
        classN: document.getElementById('teacherClass').value
    }

    if (newTeacher.firstName = '') {
        alert('insert first name')
        return
    }
    if (newTeacher.lastName = '') {
        alert('insert last name')
        return
    }
    if (newTeacher.identityNumber.length !== 9) {
        alert('identityNumber must be 9 numbers')
        return
    }
    if (newTeacher.classN = '') {
        alert('insert class number')
        return
    }

    const response = await fetch(`${SERVER}/teachers`, {
        method: 'POST',
        headers: {
            'teacherId': teacherId,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(newTeacher)
    })

    if (response.ok) {
        alert('teacher added!')
        document.getElementById('teacherForm').reset()
    } else {
        alert('error during adding teacher')
    }
})

let map = null
let markers = {}

function initMap(){
    if(map) return

    map = L.map('map').setView([31.8830, 35.2642], 13);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);
}

async function updateMap() {
    initMap()
    const response = await fetch(`${SERVER}/Locations`, {headers: {
        'teacherId': teacherId}})
    const data = await response.json()
    data.Locations.forEach(location => {
        const lat =location.latitude
        const lng = location.longitude
        const  id = location.studentIdentity

        if(markers[id]){
            markers[id].setLatLng([lat,lng])
        } else {
            markers[id] = L.marker([lat, lng]).addTo(map).bindPopup(id).openPopup()
        }
    })
}

function showTab(tab){
    document.getElementById('studentsTab').style.display = 'none'
    document.getElementById('teachersTab').style.display = 'none'
    document.getElementById('mapTab').style.display = 'none'
    document.getElementById(tab+'Tab').style.display = 'block'

    if(tab === 'map'){
       updateMap() 
    } 
}

async function checkDistance() {
    const response = await fetch(`${SERVER}/teacher-location`, {headers: {'teacherId': teacherId}})
    const data = await response.json()
    const teacherLatLng = L.latLng(data.latitude, data.longitude)

    let anyFar = false
    
    for(const id in markers){
        const studentLatLng = markers[id].getLatLng()
        const distance = teacherLatLng.distanceTo(studentLatLng)
        
        if(distance > 3000) {
            alert(`student ${id} is too far away!`)
            anyFar = true
        }
    }
    
    if(!anyFar) {
        alert('all students are close enough!')
    }
}
