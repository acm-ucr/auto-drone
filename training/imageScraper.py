import os
import datetime
from icrawler.builtin import GoogleImageCrawler

# Crawling for positive images
# print("Crawling for positives")
# positive_crawler = GoogleImageCrawler(parser_threads = 2, downloader_threads = 4, storage = {'root_dir': r'p'})
# positive_crawler.session.verify = False
# with open('pinputs.txt') as pinputs_file:
#     for line in pinputs_file:
#         positive_crawler.crawl(keyword=line, max_num=1000,
#                      min_size=(10,10), max_size=None)
        
print("Crawling for negatives")
# Crawling for negative images
negative_crawler = GoogleImageCrawler(parser_threads = 2, downloader_threads = 4, storage = {'root_dir': r'training/n'})
year = 2010
negative_crawler.session.verify = False
with open("training/inputsneg.txt") as ninputs_file:
    for line in ninputs_file:
        while year < 2024:
            negative_crawler.crawl(
                keyword=line,
                filters={'date': ((year, 1, 1), (year, 12, 31))},
                max_num=1000,
                file_idx_offset='auto')
            year+=1



# Loops to count
print("Counting Files")
pcount = 0
ncount = 0

pdirectory = os.fsencode("training/p")    
for file in os.listdir(pdirectory):
    pcount+=1

ndirectory = os.fsencode("training/n")    
for file in os.listdir(ndirectory):
    ncount+=1
    
print(f"Positives: {pcount}")
print(f"Negatives: {ncount}")

