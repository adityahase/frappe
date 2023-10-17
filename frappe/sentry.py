# Copyright (c) 2022, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE
from datetime import datetime

import rq
from sentry_sdk import configure_scope
from sentry_sdk.hub import Hub
from sentry_sdk.integrations import Integration
from sentry_sdk.tracing_utils import record_sql_queries
from sentry_sdk.utils import capture_internal_exceptions

import frappe
from frappe.database.database import Database


class FrappeIntegration(Integration):
	identifier = "frappe"

	@staticmethod
	def setup_once():
		real_connect = Database.connect
		real_sql = Database.sql

		def sql(self, query, values=None, *args, **kwargs):
			hub = Hub.current

			if not self._conn:
				self.connect()

			with record_sql_queries(
				hub, self._cursor, query, values, paramstyle="pyformat", executemany=False
			):
				return real_sql(self, query, values or (), *args, **kwargs)

		def connect(self):
			hub = Hub.current
			with capture_internal_exceptions():
				hub.add_breadcrumb(message="connect", category="query")

			with hub.start_span(op="db", description="connect"):
				return real_connect(self)

		Database.connect = connect
		Database.sql = sql


def set_sentry_context():
	with configure_scope() as scope:
		if job := rq.get_current_job():
			kwargs = job._kwargs
			transaction_name = kwargs["method"]
			context = frappe._dict({"scheduled": False, "wait": 0})
			if "run_scheduled_job" in transaction_name:
				transaction_name = kwargs.get("kwargs", {}).get("job_type", "")
				context.scheduled = True

			waitdiff = datetime.utcnow() - job.enqueued_at
			context.uuid = job.id
			context.wait = waitdiff.total_seconds()

			scope.set_extra("job", context)
		else:
			if frappe.form_dict.cmd:
				transaction_name = f"/api/method/{frappe.form_dict.cmd}"
			else:
				transaction_name = frappe.request.path

		scope.transaction.name = transaction_name

		scope.user = {"id": frappe.session.user, "email": frappe.session.user}


def before_send(event, hint):
	if event.get("logger", "") == "CSSUTILS":
		return None
	return event
