import argparse
import colorama
import requests
import justlog
import json
import os
from os.path import exists
import sys
from . import shared as shared
from .helpers import greet, get_torrent_by_id, fetch_torrent_url
from tabulate import tabulate
from .torrent import torrent, filter_out, transmission, deluge, qbittorrent, local, nzbget
from justlog import justlog, settings
from justlog.classes import Severity, Output, Format
from .config import load_config
from pathlib import Path
from urllib3.exceptions import InsecureRequestWarning
import urllib.parse
import pprint
import re
import operator
from shutil import which
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("search", help="What to search for.", nargs='?')
parser.add_argument("--indexer_manager", help="prowlarr/jackett")
parser.add_argument("--prowlarr_key", help="The Prowlarr API key.")
parser.add_argument("--jackett_key", help="The Jackett API key.")
parser.add_argument("--list", help="Path to a file of terms to search.", type=str)
parser.add_argument("-l", "--length", help="Max results description length.", type=int)
parser.add_argument("-L", "--limit", help="Max number of results.", type=int)
parser.add_argument("-c", "--config", help="Specify a different config file path.")
parser.add_argument("-s", "--sort", help="Change sorting criteria. Any combination of 'cn','protocol', 'seeders', 'leechers', 'ratio', 'size', 'description'", dest="sort")
parser.add_argument("--prowlarr_indexer", help="The Prowlarr indexer to use for your search.")
parser.add_argument("--jackett_indexer", help="The Jackett indexer to use for your search.")
parser.add_argument("-d", "--download", help="Download and send the top 'x' results (defaults to 1) to the client and exit.", nargs='?', const=1, type=int)
parser.add_argument("-K", "--insecure", help="Enables to use self-signed certificates.", action="store_true")
parser.add_argument("--local", help="Override torrent provider with local download.", action="store_true")
parser.add_argument("--verbose", help="Very verbose output to logs.", action="store_true")
args = parser.parse_args()

shared.init()

# Use default path for the config file and load it initially
cfg_path = f"{str(Path.home())}/.config/{shared.APP_NAME}.json"
if not exists(cfg_path):
    cfg_path = f"{os.path.dirname(os.path.realpath(__file__))}/{shared.APP_NAME}.json"
if args.config is not None:
    cfg_path = args.config
cfg = load_config(cfg_path)

shared.TORRENTS = []
shared.JACKETT_APIKEY = cfg['jackett_apikey']
shared.JACKETT_URL = cfg['jackett_url']
shared.JACKETT_INDEXER = cfg['jackett_indexer']
shared.DESC_LENGTH = cfg['description_length']
shared.EXCLUDE = cfg['exclude']
shared.RESULTS_LIMIT = cfg['results_limit']
shared.CLIENT_URL = cfg['client_url']
shared.DISPLAY = cfg['display']
shared.TOR_CLIENT = cfg['torrent_client']
shared.TOR_CLIENT_USER = cfg['torrent_client_username']
shared.TOR_CLIENT_PW = cfg['torrent_client_password']
shared.DOWNLOAD_DIR = cfg['download_dir']
shared.CURRENT_PAGE = 0


shared.INDEXER_MANAGER = cfg['indexer_manager']
shared.SORT = cfg['sort']
shared.PROWLARR_APIKEY = cfg['prowlarr_apikey']
shared.PROWLARR_URL = cfg['prowlarr_url']
shared.PROWLARR_INDEXER = cfg['prowlarr_indexer']
shared.NZBGET_URL = cfg['nzbget_url']
shared.NZBGET_USER = cfg['nzbget_username']
shared.NZBGET_PW = cfg['nzbget_password']
shared.NZBGET_PORT = cfg['nzbget_port']



# Setup logger
logger = justlog.Logger(settings.Settings())
logger.settings.colorized_logs = True
logger.settings.log_output = [Output.FILE]
logger.settings.log_format = Format.TEXT
logger.settings.log_file = f"{str(Path.home())}/.config/{shared.APP_NAME}.log"
logger.settings.update_field("timestamp", "$TIMESTAMP")
logger.settings.update_field("level", "$CURRENT_LOG_LEVEL")
logger.settings.string_format = "[ $timestamp ] :: $CURRENT_LOG_LEVEL :: $message"

