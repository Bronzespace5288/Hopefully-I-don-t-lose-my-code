import datetime

def print_github_reminder():
    # Get the current date
    current_date = datetime.date.today()
    
    # Format the date as a string
    date_string = current_date.strftime("%A, %B %d, %Y")
    
    # Print the date and message
    print(f"Today's date: {date_string}")
    print("Remember to make your daily GitHub push!")
    print("Consistent contributions keep your skills sharp and your profile active.")

# Call the function
print_github_reminder()