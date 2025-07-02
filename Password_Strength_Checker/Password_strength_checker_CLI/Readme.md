🖥️ How does it work? – CLI Version

🔹 1. User Input

The user is prompted in the terminal to enter a password using input().

🔹 2. Password Analysis

The script checks the password against five criteria:

    Contains lowercase letters

    Contains uppercase letters

    Contains digits

    Contains symbols

    Is 12 characters or longer

Each satisfied condition adds +1 to the password’s score (max: 5).

🔹 3. Feedback & Suggestions

    The script provides a strength rating (Weak → Very Strong) based on the score.

    If any criteria are unmet, the script generates tips to help the user improve their password.

🔹 4. Entropy Estimation

The password is analyzed to estimate entropy using:

    entropy = length × log2(charset size)

Entropy level is interpreted into practical strength (e.g., “Crackable in seconds” or “Very strong”).

🔹 5. Common Password Check

The password is checked against a list of common passwords (common_passwords.txt).
If it matches, a warning is shown:

    ⚠️ This password is very common!

🔹 6. Output & Report

All results are printed directly to the terminal.

    A report.json file is created, logging masked password info, score, and rating.
