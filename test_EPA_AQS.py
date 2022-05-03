from EPA_AQS_functions import *
from matplotlib.dates import DateFormatter


#additional learning objective: make plots that are relevant to what we learned about criteria air pollutants in the US. 
#For example, noting the NAAQS concentrations on plots, using appropriate axis labels, discussing not only what is being plotted by why it is important


'''
National Ambient Air Quality Standards (NAAQS)
CO: 8 hr avg: 9 ppm, 1hr: 35 ppm (not to be exceeded more than 1 time/yr)
#Lead (Pb): rolling 3 month avg: .15 ug/m3
O3: 8 hr avg: .07 ppm

PM2.5: 1 yr avg: primary: 12 ug/m3, secondary: 15 ug/m3, 24 hr avg: 35 ug/m3

SO2: 1 hr avg: 75 ppb, 3 hr avg: .5 ppb


params (from: https://www.epa.gov/aqs/aqs-code-list) : 
CO: 42101
Pb:
NO2:42602
O3:44201
PM2.5: 88101 (local conditions)
PM10: 85101 (LC)
SO2: 42401


'''

#d = mon_byState(param='42101',bdate='20190101',edate='20190102',state='Iowa') #davenport
#print(d[['site_number', 'parameter_name', 'county_code']])
#print(county_code("Iowa", "Scott"),state_code('Iowa'))

labels = ['CO', 'O3', 'PM2.5', 'SO2']
naaqs_units = ['ppm','ppm', 'ug/m3', 'ppb']
naaqs_limit = [8,.07,12,75]
param_list=['42101','44201','88101','42401']
#CO ts
d = samp_bySite(param=param_list[0],bdate='20200101',edate='20201231',state='Iowa',county='Scott',site='0015')
#print(d.columns.values)
#print(d[['date_gmt','time_gmt','sample_measurement', 'units_of_measure']].dtypes)

d['GMT']=pd.to_datetime(d['date_gmt'] + d['time_gmt'], format='%Y-%m-%d%H:%M')
print(d['GMT'])

x=d['GMT']
y=d['sample_measurement']
y_8hr_avg=d['sample_measurement'].rolling(8).mean()
fig, ax = plt.subplots(figsize=(10, 10))

# Add x-axis and y-axis
ax.plot(x,y,color='blue',label='raw data')
ax.plot(x,y_8hr_avg,color='red',label='8 hr avg')

# Set title and labels for axes
ax.set(xlabel="Date",
       ylabel="ppm",
       title="2020 CO concentration \n Scott County, IA")

# Define the date format
date_form = DateFormatter("%m-%d-%y")
ax.xaxis.set_major_formatter(date_form)
plt.xticks(rotation=45)
plt.axhline(y=naaqs_limit[0],color='purple',linestyle='-')
ax.annotate('NAAQS 8 hr limit', (d['GMT'].iat[-1150],naaqs_limit[0]+.1))
#

ax.legend(loc='upper left')

parameters = {'axes.labelsize': 15,
          'axes.titlesize': 30,
          'xtick.labelsize': 15,
          'ytick.labelsize': 15,
          'legend.fontsize':10}
plt.rcParams.update(parameters)


