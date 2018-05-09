-- Modulos custom a eliminar
UPDATE ir_module_module SET state = 'to remove' WHERE name = 'indaws_sports_comisiones';
UPDATE ir_module_module SET state = 'to remove' WHERE name = 'mail_delete_sent_by_footer';
UPDATE ir_module_module SET state = 'to remove' WHERE name = 'o2b_pricelist_import';
UPDATE ir_module_module SET state = 'to remove' WHERE name = 'o2b_pricelist_per_product';
UPDATE ir_module_module SET state = 'to remove' WHERE name = 'o2b_prod_pricelist_grid';
UPDATE ir_module_module SET state = 'to remove' WHERE name = 'pos_autoreconcile';
UPDATE ir_module_module SET state = 'to remove' WHERE name = 'tko_mail_smtp_per_user';
UPDATE ir_module_module SET state = 'to remove' WHERE name = 'wk_base_partner_patch';
UPDATE ir_module_module SET state = 'to remove' WHERE name = 'product_do_merge';
UPDATE ir_module_module SET state = 'to remove' WHERE name = 'web_widget_one2many_tags';

-- Me cargo vistas
delete from ir_ui_view where arch_db like '%date_confirm%';
--Me cargo la herencia de el report de duasal_sale para que no entre en conflicto con el de nostrum custom
delete from ir_ui_view where id = 1493;


-- Modulos OCA o de odoo no encontrados a eliminar 
UPDATE ir_module_module SET state = 'to remove' WHERE name = 'im_chat';
UPDATE ir_module_module SET state = 'to remove' WHERE name = 'edi';
UPDATE ir_module_module SET state = 'to remove' WHERE name = 'portal_project_issue';
UPDATE ir_module_module SET state = 'to remove' WHERE name = 'hr_evaluation';
UPDATE ir_module_module SET state = 'to remove' WHERE name = 'portal_payment_mode';
UPDATE ir_module_module SET state = 'to remove' WHERE name = 'account_payment_order_return';
-- UPDATE ir_module_module SET state = 'to remove' WHERE name = 'purchase_landed_cost'; PR
UPDATE ir_module_module SET state = 'to remove' WHERE name = 'account_journal_report';
UPDATE ir_module_module SET state = 'to remove' WHERE name = 'account_invoice_export_xls';
UPDATE ir_module_module SET state = 'to remove' WHERE name = 'account_admin_tools_importer';
UPDATE ir_module_module SET state = 'to remove' WHERE name = 'l10n_es_aeat_mod123';
UPDATE ir_module_module SET state = 'to remove' WHERE name = 'product_variant_supplierinfo';
UPDATE ir_module_module SET state = 'to remove' WHERE name = 'multi_company';
UPDATE ir_module_module SET state = 'to remove' WHERE name = 'l10n_es_account_financial_report_xlsx';
UPDATE ir_module_module SET state = 'to remove' WHERE name = 'product_variant_cost_price';
UPDATE ir_module_module SET state = 'to remove' WHERE name = 'report_webkit';
-- UPDATE ir_module_module SET state = 'to remove' WHERE name = 'account_payment_purchase'; PR
-- UPDATE ir_module_module SET state = 'to remove' WHERE name = 'l10n_es_aeat_mod347'; PR
UPDATE ir_module_module SET state = 'to remove' WHERE name = 'crm_mass_mailing';
UPDATE ir_module_module SET state = 'to remove' WHERE name = 'warning';
UPDATE ir_module_module SET state = 'to remove' WHERE name = 'portal_project';
UPDATE ir_module_module SET state = 'to remove' WHERE name = 'knowledge';
UPDATE ir_module_module SET state = 'to remove' WHERE name = 'stock_invoice_directly';
UPDATE ir_module_module SET state = 'to remove' WHERE name = 'product_variant_csv_import';
UPDATE ir_module_module SET state = 'to remove' WHERE name = 'account_payment_mode_term';
UPDATE ir_module_module SET state = 'to remove' WHERE name = 'account_admin_tools';


