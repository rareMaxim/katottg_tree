import frappe
from frappe import _
from frappe.utils.nestedset import get_ancestors_of


@frappe.whitelist()
def get_default_katottg_hierarchy():
	"""
	Повертає ієрархію для значення за замовчуванням.
	Використовує налаштування з KATOTTG Settings.
	"""
	from katottg_tree.katottg_tree.doctype.katottg_settings.katottg_settings import (
		get_default_katottg,
	)

	default_name = get_default_katottg()
	if not default_name:
		return []

	cache_key = f"katottg_default_hierarchy_{default_name}"
	cached = frappe.cache.get_value(cache_key)
	if cached:
		return cached

	try:
		ancestors = get_ancestors_of("KATOTTG", default_name, order_by="lft asc")
		result = [*ancestors, default_name]

		# Кешуємо результат
		_cache_result(cache_key, result)
		return result
	except frappe.DoesNotExistError:
		frappe.log_error(
			_("Об'єкт КАТОТТГ за замовчуванням не знайдено: {0}").format(default_name),
			"KATOTTG Default Hierarchy Error",
		)
		return []
	except Exception:
		frappe.log_error(frappe.get_traceback(), "KATOTTG Default Hierarchy Error")
		return []


@frappe.whitelist()
def get_katottg_full_path(name):
	"""
	Повертає повний ієрархічний шлях, відформатований за шаблоном.
	Приклад: Запорізька область, Запорізький район, Запорізька ТГ, м. Запоріжжя
	"""
	if not name:
		return ""

	# Перевірка кешу
	cache_key = f"katottg_full_path_{name}"
	cached = frappe.cache.get_value(cache_key)
	if cached:
		return cached

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
		result = ", ".join(path_parts)

		# Кешуємо результат
		_cache_result(cache_key, result)
		return result

	except frappe.DoesNotExistError:
		frappe.log_error(_("Об'єкт КАТОТТГ не знайдено: {0}").format(name), "KATOTTG Full Path Error")
		return name
	except Exception:
		frappe.log_error(frappe.get_traceback(), "KATOTTG Full Path Error")
		return name


@frappe.whitelist()
def get_katottg_hierarchy(name):
	"""Повертає ієрархію у вигляді списку кодів для заповнення діалогу."""
	if not name:
		return []

	# Перевірка кешу
	cache_key = f"katottg_hierarchy_{name}"
	cached = frappe.cache.get_value(cache_key)
	if cached:
		return cached

	try:
		ancestors = get_ancestors_of("KATOTTG", name, order_by="lft asc")
		result = [*ancestors, name]

		# Кешуємо результат
		_cache_result(cache_key, result)
		return result
	except frappe.DoesNotExistError:
		frappe.log_error(_("Об'єкт КАТОТТГ не знайдено: {0}").format(name), "KATOTTG Hierarchy Error")
		return []
	except Exception:
		frappe.log_error(frappe.get_traceback(), "KATOTTG Hierarchy Error")
		return []


@frappe.whitelist()
def search_katottg(query, filters=None, limit=50):
	"""
	Пошук об'єктів КАТОТТГ по коду або назві.
	Підтримує звичайний та нечіткий (fuzzy) пошук.

	Args:
	    query: Пошуковий запит
	    filters: Додаткові фільтри (категорія, тощо)
	    limit: Максимальна кількість результатів

	Returns:
	    Список об'єктів КАТОТТГ з повною інформацією
	"""
	from katottg_tree.katottg_tree.doctype.katottg_settings.katottg_settings import (
		get_settings,
	)

	if not query:
		return []

	# Отримуємо налаштування
	try:
		settings = get_settings()
		limit = min(limit or 50, settings.search_results_limit or 50)
		enable_fuzzy = settings.enable_fuzzy_search or False
	except Exception:
		limit = 50
		enable_fuzzy = False

	# Базові фільтри
	search_filters = []
	if filters:
		search_filters.append(filters)

	try:
		if enable_fuzzy:
			# Нечіткий пошук (fuzzy search)
			results = _fuzzy_search(query, search_filters, limit)
		else:
			# Звичайний пошук
			or_filters = [["code", "like", f"%{query}%"], ["title", "like", f"%{query}%"]]

			results = frappe.get_all(
				"KATOTTG",
				filters=search_filters,
				or_filters=or_filters,
				fields=["name", "code", "title", "category", "parent_katottg", "is_group"],
				limit=limit,
				order_by="code asc",
			)

		# Додаємо повний шлях для кожного результату
		for result in results:
			result["full_path"] = get_katottg_full_path(result["name"])

		return results
	except Exception:
		frappe.log_error(frappe.get_traceback(), "KATOTTG Search Error")
		return []