logger.debug(f"{shared.APP_NAME} v{shared.VERSION}")
greet(shared.VERSION)

def set_overrides():
    if args.jackett_key is not None:
        shared.JACKETT_APIKEY = args.jackett_key       

    if args.length is not None:        
        shared.DESC_LENGTH = args.length

    if args.limit is not None:        
        shared.RESULTS_LIMIT = args.limit

    if args.jackett_indexer is not None:        
        shared.JACKETT_INDEXER = args.jackett_indexer

    # Set default sorting
    if args.sort is not None:
        shared.SORT = "cn,size"

    if args.local:
        shared.TOR_CLIENT = "local"
    
    if args.verbose:
        shared.VERBOSE_MODE = True

    if args.download:
        shared.DOWNLOAD = args.download
    
    if args.insecure:
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        shared.VERIFY = False

    if args.indexer_manager is not None:
        shared.INDEXER_MANAGER = args.indexer_manager       

    if args.prowlarr_key is not None:
        shared.PROWLARR_APIKEY = args.prowlarr_key

    if args.prowlarr_indexer is not None:        
        shared.PROWLARR_INDEXER = args.prowlarr_indexer


    if args.list:        
        if os.path.exists(args.list):
            shared.TERM_FILE = args.list
        else:
            print(f"{args.list} does not exist.")
            exit()

def prompt_torrent():
    if shared.DOWNLOAD:
        if len(shared.TORRENTS) > 0:
            # Prevent out of bound results
            if shared.DOWNLOAD > len(shared.TORRENTS):
                shared.DOWNLOAD = len(shared.TORRENTS)
            for i in range(shared.DOWNLOAD):
                download(shared.TORRENTS[i].id)
            if shared.TERM_FILE != None:
                return
            else:
                exit()
        else:
            print("Search did not yield any results.")
            exit()
    print("\nCommands: \n\t:download, :d ID\n\t:next, :n\n\t:prev, :p\n\t:quit, :q\n\tTo search something else, just type it and press enter.")
    try:
        cmd = input("-> ")
    except Exception as e:
        print(f"Invalid input: {str(e)}")
        prompt_torrent()
    if cmd.startswith(":download") or cmd.startswith(":d"):
        if len(cmd.split()) < 2:
            print("Invalid input")
            prompt_torrent()
        id = cmd.split()[1]
        if not id.isdigit():
            print(f"Not a valid id.({id})")
            logger.warning(f"Not a valid id.({id}). We were expecting an integer.")
            prompt_torrent()
        else:
            download(id)
            exit()
    if cmd.startswith(":quit") or cmd.startswith(":q"):
        exit()
    if cmd.startswith(":next") or cmd.startswith(":n"):
        display_results(shared.CURRENT_PAGE + 1)
    if cmd.startswith(":prev") or cmd.startswith(":p"):
        display_results(shared.CURRENT_PAGE - 1)        
    if cmd.strip() == "":
        prompt_torrent()
    search(cmd)


################################################################################
################################################################################
###			download function
################################################################################
################################################################################

