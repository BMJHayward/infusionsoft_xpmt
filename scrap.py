
def list_to_file(targ_list):

    with open('inv_list','a+') as tempfile:
        for i in range(0, len(targ_list)):
            tempfile.write(repr(targ_list[i]))
            tempfile.write(",")
            tempfile.write("\n")

def extend_list(targ_list):

    idinv_list = []
    for i in targ_list:
        idinv_list.extend(i['Id'])

def recurs_iter(target):

    if type(target) is list:
        src = recurs_iter(iter(target))
    return type(src)
