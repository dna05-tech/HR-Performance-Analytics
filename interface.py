import matplotlib.pyplot as plt
import customtkinter as ctk
import csv
import os
from datetime import datetime
from tkinter import messagebox, ttk
from matplotlib.lines import Line2D
import matplotlib.font_manager as fm

# --- LIBRARY DEPENDENCY CHECK ---
try:
    import seaborn as sns
    has_seaborn = True
except ImportError:
    has_seaborn = False
    print("System Notification: Seaborn library not detected. Using standard visualization engine.")

# UI Theme Configuration
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class HRSystem(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("HR Performance Analytics Suite v9.3") 
        self.geometry("500x920") 
        self.resizable(False, False)
        
        # Initialize the application with the Login Interface
        self.show_login_screen()

    def clear_screen(self):
        """Utility to remove all widgets from the active window for screen transitions."""
        for widget in self.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        """Renders the Secure Access Gateway (Login Screen)."""
        self.clear_screen()
        
        # Header Section
        self.header = ctk.CTkLabel(
            self, 
            text="SECURE ACCESS GATEWAY", 
            font=("Roboto", 22, "bold")
        )
        self.header.pack(pady=(60, 30))

        # Credentials Input
        self.username_entry = ctk.CTkEntry(
            self, 
            placeholder_text="Username", 
            width=280, 
            height=40
        )
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(
            self, 
            placeholder_text="Password", 
            show="*", 
            width=280, 
            height=40
        )
        self.password_entry.pack(pady=10)
        
        # Bind 'Enter' key to trigger login
        self.password_entry.bind("<Return>", lambda e: self.handle_login())

        # Authentication Button
        self.login_button = ctk.CTkButton(
            self, 
            text="LOGIN", 
            command=self.handle_login, 
            width=200, 
            height=45,
            font=("Roboto", 14, "bold")
        )
        self.login_button.pack(pady=30)
        
        # Dynamic Error Message Display
        self.error_msg = ctk.CTkLabel(
            self, 
            text="", 
            font=("Roboto", 11), 
            text_color="#ff4d4d"
        )
        self.error_msg.pack(pady=5)

        # --- SIGNATURE 1: LOGIN SCREEN ---
        self.footer = ctk.CTkLabel(
            self, 
            text="Engineered by D.N.A. | v9.3", 
            font=("Consolas", 10), 
            text_color="gray50"
        )
        self.footer.pack(side="bottom", pady=15)

    def handle_login(self):
        """Authenticates the user against hardcoded credentials."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        print(f"Auth Log: Login attempt detected for user: '{username}'")
        
        if username == "dna05" and password == "project2026":
            self.header.configure(text="✓ ACCESS GRANTED", text_color="#2ecc71")
            self.error_msg.configure(text="")
            self.after(800, self.show_analysis_dashboard)
        else:
            self.header.configure(text="✗ ACCESS DENIED", text_color="#e74c3c")
            self.error_msg.configure(text="Invalid credentials. Access prohibited.")
            self.password_entry.delete(0, 'end')

    def show_analysis_dashboard(self):
        """Renders the main Performance Analytics Dashboard."""
        self.clear_screen()
        
        ctk.CTkLabel(
            self, 
            text="PERFORMANCE ANALYSIS DASHBOARD", 
            font=("Roboto", 18, "bold")
        ).pack(pady=20)

        # Metric Input Fields
        self.emp_id = ctk.CTkEntry(
            self, 
            placeholder_text="Employee Name / ID", 
            width=350, 
            height=35
        )
        self.emp_id.pack(pady=5)
        
        self.eff_val = ctk.CTkEntry(
            self, 
            placeholder_text="Efficiency Score (0-100)", 
            width=350, 
            height=35
        )
        self.eff_val.pack(pady=5)
        
        self.speed_val = ctk.CTkEntry(
            self, 
            placeholder_text="Speed Factor (1.0-2.0)", 
            width=350, 
            height=35
        )
        self.speed_val.pack(pady=5)
        
        self.success_val = ctk.CTkEntry(
            self, 
            placeholder_text="Success Rate (0-100)", 
            width=350, 
            height=35
        )
        self.success_val.pack(pady=5)

        # --- COMMAND CENTER (BUTTONS) ---
        
        # 1. Calculation
        ctk.CTkButton(
            self, 
            text="GENERATE STRATEGIC REPORT", 
            command=self.process_analysis, 
            fg_color="#27ae60", 
            hover_color="#2ecc71", 
            width=250, 
            height=45
        ).pack(pady=15)
        
        # 2. Visualization
        ctk.CTkButton(
            self, 
            text="SHOW COMPANY ANALYTICS", 
            command=self.show_statistics, 
            fg_color="#2980b9", 
            hover_color="#3498db", 
            width=250, 
            height=35
        ).pack(pady=5)
        
        # 3. Data Viewer
        ctk.CTkButton(
            self, 
            text="VIEW DATABASE LOGS", 
            command=self.open_log_viewer, 
            fg_color="#8e44ad", 
            hover_color="#9b59b6", 
            width=250, 
            height=35
        ).pack(pady=5)

        # 4. Export
        ctk.CTkButton(
            self, 
            text="EXPORT PDF REPORT", 
            command=self.export_to_pdf, 
            fg_color="#d35400", 
            hover_color="#e67e22", 
            width=250, 
            height=35
        ).pack(pady=5)
        
        # 5. Reset
        ctk.CTkButton(
            self, 
            text="RESET FORM", 
            command=self.clear_inputs, 
            fg_color="gray", 
            hover_color="#95a5a6", 
            width=250, 
            height=30
        ).pack(pady=5)
        
        # 6. Delete (GDPR)
        ctk.CTkButton(
            self, 
            text="DELETE EMPLOYEE DATA", 
            command=self.delete_employee_data, 
            fg_color="#c0392b", 
            hover_color="#e74c3c", 
            width=250, 
            height=30
        ).pack(pady=5)

        # System Status Indicator
        self.result_label = ctk.CTkLabel(
            self, 
            text="System Initialized. Awaiting Data Entry...", 
            font=("Roboto", 13), 
            text_color="gray", 
            wraplength=450
        )
        self.result_label.pack(pady=20)

        # --- SIGNATURE 2: DASHBOARD (UPDATED) ---
        self.footer = ctk.CTkLabel(
            self, 
            text="System Architecture: D.N.A.", 
            font=("Arial", 9), 
            text_color="gray50"
        )
        self.footer.pack(side="bottom", pady=10)
        
        self.ensure_csv_exists()

    def ensure_csv_exists(self):
        """Checks for database existence and initializes schema if missing."""
        if not os.path.exists("performance_logs.csv"):
            with open("performance_logs.csv", mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    "Timestamp", "Employee_ID", "Final_Score", "Status", 
                    "Efficiency", "Speed", "Success", "Company_Avg"
                ])

    # --- SUB-WINDOW: DATA VIEWER ---
    def open_log_viewer(self):
        """Spawns a child window to display logs (Newest on TOP)."""
        if not os.path.exists("performance_logs.csv"):
            self.result_label.configure(text="⚠ Database Error: No logs found.", text_color="#f39c12")
            return

        # Initialize Top-Level Window
        log_window = ctk.CTkToplevel(self)
        log_window.title("System Logs Viewer")
        log_window.geometry("900x530") 
        log_window.grab_set() 

        # Window Header
        ctk.CTkLabel(
            log_window, 
            text="Historical Performance Records (Newest First)", 
            font=("Roboto", 16, "bold")
        ).pack(pady=10)

        # Styling
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview", 
            background="#2b2b2b", 
            foreground="white", 
            fieldbackground="#2b2b2b", 
            rowheight=25
        )
        style.configure(
            "Treeview.Heading", 
            background="#3b3b3b", 
            foreground="white", 
            font=("Roboto", 10, "bold")
        )
        style.map("Treeview", background=[('selected', '#1f538d')])

        # Table Config
        columns = ("Time", "ID", "Score", "Status", "Eff.", "Speed", "Success", "Avg")
        tree = ttk.Treeview(log_window, columns=columns, show="headings", height=15)
        
        # Headings
        tree.heading("Time", text="Timestamp")
        tree.column("Time", width=140)
        tree.heading("ID", text="Employee ID")
        tree.column("ID", width=120)
        tree.heading("Score", text="Final Score")
        tree.column("Score", width=80)
        tree.heading("Status", text="Status")
        tree.column("Status", width=80)
        tree.heading("Eff.", text="Eff.")
        tree.column("Eff.", width=50)
        tree.heading("Speed", text="Spd")
        tree.column("Speed", width=50)
        tree.heading("Success", text="Succ.")
        tree.column("Success", width=50)
        tree.heading("Avg", text="Mkt. Avg")
        tree.column("Avg", width=80)

        # Scrollbar
        scrollbar = ttk.Scrollbar(log_window, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True, padx=20, pady=10)

        # Populate Data (REVERSE ORDER LOGIC)
        with open("performance_logs.csv", 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # '0' inserts the new item at the TOP of the list
                tree.insert("", 0, values=(
                    row['Timestamp'], row['Employee_ID'], row['Final_Score'], 
                    row['Status'], row['Efficiency'], row['Speed'], 
                    row['Success'], row['Company_Avg']
                ))

        # Close Action
        ctk.CTkButton(
            log_window, 
            text="Close Viewer", 
            command=log_window.destroy, 
            fg_color="#c0392b", 
            hover_color="#e74c3c"
        ).pack(pady=10)

        # --- SIGNATURE 2 (Repeated for Table - UPDATED): ---
        ctk.CTkLabel(
            log_window, 
            text="System Architecture: D.N.A.", 
            font=("Arial", 9), 
            text_color="gray50"
        ).pack(side="bottom", pady=5)

    def process_analysis(self):
        """Core Logic: Computes Weighted Score and Updates Database."""
        try:
            emp_id = self.emp_id.get().strip()
            if not emp_id:
                self.result_label.configure(text="⚠ Validation Error: Employee Name is required.", text_color="#f39c12")
                return
            
            eff = float(self.eff_val.get())
            spd = float(self.speed_val.get())
            success = float(self.success_val.get())
            
            if not (0 <= eff <= 100) or not (0 <= success <= 100):
                raise ValueError("Range Error")
            
            real_score = min(((eff * spd + success) / 2), 100)
            
            all_scores = []
            if os.path.exists("performance_logs.csv"):
                with open("performance_logs.csv", mode='r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if 'Final_Score' in row: 
                            try: all_scores.append(float(row['Final_Score']))
                            except: continue
            
            all_scores.append(real_score)
            current_company_avg = sum(all_scores) / len(all_scores)

            if real_score >= 80:
                status = "ELITE"
                color = "#2ecc71"
            elif real_score >= 70:
                status = "STEADY"
                color = "#3498db"
            else:
                status = "CRITICAL"
                color = "#e74c3c"

            diff = real_score - current_company_avg
            comp_txt = f"▲ ABOVE Avg (+{diff:.1f})" if diff > 0 else f"▼ BELOW Avg ({diff:.1f})"
            
            report = (
                f"REPORT FOR: {emp_id}\n"
                f"SCORE: {real_score:.2f} / 100\n"
                f"STATUS: {status}\n"
                f"MARKET AVG: {current_company_avg:.2f} ({comp_txt})"
            )
            self.result_label.configure(text=report, text_color=color)

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("performance_logs.csv", mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    current_time, emp_id, round(real_score, 2), status, 
                    eff, spd, success, round(current_company_avg, 2)
                ])
            
        except ValueError:
            self.result_label.configure(text="⚠ Input Error: Ensure all numeric fields are correct.", text_color="#e67e22")

    def clear_inputs(self):
        self.emp_id.delete(0, 'end')
        self.eff_val.delete(0, 'end')
        self.speed_val.delete(0, 'end')
        self.success_val.delete(0, 'end')
        self.result_label.configure(text="Form Reset. Ready.", text_color="gray")

    def show_statistics(self):
        """Generates the High-Low Company Analytics Chart."""
        if has_seaborn:
            sns.set_theme(style="whitegrid", rc={"axes.facecolor": "#F8F9FA", "grid.color": "#E9ECEF"})
        else:
            plt.style.use('bmh')

        if not os.path.exists("performance_logs.csv"):
            self.result_label.configure(text="⚠ Database not initialized.", text_color="#f39c12")
            return
        
        employee_data = {}
        all_scores = []

        with open("performance_logs.csv", 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    name = row['Employee_ID']
                    score = float(row['Final_Score'])
                    if name not in employee_data: employee_data[name] = []
                    employee_data[name].append(score)
                    all_scores.append(score)
                except: continue
        
        if not employee_data:
            self.result_label.configure(text="⚠ No analytical data available.", text_color="#f39c12")
            return

        color_current = '#E74C3C'
        color_history = '#34495E'
        color_avg = '#F39C12'
        color_bg = '#D5D8DC'

        names = list(employee_data.keys())
        fig, ax = plt.subplots(figsize=(12, 7))
        
        if not has_seaborn: ax.set_facecolor("#F8F9FA")
        company_avg = sum(all_scores) / len(all_scores)

        for i, name in enumerate(names):
            scores = employee_data[name]
            latest_score = scores[-1]
            past_scores = scores[:-1]
            max_score = max(scores)
            
            ax.bar(i, max_score, color=color_bg, width=0.5, alpha=0.3, zorder=1, edgecolor='none')
            for score in past_scores:
                ax.hlines(y=score, xmin=i-0.22, xmax=i+0.22, color=color_history, linewidth=2.5, zorder=2, alpha=0.8)
            ax.hlines(y=latest_score, xmin=i-0.28, xmax=i+0.28, color=color_current, linewidth=7, zorder=3, alpha=0.3)
            ax.hlines(y=latest_score, xmin=i-0.28, xmax=i+0.28, color=color_current, linewidth=4, zorder=4)
            ax.text(i, latest_score + 2, f"{latest_score:.1f}", ha='center', va='bottom', fontsize=10, fontweight='bold', color=color_current)

        ax.axhline(y=company_avg, color=color_avg, linestyle='--', linewidth=2, alpha=0.9)
        
        if has_seaborn: sns.despine(left=True, bottom=True)
        else:
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
        
        ax.tick_params(axis='both', colors='#7F8C8D', labelsize=10)
        ax.set_xticks(range(len(names)))
        ax.set_xticklabels(names, rotation=30, ha='right')
        ax.set_ylabel("Performance Score (0-100)", color='#7F8C8D', labelpad=10)
        ax.set_title("Executive Performance Summary: History & Current Status", fontsize=14, fontweight='bold', pad=20, color='#2C3E50')
        ax.set_ylim(0, 118)
        
        custom_lines = [
            Line2D([0], [0], color=color_current, lw=4),
            Line2D([0], [0], color=color_history, lw=2.5, alpha=0.8),
            Line2D([0], [0], color=color_avg, linestyle='--', lw=2)
        ]
        legend = ax.legend(custom_lines, ['Current Status (Latest)', 'Historical Records', f'Company Avg ({company_avg:.1f})'], loc='upper right', frameon=False, fontsize=10)
        for text in legend.get_texts(): text.set_color('#7F8C8D')

        plt.tight_layout()
        plt.show()
        self.result_label.configure(text="✓ Analytics Chart Generated Successfully.", text_color="#2ecc71")

    
    
    def export_to_pdf(self):
        """Generates a professional PDF Report (Full Size Chart, Single Page)."""
        try:
            from fpdf import FPDF
            import matplotlib.pyplot as plt
            
            name = self.emp_id.get().strip()
            if not name:
                self.result_label.configure(text="⚠ Error: Employee Name required.", text_color="#f39c12")
                return

            timestamps, efficiency, success, total_score, company_avg, speed = [], [], [], [], [], []
            
            if os.path.exists("performance_logs.csv"):
                with open("performance_logs.csv", 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if row['Employee_ID'] == name:
                            try:
                                full_time = row['Timestamp']
                                short_time = full_time[5:16] 
                                timestamps.append(short_time)
                                efficiency.append(float(row['Efficiency']))
                                success.append(float(row['Success']))
                                total_score.append(float(row['Final_Score']))
                                company_avg.append(float(row['Company_Avg']))
                                speed.append(float(row['Speed']))
                            except: continue

            chart_filename = None
            if len(total_score) > 0:
                x_pos = range(len(timestamps))
                
                # --- CHART CONFIGURATION: Full Size (10x5 inches) ---
                fig, ax1 = plt.subplots(figsize=(10, 5))

                ax1.set_xlabel('Timeline (Entry Sequence)')
                ax1.set_ylabel('Score (0-100)', color='#333333')
                
                l1, = ax1.plot(x_pos, total_score, marker='o', color='#e74c3c', linewidth=3, label='Total Score')
                l2, = ax1.plot(x_pos, efficiency, marker='x', color='#3498db', linestyle=':', label='Efficiency')
                l3, = ax1.plot(x_pos, success, marker='s', color='#2ecc71', linestyle=':', label='Success')
                l4, = ax1.plot(x_pos, company_avg, color='gray', linestyle='--', label='Avg')
                
                ax1.tick_params(axis='y', labelcolor='#333333')
                ax1.grid(True, alpha=0.3, linestyle='--')
                plt.xticks(x_pos, timestamps, rotation=45, ha='right', fontsize=8)

                ax2 = ax1.twinx()
                ax2.set_ylabel('Speed Factor', color='#8e44ad')
                l5, = ax2.plot(x_pos, speed, marker='^', color='#8e44ad', linestyle='-.', linewidth=2, label='Speed')
                ax2.tick_params(axis='y', labelcolor='#8e44ad')
                ax2.set_ylim(0, 3.5)

                lines = [l1, l2, l3, l4, l5]
                labels = [l.get_label() for l in lines]
                ax1.legend(lines, labels, loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=5, fontsize='small')

                plt.title(f"Performance Trends: {name}", y=1.15, fontsize=12, fontweight='bold')
                plt.tight_layout()
                
                chart_filename = "temp_multi_chart.png"
                plt.savefig(chart_filename, dpi=100)
                plt.close()

            # --- PDF GENERATION LOGIC ---
            pdf = FPDF()
            
            # Disable automatic page break to force single-page layout
            pdf.set_auto_page_break(auto=False, margin=0)
            
            pdf.add_page()
            
            # Header Section
            pdf.set_y(10) 
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, "STRATEGIC HR REPORT", ln=True, align='C')
            
            # Timestamp
            pdf.set_font("Arial", 'I', 10)
            pdf.cell(0, 5, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align='C')
            
            # Employee Details
            pdf.ln(5) 
            pdf.set_font("Arial", size=12)
            pdf.cell(0, 8, f"Employee: {name}", ln=True)
            if total_score:
                pdf.cell(0, 8, f"Latest Score: {total_score[-1]} / 100", ln=True)
            
            # Chart Placement (Full width)
            pdf.ln(2)
            if chart_filename:
                pdf.image(chart_filename, x=10, w=190)
            
            # Signature Footer (Fixed at the bottom of the page)
            pdf.set_y(-15)
            pdf.set_font("Arial", 'I', 8)
            pdf.cell(0, 10, "Secure HR Analytics v9.3 | Engineered by Defne Nil | Confidential", align='C')
            
            out_file = f"Report_{name}.pdf"
            pdf.output(out_file)
            
            if chart_filename and os.path.exists(chart_filename):
                os.remove(chart_filename)
            
            self.result_label.configure(text=f"✓ PDF Report Exported: {out_file}", text_color="#27ae60")

        except Exception as e:
            print(f"Error: {e}")
            self.result_label.configure(text="System Error: Check Terminal", text_color="#e74c3c")         

    def delete_employee_data(self):
        """GDPR Compliant Deletion with Official Warning Icon."""
        target_name = self.emp_id.get().strip()
        
        if not target_name:
            self.result_label.configure(text="⚠ Error: Enter Employee ID", text_color="#f39c12")
            return
            
        if not os.path.exists("performance_logs.csv"): 
            self.result_label.configure(text="Error: Database not found.", text_color="gray")
            return

        # official warning icon
        confirm = messagebox.askyesno(
            title="SECURITY WARNING",
            message=f"CRITICAL ACTION:\n\nAre you sure you want to PERMANENTLY delete all records for:\n'{target_name}'?\n\nThis action cannot be undone.",
            icon='warning'
        )

        if not confirm:
            self.result_label.configure(text="Action Cancelled. Data Safe.", text_color="gray")
            return

        try:
            rows = []
            deleted_count = 0
            
            with open("performance_logs.csv", mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['Employee_ID'] != target_name:
                        rows.append(row)
                    else:
                        deleted_count += 1
            
            if deleted_count > 0:
                with open("performance_logs.csv", mode='w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=[
                        "Timestamp", "Employee_ID", "Final_Score", "Status",
                        "Efficiency", "Speed", "Success", "Company_Avg"
                    ])
                    writer.writeheader()
                    writer.writerows(rows)
                
                self.clear_inputs()
                self.result_label.configure(text=f"✓ SUCCESS: {deleted_count} records deleted.", text_color="#c0392b")
                messagebox.showinfo("Deletion Complete", f"All data for '{target_name}' has been wiped.")
            else:
                messagebox.showwarning("Not Found", f"User '{target_name}' not found.")
                
        except Exception as e:
            self.result_label.configure(text="Critical System Error.", text_color="orange")
            print(f"Error: {e}")

if __name__ == "__main__":
    app = HRSystem()
    app.mainloop()
           