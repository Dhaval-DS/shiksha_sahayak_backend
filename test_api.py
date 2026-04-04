import requests

BASE = "http://127.0.0.1:5000/api"

def test(label, method, url, data=None, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        r = getattr(requests, method)(url, json=data, headers=headers)
        status = "✅" if r.status_code in [200, 201] else "❌"
        print(f"{status} [{r.status_code}] {label}")
        return r.json()
    except Exception as e:
        print(f"❌ ERROR {label}: {e}")
        return {}

print("\n🔐 AUTH")
test("Register teacher", "post", f"{BASE}/auth/register", {
    "first_name": "Test", "last_name": "Teacher",
    "email": "test@test.com", "password": "test123",
    "subject_taught": "Math", "role": "teacher"
})
res = test("Login teacher", "post", f"{BASE}/auth/login", {
    "email": "test@test.com", "password": "test123"
})
token = res.get("token", "")

print("\n🏫 CLASSES")
test("Create class", "post", f"{BASE}/classes/createClass", {
    "grade": "10", "section": "A", "teacher_id": 1
}, token)
test("Get all classes", "get", f"{BASE}/classes/getAllClasses", token=token)
test("Get class by id", "get", f"{BASE}/classes/getClassById/1", token=token)
test("Update class", "put", f"{BASE}/classes/updateClass/1", {
    "grade": "10", "section": "B"
}, token)

print("\n👨‍🎓 STUDENTS")
test("Create student", "post", f"{BASE}/createStudent", {
    "first_name": "John", "last_name": "Doe",
    "roll_number": "R001", "age": 15,
    "parent_name": "Jane Doe", "parent_contact": 9999999999,
    "parent_email": "jane@test.com",
    "parent_preferred_language": "English", "class_id": 1
}, token)
test("Get all students", "get", f"{BASE}/getAllStudents", token=token)
test("Get student by id", "get", f"{BASE}/getStudentById/1", token=token)
test("Update student", "put", f"{BASE}/updateStudent/1", {
    "first_name": "Johnny"
}, token)

print("\n👨‍🏫 TEACHERS")
test("Get all teachers", "get", f"{BASE}/teachers", token=token)
test("Get teacher by id", "get", f"{BASE}/teachers/1", token=token)

print("\n📋 ASSIGNMENTS")
test("Create assignment", "post", f"{BASE}/assignments/create", {
    "title": "Math HW", "description": "Chapter 1",
    "due_date": "2026-04-10", "class_id": 1
}, token)
test("Get all assignments", "get", f"{BASE}/assignments/getAllAssignments", token=token)
test("Get assignment by id", "get", f"{BASE}/assignments/1", token=token)
test("Get assignments by class", "get", f"{BASE}/assignments/class/1", token=token)

print("\n📝 SUBMISSIONS")
test("Submit assignment", "post", f"{BASE}/submissions/submit", {
    "assignment_id": 1, "student_id": 1, "comment": "Done!"
}, token)
test("Get submissions", "get", f"{BASE}/submissions/assignment/1", token=token)

print("\n📅 ATTENDANCE")
test("Mark attendance", "post", f"{BASE}/attendance", {
    "student_id": 1, "teacher_id": 1,
    "date": "2026-04-04", "status": "present"
}, token)
test("Get by student", "get", f"{BASE}/attendance/student/1", token=token)
test("Get by teacher", "get", f"{BASE}/attendance/teacher/1", token=token)
test("Get by date", "get", f"{BASE}/attendance/date/2026-04-04", token=token)

print("\nDone! ✅")