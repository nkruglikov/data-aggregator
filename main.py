import optparse
import sys
import os
import urllib.request
import urllib.parse
import configparser

import browser


# Create or load configuration file
config = configparser.ConfigParser()
if os.path.exists("config.ini"):
    config.read("config.ini")
else:
    with open("config.ini", "w") as config_file:
        config.read("defaultconfig.ini")
        config.write(config_file)
vk_config = config["vk.com"]

# Set up global constants
api_url = vk_config["api_url"]
oauth_url = vk_config["oauth_url"]
permissions = list(vk_config["permissions"])


def auth():
    """ Opens a browser window with an authenitication invitation. """
    """ Returns a tuple of access_token and expires_in values. """
    values = {"client_id": "4554642",
              "scope": ",".join(permissions),
              "redirect_uri": "https://oauth.vk.com/blank.html",
              "display": "page",
              "v": "5.24",
              "response_type": "token"}
    brwsr = browser.Browser(oauth_url, values)
    return brwsr.data


def get_data(ids):
    values = {"access_token": vk_config["access_token"],
              "uids": ",".join(ids)}
    method_url = api_url + "users.get"
    query = urllib.parse.urlencode(values).encode("utf8")
    request = urllib.request.Request(method_url, query)
    response = urllib.request.urlopen(request).read().decode()
    return response


def main():
    # Parse command-line options
    parser = optparse.OptionParser()
    parser.set_description("Saves profiles of users, whose ids listed"
            " as options")
    parser.add_option("-o", "--output", dest="filename",
            help="print to <filename>, not stdout")

    opts, ids = parser.parse_args()

    # Select console/file output
    if opts.filename is not None:
        output = open(opts.filename + ".dat", "w", encoding="utf8")
    else:
        output = sys.stdout

    # Get user session
    if "access_token" not in vk_config:
        print("[*] Getting user session...")
        access_token, user_id = auth()
        vk_config.update({"access_token": access_token, "user_id": user_id})
        print("[+] Got.")

    with output as fh:
        print("[*] Gathering data...")
        fh.write(str(get_data([vk_config["user_id"]])))
        print("[+] Done.")


try:
    main()
finally:
    with open("config.ini", "w") as config_file:
        config.write(config_file)
