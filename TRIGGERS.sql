/*
### STORES PROCEDURES
*/
-- DROP FUNCTION proc_erase_all_inventory()
CREATE OR REPLACE FUNCTION proc_erase_all_inventory()
  RETURNS BOOLEAN AS
$body$
BEGIN
    DELETE FROM almacen_inventoryBrand;
    DELETE FROM almacen_inventario;
    RETURN true;
  EXCEPTION
    WHEN OTHERS THEN
      ROLLBACK;
      RETURN FALSE;
END;
$body$
LANGUAGE plpgsql VOLATILE
COST 100;
/* END STORE PROCEDURES */
/*
### TRIGGERS FOR ALMACEN
*/
-- FUNCTION ADD ITEMS ON TABLE MATERIALS
CREATE OR REPLACE FUNCTION proc_verify_insert_materials()
  RETURNS TRIGGER AS
$BODY$
BEGIN
  IF EXISTS(SELECT * FROM home_materiale WHERE materiales_id LIKE NEW.materiales_id) THEN
    RETURN NULL;
  ELSE
    RETURN NEW;
  END IF;
END;
$BODY$
LANGUAGE plpgsql VOLATILE
COST 100;

CREATE TRIGGER tr_valid_exists_material
BEFORE INSERT ON home_materiale
FOR EACH ROW EXECUTE PROCEDURE proc_verify_insert_materials();
-- END TRIGGER
-- FUNCTION INCREMENT STOCK WHEN INSERT TABLE INVENTORYBRAND
CREATE OR REPLACE FUNCTION PROC_input_inventory_after_inventorybrand()
  RETURNS trigger AS
$BODY$
DECLARE
  _stock double precision := 0;
  _stkold DOUBLE PRECISION := 0;
  raw RECORD;
BEGIN
    _stock := NEW.stock;
    IF EXISTS( SELECT * FROM almacen_inventario WHERE materiales_id LIKE NEW.materials_id) THEN
      IF TG_OP = 'INSERT' THEN
        _stock := (SELECT SUM(stock) FROM almacen_inventoryBrand WHERE materials_id LIKE NEW.materials_id);
        UPDATE almacen_inventario SET stock = _stock
        WHERE materiales_id LIKE NEW.materials_id;
      ELSIF TG_OP = 'UPDATE' THEN
        _stkold := (NEW.stock - OLD.stock);
        RAISE INFO 'NEW VAL %', NEW.stock;
        RAISE INFO 'OLD VAL %', OLD.stock;
        IF (NEW.stock < OLD.stock) THEN
          RAISE INFO 'DECREASE UPDATE';
          RAISE INFO 'DECREASE VAL %', _stkold;
          UPDATE almacen_inventario SET stock = (stock - (@_stkold))
          WHERE materiales_id LIKE NEW.materials_id;
        ELSE
          RAISE INFO 'INCREASE UPDATE';
          UPDATE almacen_inventario SET stock = (stock + _stkold)
          WHERE materiales_id LIKE NEW.materials_id;
        END IF;
      END IF;
    ELSE
      INSERT INTO almacen_inventario (materiales_id,almacen_id,precompra,preventa,stkmin,stock,stkpendiente,stkdevuelto,periodo,ingreso,spptag,flag)
      VALUES (NEW.materials_id,'AL01',0,0,0,_stock,0,0,to_char(now(),'YYYY'),now(),false,true);
    END IF;
    --COMMIT;
    RETURN NEW;
    EXCEPTION
    WHEN OTHERS THEN
      RAISE INFO 'EXCEPTION ERROR %', SQLERRM;
      ROLLBACK;
      RETURN NULL;
END;
$BODY$
LANGUAGE 'plpgsql' VOLATILE
COST 100;

CREATE TRIGGER TR_balance_inventario
AFTER INSERT OR UPDATE ON almacen_inventoryBrand
FOR EACH ROW EXECUTE PROCEDURE PROC_input_inventory_after_inventorybrand();
-- test
-- DELETE ALL FROM TABLE INVENTARIO AND INVENTORYBRAND
DELETE FROM almacen_inventario WHERE materiales_id LIKE '115354089913003';
DELETE FROM almacen_inventoryBrand WHERE materials_id like '115354089913003';
DELETE FROM almacen_inventorybrandauditlogentry;
-- INPUT ROW IN INVENTORYBRAND
INSERT INTO almacen_inventoryBrand (storage_id, period, materials_id, brand_id, model_id, ingress, stock, purchase, sale, flag)
VALUES ('AL01', TO_CHAR(NOW(), 'YYYY'), '115354089913003', 'BR000', 'MO000', now(), 10, 1, 2, TRUE);
INSERT INTO almacen_inventoryBrand (storage_id, period, materials_id, brand_id, model_id, ingress, stock, purchase, sale, flag)
VALUES ('AL01', TO_CHAR(NOW(), 'YYYY'), '115354089913003', 'BR001', 'MO000', now(), 10, 1, 2, TRUE);
INSERT INTO almacen_inventoryBrand (storage_id, period, materials_id, brand_id, model_id, ingress, stock, purchase, sale, flag)
VALUES ('AL01', TO_CHAR(NOW(), 'YYYY'), '115354089913003', 'BR002', 'MO000', now(), 10, 1, 2, TRUE);
-- UPDATE INVENTORYBRAND
UPDATE almacen_inventoryBrand SET stock = 0
WHERE materials_id LIKE '115354089913003'
and brand_id like 'BR000' and model_id like 'MO000';
-- GET VERIFY DATA
SELECT * FROM almacen_inventoryBrand WHERE materials_id LIKE '115354089913003';
SELECT * FROM almacen_inventario WHERE materiales_id LIKE '115354089913003';
--
/* END BLOCK INVENTORY GLOBAL */

/* BLOCK TRIGGER REGISTER DECREATE INVENTORYBRAND WHEN REGISTER GUIDE REMISION */

/* END BLOCK REGISTER DET. GUIDE REMISION */
do $$
	declare a int;
	begin
		a := 3;
		a = a + 4;
		raise notice '%', a;
	end;
$$
---