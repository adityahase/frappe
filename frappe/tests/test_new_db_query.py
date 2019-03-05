# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt
from __future__ import unicode_literals

import frappe, unittest

class TestReportview(unittest.TestCase):
	def test_basic(self):
		DocType = frappe.query("DocType")
		query = (DocType
			.select(DocType.autoname, DocType.istable)
			.where(DocType.istable == 1)
			.dump())
		print(query)
