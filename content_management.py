
from datetime import date
from operator import itemgetter


class Content():
    def __init__(self):
        self.content_dict = {"Data Analysis":
                             [["Weather and Earthquakes",
                               "weather-earthquakes",
                               date(2017, 8, 31)]],
                             "Education": [],
                             "Geology": []}

        self.projects_list = [["GFA: GNSS Field Analysis",
                               "https://github.com/VicenteYanez/GFA"]]

    def top5(self):
        """
        Method that calculates the last 5 post
        """
        tagdata = self.content_dict['Data Analysis']
        tagedu = self.content_dict['Education']
        # add any other tag in the dictionaty !!!!!!!!!!!!!!!!!!!!

        allcontent = tagdata + tagedu

        sortedcontent = sorted(allcontent, key=itemgetter(2), reverse=True)

        return sortedcontent[:5]

    def load_dates(self):
        return
