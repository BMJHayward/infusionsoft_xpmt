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

def iterate():
    for condition, answer in questionnaire.items():
        print( "%s gives %s" % (condition, answer ))

x = [ ]
for condition, answer in questionnaire.items():
    x.append((condition, answer))
