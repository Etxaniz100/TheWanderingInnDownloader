from bs4 import BeautifulSoup
import requests
import os
import shutil
import time
import random

# BOOK DATA
book_title = "The Wandering Inn Volume 9 - Pirateaba"
book_author = "PirateAba"
cover_file = "BookCover.jpg"

chapter_list_directory = "chapters"
template_directory = "./Output/template"

def sustituteNames(file_name, author_name, book_name):
    file_text = ""
    with open(file_name, 'r', encoding='utf8') as file:
        file_text = file.read()
    file_text = file_text.replace("book_title", book_name)
    file_text = file_text.replace("author_name", author_name)
    with open(file_name, 'w', encoding='utf8') as file:
        file.write(file_text)


def getChapter(link):

    # Random request headers
    HEADERS_LIST = [
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:118.0) Gecko/20100101 Firefox/118.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        },
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive"
        },
        {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
            "Connection": "keep-alive"
        },
        {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive"
        }
    ]

    r = requests.get(link, headers=random.choice(HEADERS_LIST))

    print("\tRequest status: ", r.status_code)
    soup = BeautifulSoup(r.content, "html.parser")
    chapter_title_soup_list = soup.find_all("div", {"class": "elementor-element elementor-element-1ca7ec4 e-con-full e-flex e-con e-child"})

    if len(chapter_title_soup_list) == 0:
        return ["", ""]

    chapter_title = chapter_title_soup_list[0].text
    chapter_title = chapter_title.strip()

    print("\tChapter name: ", chapter_title)

    # Get the main content
    #chapter_text_soup_list = soup.find_all("main", {"id": "main-content"})
    chapter_text_soup_list = soup.find_all("article", {"class": "twi-article"})

    if len(chapter_text_soup_list) == 0:
        return [chapter_title, ""]

    chapter_text_soup = chapter_text_soup_list[0]
    chapter_text = chapter_text_soup.contents
    new_chapter_text = ""
    for i in chapter_text:
        if("href" not in str(i) and i != "\n"):
            new_chapter_text += str(i)

    return [chapter_title, new_chapter_text]


def generateChapterFile(chapter_name, content):

    relative_chapter_file = 'Text/'+ chapter_name.replace("/", "").replace(":", "").replace(".", "").replace("–", "-") +'.xhtml'
    chapter_file = template_directory+'/OEBPS/' + relative_chapter_file
    shutil.copy(template_directory+'/OEBPS/Text/example_chapter.xhtml', chapter_file)

    file_text = ""
    with open(chapter_file, 'r', encoding='utf8') as file:
        file_text = file.read()
    file_text = file_text.replace("chapter_name", chapter_name)
    file_text = file_text.replace("text_content", content)
    with open(chapter_file, 'w', encoding='utf8') as file:
        file.write(file_text)

    return relative_chapter_file


def addChapterToBook(chapter_file, chapter_number, chapter_name):

    # ------ Changing content.opf
    file_content = ""
    with open(template_directory+'/OEBPS/content.opf', 'r', encoding='utf8') as file:
        file_content = file.read()

    new_line = '<item href="' + chapter_file + '" id="chap' + str(chapter_number) + '" media-type="application/xhtml+xml"/>\n'
    file_content = file_content.replace("</manifest>", new_line + "</manifest>")

    new_line = '<itemref idref="chap' + str(chapter_number) + '"/>\n'
    file_content = file_content.replace("</spine>", new_line + "</spine>")

    with open(template_directory+'/OEBPS/content.opf', 'w', encoding='utf8') as file:
        file.write(file_content)

    # ------ Changing toc.ncx
    file_content = ""
    with open(template_directory+'/OEBPS/toc.ncx', 'r', encoding='utf8') as file:
        file_content = file.read()

    new_line = ('<navPoint id = "num_' + str(int(chapter_number) + 2) + '" playOrder = "' + str(int(chapter_number) + 2) + '"><navLabel><text>'+
                str(chapter_name) + '</text></navLabel><content src = "' + chapter_file + '"/></navPoint> \n')

    file_content = file_content.replace("</navMap>", new_line + "</navMap>")

    with open(template_directory+'/OEBPS/toc.ncx', 'w', encoding='utf8') as file:
        file.write(file_content)

    # ------ Changing toc.xhtml
    file_content = ""
    with open(template_directory+'/OEBPS/Text/toc.xhtml', 'r', encoding='utf8') as file:
        file_content = file.read()

    new_line = '<a href="../' + chapter_file.replace("/Text", "") + '">Chapter ' + chapter_name + '</a><br/>'

    file_content = file_content.replace("<p></p>", new_line + "<p></p>")

    with open(template_directory+'/OEBPS/Text/toc.xhtml', 'w', encoding='utf8') as file:
        file.write(file_content)










if __name__ == '__main__':

    # Duplicar carpeta plantilla
    # Poner título del libro y autor
    # Para cada capitulo
    #   Descargar texto
    #   Crear el archivo
    #   Añadir capitulo a la tabla de contenido y resto de archivos
    # Borrar capitulo de ejemplo
    # Comprimir a archivo zip
    # Cambiar el nombre a titulo.epub

    print("Starting book generation")

    final_file = "Output/" + book_title + ".epub"

    # Copy directory
    shutil.copytree("./Plantilla", template_directory, dirs_exist_ok=True)

    # Change the epub metadata
    sustituteNames(template_directory + '/OEBPS/Text/toc.xhtml', book_author, book_title)
    sustituteNames(template_directory + '/OEBPS/Text/title.xhtml', book_author, book_title)
    sustituteNames(template_directory + '/OEBPS/content.opf', book_author, book_title)
    sustituteNames(template_directory + '/OEBPS/toc.ncx', book_author, book_title)

    if os.path.exists(chapter_list_directory):

        chapter_number = 1
        with open(chapter_list_directory) as file:
            for link in file:
                print("-------------------- Chapter ", chapter_number, "--------------------")
                if(chapter_number != 1):
                    print("\tWait start")
                    # The https://wanderinginn.com/robots.txt ask to wait 10 seconds between requests
                    time.sleep(random.uniform(10, 11))
                    print("\tWait end")
                response = getChapter(link.replace("\n", ""))
                chapter_name = response[0]
                chapter_content = response[1]
                if(chapter_name == "" or chapter_content == ""):
                    print("\tError reading chapter: ", link.replace("\n", ""))

                chapter_file_name = generateChapterFile(chapter_name, chapter_content)

                addChapterToBook(chapter_file_name, chapter_number, str(chapter_name))

                chapter_number += 1

        print("-------------------- Download ended --------------------")

        if(cover_file != ""):
            print("Adding cover image")
            shutil.copy(cover_file, template_directory + "/OEBPS/Images/cover.jpg")
            print("\t...done")

        print("Generating epub file...")
        shutil.make_archive(template_directory, 'zip', template_directory)

        if(os.path.isfile(final_file)):
            os.remove(final_file)
        os.rename(template_directory+".zip", final_file)

        shutil.rmtree(template_directory)
        print("\t..done")

        print("Book genearion completed : " + final_file)

    else:
        print("Chapter list file not found")




