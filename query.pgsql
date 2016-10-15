--INSERT INTO home_mniple VALUES ('A', 'ROSCADO', true), ('B', 'RANURADO', true), ('C', 'ROSCA-RANURA', true), ('D', 'BRIDA', true), ('E', 'BRIDA-ROSCA', true), ('F', 'BRIDA-RANURA', true), ('G', 'BISEL', true), ('H', 'BISEL-ROSCA', true), ('I', 'BRIDA HECHIZO', true),('-', 'ROSCADO', true);
-- select * from home_materiale where lower(matnom) like 'tuberia%' order by matnom;
-- select * from home_materiale where materiales_id = '115100030400040';
select * from almacen_niple g having (select count(*) from almacen_niple n where g.pedido_id = n.pedido_id) > 15;