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

def create_area_list():
    area_list = []
    for area in CommunityMembers["Area"]:
        if area not in area_list:
            area_list.append(area)
    return area_list

# Last Log ID
def last_id(outage_logs):
    return outage_logs["LogID"][-1]
# Count logs
def count_logs(outage_logs):
    return len(outage_logs["LogID"])

# Automatically generate the next Log ID
def generate_log_id(outage_logs):
    last_id = outage_logs["LogID"][-1]   # e.g. "LOG-010"
    number = int(last_id.split("-")[1])
    return f"LOG-{number+1:03d}"

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
def log_outage(date, area, block, stage,
               scheduled_start, scheduled_end,
               actual_start, actual_end, monitor):
    # Auto-generate log ID
    log_id = generate_log_id(OutageLog)

    # Use the new calculate_overrun with start + end times
    overrun = calculate_overrun(scheduled_start, scheduled_end,
                                actual_start, actual_end)

    OutageLog["LogID"].append(log_id)
    OutageLog["Date"].append(date.strip())
    OutageLog["Area"].append(area.strip().title())  # standardise
    OutageLog["Block"].append(block)
    OutageLog["Stage"].append(stage)
    OutageLog["ScheduledStart"].append(scheduled_start.strip())
    OutageLog["ScheduledEnd"].append(scheduled_end.strip())
    OutageLog["ActualStart"].append(actual_start.strip())
    OutageLog["ActualEnd"].append(actual_end.strip())
    OutageLog["Overrun"].append(overrun)
    OutageLog["Monitor"].append(monitor.strip().title())

    print(f"Outage logged successfully with ID {log_id}. Overrun = {overrun} minutes.")

    # Immediately flag vulnerable alerts
    alerts = flag_vulnerable_alerts(area, block, overrun)
    for alert in alerts:
        print(alert)


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
def get_block_summary(area, block, outage_logs, impact_reports, community_members):
    print(f"\n=== Block Summary for {area.title()}, Block {block} ===")

    # Table header
    header = f"{'Member':<30} | {'Impact':<60}"
    print(header)
    print("-" * len(header))

    found = False
    for i in range(len(outage_logs["LogID"])):
        if outage_logs["Area"][i].strip().title() == area.strip().title() and outage_logs["Block"][i] == block:
            if outage_logs["Overrun"][i] > 30:
                log_id = outage_logs["LogID"][i]

                # Find linked impacts
                for j in range(len(impact_reports["LogID"])):
                    if impact_reports["LogID"][j] == log_id:
                        found = True
                        member_id = impact_reports["MemberID"][j]
                        member_name = community_members["Name"][community_members["ID"].index(member_id)]
                        description = impact_reports["Description"][j]

                        row = f"{member_name:<30} | {description:<60}"
                        print(row)

    if not found:
        print("No affected members found for this block.")


# Calculate total financial loss from impact reports
def calculate_financial_loss(impact_reports):
    total_loss = 0
    for loss in impact_reports["Loss"]:
        if loss != "N/A":
            total_loss += int(loss)
    return total_loss


# Generate a formatted complaint report showing only affected members and impacts
def generate_complaint_report(outage_logs, impact_reports, community_members):
    print("\n=== Complaint Report (Affected Members & Impacts) ===")

    # Table header
    header = f"{'Member':<30} | {'Impact':<100}"
    print(header)
    print("-" * len(header))

    found = False
    for i in range(len(outage_logs["LogID"])):
        if outage_logs["Overrun"][i] > 30:
            log_id = outage_logs["LogID"][i]

            # Find linked impacts
            for j in range(len(impact_reports["LogID"])):
                if impact_reports["LogID"][j] == log_id:
                    found = True
                    member_id = impact_reports["MemberID"][j]
                    member_name = community_members["Name"][community_members["ID"].index(member_id)]
                    description = impact_reports["Description"][j]

                    row = f"{member_name:<30} | {description:<100}"
                    print(row)

    if not found:
        print("No affected members found for overruns greater than 30 minutes.")




# Print all flagged logs in a table format
def print_all_flagged_logs(outage_logs):
    print("\n=== All Flagged Logs (Overruns > 30 mins) ===")

    # Table header
    header = f"{'Log ID':<10} | {'Date':<12} | {'Area':<12} | {'Block':<6} | {'Stage':<6} | {'Scheduled':<15} | {'Actual':<15} | {'Overrun(mins)':<15} | {'Monitor':<20}"
    print(header)
    print("-" * len(header))

    found = False
    for i in range(len(outage_logs["LogID"])):
        if outage_logs["Overrun"][i] > 30:
            found = True
            scheduled = f"{outage_logs['ScheduledStart'][i]}-{outage_logs['ScheduledEnd'][i]}"
            actual = f"{outage_logs['ActualStart'][i]}-{outage_logs['ActualEnd'][i]}"
            row = f"{outage_logs['LogID'][i]:<10} | {outage_logs['Date'][i]:<12} | {outage_logs['Area'][i]:<12} | {outage_logs['Block'][i]:<6} | {outage_logs['Stage'][i]:<6} | {scheduled:<15} | {actual:<15} | {outage_logs['Overrun'][i]:<15} | {outage_logs['Monitor'][i]:<20}"
            print(row)

    if not found:
        print("No flagged logs found.")

