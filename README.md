#Scrapy Template
Quickly deploy a spider.

Just change the settings + spider file and you'r good to go.


##Helpfull comands:

Run Crawler:
scrapy crawl spider -L INFO -s JOBDIR=crawls/run_01

Export to csv/json:
scrapy crawl spider -o data.csv

Using Screen:
screen -r = Returns to last session
ctrl + a and then press d to leave session
