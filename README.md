# smtptest&convert
# ✅ Multi SMTP Checker & Converter

This tool checks a list of SMTP credentials in bulk to determine which ones are **working and capable of delivering emails**. The valid SMTPs are then saved in a structured **JSON format**.

---

## 📌 Features

- Bulk test SMTP credentials from a `.txt` file  
- Sends a real test email to verify delivery capability  
- Converts valid SMTPs to JSON format:
  ```json
  {
      "host": "smtp.example.com",
      "port": 587,
      "secure": false,
      "user": "username",
      "pass": "password",
      "fromAddress": "sender@example.com"
  }
