import requests
import argparse
from pathlib import Path
#import shutil
import os
import yt_dlp
#from text import isValidFile
from validSites import VALID_YT_DLP_SITES

#GLOBAL VARS
URL_FILE = r"downloadQueue.txt" #ENTER THE FILE TO STORE THE URLS HERE
DEFAULT_OUTPUT_FOLDER = r"web-downloads" #ENTER THE OUTPUT FOLDER OF THE DOWNLOADS
#os.chdir(r"") OPTIONAL: MOVE DIRECTORY TO DESKTOP
PATH = os.getcwd()

def getFileType(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)
        contentType = response.headers.get("Content-Type", "").lower()
        if "video" in contentType or "audio" in contentType or any(site in url.lower() for site in VALID_YT_DLP_SITES):
            return "media"
        elif any(x in contentType for x in [
            "application", "text", "image"
        ]):
            return "file"
        else:
            return "unknown"
    except Exception as e:
        print(f"Error determining file type of {url}. {e}")
        return "unknown"

def downloadFile(url, outputFolder):
    try:
            
        response = requests.get(url)

        fileName = url.split("/")[-1]
        fileName = fileName.split("?")[0]

        path = Path(outputFolder) / fileName
        with open(path, "wb") as f:
            f.write(response.content)
        
        print(f"Successfully downloaded {fileName} into {path}")
        return
    except Exception as e:
        print(f"Failed to download {url}. {e}")    
        return

def downloadMedia(url, outputFolder):
    try:
            
        outputFolder = Path(outputFolder).absolute()
        outputFolder.mkdir(exist_ok=True, parents=True)

        options = {"outtmpl": str(outputFolder / "%(title)s.%(ext)s"),
                   "verbose": False,
                   "restrictfilenames":True,
                   "noplaylist": True,
                   "format": "best",
                   "quiet": False,
                   "format": "bestvideo[height>=720]+bestaudio[abr>=128]/best[height>=720]/best",
                   "postprocessors": [
                       {
                            "key": "FFmpegVideoConvertor",
                            "preferedformat": "mp4",  # Force final format to mp4
                       }
                   ],
                }
        print(options["outtmpl"])
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])

        print(f"Downloaded to {outputFolder if outputFolder.exists else None}")
        return
    except Exception as e:
        print(f"Failed to download {url}. {e}")
        return
    
def readURLS(filePath):
    with open(filePath, "r") as f:
        urls = [line.strip() for line in f if line.strip()]
    return urls

def downloadType(url, outputFolder):
    try:
        temp_type = getFileType(url)
        match(temp_type):
            case "media":
                downloadMedia(url, outputFolder)
            case "file":
                downloadFile(url, outputFolder)
            case "unknown":
                print(f"Unknown or Invalid file type: {url}")
    except Exception as e:
        print(f"Failed to download {url}. {e}")
        return

#"C:\Users\jackr\OneDrive\Desktop\Huge political tiktoker just ruined his life.. [QOmCvf6sUNo].mp4"
def main():
    #Change this so that it gets urls from downloadQueue.txt
    parser = argparse.ArgumentParser()
    parser.add_argument("url", nargs="?", help="Enter a URL to download from")
    parser.add_argument("-b", "--batch", action="store_true", help=f"Download all URLs from {URL_FILE}")
    parser.add_argument("--out", default = DEFAULT_OUTPUT_FOLDER, help="File to store all downloads")
    parser.add_argument("-c", "--clear", action="store_true", help="Choose whether to delete queue after downloading")
    args = parser.parse_args()
    
    Path(args.out).mkdir(exist_ok=True)

    if args.url:
        downloadType(args.url, args.out)
    if args.batch:
        URLS = readURLS(URL_FILE)
        for link in URLS:
            downloadType(link, args.out)
        if args.clear:
            with open(URL_FILE, "w") as f:
                f.write("")

if __name__ =="__main__":
    main()
