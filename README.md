# AmeDoko
vTuber Members Stream Archiver

Description:

  AmeDoko is a script meant to easily archive the member only streams of a vTuber using Holodex lookup to find content.
  It archives the following from each memebers only stream:
   - Stream video
   - Comments
   - Live Chat
   - Any available subtitles including auto-generated ones
  Currently only works on Windows.


!!!WARNING!!!:

  !!!BAN RISK!!!:

    I am not responsibly for any ban or other retaliation from YouTube for use of this script.
    I have used it multiple times with no detrimental effects but that is no guarantee.
    Downloading video content is against terms of service and downloading large amounts of content is a risk.
    When possible it's recommended to use a burner account to download content and not your primary.
  
PreReqs:

    Have a membership on the YouTube channel you want to archive 
    Get Holodex API key https://docs.holodex.net/#section/Getting-Started/Obtaining-API-Key
    Download yt-dlp https://github.com/yt-dlp/yt-dlp/releases
    Download ffmpeg https://ffmpeg.org/download.html
    Download Python 3 https://www.python.org/downloads/
    Download HolodexClient from https://github.com/Brok3nHalo/HolodexClient as zip

Setup:

    Extract yt-dlp and ffmpeg to the same directory as AmeDoko.py the following files specifically are required:
    - yt-dlp.exe
    - ffmpeg.exe
    - ffprobe.exe

    Extract the Holodex folder from HolodexClient-Master.zip in the same directory as AmeDoko.py

    Install Python 3

    Open a terminal to the directory of AmeDoko.py

    Run the following command to install dependencies:
        pip install -r requirements.txt

    Set holodex_key in config.yaml to your holodex API key or put it in holodexKey.txt

Usage:

    In config.yaml set cookies_from_browser to your browser of choice and log into youtube it that browser
    Or extract youtube cookies from your browser of choice in Netscape format and paste them into cookies.txt or another file specified via command line

    Cookie Notes:
      When using a cookie file avoid opening youtube in the browser you extracted the cookie from, it can void your cookies during download and cause it to fail
      When using cookies_from_browser note that chrome is broken on Windows, if you try it it will print out an error wirth a URL with more information if you want to attempt to work around the issue
      I've only tested cookies_from_browser with FireFox, I don't know if the others besides that and chrome work or not

    Open a terminal in the folder containing AmeDoko and run:
        python AmeDoko.py

    Parameters:
        python AmeDoko.py [-h] [-k KEYFILE] [-c COOKIESFILE] [-p PATH]
    options:
        -h, --help                                  Show this help message and exit
        -k KEYFILE, --keyFile KEYFILE               File containing Holodex API key, defualt holodexkey.txt, overrides key in config.yaml
        -c COOKIESFILE, --cookiesFile COOKIESFILE   File containing YouTube cookies, overrides settings in config.yaml
        -p PATH, --path PATH                        Path to where files should be saved, default current directory

TODO:
 - Improved UI
 - Download options
  - Other Topics
  - Videos in Time Span
  - Video count
  - Provide customization of video downloads
   - Toggle to download comments/generated subtitles/live chats etc
   - Additional options
 - Video search paging
 - Video download selection
 - Better issue handling
 - Real Logging
 - Fix Holodex python SDK to not require topic patch
 - Multiplatform support
