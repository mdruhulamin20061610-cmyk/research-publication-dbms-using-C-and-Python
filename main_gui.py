import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
import middleware


class MainGUI:
    def __init__(self, root, user_role="admin"):
        self.root = root
        self.user_role = user_role
        self.root.title("Research DBMS - BUET Mechanical")
        self.root.geometry("900x700")
        self.root.configure(bg="#2c3e50")

        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        header = tk.Frame(root, bg="#3498db", height=100)
        header.pack(fill="x")

        tk.Label(
            header,
            text="RESEARCH PUBLICATION DATABASE SYSTEM",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#3498db"
        ).pack(pady=15)

        tk.Label(
            header,
            text="Department of Mechanical Engineering, BUET",
            font=("Arial", 12),
            fg="white",
            bg="#3498db"
        ).pack()

        user_frame = tk.Frame(root, bg="#34495e", height=40)
        user_frame.pack(fill="x", pady=5)

        tk.Label(
            user_frame,
            text=f"Logged in as: {user_role.upper()}",
            font=("Arial", 11),
            fg="white",
            bg="#34495e"
        ).pack(side="left", padx=20)

        tk.Button(
            user_frame,
            text="Logout",
            font=("Arial", 10),
            bg="#e74c3c",
            fg="white",
            command=self.logout
        ).pack(side="right", padx=20, pady=5)

        self.main_frame = tk.Frame(root, bg="#2c3e50")
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=20)

        self.show_main_menu()

    def run_command(self, command, *args):
        # every request goes through the middleware
        try:
            return middleware.handle_command(command, *args)
        except Exception as e:
            messagebox.showerror("Error", "Could not run " + command + "\n" + str(e) +
                                 "\n\nRun setup.py first to compile the C programs.")
            return None

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        self.clear_main_frame()

        tk.Label(
            self.main_frame,
            text="MAIN MENU",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#2c3e50"
        ).pack(pady=20)

        options_frame = tk.Frame(self.main_frame, bg="#34495e", padx=20, pady=20)
        options_frame.pack(fill="both", expand=True)

        if self.user_role == "admin":
            options = [
                ("Add Faculty", self.open_add_faculty, "#27ae60"),
                ("Add Publication", self.open_add_publication, "#27ae60"),
                ("Search Publications", self.open_search, "#3498db"),
                ("Generate Reports", self.open_reports, "#9b59b6"),
                ("Delete Record", self.open_delete, "#c0392b"),
                ("Save & Exit", self.save_exit, "#7f8c8d"),
            ]
        else:
            options = [
                ("Search Publications", self.open_search, "#3498db"),
                ("Generate Reports", self.open_reports, "#9b59b6"),
                ("Save & Exit", self.save_exit, "#7f8c8d"),
            ]

        row, col = 0, 0
        for text, command, color in options:
            btn = tk.Button(
                options_frame,
                text=text,
                font=("Arial", 13),
                bg=color,
                fg="white",
                width=22,
                height=3,
                command=command
            )
            btn.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            col += 1
            if col > 1:
                col = 0
                row += 1

        for i in range(2):
            options_frame.grid_columnconfigure(i, weight=1)
        for i in range(4):
            options_frame.grid_rowconfigure(i, weight=1)

    def open_add_faculty(self):
        self.show_faculty_form()

    def show_faculty_form(self):
        self.clear_main_frame()

        tk.Button(
            self.main_frame,
            text="<- Back to Menu",
            font=("Arial", 10),
            bg="#34495e",
            fg="white",
            command=self.show_main_menu
        ).pack(anchor="w", pady=10)

        tk.Label(
            self.main_frame,
            text="ADD NEW FACULTY",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#2c3e50"
        ).pack(pady=10)

        form_frame = tk.Frame(self.main_frame, bg="#34495e", padx=30, pady=20)
        form_frame.pack(pady=10)

        fields = [
            ("Faculty ID:", "entry"),
            ("Full Name:", "entry"),
            ("Short Name:", "entry"),
            ("Designation:", "combobox",
             ["Professor", "Associate Professor", "Assistant Professor", "Lecturer"]),
            ("Research Interest:", "entry"),
        ]

        self.faculty_entries = {}

        for i, (label, ftype, *opts) in enumerate(fields):
            tk.Label(
                form_frame,
                text=label,
                font=("Arial", 11),
                fg="white",
                bg="#34495e"
            ).grid(row=i, column=0, pady=10, sticky="w")

            key = label.strip(":").replace(" ", "_").lower()

            if ftype == "entry":
                e = tk.Entry(form_frame, font=("Arial", 11), width=40)
                e.grid(row=i, column=1, pady=10, padx=10)
                self.faculty_entries[key] = e
            else:
                c = ttk.Combobox(form_frame, font=("Arial", 11), width=38, values=opts[0], state="readonly")
                c.grid(row=i, column=1, pady=10, padx=10)
                self.faculty_entries[key] = c

        tk.Button(
            form_frame,
            text="ADD FACULTY",
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            width=20,
            height=2,
            command=self.submit_faculty
        ).grid(row=len(fields), column=0, columnspan=2, pady=20)

    def submit_faculty(self):
        keys = ["faculty_id", "full_name", "short_name", "designation", "research_interest"]
        data = []

        for key in keys:
            w = self.faculty_entries.get(key)
            if w is None:
                messagebox.showerror("Error", f"Field {key} not found")
                return

            v = w.get().strip()
            if not v:
                messagebox.showerror("Error", f"Please fill {key.replace('_', ' ').title()}")
                return

            data.append(v)

        csv_data = ",".join(data)
        result = self.run_command("ADD_FACULTY", csv_data)
        if result is None:
            return

        output = (result.stdout or "").strip()
        if "SUCCESS" in output:
            messagebox.showinfo("Success", "Faculty added successfully!")
            self.show_main_menu()
        else:
            messagebox.showerror("Error", output or result.stderr or "Failed to add faculty")

    def open_add_publication(self):
        self.show_publication_form()

    def show_publication_form(self):
        self.clear_main_frame()

        tk.Button(
            self.main_frame,
            text="<- Back to Menu",
            font=("Arial", 10),
            bg="#34495e",
            fg="white",
            command=self.show_main_menu
        ).pack(anchor="w", pady=10)

        tk.Label(
            self.main_frame,
            text="ADD NEW PUBLICATION",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#2c3e50"
        ).pack(pady=10)

        form_frame = tk.Frame(self.main_frame, bg="#34495e", padx=30, pady=20)
        form_frame.pack(pady=10)

        years = [str(y) for y in range(2025, 1999, -1)]

        fields = [
            ("Year:", "combobox", years),
            ("Publication Type:", "combobox",
             ["Journal", "Conference", "Review", "Book Chapter", "Other"]),
            ("Faculty Short Name:", "entry"),
            ("Title:", "entry"),
        ]

        self.pub_entries = {}

        for i, (label, ftype, *opts) in enumerate(fields):
            tk.Label(
                form_frame,
                text=label,
                font=("Arial", 11),
                fg="white",
                bg="#34495e"
            ).grid(row=i, column=0, pady=10, sticky="w")

            key = label.strip(":").replace(" ", "_").lower()

            if ftype == "entry":
                e = tk.Entry(form_frame, font=("Arial", 11), width=40)
                e.grid(row=i, column=1, pady=10, padx=10)
                self.pub_entries[key] = e
            else:
                c = ttk.Combobox(form_frame, font=("Arial", 11), width=38, values=opts[0], state="readonly")
                c.grid(row=i, column=1, pady=10, padx=10)
                c.current(0)
                self.pub_entries[key] = c

        tk.Button(
            form_frame,
            text="ADD PUBLICATION",
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            width=20,
            height=2,
            command=self.submit_publication
        ).grid(row=len(fields), column=0, columnspan=2, pady=20)

    def submit_publication(self):
        keys = ["year", "publication_type", "faculty_short_name", "title"]
        data = []

        for key in keys:
            w = self.pub_entries.get(key)
            if w is None:
                messagebox.showerror("Error", f"Field {key} not found")
                return

            v = w.get().strip()
            if not v:
                messagebox.showerror("Error", f"Please fill {key.replace('_', ' ').title()}")
                return

            data.append(v)

        csv_data = ",".join(data)
        result = self.run_command("ADD_PUBLICATION", csv_data)
        if result is None:
            return

        output = (result.stdout or "").strip()
        if "SUCCESS" in output:
            messagebox.showinfo("Success", "Publication added successfully!")
            self.show_main_menu()
        else:
            messagebox.showerror("Error", output or result.stderr or "Failed to add publication")

    def open_delete(self):
        self.show_delete_choice()

    def show_delete_choice(self):
        self.clear_main_frame()

        tk.Button(
            self.main_frame,
            text="<- Back to Menu",
            font=("Arial", 10),
            bg="#34495e",
            fg="white",
            command=self.show_main_menu
        ).pack(anchor="w", pady=10)

        tk.Label(
            self.main_frame,
            text="DELETE RECORD",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#2c3e50"
        ).pack(pady=30)

        tk.Label(
            self.main_frame,
            text="What would you like to delete?",
            font=("Arial", 13),
            fg="#ecf0f1",
            bg="#2c3e50"
        ).pack(pady=10)

        btn_frame = tk.Frame(self.main_frame, bg="#2c3e50")
        btn_frame.pack(pady=30)

        tk.Button(
            btn_frame,
            text="Delete Faculty",
            font=("Arial", 14),
            bg="#c0392b",
            fg="white",
            width=22,
            height=3,
            command=self.show_delete_faculty
        ).grid(row=0, column=0, padx=20)

        tk.Button(
            btn_frame,
            text="Delete Publication",
            font=("Arial", 14),
            bg="#c0392b",
            fg="white",
            width=22,
            height=3,
            command=self.show_delete_publication
        ).grid(row=0, column=1, padx=20)

    def show_delete_faculty(self):
        self.clear_main_frame()

        tk.Button(
            self.main_frame,
            text="<- Back to Delete Menu",
            font=("Arial", 10),
            bg="#34495e",
            fg="white",
            command=self.show_delete_choice
        ).pack(anchor="w", pady=10)

        tk.Label(
            self.main_frame,
            text="DELETE FACULTY",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#2c3e50"
        ).pack(pady=10)

        form_frame = tk.Frame(self.main_frame, bg="#34495e", padx=30, pady=30)
        form_frame.pack(pady=10)

        tk.Label(
            form_frame,
            text="Search By:",
            font=("Arial", 12),
            fg="white",
            bg="#34495e"
        ).grid(row=0, column=0, pady=15, sticky="w")

        self.del_fac_criteria = ttk.Combobox(
            form_frame,
            font=("Arial", 11),
            width=35,
            state="readonly",
            values=["ID", "Name", "Short Name"]
        )
        self.del_fac_criteria.grid(row=0, column=1, pady=15, padx=10)
        self.del_fac_criteria.current(0)

        tk.Label(
            form_frame,
            text="Enter Value:",
            font=("Arial", 12),
            fg="white",
            bg="#34495e"
        ).grid(row=1, column=0, pady=15, sticky="w")

        self.del_fac_value = tk.Entry(form_frame, font=("Arial", 11), width=37)
        self.del_fac_value.grid(row=1, column=1, pady=15, padx=10)

        tk.Label(
            form_frame,
            text="Examples  ID: MEF-01 | Name: Dr. Md. Hasan Khan | Short Name: MHK",
            font=("Arial", 9),
            fg="#bdc3c7",
            bg="#34495e"
        ).grid(row=2, column=0, columnspan=2, pady=5)

        tk.Button(
            form_frame,
            text="DELETE FACULTY",
            font=("Arial", 12, "bold"),
            bg="#c0392b",
            fg="white",
            width=22,
            height=2,
            command=self.confirm_delete_faculty
        ).grid(row=3, column=0, columnspan=2, pady=20)

    def confirm_delete_faculty(self):
        criteria = self.del_fac_criteria.get()
        value = self.del_fac_value.get().strip()

        if not value:
            messagebox.showerror("Error", "Please enter a value to search by.")
            return

        answer = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete faculty where {criteria} = '{value}'?\n"
            "This action cannot be undone."
        )
        if not answer:
            return

        result = self.run_command("DELETE_FACULTY", criteria, value)
        if result is None:
            return

        output = (result.stdout or "").strip()

        if "SUCCESS" in output:
            messagebox.showinfo("Deleted", "Faculty record(s) deleted successfully!")
            self.show_delete_choice()
        elif "NOT_FOUND" in output:
            messagebox.showwarning("Not Found", f"No faculty record found where {criteria} = '{value}'.")
        else:
            messagebox.showerror("Error", output or result.stderr or "An unexpected error occurred.")

    def show_delete_publication(self):
        self.clear_main_frame()

        tk.Button(
            self.main_frame,
            text="<- Back to Delete Menu",
            font=("Arial", 10),
            bg="#34495e",
            fg="white",
            command=self.show_delete_choice
        ).pack(anchor="w", pady=10)

        tk.Label(
            self.main_frame,
            text="DELETE PUBLICATION",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#2c3e50"
        ).pack(pady=10)

        form_frame = tk.Frame(self.main_frame, bg="#34495e", padx=30, pady=30)
        form_frame.pack(pady=10)

        tk.Label(
            form_frame,
            text="Search By:",
            font=("Arial", 12),
            fg="white",
            bg="#34495e"
        ).grid(row=0, column=0, pady=15, sticky="w")

        self.del_pub_criteria = ttk.Combobox(
            form_frame,
            font=("Arial", 11),
            width=35,
            state="readonly",
            values=["Year", "Type", "Faculty Short Name", "Title Keyword"]
        )
        self.del_pub_criteria.grid(row=0, column=1, pady=15, padx=10)
        self.del_pub_criteria.current(0)
        self.del_pub_criteria.bind("<<ComboboxSelected>>", self._update_pub_hint)

        tk.Label(
            form_frame,
            text="Enter Value:",
            font=("Arial", 12),
            fg="white",
            bg="#34495e"
        ).grid(row=1, column=0, pady=15, sticky="w")

        self.del_pub_value = tk.Entry(form_frame, font=("Arial", 11), width=37)
        self.del_pub_value.grid(row=1, column=1, pady=15, padx=10)

        self.pub_hint_var = tk.StringVar(value="Example  Year: 2022")
        tk.Label(
            form_frame,
            textvariable=self.pub_hint_var,
            font=("Arial", 9),
            fg="#bdc3c7",
            bg="#34495e"
        ).grid(row=2, column=0, columnspan=2, pady=5)

        tk.Button(
            form_frame,
            text="DELETE PUBLICATION",
            font=("Arial", 12, "bold"),
            bg="#c0392b",
            fg="white",
            width=22,
            height=2,
            command=self.confirm_delete_publication
        ).grid(row=3, column=0, columnspan=2, pady=20)

    def _update_pub_hint(self, event=None):
        hints = {
            "Year": "Example  Year: 2022",
            "Type": "Example  Type: Journal or Conference or Review",
            "Faculty Short Name": "Example  Faculty Short Name: MHK",
            "Title Keyword": "Example  Title Keyword: Heat Transfer  (partial match OK)",
        }
        self.pub_hint_var.set(hints.get(self.del_pub_criteria.get(), ""))

    def confirm_delete_publication(self):
        criteria = self.del_pub_criteria.get()
        value = self.del_pub_value.get().strip()

        if not value:
            messagebox.showerror("Error", "Please enter a value to search by.")
            return

        answer = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete all publications where {criteria} = '{value}'?\n"
            "This action cannot be undone."
        )
        if not answer:
            return

        result = self.run_command("DELETE_PUBLICATION", criteria, value)
        if result is None:
            return

        output = (result.stdout or "").strip()

        if "SUCCESS" in output:
            messagebox.showinfo("Deleted", "Publication record(s) deleted successfully!")
            self.show_delete_choice()
        elif "NOT_FOUND" in output:
            messagebox.showwarning("Not Found", f"No publication found where {criteria} = '{value}'.")
        else:
            messagebox.showerror("Error", output or result.stderr or "An unexpected error occurred.")

    def open_search(self):
        self.show_search_options()

    def show_search_options(self):
        self.clear_main_frame()

        tk.Button(
            self.main_frame,
            text="<- Back to Menu",
            font=("Arial", 10),
            bg="#34495e",
            fg="white",
            command=self.show_main_menu
        ).pack(anchor="w", pady=10)

        tk.Label(
            self.main_frame,
            text="SEARCH PUBLICATIONS",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#2c3e50"
        ).pack(pady=20)

        search_frame = tk.Frame(self.main_frame, bg="#34495e", padx=30, pady=30)
        search_frame.pack(pady=10)

        tk.Label(
            search_frame,
            text="Search By:",
            font=("Arial", 11),
            fg="white",
            bg="#34495e"
        ).grid(row=0, column=0, pady=10, sticky="w")

        self.criteria_combo = ttk.Combobox(
            search_frame,
            font=("Arial", 11),
            width=38,
            values=["Faculty Name", "Year", "Publication Type", "Research Topic"],
            state="readonly"
        )
        self.criteria_combo.grid(row=0, column=1, pady=10, padx=10)
        self.criteria_combo.current(0)

        tk.Label(
            search_frame,
            text="Search Term:",
            font=("Arial", 11),
            fg="white",
            bg="#34495e"
        ).grid(row=1, column=0, pady=10, sticky="w")

        self.search_term_entry = tk.Entry(search_frame, font=("Arial", 11), width=40)
        self.search_term_entry.grid(row=1, column=1, pady=10, padx=10)

        tk.Button(
            search_frame,
            text="SEARCH",
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            width=20,
            height=2,
            command=self.perform_search
        ).grid(row=2, column=0, columnspan=2, pady=20)

    def perform_search(self):
        criteria = self.criteria_combo.get()
        term = self.search_term_entry.get().strip()

        if not term:
            messagebox.showerror("Error", "Please enter a search term")
            return

        result = self.run_command("SEARCH_PUB", criteria, term)
        if result is None:
            return

        self.show_search_results(result.stdout)

    def show_search_results(self, results):
        self.clear_main_frame()

        tk.Button(
            self.main_frame,
            text="<- Back to Search",
            font=("Arial", 10),
            bg="#34495e",
            fg="white",
            command=self.show_search_options
        ).pack(anchor="w", pady=10)

        tk.Label(
            self.main_frame,
            text="SEARCH RESULTS",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#2c3e50"
        ).pack(pady=10)

        text_frame = tk.Frame(self.main_frame, bg="black")
        text_frame.pack(fill="both", expand=True, padx=20, pady=10)

        text_area = tk.Text(text_frame, bg="black", fg="white", font=("Courier", 10), wrap="none")
        sy = tk.Scrollbar(text_frame, orient="vertical", command=text_area.yview)
        sx = tk.Scrollbar(text_frame, orient="horizontal", command=text_area.xview)

        text_area.configure(yscrollcommand=sy.set, xscrollcommand=sx.set)
        text_area.pack(side="left", fill="both", expand=True)
        sy.pack(side="right", fill="y")
        sx.pack(side="bottom", fill="x")

        text_area.insert("1.0", results)
        text_area.config(state="disabled")

    def open_reports(self):
        self.show_report_options()

    def show_report_options(self):
        self.clear_main_frame()

        tk.Button(
            self.main_frame,
            text="<- Back to Menu",
            font=("Arial", 10),
            bg="#34495e",
            fg="white",
            command=self.show_main_menu
        ).pack(anchor="w", pady=10)

        tk.Label(
            self.main_frame,
            text="GENERATE REPORTS",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#2c3e50"
        ).pack(pady=20)

        report_frame = tk.Frame(self.main_frame, bg="#34495e", padx=30, pady=30)
        report_frame.pack(pady=10)

        reports = [
            ("Faculty Information", "faculty_info"),
            ("Faculty-wise Publications", "faculty_pub"),
            ("Year-wise Publications", "year_pub"),
            ("Publication Type Summary", "type_summary"),
            ("Department Statistics", "dept_stats"),
        ]

        for i, (text, rtype) in enumerate(reports):
            tk.Button(
                report_frame,
                text=text,
                font=("Arial", 12),
                bg="#9b59b6",
                fg="white",
                width=28,
                height=2,
                command=lambda rt=rtype: self.generate_report(rt)
            ).grid(row=i, column=0, pady=8)

    def generate_report(self, report_type):
        result = self.run_command("GENERATE_REPORT", report_type)
        if result is None:
            return

        self.show_report_results(result.stdout, report_type)

    def show_report_results(self, results, report_type):
        self.clear_main_frame()

        tk.Button(
            self.main_frame,
            text="<- Back to Reports",
            font=("Arial", 10),
            bg="#34495e",
            fg="white",
            command=self.show_report_options
        ).pack(anchor="w", pady=10)

        tk.Label(
            self.main_frame,
            text="REPORT RESULTS",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#2c3e50"
        ).pack(pady=10)

        text_frame = tk.Frame(self.main_frame, bg="black")
        text_frame.pack(fill="both", expand=True, padx=20, pady=10)

        text_area = tk.Text(text_frame, bg="black", fg="white", font=("Courier", 10), wrap="none")
        sy = tk.Scrollbar(text_frame, orient="vertical", command=text_area.yview)
        sx = tk.Scrollbar(text_frame, orient="horizontal", command=text_area.xview)

        text_area.configure(yscrollcommand=sy.set, xscrollcommand=sx.set)
        text_area.pack(side="left", fill="both", expand=True)
        sy.pack(side="right", fill="y")
        sx.pack(side="bottom", fill="x")

        text_area.insert("1.0", results)
        text_area.config(state="disabled")

        tk.Button(
            self.main_frame,
            text="Export Report",
            font=("Arial", 11),
            bg="#3498db",
            fg="white",
            command=lambda: self.export_report(results)
        ).pack(pady=10)

    def export_report(self, content):
        report_path = os.path.join(self.base_dir, "report.txt")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(content)
        messagebox.showinfo("Success", f"Report exported as\n{report_path}")

    def save_exit(self):
        result = self.run_command("SAVE_DATA")
        if result is not None:
            if "SUCCESS" in result.stdout:
                messagebox.showinfo("Success", result.stdout.strip())
            else:
                messagebox.showerror("Error", result.stdout.strip())

        self.root.quit()
        sys.exit(0)

    def logout(self):
        self.root.destroy()
        import login_gui
        root = tk.Tk()
        login_gui.LoginGUI(root)
        root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainGUI(root, "admin")
    root.mainloop()