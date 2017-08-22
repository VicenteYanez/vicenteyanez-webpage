
from datetime import date


class Content():
    content_dict = {"Data Analysis":
                    [["Heath and Earthquakes", "weather-earthquakes"],
                     ["Stress on Volcanos: Villarica", "stress-villarica"]],
                    "Geology":
                    [["The History of Concepcion", "concepcion-history"],
                     ["The History of Toronto", "toronto-history"]],
                    "Education":
                    [["How to make boring thing fun", "boring-things-fun"]]}

    projects_list = [["GFA: GNSS Field Analysis",
                      "https://github.com/VicenteYanez/GFA"]]

    def top5():
        """
        Method that calculates the last 5 post
        """
        d1 = date(2005, 7, 14)
        d2 = date(2005, 7, 15)
        d3 = date(2005, 7, 16)
        d4 = date(2005, 7, 17)
        d5 = date(2005, 7, 18)

        post_list = [["Heath and Earthquakes", "heath-earthquakes", d1],
                     ["Stress on Volcanos: Villarica", "stress-villarica", d2],
                     ["The History of Concepcion", "concepcion-history", d3],
                     ["The History of Toronto", "toronto-history", d4],
                     ["How to make boring thing fun", "boring-things-fun", d5]]

        return post_list
