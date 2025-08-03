import random

def random_ascii_art():
    shapes = ['*', '#', '@', '%', '&', '+']
    for i in range(10):
        line = ''.join(random.choice(shapes) for _ in range(30))
        print(line)

if __name__ == '__main__':
    print("Check out this random ASCII art!")
    random_ascii_art()
