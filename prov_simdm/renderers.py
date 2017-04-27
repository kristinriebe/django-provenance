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


        def render(self, data, votable_meta={}, prettyprint=False):
            """
            parameters:
              data = list of Python dictionaries (ordered, one for each row)
              votable_meta = dictionary of attributes and/or descriptions etc., also may include
                            field definitions;
                            attributes have to be provided as extra dictionary, e.g. for the fields:
                            e.g. votable_meta['VOTABLE']['RESOURCE']['TABLE']['FIELDS'] =
                                    [ {'FIELD': {'attrs': {'name': 'ra', 'ID': 'ra', 'datatype': 'float'}, 'DESCRIPTION': 'This is the right ascension'}},
                                      {'FIELD': {'attrs': {'name': 'de', 'ID': 'de', 'datatype': 'float'}}
                                    ]
                            TODO: include here group, info, param-elements as well!
            """

            stream = StringIO()
            xml = SimplerXMLGenerator(stream, self.charset)

            xml.startDocument()

            # add a comment
            xml._write(self.comment)

            # add namespace definitions, if not there already
            if 'VOTABLE' not in votable_meta:
                votable_meta['VOTABLE'] = {}
            attrs = {}
            if 'attrs' in votable_meta['VOTABLE']:
                attrs = votable_meta['VOTABLE']['attrs']

            if 'version' not in attrs:
                attrs['version'] = self.version
            if 'xmlns' not in attrs:
                attrs['xmlns'] = self.xmlns
            if 'xmlns:xsi' not in attrs:
                attrs['xmlns:xsi'] = self.xmlns_xsi
            votable_meta['VOTABLE']['attrs'] = attrs

            # construct the nested dictionary for VOTABLE structure, if not yet existing
            if 'RESOURCE' not in votable_meta['VOTABLE']:
                votable_meta['VOTABLE']['RESOURCE'] = {}

            if 'TABLE' not in votable_meta['VOTABLE']['RESOURCE']:
                votable_meta['VOTABLE']['RESOURCE']['TABLE'] = {}

            if 'FIELDS' not in votable_meta['VOTABLE']['RESOURCE']['TABLE']:
                votable_meta['VOTABLE']['RESOURCE']['TABLE']['FIELDS'] = {}

            # fill missing field definitions by inspecting first data row
            if data is not None:
                fields = votable_meta['VOTABLE']['RESOURCE']['TABLE']['FIELDS']
                fields = self.get_fields_properties(data[0], fields)
                votable_meta['VOTABLE']['RESOURCE']['TABLE']['FIELDS'] = fields


            # add data-node to votable dictionary:
            votable_meta['VOTABLE']['RESOURCE']['TABLE']['DATA'] = data

            # convert to proper xml VOTable
            self.add_node(xml, votable_meta)

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


        def add_node(self, xml, data):
            if isinstance(data, dict):
                # Because the order of items in the votable dictionary actually
                # matters, we need to make sure that we go through these
                # items in the correct order.
                # Thus, first define list of possible keys and then compare:

                votable_keys = ['attrs', 'VOTABLE', 'DESCRIPTION', 'PARAMS', 'GROUPS', 'VALUES', 'LINK', 'TABLE', 'RESOURCE', 'FIELDS', 'FIELD', 'DATA', 'INFO', 'MIN', 'MAX', 'OPTION']

                for key in votable_keys:
                    if key in data:
                        value = data[key]

                        if key.upper() == 'DATA':
                            self.add_data(xml, value)
                        elif key.upper() == 'FIELDS' or key.upper() == 'PARAMS':
                            self.add_node(xml, value)
                        elif key.lower() == 'attrs':
                            # exclude attrs, i.e. do not add as child-element
                            pass
                        else:
                            attrs = {}
                            if 'attrs' in value:
                                attrs = value['attrs']

                            xml.startElement(key.upper(), attrs)
                            self.add_node(xml, value)
                            xml.endElement(key.upper())
            elif hasattr(data, '__iter__'):
                # This is a list. Lists in VOTables have no wrapper
                # around them (except for groups, maybe), so add list items directly
                for d in data:
                    self.add_node(xml, d)
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
            #
            # TODO: rewrite, so this returns everything from the datarow,
            # merge with provided fieldsdef in a second step in another function

            fieldnames = []
            if fieldsdef is not None:
                fieldnames = [f['FIELD']['attrs']['name'] for f in fieldsdef]

            newfieldsdef = []
            for key, value in datarow.items():
                # create dict of FIELD attributes based on available information
                # Note: ID *must* be unique, name should be unique in FIELD attributes of VOTable

                # first check, if field information is already provided,
                # if not, fill at least name, ID and datatype attributes
                field = {}
                fieldattrs = {}
                if key in fieldnames:
                    field = [f['FIELD'] for f in fieldsdef if f['FIELD']['attrs']['name'] == key][0]
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

                newfieldsdef.append({'FIELD': field})

            return newfieldsdef


