import dataserv as ds

dscxn = ds.Query()
pls_explain = {'limit': 999, 'returnData': ['Id','DateCreated']}
contacts_with_dates = dscxn.dates(**pls_explain)

def invoice():

    inv_args = dict(
        table='Invoice',
        limit=999,
        page=0,
        queryData={'ContactId': '123679'},
        returnData=['DateCreated']
        )

    inv_dates = dscxn._basequery(**inv_args)

    return inv_dates


def all_contact_IDs():

    id_list = []
    pages = dscxn._getpages('Contact', 'Id')

    for i in range(0, pages + 1):
        id_list.extend(dscxn.dates(**pls_explain))
    
    return id_list
    