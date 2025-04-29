from io import BytesIO
import pickle
from pathlib import Path
from subprocess import Popen, PIPE
import sys
import argparse
import re
import importlib
from urllib.request import urlopen
from zipfile import ZipFile
from os import path, makedirs
from shutil import copyfileobj


dependencies = False
while not dependencies:
    try:
        import asyncio
        import yaml
        import keyboard
        
        if not (importlib.util.find_spec("aiohttp") and importlib.util.find_spec("typing_extensions")):
            raise ImportError()
    except ImportError:
        print("Dependencies not found! Install dependencies?")
        match(input("Y/N: ")):
            case "Y" | "y":
                try:
                    pip = Popen("pip install -r requirements.txt", stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
                except:
                    print("Install failed try instealling dependencies manually, see README for details")
                
                while(pip.poll() == None):
                    # Echo output to console
                    for c in iter(lambda: pip.stdout.read(1), b""):
                        sys.stdout.buffer.write(c)
                    for c in iter(lambda: pip.stderr.read(1), b""):
                        sys.stderr.buffer.write(c)

                print("\nDependencies installed!\n")
            case "N" | "n":
                print("Dependencies required to continue, exiting...")
                exit()
        continue
    
    try:
        from holodex.client import HolodexClient
    except ImportError:
        print("Holodex library not found, download it?")

        match(input("Y/N: ")):
            case "Y" | "y":
                print("Downloading library...")
                try:
                    script_path = Path(path.realpath(__file__)).parent
                    response = urlopen("https://github.com/Brok3nHalo/HolodexClient/archive/refs/heads/master.zip")
                    data = response.read()
                    with ZipFile(BytesIO(data)) as archive:
                        for item_name in archive.namelist():
                            if item_name.startswith("HolodexClient-master/holodex/") and not item_name.endswith("/"):
                                item_path = script_path/item_name.removeprefix("HolodexClient-master/")
                                item = archive.open(item_name)
                                if not path.exists(item_path.parent):
                                    makedirs(item_path.parent)
                                with open(item_path, "wb") as file:
                                    copyfileobj(item, file)
                except Exception as e:
                    print(f"Issue downloading holodex library, maybe try getting it manually? See README for details\n{e}")
                    exit()
                print("Holodex library downloaded!")
            case "N" | "n":
                print("Holodex Client required to continue, exiting...")
                exit()

        continue

    
    dependencies = True


STATE_LOADABLE = [0]
STATE_VERSION = 0
STATE_NAME = "AmeDoko.state"

async def main(holodex_key_file = None, cookies_file = None, path = None):
    config = None
    try:
        with open("config.yaml") as config_yaml:
            config = yaml.safe_load(config_yaml)
    except Exception as error:
        print(f"Failed to load config.yaml with error:\n{error}")


    session = loadSession() or {
        "channel_name": None,
        "channel_id": None,
        "output_path": None,
        "missing": [],
        "available": [],
        "completed": [],
        "issue": [],
        "loaded": False
    }

    missing = session["missing"]
    available = session["available"]
    completed = session["completed"]
    issue = session["issue"]
    loaded = session["loaded"]

    channel_name = session["channel_name"]
    channel_id = session["channel_id"]
    output_path = session["output_path"]
    
    approved = False
    update = False
    while not approved:
        if not loaded or update:
            holodex_key = loadHolodexKey(holodex_key_file, config)

            async with HolodexClient(key = holodex_key) as client:
                if not channel_id:
                    channel = None
                    while not channel:
                        name = input("Search channel, leave blank to exit: ")
                        if not name:
                            exit()

                        print("Finding Channel...")
                        search = await client.autocomplete(name)

                        channels = search.contents
                        if len(channels) > 1:
                            print("Multiple matches, select desired channel or X to exit:")
                            for i, option in enumerate(channels):
                                print(f"  {i}: {option.text}")
                            selection = -1
                            while not 0 <= selection < len(channels):
                                choice = input("Selection: ")
                                if choice in ("X", "x"):
                                    exit()
                                elif choice in ("N", "n"):
                                    break
                                else:
                                    try:
                                        selection = int(choice)
                                        if not 0 <= selection < len(channels):
                                            raise
                                        
                                        channel = channels[selection]
                                    except:
                                        print("Invalid selection, try again")
                        elif len(channels) == 1:
                            print(f"Is {channels[0].text} the correct channel?")
                            while True:
                                    match input("Y/N: "):
                                        case "Y" | "y":
                                            channel = channels[0]
                                            break
                                        case "N" | "n":
                                            break
                        else:
                            print("No channels found")
                            continue

                    channel_name = channel.text
                    channel_id = channel.value

                print(f"Channel Name: {channel_name}")
                print(f"Channel ID: {channel_id}")

                print("Retreiveing video data...")
                video_request_limit = config["video_request_limit"] if "video_request_limit" in config and config["video_request_limit"] is int else 100
                videos = await client.videos_from_channel(channel_id, "videos", topic = ["membersonly"], limit = video_request_limit)

                print(f"Retrieved {len(videos.contents)} videos, processing...")
                for video in videos.contents:
                    if video.status == "missing":
                        if not any(video.id == v.id for v in missing):
                            missing.append(video)
                    elif not any(video.id == v.id for v in available):
                        available.append(video)

                print("Completed...")

                if not output_path:
                    if not path and "path" in config: path = config["path"]
                    output_path = (Path(path) if path else Path())/channel_name.translate(str.maketrans("","","<>:/\\|?*\n"))

                session["channel_name"] = channel_name
                session["channel_id"] = channel_id
                session["output_path"] = output_path
                session["loaded"] = True
                saveSession(session)

        print(f"\n{len(available)} Available:")
        for video in available:
            print(("X " if video in completed else "! " if video in issue else "  ") + video.id + "\t" + video.title)

        print(f"\n{len(missing)} Missing:")
        for video in missing:
            print(f"  {video.title}")
            
        while True:
            print("Begin Archiving? Or U to update video list")
            match input("\n Y/N/U: "):
                case "U" | "u":
                    update = True
                    break
                case "Y" | "y":
                    approved = True
                    break
                case "N" | "n":
                    exit()

    if issue:
        while True:
            match input("\nRetry failed downloads? Y/N: "):
                case "Y" | "y":
                    issue.clear()
                    break
                case "N" | "n":
                    break
    
    downloads = [video for video in available if not video in completed and not video in issue]
    if len(downloads) > 0: print("\nDownloading videos...")
    for i, video in enumerate(downloads, start = 1):
        yt_url = f"https://youtu.be/{video.id}"
        
        print(f"{i}/{len(downloads)}\t{video.id}\t{video.title}")

        ytdlp = None
        sub_lang = ",".join(re.split(r"[^a-zA-Z0-9-]+", config["sub_lang"])) if "sub_lang" in config and config["sub_lang"] else "en"
        cookies_file = cookies_file if cookies_file else config["cookies_file"] if "cookies_file" in config and config["cookies_file"] else None
        cookie_source = config["cookies_from_browser"] if "cookies_from_browser" in config and config["cookies_from_browser"] else None

        cmd = (".\\yt-dlp.exe --embed-thumbnail --embed-metadata --write-auto-subs --write-sub --embed-sub --write-comments --download-archive --continue --embed-chapters --merge-output-format mp4 "
        + (f"--sub-lang {sub_lang},live_chat ")
        + (f"--cookies {cookies_file} " if cookies_file else f"--cookies-from-browse {cookie_source} " if cookie_source else "")
        + (f"--paths \"{output_path}\" " if output_path else "")
        + yt_url)

        try:
            ytdlp = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
        except:
            print("Failed to execute yt-dlp.exe, exiting")
            exit()

        while(ytdlp.poll() == None):
            # Echo yt-dlp output to console
            for c in iter(lambda: ytdlp.stdout.read(1), b""):
                sys.stdout.buffer.write(c)
                if keyboard.is_pressed(" "):
                    match input("\nX to exit, anything else to continue: ").strip():
                        case "X" | "x":
                            exit()
            for c in iter(lambda: ytdlp.stderr.read(1), b""):
                sys.stderr.buffer.write(c)

        if ytdlp.returncode == 0:
            print("Video download completed successfully!")
            completed.append(video)
        else:
            print(f"Video download ended with issue! (Code {ytdlp.returncode})")
            issue.append(video)

        saveSession(session)

    print("Archival completed")

def loadHolodexKey(holodex_key_file, config):
    holodex_key = None

    try:
        with open(holodex_key_file or "holodexKey.txt", "r") as key_file:
            holodex_key = key_file.readline()
    except: pass
    
    if not holodex_key:
        try : holodex_key = config["holodex_key"]
        except: 
            print("Failed to read holodex key from config.yaml")
            exit()

    if not holodex_key:
        print("Please place Holodex API key in config.yaml, holodexkey.txt, or provide a custom file")
        exit()
    return holodex_key

def loadSession():

    state = loadState()

    if not state:
        return None

    print("Active Sessions:")
    sessions = [state["sessions"][id] for id in state["sessions"]]
    for i, session in enumerate(sessions):
        print(f"{i}: {session["channel_name"]}")

    print("Input number of selection to continue, N for new search, X to exit")

    selection = -1
    while not 0 <= selection < len(sessions):
            choice = input("Selection: ")
            if choice in ("X", "x"):
                exit()
            elif choice in ("N", "n"):
                return None
            else:
                try:
                    selection = int(choice)
                    if 0 <= selection < len(sessions):
                        return sessions[selection]
                    raise
                except:
                    print("Invalid selection, try again")
    
def loadState():
    state = None

    try: 
        print("Loading state...")
        with open(STATE_NAME, "rb") as f:
            state = pickle.load(f)
    except:
        print("No state loaded...")
        return None
    
    print("Loaded state!")
    version = state["version"] if "version" in state else None
    if version not in STATE_LOADABLE:
        print(f"State verion {version} not compatible with current version {STATE_VERSION}")
        return None
    
    return state

def saveSession(session):
    print("\nSaving state...")
    
    state = loadState() or {
        "version": STATE_VERSION,
        "sessions": {}
    }

    state["version"] = STATE_VERSION
    state["sessions"][session["channel_id"]] = session

    
    print("\nWriting state...")
    try:
        with open(STATE_NAME, "wb") as f:
            pickle.dump(state, f, pickle.HIGHEST_PROTOCOL)
            print("State saved!\n")
    except:
        print("Save failed, exiting!")
        exit()

parser = argparse.ArgumentParser()
parser.add_argument("-k", "--keyFile", help="File containing Holodex API key, default holodexkey.txt, overrides key in config.yaml")
parser.add_argument("-c", "--cookiesFile", help="File containing YouTube cookies, overrides settings in config.yaml")
parser.add_argument("-p", "--path", help="Path to where files should be saved, default current directory")

args = parser.parse_args()

asyncio.run(main(
    holodex_key_file = args.keyFile,
    cookies_file = args.cookiesFile,
    path = args.path
))
