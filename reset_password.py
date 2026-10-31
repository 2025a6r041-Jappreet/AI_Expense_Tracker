from database import reset_password

username = "YOUR_USERNAME"

new_password = input("Enter your new password: ")

if len(new_password) < 8:
    print("Password must be at least 8 characters.")
else:
    success = reset_password(username, new_password)

    if success:
        print("Password reset successful!")
    else:
        print("Username not found.")