import frappe
from frappe.utils.nestedset import get_ancestors_of


@frappe.whitelist()
def get_default_katottg_hierarchy():
	"""
	Повертає ієрархію для значення за замовчуванням (м. Мелітополя).
	"""
	# ✅ ГОЛОВНЕ ВИПРАВЛЕННЯ:
	# UA23080070010092407 - це код для "м. Мелітополя".
	# Функція get_ancestors_of сама знайде його громаду, район та область.
	default_name = "UA23080070010092407"
	try:
		ancestors = get_ancestors_of("KATOTTG", default_name, order_by="lft asc")
		return [*ancestors, default_name]
	except frappe.DoesNotExistError:
		return []


@frappe.whitelist()
def get_katottg_full_path(name):
	"""
	Повертає повний ієрархічний шлях,
	послідовно піднімаючись по батьківських елементах.
	"""
	if not name:
		return ""

	try:
		path_parts = []
		# Отримуємо початковий документ
		current_doc = frappe.get_doc("KATOTTG", name)

		# Додаємо його назву до шляху
		path_parts.append(current_doc.title)

		# В циклі піднімаємось вгору, поки є батьківські елементи
		while current_doc.parent_katottg:
			# Отримуємо батьківський документ
			current_doc = current_doc.get_parent()
			if not current_doc:
				break
			# Додаємо назву батька на початок списку
			path_parts.insert(0, current_doc.title)

		return " > ".join(path_parts)

	except frappe.DoesNotExistError:
		return name


@frappe.whitelist()
def get_katottg_hierarchy(name):
	"""Повертає ієрархію у вигляді списку кодів для заповнення діалогу."""
	if not name:
		return []
	try:
		ancestors = get_ancestors_of("KATOTTG", name, order_by="lft asc")
		return [*ancestors, name]
	except frappe.DoesNotExistError:
		return []
