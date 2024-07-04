import json
import webbrowser
import customtkinter as ctk
import requests
from tkinter import messagebox

BASE_URL = 'http://127.0.0.1:5000'


class LinkManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Link Manager")
        self.root.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        self.tab_control = ctk.CTkTabview(self.root, width=780, height=550)
        self.tab_control.pack(expand=1, fill="both")

        # Links Management Tab (combined tab)
        self.tab_control.add("Manage Links")
        self.create_links_management_tab(self.tab_control.tab("Manage Links"))

        # Extract Link Tab
        self.tab_control.add("Extract Link")
        self.create_extract_link_tab(self.tab_control.tab("Extract Link"))

        # Cluster Data Tab
        self.tab_control.add("Cluster Data")
        self.create_cluster_data_tab(self.tab_control.tab("Cluster Data"))

        # Find Clustered Links Tab
        self.tab_control.add("Find Clustered Links")
        self.create_find_clustered_links_tab(self.tab_control.tab("Find Clustered Links"))

        # Search Word Tab
        self.tab_control.add("Search Word")
        self.create_search_word_tab(self.tab_control.tab("Search Word"))

    def create_links_management_tab(self, tab):
        self.frame_add_link = ctk.CTkFrame(tab, width=750, height=100, corner_radius=10)
        self.frame_add_link.pack(pady=10, padx=10, fill="x")

        self.frame_delete_link = ctk.CTkFrame(tab, width=750, height=150, corner_radius=10)
        self.frame_delete_link.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(self.frame_add_link, text="Enter the link to add:").pack(side="left", padx=10, pady=10)
        self.entry_add_link = ctk.CTkEntry(self.frame_add_link, width=400)
        self.entry_add_link.pack(side="left", padx=10, pady=10)
        ctk.CTkButton(self.frame_add_link, text="Add Link", command=self.add_link).pack(side="left", padx=10, pady=10)

        self.scrollable_links = ctk.CTkScrollableFrame(self.frame_delete_link, width=700, height=100, corner_radius=10)
        self.scrollable_links.pack(pady=10)

        self.show_links()

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
            self.entry_add_link.delete(0, ctk.END)
            self.show_links()
        else:
            messagebox.showerror("Error", f"Error: {response.status_code}\n{response.json()}")

    def show_links(self):
        response = requests.get(f"{BASE_URL}/api/links")
        if response.status_code == 200:
            links = response.json()
            for widget in self.scrollable_links.winfo_children():
                widget.destroy()  # پاک کردن محتوای قدیمی

            for i, link in enumerate(links):
                link_frame = ctk.CTkFrame(self.scrollable_links, width=650, height=30, corner_radius=10)
                link_frame.pack(pady=2, padx=10, fill="x")

                link_label = ctk.CTkLabel(link_frame, text=f"{i + 1}. {link}", width=550)
                link_label.pack(side="left", padx=10)

                delete_button = ctk.CTkButton(link_frame, text="Delete", command=lambda l=link: self.delete_specific_link(l))
                delete_button.pack(side="right", padx=10)
        else:
            messagebox.showerror("Error", f"Error: {response.status_code}\n{response.json()}")

    def delete_specific_link(self, link):
        data = {"link": link}
        response = requests.delete(f"{BASE_URL}/api/links", headers={'Content-Type': 'application/json'},
                                   data=json.dumps(data))
        if response.status_code == 200:
            messagebox.showinfo("Success", "Link deleted successfully!")
            self.show_links()  # به‌روزرسانی لیست پس از حذف لینک
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
                    self.entry_delete_link.delete(0, ctk.END)
                    self.show_links()  # به‌روزرسانی لیست پس از حذف لینک
                else:
                    messagebox.showerror("Error", f"Error: {response.status_code}\n{response.json()}")
            else:
                messagebox.showerror("Error", f"Error: {response.status_code}\n{response.json()}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid number.")


    def create_extract_link_tab(self, tab):
        ctk.CTkButton(tab, text="Refresh Links", command=self.show_links_extract).pack(pady=10)  # دکمه Refresh Links

        self.frame_extract_link = ctk.CTkFrame(tab, width=750, height=100, corner_radius=10)
        self.frame_extract_link.pack(fill="x")

        self.scrollable_extract_links = ctk.CTkScrollableFrame(self.frame_extract_link, width=750, height=100, corner_radius=10)
        self.scrollable_extract_links.pack(pady=10)

        ctk.CTkLabel(tab, text="Enter the numbers of the links to extract, separated by commas or 'all':").pack(pady=10)
        self.entry_extract_link = ctk.CTkEntry(tab, width=200)
        self.entry_extract_link.pack(pady=10)
        ctk.CTkButton(tab, text="Extract Links", command=self.extract_link).pack(pady=10)

        self.frame_extract_data = ctk.CTkFrame(tab, width=750, height=100, corner_radius=10)
        self.frame_extract_data.pack(pady=5, padx=5, fill="x")

        self.scrollable_extracted_data = ctk.CTkScrollableFrame(self.frame_extract_data, width=750, height=300, corner_radius=10)
        self.scrollable_extracted_data.pack(pady=5)

        # نمایش اولیه لینک‌ها
        self.show_links_extract()

    def show_links_extract(self):
        response = requests.get(f"{BASE_URL}/api/links")
        if response.status_code == 200:
            links = response.json()
            for widget in self.scrollable_extract_links.winfo_children():
                widget.destroy()
            for i, link in enumerate(links):
                ctk.CTkLabel(self.scrollable_extract_links, text=f"{i + 1}. {link}").pack(pady=0)
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

            for widget in self.scrollable_extracted_data.winfo_children():
                widget.destroy()
            for link in selected_links:
                data = {"link": link}
                response = requests.post(f"{BASE_URL}/api/extract", headers={'Content-Type': 'application/json'},
                                         data=json.dumps(data))
                if response.status_code == 200:
                    extracted_data = response.json()
                    self.display_extracted_data(link, extracted_data)
                else:
                    ctk.CTkLabel(self.scrollable_extracted_data,
                                 text=f"Error extracting {link}: {response.status_code}\n{response.json()}").pack(
                        pady=5)
        else:
            messagebox.showerror("Error", f"Error: {response.status_code}\n{response.json()}")

    def display_extracted_data(self, link, data):
        for widget in self.scrollable_extracted_data.winfo_children():
            widget.destroy()  # پاک کردن محتوای قدیمی

        ctk.CTkLabel(self.scrollable_extracted_data, text=f"Extracted data for {link}:", wraplength=750).pack(pady=5)

        for key, value in data.items():
            link_button = ctk.CTkButton(self.scrollable_extracted_data, text=key,
                                        command=lambda url=value: self.open_link(url))
            link_button.pack(pady=2)

        self.scrollable_extracted_data.update_idletasks()  # به‌روزرسانی ویجت‌ها

    def open_link(self, url):
        webbrowser.open(url)

    def create_cluster_data_tab(self, tab):
        ctk.CTkButton(tab, text="Cluster Data", command=self.cluster_data).pack(pady=10)
        self.frame_clustered_data = ctk.CTkFrame(tab, width=750, height=300, corner_radius=10)
        self.frame_clustered_data.pack(pady=5, padx=5, fill="x")
        self.scrollable_clustered_data = ctk.CTkScrollableFrame(self.frame_clustered_data, width=700, height=200)
        self.scrollable_clustered_data.pack(pady=10)

    def cluster_data(self):
        response = requests.get(f"{BASE_URL}/api/cluster")
        if response.status_code == 200:
            clustered_data = response.json()
            for widget in self.scrollable_clustered_data.winfo_children():
                widget.destroy()
            for key, value in clustered_data.items():
                ctk.CTkLabel(self.scrollable_clustered_data, text=f"{key}: {value}", wraplength=680).pack(pady=5)
        else:
            messagebox.showerror("Error", f"Error: {response.status_code}\n{response.json()}")

    def create_find_clustered_links_tab(self, tab):
        ctk.CTkLabel(tab, text="Enter the clustered texts to find links for, separated by commas:").pack(pady=10)
        self.entry_find_clustered_links = ctk.CTkEntry(tab, width=200)
        self.entry_find_clustered_links.pack(pady=10)
        ctk.CTkButton(tab, text="Find Clustered Links", command=self.find_clustered_links).pack(pady=10)
        self.frame_text_find = ctk.CTkFrame(tab, width=750, height=300, corner_radius=10)
        self.frame_text_find.pack(pady=10, padx=10, fill="x")
        self.scrollable_text_find = ctk.CTkScrollableFrame(self.frame_text_find, width=700, height=200)
        self.scrollable_text_find.pack(pady=10)

    def find_clustered_links(self):
        texts = self.entry_find_clustered_links.get().split(',')
        data = {"texts": [text.strip() for text in texts]}
        response = requests.post(f"{BASE_URL}/api/find-links", headers={'Content-Type': 'application/json'},
                                 data=json.dumps(data))
        if response.status_code == 200:
            result_links = response.json()

            for widget in self.scrollable_text_find.winfo_children():
                widget.destroy()

            if result_links:
                for link in result_links:
                    link_text = json.dumps(link, indent=2, ensure_ascii=False)
                    ctk.CTkLabel(self.scrollable_text_find, text=link_text, wraplength=680).pack(pady=5)
            else:
                ctk.CTkLabel(self.scrollable_text_find, text="No links found for the given clusters.",
                             wraplength=680).pack(pady=5)
        else:
            messagebox.showerror("Error", f"Error: {response.status_code}\n{response.json()}")
    def create_search_word_tab(self, tab):
        ctk.CTkLabel(tab, text="Enter the word or phrase to search:").pack(pady=10)
        self.entry_search_word = ctk.CTkEntry(tab, width=200)
        self.entry_search_word.pack(pady=10)
        ctk.CTkButton(tab, text="Search", command=self.search_word).pack(pady=10)
        self.frame_search_results = ctk.CTkFrame(tab, width=750, height=300, corner_radius=10)
        self.frame_search_results.pack(pady=10, padx=10, fill="x")
        self.scrollable_search_results = ctk.CTkScrollableFrame(self.frame_search_results, width=700, height=200)
        self.scrollable_search_results.pack(pady=10)

    def search_word(self):
        word = self.entry_search_word.get()
        data = {"query": word}
        response = requests.post(f"{BASE_URL}/api/search/query", headers={'Content-Type': 'application/json'},
                                 data=json.dumps(data))
        if response.status_code == 200:
            results = response.json()
            for widget in self.scrollable_search_results.winfo_children():
                widget.destroy()
            for result in results:
                ctk.CTkLabel(self.scrollable_search_results,
                             text=json.dumps(result["_source"], indent=2, ensure_ascii=False), wraplength=680).pack(
                    pady=5)
        else:
            messagebox.showerror("Error", f"Error: {response.status_code}\n{response.json()}")


if __name__ == "__main__":
    root = ctk.CTk()
    app = LinkManagerApp(root)
    root.mainloop()