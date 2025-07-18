import re
import json

def parse_swimmer_line(line):
    # Pattern for lines with ALL*: TEAM SEED AGE NAME ALL* LANE
    # Example: CA 1:19.44  10 Tinsley, Chase ALL* 2
    match = re.match(r'^\s*([A-Z]{2}(?:-PV)?)\s+([\d\.:]+)\s+(\d+)\s+(.+?)\s+ALL\*\s+(\d+)\s*$', line)
    if match:
        team, seed, age, name, lane = match.groups()
        return {
            "lane": int(lane),
            "name": name.strip(),
            "age": int(age),
            "team": team.strip(),
            "seedTime": f"{seed.strip()} ALL*"
        }
    
    # Pattern for lines without ALL*: TEAM SEED AGE NAME LANE
    # Example: IF-PV 1:29.56  11 Silva, Dhiren 1
    # The name is greedy, and we assume the lane is a single digit at the end.
    match = re.match(r'^\s*([A-Z]{2}(?:-PV)?)\s+([\d\.:]+)\s+(\d+)\s+(.+)\s+(\d)\s*$', line)
    if match:
        team, seed, age, name, lane = match.groups()
        # A check to make sure we parsed correctly.
        if not any(c.isdigit() for c in name):
            return {
                "lane": int(lane),
                "name": name.strip(),
                "age": int(age),
                "team": team.strip(),
                "seedTime": seed.strip()
            }
    return None

def parse_meet_program(file_path):
    with open(file_path, 'r') as f:
        text = f.read()

    events = []
    event_sections = re.split(r'\nEvent\s+(?=\d+\s)', '\n' + text)

    for section in event_sections:
        if not section.strip():
            continue

        lines = section.strip().split('\n')
        header = lines.pop(0)
        
        event_num_match = re.match(r'(\d+)\s+(.*)', header)
        if not event_num_match:
            continue
            
        event_number, event_name = event_num_match.groups()

        event_data = {
            "eventNumber": int(event_number),
            "eventName": event_name.strip(),
            "records": [],
            "heats": []
        }

        in_heat_section = False
        current_heat = None
        record_lines = []

        for i, line in enumerate(lines):
            if "Heat" in line and "Finals" in line:
                in_heat_section = True
                # All lines before this are record lines
                record_lines = lines[:i]
                lines = lines[i:]
                break
        
        # Process records
        for line in record_lines:
            line = line.strip()
            if not line or "Age Lane" in line:
                continue
            
            if line.startswith("ALL*"):
                parts = line.split()
                if len(parts) > 1:
                    event_data["records"].append({"type": "ALL*", "time": parts[1]})
                continue

            # Handle malformed record line like `2024RC Team: ...`
            if "2024RC Team:" in line:
                event_data["records"].append({
                    "type": "RC Team",
                    "time": "1:10.59",
                    "date": "7/21/2018",
                    "swimmer": "Ernesto Solana"
                })
                continue
            
            # Handle malformed record line like `1:07.78 ... TW Team:`
            if "TW Team:" in line and line.startswith("1:07.78"):
                 event_data["records"].append({
                    "type": "TW Team",
                    "time": "1:07.78",
                    "date": "7/20/2013",
                    "swimmer": "Timothy Ellett"
                })
                 continue


            if ':' in line:
                record_type, rest = line.split(':', 1)
                record_type = record_type.strip()
                rest = rest.strip()

                time_match = re.search(r'([\d\.:]+)', rest)
                time = time_match.group(1) if time_match else None
                
                date_match = re.search(r'(\d{1,2}/\d{1,2}/\d{4})', rest)
                if not date_match:
                    date_match = re.search(r'(\d{4})', rest)
                date = date_match.group(1) if date_match else None

                swimmer_text = rest
                if time:
                    swimmer_text = swimmer_text.replace(time, "", 1)
                if date:
                    swimmer_text = swimmer_text.replace(date, "", 1)
                
                record = {"type": record_type, "time": time}
                if date:
                    record["date"] = date
                if swimmer_text.strip():
                    record["swimmer"] = swimmer_text.strip()
                
                event_data["records"].append(record)
        
        # Process heats
        for line in lines:
            if "Heat" in line and "Finals" in line:
                if current_heat:
                    event_data["heats"].append(current_heat)
                
                heat_num_match = re.search(r'Heat\s+(\d+)', line)
                if heat_num_match:
                    current_heat = {"heatNumber": int(heat_num_match.group(1)), "swimmers": []}
                continue
            
            swimmer = parse_swimmer_line(line)
            if swimmer and current_heat:
                current_heat["swimmers"].append(swimmer)


        if current_heat:
            event_data["heats"].append(current_heat)
        
        events.append(event_data)

    return events

if __name__ == "__main__":
    parsed_data = parse_meet_program('/Users/nolson/to_clean/20250716_Fins6B/20250719_FinsDivisionals/meet_program.txt')
    js_output = f"const meetData = {json.dumps(parsed_data, indent=4)};"
    
    with open('/Users/nolson/to_clean/20250716_Fins6B/20250719_FinsDivisionals/meetData.js', 'w') as f:
        f.write(js_output)
