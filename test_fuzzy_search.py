#!/usr/bin/env python3
"""
Тестовий скрипт для демонстрації роботи Fuzzy Search в KATOTTG Tree
"""

import frappe

from katottg_tree.utils.api import search_katottg


def test_fuzzy_search():
	"""Тестування fuzzy search з різними запитами"""

	print("=" * 80)
	print("ТЕСТУВАННЯ FUZZY SEARCH В KATOTTG TREE")
	print("=" * 80)

	# Ініціалізація Frappe
	frappe.init(site="dev.itmlt.win")
	frappe.connect()

	# Тестові запити
	test_queries = [
		{"query": "Запоріжжя", "description": "Точний пошук міста"},
		{"query": "Запор", "description": "Неповна назва (початок)"},
		{"query": "Мелітоп", "description": "Неповна назва без останньої букви"},
		{"query": "зька область", "description": "Пошук по частині та слову"},
		{"query": "громада", "description": "Пошук по типу об'єкта", "limit": 10},
	]

	# Перевіряємо налаштування
	settings = frappe.get_single("KATOTTG Settings")
	fuzzy_enabled = settings.enable_fuzzy_search

	print("\n📊 Налаштування:")
	print(f"   Fuzzy Search: {'✅ Увімкнено' if fuzzy_enabled else '❌ Вимкнено'}")
	print(f"   Ліміт результатів: {settings.search_results_limit or 50}")
	print(f"   Кешування: {'✅ Увімкнено' if settings.enable_caching else '❌ Вимкнено'}")

	# Виконуємо тести
	for idx, test in enumerate(test_queries, 1):
		print(f"\n{'=' * 80}")
		print(f"ТЕСТ #{idx}: {test['description']}")
		print(f"Запит: '{test['query']}'")
		print("-" * 80)

		try:
			results = search_katottg(query=test["query"], limit=test.get("limit", 5))

			if results:
				print(f"✅ Знайдено результатів: {len(results)}\n")

				for i, result in enumerate(results, 1):
					relevance = result.get("relevance", "N/A")
					print(f"{i}. [{relevance}%] {result['title']}")
					print(f"   Код: {result['code']}")
					print(f"   Категорія: {result['category']}")
					if "full_path" in result:
						print(f"   Шлях: {result['full_path']}")
					print()
			else:
				print("❌ Нічого не знайдено\n")

		except Exception as e:
			print(f"❌ Помилка: {e!s}\n")
			frappe.log_error(frappe.get_traceback(), "Fuzzy Search Test Error")

	# Порівняльний тест
	print(f"\n{'=' * 80}")
	print("ПОРІВНЯЛЬНИЙ ТЕСТ: Fuzzy ON vs OFF")
	print("-" * 80)

	test_query = "Мелітоп"

	# Тест з fuzzy
	print(f"\n🔍 З Fuzzy Search (query: '{test_query}'):")
	settings.enable_fuzzy_search = 1
	settings.save()
	frappe.db.commit()

	results_fuzzy = search_katottg(test_query, limit=5)
	print(f"   Знайдено: {len(results_fuzzy)} результатів")
	for r in results_fuzzy[:3]:
		print(f"   - {r['title']} (relevance: {r.get('relevance', 'N/A')}%)")

	# Тест без fuzzy
	print(f"\n🔍 Без Fuzzy Search (query: '{test_query}'):")
	settings.enable_fuzzy_search = 0
	settings.save()
	frappe.db.commit()

	results_normal = search_katottg(test_query, limit=5)
	print(f"   Знайдено: {len(results_normal)} результатів")
	for r in results_normal[:3]:
		print(f"   - {r['title']}")

	# Відновлюємо початкові налаштування
	settings.enable_fuzzy_search = fuzzy_enabled
	settings.save()
	frappe.db.commit()

	print(f"\n{'=' * 80}")
	print("✅ ТЕСТУВАННЯ ЗАВЕРШЕНО")
	print("=" * 80)

	# Закриваємо з'єднання
	frappe.destroy()


if __name__ == "__main__":
	test_fuzzy_search()
