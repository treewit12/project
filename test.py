from collections import defaultdict, Counter

def analyze_log_file(log_file_path: str) -> dict:
    requests_by_ip = defaultdict(int)
    resource_counter = Counter()
    total_404_errors = 0
    total_bytes = 0

    try:
        with open(log_file_path, 'r') as log_file:
            for line in log_file:
                parts = line.split()
                if len(parts) != 5:
                    # ข้ามบรรทัดที่ข้อมูลไม่ตรงรูปแบบ
                    print(f"Skipping malformed line: {line.strip()}")
                    continue

                ip = parts[0]
                method = parts[1]
                resource = parts[2]
                status_code = parts[3]
                bytes_transferred = parts[4]

                # นับจำนวนการร้องขอจากแต่ละ IP
                requests_by_ip[ip] += 1

                # นับจำนวนการร้องขอแต่ละทรัพยากร
                resource_counter[resource] += 1

                # นับจำนวนข้อผิดพลาด 404
                if status_code == '404':
                    total_404_errors += 1

                # คำนวณขนาดของการร้องขอทั้งหมด
                if bytes_transferred.isdigit():
                    total_bytes += int(bytes_transferred)

        # หาทรัพยากรที่ถูกเรียกร้องมากที่สุด
        most_requested_resource = resource_counter.most_common(1)[0][0] if resource_counter else None

        return {
            "requests_by_ip": dict(requests_by_ip),
            "most_requested_resource": most_requested_resource,
            "total_404_errors": total_404_errors,
            "total_bytes": total_bytes
        }

    except FileNotFoundError:
        print(f"Error: File {log_file_path} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# ทดสอบฟังก์ชัน
log_file_path = 'server_log.txt'  # เปลี่ยนเป็น path ของไฟล์ log ของคุณ
result = analyze_log_file(log_file_path)

# แสดงผลลัพธ์การวิเคราะห์
if result:
    print("Log File Analysis Result:")
    print(f"Requests by IP: {result['requests_by_ip']}")
    print(f"Most Requested Resource: {result['most_requested_resource']}")
    print(f"Total 404 Errors: {result['total_404_errors']}")
    print(f"Total Bytes Transferred: {result['total_bytes']}")
