import numpy

tinnitus_yes = [ 1796, 1826, 1856, 1886 ]
tinnitus_no = [ 1800, 1830, 1860, 1890 ]
tinnitus_sometimes = [ 1798, 1828, 1858, 1888 ]
tinnitus = [ tinnitus_yes,  tinnitus_no,  tinnitus_sometimes ]

hearing_yes = [ 1808, 1838, 1868, 1898  ]
hearing_no = [ 1812, 1842, 1872, 1902 ]
hearing_sometimes = [ 1810, 1840, 1870, 1900 ]
hearing = [ hearing_yes,  hearing_no,  hearing_sometimes ]

hyperacusis_yes = [ 1802, 1832, 1862, 1892 ]
hyperacusis_no = [ 1806, 1836, 1866, 1896 ]
hyperacusis_sometimes = [ 1804, 1834, 1864, 1894 ]
hyperacusis = [ hyperacusis_yes,  hyperacusis_no,  hyperacusis_sometimes ]

dizziness_yes = [ 1814, 1844, 1874, 1904 ]
dizziness_no = [ 1818, 1848, 1878, 1908 ]
dizziness_sometimes = [ 1816, 1846, 1876, 1906 ]
dizziness = [ dizziness_yes,  dizziness_no,  dizziness_sometimes ]

blockear_yes = [ 1820, 1850, 1880, 1910  ]
blockear_no = [ 1824, 1854, 1884, 1914 ]
blockear_sometimes = [ 1822, 1852, 1882, 1912 ]
blockear    = [ blockear_yes,  blockear_no,  blockear_sometimes ]

# questionnaire = [ tinnitus,  hearing,  hyperacusis,  dizziness,  blockear ]
# questionnaire = numpy.array(questionnaire)

questionnaire = { "tinnitus" : tinnitus, "hearing" : hearing, "hyperacusis" : hyperacusis, "dizziness" : dizziness, "blockedear" : blockear }


tag_result = { "tinnitus" : 2278, "hyperacusis" : 2280, "hearing" : 2282,  "dizziness" : 2284, "blockear" : 2286 }


def iterate():
    for x,y,z in questionnaire:
        for i in z:
            print(z[i],"\n")

# eval('questionnaire')
# eval('questionnaire['tinnitus']')

from past import autotranslate
autotranslate('infusionsoft')
import infusionsoft
from infusionsoft.library import Infuionsoft