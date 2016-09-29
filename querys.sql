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

select * from almacen_guiaremision;
select * from almacen_guiaremision where guia_id = '001-10019104';
SELECT * from almacen_detguiaremision where guia_id = '001-10019104';
select * from almacen_pedido where pedido_id = 'PE16000851';
select * from almacen_detpedido WHERE pedido_id = 'PE16000851';
select * from almacen_inventorybrand where materials_id in ('342032441900004','221098036001007')

   guia_id    | pedido_id  | ruccliente_id |                           puntollegada                           |          registrado           |  traslado  |  traruc_id  | condni_id | nropla_id | status | flag | motive | comment | observation | nota | dotoutput | orders | perreg_id | moveby 
--------------+------------+---------------+------------------------------------------------------------------+-------------------------------+------------+-------------+-----------+-----------+--------+------+--------+---------+-------------+------+-----------+--------+-----------+--------
 001-10019104 | PE16000851 | 20100154057   | Av. Alonso de Molina Nº 1652  - Santiago de Surco  - Lima - Lima | 2016-05-21 10:21:11.837466-05 | 2016-05-21 | 20428776110 | 43179067  | B6Z-761   | GE     | t    |        |         |             |      |           |        |           | Venta
(1 row)

  id   |   guia_id    |  materiales_id  | cantguide | flag | brand_id | model_id | observation | order_id | obrand_id | omodel_id 
-------+--------------+-----------------+-----------+------+----------+----------+-------------+----------+-----------+-----------
 11994 | 001-10019104 | 342032441900004 |        11 | t    | BR000    | MO000    |             |          | BR000     | MO000
 11995 | 001-10019104 | 221098036001007 |         6 | t    | BR000    | MO000    |             |          | BR000     | MO000
(2 rows)

 pedido_id  | proyecto_id | subproyecto_id |  sector_id   | almacen_id |               asunto               | empdni_id |          registrado           |  traslado  | obser | status | flag | orderfile |     dsector_id     
------------+-------------+----------------+--------------+------------+------------------------------------+-----------+-------------------------------+------------+-------+--------+------+-----------+--------------------
 PE16000851 | PR16020     |                | PR16020VEN01 | AL01       | Accesorios para valvulas angulares | 46377134  | 2016-05-18 16:25:50.080751-05 | 2016-05-20 | .     | CO     | t    |           | PR16020SG0002DS005
(1 row)

  id   | pedido_id  |  materiales_id  | brand_id | model_id | cantidad | cantshop | cantguide | tag | spptag | comment | flag 
-------+------------+-----------------+----------+----------+----------+----------+-----------+-----+--------+---------+------
 14755 | PE16000851 | 222118036013006 | BR000    | MO000    |        2 |        0 |         2 | 2   | f      |         | t
 14756 | PE16000851 | 336711070013002 | BR000    | MO000    |        2 |        0 |         2 | 2   | f      |         | t
 14754 | PE16000851 | 222118036013031 | BR000    | MO000    |        2 |        0 |         2 | 2   | f      |         | t
 14752 | PE16000851 | 342032441900004 | BR000    | MO000    |       11 |        0 |        11 | 2   | f      |         | t
 14753 | PE16000851 | 221098036001007 | BR000    | MO000    |        6 |        0 |         6 | 2   | f      |         | t
(5 rows)

  id  | storage_id | period |  materials_id   | brand_id | model_id |          ingress           | stock | purchase | flag | sale 
------+------------+--------+-----------------+----------+----------+----------------------------+-------+----------+------+------
 8205 | AL01       | 2016   | 342032441900004 | BR002    | MO022    | 2016-09-22 08:47:06.523-05 |    58 |     4.12 | t    |    2
 8206 | AL01       | 2016   | 342032441900004 | BR011    | MO022    | 2016-09-22 08:47:06.754-05 |     1 |     4.12 | t    |    2

 UPDATE 1
