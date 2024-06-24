import datetime

def parse_log_line(line):
    # Parse a single log line and return its components
    parts = line.strip().split()
    timestamp_str = parts[0] + " " + parts[1]
    ip_address = parts[2]
    username = parts[3]
    login_status = parts[4]
    timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
    return timestamp, ip_address, username, login_status

def read_log_file(file_path):
    # Read the log file and return a list of log entries
    log_entries = []
    with open(file_path, 'r') as file:
        for line in file:
            log_entries.append(parse_log_line(line))
    return log_entries

def analyze_log_entries(log_entries):
    # Analyze log entries to identify suspicious activity
    failed_attempts = {}
    
    for entry in log_entries:
        timestamp, ip_address, username, login_status = entry
        if login_status == 'FAILURE':
            if ip_address not in failed_attempts:
                failed_attempts[ip_address] = []
            failed_attempts[ip_address].append(timestamp)
    
    report_suspicious_activity(failed_attempts)

def report_suspicious_activity(failed_attempts):
    for ip_address, timestamps in failed_attempts.items():
        timestamps.sort()
        
        for i in range(len(timestamps) - 5):
            if timestamps[i + 5] - timestamps[i] <= datetime.timedelta(minutes=10):
                print(f"Suspicious activity detected from IP address: {ip_address}")
                break

def main():
    log_file_path = "log.txt"
    
    log_entries = read_log_file(log_file_path)
    
    analyze_log_entries(log_entries)

if __name__ == '__main__':
    main()
