import os
from icrawler.builtin import BingImageCrawler
from PIL import Image

# Crawling for positive images
print("Crawling for positives")
positive_crawler = BingImageCrawler(parser_threads = 2, downloader_threads = 4, storage = {'root_dir': r'training/p'})
positive_crawler.session.verify = False
with open("training/inputspos.txt") as pinputs_file:
    for line in pinputs_file:
        positive_crawler.crawl(
            keyword = line,
            max_num = 500,
            file_idx_offset = 'auto')
        
# print("Crawling for negatives")
# # Crawling for negative images
# negative_crawler = BingImageCrawler(parser_threads = 2, downloader_threads = 4, storage = {'root_dir': r'training/n'})
# negative_crawler.session.verify = False
# with open("training/inputsneg.txt") as ninputs_file:
#     for line in ninputs_file:
#         negative_crawler.crawl(
#             keyword = line,
#             max_num = 1000,
#             file_idx_offset = 'auto')

# Resize negative images

with open ("training/n") as negFiles:
    for img in negFiles:
        image = Image.open(img)
        image = image.resize(640, 480)
        image.save(img)
        print("image resized")


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

