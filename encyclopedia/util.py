import re
from random import choice

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def list_entries():
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))

def save_entry(title, content):
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))

def get_entry(title):
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return "###This entity is not exist, go ahead and create one!"

def searching(title):
    result = []
    for i in list_entries():
        if re.search(title, i, re.IGNORECASE) :
            result.append(i)  
    return result
           
def random():
    return choice(list_entries())

def compare(title1:str):
    result = False
    for i in list_entries():
        if title1.casefold() == i.casefold():
            result = True
            return result