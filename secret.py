import secrets

# Generate a secure random key
private_key = secrets.token_hex(32)  # Generates a 64-character hexadecimal string
print(private_key)
