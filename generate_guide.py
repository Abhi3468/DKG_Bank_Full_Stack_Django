import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def draw_page_decorations(canvas, doc):
    if doc.page == 1:
        # Draw dark premium cover page background
        canvas.saveState()
        # Navy blue backdrop
        canvas.setFillColor(colors.HexColor('#0a192f'))
        canvas.rect(0, 0, 612, 792, fill=True, stroke=False)
        # Left border cyan line decoration
        canvas.setFillColor(colors.HexColor('#00f2fe'))
        canvas.rect(0, 0, 15, 792, fill=True, stroke=False)
        canvas.restoreState()
        return
    
    canvas.saveState()
    # Header
    canvas.setFont('Helvetica-Bold', 8)
    canvas.setFillColor(colors.HexColor('#475569'))
    canvas.drawString(36, 756, "DKG BANK ATM SYSTEM - TECHNICAL ARCHITECTURE & INTERVIEW GUIDE")
    canvas.setStrokeColor(colors.HexColor('#cbd5e1'))
    canvas.setLineWidth(0.5)
    canvas.line(36, 748, 576, 748)
    
    # Footer
    canvas.line(36, 48, 576, 48)
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(colors.HexColor('#64748b'))
    canvas.drawString(36, 34, "CONFIDENTIAL - INTERVIEW PREPARATION PRE-RELEASE")
    canvas.drawRightString(576, 34, f"Page {doc.page}")
    canvas.restoreState()

