import re
from collections import defaultdict

def parse_logs(logfile):
    with open(logfile) as f:
        logs = f.readlines()
    return logs

def filter_logs(logs, level=None, keyword=None):
    filtered = []
    for line in logs:
        if level and level not in line:
            continue
        if keyword and keyword not in line:
            continue
        filtered.append(line)
    return filtered

def log_stats(logs):
    levels = defaultdict(int)
    for line in logs:
        match = re.match(r'\[(\w+)\]', line)
        if match:
            levels[match.group(1)] += 1
    return levels

if __name__ == "__main__":
    file = input("Log file name: ")
    logs = parse_logs(file)
    while True:
        action = input("1. View All 2. Filter by Level 3. Search by Keyword 4. Stats 5. Exit: ")
        if action == '1':
            print("".join(logs))
        elif action == '2':
            lvl = input("Enter level (INFO/WARN/ERROR): ")
            for l in filter_logs(logs, level=lvl):
                print(l, end='')
        elif action == '3':
            kw = input("Enter keyword: ")
            for l in filter_logs(logs, keyword=kw):
                print(l, end='')
        elif action == '4':
            stats = log_stats(logs)
            for k, v in stats.items():
                print(f"{k}: {v}")
        elif action == '5':
            break
