# The Wandering Inn Downloader

![The Wandering Inn cover](BookCover.jpg "BookCover")

[The Wandering Inn](https://wanderinginn.com/) is a fantasy web novel which can be read online for free on the official website. The problem is I prefer to read in my e-book instead of reading on my phone or computer. 

This is where this downloader comes to play. 

This python script is divided in two parts, a chapter finder and a chapter downloader. Given a two chapter name, the chapter finder finds the links to these two and all the chapters in between and puts them on a list. 
The chapter downloader takes the list, downloads each chapter and creates an EPUB file with them.  

An epub file is simply a ZIP file with another extension, so instead of using some EPUB creating library, the script uses a EPUB template and modifies it with the appropriate data. It may not be the prettiest result, but it is functional.

To download the data a http request is made, and then it is analyzed using Beautiful Soup. As there are a lot of chapters per volume, this downloader can take a while to download a full "book". This is because between chapters, a 10 second wait is made. This is to respect the robots.txt file. 
