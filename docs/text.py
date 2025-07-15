import argparse
import requests

TEXT_PATH = r"C:\Users\jackr\OneDrive\Desktop\C_Files\python\downloadQueue.txt"
MAX_SIZE = 100


def isValidFile(url, allowedTypes=None, maxSize = 100):
    #Change this so that it prompts user to confirm
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)

        if response.status_code != 200:
            return False
        
        #check type
        content_type = response.headers.get('Content-Type', '').lower()
        if allowedTypes and not any(t in content_type for t in allowedTypes):
            print(f"Content-Type '{content_type}' not allowed.")
            return False
        
        #check length
        content_length = response.headers.get('Content-Length')
        if content_length:
            size_mb = int(content_length) / (1024 * 1024)
            if size_mb > maxSize:
                prompt = input(f"Size of file is {size_mb} mb. Would you still like to download? [y/n]: ").lower()
                if prompt == "y":
                    return True
                else:
                    return False

        return True
    except Exception as e:
        print(f"Failed to check {url}. {e}")
        return
    

def main():
    
    ALLOWED_TYPES = [
        "video/",                # mp4, webm, mkv, etc.
        "audio/",                # mp3, wav, etc.
        "image/",
        "application/pdf",       # PDF files
        "text/plain",            # .txt files
        "text/markdown",         # .md files
        "text/x-python",         # .py
        "text/x-c++src",         # .cpp
        "text/x-csrc",           # .c
        "application/javascript",# .js
        "text/css",              # .css
        "text/html",             # .html
        "application/json",      # .json
    ]

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--add",default=None, nargs="*", help=f"Add a url to {TEXT_PATH}")
    parser.add_argument("-r", "--remove",default=None, nargs= "*", help = f"Delete a url from {TEXT_PATH}")
    args = parser.parse_args()

    if args.add:
        try:
            with open(TEXT_PATH, "a") as f:
                for i in args.add:
                    if isValidFile(url=i, allowedTypes=ALLOWED_TYPES, maxSize=MAX_SIZE):
                        f.write(i + "\n")
                        print(f"Successfully added file: {i.split("/")[-1]}")
                    else:
                        print("Invalid file. Moving on\n")
                        continue
        except FileNotFoundError:
            print("File not found.")
            return
    if args.remove:
        try:
            with open(TEXT_PATH, "r") as f:
                lines = [line.strip() for line in f.readlines()]

            updatedLines = [line.strip() for line in lines if line not in args.remove]

            with open(TEXT_PATH, "w") as f:
                for line in updatedLines:
                    f.write(line + "\n")
            print(f"Removed valid lines in {args.remove}")
        except FileNotFoundError:
            print("File not found")
            return
        
if __name__ == "__main__":
    main()

