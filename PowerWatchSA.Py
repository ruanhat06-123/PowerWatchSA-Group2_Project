from datetime import datetime

#Data Design
#The data design for PowerWatchSA is built using dictionaries.

# Loadshedding Stages
Stages = {
    "Stage": [1, 2, 3, 4, 5, 6],
    "MW Shed": [1000, 2000, 3000, 4000, 5000, 6000],
    "Hours Off": [2, 4, 6, 8.5, 10.5, 12],
    "Blocks": ["1 block/day", "2 blocks/day", "2-3 blocks/day",
               "3 blocks/day", "4 blocks/day", "4-5 blocks/day"],
    "Severity": ["Low", "Moderate", "Significant", "Severe", "Critical", "Emergency"]
}

# Registered Community Members
CommunityMembers = {
    "ID": ["PW-001","PW-002","PW-003","PW-004","PW-005",
           "PW-006","PW-007","PW-008","PW-009","PW-010"],
    "Name": ["Nomsa Dlamini","Sipho's Spaza Shop","Benoni Auto Repair","Thandi Mokoena",
             "Katlego's Hair Salon","St Francis Primary School","Patrick van Wyk",
             "Duduza Clinic","Zanele's Catering","Lerato Sithole"],
    "Type": ["Household","Spaza shop","SME","Household","SME",
             "School","Household","Healthcare","SME","Household"],
    "Area": ["Boksburg","Benoni","Benoni","Germiston","Boksburg",
             "Boksburg","Germiston","Germiston","Benoni","Boksburg"],
    "Block": [4,7,7,2,4,4,2,2,7,4],
    "Generator": ["No","No","Yes","No","No","No","No","Yes","No","No"],
    "Solar": [False,False,False,False,False,False,True,False,False,False],
    "Vulnerable": ["Oxygen machine","None","None","None","None",
                   "None","None","Medical fridges","None","Dialysis patient"]
}

# Outage Log
OutageLog = {
    "LogID": ["LOG-001","LOG-002","LOG-003","LOG-004","LOG-005",
              "LOG-006","LOG-007","LOG-008","LOG-009","LOG-010"],
    "Date": ["2025-04-01","2025-04-01","2025-04-02","2025-04-02","2025-04-03",
             "2025-04-04","2025-04-04","2025-04-05","2025-04-06","2025-04-07"],
    "Area": ["Boksburg","Benoni","Germiston","Boksburg","Benoni",
             "Germiston","Boksburg","Benoni","Germiston","Boksburg"],
    "Block": [4,7,2,4,7,2,4,7,2,4],
    "Stage": [3,3,3,3,4,4,4,2,2,3],
    "ScheduledStart": ["06:00","10:00","14:00","18:00","02:00",
                       "06:00","10:00","14:00","18:00","22:00"],
    "ScheduledEnd": ["08:30","12:30","16:30","20:30","06:30",
                     "10:30","14:30","16:00","20:00","00:30"],
    "ActualStart": ["06:05","10:10","14:00","18:15","02:00",
                    "06:00","10:30","14:00","17:55","22:10"],
    "ActualEnd": ["09:15","12:35","17:20","21:45","06:30",
                  "11:50","15:20","16:05","20:45","01:30"],
    "Overrun": [45,5,50,75,0,80,50,5,45,60],
    "Monitor": ["Kagiso Sithole","Ayanda Dube","Nomvula Nkosi","Kagiso Sithole","Ayanda Dube",
                "Nomvula Nkosi","Kagiso Sithole","Ayanda Dube","Nomvula Nkosi","Kagiso Sithole"]
}

# Impact Reports
ImpactReports = {
    "ImpactID": ["IMP-001","IMP-002","IMP-003","IMP-004","IMP-005","IMP-006","IMP-007"],
    "LogID": ["LOG-001","LOG-001","LOG-004","LOG-004","LOG-006","LOG-007","LOG-010"],
    "MemberID": ["PW-001","PW-006","PW-005","PW-002","PW-008","PW-005","PW-010"],
    "ImpactType": ["Medical","Education","Financial","Financial","Medical","Financial","Medical"],
    "Description": [
        "Oxygen machine lost power for 70 mins - family distressed",
        "Morning computer class cancelled - 45 learners affected",
        "Hair salon lost 4 clients during evening overrun",
        "Spaza fridge off 3+ hours - cold drinks spoiled",
        "Clinic generator kicked in but medical fridge alarmed twice",
        "Hair salon closed entire morning shift",
        "Dialysis patient could not complete home treatment"
    ],
    "Loss": ["N/A","N/A",800,1200,"N/A",1500,"N/A"]
}


#Functions for PowerWatchSA

# Last Log ID
def last_id(outage_logs):
    return outage_logs["LogID"][-1]
# Count logs
def count_logs(outage_logs):
    return len(outage_logs["LogID"])

# Automatically generate the next Log ID
def generate_log_id(log_count):
    # Get the last log ID in the list
    last_id = OutageLog["LogID"][-1]   # e.g. "LOG-010"
    
    # Extract the number part and increment
    number = int(last_id.split("-")[1])
    new_number = number + 1
    
    # Format with leading zeros (e.g. LOG-011)
    return f"LOG-{new_number:03d}"

