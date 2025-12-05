# Copyright (c) 2025, Maxim S and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestKATOTTGTerritoryMarker(FrappeTestCase):
	def setUp(self):
		"""Підготовка тестового середовища"""
		# Видаляємо тестові дані якщо вони існують
		if frappe.db.exists("KATOTTG Territory Marker", "test_active_combat"):
			frappe.delete_doc("KATOTTG Territory Marker", "test_active_combat")

	def tearDown(self):
		"""Очистка після тестів"""
		if frappe.db.exists("KATOTTG Territory Marker", "test_active_combat"):
			frappe.delete_doc("KATOTTG Territory Marker", "test_active_combat")

	def test_create_territory_marker(self):
		"""Тест створення позначки території"""
		marker = frappe.get_doc({
			"doctype": "KATOTTG Territory Marker",
			"title": "Тестова позначка",
			"marker_code": "test_active_combat",
			"color": "#FF0000",
			"description": "Тестовий опис"
		})
		marker.insert()

		self.assertEqual(marker.title, "Тестова позначка")
		self.assertEqual(marker.marker_code, "test_active_combat")
		self.assertEqual(marker.color, "#FF0000")

	def test_invalid_marker_code(self):
		"""Тест валідації коду позначки"""
		marker = frappe.get_doc({
			"doctype": "KATOTTG Territory Marker",
			"title": "Тестова позначка",
			"marker_code": "INVALID-CODE!",  # Невалідний код
		})

		with self.assertRaises(frappe.ValidationError):
			marker.insert()

	def test_unique_marker_code(self):
		"""Тест унікальності коду позначки"""
		marker1 = frappe.get_doc({
			"doctype": "KATOTTG Territory Marker",
			"title": "Позначка 1",
			"marker_code": "test_active_combat",
		})
		marker1.insert()

		marker2 = frappe.get_doc({
			"doctype": "KATOTTG Territory Marker",
			"title": "Позначка 2",
			"marker_code": "test_active_combat",  # Дублікат
		})

		with self.assertRaises(frappe.DuplicateEntryError):
			marker2.insert()
