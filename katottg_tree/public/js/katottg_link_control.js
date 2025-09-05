// my_app/public/js/katottg_link_control.js

const OriginalControlLink = frappe.ui.form.ControlLink;

const CustomControlLink = class extends OriginalControlLink {
	is_custom_rendered() {
		return this.$wrapper.find(".katottg-link-wrapper").length > 0;
	}

	render_katottg_field() {
		if (!this.is_custom_rendered()) {
			// ✅ ДОДАНО ВІДСТУП: style="margin-bottom: 5px;"
			this.$wrapper.html(`
            <div class="katottg-link-wrapper" style="display: flex; align-items: center; margin-bottom: 10px;">
                <span class="katottg-display-area" style="flex-grow: 1; min-height: 20px;"></span>
                <button class="btn btn-xs btn-default btn-edit-katottg" style="margin-left: 10px;">
                    <i class="fa fa-search"></i> ${__("Обрати")}
                </button>
            </div>
        `);
			this.$display = this.$wrapper.find(".katottg-display-area");

			this.$wrapper.find(".btn-edit-katottg").on("click", () => {
				this.open_selection_dialog();
			});
		}

		// ✅ ВИРІШЕННЯ ПРОБЛЕМИ 1: Надійне отримання значення з моделі документа
		const value = this.frm ? this.frm.doc[this.df.fieldname] : null;

		if (value) {
			this.$display.text(__("Завантаження..."));
			frappe.call({
				method: "katottg_tree.utils.api.get_katottg_full_path", // Перевірте назву додатку
				args: { name: value },
				callback: (r) => {
					if (this.$display) {
						this.$display.html(r.message ? `<strong>${r.message}</strong>` : value);
					}
				},
			});
		} else {
			this.$display.html(`<span class="text-muted">${__("Не обрано")}</span>`);
		}
	}

	make_input() {
		if (this.df.options === "KATOTTG") {
			this.render_katottg_field();
		} else {
			super.make_input();
		}
	}

	refresh_input() {
		if (this.df.options === "KATOTTG") {
			this.render_katottg_field();
		} else {
			if (super.refresh_input) super.refresh_input();
		}
	}

	open_selection_dialog() {
		const control = this;
		frappe.ui.form.ControlLink = OriginalControlLink;

		const dialog = new frappe.ui.Dialog({
			title: __("Оберіть об'єкт"),
			fields: [
				{ label: "Область", fieldname: "level_1", fieldtype: "Link", options: "KATOTTG" },
				{ label: "Район", fieldname: "level_2", fieldtype: "Link", options: "KATOTTG" },
				{ label: "Громада", fieldname: "level_3", fieldtype: "Link", options: "KATOTTG" },
				{
					label: "Населений пункт",
					fieldname: "level_4",
					fieldtype: "Link",
					options: "KATOTTG",
				},
			],
			primary_action_label: __("Зберегти"),
			primary_action: (values) => {
				const final_value =
					values.level_4 || values.level_3 || values.level_2 || values.level_1;
				control.set_value(final_value).then(() => {
					control.refresh();
				});
				dialog.hide();
			},
		});

		const setup_filters_and_queries = () => {
			// Налаштування get_query для кожного поля
			dialog.get_field("level_1").get_query = () => ({
				filters: { is_group: 1, parent_katottg: "" },
			});
			dialog.get_field("level_2").get_query = () => ({
				filters: { is_group: 1, parent_katottg: dialog.get_value("level_1") },
			});
			dialog.get_field("level_3").get_query = () => ({
				filters: { is_group: 1, parent_katottg: dialog.get_value("level_2") },
			});
			dialog.get_field("level_4").get_query = () => ({
				filters: { parent_katottg: dialog.get_value("level_3") },
			});

			// Очищення дочірніх полів при зміні батьківського
			dialog.fields_dict.level_1.df.onchange = () => {
				dialog.set_value("level_2", "");
				dialog.set_value("level_3", "");
				dialog.set_value("level_4", "");
			};
			dialog.fields_dict.level_2.df.onchange = () => {
				dialog.set_value("level_3", "");
				dialog.set_value("level_4", "");
			};
			dialog.fields_dict.level_3.df.onchange = () => {
				dialog.set_value("level_4", "");
			};
		};

		const set_dialog_values = (hierarchy) => {
			if (!hierarchy || hierarchy.length === 0) return;
			// Встановлюємо значення послідовно
			if (hierarchy[0]) dialog.set_value("level_1", hierarchy[0]);
			if (hierarchy[1]) dialog.set_value("level_2", hierarchy[1]);
			if (hierarchy[2]) dialog.set_value("level_3", hierarchy[2]);
			if (hierarchy[3]) dialog.set_value("level_4", hierarchy[3]);
		};

		setup_filters_and_queries();

		const current_value = control.frm ? control.frm.doc[control.df.fieldname] : null;

		// ✅ ГОЛОВНЕ ВИПРАВЛЕННЯ:
		if (current_value) {
			// Якщо значення вже є, завантажуємо його ієрархію
			frappe.call({
				method: "katottg_tree.utils.api.get_katottg_hierarchy",
				args: { name: current_value },
				callback: (r) => {
					set_dialog_values(r.message);
				},
			});
		} else {
			// Якщо значення немає, завантажуємо ієрархію за замовчуванням
			frappe.call({
				method: "katottg_tree.utils.api.get_default_katottg_hierarchy", // Викликаємо новий метод
				callback: (r) => {
					set_dialog_values(r.message);
				},
			});
		}

		dialog.onhide = () => {
			frappe.ui.form.ControlLink = CustomControlLink;
		};

		dialog.show();
	}
};

frappe.ui.form.ControlLink = CustomControlLink;