def _fuzzy_search(query, base_filters, limit):
	"""
	Нечіткий пошук (fuzzy search) з кількома рівнями точності.

	Стратегія пошуку:
	1. Точний збіг (exact match)
	2. Збіг на початку (starts with)
	3. Збіг будь-де (contains)
	4. Пошук по словах (word search)
	5. Транслітерація (для української/англійської)

	Args:
	    query: Пошуковий запит
	    base_filters: Базові фільтри
	    limit: Максимальна кількість результатів

	Returns:
	    Список результатів з оцінкою релевантності
	"""
	query_lower = query.lower().strip()
	results = []
	seen = set()

	# Рівень 1: Точний збіг
	exact_match = frappe.get_all(
		"KATOTTG",
		filters=base_filters,
		or_filters=[
			["code", "=", query],
			["title", "=", query],
		],
		fields=["name", "code", "title", "category", "parent_katottg", "is_group"],
		limit=limit,
	)

	for r in exact_match:
		if r.name not in seen:
			r["relevance"] = 100  # Найвища релевантність
			results.append(r)
			seen.add(r.name)

	# Рівень 2: Починається з (case-insensitive)
	if len(results) < limit:
		starts_with = frappe.get_all(
			"KATOTTG",
			filters=base_filters,
			or_filters=[
				["code", "like", f"{query}%"],
				["title", "like", f"{query}%"],
			],
			fields=["name", "code", "title", "category", "parent_katottg", "is_group"],
			limit=limit * 2,
		)

		for r in starts_with:
			if r.name not in seen and len(results) < limit:
				r["relevance"] = 80
				results.append(r)
				seen.add(r.name)

	# Рівень 3: Містить (case-insensitive)
	if len(results) < limit:
		contains = frappe.get_all(
			"KATOTTG",
			filters=base_filters,
			or_filters=[
				["code", "like", f"%{query}%"],
				["title", "like", f"%{query}%"],
			],
			fields=["name", "code", "title", "category", "parent_katottg", "is_group"],
			limit=limit * 2,
		)

		for r in contains:
			if r.name not in seen and len(results) < limit:
				r["relevance"] = 60
				results.append(r)
				seen.add(r.name)

	# Рівень 4: Пошук по окремих словах
	if len(results) < limit:
		words = query_lower.split()
		if len(words) > 1:
			word_filters = []
			for word in words:
				if len(word) >= 2:  # Ігноруємо дуже короткі слова
					word_filters.extend(
						[
							["title", "like", f"%{word}%"],
						]
					)

			if word_filters:
				word_search = frappe.get_all(
					"KATOTTG",
					filters=base_filters,
					or_filters=word_filters,
					fields=["name", "code", "title", "category", "parent_katottg", "is_group"],
					limit=limit * 2,
				)

				for r in word_search:
					if r.name not in seen and len(results) < limit:
						# Підраховуємо скільки слів збіглось
						title_lower = r.title.lower()
						matched_words = sum(1 for word in words if word in title_lower)
						r["relevance"] = 40 + (matched_words * 5)
						results.append(r)
						seen.add(r.name)

	# Сортуємо за релевантністю
	results.sort(key=lambda x: x.get("relevance", 0), reverse=True)

	# Обмежуємо кількість результатів
	return results[:limit]


@frappe.whitelist()
def get_katottg_by_category(category, parent=None, limit=100):
	"""
	Отримати список об'єктів КАТОТТГ по категорії.

	Args:
	    category: Категорія (O, P, H, M, C, X, B, K)
	    parent: Батьківський об'єкт (опціонально)
	    limit: Максимальна кількість результатів

	Returns:
	    Список об'єктів КАТОТТГ
	"""
	if not category:
		return []

	filters = {"category": category}
	if parent:
		filters["parent_katottg"] = parent

	try:
		return frappe.get_all(
			"KATOTTG",
			filters=filters,
			fields=["name", "code", "title", "category", "parent_katottg", "is_group"],
			limit=limit,
			order_by="title asc",
		)
	except Exception:
		frappe.log_error(frappe.get_traceback(), "KATOTTG By Category Error")
		return []


def _cache_result(key, value):
	"""Допоміжна функція для кешування результатів з урахуванням налаштувань"""
	from katottg_tree.katottg_tree.doctype.katottg_settings.katottg_settings import (
		get_cache_ttl,
	)

	try:
		ttl = get_cache_ttl()
		frappe.cache.set_value(key, value, expires_in_sec=ttl)
	except Exception:
		# Якщо не вдалося отримати TTL, використовуємо значення за замовчуванням
		frappe.cache.set_value(key, value, expires_in_sec=3600)
