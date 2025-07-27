# JWT Parser & Verifier (Python GUI)

A lightweight desktop GUI tool built with Python and Tkinter to decode and verify JSON Web Tokens (JWT). Designed for developers, security learners, and pentesters who need to inspect JWTs and validate their integrity.

---

## Features

- Decode the JWT header and payload (base64-decoded)
- Display claims like `iat`, `exp`, `sub`, and `name`
- Highlight if the token is expired or missing key fields
- Detect use of insecure algorithms like `alg: none`
- Verify the token’s signature using a shared secret (HS256)
- Simple GUI interface – no command line needed

---

## 💻How JWT Works (In Simple Terms)

A JWT is a token often used for user authentication in websites and APIs. It has three parts:

<HEADER>.<PAYLOAD>.<SIGNATURE> ```

    Header: Info about the algorithm (e.g., HS256)

    Payload: The actual data (username, ID, expiration time)

    Signature: A digital signature generated using a secret key to ensure the token hasn't been tampered with


## Usage

    Paste your JWT token into the "Token" input box

    (Optional) Enter the secret key if you want to verify the signature

    Click "Parse Token"

    View decoded JSON, expiration info, and signature status in the result area


Example Test Token

This is a safe, public JWT for testing (from jwt.io):
Token:

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
