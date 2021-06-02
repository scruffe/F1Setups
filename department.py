class Department:
    def __init__(self, department_id, name):
        self.name = name
        self.department_id = department_id

    def __repr__(self):
        return "Department('{}', '{}')".format(self.name, self.department_id)