INFO:  OLD VERSION
INFO:  DET GUIDE (11994,001-10019104,342032441900004,11,t,BR000,MO000,,,BR000,MO000)
INFO:  DET ORDER (14752,PE16000851,342032441900004,BR000,MO000,11,0,11,2,f,"",t) 
INFO:  DET GUIDE (11995,001-10019104,221098036001007,6,t,BR000,MO000,,,BR000,MO000)
INFO:  DET ORDER (14753,PE16000851,221098036001007,BR000,MO000,6,0,6,2,f,"",t) 


   guia_id    | pedido_id  | ruccliente_id |                           puntollegada                           |          registrado           |  traslado  |  traruc_id  | condni_id | nropla_id | status | flag | motive | comment | observation | nota | dotoutput | orders | perreg_id | moveby 
--------------+------------+---------------+------------------------------------------------------------------+-------------------------------+------------+-------------+-----------+-----------+--------+------+--------+---------+-------------+------+-----------+--------+-----------+--------
 001-00018509 | PE16000392 | 20100154057   | Av. Alonso de Molina Nº 1652  - Santiago de Surco  - Lima - Lima | 2016-04-01 08:23:17.182084-05 | 2016-04-01 | 20428776110 | 43179067  | B6Z-761   | GE     | t    |        |         |             |      |           |        |           | Venta
(1 row)

  id  |   guia_id    |  materiales_id  | cantguide | flag | brand_id | model_id | observation | order_id | obrand_id | omodel_id 
------+--------------+-----------------+-----------+------+----------+----------+-------------+----------+-----------+-----------
 9556 | 001-00018509 | 343111440150008 |         1 | t    | BR000    | MO000    |             |          | BR000     | MO000
 9557 | 001-00018509 | 343111440150003 |         1 | t    | BR000    | MO000    |             |          | BR000     | MO000
 9558 | 001-00018509 | 343111440150004 |         1 | t    | BR000    | MO000    |             |          | BR000     | MO000
 9559 | 001-00018509 | 115100030400038 |      2.28 | t    | BR000    | MO000    |             |          | BR000     | MO000
 9560 | 001-00018509 | 115100030400037 |       7.1 | t    | BR000    | MO000    |             |          | BR000     | MO000
 9561 | 001-00018509 | 115100030400034 |       3.9 | t    | BR000    | MO000    |             |          | BR000     | MO000
(6 rows)

  id  |   guia_id    |  materiales_id  | metrado | cantguide | tipo | flag | brand_id | model_id | related | order_id 
------+--------------+-----------------+---------+-----------+------+------+----------+----------+---------+----------
 6960 | 001-00018509 | 115100030400038 |     228 |         1 | B    | t    | BR000    | MO000    |       0 | 
 6961 | 001-00018509 | 115100030400037 |     600 |         1 | B    | t    | BR000    | MO000    |       0 | 
 6962 | 001-00018509 | 115100030400037 |     110 |         1 | C    | t    | BR000    | MO000    |       0 | 
 6963 | 001-00018509 | 115100030400034 |     235 |         1 | A    | t    | BR000    | MO000    |       0 | 
 6964 | 001-00018509 | 115100030400034 |     155 |         1 | A    | t    | BR000    | MO000    |       0 | 
(5 rows)

 pedido_id  | proyecto_id | subproyecto_id |  sector_id   | almacen_id |           asunto           | empdni_id |          registrado          |  traslado  |    obser    | status | flag |                      orderfile                      |     dsector_id     
------------+-------------+----------------+--------------+------------+----------------------------+-----------+------------------------------+------------+-------------+--------+------+-----------------------------------------------------+--------------------
 PE16000392 | PR16020     |                | PR16020VEN01 | AL01       | NIPLERIA Y ACCESORIOS ESAN | 46377134  | 2016-03-29 16:23:55.19792-05 | 2016-03-31 | VER DETALLE | CO     | t    | storage/projects/2016/PR16020/orders/PE16000392.pdf | PR16020SG0002DS001
