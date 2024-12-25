import os
import datetime
from icrawler.builtin import GoogleImageCrawler

# Crawling for positive images
print("Crawling for positives")
positive_crawler = GoogleImageCrawler(parser_threads = 2, downloader_threads = 4, storage = {'root_dir': r'p'})
positive_crawler.session.verify = False
with open('pinputs.txt') as pinputs_file:
    for line in pinputs_file:
        positive_crawler.crawl(keyword=line, max_num=1000,
                     min_size=(10,10), max_size=None)
        
print("Crawling for negatives")
# Crawling for negative images
negative_crawler = GoogleImageCrawler(parser_threads = 2, downloader_threads = 4, storage = {'root_dir': r'n'})

negative_crawler.session.verify = False
with open('ninputs.txt') as ninputs_file:
    for line in ninputs_file:
        negative_crawler.crawl(keyword=line, max_num=1000,
                     min_size=(10,10), max_size=None)


# Loops to count
print("Counting Files")
pcount = 0
ncount = 0

pdirectory = os.fsencode("p")    
for file in os.listdir(pdirectory):
    pcount+=1

ndirectory = os.fsencode("n")    
for file in os.listdir(ndirectory):
    ncount+=1
    
print("Positives: " + pcount)  
print("Negatives:" + ncount)