class VosiTablesRenderer(BaseRenderer):
        """
        Takes ... and
        returns an xmlstream for VOSI tables/ endpoint
        """

        charset = 'utf-8'

        # namespace declarations
        ns_vosi = 'http://www.ivoa.net/xml/VOSITables/v1.0'
        ns_vs = 'http://www.ivoa.net/xml/VODataService/v1.1'
        ns_xsi = "http://www.w3.org/2001/XMLSchema-instance"
        version = '1.1'

        comment = "<!--\n"\
                + " !  Generated using Django with SimplerXMLGenerator\n"\
                + " !  at "+str(timezone.now())+"\n"\
                + " !-->\n"


        def render(self, data, detaillevel='max', prettyprint=False):
            """
            parameters:
              data = result from django query set, from TAP_SCHEMA_tables
              detaillevel = max or min, level of detail as specified in VOSI 1.1 -- ignored for now
              prettyprint = flag for pretty printing the xml output (including whitespace and linebreaks)
            """

            stream = StringIO()
            xml = SimplerXMLGenerator(stream, self.charset)

            xml.startDocument()

            # add a comment
            xml._write(self.comment)

            # add namespace definitions
            nsattrs = {}
            nsattrs['version'] = self.version
            nsattrs['xmlns:vosi'] = self.ns_vosi
            nsattrs['xmlns:xsi'] = self.ns_xsi
            nsattrs['xmlns:vs'] = self.ns_vs

            # add root node
            xml.startElement('vosi:tableset', nsattrs)

            # add schema nodes, tables and columns etc.
            schema_name_prev = ''
            for row in data:
                schema_name = row['schema_name']
                table_name = row['table_name']
                if schema_name.lower() != schema_name_prev.lower():
                    if schema_name_prev != '':
                        xml.endElement('schema')
                    schema_name_prev = schema_name
                    xml.startElement('schema', {})
                    xml.startElement('name', {})
                    xml.characters(smart_unicode(schema_name))
                    xml.endElement('name')

                xml.startElement('table', {})
                xml.startElement('name', {})
                xml.characters(smart_unicode(table_name))
                xml.endElement('name')
                xml.endElement('table')

            xml.endElement('schema')

            xml.endElement('vosi:tableset')

            xml.endDocument()


            xml_string = stream.getvalue()

            # make the xml pretty, i.e. use linebreaks and indentation
            # the sax XMLGenerator behind SimpleXMLGenerator does not seem to support this,
            # thus need a library that can do it.
            # TODO: since we use lxml anyway, maybe build the whole xml-tree with lxml.etree!
            # NOTE: This removes any possibly existing comments from the xml output!
            if prettyprint is True:
                parsed = etree.fromstring(xml_string)
                pretty_xml = etree.tostring(parsed, pretty_print=True)
                xml_string = pretty_xml

            return xml_string


class VosiTableRenderer(BaseRenderer):
        """
        Takes table and column data and
        returns an xmlstream for VOSI table/ endpoint
        """

        charset = 'utf-8'

        # namespace declarations
        ns_vosi = 'http://www.ivoa.net/xml/VOSITables/v1.0'
        ns_vs = 'http://www.ivoa.net/xml/VODataService/v1.1'
        ns_xsi = "http://www.w3.org/2001/XMLSchema-instance"
        version = '1.1'

        comment = "<!--\n"\
                + " !  Generated using Django with SimplerXMLGenerator\n"\
                + " !  at "+str(timezone.now())+"\n"\
                + " !-->\n"


        def render(self, data, prettyprint=False):
            """
            parameters:
              data = result from django query set, from TAP_SCHEMA_tables
              prettyprint = flag for pretty printing the xml output (including whitespace and linebreaks)
            """

            stream = StringIO()
            xml = SimplerXMLGenerator(stream, self.charset)

            xml.startDocument()

            # add a comment
            xml._write(self.comment)

            # add namespace definitions
            nsattrs = {}
            nsattrs['version'] = self.version
            #nsattrs['encoding'] = "UTF-8"
            nsattrs['xmlns:vosi'] = self.ns_vosi
            #nsattrs['xmlns:xsi'] = self.ns_xsi
            #nsattrs['xmlns:vs'] = self.ns_vs

            # add root node
            xml.startElement('vosi:table', nsattrs)

            # add schema nodes, tables and columns etc.
            table_name = data[0]['table_name']
            xml.startElement('table', {})
            xml.startElement('name', {})
            xml.characters(smart_unicode(table_name))
            xml.endElement('name')
            for row in data:
                col_name = row['column_name']
                xml.startElement('column', {})

                xml.startElement('name', {})
                xml.characters(smart_unicode(col_name))
                xml.endElement('name')

                xml.startElement('description', {})
                xml.characters(smart_unicode(row['description']))
                xml.endElement('description')

                xml.startElement('datatype', {})
                xml.characters(smart_unicode(row['datatype']))
                xml.endElement('datatype')

                xml.endElement('column')

            xml.endElement('table')

            xml.endElement('vosi:table')

            xml.endDocument()

            xml_string = stream.getvalue()


            # make the xml pretty, i.e. use linebreaks and indentation
            # the sax XMLGenerator behind SimpleXMLGenerator does not seem to support this,
            # thus need a library that can do it.
            # TODO: since we use lxml anyway, maybe build the whole xml-tree with lxml.etree!
            # NOTE: This removes any possibly existing comments from the xml output!
            if prettyprint is True:
                parsed = etree.fromstring(xml_string)
                pretty_xml = etree.tostring(parsed, pretty_print=True)
                xml_string = pretty_xml

            return xml_string

