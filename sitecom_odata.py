# Src from: https://statoilsrm.sharepoint.com/sites/cw-21579/dw/Documents/Forms/AllItems.aspx?RootFolder=%2Fsites%2Fcw%2D21579%2Fdw%2FDocuments%2FPython&FolderCTID=0x012000E8A10580CD13264C878F85FF29227AE0&OR=Teams%2DHL&CT=1635239126845
# Code by: Kjell Inge Meisal
import requests
import json
from datetime import datetime
import time
import pandas as pd

class well():
    def __init__(self, json):
        self.__dict__  = json

    def get_wellbores():
        pass

class wellbore():
    def __init__(self, json):
        self.__dict__  = json

    def get_logs():
        pass

class log():
    def __init__(self, json):
        self.__dict__  = json

    def get_data(self):
        pass

class curve():
    def __init__(self, json):
        self.__dict__  = json

class datapoint():
    def __init__(self, json):
        self.__dict__  = json

class request_mapper:
    def __init__(self, path, user, password):
        self.path = path
        self.user = user
        self.password = password

    def get(self, url, raw=False):
        if not raw:
            #print('Operation: GET, url: ' + self.path + url)
            #start = time.time()
            r = requests.get(self.path + url, auth=(self.user, self.password), verify=True)
            #end = time.time()
            #print('Time elapsed:' + str(end - start))
            return r
        else:
            #print('Operation: GET, url: ' + url)
            #start = time.time()
            r =  requests.get(url, auth=(self.user, self.password), verify=True)
            #end = time.time()
            #print('Time elapsed:' + str(end - start))
            return r

    def post(self, url, json=None):
        if not json:
            #print('Operation: POST, url: ' + self.path + url)
            return requests.post(self.path + url, auth=(self.user, self.password))
        else:
            json_string = str(json)
            if len(json_string) > 100:
                json_string = json_string[0:99] + '...'
            #print('Operation: POST, url: ' + self.path + url + ', data: ' + json_string)
            return requests.post(self.path + url, json=json, auth=(self.user, self.password))

    def delete(self, url):
        #print('Operation: DELETE, url: ' + url)
        return requests.delete(self.path + url, auth=(self.user, self.password))

class sitecom_odata:
    def __init__(self, url, user=None, password=None):
        self.url = url

        if not user:
            self.user = 'user'
        else:
            self.user = user

        if not password:
            self.password = 'password'
        else:
            self.password = password

        self.request_mapper = request_mapper(self.url, self.user, self.password)

    def get_wells(self):       
        r = self.request_mapper.get('wells')
        if r.status_code == 200:
            # Return well array based on JSON.
            wells = []
            for well_item in r.json()['value']:
                wells.append(well(well_item))
            return wells
        else:
            print('Failed to get wells, error: {0}, {1}'.format(r.status_code, r.reason))

    def get_well(self, well_id):
        r = self.request_mapper.get('wells' + '(\'' + str(well_id) + '\')')
        if r.status_code == 200:
            # Return well based on JSON.
            return well(r.json())
        else:
            print('Failed to get well, error: {0}, {1}'.format(r.status_code, r.reason))

    def get_wellbores(self, well_id):
        r = self.request_mapper.get('wells(\'' + str(well_id) + '\')/wellbores')
        if r.status_code == 200:
            # Return wellbore array based on JSON.
            wellbores = []
            for wellbore_item in r.json()['value']:
                wellbores.append(wellbore(wellbore_item))
            return wellbores
        else:
            print('Failed to get wellbores, error: {0}, {1}'.format(r.status_code, r.reason))

    def get_wellbore(self, well_id, wellbore_id):
        r = self.request_mapper.get('wells(\'' + str(well_id) + '\')/wellbores(\'' +  str(wellbore_id)  + '\')')
        if r.status_code == 200:
            # Return wellbore based on JSON.
            return wellbore(r.json())
        else:
            print('Failed to get wellbore, error: {0}, {1}'.format(r.status_code, r.reason))

    def get_logs(self, well_id, wellbore_id):
        r = self.request_mapper.get('wells(\'' + str(well_id) + '\')/wellbores(\'' +  str(wellbore_id)  + '\')/logs')
        if r.status_code == 200:
            # Return log array based on JSON.
            logs = []
            for log_item in r.json()['value']:
                logs.append(log(log_item))
            return logs
        else:
            print('Failed to get log, error: {0}, {1}'.format(r.status_code, r.reason))

    def get_log(self, well_id, wellbore_id, log_id):
        r = self.request_mapper.get('wells(\'' + str(well_id) + '\')/wellbores(\'' +  str(wellbore_id)  + '\')/logs(\'' +  str(log_id) + '\')')
        if r.status_code == 200:
            # Return log based on JSON.
            return log(r.json())
        else:
            print('Failed to get log, error: {0}, {1}'.format(r.status_code, r.reason))

    def get_curves(self, well_id, wellbore_id, log_id):
        r = self.request_mapper.get('wells(\'' + str(well_id) + '\')/wellbores(\'' +  str(wellbore_id)  + '\')/logs(\'' +  str(log_id) + '\')/curves')
        if r.status_code == 200:
            # Return log array based on JSON.
            curves = []
            for curve_item in r.json()['value']:
                curves.append(curve(curve_item))
            return curves
        else:
            print('Failed to get curves, error: {0}, {1}'.format(r.status_code, r.reason))

    def get_time_data(self, well_id, wellbore_id, log_id, filter=None, gt=None, ge=None, lt=None, le=None):
        return self.get_data( well_id, wellbore_id, log_id, 'timeData', filter, gt, ge, lt, le)

    def get_depth_data(self, well_id, wellbore_id, log_id, filter=None, gt=None, ge=None, lt=None, le=None):
        return self.get_data(well_id, wellbore_id, log_id, 'depthData', filter, gt, ge, lt, le)

    def get_data(self, well_id, wellbore_id, log_id, node, filter=None, gt=None, ge=None, lt=None, le=None):
        req_str = self.url + 'wells(\'' + str(well_id) + '\')/wellbores(\'' +  str(wellbore_id)  + '\')/logs(\'' +  str(log_id) + '\')/' + node

        # Parse filter parameters.
        if gt or ge or lt or le:
            filter_str = '?$filter='
            if lt or le:
                filter_str += 'Index '
                if lt:
                    filter_str += 'lt ' + lt
                if le:
                    filter_str += 'le ' + le
            if gt or ge:
                if lt or le:
                    filter_str += ' and '
                filter_str +='Index '
                if gt:
                    filter_str += 'gt ' + gt
                if ge:
                    filter_str += 'ge ' + ge

            req_str += filter_str

        if filter:
            req_str += '?$filter=' + filter

        get_data = True
        data = pd.DataFrame()
        while get_data:
            r = self.request_mapper.get(req_str, raw=True)
            if r.status_code == 200:
                # Return data based on JSON.
                values = r.json()['value']
                if len(values) > 0 :
                    data = data.append(r.json()['value'])
                # Check if we should read the next link.
                if '@odata.nextLink' in r.json():
                    req_str = r.json()['@odata.nextLink']
                    print('Retrieving next 10,0000 rows')
                else:
                    return data
            else:
                print('Failed to get data, error: {0}, {1}'.format(r.status_code, r.reason))
                return
