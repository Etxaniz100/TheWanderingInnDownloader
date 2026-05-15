from bs4 import BeautifulSoup
import requests
import random

TABLE_OF_CONTENTS_LINK = "https://wanderinginn.com/table-of-contents/"
starting_chapter = "9.00"
ending_chapter = "Volume 9 – Epilogue"


def getChapter(start_chapter, end_chapter):

    chapter_list = []

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

    r = requests.get(TABLE_OF_CONTENTS_LINK, headers=random.choice(HEADERS_LIST))

    print("\tRequest status: ", r.status_code)
    soup = BeautifulSoup(r.content, "html.parser")
    volumes_soup = soup.find_all("div", {"class": "volume-wrapper"})

    print("\tNumber of volumes found: ", len(volumes_soup))

    started = False
    if start_chapter == "":
        started = True
    ended = False

    volume_number = 1
    for volume in volumes_soup:

        chapters_soup = volume.find_all("a", href=True)

        print("\t\tNumber of chapter in volume ", volume_number, " : ", len(chapters_soup))


        for chapter in chapters_soup:
            link = chapter['href']
            chapter_name = chapter.text

            if(end_chapter != "" and (chapter_name == end_chapter or end_chapter in chapter_name)):
                chapter_list.append(link)
                ended = True
                break

            elif(started):
                chapter_list.append(link)

            elif(chapter_name == start_chapter or start_chapter in chapter_name):
                started = True
                chapter_list.append(link)

        if ended:
            break

        volume_number += 1

    return chapter_list



if __name__ == '__main__':

    print("Starting link find")

    chapter_list = getChapter(starting_chapter, ending_chapter)

    print("Number of chapters: ", len(chapter_list))

    file_content = ""

    for chapter in chapter_list:
        file_content += chapter + "\n"

    with open('./chapters', 'w', encoding='utf8') as file:
        file.write(file_content)



