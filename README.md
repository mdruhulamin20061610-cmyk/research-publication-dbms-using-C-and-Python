# Research Publication Database System

A desktop database system for managing faculty members and their research publications in the Department of Mechanical Engineering, BUET.
I built it as my **C Programming Assignment (Level 1, Term 2)**.

The GUI is made with **Python (Tkinter)**. It sends every request through a **Python middleware** to small **C programs**, which read and write the data files.

## 🎥 Demo Video

[![Watch the demo](https://img.youtube.com/vi/9Tf0TVPy0iE/0.jpg)](https://youtu.be/9Tf0TVPy0iE)

▶️ https://youtu.be/9Tf0TVPy0iE

## 🏗️ Software Architecture

The system has **three layers**. Each layer only talks to the layer next to it.

```
┌──────────────────────────────────────────────┐
│  1. PRESENTATION LAYER  (Python + Tkinter)   │
│     login_gui.py  →  main_gui.py             │
│     Forms, buttons, result screens           │
└──────────────────────┬───────────────────────┘
                       │ handle_command("SEARCH_PUB", "Year", "2021")
                       ▼
┌──────────────────────────────────────────────┐
│  2. MIDDLEWARE LAYER  (Python)               │
│     middleware.py                            │
│     Maps each command to its C program and   │
│     runs it with subprocess                  │
└──────────────────────┬───────────────────────┘
                       │ search_publication.exe "Year" "2021"
                       ▼
┌──────────────────────────────────────────────┐
│  3. BACK-END / DATA LAYER  (C)               │
│     c_programs/*.exe                         │
│     Reads/writes the data files and prints   │
│     the result (SUCCESS / ERROR / report)    │
└──────────────────────┬───────────────────────┘
                       ▼
            data_files/faculty.dat
            data_files/publication.dat
```

**Why it's split like this**
- The **GUI** only handles what the user sees. It never opens the data files itself.
- The **middleware** is the single entry point to the back-end. The GUI just sends a command name (for example `ADD_FACULTY`) and doesn't need to know which program runs.
- The **C programs** do all the data processing. Each one is small and does one job.

## ⚙️ How It Works

### Program flow

```
login_gui.py ──(admin/user)──► main_gui.py (Main Menu)
                                   ├── Add Faculty
                                   ├── Add Publication
                                   ├── Search Publications
                                   ├── Generate Reports
                                   ├── Delete Record
                                   └── Save & Exit
```

### Example: adding a publication

1. The admin fills the form: `2022`, `Journal`, `SA`, `Stress Analysis of Composite Beams`.
2. `main_gui.py` joins the fields into one line: `2022,Journal,SA,Stress Analysis of Composite Beams`.
3. It calls `middleware.handle_command("ADD_PUBLICATION", line)`.
4. The middleware runs `c_programs/publication_update.exe "<line>"`.
5. The C program opens `publication.dat` in append mode, writes the line, and prints `SUCCESS`.
6. The GUI sees `SUCCESS` and shows a confirmation message.

### Middleware commands

| Command              | C program                | Arguments          | Used for                      |
|----------------------|--------------------------|--------------------|-------------------------------|
| `ADD_FACULTY`        | `faculty_update.exe`     | CSV line           | Add a faculty                 |
| `ADD_PUBLICATION`    | `publication_update.exe` | CSV line           | Add a publication             |
| `GET_FACULTY_INFO`   | `faculty_info.exe`       | none               | List all faculty              |
| `SEARCH_PUB`         | `search_publication.exe` | criteria, term     | Search publications           |
| `GENERATE_REPORT`    | `generate_report.exe`    | report type        | Reports                       |
| `DELETE_FACULTY`     | `delete_faculty.exe`     | criteria, value    | Delete faculty                |
| `DELETE_PUBLICATION` | `delete_publication.exe` | criteria, value    | Delete publication            |
| `SAVE_DATA`          | `save_data.exe`          | none               | Check & confirm save on exit  |

### How the C programs work

| Program | Logic |
|---|---|
| `faculty_update.c` / `publication_update.c` | Open the `.dat` file in **append** mode (`"a"`) and write the new record as one line. |
| `faculty_info.c` | Read `faculty.dat` line by line with `fgets`, split it with `strtok`, and print a table. |
| `search_publication.c` | Read each publication with `fgets` and split it with `sscanf`. **Year** and **type** use `strcmp` (exact match); **topic** uses `strstr` (keyword match). For **faculty name**, it first looks up the faculty's short name in `faculty.dat`, then matches publications with that short name. |
| `generate_report.c` | One program, five reports (chosen by argument): faculty info, faculty-wise count, year-wise count (array indexed by `year - 2000`), type summary (counters), department statistics (line counts and average). |
| `delete_faculty.c` / `delete_publication.c` | Read every line into an array, then open the file again in **write** mode and write back only the lines that **don't** match. |
| `save_data.c` | Records are saved as soon as they are added, so this checks that both data files exist and reports how many records are stored. |

The C programs report back to the GUI by printing keywords to standard output: `SUCCESS`, `ERROR` or `NOT_FOUND`. The GUI reads these to decide which message to show.

### Search and delete options

| Screen | Options |
|---|---|
| Search | Faculty Name, Year, Publication Type, Research Topic |
| Delete Faculty | ID, Name, Short Name |
| Delete Publication | Year, Type, Faculty Short Name, Title Keyword |

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

## 📸 Screenshots

> Add screenshots here: upload them into a `screenshots/` folder and link them like `![Main Menu](screenshots/main_menu.png)`.

## ⚠️ Limitations

- Login usernames and passwords are written in the code (no users file).
- Data is stored as plain comma-separated text, so fields (except a publication title) must not contain commas.
- Search and delete are case-sensitive (`Journal` ≠ `journal`).
- The program doesn't check that a publication's faculty short name exists before saving it.
- Deleting a faculty does not delete their publications.

## 🔮 Possible Improvements

- Store user accounts in a file
- Use `struct` records and binary files (`fread` / `fwrite`)
- Check that the faculty exists before adding a publication
- Edit/update existing records

## 🛠️ Built With

- **C**: file handling (`fopen`, `fgets`, `fprintf`), string functions (`strcmp`, `strstr`, `strtok`, `sscanf`), command-line arguments (`argc`, `argv`)
- **Python 3**: middleware (`subprocess`)
- **Tkinter**: GUI

## 👤 Author

**Md. Ruhul Amin**
Department of Mechanical Engineering, BUET

[GitHub](https://github.com/mdruhulamin20061610-cmyk) · [LinkedIn](https://linkedin.com/in/mdruhulamin124)

---
*Made for academic purposes: C Programming course, Level 1 Term 2, BUET.*