plt.show()
'''
#O3 ts
d = samp_bySite(param=param_list[1],bdate='20200501',edate='20200731',state='Iowa',county='Scott',site='0015')
print(d.columns.values)
print(d[['date_gmt','time_gmt','sample_measurement', 'units_of_measure']].dtypes)

d['GMT']=pd.to_datetime(d['date_gmt'] + d['time_gmt'], format='%Y-%m-%d%H:%M')
print(d['GMT'])

x=d['GMT']
y=d['sample_measurement']
y_8hr_avg=d['sample_measurement'].rolling(8).mean()
fig, ax = plt.subplots(figsize=(10, 10))

# Add x-axis and y-axis
ax.plot(x,y,color='blue',label='raw data')
ax.plot(x,y_8hr_avg,color='red',label='8 hr avg')

# Set title and labels for axes
ax.set(xlabel="Date",
       ylabel="ppm",
       title="2020 O3 concentration \n Scott County, IA")

# Define the date format
date_form = DateFormatter("%m-%d-%y")
ax.xaxis.set_major_formatter(date_form)
plt.xticks(rotation=45)
plt.axhline(y=naaqs_limit[1],color='purple',linestyle='-')
ax.annotate('NAAQS 8 hr limit', (d['GMT'].iat[-1150],naaqs_limit[1]+.001))
#

ax.legend(loc='upper left')

parameters = {'axes.labelsize': 15,
          'axes.titlesize': 30,
          'xtick.labelsize': 15,
          'ytick.labelsize': 15,
          'legend.fontsize':10}
plt.rcParams.update(parameters)


plt.show()
'''
'''
#O3 hist
d = samp_bySite(param=param_list[1],bdate='20200101',edate='20201231',state='Iowa',county='Scott',site='0015')
print(d.columns.values)
print(d[['date_gmt','time_gmt','sample_measurement', 'units_of_measure']].dtypes)

d['GMT']=pd.to_datetime(d['date_gmt'] + d['time_gmt'], format='%Y-%m-%d%H:%M')
print(d['GMT'])

x=d['GMT']
y=d['sample_measurement']

fig, ax = plt.subplots(figsize=(10, 10))

# Add x-axis and y-axis
ax.hist(y,color='blue',label='CO concentration')

# Set title and labels for axes
ax.set(xlabel="ppm",
       ylabel="",
       title="2020 O3 concentration \n Scott County, IA")

# Define the date format
#date_form = DateFormatter("%m-%d-%y")
#ax.xaxis.set_major_formatter(date_form)
#plt.axhline(y=naaqs_limit[0],color='r',linestyle='-')
#ax.annotate('NAAQS 8 hr limit', (d['GMT'].iat[-1100],naaqs_limit[0]+.1))
#plt.xticks(rotation=45)

#ax.legend(loc='upper right')

parameters = {'axes.labelsize': 15,
          'axes.titlesize': 30,
          'xtick.labelsize': 15,
          'ytick.labelsize': 15}
plt.rcParams.update(parameters)


plt.show()
'''
'''
d = samp_bySite(param=param_list[0],bdate='20200101',edate='20201231',state='Iowa',county='Scott',site='0015')
print(d.columns.values)
print(d[['date_gmt','time_gmt','sample_measurement', 'units_of_measure']].dtypes)

d['GMT']=pd.to_datetime(d['date_gmt'] + d['time_gmt'], format='%Y-%m-%d%H:%M')
print(d['GMT'])

x=d['GMT']
y=d['sample_measurement']

fig, ax = plt.subplots(figsize=(10, 10))

# Add x-axis and y-axis
ax.hist(y,color='purple',label='CO concentration')

# Set title and labels for axes
ax.set(xlabel="ppm",
       ylabel="",
       title="2020 CO concentration \n Scott County, IA")

# Define the date format
#date_form = DateFormatter("%m-%d-%y")
#ax.xaxis.set_major_formatter(date_form)
#plt.axhline(y=naaqs_limit[0],color='r',linestyle='-')
#ax.annotate('NAAQS 8 hr limit', (d['GMT'].iat[-1100],naaqs_limit[0]+.1))
#plt.xticks(rotation=45)

#ax.legend(loc='upper right')

parameters = {'axes.labelsize': 15,
          'axes.titlesize': 30,
          'xtick.labelsize': 15,
          'ytick.labelsize': 15}
plt.rcParams.update(parameters)


plt.show()
'''
'''
#CO ts
d = samp_bySite(param=param_list[0],bdate='20100101',edate='20101231',state='Iowa',county='Scott',site='0015')
print(d.columns.values)
print(d[['date_gmt','time_gmt','sample_measurement', 'units_of_measure']].dtypes)

d['GMT']=pd.to_datetime(d['date_gmt'] + d['time_gmt'], format='%Y-%m-%d%H:%M')
print(d['GMT'])

x=d['GMT']
y=d['sample_measurement']

fig, ax = plt.subplots(figsize=(10, 10))

# Add x-axis and y-axis
ax.plot(x,y,color='purple',label='CO concentration')

# Set title and labels for axes
ax.set(xlabel="Date",
       ylabel="ppm",
       title="2010 CO concentration \n Scott County, IA")

# Define the date format
date_form = DateFormatter("%m-%d-%y")
ax.xaxis.set_major_formatter(date_form)
plt.axhline(y=naaqs_limit[0],color='r',linestyle='-')
ax.annotate('NAAQS 8 hr limit', (d['GMT'].iat[-1100],naaqs_limit[0]+.1))
#plt.xticks(rotation=45)

#ax.legend(loc='upper right')

parameters = {'axes.labelsize': 15,
          'axes.titlesize': 30,
          'xtick.labelsize': 15,
          'ytick.labelsize': 15}
plt.rcParams.update(parameters)


plt.show()
'''