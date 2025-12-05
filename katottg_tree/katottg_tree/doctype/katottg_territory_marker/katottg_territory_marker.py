# Copyright (c) 2025, Maxim S and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class KATOTTGTerritoryMarker(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		color: DF.Color | None
		description: DF.SmallText | None
		marker_code: DF.Data
		title: DF.Data
	# end: auto-generated types

	def validate(self):
		"""Валідація даних перед збереженням"""
		self.validate_marker_code()

	def validate_marker_code(self):
		"""Валідація коду позначки"""
		if not self.marker_code:
			frappe.throw(_("Код позначки є обов'язковим"))

		# Код має містити лише латинські літери, цифри та підкреслення
		import re
		if not re.match(r"^[a-z0-9_]+$", self.marker_code):
			frappe.throw(
				_("Код позначки має містити лише малі латинські літери, цифри та підкреслення")
			)


@frappe.whitelist()
def get_territory_markers():
	"""
	Отримати всі типи позначок територій.
	Використовується для вибору в UI.
	"""
	return frappe.get_all(
		"KATOTTG Territory Marker",
		fields=["name", "title", "marker_code", "color", "description"],
		order_by="title asc",
	)


@frappe.whitelist()
def get_marker_by_code(marker_code: str):
	"""
	Отримати позначку за кодом.
	"""
	if not marker_code:
		return None

	markers = frappe.get_all(
		"KATOTTG Territory Marker",
		filters={"marker_code": marker_code},
		fields=["name", "title", "marker_code", "color", "description"],
		limit=1,
	)
	return markers[0] if markers else None
