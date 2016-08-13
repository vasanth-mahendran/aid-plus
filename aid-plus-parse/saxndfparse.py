# using sax over the xml.dom library
import xml.sax
import pymongo
# will talk over pymongo at a later date
from pymongo import MongoClient
from bson.objectid import ObjectId

# Grant Load is our model
from databeans.ndf_def import NdfDef

from databeans.ndf_property import NdfProperty

#globals strings for xml
_kind_def = 'kindDef'
_name_space_def = 'namespaceDef'
_role_def = 'roleDef'
_property_def = 'propertyDef'
_association_def = 'associationDef'
_qualifier_def = 'qualifierDef'
_concept_def = 'conceptDef'
_name = 'name'
_code = 'code'
_id = 'id'
_namespace = 'namespace'
_domain = 'domain'
_range = 'range'
_primitive = 'primitive'
_contains_index = 'containsIndex'
_pick_list = 'pickList'
_pick_list_item = 'pickListItem'
_properties = 'properties'
_property = 'property'
_value = 'value'
_defining_roles = 'definingRoles'
_defining_concepts = 'definingConcepts'
_concept = 'concept'
_kind = 'kind'
_role = 'role'
_qualifiers = 'qualifiers'
_qualifier = 'qualifier'
_associations = 'associations'
_association = 'association'

#ndfdef class


