# -*- coding:utf-8 -*-
"""
The MIT License (MIT)
Copyright (c) 2023-present Dmitry Filinov
Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
import requests

from typing import Union, Tuple

__all__ = ("Map",)


class Map(object):

    def __init__(
            self, api_key: str,
            coordinates: Union[Tuple[float, ...], str] = (0.0, 0.0),
            zoom: float = 10, type_of_point: str = "flag",
            points_city: str = "Moscow"

    ) -> None:
        """

        convert_address_to_coordinates(address: :class:`str`) -> tuple[float, float]
            The function converts the address to coordinates
        generate_map_url() -> None
            The function generates the main link
        add_point(coordinates: Union[str, tuple[float, float]]) -> None
            Add a point to the map
        commit_points(map_url: :class:`str`) -> :class:`str`
            Confirm all points
        """
        self.__map_url = "http://static-maps.yandex.ru/1.x/?ll={ll}&z={z}&l={type}"
        self.__api_url_template = "http://api.positionstack.com/v1/forward?access_key={key}&query={query}"

        self.points = []
        self.type_of_point: str = type_of_point
        self.api_key: str = api_key
        self.zoom: float = zoom
        self.city: str = points_city

        if isinstance(coordinates, tuple):
            self.coordinates: tuple = coordinates
        else:
            self.coordinates: tuple = self.convert_address_to_coordinates(coordinates)

        self.main_url = self.generate_map_url()

    def convert_address_to_coordinates(self, address: str) -> Tuple[float, ...]:
        request = requests.get(self.__generate_api_url(address)).json()
        return request["data"][0]["latitude"], request["data"][0]["longitude"]

    @staticmethod
    def __convert_coordinates_to_text_view(coordinates: Tuple[float, ...]) -> str:
        return str(coordinates[1]) + "," + str(coordinates[0])

    def generate_map_url(self) -> str:
        url = self.__map_url.format(
            ll=self.__convert_coordinates_to_text_view(self.coordinates),
            z=self.zoom,
            type="map"
        )
        self.commit_points(url)
        return url

    def __generate_api_url(self, address: str) -> str:
        return self.__api_url_template.format(
            key=self.api_key,
            query=f"{self.city} {address}"
        )

    def add_point(self, coordinates: Union[str, Tuple[float, ...]]) -> None:
        if isinstance(coordinates, str):
            self.points.append(self.convert_address_to_coordinates(coordinates))
        else:
            self.points.append(coordinates)

    def commit_points(self, map_url: str) -> str:
        for i in self.points:
            if "&pt=" not in map_url:
                map_url += f"&pt={i},{self.type_of_point}"
            else:
                map_url += f"~{i},{self.type_of_point}"
        self.points = []
        return map_url

    def __call__(self, path: str = "") -> None:
        response = requests.get(self.main_url)
        if not response:
            raise NameError(f"HTTP Error: {response.status_code} ({response.reason})")
        with open(f"{path + '/' if path != '' else ''}map.png", "wb") as file:
            file.write(response.content)
