# middleware.py - connects the GUI to the C programs
# GUI -> middleware -> C programs -> data files
import sys
import subprocess
import os

# work from the project folder so the C programs find c_programs/ and data_files/
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def handle_command(command, *args):
    """Route commands to appropriate C programs"""
    
    if command == "ADD_FACULTY":
        # Faculty data passed as string
        faculty_data = args[0]
        result = subprocess.run(['./c_programs/faculty_update.exe', faculty_data],
                               capture_output=True, text=True)
        return result
    
    elif command == "ADD_PUBLICATION":
        pub_data = args[0]
        result = subprocess.run(['./c_programs/publication_update.exe', pub_data],
                               capture_output=True, text=True)
        return result
    
    elif command == "GET_FACULTY_INFO":
        result = subprocess.run(['./c_programs/faculty_info.exe'],
                               capture_output=True, text=True)
        return result
    
    elif command == "SEARCH_PUB":
        criteria = args[0]
        term = args[1]
        result = subprocess.run(['./c_programs/search_publication.exe', criteria, term],
                               capture_output=True, text=True)
        return result
    
    elif command == "GENERATE_REPORT":
        report_type = args[0]
        result = subprocess.run(['./c_programs/generate_report.exe', report_type],
                               capture_output=True, text=True)
        return result
    
    elif command == "DELETE_FACULTY":
        criteria = args[0]
        value = args[1]
        result = subprocess.run(['./c_programs/delete_faculty.exe', criteria, value],
                               capture_output=True, text=True)
        return result
    
    elif command == "DELETE_PUBLICATION":
        criteria = args[0]
        value = args[1]
        result = subprocess.run(['./c_programs/delete_publication.exe', criteria, value],
                               capture_output=True, text=True)
        return result
    
    elif command == "SAVE_DATA":
        result = subprocess.run(['./c_programs/save_data.exe'],
                               capture_output=True, text=True)
        return result
    
    else:
        print(f"Unknown command: {command}")
        return None

if __name__ == "__main__":
    # For testing middleware directly
    if len(sys.argv) > 1:
        command = sys.argv[1]
        args = sys.argv[2:] if len(sys.argv) > 2 else []
        result = handle_command(command, *args)
        if result:
            print(result.stdout)
            sys.exit(result.returncode)