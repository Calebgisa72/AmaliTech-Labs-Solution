#  Student Course Management System  

This project is a simple command-line-based **Student Course Management System** built using Python and Object-Oriented Programming (OOP) principles.  
It demonstrates **inheritance, abstraction, composition, data storage using dictionaries, and modular program design**.

The system allows an administrator to:
- Add students (Undergraduate or Graduate)
- Add courses according to level
- Enroll students in courses
- Assign grades
- View marks per student or per course
- View all students/courses
- View detailed student information

---

## Project Structure
### **1. Student Management**
Supports two student types:
- **UndergraduateStudent**
- **GraduateStudent** (includes thesis topic)

Each student is automatically assigned a unique ID.

### **2. Course Management**
Courses are added with:
- Course code (e.g., CSC101)
- Title (e.g., Introduction to Python)
- Level (Undergraduate or Graduate)

### **3. Enrollment**
Students can only enroll in courses that match their level.

### **4. Grading**
Admin can assign marks to a student for a given course.

Includes:
- Viewing student marks
- Viewing marks of all students in a course
- Average grade calculation

---

## Setup Instructions

### **Requirements**
- Python **3.10+**
- Terminal / Command Prompt

### **Cloning the project and running it**

```bash
git clone <https://github.com/Calebgisa72/AmaliTech-Labs-Solution>
cd Student Course Management System
python main.py
```
