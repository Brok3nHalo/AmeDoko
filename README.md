# AmeDoko
vTuber Members Stream Archiver

## Description
AmeDoko is a script meant to easily archive the member only streams of a vTuber using Holodex lookup to find content.
It archives the following from each members only stream:
 - Stream video
 - Comments
 - Live Chat
 - Any available subtitles including auto-generated ones
   - By default English is downloaded but languages can be set in the config

It saves progress as it goes along and lets you resume on the next run.

Currently only works on Windows.


## !!!WARNING BAN RISK!!!
I am not responsibly for any ban or other retaliation from YouTube for use of this script.
I have used it multiple times with no detrimental effects but that is no guarantee.
Downloading video content is against terms of service and downloading large amounts of content is a risk.
When possible it's recommended to use a burner account to download content and not your primary.
  
## PreReqs
- Have a membership on the YouTube channel you want to archive
- Get Holodex API key https://docs.holodex.net/#section/Getting-Started/Obtaining-API-Key
- Download Python 3 https://www.python.org/downloads/
- Download AmeDoko https://github.com/Brok3nHalo/AmeDoko/releases
- Download yt-dlp https://github.com/yt-dlp/yt-dlp/releases
- Download ffmpeg https://ffmpeg.org/download.html

## Setup
1. Install Python 3
2. Extract the AmeDoko.zip contents to folder of choice
3. Extract yt-dlp and ffmpeg to the same directory as AmeDoko.py, the following files specifically are required:
   - yt-dlp.exe
   - ffmpeg.exe
   - ffprobe.exe
4. Set holodex_key in config.yaml to your holodex API key or put it in holodexKey.txt
5. . Run Amedoko.py and follow the prompts to complete automatic setup:
```
python AmeDoko.py
```

## Manual Setup
If automatic setup fails when running AmeDoko.py you can do the following to complete the setup manually before running:
- Download the holodex library from https://github.com/Brok3nHalo/HolodexClient as zip
  -  Extract the holodex folder from HolodexClient-Master.zip in the same directory as AmeDoko.py
-  Open a terminal to the directory of AmeDoko.py
   -  Run the following command to install remaining dependencies:
     ```
     pip install -r requirements.txt
     ```
## Usage

In config.yaml set cookies_from_browser to your browser of choice and log into youtube it that browser
OR extract youtube cookies from your browser of choice in Netscape format and paste them into cookies.txt or another file specified via command line

Cookie Notes:
- When using a cookie file avoid opening youtube in the browser you extracted the cookie from, it can void your cookies during download and cause it to fail
- When using cookies_from_browser note that Chrome is broken on Windows, if you try it it will print out an error wirth a URL with more information if you want to attempt to work around the issue
- I've only tested cookies_from_browser with FireFox, I don't know if the others besides that and chrome work or not

Open a terminal in the folder containing AmeDoko and run:
```
python AmeDoko.py
```

### Parameters
    python AmeDoko.py [-h] [-k KEYFILE] [-c COOKIESFILE] [-p PATH]
### Options:
    -h, --help                                  Show this help message and exit
    -k KEYFILE, --keyFile KEYFILE               File containing Holodex API key, default holodexkey.txt, overrides key in config.yaml
    -c COOKIESFILE, --cookiesFile COOKIESFILE   File containing YouTube cookies, overrides settings in config.yaml
    -p PATH, --path PATH                        Path to where files should be saved, default current directory

### Interface
On initial launch you'll be prompted to search for the channel to archive:
![1 Search](https://github.com/user-attachments/assets/b93e428f-0a57-46e6-bac3-f452aef1a451)

If multiple matches are found you can select the one you want:
![2 Search Results](https://github.com/user-attachments/assets/ef2def14-eec5-4277-b8d1-71f748d8bdc6)

On future launches previous searches will be saved and you can select which one to continue or N for a new search:
![3 Selection](https://github.com/user-attachments/assets/4f307f53-20ce-42ca-a101-353c4ba64dcf)

A list of available and missing videos will be shown so you can verify it's the correct channel:
![4 Video List](https://github.com/user-attachments/assets/946ce8df-6614-464f-b31d-6fb9327de516)

Missing videos are no longer available to stream and can't be downloaded.

You can then choose to continue or press U to update the list if there have been new videos since the last use:
![5 Continue or Update](https://github.com/user-attachments/assets/f300b6a2-5ffc-4f8a-ae38-0bad498b2de6)

As it downloads it will keep you updated on progress:
![6 Downloading](https://github.com/user-attachments/assets/ad5ee66f-e9ca-4850-a453-5c9065725257)

It saves the current state after each download so it can be resumed later:
![7 Finished Download](https://github.com/user-attachments/assets/15ddad72-cc4b-417b-b8f1-2b197f1cf168)

When continuing a previous download the video list will mark completed downloads with a X and errors with a !:
![8 Finished and Error](https://github.com/user-attachments/assets/73260eb1-53aa-4944-8969-9e58586f6b60)

If the last session had any errors, you will be asked if you'd like to retry the videos with issues:
![9 Retry](https://github.com/user-attachments/assets/416bb36c-8f70-4d3a-935d-ed17e090e467)

If you need to exit early while downloading hit the spac bar, you will be prompted to exit safely

Currently there is no way to redownload successfully downloaded videos, currently the solution to this is to delete AmdeDoko.state and --continue files from the AmeDoko folder. Note this will lose track of all your current sessions and be a fresh start so you may want to back them up and restore them after you are done redownloading.


## TODO
 - Improved UI
 - Redownloading support
 - Better failure handling
 - Download options
   - Other Topics
   - Videos in time span
   - Video count
   - Toggle to download comments/generated subtitles/live chats etc
   - Additional options
 - Video search paging
 - Video download selection
 - Better issue handling
 - Real Logging
 - Multiplatform support
