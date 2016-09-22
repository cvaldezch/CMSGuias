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

CREATE OR REPLACE FUNCTION proc_erase_all_balance()
  RETURNS BOOLEAN AS
$$
BEGIN
DELETE FROM almacen_balance;
RETURN TRUE;
EXCEPTION
  WHEN OTHERS THEN
  ROLLBACK;
  RETURN FALSE;
END;
$$
LANGUAGE plpgsql VOLATILE
COST 100;

CREATE OR REPLACE FUNCTION proc_register_new_balance()
  RETURNS TRIGGER AS
$$
BEGIN
  IF TG_OP = 'INSERT' THEN
    INSERT INTO almacen_balance(materials_id, storage_id, register, brand_id, model_id, balance)
    VALUES (NEW.materials_id, 'AL01', now(), NEW.brand_id, NEW.model_id, NEW.stock);
  ELSIF TG_OP = 'UPDATE' THEN
    UPDATE almacen_balance SET balance = NEW.stock
    WHERE materials_id = NEW.materials_id AND brand_id = NEW.brand_id AND model_id = NEW.model_id;
  END IF;
  RETURN NEW;
EXCEPTION
  WHEN OTHERS THEN
  ROLLBACK;
  RETURN NULL;
END;
$$
LANGUAGE plpgsql VOLATILE
COST 100;

CREATE TRIGGER tr_register_new_balance
BEFORE INSERT OR UPDATE ON almacen_inventorybrand
FOR EACH ROW EXECUTE PROCEDURE proc_register_new_balance();
-- SELECT proc_erase_all_balance()
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
        -- RAISE INFO 'NEW VAL %', NEW.stock;
        -- RAISE INFO 'OLD VAL %', OLD.stock;
        IF (NEW.stock < OLD.stock) THEN
          -- RAISE INFO 'DECREASE UPDATE';
          -- RAISE INFO 'DECREASE VAL %', _stkold;
          UPDATE almacen_inventario SET stock = (stock - (@_stkold))
          WHERE materiales_id LIKE NEW.materials_id;
        ELSE
          -- RAISE INFO 'INCREASE UPDATE';
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
CREATE OR REPLACE FUNCTION proc_decrease_inventorybrand_and_detorder()
  RETURNS trigger AS
$BODY$
DECLARE
  _stk DOUBLE PRECISION := 0;
  _shop DOUBLE PRECISION := 0;
  _tag CHAR := '0';
  _status CHAR(2):= '';
  _order RECORD;
  v_error_stack text;
BEGIN
  -- DECREASE TABLE INVENTORYBRAND 
  SELECT stock into _stk FROM almacen_inventorybrand WHERE materials_id LIKE NEW.materiales_id AND brand_id LIKE NEW.brand_id AND model_id LIKE NEW.model_id;
  IF (_stk IS NOT NULL) THEN
    _stk := (_stk - NEW.cantguide);
    if _stk < 0::DOUBLE PRECISION THEN
      _stk := 0;
    END IF;
    UPDATE almacen_inventorybrand SET stock = _stk
    WHERE materials_id LIKE NEW.materiales_id AND brand_id LIKE NEW.brand_id AND model_id LIKE NEW.model_id;
  END IF;
  -- DECREASE TABLE DETPEDIDO
  SELECT cantshop INTO _shop FROM almacen_detpedido WHERE pedido_id LIKE NEW.order_id AND materiales_id LIKE NEW.materiales_id AND brand_id LIKE NEW.obrand_id AND model_id LIKE NEW.omodel_id;
  IF (_shop IS NOT NULL) THEN
    _shop := (_shop - NEW.cantguide);
    IF _shop < 0 THEN
      _shop := 0;
    END IF;
    IF _shop = 0::DOUBLE PRECISION THEN
      _tag := '2';
    ELSIF _shop > 0::DOUBLE PRECISION THEN
      _tag := '1';
    END IF;
    UPDATE almacen_detpedido SET cantshop = _shop, tag = _tag::CHAR
    WHERE pedido_id LIKE NEW.order_id AND materiales_id LIKE NEW.materiales_id AND brand_id LIKE NEW.obrand_id AND model_id LIKE NEW.omodel_id;
    RAISE INFO 'THE UPDATE DETPEDIDO';
  END IF;
  FOR _order IN (SELECT pedido_id, 
          (SELECT COUNT(*) FROM almacen_detpedido WHERE pedido_id LIKE d.pedido_id) AS total, 
          (SELECT COUNT(*) FROM almacen_detpedido WHERE d.pedido_id LIKE pedido_id AND tag LIKE '2') AS complete
          FROM almacen_detpedido d WHERE d.pedido_id like NEW.order_id GROUP BY pedido_id)
  LOOP
    IF (_order.total = _order.complete) THEN
      _status := 'CO';
    ELSIF (_order.complete > 0 AND _order.total > _order.complete) THEN
      _status := 'IN';
    END IF;
    RAISE INFO 'THE UPDATE PEDIDO';
    UPDATE almacen_pedido SET status = _status WHERE pedido_id = NEW.order_id;
  END LOOP;
  PERFORM proc_register_in_balance(NEW.materiales_id, NEW.brand_id, NEW.model_id, NEW.cantguide, '-');
  RETURN NEW;
  EXCEPTION
  WHEN OTHERS THEN
    GET STACKED DIAGNOSTICS v_error_stack = PG_EXCEPTION_CONTEXT;
    RAISE WARNING 'The stack trace of the error is: "%"', v_error_stack;
    RAISE INFO 'EXCEPTION ERROR % %', SQLERRM, SQLSTATE;
    ROLLBACK;
    RETURN NULL;
