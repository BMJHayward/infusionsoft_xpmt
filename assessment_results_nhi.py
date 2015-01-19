from infusionsoft.library import  Infusionsoft
infusionsoft = Infusionsoft( soundtherapy , insert_api_key )

# these 4 digit numbers correspond to tag id for answer to each assessment question in Infusionsoft form
# python probably doesn't like doing arrays like this, we'll find out, or use arrary library or numpy.ndarray
# current approach using dicts looks like it has potential

tinnitus_yes = [ 1796, 1826, 1856, 1886 ]
tinnitus_no = [ 1800, 1830, 1860, 1890 ]
tinnitus_sometimes = [ 1798, 1828, 1858, 1888 ]
tinnitus = { 'yes' : tinnitus_yes, 'no' : tinnitus_no, 'sometimes' : tinnitus_sometimes }

hearing_yes = [ 1808, 1838, 1868, 1898  ]
hearing_no = [ 1812, 1842, 1872, 1902 ]
hearing_sometimes = [ 1810, 1840, 1870, 1900 ]
hearing = { 'yes' : hearing_yes, 'no' : hearing_no, 'sometimes' : hearing_sometimes }

hyperacusis_yes = [ 1802, 1832, 1862, 1892 ]
hyperacusis_no = [ 1806, 1836, 1866, 1896 ]
hyperacusis_sometimes = [ 1804, 1834, 1864, 1894 ]
hyperacusis = { 'yes' : hyperacusis_yes, 'no' : hyperacusis_no, 'sometimes' : hyperacusis_sometimes }

dizziness_yes = [ 1814, 1844, 1874, 1904 ]
dizziness_no = [ 1818, 1848, 1878, 1908 ]
dizziness_sometimes = [ 1816, 1846, 1876, 1906 ]
dizziness = { 'yes' : dizziness_yes, 'no' : dizziness_no, 'sometimes' : dizziness_sometimes }

blockear_yes = [ 1820, 1850, 1880, 1910  ]
blockear_no = [ 1824, 1854, 1884, 1914 ]
blockear_sometimes = [ 1822, 1852, 1882, 1912 ]
blockear    = { 'yes' : blockear_yes, 'no' : blockear_no, 'sometimes' : blockear_sometimes }

questionnaire = { 'tinnitus' : tinnitus, 'hearing' : hearing, 'hyperacusis' : hyperacusis, 'dizziness' : dizziness, 'blockear' : blockear }

tag_result = { "tinnitus" : 2278, "hyperacusis" : 2280, "hearing" : 2282,  "dizziness" : 2284, "blockear" : 2286 }

def query_tags ( contact_id ):

    returnFields = [ "GroupId" ]
    query = { "ContactID": contact_id }
    tags = infusionsoft.DataService( "ContactGroupAssign", 100, 0, query, returnFields )

    for tag in tags:
        return_tags = tags[ tag ]

    return return_tags # could we just return tags from 3 lines ago? DataService.query returns as an array anyway

def get_results ( tag_id ):
    # put function code here
    for results in questionnaire:
        for answers in results:
            for tags in answers:
                if tags == tag_id: pass


if (infusionsoft.cfgCon("soundtherapy"))

    #this does all the sorting, i think
    mcontact_tags = infusionsoft.ContactService( load, contact_id, ContactGroup )

    for tags in contact_tags:
        get_results( tags )

print ( 'highest score: ' , highest_score )

for results in comparison[ results]:
    if (results == highest_score && if  final_result == NULL):
        final_result[ results ] = results

print ('<br> Final Result: ' . final_result )
print ('<br>Tag Final Result ' . tag_result[ final_result ])
print ('<br><br>Raw reference data : <br><pre>')
print( results )

data = (('assessment_type' , 'Natural Hearing Improvement Assessment'),
                ('assessmentt_option0' , ucfirst( final_result ), #'ucfirrst is a PHP function, TODO: find its equivalent
                ('assessment_score' , highest_score ),
                ('assessment_score_condition1' , results[ tinnitus ][ scores ]),
                ('assessment_score_condition2' , results[ hearing ][ scores ]),
                ('assessment_score_condition3' , results[ dizziness ][ scores ]),
                ('assessment_score_condition4' , results[ hyperacusis ][ scores ]),
                ('assessment_score_condition5' , results[ blockedear ][ scores ])
              )

infusionsoft.updateCon( contact_id, data)
infusionsoft.grpAssign( contact_id, tag_result[ final_result ])
print ( contact_id )
print(  tag_result[ final_result ] )
