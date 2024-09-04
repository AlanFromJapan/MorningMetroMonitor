class Route():
    def __init__(self, duration, transfer_count, departure, arrival, flags=None) -> None:
        self.duration = duration
        self.transfer_count = transfer_count
        self.departure = departure
        self.arrival = arrival
        self.flags = [] if flags is None else flags
    
    def __str__(self) -> str:
        return f"Duration: {self.duration}\nTransfer Count: {self.transfer_count}\nDeparture: {self.departure}\nArrival: {self.arrival}\nFlags: {self.flags}\n"
    
    def from_html(self, html):
        self.duration = html.find("li", class_="duration").text
        self.transfer_count = html.find("li", class_="transfer").text
        self.departure = html.find("li", class_="time").text
        self.arrival = html.find("li", class_="arrival").text
        self.flags = html.find("li", class_="flags").text