import re
import datetime
import time

def waiting(time_from_gpt):
    time_pattern = r'(\d{1,2}:\d{2} [AP]M)'
    match = re.search(time_pattern, time_from_gpt)
    if match:
        time_str = match.group(0)
        print("Found time:", time_str)
    else:
        print("Time not found")
        return

    current_time = datetime.datetime.now().strftime("%I:%M %p")
    print("Current time:", current_time)

    # Convert current time and desired time to datetime objects
    current_time_dt = datetime.datetime.strptime(current_time, "%I:%M %p")
    desired_time_dt = datetime.datetime.strptime(time_str, "%I:%M %p")

    # Check if desired time is in the future compared to the current time
    if desired_time_dt <= current_time_dt:
        print("Desired time is in the past or the same as the current time.")
        return

    # Calculate the time difference in seconds
    time_diff_seconds = (desired_time_dt - current_time_dt).total_seconds()
    print("Time difference in seconds:", time_diff_seconds)

    total_seconds = max(0, int(time_diff_seconds))  # Ensure non-negative total_seconds

    if total_seconds > 0:
        print("Waiting for", total_seconds, "seconds")
        time.sleep(total_seconds)
        print("Waited for", total_seconds, "seconds")
    else:
        print("No need to wait")

# Example usage
time_from_gpt = "You have reached the current usage cap for GPT-4 at 7:16 PM"
waiting(time_from_gpt)


def main():
    waiting("You've reached the current usage cap for GPT-4."
            " You can continue with the default model now, or try again after 7:16 PM. Learn more")
    time.sleep(10000)

main()