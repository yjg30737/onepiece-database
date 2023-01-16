# onepiece-database
Get the One Piece characters info with one click from <a href="https://onepiece.fandom.com/wiki/One_Piece_Wiki">ONE PIECE WIKI(FANDOM)</a>

Using scrapy to crawl the WIKI page data

This is the GUI version of <a href="https://github.com/yjg30737/one-piece-character-data-scraper">one-piece-character-data-scraper</a>, this uses it as a submodule.

You can see what kind of info this get in the link above. Such as character name, height..

## Requirements
* PyQt5 (for GUI)
* pandas (for converting)
* Scrapy (for getting the data from the site)

## How to Install
1. git clone ~
2. pip install -r requirements.txt
3. go into the onepiece_database directory
4. python main.py (py main.py if you use Python 3.11)

## Preview

First screen, press the "get characters info" button

![image](https://user-images.githubusercontent.com/55078043/212575373-6ea962d1-af92-42ae-a4a8-6326d505c9cf.png)

New dialog will show up to process the getting characters' info from the pages, wait till it finished

![image](https://user-images.githubusercontent.com/55078043/212575322-ebbc6de3-29a7-483d-bf6f-e9d848d4ff79.png)

Result

![image](https://user-images.githubusercontent.com/55078043/212575088-d7c441fc-5cbb-4af5-9e4e-a3ef0eb30e45.png) 
