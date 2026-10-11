# Research Publication Database System

A desktop database system for managing faculty members and their research publications in the Department of Mechanical Engineering, BUET.
I built it as my **C Programming Assignment (Level 1, Term 2)**.

The GUI is made with **Python (Tkinter)**. It sends every request through a **Python middleware** to small **C programs**, which read and write the data files.

## 🎥 Demo Video

[![Watch the demo](https://img.youtube.com/vi/9Tf0TVPy0iE/0.jpg)](https://youtu.be/9Tf0TVPy0iE)

▶️ https://youtu.be/9Tf0TVPy0iE

## ⚙️ How It Works

```
GUI (Python/Tkinter)  →  Middleware (Python)  →  C Programs  →  Data Files (.dat)
```

1. The user does something in the GUI (for example, adds a faculty member).
2. The GUI calls `middleware.handle_command()` with a command such as `ADD_FACULTY`.
3. The middleware runs the matching C program.
4. The C program reads or writes `faculty.dat` / `publication.dat` and prints the result.
5. The GUI shows that output to the user.

## ✨ Features

- **Login** with two roles: Admin and User
- **Add Faculty**: ID, full name, short name, designation, research interest
- **Add Publication**: year, type, faculty short name, title
- **Search Publications** by faculty name, year, publication type or research topic
- **Reports**
  - Faculty Information
  - Faculty-wise Publications
  - Year-wise Publications
  - Publication Type Summary
  - Department Statistics
- **Delete** a faculty or publication record (Admin only)
- **Save & Exit**

| Role  | Add | Search | Reports | Delete |
|-------|:---:|:------:|:-------:|:------:|
| Admin | ✅  | ✅     | ✅      | ✅     |
| User  | ❌  | ✅     | ✅      | ❌     |

## 📁 Project Structure

```
research-publication-dbms/
├── login_gui.py              # Login window (start here)
├── main_gui.py               # Main menu and all screens
├── middleware.py             # Connects the GUI to the C programs
├── setup.py                  # Compiles the C programs, creates sample data
├── c_programs/
│   ├── faculty_update.c      # Add faculty
│   ├── publication_update.c  # Add publication
│   ├── faculty_info.c        # List all faculty
│   ├── search_publication.c  # Search publications
│   ├── generate_report.c     # All reports
│   ├── delete_faculty.c      # Delete faculty
│   ├── delete_publication.c  # Delete publication
│   └── save_data.c           # Save check on exit
└── data_files/
    ├── faculty.dat           # id,full_name,short_name,designation,research
    └── publication.dat       # year,type,faculty_short_name,title
```

## 🚀 How to Run

**Requirements:** Python 3 (Tkinter comes with it) and the GCC compiler (MinGW on Windows).

```bash
git clone https://github.com/mdruhulamin20061610-cmyk/research-publication-dbms.git
cd research-publication-dbms
python setup.py        # compiles the C programs
python login_gui.py    # starts the app
```

**Default login**

| Role  | Username | Password |
|-------|----------|----------|
| Admin | admin    | admin123 |
| User  | user     | user123  |

## 🗃️ Data Format

Records are stored one per line, with fields separated by commas:

```
faculty.dat      MEF-01,Dr. Md. Hasan Khan,MHK,Professor,Heat Transfer
publication.dat  2021,Journal,MHK,Heat Transfer Enhancement Using CNT
```

Publications are linked to faculty by the faculty's **short name**.

## 🛠️ Built With

- **C**: file handling, string processing, command-line arguments
- **Python 3**: middleware (`subprocess`)
- **Tkinter**: GUI

## 👤 Author

**Md. Ruhul Amin**
Department of Mechanical Engineering, BUET

[GitHub](https://github.com/mdruhulamin20061610-cmyk) · [LinkedIn](https://linkedin.com/in/mdruhulamin124)

---
*Made for academic purposes: C Programming course, Level 1 Term 2, BUET.*
