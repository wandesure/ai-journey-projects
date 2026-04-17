"""Generate bcrypt password hashes for streamlit-authenticator."""
import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

passwords = ["admin123", "client123", "client123"]

print("Generated password hashes:")
print("-" * 50)
for pwd in passwords:
    hashed = hash_password(pwd)
    print(f"{pwd}: {hashed}")
print("-" * 50)
print("\nCopy these hashes to your .streamlit/secrets.toml file")
