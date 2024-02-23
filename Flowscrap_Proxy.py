import requests
import threading
import random
import os

proxyList = [] # there are two sample proxy ip

def file_opener(filetoopen):
    # Initialize an empty list to store proxy information
    proxyList = []

    # Open the specified file in read mode ("r")
    with open(filetoopen, "r") as file:
        # Print a message indicating that the proxy list is being filled
        print("Filling the proxy list")

        # Read the first line from the file and remove leading/trailing whitespaces
        line = file.readline().strip()

        # Continue reading lines from the file until reaching the end
        while line:
            # Append the current line to the proxy list
            proxyList.append(line)

            # Read the next line from the file and remove leading/trailing whitespaces
            line = file.readline().strip()

    # Print the size of the filled proxy list
    print(f"Size of proxy list to test: {len(proxyList)} ")

    # Return the filled proxy list
    return proxyList

def proxytest(begin, end, name_extention):
    # Iterate through the range of proxyList indices from 'begin' to 'end - 1'
    for i in range(begin, end - 1):
        # Construct a proxy string by concatenating 'name_extention' with the current proxy from proxyList
        socks_proxy = name_extention + proxyList[i]

        # Define a dictionary with proxy configuration for both HTTPS and HTTP
        proxies = {
            "https": socks_proxy,
            "http": socks_proxy
        }

        try:
            # Attempt to make a GET request using the specified proxy and a timeout of 3 seconds
            r = requests.get("https://crt.sh/?d=100", proxies=proxies, timeout=3)
            
            # Check if the response status code indicates success
            r.raise_for_status()

            # If successful, print a message indicating that the proxy is good
            print(f"Proxy {name_extention}{proxyList[i]} is good")

            # Append the good proxy to the "Good_Proxies.txt" file
            with open("Good_Proxies.txt", "a") as file:
                file.write(f"{name_extention}{proxyList[i]}\n")
        
        except:
            # If an exception occurs (e.g., timeout, connection error), ignore and continue to the next proxy
            pass
    
def get_random_proxy():
    # Assuming proxyList is defined and contains proxies gives a random one
    return random.choice(proxyList)

def make_requests_with_proxies(url, begin, end):
    folder_name = "Certificates"
    
    # Create the 'Certificates' folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    # Get a random proxy from the proxyList
    proxies = get_random_proxy()
    print(f"At proxy {proxies}")
    
    # Loop through the range of indices from 'begin' to 'end-1'
    for i in range(begin, end - 1):
        try:
            # Create a dictionary with proxy configuration for both HTTPS and HTTP
            proxy = {"https": proxies, "http": proxies}
            
            # Make a GET request using the specified URL and proxy, with a timeout of 3 seconds
            r = requests.get(f"{url}{i}", proxies=proxy, timeout=2)
            r.raise_for_status()  # Raise an HTTPError for bad responses

            # Save the response content (certificate) to a file
            file_path = os.path.join(folder_name, f"{i}.crt")
            with open(file_path, mode="wb") as file:
                file.write(r.content)
            
            # Print a success message with the request index and the file path
            print(f"Request {i} successful. File saved at: {file_path}")
        
        except requests.exceptions.RequestException as e:
            # If an exception occurs (e.g., timeout, connection error), get a new random proxy
            proxies = get_random_proxy()  # Get a new random proxy


if __name__ == '__main__':
    while True:
        # Get the number of threads from the user input
        num_thread_cert = input("\nHello! We are going to collect certificates. How many threads do you want for it ? ")
        
        try:
            num_thread_cert = int(num_thread_cert)
            break  # Exit the loop if input is a valid integer
        except ValueError:
            print("Please enter a valid number.")

    while True:
        # Ask the user if they want to create a 'Good_Proxies.txt' file
        answer = input("\nDo you wish to create a 'Good_Proxies.txt' file? (y/n) ").lower()
        
        if answer == 'y' :
            num_thread = 1500  # Define the number of threads here

            #
            # Testing for SOCKS5
            #

            # Open the file "SOCKS5.txt" and get the proxy list
            proxyList = file_opener("SOCKS5.txt")
            print("Looking for good proxies in file SOCKS5.txt")

            # Calculate the size of each thread's portion of the proxy list
            size = round(len(proxyList) / num_thread)
            print(size)

            # Create a list to store thread objects
            zactrobo = []

            # Create threads for testing SOCKS5 proxies
            for i in range(num_thread):
                zactrobo.append(threading.Thread(target=proxytest, args=((i - 1) * round(size), i * round(size), "socks5://")))

            # Start the SOCKS5 threads
            for i in zactrobo:
                i.start()

            # Wait for all SOCKS5 threads to finish
            for i in zactrobo:
                i.join()

            print("All threads for SOCKS5 have finished.")

            #
            # Testing for SOCKS4
            #

            # Open the file "SOCKS4.txt" and get the proxy list
            proxyList = file_opener("SOCKS4.txt")
            print("Looking for good proxies in file SOCKS4.txt")

            # Calculate the size of each thread's portion of the proxy list
            size = round(len(proxyList) / num_thread)

            # Create threads for testing SOCKS4 proxies
            zactrobo = []
            for i in range(num_thread):
                zactrobo.append(threading.Thread(target=proxytest, args=((i - 1) * round(size), i * round(size), "socks4://")))

            # Start the SOCKS4 threads
            for i in zactrobo:
                i.start()

            # Wait for all SOCKS4 threads to finish
            for i in zactrobo:
                i.join()

            print("All threads for SOCKS4 have finished.")

            #
            # Testing for HTTP
            #

            # Open the file "HTTP.txt" and get the proxy list
            proxyList = file_opener("HTTP.txt")
            print("Looking for good proxies in file HTTP.txt")

            # Calculate the size of each thread's portion of the proxy list
            size = round(len(proxyList) / num_thread)

            # Create threads for testing HTTP proxies
            zactrobo = []
            for i in range(num_thread):
                zactrobo.append(threading.Thread(target=proxytest, args=((i - 1) * round(size), i * round(size), "http://")))

            # Start the HTTP threads
            for i in zactrobo:
                i.start()

            # Wait for all HTTP threads to finish
            for i in zactrobo:
                i.join()

            print("All threads for HTTP have finished.")
            break # Exit the loop
            
        if answer == 'n' :
            break  # Exit the loop if input is 'n'
        else:
            print("Please enter 'y' or 'n'.")

    # Open the 'Good_Proxies.txt' file and get the proxy list
    proxyList = file_opener("Good_Proxies.txt")

    sample = 400000000
    zactrobo = []

    # Calculate the size of each thread's portion of the sample
    size = abs(sample / num_thread_cert)

    # Create threads for making requests with proxies
    for i in range(num_thread_cert):
        zactrobo.append(threading.Thread(target=make_requests_with_proxies, args=("https://crt.sh/?d=", (i - 1) * round(size), i * round(size))))

    # Start the threads for making requests
    for i in zactrobo:
        i.start()

    # Wait for all threads to finish
    for i in zactrobo:
        i.join()