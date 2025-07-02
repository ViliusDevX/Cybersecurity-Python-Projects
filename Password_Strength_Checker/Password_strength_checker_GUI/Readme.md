🖥️ How Does It Work? – GUI Version

🔹 1. Graphical User Interface (Tkinter)

The program uses Python’s tkinter library to create a simple, cross-platform graphical interface. When the script is run:

    A small window opens with:

        A label prompting the user to enter a password

        A masked input field (Entry(show="*"))

        A "Check Password" button

🔹 2. User Input

The user enters their password into the input field.
Once they click the button, the check_password_gui() function is triggered, which:

    Retrieves the password from the input field

    Passes it to the same core functions used in the CLI version

🔹 3. Password Analysis

The script checks for five password characteristics:

    ✅ At least one lowercase letter

    ✅ At least one uppercase letter

    ✅ At least one digit

    ✅ At least one symbol (string.punctuation)

    ✅ Length of at least 12 characters

Each condition adds +1 to a total score (0–5).
If a condition is missing, a helpful suggestion is generated (e.g., "Tip: Add digits").

🔹 4. Entropy Calculation

The script estimates password entropy using this formula:

    entropy = length × log2(character set size)

Entropy level is interpreted and rated:

    < 28 bits → Crackable in seconds

    28–35 bits → Fair

    36–59 bits → Strong

    60+ bits → Very strong

🔹 5. Common Password Check

The entered password is compared against entries in common_passwords.txt.
If found, a warning is added to the result:

    ⚠️ This password is very common!

🔹 6. Output Display

All results are combined into a summary and displayed using:

    tkinter.messagebox.showinfo()

The popup includes:

    Strength score and rating

    Entropy score and interpretation

    Suggestions for improvement (if any)

    Common password warning (if applicable)

🔹 7. Report Generation

A report.json file is created in the working directory, storing:

    The masked password (e.g. "**********")

    The numerical strength score (0–5)

    The corresponding rating (e.g. "Strong")

📝 Example Output (in popup):

    Password strength: Strong (4/5)
    Entropy: 54.21 bits – Strong
    
    Suggestions:
     - Tip: Make it at least 12 characters long.
    
    ⚠️ Warning: This password is very common!

This version is ideal for non-technical users, showcasing projects, or building GUI-based tools with a security focus.
The logic remains the same as the CLI version — only the interface changes.
