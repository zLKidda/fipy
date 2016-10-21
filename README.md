# Fipy
python local and remote file inclusion scanner for testing web servers 

![Alt text](https://i.gyazo.com/82c107594ad8af82b56366bfaad5cb36.png )

# Prerequisites
--------------------------------------------
sudo pip install termcolor requests BeautifulSoup lxml
Linux

# Demo 
---------------------------------------------
https://www.youtube.com/watch?v=zci-Q76NivU subscribe :)

# Running
---------------------------------------------
python fipy.py -u http://www.somesite.com?page=
python fipy.py -d 

# Usage 
---------------------------------------------
Usage: fipy.py [options]

Options:
  -h, --help            show this help message and exit
  -u http://www.somesite.com/index.php?page=, --url=http://www.somesite.com/index.php?page=
                        URL of target
  -c, --crawl           Crawl website enabled
  -d, --dork            provide a google dork