# View impact report for a specific flagged log
def view_impact_report(log_id, outage_logs, impact_reports, community_members):
    print(f"\n=== Impact Report for Log ID {log_id} ===")

    # Table header
    header = f"{'Member':<30} | {'Impact':<100}"
    print(header)
    print("-" * len(header))

    found = False
    for j in range(len(impact_reports["LogID"])):
        if impact_reports["LogID"][j] == log_id:
            found = True
            member_id = impact_reports["MemberID"][j]
            member_name = community_members["Name"][community_members["ID"].index(member_id)]
            description = impact_reports["Description"][j]

            row = f"{member_name:<30} | {description:<100}"
            print(row)

    if not found:
        print("No impact report found for that Log ID.")

# Let user select a flagged log ID and view its impact report
def select_and_view_impact(outage_logs, impact_reports, community_members):
    # Collect flagged logs
    flagged_logs = [log_id for i, log_id in enumerate(outage_logs["LogID"]) if outage_logs["Overrun"][i] > 30]

    if not flagged_logs:
        print("No flagged logs available.")
        return

    # Show list of flagged logs
    print("\n=== Select a Flagged Log ===")
    for idx, log_id in enumerate(flagged_logs, start=1):
        date = outage_logs["Date"][outage_logs["LogID"].index(log_id)]
        area = outage_logs["Area"][outage_logs["LogID"].index(log_id)]
        overrun = outage_logs["Overrun"][outage_logs["LogID"].index(log_id)]
        print(f"{idx}. {log_id}")
    # User selects from list
    choice = input("Enter the number of the log you want to view: ").strip()
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(flagged_logs):
        print("Invalid selection.")
        return

    selected_log = flagged_logs[int(choice) - 1]

    # Print impact report for selected log
    print(f"\n=== Impact Report for {selected_log} ===")
    header = f"{'Member':<30} | {'Impact':<100}"
    print(header)
    print("-" * len(header))

    found = False
    for j in range(len(impact_reports["LogID"])):
        if impact_reports["LogID"][j] == selected_log:
            found = True
            member_id = impact_reports["MemberID"][j]
            member_name = community_members["Name"][community_members["ID"].index(member_id)]
            description = impact_reports["Description"][j]
            row = f"{member_name:<30} | {description:<100}"
            print(row)

    if not found:
        print("No impact report found for this log.")



    



#Menu
while True:
    print("\n--- PowerWatchSA Menu ---")
    print("1. Log outage")
    print("2. View flagged logs")
    print("3. View block summary")
    print("4. View financial losses")
    print("5. Generate complaint report")
    print("6. Exit")
    
    choice = input("Enter choice: ")
    
    #Log outage
    if choice == "1":
        date = input("Enter date (YYYY-MM-DD): ").strip()
        if not date: 
            print("Date cannot be blank."); continue

        for i in range(len(create_area_list())):
            print(f"{i+1}. {create_area_list()[i]}")
        area = create_area_list()[int(input("Enter area number: "))-1].strip().title()

        stage = int(input("Enter stage (1-6): ").strip())
        block = int(input(f"Enter block ({Stages['Blocks'][stage-1]}): ").strip())

        scheduled_start = input("Enter scheduled start time (HH:MM): ").strip()
        scheduled_end = input("Enter scheduled end time (HH:MM): ").strip()
        actual_start = input("Enter actual start time (HH:MM): ").strip()
        actual_end = input("Enter actual end time (HH:MM): ").strip()
        monitor = input("Enter monitor name: ").strip().title()

        if not all([scheduled_start, scheduled_end, actual_start, actual_end, monitor]):
            print("All fields must be filled."); continue

        log_outage(date, area, block, stage,scheduled_start, scheduled_end,actual_start, actual_end, monitor)

    # View flagged logs
    elif choice == "2":
        print_all_flagged_logs(OutageLog)
        print("1. Continue to main menu")
        print("2. View Impact report for a flagged log")
        print("3. Exit")
        choice2 = input("Enter choice: ").strip()

        if choice2 == "1":
            continue
        elif choice2 == "2":
            select_and_view_impact(OutageLog, ImpactReports, CommunityMembers)
        elif choice2 == "3":
            print("Exiting PowerWatchSA...")
            break
        else:
            print("Invalid choice, returning to main menu.")


    # View block summary
    elif choice == "3":
        for i in range(len(create_area_list())):
            print(f"{i+1}. {create_area_list()[i]}")
        area = create_area_list()[int(input("Enter area number: "))-1].strip().title()

        block = int(input("Enter block: ").strip())
        get_block_summary(area, block, OutageLog, ImpactReports, CommunityMembers)

    # View financial losses
    elif choice == "4":
        print(f"Total financial loss: R{calculate_financial_loss(ImpactReports)}")
    
    # Generate complaint report
    elif choice == "5":
        generate_complaint_report(OutageLog, ImpactReports, CommunityMembers)
    
    # Exit
    elif choice == "6":
        print("Exiting PowerWatchSA...")
        break
    else:
        print("Invalid choice, try again.")