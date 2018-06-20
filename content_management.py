
from datetime import date
from operator import itemgetter


class Content():
    def __init__(self):
        self.content_dict = {"Data Analysis":
                             [["Building the blog part I(spanish only)",
                               "building-the-blog-1",
                               date(2017, 10, 23)]],
                             "Education": [],
                             "Geology": []}
        self.map_dict = {"Data Analysis": [],
                         "Education": [["Constitución-Malargue",
                                       "mapa-constitucion-malargue",
                                        date(2014, 11, 1)]],
                         "Geology": [["Mapa Geológico Andes del Sur",
                                      "mapa-geologico-andes",
                                      date(2016, 10, 1)]]
                         }
        
    def lists(self):
        """
        Method a list with the posts
        """
        # lists with the posts in every tag
        tagdata = self.content_dict['Data Analysis']
        tagedu = self.content_dict['Education']
        taggeo = self.content_dict['Geology']
        # add any other tag in the dictionaty !!!!!!!!!!!!!!!!!!!!

        # sum all the post in one list and sorted by date
        allcontent = tagdata + tagedu + taggeo
        sortedcontent = sorted(allcontent, key=itemgetter(2), reverse=True)
        
        return sortedcontent

    def maps(self):
        """
        Method that return list with the maps
        """
        # lists with the posts in every tag
        tagdata = self.map_dict['Data Analysis']
        tagedu = self.map_dict['Education']
        taggeo = self.map_dict['Geology']
        # add any other tag in the dictionaty !!!!!!!!!!!!!!!!!!!!

        # sum all the post in one list and sorted by date
        allcontent = tagdata + tagedu + taggeo
        maplist = sorted(allcontent, key=itemgetter(2), reverse=True)

        return maplist
