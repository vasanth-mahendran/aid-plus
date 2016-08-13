# a very simple object for our NDF XML
class NdfDef(object):
    """
    A Class to represent a node in the NDF file
    """
    def __init__(self):
        self.name = None
        self.code = None
        self.id = None
        self.namespace = None
        self.type = None
        self.domain = None
        self.range = None
        self.primitive = None
        self.containsIndex = None
        self.definingConcepts = None
        self.definingRoles = None
        self.pickList = None
        self.properties = None
        self.propertyid = None
        self.inverseName = None
        self.properties_embed = None
        self.kind = None
        self.qualifiers = None
        self.associations = None

    def __str__(self):
        return self.name

    # an internal method to generate a Pymongo object
    def generate_mongodbobj(self):
        mongodb_dict = {}
        if self.name:
            mongodb_dict['name'] = self.name
        if self.code:
            mongodb_dict['code'] = self.code
        if self.id:
            mongodb_dict['id'] = self.id
        if self.namespace:
            mongodb_dict['namespace'] = self.namespace
        if self.type:
            mongodb_dict['type'] = self.type
        if self.domain:
            mongodb_dict['domain'] = self.domain
        if self.range:
            mongodb_dict['range'] = self.range
        if self.primitive:
            mongodb_dict['primitive'] = self.primitive
        if self.containsIndex:
            mongodb_dict['containsIndex'] = self.containsIndex
        if self.definingConcepts:
            mongodb_dict['definingConcepts'] = self.definingConcepts
        if self.definingRoles:
            mongodb_dict['definingRoles'] = self.definingRoles
        if self.pickList:
            mongodb_dict['pickList'] = self.pickList
        if self.propertyid:
            mongodb_dict['propertyid'] = self.propertyid
        if self.inverseName:
            mongodb_dict['inverseName'] = self.inverseName
        if self.kind:
            mongodb_dict['kind'] = self.kind
        if self.qualifiers:
            mongodb_dict['qualifiers'] = self.qualifiers
        if self.properties_embed:
            mongodb_dict['properties'] = self.properties_embed
        if self.associations:
            mongodb_dict['associations'] = self.associations

        return mongodb_dict

