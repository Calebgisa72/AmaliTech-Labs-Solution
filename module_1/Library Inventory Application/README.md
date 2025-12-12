# Library Inventory Application

This project is a command-line **Library Inventory Application** built using Python and Object-Oriented Programming (OOP).  
It demonstrates principles such as **inheritance, abstraction, polymorphism, encapsulation, and modular system design**.

The system allows a librarian to:

- Add authors  
- Add different types of books  
- Loan books to borrowers  
- Return books with overdue charge calculation  
- Search books by title  
- Edit or delete existing books  
- List all books, authors, and active loans  
- Load sample books and authors for quick testing  

Book types supported:

- **Textbook**  
- **Audiobook**

---

## Project Structure

### 1. Author Management

Authors include essential details stored in the system:

#### **Author**
- Auto-generated author ID  
- Name  
- Nationality  

Authors are stored centrally so books can easily be linked to them.

---

### 2. Book Management

Books are managed through an abstract base class and two concrete subclasses.

#### **Book (Abstract Class)**
Shared attributes:
- Book ID (auto-generated)  
- Title  
- Year of publication  
- Availability status  
- Genre (Textbook / Audiobook)

Common features:
- Marking a book as checked-out or available  
- Displaying formatted book information  
- Updating editable fields  

Two book categories extend this base class:

---

#### **Textbook**
- Title  
- Publication year  
- Linked Author object  
- Editable fields: *title, year, author*  

---

#### **Audiobook**
- Title  
- Publication year  
- Duration in seconds (automatically formatted as H:M:S)  
- Narrator name  
- Editable fields: *title, year, duration, narrator*  

---

### 3. Borrower Management

Borrowers represent individuals who take out books.

#### **Borrower**
- Auto-generated borrower ID  
- Name  
- Telephone number  

A borrower is created automatically when a book is loaned.

---

### 4. Loan Management

Loans track the borrowing and returning of books.

#### **Loan**
- Book ID  
- Borrower information  
- Loan date  
- Return date  
- Overdue fee calculation (300 FRW per day)  

Key features:
- Automatically marks book as checked-out  
- Checks if a book is overdue  
- Calculates total overdue charge  
- Allows librarian to confirm charge payment before returning  

---

## Example Features

- Start with preloaded sample authors and books  
- Add new textbooks or audiobooks  
- Add authors and link them to books  
- Loan a book to a borrower  
- Return a book with overdue payment options  
- Search books by title (case-insensitive)  
- Edit book information  
- Delete available books  
- Display detailed information for all stored items  

---

## Setup Instructions

### **Requirements**
- Python **3.10+**
- Terminal / Command Prompt

---

## Running the Project

### **1. Clone the Repository**
```bash
git clone https://github.com/Calebgisa72/AmaliTech-Labs-Solution
cd "Library Inventory Application"
python main.py