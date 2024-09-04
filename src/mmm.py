from bs4 import BeautifulSoup
from webutils import get_web_page_content
import routes
import re

URL="https://transit.yahoo.co.jp/search/result?from=%E7%B6%BE%E7%80%AC&to=%E6%96%B0%E6%9D%BF%E6%A9%8B&fromgid=&togid=&flatlon=%2C%2C22499&tlatlon=%2C%2C22729&via=&viacode&type=1&ticket=ic&expkind=1&userpass=1&ws=3&s=0&al=1&shin=1&ex=1&hb=1&lb=1&sr=1"

RE_DEPART_END="""(?P<departure>[^→]+)→(?P<arrival>[^（]+)（(?P<duration>\d+)"""
re_depart_end = re.compile(RE_DEPART_END)


def get_metro_status():
    result = []

    html_body = get_web_page_content(URL)

    soup = BeautifulSoup(html_body.decode("utf-8"), 'html.parser')

    # with open("output.html", "w") as file:
    #     file.write(str(response.decode("utf-8"),))

    routelist = soup.find_all("ul", class_="summary")

    for route in routelist:
        
        m = re_depart_end.match(route.find("li", class_="time").text)
        r = routes.Route(
            duration= m.group("duration"),
            transfer_count= re.findall(r"\d+", route.find("li", class_="transfer").text)[0],
            departure= m.group("departure"),
            arrival= m.group("arrival")
        )
        
        for flag in route.find_all("li", class_="priority"):
            if flag is not None and flag.span is not None:
                r.flags.append(flag.span.text)

        result.append(r)
        

    return result

def main():
    metro_status = get_metro_status()

    for route in metro_status:
        print(route)
        print(" ")

if __name__ == "__main__":
    main()