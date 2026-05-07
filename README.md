# 🏦 Enterprise Bank (DKG Bank)

An enterprise-grade, high-performance web application designed to simulate a modern banking environment. This project demonstrates advanced backend architecture, robust security principles, API-first design, and a premium "Glassmorphism" frontend.

## 🚀 Features & Engineering Highlights

### 1. Robust Concurrency & Race-Condition Prevention
- **Database Row-Level Locking:** Uses Django's `transaction.atomic()` and `select_for_update()` to prevent race conditions during simultaneous bank withdrawals. Mathematically guarantees that account balances never drop below zero under high-concurrency load.
- **Automated Concurrency Testing:** Includes a multi-threaded Python test suite that intentionally simulates thousands of simultaneous withdrawal requests to verify lock stability and timeout handling.

### 2. API-First Architecture (Django Rest Framework)
- Completely decoupled business logic from the frontend by implementing DRF `APIViews`.
- JWT & Session-based authentication systems integrated.
- Clean, structured JSON endpoints for Withdrawals, Deposits, and PIN Verification.

### 3. Enterprise Security
- **API Rate Limiting (Throttling):** Blocks brute-force attacks and OTP spamming by rate-limiting anonymous users to 20 requests/minute and authenticated users to 100 requests/minute.
- **Audit Logging:** Employs Python's built-in `logging` module to silently write immutable logs of every transaction, successful login, and failed PIN attempt to a secure `bank_audit.log` file.

### 4. Premium Frontend Design
- **Dark Mode Glassmorphism:** Features a sleek, modern UI utilizing raw CSS (no heavy frameworks).
- Incorporates dynamic animated neon gradients, translucent frosted-glass cards (`backdrop-filter: blur`), and micro-animations for a highly interactive UX.

## 🛠 Tech Stack
- **Backend:** Python, Django, Django Rest Framework (DRF)
- **Frontend:** HTML5, Vanilla CSS3 (Glassmorphism), Vanilla JavaScript
- **Database:** SQLite (Local) / MySQL or PostgreSQL (Production)
- **DevOps:** GitHub Actions (CI/CD), Gunicorn

## ⚙️ How to Run Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ATM_Bank_full-stack.git
   cd ATM_Bank_full-stack/DKG_ATM
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

4. **Start the Server**
   ```bash
   python manage.py runserver
   ```
   *Navigate to `http://127.0.0.1:8000` to view the application.*

## 🧪 Running Automated Tests
To run the test suite and verify the concurrency protections:
```bash
python manage.py test BankInterface
```
