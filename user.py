import json

import requests

BASE_URL = 'http://127.0.0.1:5000'


def add_link():
    link = input("Enter the link to add: ")
    data = {
        "link": link
    }
    response = requests.post(f"{BASE_URL}/api/links", headers={'Content-Type': 'application/json'},
                             data=json.dumps(data))
    if response.status_code == 201:
        print("Link added successfully!")
    else:
        print(f"Error: {response.status_code}")
        print(response.json())


def show_links():
    response = requests.get(f"{BASE_URL}/api/links")
    if response.status_code == 200:
        links = response.json()
        for i, link in enumerate(links):
            print(f"{i + 1}. {link}")
        return links
    else:
        print(f"Error: {response.status_code}")
        print(response.json())
        return []


def delete_link_by_number():
    links = show_links()
    if not links:
        print("No links to delete.")
        return

    try:
        number = int(input("Enter the number of the link to delete: "))
        if number < 1 or number > len(links):
            print("Invalid number.")
            return

        link_to_delete = links[number - 1]
        data = {
            "link": link_to_delete
        }
        response = requests.delete(f"{BASE_URL}/api/links", headers={'Content-Type': 'application/json'},
                                   data=json.dumps(data))
        if response.status_code == 200:
            print("Link deleted successfully!")
        else:
            print(f"Error: {response.status_code}")
            print(response.json())
    except ValueError:
        print("Invalid input. Please enter a valid number.")


def extract_link():
    links = show_links()
    if not links:
        print("No links to extract.")
        return

    print("Enter the numbers of the links to extract, separated by commas (e.g., 1,2,3) or 'all' to extract all links:")
    choice = input("Your choice: ")

    if choice.lower() == 'all':
        selected_links = links
    else:
        try:
            selected_numbers = [int(x) for x in choice.split(',')]
            selected_links = [links[i - 1] for i in selected_numbers if 1 <= i <= len(links)]
        except ValueError:
            print("Invalid input. Please enter valid numbers.")
            return

    for link in selected_links:
        data = {
            "link": link
        }
        response = requests.post(f"{BASE_URL}/api/extract", headers={'Content-Type': 'application/json'},
                                 data=json.dumps(data))
        if response.status_code == 200:
            extracted_data = response.json()
            print(f"Extracted data for {link}:")
            print(json.dumps(extracted_data, indent=2, ensure_ascii=False))
        else:
            print(f"Error extracting {link}: {response.status_code}")
            print(response.json())


def cluster_data():
    response = requests.get(f"{BASE_URL}/api/cluster")
    if response.status_code == 200:
        clustered_data = response.json()
        print("Clustered data:")
        print(json.dumps(clustered_data, indent=2, ensure_ascii=False))
    else:
        print(f"Error: {response.status_code}")
        print(response.json())


def find_clustered_links():
    texts = input("Enter the clustered texts to find links for, separated by commas: ").split(',')
    data = {
        "texts": [text.strip() for text in texts]
    }
    response = requests.post(f"{BASE_URL}/api/find-links", headers={'Content-Type': 'application/json'},
                             data=json.dumps(data))
    if response.status_code == 200:
        result_links = response.json()
        print("Clustered links:")
        print(json.dumps(result_links, indent=2, ensure_ascii=False))
    else:
        print(f"Error: {response.status_code}")
        print(response.json())


def search_word():
    word = input("Enter the word or phrase to search: ")
    data = {
        "query": word
    }
    response = requests.post(f"{BASE_URL}/api/search/query", headers={'Content-Type': 'application/json'},
                             data=json.dumps(data))
    if response.status_code == 200:
        results = response.json()
        for result in results:
            print(json.dumps(result["_source"], indent=2, ensure_ascii=False))
    else:
        print(f"Error: {response.status_code}")
        print(response.json())


def show_menu():
    while True:
        print("\nMenu:")
        print("1. Add a link")
        print("2. Show links")
        print("3. Delete a link by number")
        print("4. Extract a link")
        print("5. Cluster data")
        print("6. Find clustered links")
        print("7. Search for a word or phrase")
        print("8. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_link()
        elif choice == '2':
            show_links()
        elif choice == '3':
            delete_link_by_number()
        elif choice == '4':
            extract_link()
        elif choice == '5':
            cluster_data()
        elif choice == '6':
            find_clustered_links()
        elif choice == '7':
            search_word()
        elif choice == '8':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    show_menu()