def build_pdf():
    pdf_filename = "DKG_ATM_Interview_Guide.pdf"
    
    # Page dimensions: letter = 612 x 792 points. Margins: 36 (0.5 in) left/right, 54 (0.75 in) top/bottom.
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Define primary colors
    c_primary = colors.HexColor('#0f172a')  # Slate-900
    c_accent = colors.HexColor('#0284c7')   # Sky-600
    c_cyan = colors.HexColor('#00f2fe')     # Cyan
    c_text_dark = colors.HexColor('#334155') # Slate-700
    c_code_bg = colors.HexColor('#f8fafc')   # Slate-50
    
    # Custom Paragraph Styles
    style_cover_title = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=32,
        leading=38,
        textColor=colors.white,
        spaceAfter=12
    )
    
    style_cover_subtitle = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=16,
        leading=22,
        textColor=colors.HexColor('#38bdf8'), # Sky-400
        spaceAfter=250
    )
    
    style_cover_meta = ParagraphStyle(
        'CoverMeta',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#94a3b8') # Slate-400
    )
    
    style_h1 = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    style_h2 = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#0284c7'),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )
    
    style_body = ParagraphStyle(
        'Body_Custom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=c_text_dark,
        spaceAfter=8
    )

    style_bullet = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=c_text_dark,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )
    
    style_code = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=4
    )
    
    story = []
    
    # ------------------ COVER PAGE ------------------
    story.append(Spacer(1, 150))
    story.append(Paragraph("🏦 DKG BANK ENTERPRISE ATM", style_cover_title))
    story.append(Paragraph("Technical Architecture & Interview Preparation Guide", style_cover_subtitle))
    
    meta_text = (
        "<b>Project Stack:</b> Django 5.0, DRF, SQLite (Local) / PostgreSQL (Production), Nginx, Docker, GitHub Actions<br/>"
        "<b>Interview Core Focus:</b> Concurrency, Row-level Locking, API Design, Dockerization, Production Deployment on Render<br/>"
        "<b>Author:</b> Antigravity Assistant & Technical Team<br/>"
        "<b>Date:</b> June 2026 (Updated for Render Hosting Configuration)"
    )
    story.append(Paragraph(meta_text, style_cover_meta))
    story.append(PageBreak())
    
    # ------------------ PAGE 1: ARCHITECTURE OVERVIEW ------------------
    story.append(Paragraph("1. System Architecture Overview", style_h1))
    story.append(Paragraph(
        "DKG Bank is an enterprise-grade full-stack ATM application. It represents a <b>decoupled Django and Vanilla JS</b> architecture "
        "built to simulate core banking transactions under heavy production scenarios. Below are the design principles of the application:",
        style_body
    ))
    
    story.append(Paragraph("<b>• Decoupled API-First Design:</b> The frontend (HTML/CSS/JS templates) interacts with the Django backend purely via REST API "
                           "endpoints implemented using Django REST Framework (DRF) <code>APIViews</code>. This separates layout rendering from transactional business logic.", style_bullet))
    story.append(Paragraph("<b>• CSRF and Authentication Stack:</b> Security is implemented at the API level. User account management relies on Django's built-in "
                           "<code>django.contrib.auth</code> session mechanism. CSRF cookies are dynamically fetched and attached by the Vanilla JS frontend to all state-modifying requests (POST).", style_bullet))
    story.append(Paragraph("<b>• Concurrency Safeguard:</b> Uses Django's database transaction blocks (<code>transaction.atomic</code>) and row-level locks (<code>select_for_update</code>) "
                           "to prevent double-withdrawal race conditions, mathematically ensuring account balances never go below zero.", style_bullet))
    story.append(Paragraph("<b>• Responsive Glassmorphism Design:</b> The layout uses custom raw CSS to deliver a premium modern banking look featuring "
                           "neon glows, translucid frosted cards, and subtle transitions.", style_bullet))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("System Flow Diagram", style_h2))
    
    # Text-based flow explanation
    flow_data = [
        ["User Browser (Frontend)", "--> [HTTP Requests + CSRF Header] -->", "Nginx Reverse Proxy"],
        ["Nginx Reverse Proxy", "--> [Port 80 to Port 8000] -->", "Gunicorn (WSGI Server)"],
        ["Gunicorn (WSGI Server)", "--> [Spawns 4 worker threads] -->", "Django Web Application"],
        ["Django Application", "--> [Row-Level Locking Query] -->", "PostgreSQL / SQLite Database"]
    ]
    t_flow = Table(flow_data, colWidths=[160, 170, 190])
    t_flow.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_code_bg),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_flow)
    story.append(PageBreak())
    
    # ------------------ PAGE 2: FILE STRUCTURE & COMPONENT ROLES ------------------
    story.append(Paragraph("2. Project Directory Structure & Key Components", style_h1))
    story.append(Paragraph(
        "The project is structured with a root directory that contains configuration and deployment assets, and a main python source folder "
        "named <code>DKG_ATM</code> containing two separate Django apps:",
        style_body
    ))
    
    struct_data = [
        ["Directory/File Path", "Primary Role / Responsibilities"],
        ["/build.sh & /DKG_ATM/build.sh", "Render build scripts (installs packages, executes migrations, collectstatic)."],
        ["/Procfile & /DKG_ATM/Procfile", "Defines the WSGI startup command using Gunicorn server."],
        ["/DKG_ATM/DKG_ATM/", "Project root configuration folder containing settings.py, urls.py, and wsgi.py."],
        ["/DKG_ATM/BankInterface/", "The core banking backend app. Contains models.py, views.py (DRF APIs), serializers.py, and tests.py."],
        ["/DKG_ATM/UserInterface/", "Frontend controller app. Manages HTML templates and login/registration routing."],
        ["/DKG_ATM/static/", "Holds static files (CSS/JS) decoupled into UserInterface/ (auth pages) and BankInterface/ (dashboard)."],
        ["/DKG_ATM/templets/", "Stores the base HTML templates (index, register, next_page, history, etc.)."],
        ["/DKG_ATM/requirements.txt", "Lists python libraries (Django, DRF, whitenoise, reportlab, dj-database-url, gunicorn, etc.)."],
        ["/DKG_ATM/nginx.conf", "Production Nginx server configuration for reverse proxying and caching static files."]
    ]
    
    t_struct = Table(struct_data, colWidths=[170, 350])
    t_struct.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_accent),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
    ]))
    story.append(t_struct)
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("App Isolation & Clean Routing Design", style_h2))
    story.append(Paragraph(
        "Notice the complete division of labor: <b>UserInterface</b> is responsible for authentication views "
        "(login page rendering, forgot password templates, reset passwords, OTP requests) while <b>BankInterface</b> acts "
        "strictly as a transactions API (providing JSON endpoints for cash withdrawals, deposits, receipts, and balance checks). "
        "This follows the separation of concerns paradigm, facilitating maintenance and scalability.",
        style_body
    ))
    story.append(PageBreak())
    
    # ------------------ PAGE 3: DATABASE MODELS & SCHEMAS ------------------
    story.append(Paragraph("3. Database Schema Design (BankInterface)", style_h1))
    story.append(Paragraph(
        "The application models represent bank accounts, transactions, and credit systems. It extends the default Django User model.",
        style_body
    ))
    
    story.append(Paragraph("<b>Account Model</b> (Stores ATM profile information)", style_h2))
    story.append(Paragraph(
        "• <code>user</code>: OneToOneField to Django's built-in <code>User</code>. Cascades on deletion.<br/>"
        "• <code>card_number</code>: Unique 16-character string representing the physical ATM card.<br/>"
        "• <code>card_pin</code>: 4-character string checking verification.<br/>"
        "• <code>balance</code>: DecimalField (max digits 12, decimal places 2) storing funds.<br/>"
        "• <code>is_locked</code>: Boolean field. Automatically flips to True if user fails PIN checks 3 consecutive times.<br/>"
        "• <code>failed_attempts</code>: Integer field incremented on bad PIN entries; resets to 0 on successful verification.<br/>"
        "• <code>customer_id</code>: Unique 8-digit random string generated inside the <code>save()</code> override.<br/>"
        "• <code>account_number</code>: Unique 12-digit random string generated inside the <code>save()</code> override.",
        style_body
    ))
    
    story.append(Paragraph("<b>Transaction Model</b> (Stores immutable transaction records)", style_h2))
    story.append(Paragraph(
        "• <code>account</code>: ForeignKey linking directly to the <code>Account</code> model. Enables backwards queries.<br/>"
        "• <code>amount</code>: Decimal field representing cash volume.<br/>"
        "• <code>transaction_type</code>: Choices: Withdrawal, Deposit, Loan Disbursement, Loan Repayment, Transfer.<br/>"
        "• <code>timestamp</code>: Auto-created timezone-aware date-time stamp marking the audit point.",
        style_body
    ))

    story.append(Paragraph("<b>Loan Model</b> (Stores financial loan approvals)", style_h2))
    story.append(Paragraph(
        "• <code>account</code>: ForeignKey to the applicant account.<br/>"
        "• <code>loan_amount</code>: Total requested loan principal.<br/>"
        "• <code>status</code>: PENDING, APPROVED, REJECTED, CLOSED.",
        style_body
    ))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("Code Insight: Custom ID Generators on Save", style_h2))
    story.append(Paragraph(
        "To guarantee unique identifiers without manual input, the <code>Account.save()</code> method is overridden:",
        style_body
    ))
    
    code_save_override = (
        "def save(self, *args, **kwargs):\n"
        "    if not self.account_number:\n"
        "        while True:\n"
        "            acc_num = ''.join(random.choices(string.digits, k=12))\n"
        "            if not Account.objects.filter(account_number=acc_num).exists():\n"
        "                self.account_number = acc_num\n"
        "                break\n"
        "    super().save(*args, **kwargs)"
    )
    t_code = Table([[code_save_override]], colWidths=[520])
    t_code.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_code_bg),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('FONTNAME', (0,0), (-1,-1), 'Courier'),
        ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_code)
    story.append(PageBreak())
    
    # ------------------ PAGE 4: DECOUPLED APIS & ENDPOINTS ------------------
    story.append(Paragraph("4. Decoupled REST APIs and Endpoints", style_h1))
    story.append(Paragraph(
        "The communication layer utilizes structured REST API requests. When a customer interacts with the ATM (e.g. keying a PIN "
        "or withdrawing cash), the client-side JavaScript issues a <code>fetch()</code> request with a JSON payload.",
        style_body
    ))
    
    api_headers = [["Endpoint", "HTTP Verb", "Payload Details", "API Response Output"]]
    api_rows = [
        ["/verify_pin/", "POST", '{"card_pin": "1234"}', '{"message": "Verified", "card_number": "...", ...}'],
        ["/available_balance/", "POST", '{"card_number": "..."}', '{"balance": 1000.00}'],
        ["/withdraw/", "POST", '{"card_number": "...", "amount": 100}', '{"message": "Withdrawal successful", ...}'],
        ["/deposit/", "POST", '{"card_number": "...", "amount": 100}', '{"message": "Deposit successful", ...}'],
        ["/pin_change/", "POST", '{"card_number": "...", "new_pin": "5678"}', '{"message": "PIN changed successfully"}'],
        ["/loan_request/", "POST", '{"card_number": "...", "amount": 5000}', '{"message": "Loan application submitted"}'],
        ["/analytics/<card_number>/", "GET", "None (URL Param)", '{"withdrawals": 500.00, "deposits": 1200.00}'],
        ["/receipt/<tx_id>/", "GET", "None (URL Param)", "PDF stream (Generated on-the-fly via ReportLab)"]
    ]
    t_api = Table(api_headers + api_rows, colWidths=[130, 60, 150, 180])
    t_api.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_accent),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
    ]))
    story.append(t_api)
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("Security Safeguard: Dynamic CSRF Passing in JS", style_h2))
    story.append(Paragraph(
        "Because Django enforces Cross-Site Request Forgery protections, the Vanilla Javascript reads the token dynamically "
        "and injects it into the HTTP header of every request:",
        style_body
    ))
    
    code_csrf = (
        "function getCSRFToken() {\n"
        "    const input = document.querySelector('[name=csrfmiddlewaretoken]');\n"
        "    return input ? input.value : getCookie('csrftoken') || '';\n"
        "}\n\n"
        "fetch('/withdraw/', {\n"
        "    method: 'POST',\n"
        "    headers: {\n"
        "        'Content-Type': 'application/json',\n"
        "        'X-CSRFToken': getCSRFToken()\n"
        "    },\n"
        "    body: JSON.stringify({ card_number: currentCardNumber, amount: amount })\n"
        "})"
    )
    t_code2 = Table([[code_csrf]], colWidths=[520])
    t_code2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_code_bg),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('FONTNAME', (0,0), (-1,-1), 'Courier'),
        ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_code2)
    story.append(PageBreak())
    
    # ------------------ PAGE 5: CONCURRENCY & ROW-LEVEL LOCKING ------------------
    story.append(Paragraph("5. Concurrency Control & Race Condition Prevention", style_h1))
    story.append(Paragraph(
        "<b>Crucial Interview Topic:</b> How do you prevent double-withdrawal race conditions? "
        "In high-traffic environments, two request threads could query a customer's account balance at the exact same millisecond. "
        "If both read a balance of $100 and attempt to withdraw $100 simultaneously, both threads might approve the operation before "
        "updating the database, causing the balance to drop to -$100 (a critical banking exploit).",
        style_body
    ))
    
    story.append(Paragraph("The Row-Level Lock Solution: <code>select_for_update</code>", style_h2))
    story.append(Paragraph(
        "DKG Bank solves this by locking the database row during the transaction using Django's <code>select_for_update()</code> "
        "within a transaction block (<code>transaction.atomic()</code>):",
        style_body
    ))
    
    code_lock = (
        "with transaction.atomic():\n"
        "    # Locks the account row. Any other concurrent query is blocked until this block completes.\n"
        "    account = get_object_or_404(Account.objects.select_for_update(), card_number=card_number)\n"
        "    \n"
        "    if account.balance < amount:\n"
        "        return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)\n"
        "        \n"
        "    account.balance -= amount\n"
        "    account.save()\n"
        "    Transaction.objects.create(account=account, amount=amount, transaction_type='WITHDRAWAL')"
    )
    t_code3 = Table([[code_lock]], colWidths=[520])
    t_code3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_code_bg),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('FONTNAME', (0,0), (-1,-1), 'Courier'),
        ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_code3)
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("How it works under the hood (SQL Translation)", style_h2))
    story.append(Paragraph(
        "Under PostgreSQL, this code generates the SQL query:<br/>"
        "<code>SELECT * FROM BankInterface_account WHERE card_number = '...' FOR UPDATE;</code><br/>"
        "The <code>FOR UPDATE</code> clause tells the database engine to acquire an exclusive write lock on that row. "
        "If a second thread attempts to run a query with <code>FOR UPDATE</code> on the same row, PostgreSQL halts its execution "
        "and makes it wait in queue until the first thread's transaction commits or rolls back.",
        style_body
    ))
    
    story.append(Paragraph("Threaded Concurrency Testing", style_h2))
    story.append(Paragraph(
        "The test suite includes a multi-threaded Python test (<code>test_concurrent_withdrawals_prevent_negative_balance</code>) "
        "that spawns concurrent threads using Python's <code>concurrent.futures.ThreadPoolExecutor</code> to intentionally hit "
        "the withdrawal API at the same time, confirming that one request succeeds while the second fails gracefully with an insufficient funds or lock error.",
        style_body
    ))
    story.append(PageBreak())
    
    # ------------------ PAGE 6: SECURITY FEATURES ------------------
    story.append(Paragraph("6. Enterprise Security Implementation", style_h1))
    story.append(Paragraph(
        "Security is implemented at several layers of the application to prevent automated attacks, brute-force hacking, "
        "and to provide a proper audit trail.",
        style_body
    ))
    
    story.append(Paragraph("1. API Rate Limiting (Throttling)", style_h2))
    story.append(Paragraph(
        "To prevent script-kiddies and botnets from brute-forcing card PINs or spamming the OTP login endpoint, DKG Bank utilizes "
        "Django REST Framework's rate-limiting middleware configured in <code>settings.py</code>:",
        style_body
    ))
    
    code_throttle = (
        "REST_FRAMEWORK = {\n"
        "    'DEFAULT_THROTTLE_CLASSES': [\n"
        "        'rest_framework.throttling.AnonRateThrottle',\n"
        "        'rest_framework.throttling.UserRateThrottle'\n"
        "    ],\n"
        "    'DEFAULT_THROTTLE_RATES': {\n"
        "        'anon': '20/min',   # 20 requests per minute max for guest calls\n"
        "        'user': '100/min'   # 100 requests per minute max for logged users\n"
        "    }\n"
        "}"
    )
    t_code4 = Table([[code_throttle]], colWidths=[520])
    t_code4.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_code_bg),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('FONTNAME', (0,0), (-1,-1), 'Courier'),
        ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_code4)
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("2. Immutable Audit Logging", style_h2))
    story.append(Paragraph(
        "Every crucial transactional operation (successful logins, deposits, withdrawals, card locking) is recorded to a secure, "
        "append-only file <code>bank_audit.log</code> using Python's <code>logging</code> module. If a security analyst wants to "
        "trace account behavior, the logs list timestamped events in the following verbose format:",
        style_body
    ))
    story.append(Paragraph("<code>INFO 2026-06-10 13:30:00 views Successful Withdrawal of $200 from card 1111222233334444. New Balance: $4800.00</code><br/>"
                           "<code>CRITICAL 2026-06-10 13:31:00 views Account AUTOMATICALLY LOCKED for user guest_user after 3 failed attempts.</code>", style_body))
    
    story.append(Paragraph("3. Session-Backed OTP Verification", style_h2))
    story.append(Paragraph(
        "When a user signs in using the OTP flow, a random 6-digit string is generated on the server and saved to the Django database-backed session "
        "(<code>request.session['login_otp'] = otp</code>) while being sent to the user's email via Gmail SMTP. When submitted, the backend verifies the "
        "match and clears the session variable to guarantee single-use. This prevents replay attacks.",
        style_body
    ))
    story.append(PageBreak())
    
    # ------------------ PAGE 7: CONTAINERIZATION (DOCKER) ------------------
    story.append(Paragraph("7. Containerization & Production Docker Setup", style_h1))
    story.append(Paragraph(
        "To ensure development environments match production exactly, the application is containerized using Docker, "
        "Docker Compose, and Nginx. This setup isolates the Python runtime, PostgreSQL database, and web server proxy.",
        style_body
    ))
    
    story.append(Paragraph("Dockerfile Analysis", style_h2))
    story.append(Paragraph(
        "The <code>Dockerfile</code> uses a slim base python image (<code>python:3.12-slim</code>) to keep image size small. "
        "It installs necessary build dependencies for PostgreSQL (<code>libpq-dev</code>, <code>gcc</code>), copies the code, "
        "collects static files, and creates a <b>non-root application user</b> (<code>appuser</code>) for security. "
        "The container is executed using Gunicorn with optimized workers (4 workers, sync worker class, 60s timeout).",
        style_body
    ))
    
    story.append(Paragraph("Docker Compose Coordination (docker-compose.yml)", style_h2))
    story.append(Paragraph(
        "Docker Compose coordinates three service containers on a bridge network:",
        style_body
    ))
    
    compose_details = [
        ["Container Service", "Role in Stack", "Ports / Volumes / Dependencies"],
        ["db", "PostgreSQL Database engine. Stores tables securely.", "Port 5432. Persists data via postgres_data volume. Health checked."],
        ["web", "The Django + Gunicorn application container.", "Port 8000. Depends on db being healthy. Collects static and runs migrations."],
        ["nginx", "Nginx web server acting as a reverse proxy.", "Port 80. Maps static files directly; forwards dynamic requests to web:8000."]
    ]
    t_comp = Table(compose_details, colWidths=[120, 200, 200])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_accent),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('FONTSIZE', (0,0), (-1,-1), 8),
    ]))
    story.append(t_comp)
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("Production Nginx Reverse Proxy Config (nginx.conf)", style_h2))
    story.append(Paragraph(
        "Nginx serves static files (CSS, JS) directly from a shared Docker volume (<code>/app/staticfiles/</code>) with cache-control headers "
        "enabled for 30 days. This bypasses Django entirely for static assets, saving significant CPU resources. All other requests are "
        "forwarded to the upstream Gunicorn backend:",
        style_body
    ))
    
    code_nginx = (
        "location /static/ {\n"
        "    alias /app/staticfiles/;\n"
        "    expires 30d;\n"
        "    add_header Cache-Control \"public, immutable\";\n"
        "}\n"
        "location / {\n"
        "    proxy_pass http://web;\n"
        "    proxy_set_header Host $host;\n"
        "    proxy_set_header X-Real-IP $remote_addr;\n"
        "}"
    )
    t_code5 = Table([[code_nginx]], colWidths=[520])
    t_code5.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_code_bg),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('FONTNAME', (0,0), (-1,-1), 'Courier'),
        ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_code5)
    story.append(PageBreak())
    
    # ------------------ PAGE 8: CI/CD & PRODUCTION DEPLOYMENT ------------------
    story.append(Paragraph("8. CI/CD Pipeline & Production Deployment", style_h1))
    story.append(Paragraph(
        "For modern deployment, DKG Bank leverages automated continuous integration (GitHub Actions) "
        "and hosting configurations on Render.",
        style_body
    ))
    
    story.append(Paragraph("1. GitHub Actions CI (django.yml)", style_h2))
    story.append(Paragraph(
        "Whenever code is pushed to <code>master</code> or <code>main</code>, GitHub Actions automatically executes "
        "the CI pipeline to verify code quality. Under a fresh Ubuntu runner environment, it:<br/>"
        "• Spins up a temporary PostgreSQL service container.<br/>"
        "• Checks out the source code and configures Python 3.11.<br/>"
        "• Installs dependencies from <code>requirements.txt</code> along with DB drivers.<br/>"
        "• Runs database migrations (<code>python manage.py migrate</code>).<br/>"
        "• Runs the test suite (<code>python manage.py test</code>) to prevent regression bugs from reaching production.",
        style_body
    ))
    
    story.append(Paragraph("2. Production Deployment on Render", style_h2))
    story.append(Paragraph(
        "Render connects to the GitHub repository and deploys the app dynamically using the newly implemented configuration files:",
        style_body
    ))
    
    story.append(Paragraph("<b>• Unified Build Script (build.sh):</b> Render runs <code>./build.sh</code> during the build phase. This script automates "
                           "installing packages, running database migrations on the live database, collecting static files using WhiteNoise, and "
                           "executing <code>create_test_user.py</code> to ensure a default test account is seeded.", style_bullet))
    story.append(Paragraph("<b>• WSGI Gunicorn Server (Procfile):</b> Informs Render to start Gunicorn using the proper wsgi module, "
                           "allowing the app to handle production web traffic safely.", style_bullet))
    story.append(Paragraph("<b>• Database SSL Requirement:</b> Render's PostgreSQL databases require SSL. The database setup in "
                           "<code>settings.py</code> is updated to detect the <code>RENDER</code> environment variable and dynamically enable "
                           "<code>ssl_require=True</code> only in the production cloud database, keeping local sqlite running without SSL problems.", style_bullet))
    story.append(Paragraph("<b>• Email Fallback Interface:</b> If registration SMTP is offline, the API response is modified to return the newly generated card number "
                           "and ATM PIN in the JSON payload, displaying it directly on the success modal on the screen. This guarantees zero lockouts during testing.", style_bullet))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("Summary of Render Deployment Settings", style_h2))
    
    render_settings = [
        ["Setting Field", "Value / Configuration", "Purpose"],
        ["Build Command", "./build.sh", "Runs requirements install, DB migration, static collect, and seeding."],
        ["Start Command", "gunicorn --chdir DKG_ATM DKG_ATM.wsgi --log-file -", "Launches the production WSGI server instance."],
        ["Env: DATABASE_URL", "postgres://...", "Auto-injected by Render PostgreSQL connection binding."],
        ["Env: RENDER", "true", "Used by settings.py to force database SSL connection mode."]
    ]
    t_rend = Table(render_settings, colWidths=[120, 240, 160])
    t_rend.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_accent),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('FONTSIZE', (0,0), (-1,-1), 8),
    ]))
    story.append(t_rend)
    
    # Build document
    doc.build(story, onFirstPage=draw_page_decorations, onLaterPages=draw_page_decorations)
    print(f"Successfully generated {pdf_filename}")

if __name__ == "__main__":
    build_pdf()
