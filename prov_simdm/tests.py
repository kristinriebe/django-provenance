from django.test import TestCase
#from django.utils import unittest
from prov_simdm.models import Protocol
from prov_simdm.renderers import VOTableRenderer
from django.utils import timezone
from django.http import HttpResponse


# TODO: Tests for VOTableRenderer:
# provide fields (incomplete), still get correct names for all fields etc.
#  (need to use some example data for this!)
# provide tabledescription => votable contains description-element

class VOTableRendererTestCase(TestCase):
    """
    Tests specific to VOTableRenderer
    """

    def setUp(self):
        Protocol.objects.create(name="AHF", id="cs:ahf", description="AMIGA halo finder")
        Protocol.objects.create(name="FOF", id="cs:fof", description="Friends-of-Friends cluster finder")

    def test_votable_simple(self):
        protocols = Protocol.objects.order_by('id')
        data = protocols.values('name','id','description')

        votable = VOTableRenderer().render(data, prettyprint=False)

        expected_votable = '<?xml version="1.0" encoding="utf-8"?>\n' \
            + '<!--\n'\
            + ' !  Generated using Django with SimplerXMLGenerator and VOTableRenderer\n'\
            + ' !  at XXXX-XX-XX 08:26:20.XXXXXX\n'\
            + ' !-->\n'\
            + '<VOTABLE version="1.3" xmlns="http://www.ivoa.net/xml/VOTable/v1.3"><RESOURCE><TABLE>'\
            + '<FIELD datatype="char" name="description" arraysize="*" ID="description"></FIELD>'\
            + '<FIELD datatype="char" name="name" arraysize="*" ID="name"></FIELD>'\
            + '<FIELD datatype="char" name="id" arraysize="*" ID="id"></FIELD>'\
            + '<DATA><TABLEDATA><TR><TD>AMIGA halo finder</TD><TD>AHF</TD><TD>cs:ahf</TD></TR>'\
            + '<TR><TD>Friends-of-Friends cluster finder</TD><TD>FOF</TD><TD>cs:fof</TD></TR>'\
            + '</TABLEDATA></DATA></TABLE></RESOURCE></VOTABLE>'

        # strings must be equal, except for the datetime; thus find position of date-time-string
        # and compare everything before and after that
        ibegindate = expected_votable.find('XXXX')
        ienddate = expected_votable.rfind('XXXX')+4
        self.assertEqual(votable[0:ibegindate], expected_votable[0:ibegindate])
        self.assertEqual(votable[ienddate:], expected_votable[ienddate:])


    def test_votable_emptytable(self):
        data = None
        votable = VOTableRenderer().render(data, prettyprint=False)
        expected_votable = '<?xml version="1.0" encoding="utf-8"?>\n' \
            + '<!--\n'\
            + ' !  Generated using Django with SimplerXMLGenerator and VOTableRenderer\n'\
            + ' !  at XXXX-XX-XX 08:26:20.XXXXXX\n'\
            + ' !-->\n'\
            + '<VOTABLE version="1.3" xmlns="http://www.ivoa.net/xml/VOTable/v1.3"><RESOURCE><TABLE></TABLE></RESOURCE></VOTABLE>'

        ibegindate = expected_votable.find('XXXX')
        ienddate = expected_votable.rfind('XXXX')+4
        self.assertEqual(votable[0:ibegindate], expected_votable[0:ibegindate])
        self.assertEqual(votable[ienddate:], expected_votable[ienddate:])
