from __future__ import unicode_literals

from django.utils.xmlutils import SimplerXMLGenerator
from django.utils.six.moves import StringIO
from django.utils.encoding import smart_text
from django.utils.encoding import smart_unicode
from rest_framework.renderers import BaseRenderer


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

        def render(self, data, fields=None, tabledescription=None):
            """
            parameters:
              data = list of Python dictionaries (one for each row)
              fields = optional list of field definitions; MUST contain a unique 'name' key
                       e.g. field = [ {'name': 'ra', 'ID': 'ra', 'datatype': 'float'},
                                      {'name': 'de', 'ID': 'de', 'datatype': 'float'}
                                    ]
              tabledescription = optional free text for table DESCRIPTION element
            """

            if data is None:
                return  ''
            # TODO: should return empty table instead, but then it's not so easy
            # to get the field definitions !
        
            stream = StringIO()
            xml = SimplerXMLGenerator(stream, self.charset)

            xml.startDocument()

            # add votable magic
            xml.startElement("VOTABLE", {'version': self.version, 'xmlns': self.xmlns, 'xmlns:xsi': self.xmlns_xsi})

            xml.startElement("RESOURCE", {})    # possible attribute: "name"
            xml.startElement("TABLE", {})    # possible attribute: "name"
            

            # table DESCRIPTION
            if tabledescription is not None:
                xml.startElement("DESCRIPTION", {})
                xml.characters(smart_text(tabledescription))
                xml.endElement("DESCRIPTION")
            # GROUP, with children: PARAM and FIELDref
            #xml.startElement("GROUP", {})
            #if tabledescription is not None:
            #    xml.characters(smart_text(tabledescription))
            #xml.endElement("GROUP")
            
            # PARAM and FIELD definitions with name, ID, ucd, datatype, width, precision, unit
            # and possible DESCRIPTION as child
            xml.startElement("PARAM", {'url': '/protocols/', 'datatype': 'char'})
            xml.endElement("PARAM")
            
            # define one field for each column:
            # assume, that all rows have the same columns (even if empty value),
            # and that all fields are sorted in the same way for each row,
            # so can use the first row to determine the field names, datatypes etc.
            fieldnames = []
            if fields is not None:
                fieldnames = [f['name'] for f in fields]

            for key, value in data[0].items():
                # create dict of FIELD attributes based on available information
                # Note: ID *must* be unique, name should be unique in FIELD attributes of VOTable
                
                field = {}
                if key in fieldnames:
                    field = [f for f in fields if f['name'] == key][0]

                # 'name' is a required key in provided fields-dict
                if 'name' not in field:
                    field['name'] = key
        
                if 'ID' not in field:
                    field['ID'] = key

                if 'datatype' not in field:
                    try:
                        vodatatype = datatypes[type(data)]
                    except:
                        vodatatype = 'char'

                    field['datatype'] = vodatatype

                # more possible attributes: unit, ucd, arraysize, width, precision
                # need to be provided by fields-dictionary or won't be used at all

                # extract description from field-dictionary, since it will be a child-element:
                fielddescription = None
                if 'description' in field:
                    fielddescription = field['description']
                    # remove from field-dict:
                    field.pop('description', None)

                xml.startElement("FIELD", field)
                if 'fielddescription' in field:
                    xml.startElement("DESCRIPTION", {})
                    xml.characters(smart_text(fielddescription))
                    xml.endElement("DESCRIPTION")
                xml.endElement("FIELD")

            # DATA element
            xml.startElement("DATA", {})
            # TABLEDATA element
            xml.startElement("TABLEDATA", {})

            # TR/TD for rows and data fields
            if data is not None:
                self.votable_data(xml, data)
            #self._to_xml(xml, data)

            xml.endElement("TABLEDATA")
            xml.endElement("DATA")
            xml.endElement("TABLE")
            xml.endElement("RESOURCE")
            xml.endElement("VOTABLE")
            xml.endDocument()

            return stream.getvalue()

        def votable_data(self, xml, data):
            # not working yet for nested votables!!
            #if hasattr(data, '__iter__'):
            #xml.startElement("DATA", {})
            #xml.startElement("TABLEDATA", {})

            for row in data:
                xml.startElement('TR', {})

                for key, value in row.items():
                    xml.startElement('TD', {})
                    xml.characters(smart_unicode(value))
                    xml.endElement('TD')

                xml.endElement('TR')

            #xml.endElement("TABLEDATA")
            #xml.endElement("DATA")
 
