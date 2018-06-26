-- HACER DESPUÉS UPDATE ALL --


-- Pasar las descrition_sale a nuevo campo internal_note
update product_template set internal_note = description_sale;
update product_template set description_sale=null;

-- Copiar descripción del nombre y de los plazos de pago
update account_payment_term set note=name;
update account_payment_mode set note=name;

-- Albarán valorado por defecto false
update res_partner set valued_picking = False;

