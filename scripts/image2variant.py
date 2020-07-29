# -*- coding: utf-8 -*-
db_name = 'nostrum'
session.open(db=db_name)
templates = session.env['product.template'].search([('image', '!=', False)])
idx = 0
len_tmp = len(templates)
for tmp in templates:
    idx += 1
    print("***********************************************")
    # print(tmp.name) ralentiza
    print("%s / %s" % (idx, len_tmp))
    print("***********************************************")
    if tmp.image and len(tmp.product_variant_ids) == 1:
        tmp.product_variant_ids.write({'image': tmp.image})

session.cr.commit()
session.cr.close()