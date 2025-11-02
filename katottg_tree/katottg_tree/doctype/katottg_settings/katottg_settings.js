// Copyright (c) 2025, Maxim S and contributors
// For license information, please see license.txt

frappe.ui.form.on("KATOTTG Settings", {
	refresh(frm) {
		// Додаємо обробник для кнопки очищення кешу
		frm.fields_dict.clear_cache_button.$input.on("click", function () {
			frappe.call({
				method: "katottg_tree.katottg_tree.doctype.katottg_settings.katottg_settings.clear_katottg_cache",
				callback: function (r) {
					if (r.message && r.message.success) {
						frappe.show_alert({
							message: __("Кеш успішно очищено"),
							indicator: "green",
						});
					}
				},
			});
		});
	},
});