END;
$BODY$
LANGUAGE plpgsql VOLATILE
COST 100;

CREATE TRIGGER tr_discount_on_inventorybrand_detpedido
AFTER INSERT ON almacen_detguiaremision
FOR EACH ROW EXECUTE PROCEDURE proc_decrease_inventorybrand_and_detorder();

-- FUNCTION FOR REGISTER DISCOUNT REGISTER GUIDE
CREATE OR REPLACE FUNCTION proc_register_in_balance(varchar, varchar, varchar, double precision, char)
  RETURNS BOOLEAN AS
$$
DECLARE
  _stk INTEGER := 0;
  valid RECORD;
  stkold numeric(8,2);
  _balance numeric(8,2) := 0;
BEGIN
  -- VERIFY ITEMS EXISTS
  IF EXISTS(SELECT * FROM almacen_balance WHERE materials_id = $1 AND brand_id = $2 AND model_id = $3) THEN
    SELECT * FROM almacen_balance WHERE materials_id = $1 AND brand_id = $2 AND model_id = $3 AND extract(year FROM register) = extract(year FROM current_date)AND extract(month FROM register) = extract(month FROM current_date) INTO valid;
    IF FOUND THEN
    -- BALANCE IN MONTH CURRENT
      IF $5 = '+' THEN
        _balance := (valid.balance + $4);
      ELSIF $5 = '-' THEN
        _balance:= (valid.balance - $4);
      END IF;
      UPDATE almacen_balance SET balance = _balance WHERE materials_id = $1 AND brand_id = $2 AND model_id = $3  AND extract(year FROM register) = extract(year FROM current_date) AND extract(month FROM register) = extract(month FROM current_date);
    ELSE
    -- BALANCE IN MONTH NOT EXISTS
      SELECT balance::numeric INTO stkold FROM almacen_balance WHERE materials_id = $1 AND brand_id = $2 AND model_id = $3 AND register < current_date ORDER BY register DESC LIMIT 1;
      INSERT INTO almacen_balance (materials_id, storage_id, register, brand_id, model_id, balance) VALUES($1, 'AL01', now(), $2, $3, stkold);
      PERFORM proc_register_in_balance($1, $2, $3, $4, $5);
    END IF;
  ELSE
    SELECT stock INTO _stk FROM almacen_inventorybrand WHERE materials_id = $1 AND brand_id = $2 AND model_id = $3;
    -- insert new register item
    INSERT INTO almacen_balance (materials_id, storage_id, register, brand_id, model_id, balance) VALUES($1, 'AL01', now(), $2, $3, _stk);
    PERFORM proc_register_in_balance($1, $2, $3, $4, $5);
  END IF;
  RETURN True;
  EXCEPTION
    WHEN OTHERS THEN
    RAISE INFO 'EXCEPTION ERROR %', SQLERRM;
    ROLLBACK;
    RETURN FALSE;
END;
$$
LANGUAGE plpgsql VOLATILE
COST 100;
-- TEST
-- select ABS(-3);
-- SELECT * FROM almacen_detguiaremision;
-- PR16011
-- 342032441900004, 343181560150005, 115100030400040
-- PE16001319, PE16000741
-- 001-00019723

