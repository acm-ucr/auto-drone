import os

def generate_negative_description_file():
    with open('neg.txt', 'w') as f:
        for filename in os.listdir('n'):
            f.write('n/' + filename + '\n')