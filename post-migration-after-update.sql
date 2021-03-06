-- HACER DESPUÉS UPDATE ALL --


-- Pasar las descrition_sale a nuevo campo internal_note
update product_template set internal_note = description_sale;
update product_template set description_sale=null;

-- Copiar descripción del nombre y de los plazos de pago. Hacerlo despues de duplicar
update account_payment_term set note=name;
update account_payment_mode set note=name;

-- Albarán valorado por defecto false
update res_partner set valued_picking = False;

UPDATE ir_module_module SET state = 'to remove' WHERE name = 'nan_partner_risk';

-- Eliminar properties duplicadas que se pasaron del product.template
delete from ir_property where id in (select max(id) from ir_property where name = 'standard_price' group by res_id having count(*) > 1);
