import json
import tkinter as tk
import webbrowser
from tkinter import ttk, messagebox

import requests

BASE_URL = 'http://127.0.0.1:5000'


class LinkManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Link Manager")

        self.create_widgets()

    def create_widgets(self):
        self.tab_control = ttk.Notebook(self.root)

        self.tab_add_link = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_add_link, text="Add Link")
        self.create_add_link_tab()

        self.tab_show_links = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_show_links, text="Show Links")
        self.create_show_links_tab()

        self.tab_delete_link = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_delete_link, text="Delete Link")
        self.create_delete_link_tab()

        self.tab_extract_link = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_extract_link, text="Extract Link")
        self.create_extract_link_tab()

        self.tab_cluster_data = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_cluster_data, text="Cluster Data")
        self.create_cluster_data_tab()

        self.tab_find_clustered_links = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_find_clustered_links, text="Find Clustered Links")
        self.create_find_clustered_links_tab()

        self.tab_search_word = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_search_word, text="Search Word")
        self.create_search_word_tab()

        self.tab_control.pack(expand=1, fill="both")

    def create_add_link_tab(self):
        ttk.Label(self.tab_add_link, text="Enter the link to add:").pack(pady=10)
        self.entry_add_link = ttk.Entry(self.tab_add_link, width=50)
        self.entry_add_link.pack(pady=10)
        ttk.Button(self.tab_add_link, text="Add Link", command=self.add_link).pack(pady=10)

    def add_link(self):
        link = self.entry_add_link.get()
        if not link:
            messagebox.showerror("Error", "Link is required")
            return

        data = {"link": link}
        response = requests.post(f"{BASE_URL}/api/links", headers={'Content-Type': 'application/json'},
                                 data=json.dumps(data))
        if response.status_code == 201:
            messagebox.showinfo("Success", "Link added successfully!")
            self.entry_add_link.delete(0, tk.END)
        else:
            messagebox.showerror("Error", f"Error: {response.status_code}\n{response.json()}")

    def create_show_links_tab(self):
        ttk.Button(self.tab_show_links, text="Show Links", command=self.show_links).pack(pady=10)
        self.text_show_links = tk.Text(self.tab_show_links, wrap=tk.WORD, width=80, height=20)
        self.text_show_links.pack(pady=10)

    def show_links(self):
        response = requests.get(f"{BASE_URL}/api/links")
        if response.status_code == 200:
            links = response.json()
            self.text_show_links.delete("1.0", tk.END)
            for i, link in enumerate(links):
                self.text_show_links.insert(tk.END, f"{i + 1}. {link}\n")
        else:
            messagebox.showerror("Error", f"Error: {response.status_code}\n{response.json()}")

    def create_delete_link_tab(self):
        ttk.Button(self.tab_delete_link, text="Show Links", command=self.show_links_delete).pack(pady=10)
        self.text_delete_links = tk.Text(self.tab_delete_link, wrap=tk.WORD, width=80, height=10)
        self.text_delete_links.pack(pady=10)
        ttk.Label(self.tab_delete_link, text="Enter the number of the link to delete:").pack(pady=10)
        self.entry_delete_link = ttk.Entry(self.tab_delete_link, width=10)
        self.entry_delete_link.pack(pady=10)
        ttk.Button(self.tab_delete_link, text="Delete Link", command=self.delete_link).pack(pady=10)

    def show_links_delete(self):
        response = requests.get(f"{BASE_URL}/api/links")
        if response.status_code == 200:
            links = response.json()
            self.text_delete_links.delete("1.0", tk.END)
            for i, link in enumerate(links):
                self.text_delete_links.insert(tk.END, f"{i + 1}. {link}\n")
        else:
            messagebox.showerror("Error", f"Error: {response.status_code}\n{response.json()}")

    def delete_link(self):
        try:
            number = int(self.entry_delete_link.get())
            response = requests.get(f"{BASE_URL}/api/links")
            if response.status_code == 200:
                links = response.json()
                if number < 1 or number > len(links):
                    messagebox.showerror("Error", "Invalid number")
                    return

                link_to_delete = links[number - 1]
                data = {"link": link_to_delete}
                response = requests.delete(f"{BASE_URL}/api/links", headers={'Content-Type': 'application/json'},
                                           data=json.dumps(data))
                if response.status_code == 200:
                    messagebox.showinfo("Success", "Link deleted successfully!")
                    self.entry_delete_link.delete(0, tk.END)
                    self.show_links_delete()
                else:
                    messagebox.showerror("Error", f"Error: {response.status_code}\n{response.json()}")
            else:
                messagebox.showerror("Error", f"Error: {response.status_code}\n{response.json()}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid number.")

    def create_extract_link_tab(self):
        ttk.Button(self.tab_extract_link, text="Show Links", command=self.show_links_extract).pack(pady=10)
        self.text_extract_links = tk.Text(self.tab_extract_link, wrap=tk.WORD, width=80, height=10)
        self.text_extract_links.pack(pady=10)
        ttk.Label(self.tab_extract_link,
                  text="Enter the numbers of the links to extract, separated by commas or 'all':").pack(pady=10)
        self.entry_extract_link = ttk.Entry(self.tab_extract_link, width=20)
        self.entry_extract_link.pack(pady=10)
        ttk.Button(self.tab_extract_link, text="Extract Links", command=self.extract_link).pack(pady=10)
        self.text_extracted_data = tk.Text(self.tab_extract_link, wrap=tk.WORD, width=200, height=20)
        self.text_extracted_data.pack(pady=10)

    def show_links_extract(self):
        response = requests.get(f"{BASE_URL}/api/links")
        if response.status_code == 200:
            links = response.json()
            self.text_extract_links.delete("1.0", tk.END)
            for i, link in enumerate(links):
                self.text_extract_links.insert(tk.END, f"{i + 1}. {link}\n")
        else:
            messagebox.showerror("Error", f"Error: {response.status_code}\n{response.json()}")

    def extract_link(self):
        choice = self.entry_extract_link.get()
        response = requests.get(f"{BASE_URL}/api/links")
        if response.status_code == 200:
            links = response.json()
            if choice.lower() == 'all':
                selected_links = links
            else:
                try:
                    selected_numbers = [int(x) for x in choice.split(',')]
                    selected_links = [links[i - 1] for i in selected_numbers if 1 <= i <= len(links)]
                except ValueError:
                    messagebox.showerror("Error", "Invalid input. Please enter valid numbers.")
                    return

            self.text_extracted_data.delete("1.0", tk.END)
            for link in selected_links:
                data = {"link": link}
                response = requests.post(f"{BASE_URL}/api/extract", headers={'Content-Type': 'application/json'},
                                         data=json.dumps(data))
                if response.status_code == 200:
                    extracted_data = response.json()
                    self.display_extracted_data(link, extracted_data)
                else:
                    self.text_extracted_data.insert(tk.END,
                                                    f"Error extracting {link}: {response.status_code}\n{response.json()}\n\n")
        else:
            messagebox.showerror("Error", f"Error: {response.status_code}\n{response.json()}")

    def display_extracted_data(self, link, data):
        self.text_extracted_data.insert(tk.END, f"Extracted data for {link}:\n")
        for key, value in data.items():
            link_button = ttk.Button(self.text_extracted_data, text=key, command=lambda url=value: self.open_link(url))
            self.text_extracted_data.window_create(tk.END, window=link_button)
            self.text_extracted_data.insert(tk.END, "\n")
        self.text_extracted_data.insert(tk.END, "\n")

    def open_link(self, url):
        webbrowser.open(url)

    def create_cluster_data_tab(self):
        ttk.Button(self.tab_cluster_data, text="Cluster Data", command=self.cluster_data).pack(pady=10)
        self.text_clustered_data = tk.Text(self.tab_cluster_data, wrap=tk.WORD, width=80, height=20)
        self.text_clustered_data.pack(pady=10)

    def cluster_data(self):
        response = requests.get(f"{BASE_URL}/api/cluster")
        if response.status_code == 200:
            clustered_data = response.json()
            self.text_clustered_data.delete("1.0", tk.END)
            self.text_clustered_data.insert(tk.END, json.dumps(clustered_data, indent=2, ensure_ascii=False))
        else:
            messagebox.showerror("Error", f"Error: {response.status_code}\n{response.json()}")

    def create_find_clustered_links_tab(self):
        ttk.Label(self.tab_find_clustered_links,
                  text="Enter the clustered texts to find links for, separated by commas:").pack(pady=10)
        self.entry_find_clustered_links = ttk.Entry(self.tab_find_clustered_links, width=50)
        self.entry_find_clustered_links.pack(pady=10)
        ttk.Button(self.tab_find_clustered_links, text="Find Clustered Links", command=self.find_clustered_links).pack(
            pady=10)
        self.text_find_clustered_links = tk.Text(self.tab_find_clustered_links, wrap=tk.WORD, width=80, height=20)
        self.text_find_clustered_links.pack(pady=10)

    def find_clustered_links(self):
        texts = self.entry_find_clustered_links.get().split(',')
        data = {"texts": [text.strip() for text in texts]}
        response = requests.post(f"{BASE_URL}/api/find-links", headers={'Content-Type': 'application/json'},
                                 data=json.dumps(data))
        if response.status_code == 200:
            result_links = response.json()
            self.text_find_clustered_links.delete("1.0", tk.END)
            self.text_find_clustered_links.insert(tk.END, json.dumps(result_links, indent=2, ensure_ascii=False))
        else:
            messagebox.showerror("Error", f"Error: {response.status_code}\n{response.json()}")

    def create_search_word_tab(self):
        ttk.Label(self.tab_search_word, text="Enter the word or phrase to search:").pack(pady=10)
        self.entry_search_word = ttk.Entry(self.tab_search_word, width=50)
        self.entry_search_word.pack(pady=10)
        ttk.Button(self.tab_search_word, text="Search", command=self.search_word).pack(pady=10)
        self.text_search_results = tk.Text(self.tab_search_word, wrap=tk.WORD, width=80, height=20)
        self.text_search_results.pack(pady=10)

    def search_word(self):
        word = self.entry_search_word.get()
        data = {"query": word}
        response = requests.post(f"{BASE_URL}/api/search/query", headers={'Content-Type': 'application/json'},
                                 data=json.dumps(data))
        if response.status_code == 200:
            results = response.json()
            self.text_search_results.delete("1.0", tk.END)
            for result in results:
                self.text_search_results.insert(tk.END, json.dumps(result["_source"], indent=2, ensure_ascii=False))
                self.text_search_results.insert(tk.END, "\n\n")
        else:
            messagebox.showerror("Error", f"Error: {response.status_code}\n{response.json()}")


if __name__ == "__main__":
    root = tk.Tk()
    app = LinkManagerApp(root)
    root.mainloop()