class NdfParse(xml.sax.ContentHandler):
    """
    a utility class to parse an xml file containing ndf defs
    usage: python dbutilsbafedxml /path/to/file
    """
    # instance vars
    MONGO_PORT = 3001
    #MONGO_PORT = 27017
    MONGO_HOST = 'localhost'
    db_client = MongoClient(MONGO_HOST, MONGO_PORT)
    #drug_db = db_client.drug_db
    drug_db = db_client.meteor
    ndf_drug_fed_collection = drug_db.ndf_drug_fed
    ndf_drug_prop_fed_collection = drug_db.ndf_property_fed
    _current_ndf_def = None
    _current_node = None
    _current_node_contents = ''
    _current_property_list = None
    _current_pick_list = None
    _current_property = None
    _current_parent_property = False
    _current_name_value_property = False
    _current_name_value_qualifier = False
    _current_name_value_role = False
    _current_name_value_association = False
    _current_qualifier = None
    _current_qualifiers = None
    _current_roles = None
    _current_role = None
    _current_concepts_list = None
    _current_associations = None
    _current_association = None

    def __init__(self):
        xml.sax.ContentHandler.__init__(self)

    # event triggered for every open tag
    def startElement(self, name, attrs):
        self.generatedef('start', name=name)

    # event triggered for every close tag
    def endElement(self, name):
        self.generatedef('end', name=name)
        self._current_node_contents = ''

    def characters(self, content):
        self._current_node_contents += content

    # method to handle parsing nodes
    def generatedef(self, position, name):

        if name in [_kind_def,_name_space_def,_role_def,_property_def,_association_def,_qualifier_def,_concept_def] and position == 'start':
            self._current_ndf_def = NdfDef()
            self._current_ndf_def.type = name
        elif name in [_kind_def,_name_space_def,_role_def,_property_def,_association_def,_qualifier_def,_concept_def] and position == 'end':
            # insert
            _property_ids = []
            '''if not self._current_ndf_def.properties == None:
                for property in self._current_ndf_def.properties:
                    _property_id = self.ndf_drug_prop_fed_collection.insert(property.generate_mongodbobj())
                    _property_ids.append(_property_id)
                self._current_ndf_def.propertyid = _property_ids'''''''''

            if not self._current_ndf_def.properties == None:
                for property in self._current_ndf_def.properties:
                    _property_ids.append(property.generate_mongodbobj())
                self._current_ndf_def.properties_embed = _property_ids
            _doc_id = self.ndf_drug_fed_collection.insert(self._current_ndf_def.generate_mongodbobj())
            self._current_ndf_def = None

        if name == _name and position == 'start':
            self._current_node = _name
        elif name == _name and position == 'end':
            if self._current_name_value_qualifier == True:
                self._current_qualifier['name'] = self._current_node_contents.strip()
            elif self._current_name_value_property == True:
                self._current_property.name = self._current_node_contents.strip()
            elif self._current_name_value_role == True:
                self._current_role['name'] = self._current_node_contents.strip()
            elif self._current_name_value_association == True:
                self._current_association['name'] = self._current_node_contents.strip()
            else:
                #print('name----', self._current_node_contents.strip().lower())
                self._current_ndf_def.name = self._current_node_contents.strip().lower()

        if name == _code and position == 'start':
            self._current_node = _code
        elif name == _code and position == 'end':
            self._current_ndf_def.code = self._current_node_contents.strip()

        if name == _id and position == 'start':
            self._current_node = _id
        elif name == _id and position == 'end':
            self._current_ndf_def.id = self._current_node_contents.strip()

        if name == _namespace and position == 'start':
            self._current_node = _namespace
        elif name == _namespace and position == 'end':
            self._current_ndf_def.namespace = self._current_node_contents.strip()

        if name == _domain and position == 'start':
            self._current_node = _domain
        elif name == _domain and position == 'end':
            self._current_ndf_def.domain = self._current_node_contents.strip()

        if name == _range and position == 'start':
            self._current_node = _range
        elif name == _range and position == 'end':
            self._current_ndf_def.range = self._current_node_contents.strip()

        if name == _pick_list and position == 'start':
            self._current_node = _pick_list
            self._current_pick_list = []
        elif name == _pick_list and position == 'end':
            self._current_ndf_def.pickList = self._current_pick_list
            self._current_pick_list = None

        if name == _pick_list_item and position == 'start':
            self._current_node = _pick_list_item
        elif name == _pick_list_item and position == 'end':
            self._current_pick_list.append(self._current_node_contents.strip())

        if name == _primitive and position == 'start':
            self._current_node = _primitive
        elif name == _primitive and position == 'end':
            self._current_ndf_def.primitive = self._current_node_contents.strip()

        if name == _contains_index and position == 'start':
            self._current_node = _contains_index
        elif name == _contains_index and position == 'end':
            self._current_ndf_def.containsIndex = self._current_node_contents.strip()

        if name == _properties and position == 'start':
            self._current_node = _properties
            self._current_property_list = []
        elif name == _properties and position == 'end':
            self._current_ndf_def.properties = self._current_property_list
            self._current_property_list = None

        if name == _property and position == 'start':
            self._current_node = _property
            self._current_name_value_property = True
            self._current_property = NdfProperty()
        elif name == _property and position == 'end':
            self._current_property_list.append(self._current_property)
            self._current_name_value_property = False
            self._current_property = None

        if name == _value and position == 'start':
            self._current_node = _value
        elif name == _value and position == 'end':
            if self._current_name_value_qualifier == True:
                self._current_qualifier['value'] = self._current_node_contents.strip()
            elif self._current_name_value_property == True:
                self._current_property.value = self._current_node_contents.strip()
            elif self._current_name_value_role == True:
                self._current_role['value'] = self._current_node_contents.strip()
            elif self._current_name_value_association == True:
                self._current_association['value'] = self._current_node_contents.strip()

        if name == _qualifiers and position == 'start':
            self._current_node = _qualifiers
            self._current_qualifiers = []
        elif name == _qualifiers and position == 'end':
            if self._current_name_value_property == True:
                self._current_property.qualifiers = self._current_qualifiers
            elif self._current_name_value_association == True:
                self._current_association['qualifiers'] = self._current_qualifiers
            self._current_qualifiers = None

        if name == _qualifier and position == 'start':
            self._current_node = _qualifier
            self._current_qualifier = {}
            self._current_name_value_qualifier = True
        elif name == _qualifier and position == 'end':
            if self._current_qualifier:
                self._current_qualifiers.append(self._current_qualifier)
            self._current_qualifier = None
            self._current_name_value_qualifier = False

        if name == _defining_roles and position == 'start':
            self._current_node = _defining_roles
            self._current_roles = []
        elif name == _defining_roles and position == 'end':
            self._current_ndf_def.definingRoles = self._current_roles
            self._current_roles = None

        if name == _role and position == 'start':
            self._current_node = _role
            self._current_role = {}
            self._current_name_value_role = True
        elif name == _role and position == 'end':
            if self._current_role:
                self._current_roles.append(self._current_role)
            self._current_role = None
            self._current_name_value_role = False

        if name == _defining_concepts and position == 'start':
            self._current_node = _defining_concepts
            self._current_concepts_list = []
        elif name == _defining_concepts and position == 'end':
            self._current_ndf_def.definingConcepts = self._current_concepts_list
            self._current_concepts_list = None

        if name == _concept and position == 'start':
            self._current_node = _concept
        elif name == _concept and position == 'end':
            self._current_concepts_list.append(self._current_node_contents.strip())

        if name == _associations and position == 'start':
            self._current_node = _associations
            self._current_associations = []
        elif name == _associations and position == 'end':
            self._current_ndf_def.associations = self._current_associations
            self._current_associations = None

        if name == _association and position == 'start':
            self._current_node = _association
            self._current_association = {}
            self._current_name_value_association = True
        elif name == _association and position == 'end':
            self._current_associations.append(self._current_association)
            self._current_name_value_association = False