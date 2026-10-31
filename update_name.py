from database import update_name

success = update_name("simple042", "YOUR FULL NAME")

if success:
    print("Full name updated successfully!")
else:
    print("User not found.")