(1 row)

  id   | pedido_id  |  materiales_id  | brand_id | model_id | cantidad | cantshop | cantguide | tag | spptag | comment | flag 
-------+------------+-----------------+----------+----------+----------+----------+-----------+-----+--------+---------+------
 11863 | PE16000392 | 343111440150008 | BR000    | MO000    |        1 |        0 |         1 | 2   | f      |         | t
 11865 | PE16000392 | 115100030400037 | BR000    | MO000    |      7.1 |        0 |       7.1 | 2   | f      |         | t
 11864 | PE16000392 | 115100030400034 | BR000    | MO000    |      3.9 |        0 |       3.9 | 2   | f      |         | t
 11860 | PE16000392 | 221098036001009 | BR000    | MO000    |        2 |        0 |         2 | 2   | f      |         | t
 11866 | PE16000392 | 115100030400038 | BR000    | MO000    |     2.28 |        0 |      2.28 | 2   | f      |         | t
 11861 | PE16000392 | 343111440150004 | BR000    | MO000    |        1 |        0 |         1 | 2   | f      |         | t
 11862 | PE16000392 | 343111440150003 | BR000    | MO000    |        1 |        0 |         1 | 2   | f      |         | t
(7 rows)

  id  | pedido_id  | proyecto_id | subproyecto_id |  sector_id   |  empdni  |  materiales_id  | cantidad | metrado | cantshop | cantguide | tipo | flag | tag |   comment   |     dsector_id     | brand_id | model_id | related 
------+------------+-------------+----------------+--------------+----------+-----------------+----------+---------+----------+-----------+------+------+-----+-------------+--------------------+----------+----------+---------
 8628 | PE16000392 | PR16020     |                | PR16020VEN01 | 46377134 | 115100030400037 |        1 |     110 |        0 |         1 | C    | t    | 2   |             | PR16020SG0002DS001 | BR000    | MO000    |       0
 8627 | PE16000392 | PR16020     |                | PR16020VEN01 | 46377134 | 115100030400034 |        1 |     235 |        0 |         1 | A    | t    | 2   |             | PR16020SG0002DS001 | BR000    | MO000    |       0
 8630 | PE16000392 | PR16020     |                | PR16020VEN01 | 46377134 | 115100030400038 |        1 |     228 |        0 |         1 | B    | t    | 2   | VER DETALLE | PR16020SG0002DS001 | BR000    | MO000    |       0
 8629 | PE16000392 | PR16020     |                | PR16020VEN01 | 46377134 | 115100030400037 |        1 |     600 |        0 |         1 | B    | t    | 2   | VER DETALLE | PR16020SG0002DS001 | BR000    | MO000    |       0
 8626 | PE16000392 | PR16020     |                | PR16020VEN01 | 46377134 | 115100030400034 |        1 |     155 |        0 |         1 | A    | t    | 2   |             | PR16020SG0002DS001 | BR000    | MO000    |       0
(5 rows)

  id  | storage_id | period |  materials_id   | brand_id | model_id |          ingress           | stock | purchase | flag | sale 
------+------------+--------+-----------------+----------+----------+----------------------------+-------+----------+------+------
 8594 | AL01       | 2016   | 343111440150003 | BR002    | MO057    | 2016-09-22 08:49:00.391-05 |  2056 |      3.3 | t    |    2
 8595 | AL01       | 2016   | 343111440150004 | BR003    | MO058    | 2016-09-22 08:49:00.747-05 |    21 |      3.4 | t    |    2
 8726 | AL01       | 2016   | 115100030400034 | BR000    | MO000    | 2016-09-22 08:49:49.467-05 |    77 |       10 | t    |    2
 8729 | AL01       | 2016   | 115100030400037 | BR000    | MO000    | 2016-09-22 08:49:50.511-05 |    15 |    19.58 | t    |    2
 8730 | AL01       | 2016   | 115100030400038 | BR000    | MO000    | 2016-09-22 08:49:50.839-05 |   119 |    31.07 | t    |    2
