import lxml
import re
import requests
import os
import tkinter as tk
from tkinter import filedialog
from urllib.parse import urlparse
from bs4 import BeautifulSoup

root = tk.Tk()
root.attributes("-topmost", True)
root.withdraw()

def retrieve_base_link(url):
    return urlparse(url).netloc

def retrieve_base_path(url):
    return urlparse(url).path


def create_folder(chosen_name):
    destination_path = os.path.join(os.getcwd(), chosen_name)
    if os.path.isdir(destination_path) == False:
        os.mkdir(destination_path)
    return destination_path

def is_downloadable(url):
    """
    Does the url contain a downloadable resource
    """
    try:
        h = requests.head(url, allow_redirects=True)
        header = h.headers
        content_type = header.get('content-type')
        if content_type != None:
            if 'text' in content_type.lower():
                return False
            if 'html' in content_type.lower():
                return False

        if '?' in url or '=' in url: return False
        
        path, filename = os.path.split(retrieve_base_path(url))
        if '.' not in filename:
            return False
        
        return True
    except Exception as e:
        return False

def get_filename(dir):
    head, tail = os.path.split(dir)
    if tail == "" : return False
    return tail

def parse_css_file(link):
    r = requests.get(link, timeout=10, allow_redirects=True)
    for url in re.findall(r'url\((.*?)\)', r.text):
        url = url.replace("\'","")
        url = url.replace("\"","")
        url_path = urlparse(link).path
        path, filename = os.path.split(url_path)
        download_link = ""
        if '../' in url:
            destination_url = url.split('/')
            path = path.split('/')
            if(path[-1] == ""): path.pop()
            for i in range(1, (url.count('../')+1)):
                destination_url.pop(0)
                path.pop()
            destination_url = '/'.join(destination_url).replace("\"","")
            path = '/'.join(path)
            download_link = f'https://{base_website}{path}/{destination_url}'
            #print(f'Download Link: {download_link} \nDestination Path: {destination_url}\nPath: {path}')
            
            try:
                download_file(download_link, f'{path}/{destination_url}', destination_folder)
            except OSError:
                print(f'DOWNLOADING ERROR: {url}')

        else:
            if 'https' in url:
                try:
                    download_file(url, retrieve_base_path(url), destination_folder)
                except OSError:
                    print(f'DOWNLOADING ERROR: {url}')
            else:
                download_link = f'https://{base_website}/{url}'
                try:
                    download_file(download_link, url, destination_folder)
                except OSError:
                    print(f'DOWNLOADING ERROR: {url}')
                    pass


def retrieve_page_html(url):
    
    HEADERS = {
        'Accept': 'text/html',
        'Accept-Language': 'en-gb',
        'Cache-Control': 'no-cache',
        'Connection':'keep-alive',
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15"
    }
    return requests.get(url, headers=HEADERS, timeout=30).text

def download_file(url, url_file_path, storage_directory):
    if '.css' in url: parse_css_file(url)
    if '?' in url or '=' in url:
        url = url.split('?')[0]
        url_file_path = url_file_path.split('?')[0]
        

    path, filename = os.path.split(url_file_path)
    storage_destination = f'{storage_directory}/{path}'

    if os.path.isdir(storage_destination) == False:
        os.makedirs(storage_destination)

    file_storage = f'{storage_destination}/{filename}'

    if os.path.isfile(file_storage):
        #print(f'File already existing {file_storage}')
        pass
    else:
        r = requests.get(url, allow_redirects=True, timeout=10)
        open(file_storage, 'wb').write(r.content)


def parse_a_tags(soup, base_url):
    for link in soup.find_all('a'):
        file_pointer = link.get("href")
        if file_pointer == None: continue
        if 'http' not in file_pointer:
            link['href'] = f'https://{base_url}{file_pointer}'

def parse_tags(soup, tag, base_path):
    for link in soup.find_all(tag):
        file_pointer = None
        if tag.lower() == "link":
            file_pointer = link.get("href")
        else:
            file_pointer = link.get("src")

        if file_pointer == None:
            continue
        elif 'http' in file_pointer or 'www' in file_pointer:
            # CORRECTION OF ANY POSSIBLE URL PROBLEMS
            if '//' in file_pointer and 'http' not in file_pointer: file_pointer = file_pointer.replace('//','/')
            if 'http' not in file_pointer: file_pointer = f'https://{base_website}{file_pointer}'
            # -----
            if is_downloadable(file_pointer):
                new_base_url = retrieve_base_link(file_pointer)
                new_base_path = retrieve_base_path(file_pointer)
                if tag.lower() == "link":
                    link['href'] = new_base_path
                    download_file(file_pointer, link['href'], destination_folder)
                else:
                    link['src'] = new_base_path
                    download_file(file_pointer, link['src'], destination_folder)
            continue
        path, filename = os.path.split(file_pointer)
        if '.' not in filename: continue
        download_link = f'https://{base_path}/{file_pointer}'
        download_file(download_link, file_pointer, destination_folder)


if __name__ == '__main__':
    selecting_site = True
    selecting_filename = True
    website_path = None
    filename = None
    base_website = None

    # DESTINATION OF SCRAPED SOURCE
    destination_folder = None
    choice = input("[SYSTEM] Choose existing directory  [Y/N] \n>>> ")
    if "y" in choice.lower():
        destination_folder = filedialog.askdirectory()
    else:
        name_choice = input("[SYSTEM] Name of Result Folder \n>>> ")
        destination_folder = create_folder(name_choice)
    # ------
    

    while selecting_filename:
        filename = input("[SYSTEM] Please enter desired filename \n>>> ")
        
        if os.path.isfile(f'{destination_folder}/index.html') == True: 
            print(f"[SYSTEM] {destination_folder}/{filename} already exists, are you sure you want to overwrite?")
        choice = input(f"[SYSTEM] Is {filename} the name you want? [Y/N] \n>>> ")
        if "y" in choice.lower():
            selecting_filename = False


    # SELECT FILE URL
    while selecting_site:
        website_path = input("[SYSTEM] Please enter website URL \n>>> ")
        choice = input(f"[SYSTEM] Is {website_path} the link you want? [Y/N] \n>>> ")
        if "y" in choice.lower():
            selecting_site = False

    base_website = retrieve_base_link(website_path)
    print(base_website)
    #------

    # WEBSITE URL OR FILE SELECTION DIRECTORY
    # BEGIN PARSING
    page_content = None
    print("\n[SYSTEM] How do you want to retrieve HTML code for website ")
    CACHE_FILE_CHOICE = input(">>> [1] Website URL\n>>> [2] Choose file from Computer\n>>>  ")
    
    if CACHE_FILE_CHOICE == "1":
        page_content = BeautifulSoup(retrieve_page_html(website_path), "lxml").prettify()
        if os.path.isfile(f'{destination_folder}/index.html') == False:
            open(f'{destination_folder}/index.html', 'w+').write(page_content)
    else:
        HTML_SOURCE = open(filedialog.askopenfilename(),"r",encoding='utf8')
        page_content = BeautifulSoup(HTML_SOURCE, "lxml").prettify()

    soup = BeautifulSoup(page_content, "lxml")
    
    parse_a_tags(soup, base_website)
    parse_tags(soup, "img", base_website)
    parse_tags(soup, "link", base_website)
    parse_tags(soup, "script", base_website)

    fileResult = soup.prettify()
    open(f'{destination_folder}/{filename}', 'w+', errors='ignore').write(soup.prettify())
    # ------
    # ------
    