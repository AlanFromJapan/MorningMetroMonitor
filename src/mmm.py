from bs4 import BeautifulSoup
from webutils import get_web_page_content
import routes
import re
from config import conf
from line_notifier import send_line_message


# Extracts the departure and arrival stations and the duration of the trip from the text "16:05→16:40（35分）" (BEWARE JAPANESE PARENTHESES)
RE_DEPART_END="""(?P<departure>[^→]+)→(?P<arrival>[^（]+)（(?P<duration>\d+)"""
re_depart_end = re.compile(RE_DEPART_END)


def get_metro_status():
    result = []

    html_body = get_web_page_content(conf["url"])

    soup = BeautifulSoup(html_body.decode("utf-8"), 'html.parser')

    #the DOM is HEAVILY modified by javascript, so we need to find the right object. So parse whatever BS4 gives us, not what you see in the browser.
    #use the summary class to get the route list
    routelist = soup.find_all("ul", class_="summary")

    for route in routelist:
        
        m = re_depart_end.match(route.find("li", class_="time").text)

        r = routes.Route(
            duration= int(m.group("duration")),
            transfer_count= int(re.findall(r"\d+", route.find("li", class_="transfer").text)[0]),
            departure= m.group("departure"),
            arrival= m.group("arrival")
        )
        
        for flag in route.find_all("li", class_="priority"):
            if flag is not None and flag.span is not None:
                r.flags.append(flag.span.text)

        result.append(r)
        

    return result


def check_for_delays(routes):
    #basically in my case if it takes me more than 45 minutes to bring the kids to school, there's a problem and I need to know about it BEFORE I leave the house.
    delay=False
    fastest_route = None

    #shouldn't take more than x minutes
    longest_expected_minimum_duration = conf["longest_expected_minimum_duration"]
    #in my case filtering on the number of transfers is enough to get the fastest route (with the "fast" flag on the route too)
    expected_transfers = conf["expected_transfers"]

    for route in routes:
        if route.transfer_count == expected_transfers and '早' in route.flags:
            fastest_route = route
            if route.duration > longest_expected_minimum_duration:
                delay= True

    return fastest_route, delay



def main():
    metro_status = get_metro_status()

    fastest_route, delay = check_for_delays(metro_status)
    print (fastest_route)
    if delay:
        print("There are delays in the metro system")
    else:
        print("Metro system is running smoothly")


    send_line_message(str(fastest_route) + "\n\n" + ("There are delays in the metro system" if delay else "Metro system is running smoothly") + "\n\n" + conf["url"])

if __name__ == "__main__":
    main()