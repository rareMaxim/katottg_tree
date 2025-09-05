frappe.ui.form.on("KATOTTG Import Settings", {
	refresh: function (frm) {
		frm.get_field("import_button")
			.$wrapper.find(".btn-default")
			.html('<i class="fa fa-upload"></i> Почати імпорт');
		frm.fields_dict.progress_display.wrapper.innerHTML = "";
	},

	import_button: function (frm) {
		if (!frm.doc.data_file) {
			frappe.msgprint({
				title: __("Помилка"),
				indicator: "red",
				message: __("Будь ласка, спершу завантажте файл кодифікатора."),
			});
			return;
		}

		frm.disable_save();
		let progress_wrapper = frm.fields_dict.progress_display.wrapper;

		progress_wrapper.innerHTML = `
            <div id="job_id_display" class="text-muted small"></div>
            <div class="progress" style="margin-top: 5px;">
                <div class="progress-bar" role="progressbar" style="width: 0%;"></div>
            </div>
            <div class="progress-message text-muted small" style="margin-top: 5px;">Запуск процесу на сервері...</div>
        `;

		let progress_bar = progress_wrapper.querySelector(".progress-bar");
		let progress_message = progress_wrapper.querySelector(".progress-message");
		let job_id_display = progress_wrapper.querySelector("#job_id_display");

		frappe.call({
			method: "katottg_tree.utils.tree_importer.enqueue_import",
			callback: function (r) {
				if (r.message) {
					let job_id = r.message;

					// === НОВИЙ РЯДОК: Відображаємо Job ID ===
					job_id_display.innerHTML = `<strong>Job ID:</strong> ${job_id}`;

					progress_message.textContent = "Процес запущено. Очікування перших даних...";

					let interval = setInterval(() => {
						frappe.call({
							method: "katottg_tree.utils.tree_importer.get_import_progress",
							args: { job_id: job_id },
							callback: function (res) {
								if (res.message) {
									let progress = res.message;

									progress_bar.style.width = progress.percent + "%";
									progress_message.textContent = progress.message;

									if (progress.percent >= 100 || progress.is_error) {
										clearInterval(interval);
										frm.enable_save();

										if (progress.is_error) {
											progress_bar.classList.add("bg-danger");
											frappe.msgprint({
												title: __("Помилка імпорту"),
												indicator: "red",
												message: progress.message,
											});
										} else {
											frappe.show_alert(
												{
													message: __("Імпорт успішно завершено!"),
													indicator: "green",
												},
												7
											);
										}
									}
								}
							},
						});
					}, 2000);
				}
			},
			error: function (r) {
				frm.enable_save();
				progress_message.textContent = "Не вдалося запустити процес імпорту.";
			},
		});
	},
});