SELECT proc_register_in_balance('342032441900004', 'BR011', 'MO022', 1, '-');
SELECT * FROM almacen_balance order by register;
select * from almacen_inventorybrand where materials_id = '342032441900004';
select * from almacen_guiaremision g
inner join almacen_pedido pagos
on g.pedido_id LIKE p.pedido_id
WHERE p.proyecto_id like 'PR16011';
select * from almacen_detpedido where pedido_id like 'PE16001319';
select * from almacen_detguiaremision where guia_id like '001-00019723';
insert into almacen_detguiaremision (guia_id, materiales_id, cantguide, flag, brand_id, model_id, observation, order_id, obrand_id, omodel_id) 
VALUES('001-00019723','342032441900004',4,true,'BR002','MO022','','PE16001319','BR000','MO000');
insert into almacen_detguiaremision (guia_id, materiales_id, cantguide, flag, brand_id, model_id, observation, order_id, obrand_id, omodel_id) 
VALUES('001-00019723','342032441900004',1,true,'BR011','MO022','','PE16001319','BR000','MO000');
--
insert into almacen_detguiaremision (guia_id, materiales_id, cantguide, flag, brand_id, model_id, observation, order_id, obrand_id, omodel_id) 
VALUES('001-00019723','117010610013001',2,true,'BR000','MO000','','PE16001319','BR000','MO000');
select * from almacen_detpedido where pedido_id like 'PE16001319';
UPDATE almacen_detpedido SET tag = '2' 
UPDATE almacen_detpedido SET cantshop = 0 where tag = '2';
select * from almacen_detpedido where pedido_id like 'PE16001319' AND materiales_id LIKE '117010610013001';
select * from almacen_detguiaremision where guia_id = '001-00019723';
delete from almacen_detguiaremision where guia_id = '001-00019723' and materiales_id = '117010610013001';
select * from almacen_niple WHERE pedido_id like 'PE16001319';
select * from almacen_balance;
select * from almacen_inventorybrand where materials_id = '117010610013001';
select * from almacen_inventario where materiales_id = '117010610013001';
/* END BLOCK REGISTER DET. GUIDE REMISION */
/* BLOCK NIPLE GUIDE REMISION */
CREATE OR REPLACE FUNCTION proc_decrease_change_status_nip_order()
  RETURNS trigger AS
$BODY$
DECLARE
  _quantity INTEGER := 0;
  _tag CHAR := '';
BEGIN
  SELECT cantshop INTO _quantity FROM almacen_niple WHERE id=NEW.related AND pedido_id LIKE NEW.order_id;
  IF FOUND _quantity THEN
    _quantity := (_quantity - NEW.cantguide);
    IF _quantity < 0 THEN
      _quantity := 0;
    END IF;
    IF _quantity = 0 THEN
      _tag := '2';
    ELSIF _quantity > 0 THEN
      _tag := '1';
    END IF;
    UPDATE almacen_niple SET tag = _tag WHERE id=NEW.related AND pedido_id LIKE NEW.order_id;
  END IF;
  EXCEPTION
  WHEN OTHERS THEN
    RAISE INFO 'EXCEPTION ERROR %', SQLERRM;
    ROLLBACK;
    RETURN NULL;
END;
$BODY$
LANGUAGE plpgsql VOLATILE
COST 100;

CREATE TRIGGER tr_change_status_nipple_order
AFTER INSERT ON almacen_nipleguiaremision
FOR EACH ROW EXECUTE PROCEDURE proc_decrease_change_status_nip_order();

/* CREATE TRIGGER tr_discount_on_inventorybrand_detpedido
AFTER INSERT ON almacen_detguiaremision
FOR EACH ROW EXECUTE PROCEDURE proc_decrease_inventorybrand_and_detorder();*/
/* END BLOCK NIPPLE GUIDE REMISION*/
do $$
	declare
  x integer;
  a record;
  status char(2) := '';
	begin
  SELECT * FROM almacen_detpedido WHERE pedido_id = 'PE16001319' AND tag = '8' limit 1 INTO a;
  -- RAISE INFO '%', pg_typeof(a);
  --RAISE INFO '%', EXISTS(x);
  GET DIAGNOSTICS x = ROW_COUNT;
  raise info '%', x;
	end;
$$
---