def download(id):
    torrent = get_torrent_by_id(shared.TORRENTS, id)
    if(torrent.protocol == "torrent"):
        if torrent is None:
            print(f"Cannot find {id}.")
            logger.warning(f"Invalid id. The ID provided was not found in the list.")
            search(args.search)    
        else:    
            if shared.TOR_CLIENT.lower() == "transmission":
                transmission(torrent, shared.CLIENT_URL, shared.TOR_CLIENT_USER, shared.TOR_CLIENT_PW, logger)
            elif shared.TOR_CLIENT.lower() == "deluge":
                deluge(torrent, shared.CLIENT_URL, shared.TOR_CLIENT_USER, shared.TOR_CLIENT_PW, logger)
            elif shared.TOR_CLIENT.lower() == "qbittorrent":
                qbittorrent(torrent, shared.CLIENT_URL, shared.TOR_CLIENT_USER, shared.TOR_CLIENT_PW, logger)
            elif shared.TOR_CLIENT.lower() == "local":
                local(torrent, shared.DOWNLOAD_DIR, logger)            
            else:
                print(f"Unsupported torrent client. ({shared.TOR_CLIENT})")
                exit()
                
    if(torrent.protocol == "usenet"):
        if torrent is None:
            print(f"Cannot find {id}.")
            logger.warning(f"Invalid id. The ID provided was not found in the list.")
            search(args.search)    
        else:
            if which("nzbget"):
                nzbget(torrent, shared.NZBGET_URL, shared.NZBGET_USER, shared.NZBGET_PW, shared.NZBGET_PORT, logger)            
            else:
                print(f"nzbget not found.")
                exit()


################################################################################
################################################################################
###			search functon
################################################################################
################################################################################
def runShellCmd(cmd):
    output = subprocess.run(cmd, stdout=subprocess.PIPE, shell = True)
    return output

def search(search_terms):
    
    print(f"Searching for \"{search_terms}\"...\n")
    try:
        if shared.INDEXER_MANAGER == "jackett":
            url = f"{shared.JACKETT_URL}/api/v2.0/indexers/{shared.JACKETT_INDEXER}/results?apikey={shared.JACKETT_APIKEY}&Query=" + urllib.parse.quote(search_terms)
            print(url)
            r = requests.get(url, verify=shared.VERIFY)
            json_data = json.loads(r.content)["Results"]
            res = []
            for item in json_data:
                item["title"] = item.pop("Title")
                item["seeders"] = item.pop("Seeders")
                item["leechers"] = item.pop("Peers")
                item["size"] = item.pop("Size")
                item["age"] = 0
                item["downloadUrl"] = item.pop("Link")
                if re.search("中文", item["title"]):
                    item['cn'] = 1
                else:
                    item['cn'] = 0
                item['protocol'] = 'torrent'
                if re.search(search_terms, item["title"]):
                    res.append(item)

        elif shared.INDEXER_MANAGER == "prowlarr":
            headers = {"Accept": "application/json",
                       "Content-Type": "application/json",
                       "X-Api-Key": shared.PROWLARR_APIKEY}
            url = f"{shared.PROWLARR_URL}/api/v1/search?query=" + urllib.parse.quote(search_terms)
            if shared.PROWLARR_INDEXER:
                url = url + "&indexerIds=" + shared.PROWLARR_INDEXER
            print(url)
            r = requests.get(url, verify=shared.VERIFY,headers = headers)
            json_data = json.loads(r.text)
            print(json_data)
            ## title must contain search_terms and add cn label
            res = []
            for item in json_data:
                if re.search("中文", item["title"]):
                    item['cn'] = 1
                else:
                    item['cn'] = 0

                if item['protocol'] == 'usenet':
                    item['seeders'] = 0
                    item['leechers'] = 0
                res.append(item)
                if re.search(search_terms, item["title"]):
                    res.append(item)
        elif shared.INDEXER_MANAGER == "MovieInfo":
            if not which("MovieInfo"):
                print("please install MovieInfo by: pip install getmovieinfo")
                exit()
            r = runShellCmd('MovieInfo --number "' + urllib.parse.quote(search_terms) +'"')
            if r.stdout :
                json_data = json.loads(r.stdout.decode("utf8"))
            res = []
            for item in json_data:
                item['cn'] = item['isChn']
                item['protocol'] = 'torrent'
                item['seeders'] = 0
                item['leechers'] = 0
                item["age"] = 0
                item["downloadUrl"] = item.pop("magnetlink")
                if not item['size'].isdigit():
                    if re.findall("GB",item['size'], flags=re.IGNORECASE):
                        item['size'] = re.sub("GB|GI|G","",item['size'].replace(" ","").strip(),flags=re.IGNORECASE)
                        item['size'] = float(item['size']) * 1000 * 1000 * 1000
                        print(item['size'])
