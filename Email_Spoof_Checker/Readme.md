##📤 Email Spoof Checker

A lightweight GUI application to evaluate a domain's email spoofing protection by inspecting its SPF, DMARC, and DKIM records.

#🔍 Features

    ✅ SPF Check — Identifies and evaluates SPF configuration

    ✅ DMARC Check — Assesses DMARC enforcement and subdomain policy

    ✅ DKIM Check — Looks for DKIM records using common selectors

    🧠 Recommendations — Offers tips to improve configuration

    📊 Security Score — Rates domain security from 0 to 6

    🖥️ User Interface — Simple PyQt5 GUI

#⚙️ How It Works

    Enter a domain name (e.g., example.com) into the input field.

    The app fetches DNS TXT records and attempts to:

        Extract and parse the SPF record (checks enforcement mode, include: count).

        Locate the DMARC policy and evaluate strictness (p= and sp= tags).

        Detect DKIM selectors and verify existence.

    Calculates a score out of 6 based on configuration strength.

    Displays a verdict and recommendations for improvements.

#📌 Verdict System

Score	Verdict
5–6	✅ Secure Email Configuration
3–4	⚠️ Acceptable but improvable
0–2	🚨 Poor email protection – spoofing risk!

------------

⚠️ Disclaimer:

It's not meant for serious or professional use, more like a portfolio piece. It might occasionally give incomplete or inaccurate results. If you're handling real email infrastructure or sensitive data, definitely go with proper tools or talk to professional. 
Thank you for understanding!
