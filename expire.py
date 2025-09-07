import datetime
import time

# Premium user IDs with expiration dates (format: user_id: "YYYY-MM-DD")
PREMIUM_USERS = {
    "7987518986": "2025-01-01",
}

def check_premium_access(user_id):
    """Check if user has premium access"""
    user_id_str = str(user_id)
    
    if user_id_str in PREMIUM_USERS:
        expiration_date = datetime.datetime.strptime(PREMIUM_USERS[user_id_str], "%Y-%m-%d")
        current_date = datetime.datetime.now()
        
        if current_date < expiration_date:
            return True, expiration_date
    return False, None

def check_user():
    try:
        user_id = int(input("Enter your Telegram User ID: "))  
    except ValueError:
        print("❌ Invalid ID! Numbers only.")
        exit()

    has_access, expiration_date = check_premium_access(user_id)
    
    if not has_access:
        print("\033[91m🚫 PREMIUM ACCESS REQUIRED!")
        print("Contact @hackxpy for access")
        exit()
    else:
        # Calculate remaining time
        current_date = datetime.datetime.now()
        remaining_time = expiration_date - current_date
        days = remaining_time.days
        hours = remaining_time.seconds // 3600
        
        print(f"\033[92m✅ Premium Access Granted!")
        print(f"⏰ Subscription valid until: {expiration_date.strftime('%Y-%m-%d')}")
        print(f"⏳ Time remaining: {days} days, {hours} hours")

# Run check at start
check_user()