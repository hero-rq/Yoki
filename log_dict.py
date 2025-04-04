from collections import defaultdict

activity_logs = {
    'neuronet.edu': [(10, 5), (14, 5), (10, 6), (10, 5), (15, 6), (9, 4), (10, 5)],
    'cybersys.tech': [(8, 3), (8, 3), (9, 3), (8, 4), (7, 2)],
    'quantumhub.ac': [(11, 10), (11, 10), (15, 12), (11, 10), (16, 12)],
    'aetherlab.io': [(13, 6), (14, 6), (13, 7), (14, 7), (14, 8), (13, 8)],
    'xvoid.org': [(20, 20), (21, 21), (20, 21), (22, 21)]
}

name_map = {
    'neuronet.edu': 'NeuroNet University',
    'cybersys.tech': 'Cyber Systems Institute',
    'quantumhub.ac': 'QuantumHub Academy',
    'aetherlab.io': 'Aether Lab of Technology',
    # 'xvoid.org' intentionally left unmapped
}

print(f"\n📊 Heatmap for logs for each institution:\n")

for inst in activity_logs:
    readable_name = name_map.get(inst, inst)  
    print(f"\n🧠 {readable_name} ({inst})")

    hour_counts = defaultdict(int)
    for hour, day in activity_logs[inst]:
        hour_counts[hour] += 1

    for hour in range(24):
        count = hour_counts.get(hour, 0)
        print(f"{hour:02d}: {'#' * count}")

