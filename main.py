import optparse
import sys
import urllib.request
import urllib.parse
import webbrowser

api_url = "https://api.vk.com/api.php"
oauth_url = "https://oauth.vk.com/authorize"
permissions = ["friends", "photos", "status", "wall", "groups",
        "messages", "offline"]
access_token = open("access-token.key").read() # TEMPORARY

headers = {
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip,deflate,sdch",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4",
    "Accept-Charset": "windows-1251,utf-8;q=0.7,*;q=0.3",
    "User-Agent": "Mozilla/5.0 (Windows; I; Windows NT 5.1; ru; rv:1.9.2.13)"
        " Gecko/20100101 Firefox/4.0",
    "Cookie": "remixlang=0",
    "Host": "oauth.vk.com"
}


def auth():
    values = {"client_id": "4554642",
              "scope": ",".join(permissions),
              "redirect_uri": "https://oauth.vk.com/blank.html",
              "display": "page",
              "v": "5.24",
              "response_type": "token"}
    query = urllib.parse.urlencode(values).encode("utf8")
    print(oauth_url + "?" + query.decode())
    webbrowser.open(oauth_url + "?" + query.decode())
    request = urllib.request.Request(oauth_url, query, headers=headers)
    response = urllib.request.urlopen(request).read().decode()
    return response


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
        fh.write(auth())


main()
