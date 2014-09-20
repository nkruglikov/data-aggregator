import optparse
import sys
import urllib.request
import urllib.parse
import browser

api_url = "https://api.vk.com/api.php"
oauth_url = "https://oauth.vk.com/authorize"
permissions = ["friends", "photos", "status", "wall", "groups",
        "messages", "offline"]


def auth():
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
    parser = optparse.OptionParser()
    parser.set_description("Saves profiles of users, whose ids listed"
            " as options")
    parser.add_option("-o", "--output", dest="filename",
            help="print to <filename>, not stdout")

    opts, ids = parser.parse_args()

    if opts.filename is not None:
        output = open(opts.filename + ".dat", "w", encoding="utf8")
    else:
        output = sys.stdout

    with output as fh:
        fh.write(str(auth()))


main()
