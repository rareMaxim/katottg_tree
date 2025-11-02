# Copyright (c) 2025, Maxim S and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class KATOTTGSettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		cache_ttl: DF.Int
		default_katottg: DF.Link | None
		enable_caching: DF.Check
		enable_fuzzy_search: DF.Check
		enable_import_validation: DF.Check
		excel_column_mapping: DF.Code | None
		import_batch_size: DF.Int
		search_results_limit: DF.Int
	# end: auto-generated types

	def validate(self):
		"""Валідація налаштувань"""
		# Перевірка мапінгу колонок
		if self.excel_column_mapping:
			try:
				import json

				json.loads(self.excel_column_mapping)
			except Exception as e:
				frappe.throw(_("Невалідний JSON в мапінгу стовпців: {0}").format(str(e)))

		# Перевірка розміру пакету
		if self.import_batch_size and self.import_batch_size < 1:
			frappe.throw(_("Розмір пакету імпорту має бути більше 0"))

		# Перевірка TTL кешу
		if self.enable_caching and self.cache_ttl and self.cache_ttl < 1:
			frappe.throw(_("Час життя кешу має бути більше 0"))


@frappe.whitelist()
def get_settings():
	"""Отримати налаштування KATOTTG з кешуванням"""
	settings = frappe.get_cached_doc("KATOTTG Settings")
	return settings


@frappe.whitelist()
def clear_katottg_cache():
	"""Очистити кеш КАТОТТГ"""
	cache_keys = frappe.cache.get_keys("katottg_*")
	for key in cache_keys:
		frappe.cache.delete_key(key)

	frappe.msgprint(_("Кеш КАТОТТГ успішно очищено"))
	return {"success": True}


def get_default_katottg():
	"""Отримати значення КАТОТТГ за замовчуванням з налаштувань"""
	try:
		settings = frappe.get_cached_doc("KATOTTG Settings")
		return settings.default_katottg or "UA23080070010092407"  # Fallback на м. Мелітополь
	except Exception:
		return "UA23080070010092407"


def get_cache_ttl():
	"""Отримати TTL кешу з налаштувань"""
	try:
		settings = frappe.get_cached_doc("KATOTTG Settings")
		if settings.enable_caching:
			return settings.cache_ttl or 3600
	except Exception:
		pass
	return 3600  # За замовчуванням 1 година


def get_excel_column_mapping():
	"""Отримати мапінг стовпців Excel з налаштувань"""
	try:
		import json

		settings = frappe.get_cached_doc("KATOTTG Settings")
		if settings.excel_column_mapping:
			return json.loads(settings.excel_column_mapping)
	except Exception:
		pass

	# Значення за замовчуванням
	return {
		"level_1": 0,
		"level_2": 1,
		"level_3": 2,
		"level_4": 3,
		"level_5": 4,
		"category": 5,
		"title": 6,
	}


def get_import_batch_size():
	"""Отримати розмір пакету для імпорту"""
	try:
		settings = frappe.get_cached_doc("KATOTTG Settings")
		return settings.import_batch_size or 500
	except Exception:
		return 500
