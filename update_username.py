from database import update_username

old_username = "simple042"
new_username = "simple10"

success = update_username(old_username, new_username)

if success:
    print("Username updated successfully!")
else:
    print("Username update failed. Check the old username.")