(5 rows)




----
   guia_id    | pedido_id  | ruccliente_id |                            puntollegada                            |          registrado           |  traslado  |  traruc_id  | condni_id | nropla_id | status | flag | motive | comment | observation | nota | dotoutput | orders | perreg_id | moveby 
--------------+------------+---------------+--------------------------------------------------------------------+-------------------------------+------------+-------------+-----------+-----------+--------+------+--------+---------+-------------+------+-----------+--------+-----------+--------
 001-00018508 | PE16000253 | 20493020618   | AV. PEDRO MIOTTA NRO 1010  - San Juan de Miraflores  - Lima - Lima | 2016-03-31 15:11:41.165169-05 | 2016-03-31 | 20428776110 | 43179067  | B6Z-761   | GE     | t    |        |         |             |      |           |        |           | Venta
(1 row)

  id  |   guia_id    |  materiales_id  | cantguide | flag | brand_id | model_id | observation | order_id | obrand_id | omodel_id 
------+--------------+-----------------+-----------+------+----------+----------+-------------+----------+-----------+-----------
 9552 | 001-00018508 | 340012441900005 |        17 | t    | BR000    | MO000    |             |          | BR000     | MO000
 9553 | 001-00018508 | 342032441900004 |         1 | t    | BR000    | MO000    |             |          | BR000     | MO000
 9554 | 001-00018508 | 221098036001007 |        23 | t    | BR000    | MO000    |             |          | BR000     | MO000
 9555 | 001-00018508 | 221098036001006 |        13 | t    | BR000    | MO000    |             |          | BR000     | MO000
(4 rows)

 pedido_id  | proyecto_id | subproyecto_id |  sector_id   | almacen_id |     asunto     | empdni_id |          registrado           |  traslado  |           obser            | status | flag | orderfile |     dsector_id     
------------+-------------+----------------+--------------+------------+----------------+-----------+-------------------------------+------------+----------------------------+--------+------+-----------+--------------------
 PE16000253 | PR16017     |                | PR16017VEN01 | AL01       | montaje de GCI | 46377134  | 2016-03-11 13:03:21.527031-05 | 2016-03-14 | PAra montaje de GCI piso 2 | CO     | t    |           | PR16017SG0011DS001
(1 row)

  id   | pedido_id  |  materiales_id  | brand_id | model_id | cantidad | cantshop | cantguide | tag | spptag | comment | flag 
-------+------------+-----------------+----------+----------+----------+----------+-----------+-----+--------+---------+------
 10659 | PE16000253 | 342032441900003 | BR000    | MO000    |        6 |        0 |         6 | 2   | f      |         | t
 10667 | PE16000253 | 229611478102044 | BR000    | MO000    |       36 |        0 |        36 | 2   | f      |         | t
 10664 | PE16000253 | 342012440350005 | BR000    | MO000    |        1 |        0 |         1 | 2   | f      |         | t
 10666 | PE16000253 | 343042440150005 | BR000    | MO000    |        1 |        0 |         1 | 2   | f      |         | t
 10665 | PE16000253 | 342012440350007 | BR000    | MO000    |        1 |        0 |         1 | 2   | f      |         | t
 10652 | PE16000253 | 220998039914004 | BR000    | MO000    |        6 |        0 |         6 | 2   | f      |         | t
 10663 | PE16000253 | 227661468001031 | BR000    | MO000    |       16 |        0 |        16 | 2   | f      |         | t
 10657 | PE16000253 | 340012441900004 | BR000    | MO000    |       11 |        0 |        11 | 2   | f      |         | t
 10656 | PE16000253 | 340032441900004 | BR000    | MO000    |        4 |        0 |         4 | 2   | f      |         | t
 10655 | PE16000253 | 220988030014001 | BR000    | MO000    |       16 |        0 |        16 | 2   | f      |         | t
 10653 | PE16000253 | 220018030014005 | BR000    | MO000    |        2 |        0 |         2 | 2   | f      |         | t
 10654 | PE16000253 | 220018030014004 | BR000    | MO000    |        2 |        0 |         2 | 2   | f      |         | t
 10658 | PE16000253 | 340012441900005 | BR000    | MO000    |       17 |        0 |        17 | 2   | f      |         | t
 10651 | PE16000253 | 220998039914001 | BR000    | MO000    |        6 |        0 |         6 | 2   | f      |         | t
 10661 | PE16000253 | 221098036001006 | BR000    | MO000    |       13 |        0 |        13 | 2   | f      |         | t
 10662 | PE16000253 | 221098036001007 | BR000    | MO000    |       23 |        0 |        23 | 2   | f      |         | t
 10660 | PE16000253 | 342032441900004 | BR000    | MO000    |        1 |        0 |         1 | 2   | f      |         | t
