
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        views.py
# Purpose:      the REST endpoints
#
#
# Author:      claudio piccinini
#
# Updated:
#-------------------------------------------------------------------------------

#   request.data -> contains the POST parameters
#   request.query_params -> contains the GET parameters
#   **kw -> contains part of the url as defined in urls.py

###########################################################



from rest_framework.views import APIView
from rest_framework.response import Response


#from rest_framework.permissions import IsAuthenticated
#from rest_framework.parsers import MultiPartParser, FormParser

import app.main as main

class Initialize(APIView):    ##########testing rest parameters
    """
    Start a synchronous task
    """
    #e.g.  http://localhost:8100/processing/synch_asynch_tests/synch/executesync/

    ####permission_classes = (IsAuthenticated,) #only authenticad users can see this
    #parser_classes = (MultiPartParser, FormParser,)


    def get(self, request, *args, **kw):
        return self.get_post(request, "get", *args, **kw)

    def post(self, request, *args, **kw):
        #return Response({"success": True, "content": "Hello World!"})
        #return Response(request.data)
        return self.get_post(request, "post", *args, **kw)


    def get_post(self, request, verb, *args, **kw ):
        """
        Handle both GET and POST requests
        :param request:  request.data -> contains the POST parameters; request.query_params -> contains the GET parameters
        :param verb: this is "get" or "post"
        :param args:
        :param kw: contains part of the url as defined in urls.py
        :return:
        """

        #name = kw['']
        #tname = kw['']

        try:

            exists =  main.check_table()
            if exists: return Response({"success": True, "content": "table was already initialized"})

            folder, file_name = main.download_zip("http://www2.census.gov/geo/tiger/GENZ2016/shp/cb_2016_us_state_20m.zip")
            base = main.unzip(folder, file_name)
            shapename = main.check_shapefile(folder + "/" + base + '/')

            epsg = main.get_epsg(folder + "/" + base + '/' + shapename)
            if epsg != "4326":
                print("Coordinate system is epgs:" + epsg)
                print("Coordinate system will be converted to epgs:4326")
                print("reprojecting....")
                dataset = main.reproject_vector(folder + "/" + base + '/' + shapename, epsg_from=int(epsg), epsg_to=4326)
                print("overwrite shapefile...")
                main.save_vector(dataset, folder + "/" + base + '/' + shapename, driver=None)
                dataset = None

            print("uploading states")
            main.upload_shape(folder + "/" + base + '/' + shapename)

            return Response({"success": True, "content": "shapefile downloaded,unzipped,checked ,and uploaded to database"})


        except Exception as e:
            return Response({"success": False, "content": str(e)})

class GetStates(APIView):    ##########testing rest parameters
    """
    Start a synchronous task
    """
    #e.g.  http://localhost:8100/processing/synch_asynch_tests/synch/executesync/

    ####permission_classes = (IsAuthenticated,) #only authenticad users can see this
    #parser_classes = (MultiPartParser, FormParser,)


    def get(self, request, *args, **kw):
        return self.get_post(request, "get", *args, **kw)

    def post(self, request, *args, **kw):
        #return Response({"success": True, "content": "Hello World!"})
        #return Response(request.data)
        return self.get_post(request, "post", *args, **kw)


    def get_post(self, request, verb, *args, **kw ):
        """
        Handle both GET and POST requests
        :param request:  request.data -> contains the POST parameters; request.query_params -> contains the GET parameters
        :param verb: this is "get" or "post"
        :param args:
        :param kw: contains part of the url as defined in urls.py
        :return:
        """


        try:
            states =  main.get_geojson()
            return Response(
                {"success": True, "content": states})


        except Exception as e:
            return Response({"success": False, "content": str(e)})


class AddPoint(APIView):    ##########testing rest parameters
    """
    Start a synchronous task
    """
    #e.g.  http://localhost:8100/processing/synch_asynch_tests/synch/executesync/

    ####permission_classes = (IsAuthenticated,) #only authenticad users can see this
    #parser_classes = (MultiPartParser, FormParser,)


    def get(self, request, *args, **kw):
        return self.get_post(request, "get", *args, **kw)

    def post(self, request, *args, **kw):
        #return Response({"success": True, "content": "Hello World!"})
        #return Response(request.data)
        return self.get_post(request, "post", *args, **kw)


    def get_post(self, request, verb, *args, **kw ):
        """
        Handle both GET and POST requests
        :param request:  request.data -> contains the POST parameters; request.query_params -> contains the GET parameters
        :param verb: this is "get" or "post"
        :param args:
        :param kw: contains part of the url as defined in urls.py
        :return:
        """


        queryparams = request.query_params

        try:

            x = queryparams .get('x', None)
            y = queryparams .get('y', None)
            label = queryparams .get('label', None)

            if not x or not y or not label:
                raise Exception("missing x,y,label")

            #check we good numbers
            float(x)
            float(y)

            x, y, size = main.upload_point(x,y,label)

            return Response({"success": True, "content": {"x": float(x), "y":float(y), "label":label, "size": size}})

        except Exception as e:
            return Response({"success": False, "content": str(e)})


class GetAllPoints(APIView):    ##########testing rest parameters
    """
    Start a synchronous task
    """
    #e.g.  http://localhost:8100/processing/synch_asynch_tests/synch/executesync/

    ####permission_classes = (IsAuthenticated,) #only authenticad users can see this
    #parser_classes = (MultiPartParser, FormParser,)


    def get(self, request, *args, **kw):
        return self.get_post(request, "get", *args, **kw)

    def post(self, request, *args, **kw):
        #return Response({"success": True, "content": "Hello World!"})
        #return Response(request.data)
        return self.get_post(request, "post", *args, **kw)


    def get_post(self, request, verb, *args, **kw ):
        """
        Handle both GET and POST requests
        :param request:  request.data -> contains the POST parameters; request.query_params -> contains the GET parameters
        :param verb: this is "get" or "post"
        :param args:
        :param kw: contains part of the url as defined in urls.py
        :return:
        """

        try:

            points = main.get_allpoints_geojson()
            return Response({"success": True, "content": points})
        #return Response({"success": False, "content": ""})

        except Exception as e:
            return Response({"success": False, "content": str(e)})