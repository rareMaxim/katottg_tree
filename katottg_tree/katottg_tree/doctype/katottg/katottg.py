# Copyright (c) 2025, Maxim S and contributors
# For license information, please see license.txt

import re

import frappe
from frappe import _
from frappe.utils.nestedset import NestedSet, rebuild_tree


class KATOTTG(NestedSet):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		category: DF.Data | None
		code: DF.Data
		is_group: DF.Check
		lft: DF.Int
		old_parent: DF.Link | None
		parent_katottg: DF.Link | None
		rgt: DF.Int
		territory_marker: DF.Link | None
		territory_marker_date: DF.Date | None
		title: DF.Data
	# end: auto-generated types

	def validate(self):
		"""Валідація даних перед збереженням"""
		self.validate_code()
		self.validate_category()
		self.validate_hierarchy()

	def validate_code(self):
		"""Валідація коду КАТОТТГ"""
		if not self.code:
			frappe.throw(_("Код КАТОТТГ є обов'язковим"))

		# Код КАТОТТГ має бути у форматі UA + цифри
		if not re.match(r"^UA\d{17}$", self.code):
			frappe.throw(_("Код КАТОТТГ має бути у форматі UA + 17 цифр. Приклад: UA12345678901234567"))

	def validate_category(self):
		"""Валідація категорії КАТОТТГ"""
		valid_categories = ["O", "K", "P", "H", "M", "X", "C", "B"]

		if self.category and self.category not in valid_categories:
			frappe.throw(
				_("Невалідна категорія: {0}. Допустимі значення: {1}").format(
					self.category, ", ".join(valid_categories)
				)
			)

	def validate_hierarchy(self):
		"""Валідація ієрархічної структури"""
		# Перевірка на циклічні залежності
		if self.parent_katottg and self.parent_katottg == self.name:
			frappe.throw(_("Об'єкт не може бути батьківським для самого себе"))

		# Якщо є батьківський об'єкт, він має бути is_group
		if self.parent_katottg:
			parent = frappe.get_cached_value("KATOTTG", self.parent_katottg, "is_group")
			if not parent:
				frappe.throw(
					_("Батьківський об'єкт {0} має бути групою (is_group)").format(self.parent_katottg)
				)

	def on_update(self):
		"""Хук після оновлення документа"""
		super().on_update()
		# Очищаємо кеш для цього об'єкта
		self.clear_cache_for_object()

	def on_trash(self):
		"""Хук перед видаленням документа"""
		super().on_trash()
		# Очищаємо кеш
		self.clear_cache_for_object()

	def clear_cache_for_object(self):
		"""Очистка кешу для конкретного об'єкта"""
		cache_keys = [
			f"katottg_full_path_{self.name}",
			f"katottg_hierarchy_{self.name}",
		]
		for key in cache_keys:
			frappe.cache.delete_key(key)


@frappe.whitelist()
def process_all_nodes():
	"""
	Обробка всіх вузлів дерева КАТОТТГ.
	Перебудовує дерево (lft, rgt значення) для коректної роботи nested set.
	"""
	try:
		frappe.msgprint(_("Розпочато перебудову дерева КАТОТТГ..."))

		# Перебудовуємо дерево
		# В новій версії Frappe rebuild_tree приймає тільки назву DocType
		rebuild_tree("KATOTTG")

		# Очищаємо весь кеш КАТОТТГ
		from katottg_tree.katottg_tree.doctype.katottg_settings.katottg_settings import (
			clear_katottg_cache,
		)

		clear_katottg_cache()

		frappe.db.commit()
		frappe.msgprint(_("Дерево КАТОТТГ успішно перебудовано!"))

		return {"success": True, "message": _("Дерево успішно перебудовано")}

	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(frappe.get_traceback(), "KATOTTG Process All Nodes Error")
		frappe.throw(_("Помилка при перебудові дерева: {0}").format(str(e)))


@frappe.whitelist()
def get_katottg_children(parent=None, is_root=False):
	"""
	Отримати дочірні елементи для конкретного вузла.
	Використовується для lazy loading в tree view.
	"""
	filters = {}

	if is_root:
		filters["parent_katottg"] = ["in", ["", None]]
	elif parent:
		filters["parent_katottg"] = parent
	else:
		return []

	try:
		return frappe.get_all(
			"KATOTTG",
			filters=filters,
			fields=["name", "code", "title", "category", "is_group", "parent_katottg", "territory_marker", "territory_marker_date"],
			order_by="code asc",
		)
	except Exception:
		frappe.log_error(frappe.get_traceback(), "KATOTTG Get Children Error")
		return []
