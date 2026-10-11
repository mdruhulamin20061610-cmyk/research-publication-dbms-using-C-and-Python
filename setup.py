# setup.py
import os
import subprocess
import sys

print("=== Setting up Research DBMS ===")

# Create directories
for d in ['c_programs', 'data_files']:
    if not os.path.exists(d):
        os.makedirs(d)
        print(f"Created directory: {d}")

# Compile C programs
print("\nCompiling C programs...")

c_files = {
    'faculty_update.c':      'Compiling faculty update...',
    'publication_update.c':  'Compiling publication update...',
    'faculty_info.c':        'Compiling faculty info...',
    'search_publication.c':  'Compiling search...',
    'generate_report.c':     'Compiling report generator...',
    'save_data.c':           'Compiling save utility...',
    'delete_faculty.c':      'Compiling delete faculty...',
    'delete_publication.c':  'Compiling delete publication...',
}

all_ok = True
for c_file, message in c_files.items():
    print(message)
    src = f'c_programs/{c_file}'
    out = f'c_programs/{c_file[:-2]}.exe'
    result = subprocess.run(['gcc', src, '-o', out], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"  ✓ {c_file[:-2]}.exe created")
    else:
        print(f"  ✗ Failed to compile {c_file}")
        if result.stderr:
            print(f"    {result.stderr.strip()}")
        all_ok = False

# Create sample data files (only if they don't exist)
print("\nCreating sample data files...")

if not os.path.exists('data_files/faculty.dat'):
    with open('data_files/faculty.dat', 'w') as f:
        f.write("MEF-01,Dr. Md. Hasan Khan,MHK,Professor,Heat Transfer\n")
        f.write("MEF-02,Dr. R. A. Sarker,RAS,Associate Professor,Solid Mechanics\n")
        f.write("MEF-03,Dr. Sadia Afrin,SA,Assistant Professor,Nanomaterials\n")
    print("  faculty.dat created")
else:
    print("  faculty.dat already exists – skipped")

if not os.path.exists('data_files/publication.dat'):
    with open('data_files/publication.dat', 'w') as f:
        f.write("2021,Journal,MHK,Heat Transfer Enhancement Using CNT\n")
        f.write("2021,Conference,RAS,MD Simulation of NPs\n")
        f.write("2022,Journal,SA,Stress Analysis of Composite Beams\n")
    print("  publication.dat created")
else:
    print("  publication.dat already exists – skipped")

print("\n=== Setup", "Complete ✓" if all_ok else "finished with errors ✗", "===")
print("\nTo run the system:")
print("  python login_gui.py")
print("\nDefault login credentials:")
print("  Admin : admin   / admin123")
print("  User  : user    / user123")
