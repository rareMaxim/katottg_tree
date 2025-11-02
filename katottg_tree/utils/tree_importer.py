import json
import os
import uuid

import frappe
from frappe import _
from openpyxl import load_workbook


@frappe.whitelist()
def enqueue_import():
	"""Створює фонове завдання для імпорту та повертає його ID."""
	try:
		settings = frappe.get_single("KATOTTG Import Settings")
		file_url = settings.data_file
		if not file_url:
			frappe.throw(_("Будь ласка, завантажте файл кодифікатора."))

		# Визначаємо шлях до файлу
		if file_url.startswith("/private"):
			file_path = frappe.get_site_path("private", "files", file_url.split("/private/files/")[-1])
		else:
			file_path = frappe.get_site_path("public", "files", file_url.split("/files/")[-1])

		# Перевірка існування файлу
		if not os.path.exists(file_path):
			frappe.throw(_("Файл не знайдено за шляхом: {0}").format(file_path))

		# Перевірка формату файлу
		if not file_path.endswith((".xlsx", ".xls")):
			frappe.throw(_("Підтримуються тільки файли Excel (.xlsx або .xls)"))

		# Логування початку імпорту
		frappe.logger().info(f"Початок імпорту КАТОТТГ з файлу: {file_path}")

		tracking_id = str(uuid.uuid4())
		frappe.enqueue(
			background_importer,
			queue="long",
			timeout=2500,
			file_path=file_path,
			site=frappe.local.site,
			tracking_id=tracking_id,
		)

		return tracking_id

	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "KATOTTG Import Enqueue Error")
		frappe.throw(_("Помилка при запуску імпорту: {0}").format(str(e)))


def background_importer(file_path, site, tracking_id):
	"""Виконує імпорт у фоновому режимі та оновлює статус у кеші."""
	try:
		frappe.init(site=site)
		frappe.connect()
		job_id = tracking_id
		print(f"!!!!!!! Job ID successfully captured: {job_id} !!!!!!!!")

		update_progress(job_id, 0, 100, "Підготовка до імпорту...")

		# Виконуємо очищення та коміт в окремій транзакції, щоб зняти блокування
		frappe.db.delete("KATOTTG")
		frappe.db.commit()

		update_progress(job_id, 5, 100, "Старі дані видалено. Читання файлу...")

		workbook = load_workbook(filename=file_path, read_only=True)
		sheet = workbook.active
		total_rows = sheet.max_row - 4
		rows_iterator = sheet.iter_rows()
		for _i in range(4):
			next(rows_iterator)
		# 1. Визначаємо список полів для вставки
		fields = ["name", "code", "title", "category", "parent_katottg", "is_group"]

		values_to_insert = []
		batch_size = 500

		for idx, row in enumerate(rows_iterator):
			if idx > 0 and idx % batch_size == 0:
				percent = 5 + int((idx / total_rows) * 90)
				update_progress(job_id, percent, 100, f"Оброблено записів: {idx}/{total_rows}")

			row_data = [cell.value for cell in row]
			if not any(row_data):
				continue

			structure = get_row_structure(row_data)
			if not structure["current_code"] or not structure["title"]:
				continue

			# 2. Формуємо список значень у тій же послідовності, що й поля
			values = [
				structure["current_code"],  # name
				structure["current_code"],  # code
				structure["title"],  # title
				structure["category"],  # category
				structure["parent_code"],  # parent_katottg
				0,  # is_group
			]
			values_to_insert.append(values)

			# 3. Викликаємо bulk_insert з правильною сигнатурою
			if len(values_to_insert) >= batch_size:
				frappe.db.bulk_insert("KATOTTG", fields, values_to_insert, ignore_duplicates=True)
				values_to_insert.clear()

		# Вставляємо залишок
		if values_to_insert:
			frappe.db.bulk_insert("KATOTTG", fields, values_to_insert, ignore_duplicates=True)

		update_progress(job_id, 98, 100, "Оновлення ієрархії...")
		frappe.db.sql("""
            UPDATE `tabKATOTTG`
            SET `is_group` = 1
            WHERE `name` IN (
                SELECT DISTINCT `parent_katottg`
                FROM `tabKATOTTG`
                WHERE `parent_katottg` IS NOT NULL
            )
        """)

		frappe.db.commit()
		update_progress(job_id, 100, 100, "Імпорт успішно завершено!")

	except Exception:
		frappe.db.rollback()
		frappe.log_error(frappe.get_traceback(), "KATOTTG Background Import Error")
		raise
	finally:
		frappe.destroy()


@frappe.whitelist()
def get_import_progress(job_id):
	"""Повертає статус завдання з кешу."""
	job_key = f"katottg_import_{job_id}"
	return frappe.cache.get_value(job_key)


def update_progress(job_id, current, total, message, is_error=False):
	print(f"{job_id} {current} {total} {message}")
	"""Оновлює статус завдання у кеші."""
	progress = {"percent": min(current, total), "message": message, "is_error": is_error}
	frappe.cache.set_value(f"katottg_import_{job_id}", progress, expires_in_sec=600)


def get_row_structure(row_data):
	codes = [code for code in row_data[0:5] if code]
	if not codes:
		# Повертаємо структуру з порожніми значеннями, щоб уникнути помилок
		return {"level": 0, "current_code": None, "parent_code": None, "category": None, "title": None}

	current_code = codes[-1]
	parent_code = codes[-2] if len(codes) > 1 else None

	return {
		"level": len(codes),
		"current_code": current_code,
		"parent_code": parent_code,
		"category": row_data[5],
		"title": row_data[6],
	}
