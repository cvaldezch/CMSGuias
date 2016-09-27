select * from home_brand;
select * from home_model;
-- remove all brands init sm
DELETE FROM almacen_inventorybrandauditlogentry;
DELETE FROM home_model WHERE model_id NOT LIKE 'MO000';
DELETE FROM home_brand WHERE brand_id NOT LIKE 'BR000';
-- initialize brand on all system
update almacen_detguiaremision set  brand_id = 'BR000', model_id = 'MO000';
update almacen_detpedido set brand_id = 'BR000', model_id = 'MO000';
update ventas_metradoventa set brand_id = 'BR000', model_id = 'MO000';
update almacen_inventorybrand set brand_id = 'BR000', model_id = 'MO000';
update almacen_inventorybrandauditlogentry set brand_id = 'BR000', model_id = 'MO000';
update almacen_detingress set brand_id = 'BR000', model_id = 'MO000';
update almacen_detingressauditlogentry set brand_id = 'BR000', model_id = 'MO000';
update home_model set brand_id = 'BR000';
update logistica_detcompra set brand_id = 'BR000', model_id = 'MO000';
update operations_metproject set brand_id = 'BR000', model_id = 'MO000';
update operations_mmetrado set brand_id = 'BR000', model_id = 'MO000';
update ventas_historymetproject set brand_id = 'BR000', model_id = 'MO000';
update ventas_metradoventa set brand_id = 'BR000', model_id = 'MO000';
update ventas_metradoventaauditlogentry set brand_id = 'BR000', model_id = 'MO000';
update ventas_updatemetproject set brand_id = 'BR000', model_id = 'MO000';
update ventas_updatemetprojectauditlogentry set brand_id = 'BR000', model_id = 'MO000';
update operations_dsmetrado set brand_id = 'BR000', model_id = 'MO000';
update operations_dsmetradoauditlogentry set brand_id = 'BR000', model_id = 'MO000';
update almacen_detpedidoauditlogentry set brand_id = 'BR000', model_id = 'MO000';
update operations_historydsmetrado set brand_id = 'BR000', model_id = 'MO000';

select * from almacen_inventorybrand limit 1;

select * from home_materiale where materiales_id like '110013040600026';

-- UPDATE MATERIALS
update home_materiale set matnom = 'Abrazadera Antisismica'
WHERE matnom LIKE 'Abrazadera Antisismica Fig. 4L';
select * from home_materiale WHERE matnom = 'Abrazadera Antisismica';
select i.* from almacen_inventorybrand i
inner join home_materiale m
on m.materiales_id like i.materials_id
where m.matnom like '%Antisismica'
 
-- UPDATE DATA ASERVICE OF TABLE SALES PROJECT
select count(*) from ventas_proyecto;
select count(*) from ventas_proyecto where aservices IS  NULL;
update ventas_proyecto set aservices = 0
where aservices IS NULL;
update ventas_proyectoauditlogentry set aservices = 0
where aservices IS NULL;

select * from almacen_niple where id = 9774;
select * from almacen_guiaremision limit 1;
select * from almacen_detguiaremision limit 3;
-- nipleria para guia de remision
select * from almacen_nipleguiaremision limit 3;
-- nipleria para pedido
select * from almacen_niple limit 3;
select * from almacen_guiaremision limit 1;

  id   | pedido_id  |  materiales_id  | brand_id | model_id | cantidad | cantshop | cantguide | tag | spptag | comment | flag 
-------+------------+-----------------+----------+----------+----------+----------+-----------+-----+--------+---------+------
 17660 | PE16001319 | 117010610013001 | BR000    | MO000    |        6 |        6 |         0 | 0   | f      |         | t
(1 row)

  id  | pedido_id  | proyecto_id | subproyecto_id |  sector_id   | empdni |  materiales_id  | cantidad | metrado | cantshop | cantguide | tipo | flag | tag |        comment         | dsector_id | brand_id | model_id | related 
------+------------+-------------+----------------+--------------+--------+-----------------+----------+---------+----------+-----------+------+------+-----+------------------------+------------+----------+----------+---------
 9774 | PE16000741 | PR15129     |                | PR15129VEN01 |        | 115100030400040 |       65 |     600 |       65 |         0 | B    | t    | 0   |                        |            | BR000    | MO000    |       0
 9777 | PE16000741 | PR15129     |                | PR15129VEN01 |        | 115100030400042 |       10 |     600 |       10 |         0 | B    | t    | 0   |                        |            | BR000    | MO000    |       0
 9775 | PE16000741 | PR15129     |                | PR15129VEN01 |        | 115100030400040 |        2 |     100 |        2 |         0 | B    | t    | 0   | Soldar aquí el paquete |            | BR000    | MO000    |       0
 9776 | PE16000741 | PR15129     |                | PR15129VEN01 |        | 115100030400043 |        2 |     600 |        2 |         0 | B    | t    | 0   |                        |            | BR000    | MO000    |       0
(4 rows)

select * from logistica_detcompra where compra_id = 'OC16000205';