# Calculate overrun time in minutes
def calculate_overrun(scheduled_start, scheduled_end, actual_start, actual_end):
    # Convert strings to datetime objects
    sched_start = to_time(scheduled_start)
    sched_end = to_time(scheduled_end)
    actual_start_dt = to_time(actual_start)
    actual_end_dt = to_time(actual_end)

    # Calculate durations in minutes
    sched_duration = (sched_end - sched_start).total_seconds() / 60
    actual_duration = (actual_end_dt - actual_start_dt).total_seconds() / 60

    # Overrun = actual duration - scheduled duration
    overrun = actual_duration - sched_duration
    return int(overrun) if overrun > 0 else 0

#Convert string time input to datetime object
def to_time(time_str):
    return datetime.strptime(time_str, "%H:%M")

# Add log entry to OutageLog
def log_outage(log_id, date, area, block, stage,
               scheduled_start, scheduled_end,
               actual_start, actual_end, monitor):
    # Use the new calculate_overrun with start + end times
    overrun = calculate_overrun(scheduled_start, scheduled_end,
                                actual_start, actual_end)

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

    return f"Outage logged successfully. Overrun = {overrun} minutes."


# Generate alerts for vulnerable members when an overrun occurs
def flag_vulnerable_alerts(area, block, overrun_minutes):
    alerts = []
    if overrun_minutes > 30:  # only trigger alerts if overrun is significant
        for i in range(len(CommunityMembers["ID"])):
            if CommunityMembers["Area"][i] == area and CommunityMembers["Block"][i] == block:
                if CommunityMembers["Vulnerable"][i] != "None":
                    alerts.append(
                        f"Alert: {CommunityMembers['Name'][i]} at risk due to {CommunityMembers['Vulnerable'][i]}"
                    )
    return alerts


# Produce a summary of outages for a given block and area
def get_block_summary(area, block, outage_logs):
    summary = {
        "ScheduledHours": 0,
        "ActualHours": 0,
        "Overruns": 0,
        "TotalOverrunMinutes": 0
    }
    for i in range(len(outage_logs["LogID"])):
        if outage_logs["Area"][i] == area and outage_logs["Block"][i] == block:
            overrun = outage_logs["Overrun"][i]
            summary["TotalOverrunMinutes"] += overrun
            if overrun > 30:
                summary["Overruns"] += 1
            # Hours can be estimated from scheduled vs actual times if needed
            # For now, just count overruns and minutes
    return summary


# Calculate total financial loss from impact reports
def calculate_financial_loss(impact_reports):
    total_loss = 0
    for loss in impact_reports["Loss"]:
        if loss != "N/A":
            total_loss += int(loss)
    return total_loss


# Generate a formatted complaint report for overruns >30 mins
def generate_complaint_report(outage_logs, impact_reports, community_members):
    report = "Complaint Report:\n"
    for i in range(len(outage_logs["LogID"])):
        if outage_logs["Overrun"][i] > 30:
            log_id = outage_logs["LogID"][i]
            area = outage_logs["Area"][i]
            block = outage_logs["Block"][i]
            report += f"\nLog {log_id} in {area}, Block {block} overran by {outage_logs['Overrun'][i]} mins."
            # Check impacts linked to this outage
            for j in range(len(impact_reports["LogID"])):
                if impact_reports["LogID"][j] == log_id:
                    member_id = impact_reports["MemberID"][j]
                    member_name = community_members["Name"][community_members["ID"].index(member_id)]
                    report += f"\n - Impact on {member_name}: {impact_reports['Description'][j]}"
    return report


#Menu
while True:
    print("\n--- PowerWatchSA Menu ---")
    print("1. Log outage")
    print("2. View flagged logs")
    print("3. View block summary")
    print("4. View financial losses")
    print("5. Generate complaint report")
    print("6. Exit")
    
    # User Choise
    choice = input("Enter choice: ")

    # Outputs for user inputs
    if choice == "1":
        log_id = input("Enter log ID: ")
        date = input("Enter date (YYYY-MM-DD): ")
        area = input("Enter area: ")
        block = int(input("Enter block: "))
        stage = int(input("Enter stage (1-6): "))
        scheduled_start = input("Enter scheduled start time (HH:MM): ")
        scheduled_end = input("Enter scheduled end time (HH:MM): ")
        actual_start = input("Enter actual start time (HH:MM): ")
        actual_end = input("Enter actual end time (HH:MM): ")
        monitor = input("Enter monitor name: ")
        log_outage(log_id, date, area, block, stage, scheduled_start, scheduled_end,
                   actual_start, actual_end, monitor)
        print("Outage logged successfully.")
    elif choice == "2":
        print("Flagged logs (overruns >30 mins):")
        for i in range(len(OutageLog["LogID"])):
            if OutageLog["Overrun"][i] > 30:
                print(f"{OutageLog['LogID'][i]} in {OutageLog['Area'][i]} Block {OutageLog['Block'][i]} "
                      f"overran by {OutageLog['Overrun'][i]} mins")
    elif choice == "3":
        area = input("Enter area: ")
        block = int(input("Enter block: "))
        summary = get_block_summary(area, block, OutageLog)
        print(summary)
    elif choice == "4":
        print(f"Total financial loss: R{calculate_financial_loss(ImpactReports)}")
    elif choice == "5":
        print(generate_complaint_report(OutageLog, ImpactReports, CommunityMembers))
    elif choice == "6":
        print("Exiting PowerWatchSA...")
        break
    else:
        print("Invalid choice, try again.")