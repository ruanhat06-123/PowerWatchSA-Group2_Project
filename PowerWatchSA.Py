import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# --- Helper functions (reuse your existing logic) ---
def to_time(time_str):
    return datetime.strptime(time_str, "%H:%M")

def calculate_overrun(scheduled_start, scheduled_end, actual_start, actual_end):
    sched_start = to_time(scheduled_start)
    sched_end = to_time(scheduled_end)
    actual_start_dt = to_time(actual_start)
    actual_end_dt = to_time(actual_end)

    sched_duration = (sched_end - sched_start).total_seconds() / 60
    actual_duration = (actual_end_dt - actual_start_dt).total_seconds() / 60
    overrun = actual_duration - sched_duration
    return int(overrun) if overrun > 0 else 0

def generate_log_id(outage_logs):
    last_id = outage_logs["LogID"][-1]
    number = int(last_id.split("-")[1])
    return f"LOG-{number+1:03d}"

# --- Example data (shortened for demo) ---
OutageLog = {
    "LogID": ["LOG-010"],
    "Date": ["2025-04-07"],
    "Area": ["Boksburg"],
    "Block": [4],
    "Stage": [3],
    "ScheduledStart": ["22:00"],
    "ScheduledEnd": ["00:30"],
    "ActualStart": ["22:10"],
    "ActualEnd": ["01:30"],
    "Overrun": [60],
    "Monitor": ["Kagiso Sithole"]
}

ImpactReports = {
    "ImpactID": ["IMP-003"],
    "LogID": ["LOG-004"],
    "MemberID": ["PW-005"],
    "ImpactType": ["Financial"],
    "Description": ["Hair salon lost 4 clients"],
    "Loss": [800]
}

CommunityMembers = {
    "ID": ["PW-001","PW-010"],
    "Name": ["Nomsa Dlamini","Lerato Sithole"],
    "Area": ["Boksburg","Boksburg"],
    "Block": [4,4],
    "Vulnerable": ["Oxygen machine","Dialysis patient"]
}

# --- GUI Functions ---
def log_outage_gui():
    log_id = generate_log_id(OutageLog)
    date = date_entry.get()
    area = area_entry.get()
    block = int(block_entry.get())
    stage = int(stage_entry.get())
    scheduled_start = sched_start_entry.get()
    scheduled_end = sched_end_entry.get()
    actual_start = actual_start_entry.get()
    actual_end = actual_end_entry.get()
    monitor = monitor_entry.get()

    overrun = calculate_overrun(scheduled_start, scheduled_end, actual_start, actual_end)

    OutageLog["LogID"].append(log_id)
    OutageLog["Date"].append(date)
    OutageLog["Area"].append(area)
    OutageLog["Block"].append(block)
    OutageLog["Stage"].append(stage)
    OutageLog["ScheduledStart"].append(scheduled_start)
    OutageLog["ScheduledEnd"].append(scheduled_end)
    OutageLog["ActualStart"].append(actual_start)
    OutageLog["ActualEnd"].append(actual_end)
    OutageLog["Overrun"].append(overrun)
    OutageLog["Monitor"].append(monitor)

    messagebox.showinfo("Log Outage", f"Outage logged successfully!\nID: {log_id}\nOverrun: {overrun} mins")

def view_flagged_logs():
    flagged = [f"{OutageLog['LogID'][i]} in {OutageLog['Area'][i]} Block {OutageLog['Block'][i]} "
               f"overran by {OutageLog['Overrun'][i]} mins"
               for i in range(len(OutageLog["LogID"])) if OutageLog["Overrun"][i] > 30]
    messagebox.showinfo("Flagged Logs", "\n".join(flagged) if flagged else "No flagged logs.")

def view_financial_loss():
    total_loss = sum(loss for loss in ImpactReports["Loss"] if isinstance(loss, int))
    messagebox.showinfo("Financial Loss", f"Total loss: R{total_loss}")

# --- GUI Layout ---
root = tk.Tk()
root.title("PowerWatchSA")

# Input fields
tk.Label(root, text="Date (YYYY-MM-DD)").grid(row=0, column=0)
date_entry = tk.Entry(root); date_entry.grid(row=0, column=1)

tk.Label(root, text="Area").grid(row=1, column=0)
area_entry = tk.Entry(root); area_entry.grid(row=1, column=1)

tk.Label(root, text="Block").grid(row=2, column=0)
block_entry = tk.Entry(root); block_entry.grid(row=2, column=1)

tk.Label(root, text="Stage").grid(row=3, column=0)
stage_entry = tk.Entry(root); stage_entry.grid(row=3, column=1)

tk.Label(root, text="Scheduled Start").grid(row=4, column=0)
sched_start_entry = tk.Entry(root); sched_start_entry.grid(row=4, column=1)

tk.Label(root, text="Scheduled End").grid(row=5, column=0)
sched_end_entry = tk.Entry(root); sched_end_entry.grid(row=5, column=1)

tk.Label(root, text="Actual Start").grid(row=6, column=0)
actual_start_entry = tk.Entry(root); actual_start_entry.grid(row=6, column=1)

tk.Label(root, text="Actual End").grid(row=7, column=0)
actual_end_entry = tk.Entry(root); actual_end_entry.grid(row=7, column=1)

tk.Label(root, text="Monitor").grid(row=8, column=0)
monitor_entry = tk.Entry(root); monitor_entry.grid(row=8, column=1)

# Buttons
tk.Button(root, text="Log Outage", command=log_outage_gui).grid(row=9, column=0, pady=10)
tk.Button(root, text="View Flagged Logs", command=view_flagged_logs).grid(row=9, column=1, pady=10)
tk.Button(root, text="View Financial Loss", command=view_financial_loss).grid(row=10, column=0, pady=10)
tk.Button(root, text="Exit", command=root.quit).grid(row=10, column=1, pady=10)

root.mainloop()
