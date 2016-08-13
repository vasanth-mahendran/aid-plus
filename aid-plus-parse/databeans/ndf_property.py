# a very simple object for our property node in NDF XML
class NdfProperty(object):
    """
    A Class to represent a property node in the NDF file
    """
    def __init__(self):
        self.name = None
        self.value = None
        self.qualifiers = None

    def __str__(self):
        return self.name

    # an internal method to generate a Pymongo object
    def generate_mongodbobj(self):
        mongodb_dict = {"name": self.name, "value": self.value}
        if self.qualifiers:
            mongodb_dict['qualifiers'] = self.qualifiers
        return mongodb_dict