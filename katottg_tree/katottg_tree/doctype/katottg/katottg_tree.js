frappe.treeview_settings["KATOTTG"] = {
	onload: function (treeview) {
		// Додаємо кнопку на сторінку
		treeview.page.add_inner_button(__("Обробити всі вузли"), function () {
			// Викликаємо серверний метод, який запустить фонове завдання
			frappe.call({
				method: "katottg_tree.katottg_tree.doctype.katottg.katottg.process_all_nodes",
				callback: function (r) {
					// Після запуску Frappe автоматично покаже індикатор прогресу
					// для фонового завдання в правому верхньому куті.
				},
			});
		});
	},
};
