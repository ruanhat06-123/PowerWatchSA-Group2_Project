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
    "Solar": ["No","No","No","No","No","No","Yes","No","No","No"],
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
# Calculate overrun time in minutes
def calculate_overrun(start_time,end_time,actual_start, actual_end):
    overrun = (end_time - start_time).total_seconds() / 60
    return overrun# log_outage()


def log_outage(log_id, date, area, block, stage, scheduled_start, scheduled_end, actual_start, actual_end, monitor):
    OutageLog["LogID"].append(log_id)
    OutageLog["Date"].append(date)
    OutageLog["Area"].append(area)
    OutageLog["Block"].append(block)
    OutageLog["Stage"].append(stage)
    OutageLog["ScheduledStart"].append(scheduled_start)
    OutageLog["ScheduledEnd"].append(scheduled_end)
    OutageLog["ActualStart"].append(actual_start)
    OutageLog["ActualEnd"].append(actual_end)
    OutageLog["Overrun"].append(calculate_overrun(scheduled_start, scheduled_end, actual_start, actual_end))
    OutageLog["Monitor"].append(monitor)
    return "Outage logged successfully."



print(f"Community Member ID: {CommunityMembers['ID']}")
print(f"Name: {CommunityMembers['Name']}")
print(f"Type: {CommunityMembers['Type']}")
print(f"Area: {CommunityMembers['Area']}")
print(f"Block: {CommunityMembers['Block']}")
print(f"Generator: {CommunityMembers['Generator']}")
print(f"Solar: {CommunityMembers['Solar']}")
print(f"Vulnerable: {CommunityMembers['Vulnerable']}")