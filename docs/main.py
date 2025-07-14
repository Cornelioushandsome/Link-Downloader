import requests
import argparse
from pathlib import Path
import shutil
import os
import yt_dlp
from text import isValidFile

def downloadFile(url, outputFolder):
    try:
            
        response = requests.get(url)

        fileName = url.split("/")[-1]
        fileName = fileName.split("?")[0]

        path = Path(outputFolder) / fileName
        with open(path, "wb") as file:
            file.write(response.content)
        
        print(f"Successfully downloaded {fileName} into {path}")
        return
    except Exception as e:
        print(f"Failed to download {url}. {e}")    
        return

def downloadMedia(url, outputFolder):
    try:
            
        outputFolder = Path(outputFolder).absolute()
        outputFolder.mkdir(exist_ok=True, parents=True)

        options = {"outtmpl": str(outputFolder / "%(title)s.%(ext)s")}
        print(options["outtmpl"])
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])

        print(f"Downloaded to {outputFolder if outputFolder.exists else None}")
        return
    except Exception as e:
        print(f"Failed to download {url}. {e}")
        return
    
def readURLS(filePath):
    with open(filePath, "r") as file:
        urls = [line.strip() for line in file if line.strip()]
    return urls

#"C:\Users\jackr\OneDrive\Desktop\Huge political tiktoker just ruined his life.. [QOmCvf6sUNo].mp4"
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Enter a url to download a file")
    parser.add_argument("--media", action="store_true", help="Use this to download media")
    parser.add_argument("--out", default="web-downloads",help="Folder to save downloaded files")
    args = parser.parse_args()
    Path(args.out).mkdir(exist_ok=True)

    print(args.url)
    '''
    if args.media:
        downloadMedia(args.url, args.out)
    else:
        downloadFile(args.url, args.out)
    '''
if __name__ =="__main__":
    os.chdir(r"C:\Users\jackr\OneDrive\Desktop")
    main()