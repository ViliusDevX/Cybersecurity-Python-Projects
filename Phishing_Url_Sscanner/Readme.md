# 🎣 Phishing URL Detector/Scanner

A Python GUI application that analyzes URLs for potential phishing threats by examining multiple security indicators including domain age, SSL certificates, URL structure, and more.

## 🔍 Features

    ✅ SPF Check — Identifies and evaluates SPF configuration

    ✅ DMARC Check — Assesses DMARC enforcement and subdomain policy

    ✅ DKIM Check — Looks for DKIM records using common selectors

    🧠 Recommendations — Offers tips to improve configuration

    📊 Security Score — Rates domain security from 0 to 6

    🖥️ User Interface — Simple PyQt5 GUI

## ⚙️ How It Works

    Enter a domain name (e.g., example.com) into the input field.

    The app fetches DNS TXT records and attempts to:

        Extract and parse the SPF record (checks enforcement mode, include: count).

        Locate the DMARC policy and evaluate strictness (p= and sp= tags).

        Detect DKIM selectors and verify existence.

    Calculates a score out of 6 based on configuration strength.

    Displays a verdict and recommendations for improvements.

## 🧠 Verdict System

| Score (out of 6) | Verdict                           | Meaning                                               |
|------------------|-----------------------------------|-------------------------------------------------------|
| 5–6              | ✅ Secure Email Configuration     | All major protections in place.                       |
| 3–4              | ⚠️ Acceptable but Improvable      | Some protections are in place, but can be better.     |
| 0–2              | 🚨 Poor Email Protection          | Spoofing risk. Key mechanisms are missing or weak.    |


------------

## ⚠️ Disclaimer:

It's not meant for serious or professional use, more like a portfolio piece. 
It might occasionally give incomplete or inaccurate results. 