(17 rows)

 id | guia_id | materiales_id | metrado | cantguide | tipo | flag | brand_id | model_id | related | order_id 
----+---------+---------------+---------+-----------+------+------+----------+----------+---------+----------
(0 rows)

 id | pedido_id | proyecto_id | subproyecto_id | sector_id | empdni | materiales_id | cantidad | metrado | cantshop | cantguide | tipo | flag | tag | comment | dsector_id | brand_id | model_id | related 
----+-----------+-------------+----------------+-----------+--------+---------------+----------+---------+----------+-----------+------+------+-----+---------+------------+----------+----------+---------
(0 rows)

  id  | storage_id | period |  materials_id   | brand_id | model_id |            ingress            | stock | purchase | flag | sale 
------+------------+--------+-----------------+----------+----------+-------------------------------+-------+----------+------+------
 8205 | AL01       | 2016   | 342032441900004 | BR002    | MO022    | 2016-09-22 08:47:06.523-05    |    58 |     4.12 | t    |    2
 8206 | AL01       | 2016   | 342032441900004 | BR011    | MO022    | 2016-09-22 08:47:06.754-05    |     1 |     4.12 | t    |    2
 8235 | AL01       | 2016   | 221098036001006 | BR001    | MO029    | 2016-09-22 08:47:14.155-05    |   208 |     0.19 | t    |    2
 8241 | AL01       | 2016   | 221098036001006 | BR012    | MO029    | 2016-09-22 08:47:15.756-05    |   100 |      0.2 | t    |    2
 8836 | AL01       | 2016   | 342032441900004 | BR000    | MO000    | 2016-09-29 10:39:14.286569-05 |    11 |        1 | t    | 1.15
 8837 | AL01       | 2016   | 221098036001007 | BR000    | MO000    | 2016-09-29 10:39:14.286569-05 |     6 |        1 | t    | 1.15
(6 rows)

----
   guia_id    | pedido_id  | ruccliente_id |                                     puntollegada                                      |          registrado           |  traslado  |  traruc_id  | condni_id | nropla_id | status | flag | motive | comment | observation | nota | dotoutput | orders | perreg_id | moveby 
--------------+------------+---------------+---------------------------------------------------------------------------------------+-------------------------------+------------+-------------+-----------+-----------+--------+------+--------+---------+-------------+------+-----------+--------+-----------+--------
 001-00019723 | PE16001319 | 20100154057   | Prolongación Incahuasi s/n, Mz. B, Lote 4, Urb. El Rancho - Miraflores  - Lima - Lima | 2016-06-30 13:10:51.129345-05 | 2016-06-30 | 20428776110 | 43179067  | B6Z-761   | GE     | t    |        |         |             |      |           |        |           | Venta
(1 row)

  id   |   guia_id    |  materiales_id  | cantguide | flag | brand_id | model_id | observation |  order_id  | obrand_id | omodel_id 
