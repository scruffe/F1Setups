class User:
    """A simple employee class"""

    def __init__(self, _id, first, last, tag, uploads, credit, email, premium):
        self.id = _id
        self.first = first
        self.last = last
        self.tag = tag
        self.uploads = uploads
        self.credit = credit
        self.email = email
        self.premium = premium

    @property
    def fullname(self):
        return '{} {}'.format(self.first, self.last)

    def __repr__(self):
        return "Employee('{}', '{}', {}, {})".format(self.first, self.last, self.credit, self.email)
