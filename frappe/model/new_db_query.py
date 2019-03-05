# Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe

""""

SELECT name ==> User.select()
User = frappe.query("User")

SELECT name, age ==> User.select(User.name, User.age)

SELECT name, age ... WHERE age ==> User.select(User.name, User.dat_of_birth).where(User.age == 10)

"""

class QueryMeta():
    def __init__(self, doctype):
        self.meta = frappe.get_meta(doctype)
        self.condition = []
        self.fields = []

    def select(self, *fields):
        self.fields = fields
        return self

    def where(self, condition):
        self.condition = condition
        return self

    def __getattr__(self, field_name):
        qf = self.meta.get_field(field_name)
        if qf:
            return QueryField(qf)
        raise Exception("Invalid field {}".format(field_name))

    def dump(self):
        print([x.df.fieldname for x in self.fields])
        print(self.condition)

class QueryField():
    def __init__(self, df):
        self.df = df

    def __eq__(self, other):
        return [self.df.fieldname, "=", other]
