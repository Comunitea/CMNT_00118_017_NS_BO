-- HACER DESPUÉS UPDATE ALL --


-- Pasar las descrition_sale a nuevo campo internal_note
update product_template set internal_note = description_sale;
update product_template set description_sale=null;