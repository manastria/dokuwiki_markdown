import re
import os
import time
from pathlib import Path

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def indent_call_out(match_obj):
    # Recupere le contenu des groupes
    match1 = match_obj.group(1)
    content_tag = match_obj.group(2)

    # test le type de tag et ajoute le type de callout
    if "tip" in match1:
        content_tag = "[!info] " + content_tag

    if "warn" in match1 or "important" in match1:
        content_tag = "[!warning] " + content_tag

    # Ajoute un chevron devant le contenu pour le callout
    content_tag = re.sub(r"^(.*)", "> \\1", content_tag, 0, re.MULTILINE)

    # Supprime les lignes vides
    lines = content_tag.split("\n")
    filtered = filter(lambda x: not re.match(r'^\s*>?\s*$', x), lines)
    content_tag = "\n".join(filtered)


    return content_tag


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    filename = r"H:\Documents\Obsidian\wiki\gand\proxylinux.md"
    timestr = time.strftime("%Y%m%d-%H%M%S")
    stf = Path(filename).stem    # Recupere uniquement le nom du fichier sans extension
    backup_filename = os.path.join(r"f:\temp", stf+"_"+timestr+".md")

    # Open the file and read its contents
    with open(filename, "r", encoding='utf-8') as f:
        contents = f.read()

    # Faire une sauvegarde
    with open(backup_filename, "w", encoding='utf-8') as f:
        f.write(contents)

    new_contents = contents
    # Replace the contents of the "p" tag

    new_contents = re.sub(r'<span class="underline">(.*?)</span>', r'<u>\1</u>', new_contents, 0, re.DOTALL | re.MULTILINE)
    new_contents = re.sub(r'\\<key\\>(.*?)\\</key\\>', r'<kbd>\1</kbd>', new_contents, 0, re.DOTALL | re.MULTILINE)
    new_contents = re.sub(r'\\<cli.*?\\>(.*?)\\</cli\\>', '\n```\n\\1\n```\n', new_contents, 0, re.DOTALL | re.MULTILINE)
    new_contents = re.sub(r"\\<WRAP (.*?)\\>(.*?)\\</WRAP\\>", indent_call_out, new_contents, 0, re.DOTALL | re.MULTILINE)
    new_contents = re.sub(r" \\!", r' !', new_contents, 0, re.DOTALL | re.MULTILINE)
    new_contents = re.sub(r"\\!", r'!', new_contents, 0, re.DOTALL | re.MULTILINE)

    # Windows ➡ Unix
    #new_contents = new_contents.replace('\n\n', '\n')

    # Write the new contents back to the file
    with open(filename, "w", encoding='utf-8', newline='\n') as f:
        f.write(new_contents)
