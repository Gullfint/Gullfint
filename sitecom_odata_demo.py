# Sample that uses sitecom_odata library
import sitecom_odata
import pandas as pd

# base url for the API request
odata_server = 'https://welladvisor.intellifield.no/'
path = 'SiteComOdata/api/v0.1/'
odata_url = odata_server + path

# create a connection to the OData service using your credentials
oDataService = sitecom_odata.sitecom_odata(odata_url, 'UserId', 'Password')

# retrieve the list of wells available
wells = oDataService.get_wells()
print('Number of wells found :', len(wells))

# retrieve info about the first well
well = oDataService.get_well(wells[0].uid)
print('First well name :', well.name)

# retrieve list of wellbores for that first well
wellbores = oDataService.get_wellbores(well.uid) 
print('Number of wellbores in the first well :', len(wellbores))

# retrieve info about the first wellbore returned for that first well
wellbore = oDataService.get_wellbore(well.uid, wellbores[0].uid) 
print('Name of the wellbore :', wellbore.name)

# retrieve the list of logs for that first wellbore
logs = oDataService.get_logs(well.uid, wellbore.uid)
print('Name of the first log found :', logs[0].name)

# retrieve info about the first log of the first wellbore of the first well :-)
log = oDataService.get_log(well.uid, wellbore.uid, logs[0].uid)

# retrieve all time-based curve data of that first log
data = oDataService.get_time_data(well.uid, wellbore.uid, log.uid)
print('Log {0} has {1} datarows for time-based data'.format(log.name, len(data)))

# retrieve all depth-based curve data of that first log
data = oDataService.get_depth_data(well.uid, wellbore.uid, log.uid)
print('Log {0} has {1} datarows for depth-based data'.format(log.name, len(data)))

# retrieve time-based curve data for a specific log and for a given time index range
# a typical query will look like this one
data = oDataService.get_time_data('d7e727e7-59d9-42ed-b2f7-5eb377e9a1a6', 'ab4202ea-2d6f-48fa-86c3-8d910bccfa26',
	'3bda1089-1795-41c8-b7b3-12da4e81c846', gt='2009-03-06T08:25:00.000Z', lt='2009-03-08T08:25:00.000Z')
print('Time-range query retrieved {0} rows, here are top few rows :'.format(len(data)))
print(data.head())

# specific wellbore data that we know has more than 10,000 rows.
# BEWARE!  This is an open ended query and this will bring complete dataset for all time based curves in that log
data2 = oDataService.get_time_data('d7e727e7-59d9-42ed-b2f7-5eb377e9a1a6', 'ab4202ea-2d6f-48fa-86c3-8d910bccfa26',
	'3bda1089-1795-41c8-b7b3-12da4e81c846')
print('Open ended query retrieved {0} rows, here are top few rows :'.format(len(data2)))
print(data2.head())
