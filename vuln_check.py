# Joker Tools, a tools made for ethical hacking purposes
# Made by JordanIsADev (C) Github JordanIsADev

# Importing necessary libraries
import os; from os import system as command
import time
import requests
from bs4 import BeautifulSoup
from colorama import *
init()

# Program display banner
banner = r"""
     __  __           ___           ____     __                     __         
    /\ \/\ \         /\_ \         /\  _`\  /\ \                   /\ \        
    \ \ \ \ \  __  __\//\ \     ___\ \ \/\_\\ \ \___      __    ___\ \ \/'\    
     \ \ \ \ \/\ \/\ \ \ \ \  /' _ `\ \ \/_/_\ \  _ `\  /'__`\ /'___\ \ , <    Version: 1.0
      \ \ \_/ \ \ \_\ \ \_\ \_/\ \/\ \ \ \L\ \\ \ \ \ \/\  __//\ \__/\ \ \\`\  
       \ `\___/\ \____/ /\____\ \_\ \_\ \____/ \ \_\ \_\ \____\ \____\\ \_\ \_\
        `\/__/  \/___/  \/____/\/_/\/_/\/___/   \/_/\/_/\/____/\/____/ \/_/\/_/

               Website Vulnerability Checker (C) Github: JordanIsADev
"""

# Create a class for loggingg purpose
class Logger:
    def Info(message : str):
        """Function to send message for information type"""
        print(f"{Style.RESET_ALL}[{Fore.YELLOW}INFO{Style.RESET_ALL}] {message}")

    def Success(message : str):
        """Function to send message for success type"""
        print(f"{Style.RESET_ALL}[{Fore.GREEN}SUCCESS{Style.RESET_ALL}] {message}")

    def Error(message : str):
        """Function to send message for error type"""
        print(f"{Style.RESET_ALL}[{Fore.RED}ERROR{Style.RESET_ALL}] {message}")

# Define a class for vulnerability checking needs
class Check:
    def __init__(self, url):
        """Define the main classes and important variable"""
        self.url = url

    def check_sql_injection(self):
        """Checks for any SQLi-related vulnerability"""
        sqli_payload = "' OR '1'='1"
        try:
            response = requests.get(self.url + sqli_payload)
            response.raise_for_status()
            if "SQL syntax" in response.text or "mysql_fetch" in response.text:
                return True
        except:
            return False
        
    def check_xss(self):
        """Checks for XSS Cross Scripting vulnerability"""
        xss_payload = "<script>alert('XSS')</script>"
        response = requests.get(self.url, params={"input": xss_payload})
        if xss_payload in response.text:
            return True
        return False
    
    def check_file_upload(self):
        """Checks for file upload vulnerability"""
        if os.path.exists('test.html'):
            files = {'file': open('test.html', 'rb')}
            response = requests.post(self.url, files=files)
            if 'text/html' in response.headers['Content-Type']:
                Logger.Info("Received HTML content.")
            else:
                Logger.Info("Unexpected content type:", response.headers['Content-Type'])
            if "test.html" in response.text:
                return True
            return False
        else:
            Logger.Error("'test.html' files does not exist, please create one")
    
    def check_vulnerabilities(self):
        """Gather all the functions into one necessary function"""
        Logger.Info(f"Checking {self.url} for vulnerabilities...")
        results = {
        "SQL Injection": self.check_sql_injection(),
        "XSS": self.check_xss(),
        "File Upload": self.check_file_upload()
        }
        for vulnerability, found in results.items():
            if found:
                Logger.Success(f"{vulnerability} vulnerability found!")
            else:
                Logger.Error(f"{vulnerability} vulnerability not found.")

# Create the main function
def main():
    """The final function to handle all function in one set"""
    command("cls")
    print(banner)
    while True:
        choice = input("Do you want to do multiple target or no? (Y/n): ")
        if choice.lower() == "n":
            target_url = input("Type in your target URL: ")
            check = Check(target_url)
            check.check_vulnerabilities()
        elif choice.lower() == "y":
            target_path = input("Type in your list file path: ")
            if os.path.exists(target_path):
                with open(target_path, 'r', encoding='utf-8') as files:
                    result = files.readlines()
                    for line in result:
                        check = Check(line)
                        check.check_vulnerabilities()
            else:
                Logger.Error("Files does not exist!")

# Run the function
if __name__ == "__main__":
    main()