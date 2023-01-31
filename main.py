import requests


class Map(object):

    def __init__(
            self, coordinates: tuple[float, float] = (0.0, 0.0), zoom: int = 10
    ):
        self.api_key = "0410f7f7f5afc21eaa20549570506f53"  # example
        self.coordinates: tuple = coordinates
        self.zoom = zoom
        self.points = []
        self.type_of_point = "flag"
        self.map_url = "http://static-maps.yandex.ru/1.x/?ll={ll}&z={z}&l={type}"
        self.api_url_template = "http://api.positionstack.com/v1/forward?access_key={key}&query={query}"
        self.city = "Новосибирск"
        self.generate_url()

    def convert_address_to_coordinates(self, address: str):
        request = requests.get(self.generate_api_url(address)).json()
        return request["data"][0]["latitude"], request["data"][0]["longitude"]

    @staticmethod
    def convert_coordinates_to_text_view(coordinates: tuple[float, float]) -> str:
        return str(coordinates[1]) + "," + str(coordinates[0])

    def generate_url(self):
        self.map_url = self.map_url.format(
            ll=self.convert_coordinates_to_text_view(self.coordinates),
            z=self.zoom,
            type="map"
        )

    def generate_api_url(self, address: str):
        return self.api_url_template.format(
            key=self.api_key,
            query=f"{self.city} {address}"
        )

    def add_point(self, coordinates: tuple[float, float]):
        if not self.points:
            self.map_url += f"&pt={self.convert_coordinates_to_text_view(coordinates)},{self.type_of_point}"
        else:
            self.map_url += f"~{self.convert_coordinates_to_text_view(coordinates)},{self.type_of_point}"
        self.points.append(coordinates)

    def __call__(self):
        print(self.map_url)
        response = requests.get(self.map_url)
        if not response:
            raise NameError(f"HTTP Error: {response.status_code} ({response.reason})")
        with open("map.png", "wb") as file:
            file.write(response.content)
