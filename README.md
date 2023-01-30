# onepiece-database
Get the One Piece characters info with one click from <a href="https://onepiece.fandom.com/wiki/One_Piece_Wiki">ONE PIECE WIKI(FANDOM)</a>

Using scrapy to crawl the WIKI page data

This is the PyQt GUI version of <a href="https://github.com/yjg30737/one-piece-character-data-scraper">one-piece-character-data-scraper</a>, this uses it as a submodule.

You can see what kind of info this get in the link above. Such as character name, height..

Also you are able to sort the data as well.

## Requirements
* PyQt5 (for GUI)
* pandas (for converting)
* Scrapy (for getting the data from the site)
* psutil (for getting the process id to show the log)

## How to Install
1. git clone ~
2. python -m pip install -r requirements.txt
3. go into the onepiece_database directory
4. python main.py

## Preview

First screen, press the "get characters info" button

![image](https://user-images.githubusercontent.com/55078043/215363743-abe7c0d9-bc8b-4e38-ad4b-95fe74e8a3b5.png)

New dialog will show up to process the getting characters' info from the pages, wait till it finished

![image](https://user-images.githubusercontent.com/55078043/212575322-ebbc6de3-29a7-483d-bf6f-e9d848d4ff79.png)

You can pause/resume or stop the process. If you press stop button, dialog will be closed.

Result

![image](https://user-images.githubusercontent.com/55078043/215363929-a196d41a-d0fa-45d2-ac9b-69881c0bc7fd.png)

TODO list
* hyperlink
* crawling in background
* colorful logging
* find/save the log message
