from __future__ import unicode_literals

from django.utils.xmlutils import SimplerXMLGenerator
from django.utils.six.moves import StringIO
from django.utils.encoding import smart_text
from django.utils.encoding import smart_unicode
from rest_framework.renderers import BaseRenderer
from django.utils import timezone
import lxml.etree as etree  # for pretty printing xml

class VOTableRenderer(BaseRenderer):
        """
        Takes a list of (ordered) Python dictionaries and 
        returns a VOTable stream
        """

        charset = 'utf-8'

        # namespace declarations
        ns_uws = 'http://www.ivoa.net/xml/UWS/v1.0'
        ns_xlink = 'http://www.w3.org/1999/xlink'
        ns_xsi = 'http://www.w3.org/2001/XMLSchema-instance'
        version = '1.3'

        xmlns_xsi = "http://www.w3.org/2001/XMLSchema-instance"
        xmlns = "http://www.ivoa.net/xml/VOTable/v1.3"
        #xmlns_stc = "http://www.ivoa.net/xml/STC/v1.30"
        # TODO: define more namespaces like for STC, maybe need to get them as params

        comment = "<!--\n"\
                + " !  Generated using Django with SimplerXMLGenerator and VOTableRenderer\n"\
                + " !  at "+str(timezone.now())+"\n"\
                + " !-->\n"

        # mapping from python data types to VOTable datatypes
        # NOTE: float in Python is implemented as double in C 
        # (see https://docs.python.org/2/library/stdtypes.html),
        # thus map all float values to doubles
        datatypes = {
            bool: 'boolean',
            #'':'bit',
            #'':'unsignedByte',
            #'':'short',
            int:'int',
            long:'long',
            str:'char',
            unicode:'unicodeChar',
            float:'float',
            #float':'double',
            complex:'floatComplex',
            #'complex':'doubleComplex'
        }


        def render(self, data, votabledef={}, fieldsdef=None, prettyprint=False):
            """
            parameters:
              data = list of Python dictionaries (ordered, one for each row)
              fieldsdef = optional list of field definitions; MUST contain a unique 'name' key
                       e.g. fieldsdef = [ {'attrs': {'name': 'ra', 'ID': 'ra', 'datatype': 'float'}, 'description': 'This is the right ascension'},
                                          {'attrs': {'name': 'de', 'ID': 'de', 'datatype': 'float'}}
                                        ]
              votabledef = dictionary of global votable attributes and/or description
                            TODO: include here group, info, param-elements as well!
            """

            if data is None:
                return  ''
            # TODO: should return empty table instead, but then it's not so easy
            # to get the field definitions !
        
            stream = StringIO()
            xml = SimplerXMLGenerator(stream, self.charset)

            xml.startDocument()

            # add a comment
            xml._write(self.comment)

            # add votable root element with namespace definitions
            votabledef['VOTABLE']['attrs'] = {}
            votabledef['VOTABLE']['attrs']['version'] = self.version
            votabledef['VOTABLE']['attrs']['xmlns'] = self.xmlns
            votabledef['VOTABLE']['attrs']['xmlns:xsi'] = self.xmlns_xsi
            
            # get field definition from first data row
            fieldsdef = self.get_fields_properties(data[0], fieldsdef)

            # add field definitions to votabledef
            votabledef['VOTABLE']['RESOURCE']['TABLE']['FIELDS'] = fieldsdef
            self.add_xml(xml, votabledef)

            xml.endDocument()

            xml_string = stream.getvalue()

            # make the xml pretty, i.e. use linebreaks and indentation
            # the sax XMLGenerator behind SimpleXMLGenerator does not seem to support this,
            # thus need a library that can do it.
            # xml.dom.minidom is a solution, but has some known bugs/inconvenience (e.g.
            #    it inserts whitespace before text nodes!)
            # lxml.etree is more advanced, thus using this one
            # TODO: since we use lxml anyway, maybe build the whole xml-tree with lxml.etree!
            # NOTE: This removes any possibly existing comments from the xml output!
            if prettyprint is True:
                parsed = etree.fromstring(xml_string)
                pretty_xml = etree.tostring(parsed, pretty_print=True)
                xml_string = pretty_xml

            return xml_string


        def add_xml(self, xml, data):
            if isinstance(data, dict):
                for key, value in data.items():

                    if key.upper() == 'DATA':
                        self.add_data(xml, value)
                    elif key.upper() == 'FIELDS' or key.upper() == 'PARAMS':
                        self.add_xml(xml, value)
                    elif key == 'attrs':
                        # exclude attrs, i.e. do not add as child-element
                        pass
                    else:
                        attrs = {}
                        if 'attrs' in value:
                            attrs = value['attrs']

                        xml.startElement(key.upper(), attrs)
                        self.add_xml(xml, value)
                        xml.endElement(key.upper())
            elif hasattr(data, '__iter__'):
                # This is a list. Lists in VOTables have no wrapper 
                # around them (except for groups, maybe), so add list items directly
                for d in data:

                    self.add_xml(xml, d)
            else:
                xml.characters(smart_unicode(data))


        def add_data(self, xml, data):
            # if there is no data, then DATA-element does not exist => nothing to do!
            if data is None:
                return

            # there is at most one DATA-element per TABLE,
            # thus no need for recursions here
            xml.startElement("DATA", {})

            # use TABLEDATA here exclusively;
            # could in the future also use FITS, BINARY or BINARY2 instead
            xml.startElement("TABLEDATA", {})

            # loop through all data rows and add them,
            # fields MUST be in the same order as for field definitions
            for row in data:
                xml.startElement('TR', {})

                for key, value in row.items():
                    xml.startElement('TD', {})
                    xml.characters(smart_unicode(value))
                    xml.endElement('TD')

                xml.endElement('TR')

            xml.endElement("TABLEDATA")
            xml.endElement("DATA")


        def get_fields_properties(self, datarow, fieldsdef):
            # define one field for each column:
            # assume, that all rows have the same columns (even if empty value),
            # and that all fields are sorted in the same way for each row,
            # so can use the first row to determine the field names, datatypes etc.

            fieldnames = []
            if fieldsdef is not None:
                fieldnames = [f['attrs']['name'] for f in fieldsdef]

            newfieldsdef = [] 
            for key, value in datarow.items():
                # create dict of FIELD attributes based on available information
                # Note: ID *must* be unique, name should be unique in FIELD attributes of VOTable
                
                # first check, if field information is already provided,
                # if not, fill at least name, ID and datatype attributes
                field = {}
                fieldattrs = {}
                if key in fieldnames:
                    field = [f for f in fieldsdef if f['attrs']['name'] == key][0]
                    fieldattrs = field['attrs']
                
                fieldattrs['name'] = key
        
                if 'ID' not in field:
                    fieldattrs['ID'] = key

                if 'datatype' not in field:
                    try:
                        vodatatype = datatypes[type(data)]
                    except:
                        vodatatype = 'char'

                    fieldattrs['datatype'] = vodatatype

                if 'arraysize' not in field:
                    fieldattrs['arraysize'] = '*'

                # more possible attributes: unit, ucd, width, precision
                # need to be provided by fields-dictionary or won't be used at all                

                field['attrs'] = fieldattrs

                newfieldsdef.append({'field': field}) 

            return newfieldsdef