import requests, csv
try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeaufifulSoup import BeautifulSoup

def main():
    url = "https://sourceconaustin2017.sched.com/directory/speakers?iframe=no&w=100%&sidebar=yes&bg=false&mobileoff=Y&ssl=yes"
    try:
        session = requests.session()
        headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.8', 
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0'
        }
        session.get("http://austin.sourcecon.com/speakers/", headers=headers, timeout=20)
        response = session.get(url, headers=headers, timeout=20)
        if response.status_code != 200:
            print "Requests.get didn't go through, without 200 status code returned."
            return
        if response == None:
            print "No valid response object returned back."
            return
        raw_html = response.text
        if raw_html:
            parse_html(raw_html)
    except:
        print "Exception thrown from requests.get! Oops..."

def parse_html(raw_html):
    try:
        soup = BeautifulSoup(raw_html, "html.parser")
        if not soup:
            return
        persons = soup.find_all("div", attrs={"class": "sched-person"})
        csvfile = open("speaker-list.csv", "wb")
        infowriter = csv.writer(csvfile, delimiter='\t', quotechar="'", quoting=csv.QUOTE_MINIMAL)
        for person in persons:
            avatar_tag = person.find("a", attrs={"class": "sched-avatar"})
            name = avatar_tag.get("title").encode('utf-8').strip()
            company = person.find("div", attrs={"class": "sched-event-details-company"}).text.encode('utf-8').strip()
            position = person.find("div", attrs={"class": "sched-event-details-position"}).text.encode('utf-8').strip()
            infowriter.writerow([name, company, position])
        csvfile.close()
    except:
        print "Exception throw from parse html@!..."


if __name__ == "__main__":
    main()