#                    if re.findall("MB|M",item['size'],flags=re.IGNORECASE):
#                        item['size'] = item['size'].replace(" ","").strip().replace("MB|M","",flags=re.IGNORECASE)
#                        item['size'] = float(item['size']) * 1000
                res.append(item)
        else:
            print(f"wrong indexer_manager, must be jackett/prowlarr:  {indexer_manager}")
                    
        res = sort_torrents(res)
        if shared.INDEXER_MANAGER == "jackett" or shared.INDEXER_MANAGER == "prowlarr":
            logger.debug(f"Request made to: {url}")
            logger.debug(f"{str(r.status_code)}: {r.reason}")
            logger.debug(f"Headers: {json.dumps(dict(r.request.headers))}")
            if r.status_code != 200:
                print(f"The request to Jackett failed. ({r.status_code})")
                logger.error(f"The request to Jackett failed. ({r.status_code}) :: {shared.JACKETT_URL}api?passkey={shared.APIKEY}&search={search_terms}")
                exit()
        res_count = len(res)
        logger.debug(f"Search yielded {str(res_count)} results.")
        if shared.VERBOSE_MODE:
            logger.debug(f"Search request content: {r.text}")
    except Exception as e:
        print(f"The request to Jackett failed.{str(e)}")
        logger.error(f"The request to Jackett failed. {str(e)}")
        exit()
    id = 1

    for r in res:
        if filter_out(r['title'], shared.EXCLUDE):
            continue
        if len(r['title']) > shared.DESC_LENGTH:
            r['title'] = r['title'][0:shared.DESC_LENGTH]
        download_url = r['downloadUrl']
        shared.TORRENTS.append(torrent(id, r['title'], "", r['seeders'], r['leechers'], download_url, r['size'],r['age'],r['protocol'],r['cn']))
        id += 1

    #Sort torrents array
    #sort_torrents(shared.TORRENTS)

    # Display results
    shared.CURRENT_PAGE = 1
    display_results(shared.CURRENT_PAGE)


################################################################################
################################################################################
###			display result using table
################################################################################
################################################################################
def display_results(page):
    display_table = []
    if page < 1:
        prompt_torrent()    
    shared.CURRENT_PAGE = page
    count = 0
    slice_index = (shared.CURRENT_PAGE - 1) * shared.RESULTS_LIMIT
    for tor in shared.TORRENTS[slice_index:]:
        if count >= shared.RESULTS_LIMIT:
            break
        tor.size = "{:.2f}".format(float(tor.size)/1000000)
        display_table.append([tor.id, tor.description, tor.media_type,
                              f"{tor.size}GB", tor.seeders, tor.leechers, tor.ratio, tor.age,tor.protocol,tor.cn])
        count += 1
    print(tabulate(display_table, headers=[    
          "ID", "Description", "Type", "Size", "Seeders", "Leechers", "Ratio","Age","Protocol","cn"], floatfmt=".2f", tablefmt=shared.DISPLAY))
    print(f"\nShowing page {shared.CURRENT_PAGE} - ({count * shared.CURRENT_PAGE} of {len(shared.TORRENTS)} results), limit is set to {shared.RESULTS_LIMIT}")    
    prompt_torrent()

    
################################################################################
################################################################################
###			new sort function
################################################################################
################################################################################

    
def sort_torrents(json_data):
    sortkeys = shared.SORT.split(",")
    print(sortkeys)
    json_data = sorted(json_data,key =operator.itemgetter(*sortkeys),reverse=True)
    #print(json_data)
    return json_data




def main():
    set_overrides()
    if shared.TERM_FILE is not None:
        f = open(shared.TERM_FILE, 'r')
        for line in f.readlines():
            search(line.strip())
        exit()
    elif not args.search:
        print("Nothing to search for.")
        exit()
    else:
        search(args.search)


if __name__ == "__main__":
    main()
