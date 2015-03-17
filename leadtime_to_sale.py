import dataserv as ds

dscxn = ds.Query()
pls_explain = {'limit': 999, 'returnData': ['Id','DateCreated']}
contacts_with_dates = dscxn.dates(**pls_explain)

def invoice(target_id=None):

    try:

        inv_args = dict(
            table='Invoice',
            limit=999,
            page=0,
            queryData={'ContactId': target_id},
            returnData=['DateCreated']
            )

        inv_dates = dscxn._basequery(**inv_args)
    
        return inv_dates

    except Exception as exc:

        print("Couldn't run query because: ", exc)


def all_contact_IDs():

    id_list = []
    pages = dscxn._getpages('Contact', 'Id')

    for i in range(0, pages + 1):
        id_list.extend(dscxn.dates(**pls_explain))
    
    return id_list


def time_to_kill():
    ''' if you have some time to kill '''
    id_list = all_contact_IDs()

    mega_list=[]
    for i in range(0, len(id_list)):
        target = id_list[i]['Id']
        mega_list.extend(invoice(target_id=target))

    return mega_list
