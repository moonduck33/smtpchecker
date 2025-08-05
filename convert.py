import smtplib
import ssl
import json
from email.message import EmailMessage
from email.utils import make_msgid
from time import sleep

SMTP_LIST_FILE = 'smtps.txt'
OUTPUT_FILE = 'working_smtps.json'
TEST_EMAIL = 'jeremywilliams25@mail.com'  # Change to your receiving test address
SUBJECT = 'SMTP Test'
BODY = 'This is a test message from the SMTP checker.'

def is_smtp_working(smtp, port, user, password, from_addr):
    try:
        context = ssl.create_default_context()
        server = smtplib.SMTP(smtp, int(port), timeout=10)
        server.ehlo()
        if int(port) == 587:
            server.starttls(context=context)
        server.login(user, password)

        msg = EmailMessage()
        msg['Subject'] = SUBJECT
        msg['From'] = from_addr
        msg['To'] = TEST_EMAIL
        msg.set_content(BODY)
        msg_id = make_msgid()
        msg['Message-ID'] = msg_id

        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"[x] Failed: {smtp}|{port}|{user} - {e}")
        return False

def parse_and_check():
    working = []
    with open(SMTP_LIST_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or '|' not in line:
                continue
            parts = line.split('|')
            if len(parts) != 5:
                continue
            smtp, port, user, password, from_addr = parts
            print(f"[>] Testing: {smtp}|{port}|{user}")
            if is_smtp_working(smtp, port, user, password, from_addr):
                print(f"[✓] Good: {smtp}")
                working.append({
                    "host": smtp,
                    "port": int(port),
                    "secure": (int(port) == 465),
                    "user": user,
                    "pass": password,
                    "fromAddress": from_addr
                })
            sleep(2)  # Avoid spam detection

    with open(OUTPUT_FILE, 'w') as f:
        json.dump(working, f, indent=4)
    print(f"\n[✓] Saved {len(working)} working SMTPs to {OUTPUT_FILE}")

if __name__ == "__main__":
    parse_and_check()
