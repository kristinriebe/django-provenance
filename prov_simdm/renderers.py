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

        def render(self, data, votabledef={}, resourcedef={}, tabledef={}, fieldsdef=None, prettyprint=False):
            """
            parameters:
              data = list of Python dictionaries (ordered, one for each row)
              fieldsdef = optional list of field definitions; MUST contain a unique 'name' key
                       e.g. field = [ {'name': 'ra', 'ID': 'ra', 'datatype': 'float'},
                                      {'name': 'de', 'ID': 'de', 'datatype': 'float'}
                                    ]
              votabledef = dictionary of global votable attributes and/or description
                            TODO: include here group, info, param-elements as well!
              tabledef = dictionary of table attributes and/or description
              resourcedef = list of dictionary of resource attributes and/or description
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
            votabledef['version'] = self.version
            votabledef['xmlns'] = self.xmlns
            votabledef['xmlns:xsi'] = self.xmlns_xsi

            xml.startElement("VOTABLE", votabledef)

            # add one or more resources;
            # there can be many resources and they can be nested ...
            # but we just assume that we have only one resource with one table;
            # may be improved in the future
            resourcedescription = None
            if 'description' in resourcedef:
                resourcedescription = resourcedef['description']
                resourcedef.pop('description', None)

            xml.startElement("RESOURCE", resourcedef)
            if resourcedescription:
                xml.startElement("DESCRIPTION", {})
                xml.characters(smart_text(resourcedescription))
                xml.endElement("DESCRIPTION")

            # add table
            tabledescription = None
            if 'description' in tabledef:
                tabledescription = tabledef['description']
                tabledef.pop('description', None)
            
            xml.startElement("TABLE", tabledef)
            if tabledescription:
                xml.startElement("DESCRIPTION", {})
                xml.characters(smart_text(tabledescription))
                xml.endElement("DESCRIPTION")

            # GROUP, with children: PARAM and FIELDref
            #xml.startElement("GROUP", {})
            #xml.endElement("GROUP")

            # PARAM and FIELD definitions with name, ID, ucd, datatype, width, precision, unit
            # and possible DESCRIPTION as child
            #xml.startElement("PARAM", {'url': '/protocols/', 'datatype': 'char'})
            #xml.endElement("PARAM")

            # define one field for each column:
            # assume, that all rows have the same columns (even if empty value),
            # and that all fields are sorted in the same way for each row,
            # so can use the first row to determine the field names, datatypes etc.
            fieldnames = []
            if fieldsdef is not None:
                fieldnames = [f['name'] for f in fieldsdef]

            for key, value in data[0].items():
                # create dict of FIELD attributes based on available information
                # Note: ID *must* be unique, name should be unique in FIELD attributes of VOTable
                
                # first check, if field information is already provided,
                # if not, fill at least name, ID and datatype attributes
                field = {}
                if key in fieldnames:
                    field = [f for f in fieldsdef if f['name'] == key][0]

                field['name'] = key
        
                if 'ID' not in field:
                    field['ID'] = key

                if 'datatype' not in field:
                    try:
                        vodatatype = datatypes[type(data)]
                    except:
                        vodatatype = 'char'

                    field['datatype'] = vodatatype

                if 'arraysize' not in field:
                    field['arraysize'] = '*'

                # more possible attributes: unit, ucd, width, precision
                # need to be provided by fields-dictionary or won't be used at all

                # extract description from field-dictionary, since it will be a child-element:
                fielddescription = None
                if 'description' in field:
                    fielddescription = field['description']
                    # remove from field-dict:
                    field.pop('description', None)

                xml.startElement("FIELD", field)
                if fielddescription is not None:
                    xml.startElement("DESCRIPTION", {})
                    xml.characters(smart_text(fielddescription))
                    xml.endElement("DESCRIPTION")
                xml.endElement("FIELD")

            # add DATA element with TABLEDATA, rows and values
            self.votable_data(xml, data)

            xml.endElement("TABLE")
            xml.endElement("RESOURCE")
            xml.endElement("VOTABLE")
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


        def votable_data(self, xml, data):
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

        def pprint_xml_string(s):
            """Pretty-print an XML string with minidom"""
            parsed = minidom.parse(io.BytesIO(s))
            return parsed.toprettyxml()