-------+--------------+-----------------+-----------+------+----------+----------+-------------+------------+-----------+-----------
 14496 | 001-00019723 | 117010610013001 |         2 | t    | BR000    | MO000    |             | PE16001319 | BR000     | MO000
 14477 | 001-00019723 | 342032441900004 |         1 | t    | BR011    | MO022    |             | PE16001319 | BR000     | MO000
 14476 | 001-00019723 | 342032441900004 |         4 | t    | BR002    | MO022    |             | PE16001319 | BR000     | MO000
(3 rows)

 pedido_id  | proyecto_id | subproyecto_id |  sector_id   | almacen_id |          asunto           | empdni_id |          registrado           |  traslado  | obser | status | flag | orderfile |       dsector_id        
------------+-------------+----------------+--------------+------------+---------------------------+-----------+-------------------------------+------------+-------+--------+------+-----------+-------------------------
 PE16001319 | PR16011     |                | PR16011VEN01 | AL01       | SOTANOS - COMPLEMENTARIOS | 46377134  | 2016-06-27 17:06:35.054615-05 | 2016-06-30 | -     | IN     | t    |           | PR16011VEN01SG0016DS001
(1 row)

  id   | pedido_id  |  materiales_id  | brand_id | model_id | cantidad | cantshop | cantguide | tag | spptag | comment | flag 
-------+------------+-----------------+----------+----------+----------+----------+-----------+-----+--------+---------+------
 17665 | PE16001319 | 344111570150018 | BR000    | MO000    |        6 |        0 |         0 | 2   | f      |         | t
 17662 | PE16001319 | 227701468001002 | BR000    | MO000    |      140 |        0 |         0 | 2   | f      |         | t
 17659 | PE16001319 | 342321560150007 | BR000    | MO000    |       16 |        0 |         0 | 2   | f      |         | t
 17656 | PE16001319 | 342032441900004 | BR000    | MO000    |        5 |        0 |         0 | 2   | f      |         | t
 17653 | PE16001319 | 340012441900005 | BR000    | MO000    |       11 |       11 |         0 | 0   | f      |         | t
 17654 | PE16001319 | 224821031713009 | BR000    | MO000    |      100 |      100 |         0 | 0   | f      |         | t
 17657 | PE16001319 | 342321560150006 | BR000    | MO000    |        8 |        8 |         0 | 0   | f      |         | t
 17658 | PE16001319 | 342321560150008 | BR000    | MO000    |        1 |        1 |         0 | 0   | f      |         | t
 17660 | PE16001319 | 117010610013001 | BR000    | MO000    |        6 |        1 |         0 | 1   | f      |         | t
 17661 | PE16001319 | 227661468001003 | BR000    | MO000    |       50 |       50 |         0 | 0   | f      |         | t
 17663 | PE16001319 | 344111570150022 | BR000    | MO000    |        3 |        3 |         0 | 0   | f      |         | t
 17671 | PE16001319 | 343111440150010 | BR000    | MO000    |        1 |        1 |         0 | 0   | f      |         | t
 17672 | PE16001319 | 343111440150011 | BR000    | MO000    |        1 |        1 |         0 | 0   | f      |         | t
 17673 | PE16001319 | 343171560150047 | BR000    | MO000    |        1 |        1 |         0 | 0   | f      |         | t
 17674 | PE16001319 | 343171560150052 | BR000    | MO000    |        1 |        1 |         0 | 0   | f      |         | t
 17675 | PE16001319 | 343161560150006 | BR000    | MO000    |        1 |        1 |         0 | 0   | f      |         | t
 17676 | PE16001319 | 226401461601003 | BR000    | MO000    |      100 |      100 |         0 | 0   | f      |         | t
 17666 | PE16001319 | 344111560150013 | BR000    | MO000    |       23 |       23 |         0 | 0   | f      |         | t
 17655 | PE16001319 | 564018030013002 | BR000    | MO000    |       12 |       12 |         0 | 0   | f      |         | t
 17664 | PE16001319 | 344111570150023 | BR000    | MO000    |        1 |        1 |         0 | 0   | f      |         | t
 17667 | PE16001319 | 344111560150023 | BR000    | MO000    |        1 |        1 |         0 | 0   | f      |         | t
 17668 | PE16001319 | 227691036201003 | BR000    | MO000    |      100 |      100 |         0 | 0   | f      |         | t
 17669 | PE16001319 | 343181560150006 | BR000    | MO000    |        1 |        1 |         0 | 0   | f      |         | t
 17670 | PE16001319 | 343181560150005 | BR000    | MO000    |        3 |        3 |         0 | 0   | f      |         | t
