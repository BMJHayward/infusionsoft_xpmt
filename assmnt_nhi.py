#!/usr/bin/python

import cgi
import cgitb

from infusionsoft.library import Infusionsoft
key = [line for line in open('APIKEY.txt')][0]
appName = [line for line in open('APPNAME.txt')][0]
infusionsoft = Infusionsoft(appName, key)

form = cgi.FieldStorage()  # request data in here. Chose CGI because simple

cgitb.enable(display=0, logdir='log')

contact_id = form.getvalue("contact_id")
print("The contact being handled is %s " % contact_id)

'''
these 4 digit numbers correspond to tag id for answer to each assessment
question in Infusionsoft form.
separate dicts for answers and results written explicitly to keep code
explicit. Not using numpy because only have standard lib in production.
'''

answers = {  # get max of 'yes' answers from this list as result
    'tinnitus_yes': [1796, 1826, 1856, 1886],
    'tinnitus_no': [1800, 1830, 1860, 1890],
    'tinnitus_sometimes': [1798, 1828, 1858, 1888],

    'hearing_yes': [1808, 1838, 1868, 1898],
    'hearing_no': [1812, 1842, 1872, 1902],
    'hearing_sometimes': [1810, 1840, 1870, 1900],

    'hyperacusis_yes': [1802, 1832, 1862, 1892],
    'hyperacusis_no': [1806, 1836, 1866, 1896],
    'hyperacusis_sometimes': [1804, 1834, 1864, 1894],

    'dizziness_yes': [1814, 1844, 1874, 1904],
    'dizziness_no': [1818, 1848, 1878, 1908],
    'dizziness_sometimes': [1816, 1846, 1876, 1906],

    'blockear_yes': [1820, 1850, 1880, 1910],
    'blockear_no': [1824, 1854, 1884, 1914],
    'blockear_sometimes': [1822, 1852, 1882, 1912],
    }

result = {  # score_update() will change values of this dict
    'tinnitus_yes': 0,
    'tinnitus_no': 0,
    'tinnitus_sometimes': 0,

    'hearing_yes': 0,
    'hearing_no': 0,
    'hearing_sometimes': 0,

    'hyperacusis_yes': 0,
    'hyperacusis_no': 0,
    'hyperacusis_sometimes': 0,

    'dizziness_yes': 0,
    'dizziness_no': 0,
    'dizziness_sometimes': 0,

    'blockear_yes': 0,
    'blockear_no': 0,
    'blockear_sometimes': 0,
    }

condition_tag = {"tinnitus": 2278, "hyperacusis": 2280, "hearing": 2282,
              "dizziness": 2284, "blockear": 2286}


def query_tags(contact_id):

    returnFields = ["GroupId"]
    query = {"ContactId": contact_id}
    tags = infusionsoft.DataService("ContactGroupAssign", 100, 0,
                                    query, returnFields)

    return_tags = [item[tag] for item in tags for tag in item]

    return return_tags


def get_results(tag):

    for key in answers.keys():
        for i in range(0, len(answers.get(key))):
            if tag == answers.get(key)[i]):
                score_update(tag)


'''
try something like: filter(get_results(), query_tags()) to get single
result 'True' and answers[key] name to update score
'''
def array_answers():  # used to compare result with client answers

    answers_list = [tag for values in answers.values() for tag in values]
      #  answer_list = iter(list(answers.values())); for a,b,c,d in answer_list: print(a,b,c,d)
    return answers_list


def score_update(tag):

    for key in list(iter(answers.keys())):

        if key.endswith('yes'):
            result[key] += 5
        elif key.endswith('some'):
            result[key] += 3
        else:
            return


def check_tag(cust_tag, target_tag):
    if cust_tag == target_tag:
        score_update(target_tag)
    else:
        return


def iterate():
    cust_tag = query_tags()
    for tag in cust_tag:
        for answer in answers.values():
            for ans in answer:
                check_tag(tag, ans)


if (infusionsoft.cfgCon("insert account name")):

    contact_tags = infusionsoft.ContactService(load, contact_id, ContactGroup)

    for tags in contact_tags:
        get_results(tags)


print ('highest score: ', highest_score)


for results in comparison[results]:
    if (results == highest_score and final_result is None):
        final_result[results] = results

max(iter(results.values()))

print ('<br> Final Result: ', final_result)
print ('<br>Tag Final Result ', condition_tag[final_result])
print ('<br><br>Raw reference data : <br><pre>')
print(results)


data = (('assessment_type' , 'insert assessment type name'),
                ('assessmentt_option0', ucfirst(final_result),
                ('assessment_score', highest_score),
                ('assessment_score_condition1', results[tinnitus][scores]),
                ('assessment_score_condition2', results[hearing][scores]),
                ('assessment_score_condition3', results[dizziness][scores]),
                ('assessment_score_condition4', results[hyperacusis][scores]),
                ('assessment_score_condition5', results[blockedear][scores])
              )

  # infusionsoft.updateCon(contact_id, data)
  # infusionsoft.grpAssign(contact_id, condition_tag[final_result])
  # print(contact_id)
  # print(condition_tag[final_result])
