import optparse
import sys
import urllib.request
import urllib.parse
import configparser

import browser


# Create or load configuration file
config = configparser.ConfigParser()
try:
    config.read("config.ini")
except EnvironmentError:
    open("config.ini", "w")
    config.read("defaultconfig.ini")
    config.write("config.ini")
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
    values = {"method": "users.get",
              "uids": ",".join(ids)}
    query = urllib.parse.urlencode(values).encode("utf8")
    request = urllib.request.Request(api_url, query)
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



    with output as fh:
        fh.write(str(auth()))


main()