(24 rows)

  id  | storage_id | period |  materials_id   | brand_id | model_id |            ingress            | stock | purchase | flag | sale 
------+------------+--------+-----------------+----------+----------+-------------------------------+-------+----------+------+------
 8205 | AL01       | 2016   | 342032441900004 | BR002    | MO022    | 2016-09-22 08:47:06.523-05    |    58 |     4.12 | t    |    2
 8206 | AL01       | 2016   | 342032441900004 | BR011    | MO022    | 2016-09-22 08:47:06.754-05    |     1 |     4.12 | t    |    2
 8289 | AL01       | 2016   | 117010610013001 | BR000    | MO000    | 2016-09-22 08:47:28.116-05    |   100 |     4.76 | t    |    2
 8836 | AL01       | 2016   | 342032441900004 | BR000    | MO000    | 2016-09-29 10:39:14.286569-05 |    12 |        1 | t    | 1.15
(4 rows)

/*++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/

   guia_id    | pedido_id  | ruccliente_id |                                   puntollegada                                    |         registrado         |  traslado  |  traruc_id  | condni_id | nropla_id | status | flag | motive | comment | observation | nota | dotoutput |   orders   | perreg_id | moveby 
--------------+------------+---------------+-----------------------------------------------------------------------------------+----------------------------+------------+-------------+-----------+-----------+--------+------+--------+---------+-------------+------+-----------+------------+-----------+--------
 001-00000147 | PE16000741 | 20388101971   | Avenidas Ferrocarril y Prolongación San Carlos, Junín - Huancayo, Huancayo , Perú | 2016-09-22 17:42:47.598-05 | 2016-05-08 | 20428776110 | 43179067  | C6J-010   | GE     | t    | VENTA  |         |             |      |           | PE16000741 | 70492850  | Venta
(1 row)

  id   |   guia_id    |  materiales_id  | cantguide | flag | brand_id | model_id | observation |  order_id  | obrand_id | omodel_id 
-------+--------------+-----------------+-----------+------+----------+----------+-------------+------------+-----------+-----------
 14498 | 001-00000147 | 115100030400040 |        60 | t    | BR000    | MO000    |             | PE16000741 | BR000     | MO000
(1 row)

 pedido_id  | proyecto_id | subproyecto_id |  sector_id   | almacen_id |               asunto               | empdni_id |          registrado           |  traslado  |  obser  | status | flag | orderfile | dsector_id 
------------+-------------+----------------+--------------+------------+------------------------------------+-----------+-------------------------------+------------+---------+--------+------+-----------+------------
 PE16000741 | PR15129     |                | PR15129VEN01 | AL01       | sotano 1, plano 13,25 y Piso 1 - 2 | 72604244  | 2016-05-06 08:50:47.288412-05 | 2016-05-08 | PR15129 | AP     | t    |           | 
(1 row)

  id   | pedido_id  |  materiales_id  | brand_id | model_id | cantidad | cantshop | cantguide | tag | spptag | comment | flag 
-------+------------+-----------------+----------+----------+----------+----------+-----------+-----+--------+---------+------
 13874 | PE16000741 | 115100030400042 | BR000    | MO000    |       60 |       60 |         0 | 0   | f      |         | t
 13873 | PE16000741 | 115100030400043 | BR000    | MO000    |       12 |       12 |         0 | 0   | f      |         | t
 13871 | PE16000741 | 220998039914006 | BR000    | MO000    |       50 |       50 |         0 | 0   | f      |         | t
 13870 | PE16000741 | 220998039914005 | BR000    | MO000    |       50 |       50 |         0 | 0   | f      |         | t
 13869 | PE16000741 | 220998039914004 | BR000    | MO000    |       20 |       20 |         0 | 0   | f      |         | t
 13868 | PE16000741 | 220998039914002 | BR000    | MO000    |       20 |       20 |         0 | 0   | f      |         | t
 13867 | PE16000741 | 220998039914001 | BR000    | MO000    |       20 |       20 |         0 | 0   | f      |         | t
 13866 | PE16000741 | 220088036013001 | BR000    | MO000    |      100 |      100 |         0 | 0   | f      |         | t
 13864 | PE16000741 | 227691036201003 | BR000    | MO000    |      300 |      300 |         0 | 0   | f      |         | t
 13863 | PE16000741 | 229601478001040 | BR000    | MO000    |      300 |      300 |         0 | 0   | f      |         | t
 13862 | PE16000741 | 117010610013001 | BR000    | MO000    |       30 |       30 |         0 | 0   | f      |         | t
 13861 | PE16000741 | 117080740013001 | BR000    | MO000    |      400 |      400 |         0 | 0   | f      |         | t
 13859 | PE16000741 | 342032441900005 | BR000    | MO000    |       12 |       12 |         0 | 0   | f      |         | t
 13858 | PE16000741 | 342321560150009 | BR000    | MO000    |       20 |       20 |         0 | 0   | f      |         | t
 13860 | PE16000741 | 344012440150012 | BR000    | MO000    |        9 |        9 |         0 | 0   | f      |         | t
 13872 | PE16000741 | 115100030400040 | BR000    | MO000    |      392 |      332 |        60 | 1   | f      |         | t
(16 rows)

  id   |   guia_id    |  materiales_id  | metrado | cantguide | tipo | flag | brand_id | model_id | related |  order_id  
-------+--------------+-----------------+---------+-----------+------+------+----------+----------+---------+------------
 10328 | 001-00000147 | 115100030400040 |     600 |        10 | B    | t    | BR000    | MO000    |    9774 | PE16000741
(1 row)

  id  | pedido_id  | proyecto_id | subproyecto_id |  sector_id   | empdni |  materiales_id  | cantidad | metrado | cantshop | cantguide | tipo | flag | tag |        comment         | dsector_id | brand_id | model_id | related 
------+------------+-------------+----------------+--------------+--------+-----------------+----------+---------+----------+-----------+------+------+-----+------------------------+------------+----------+----------+---------
 9774 | PE16000741 | PR15129     |                | PR15129VEN01 |        | 115100030400040 |       65 |     600 |       45 |         0 | B    | t    | 1   |                        |            | BR000    | MO000    |       0
 9777 | PE16000741 | PR15129     |                | PR15129VEN01 |        | 115100030400042 |       10 |     600 |       10 |         0 | B    | t    | 0   |                        |            | BR000    | MO000    |       0
 9775 | PE16000741 | PR15129     |                | PR15129VEN01 |        | 115100030400040 |        2 |     100 |        2 |         0 | B    | t    | 0   | Soldar aquí el paquete |            | BR000    | MO000    |       0
 9776 | PE16000741 | PR15129     |                | PR15129VEN01 |        | 115100030400043 |        2 |     600 |        2 |         0 | B    | t    | 0   |                        |            | BR000    | MO000    |       0
(4 rows)

  id  | storage_id | period |  materials_id   | brand_id | model_id |          ingress           | stock | purchase | flag | sale 
------+------------+--------+-----------------+----------+----------+----------------------------+-------+----------+------+------
 8732 | AL01       | 2016   | 115100030400040 | BR000    | MO000    | 2016-09-22 08:49:51.534-05 |     1 |     12.4 | t    |    2
(1 row)