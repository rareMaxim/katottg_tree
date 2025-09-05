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
	Повертає повний ієрархічний шлях, відформатований за шаблоном.
	Приклад: Запорізька область, Запорізький район, Запорізька ТГ, м. Запоріжжя
	"""
	if not name:
		return ""

	try:
		ancestors = get_ancestors_of("KATOTTG", name, order_by="lft asc")
		all_names = [*ancestors, name]

		# Отримуємо назву (title) і категорію (category) для всіх елементів
		object_data = {
			d.name: {"title": d.title, "category": d.category}
			for d in frappe.get_all(
				"KATOTTG", filters={"name": ("in", all_names)}, fields=["name", "title", "category"]
			)
		}

		# Функція для форматування назви на основі категорії
		def format_title(item_name):
			item = object_data.get(item_name)
			if not item:
				return item_name

			title = item.get("title")
			category = item.get("category")

			# Словник скорочень
			cat_map = {
				"O": "область",
				"K": "місто",  # Місто зі спец. статусом
				"P": "район",
				"H": "ТГ",  # Територіальна громада
				"M": "м.",
				"X": "с-ще",  # Селище
				"C": "с.",
				"B": "район",  # Район у місті
			}

			# Категорії, що додаються після назви
			suffix_cats = ["O", "P", "B"]

			if category in suffix_cats:
				# Наприклад, "Запорізька область", "Комунарський район"
				return f"{title} {cat_map.get(category, '')}".strip()
			elif category == "H":
				# Очищуємо від слів "міська", "сільська" тощо для чистоти
				clean_title = title.replace(" міська", "").replace(" сільська", "").replace(" селищна", "")
				return f"{clean_title} {cat_map.get(category, '')}"
			else:
				# Наприклад, "м. Запоріжжя", "с. Андріївка"
				return f"{cat_map.get(category, '')} {title}".strip()

		# Створюємо список з відформатованих частин
		path_parts = [format_title(n) for n in all_names]

		# З'єднуємо через кому і пробіл
		return ", ".join(path_parts)

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
