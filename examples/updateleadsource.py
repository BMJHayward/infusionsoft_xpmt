from infusionsoft.library import Infusionsoft
import os, sys
appname = os.environ['INFUSION_APPNAME']
apikey = os.environ['INFUSION_APIKEY']
infusion = Infusionsoft(appname, apikey)


data = infusion.DataService('query', 'LeadSource', 999, 0, {'Id' : '%'}, ['Id', 'Name', 'CostPerLead', 'Medium', 'Vendor'])
print(data)

data_0 = infusion.DataService('query', 'LeadSource', 999, 0, {'Id' : '%'}, ['Id', 'Name', 'CostPerLead', 'Medium', 'Vendor'])
data_1 = infusion.DataService('query', 'LeadSource', 999, 1, {'Id' : '%'}, ['Id', 'Name', 'CostPerLead', 'Medium', 'Vendor'])

data_test = infusion.DataService('query', 'LeadSource', 999, 0, {'Id' : '1664'}, ['Id', 'Name', 'CostPerLead', 'Medium', 'Vendor'])

print(data_test)

infusion.DataService('update', '1664', {'Medium' : 'Print'})
infusion.DataService(update, '1664', {'Medium' : 'Print'})
infusion.DataService('update', 1664, {'Medium' : 'Print'})
infusion.DataService('update', 'LeadSource', 1664, {'Medium' : 'Print'})
infusion.DataService('update', 'LeadSource', 1662, {'Medium' : 'Print'})


data_0[:10]


for source in data_0:
    if 'A - ' in source['Name']:
        print(source)


def check_medium(leadsource):
    if 'A - ' in leadsource['Name']:
        set_medium(leadsource['Id'], 'A - Advertising')
    elif 'I - ' in leadsource['Name']:
        set_medium(leadsource['Id'], 'I - Internet')
    elif 'L - ' in leadsource['Name']:
        set_medium(leadsource['Id'], 'L - Lectures')
    elif 'B - ' in leadsource['Name']:
        set_medium(leadsource['Id'], 'B - Books')
    elif 'D - ' in leadsource['Name']:
        set_medium(leadsource['Id'], 'D - Distributor')
    elif 'P - ' in leadsource['Name']:
        set_medium(leadsource['Id'], 'P - Practitioner')
    elif 'M - ' in leadsource['Name']:
        set_medium(leadsource['Id'], 'M - Media')
    elif 'LTR - ' in leadsource['Name']:
        set_medium(leadsource['Id'], 'LTR - Listen to Read')
    elif 'F - ' in leadsource['Name']:
        set_medium(leadsource['Id'], 'F - Festival'


def set_medium(id, medium):
    print('Updating leadsource id: ', id, ', to: ' + medium)
    infusion.DataService('update', 'LeadSource', id, {'Medium' : medium})
    print('Done.')


for source in data_0:
    check_medium(source)
for source in data_1:
    check_medium(source)


readline.write_history_file('updateleadsource.py')
%history -f 'updateleadsource.py'
