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

DROP TRIGGER tr_register_new_balance ON almacen_inventorybrand;
-- CREATE OR REPLACE FUNCTION proc_register_new_balance()
--   RETURNS TRIGGER AS
-- $$
-- BEGIN
--   IF TG_OP = 'INSERT' THEN
--     INSERT INTO almacen_balance(materials_id, storage_id, register, brand_id, model_id, balance)
--     VALUES (NEW.materials_id, 'AL01', now(), NEW.brand_id, NEW.model_id, NEW.stock);
--   ELSIF TG_OP = 'UPDATE' THEN
--     UPDATE almacen_balance SET balance = NEW.stock
--     WHERE materials_id = NEW.materials_id AND brand_id = NEW.brand_id AND model_id = NEW.model_id;
--   END IF;
--   RETURN NEW;
-- EXCEPTION
--   WHEN OTHERS THEN
--   ROLLBACK;
--   RETURN NULL;
-- END;
-- $$
-- LANGUAGE plpgsql VOLATILE
-- COST 100;

-- CREATE TRIGGER tr_register_new_balance
-- BEFORE INSERT OR UPDATE ON almacen_inventorybrand
-- FOR EACH ROW EXECUTE PROCEDURE proc_register_new_balance();

--raise
--"[Error 32] The process cannot access the file because it is being used by another 
--process: u'C:\\Users\\Christian\\development\\django\\icrperu\\vicrperu\\icrperu\\CMSGuias\\media/storage/Temp/storage.xlsx'"
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
-- INSERT INTO almacen_inventoryBrand (storage_id, period, materials_id, brand_id, model_id, ingress, stock, purchase, sale, flag)
-- VALUES ('AL01', TO_CHAR(NOW(), 'YYYY'), '115354089913003', 'BR000', 'MO000', now(), 10, 1, 2, TRUE);
-- INSERT INTO almacen_inventoryBrand (storage_id, period, materials_id, brand_id, model_id, ingress, stock, purchase, sale, flag)
-- VALUES ('AL01', TO_CHAR(NOW(), 'YYYY'), '115354089913003', 'BR001', 'MO000', now(), 10, 1, 2, TRUE);
-- INSERT INTO almacen_inventoryBrand (storage_id, period, materials_id, brand_id, model_id, ingress, stock, purchase, sale, flag)
-- VALUES ('AL01', TO_CHAR(NOW(), 'YYYY'), '115354089913003', 'BR002', 'MO000', now(), 10, 1, 2, TRUE);
-- UPDATE INVENTORYBRAND
-- UPDATE almacen_inventoryBrand SET stock = 0
-- WHERE materials_id LIKE '115354089913003'
-- and brand_id like 'BR000' and model_id like 'MO000';
-- GET VERIFY DATA
SELECT * FROM almacen_inventoryBrand WHERE materials_id LIKE '115100030400040';
SELECT * FROM almacen_inventario WHERE materiales_id LIKE '115100030400040';
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
    UPDATE almacen_detpedido SET cantshop = _shop, cantguide = (cantguide + NEW.cantguide), tag = _tag::CHAR
    WHERE pedido_id LIKE NEW.order_id AND materiales_id LIKE NEW.materiales_id AND brand_id LIKE NEW.obrand_id AND model_id LIKE NEW.omodel_id;
    RAISE INFO 'THE UPDATE DETPEDIDO';
  END IF;
  --PERFORM proc_register_in_balance(NEW.materiales_id, NEW.brand_id, NEW.model_id, NEW.cantguide, '-');
  RETURN NEW;
EXCEPTION
  WHEN OTHERS THEN
    -- GET STACKED DIAGNOSTICS v_error_stack = PG_EXCEPTION_CONTEXT;
    -- RAISE WARNING 'The stack trace of the error is: "%"', v_error_stack;
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

CREATE OR REPLACE FUNCTION proc_change_status_order()
  RETURNS TRIGGER AS
$$
DECLARE
  complete integer;
  _status CHAR(2):= '';
  total integer;
BEGIN
  total := (SELECT count(pedido_id) FROM almacen_detpedido WHERE pedido_id LIKE NEW.pedido_id);
  complete := (SELECT count(pedido_id) FROM almacen_detpedido WHERE pedido_id LIKE NEW.pedido_id AND tag LIKE '2');
  IF (total = complete) THEN
    _status := 'CO';
  ELSIF (complete > 0 AND total > complete) THEN
    _status := 'IN';
  ELSE
    _status := 'AP';
  END IF;
  UPDATE almacen_pedido SET status = _status WHERE pedido_id = NEW.pedido_id;
  RETURN NEW;
EXCEPTION
  WHEN OTHERS THEN
    RAISE INFO 'EXCEPTION ERROR % %', SQLERRM, SQLSTATE;
    ROLLBACK;
    RETURN NULL;
END;
$$
LANGUAGE plpgsql VOLATILE
COST 100;

CREATE TRIGGER tr_change_status_order
AFTER UPDATE ON almacen_detpedido
FOR EACH ROW EXECUTE PROCEDURE proc_change_status_order();

-- FUNCTION FOR REGISTER DISCOUNT REGISTER GUIDE
CREATE OR REPLACE FUNCTION proc_register_in_balance()
  RETURNS TRIGGER AS
$$
DECLARE
  _stk INTEGER := 0;
  valid RECORD;
  stkold numeric(8,2);
  _balance numeric(8,2) := 0;
BEGIN
  -- VERIFY ITEMS EXISTS
  IF EXISTS(SELECT * FROM almacen_balance WHERE materials_id = NEW.materials_id AND brand_id = NEW.brand_id AND model_id = NEW.model_id) THEN
    SELECT INTO valid * FROM almacen_balance WHERE materials_id = NEW.materials_id AND brand_id = NEW.brand_id AND model_id = NEW.model_id AND extract(year FROM register) = extract(year FROM current_date)AND extract(month FROM register) = extract(month FROM current_date);
    IF FOUND THEN
    -- BALANCE IN MONTH CURRENT
      UPDATE almacen_balance SET balance = NEW.stock WHERE materials_id = NEW.materials_id AND brand_id = NEW.brand_id AND model_id = NEW.model_id  AND extract(year FROM register) = extract(year FROM current_date) AND extract(month FROM register) = extract(month FROM current_date);
    ELSE
    -- BALANCE IN MONTH NOT EXISTS
      SELECT balance::numeric INTO stkold FROM almacen_balance WHERE materials_id = NEW.materials_id AND brand_id = NEW.brand_id AND model_id = NEW.model_id AND register < current_date ORDER BY register DESC LIMIT 1;
      INSERT INTO almacen_balance (materials_id, storage_id, register, brand_id, model_id, balance) VALUES(NEW.materials_id, 'AL01', now(), NEW.brand_id, NEW.model_id, stkold);
      UPDATE almacen_balance SET balance = NEW.stock WHERE materials_id = NEW.materials_id AND brand_id = NEW.brand_id AND model_id = NEW.model_id  AND extract(year FROM register) = extract(year FROM current_date) AND extract(month FROM register) = extract(month FROM current_date);
    END IF;
  ELSE
    SELECT stock INTO _stk FROM almacen_inventorybrand WHERE materials_id = NEW.materials_id AND brand_id = NEW.brand_id AND model_id = NEW.model_id;
    -- insert new register item
    INSERT INTO almacen_balance (materials_id, storage_id, register, brand_id, model_id, balance) VALUES(NEW.materials_id, 'AL01', now(), NEW.brand_id, NEW.model_id, _stk);
    UPDATE almacen_balance SET balance = NEW.stock WHERE materials_id = NEW.materials_id AND brand_id = NEW.brand_id AND model_id = NEW.model_id  AND extract(year FROM register) = extract(year FROM current_date) AND extract(month FROM register) = extract(month FROM current_date);
  END IF;
  RETURN NEW;
EXCEPTION
    WHEN OTHERS THEN
    RAISE INFO 'EXCEPTION ERROR %', SQLERRM;
    ROLLBACK;
    RETURN NULL;
END;
$$
LANGUAGE plpgsql VOLATILE
COST 100;

CREATE TRIGGER tr_register_update_balance
AFTER UPDATE OR INSERT ON almacen_inventorybrand
FOR EACH ROW EXECUTE PROCEDURE proc_register_in_balance();
-- TEST
-- select ABS(-3);
-- SELECT * FROM almacen_detguiaremision;
-- PR16011
-- 342032441900004, 343181560150005, 115100030400040
-- PE16001319, PE16000741
-- 001-00019723

-- SELECT proc_register_in_balance('342032441900004', 'BR011', 'MO022', 1, '-');
-- SELECT * FROM almacen_balance order by register;
-- select * from almacen_inventorybrand where materials_id = '342032441900004';
-- select * from almacen_guiaremision g
-- inner join almacen_pedido pagos
-- on g.pedido_id LIKE p.pedido_id
-- WHERE p.proyecto_id like 'PR16011';
select * from almacen_detpedido where pedido_id like 'PE16001319';
select * from almacen_detguiaremision where guia_id like '001-00019723';
insert into almacen_detguiaremision (guia_id, materiales_id, cantguide, flag, brand_id, model_id, observation, order_id, obrand_id, omodel_id) 
VALUES('001-00019723','342032441900004',4,true,'BR002','MO022','','PE16001319','BR000','MO000');
insert into almacen_detguiaremision (guia_id, materiales_id, cantguide, flag, brand_id, model_id, observation, order_id, obrand_id, omodel_id) 
VALUES('001-00019723','342032441900004',1,true,'BR011','MO022','','PE16001319','BR000','MO000');
--
insert into almacen_detguiaremision (guia_id, materiales_id, cantguide, flag, brand_id, model_id, observation, order_id, obrand_id, omodel_id) 
VALUES('001-00019723','117010610013001',2,true,'BR000','MO000','','PE16001319','BR000','MO000');
-- select * from almacen_detpedido where pedido_id like 'PE16001319';
-- UPDATE almacen_detpedido SET tag = '2' 
-- UPDATE almacen_detpedido SET cantshop = 0 where tag = '2';
-- select * from almacen_detpedido where pedido_id like 'PE16001319' AND materiales_id LIKE '117010610013001';
-- select * from almacen_detguiaremision where guia_id = '001-00019723';
-- delete from almacen_detguiaremision where guia_id = '001-00019723' and materiales_id = '117010610013001';
-- select * from almacen_niple WHERE pedido_id like 'PE16001319';
select * from almacen_balance;
select * from almacen_inventorybrand where materials_id = '115100030400040';
select * from almacen_inventario where materiales_id = '115100030400040';
select * from almacen_balance where materials_id = '115100030400040';
select * from almacen_nipleguiaremision limit 1;

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
  IF FOUND THEN
    _quantity := (_quantity - NEW.cantguide);
    IF _quantity < 0 THEN
      _quantity := 0;
    END IF;
    IF _quantity = 0 THEN
      _tag := '2';
    ELSIF _quantity > 0 THEN
      _tag := '1';
    END IF;
    UPDATE almacen_niple SET cantshop = _quantity, cantguide=(cantguide + NEW.cantguide), tag = _tag WHERE id=NEW.related AND pedido_id LIKE NEW.order_id;
  END IF;
  RETURN NEW;
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

INSERT INTO almacen_nipleguiaremision(guia_id, materiales_id, metrado, cantguide, tipo, flag, brand_id, model_id, related, order_id)
VALUES('001-00000146', '115100030400040', 600, 10, 'B', true, 'BR000', 'MO000', 9774, 'PE16000741');
select * from almacen_detguiaremision where guia_id = '001-00000147';
SELECT * FROM almacen_nipleguiaremision WHERE guia_id = '001-00000147';
SELECT * FROM almacen_niple WHERE pedido_id LIKE 'PE16000741';
SELECT * FROM almacen_pedido WHERE pedido_id LIKE 'PE16000741';
SELECT * FROM almacen_inventorybrand WHERE materials_id = '115100030400040';
SELECT * FROM almacen_inventario WHERE materiales_id = '115100030400040';
SELECT * FROM almacen_balance WHERE materials_id = '115100030400040';

update almacen_pedido set status = 'IN' WHERE pedido_id LIKE 'PE16000741';
DELETE FROM almacen_nipleguiaremision WHERE guia_id = '001-00000146';
select * from almacen_detguiaremision where guia_id = '001-00000146';
DELETE from almacen_detguiaremision where guia_id = '001-00000146';
/* CREATE TRIGGER tr_discount_on_inventorybrand_detpedido
AFTER INSERT ON almacen_detguiaremision
FOR EACH ROW EXECUTE PROCEDURE proc_decrease_inventorybrand_and_detorder();*/
/* END BLOCK NIPPLE GUIDE REMISION*/
do $$
	declare
  x integer;
  a record;
  status char := '';
	begin
  SELECT * FROM almacen_detpedido WHERE pedido_id = 'PE16001319' limit 1 INTO a;
  CASE WHEN a.cantidad = 6 THEN status := '0';
        WHEN a.cantidad < 5 THEN status := '1';
        ELSE status := '2';
  END CASE;
  RAISE INFO '%', status;
	end;
$$
---
-- CREATE TRIGGER FOR INGRESS NOTE
CREATE OR REPLACE FUNCTION proc_add_inventorybrand_detnoteingress()
  RETURNS TRIGGER AS
$$
DECLARE
  _stock DOUBLE PRECISION := 0;
  _invbrand RECORD;
BEGIN
  SELECT INTO _invbrand * FROM almacen_inventorybrand WHERE materials_id = NEW.materials_id AND brand_id = NEW.brand_id AND model_id = NEW.model_id;
  IF FOUND THEN
  -- update old
    _stock := (_invbrand.stock + NEW.quantity);
    UPDATE almacen_inventorybrand SET stock = _stock, purchase = NEW.purchase, sale = NEW.purchase
    WHERE materials_id = NEW.materials_id AND brand_id = NEW.brand_id AND model_id = NEW.model_id;
  ELSE
  -- insert new
    INSERT INTO almacen_inventorybrand(storage_id, period, materials_id, brand_id, model_id, ingress, stock, purchase, sale, flag)
    VALUES('AL01', TO_CHAR(current_date, 'YYYY'), NEW.materials_id, NEW.brand_id, NEW.model_id, now(), NEW.quantity, NEW.purchase, NEW.sales, true);
  END IF;
  RETURN NEW;
EXCEPTION
  WHEN OTHERS THEN
    RAISE INFO 'EXCEPTION ERROR %', SQLERRM;
    ROLLBACK;
    RETURN NULL;
END;
$$
LANGUAGE plpgsql VOLATILE
COST 100;

CREATE TRIGGER tr_add_invetorybrand_noteingress
AFTER INSERT ON almacen_detingress
FOR EACH ROW EXECUTE PROCEDURE proc_add_inventorybrand_detnoteingress();

select * from logistica_detcompra where compra_id = 'OC16000205';
select * from logistica_compra where compra_id = 'OC16000205';
select * from almacen_noteingress where ingress_id = 'NI16000083';
select * from almacen_detingress where ingress_id = 'NI16000083' order by id desc;
select * from almacen_inventorybrand where materials_id = '222128036013015';
select * from almacen_inventario where materiales_id = '222128036013015';
select * from logistica_co
INSERT INTO almacen_detingress(ingress_id, materials_id, quantity, brand_id, model_id, report, flag, purchase, sales)
VALUES('NI16000079', '222128036013015', 5, 'BR000','MO000', 0, true, 2.3, 2.7);
select * from logistica_detcompra where materiales_id = '222128036013015';
/**/
CREATE OR REPLACE FUNCTION proc_change_status_detcompra()
  RETURNS TRIGGER AS
$$
DECLARE
  reg RECORD;
  quantity DOUBLE PRECISION;
  tag CHAR;
  buy varchar(10);
BEGIN
  buy := (SELECT purchase_id FROM almacen_noteingress WHERE ingress_id = NEW.ingress_id LIMIT 1);
  SELECT INTO reg * FROM logistica_detcompra WHERE compra_id = buy AND materiales_id = NEW.materials_id AND brand_id = NEW.brand_id AND model_id = NEW.model_id;
  IF FOUND THEN
    quantity = (reg.cantidad - NEW.quantity);
    CASE WHEN quantity = 0 THEN tag := '2';
          WHEN (quantity >= 0.1) AND (quantity < reg.cantstatic) THEN tag := '1';
          WHEN (quantity = reg.cantstatic) THEN tag := '0';
    END CASE;
    IF quantity < 0 THEN
      quantity := 0;
    END IF;
    UPDATE logistica_detcompra SET flag = tag, cantidad = quantity
    WHERE compra_id = buy AND materiales_id = NEW.materials_id AND brand_id = NEW.brand_id AND model_id = NEW.model_id;
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

CREATE TRIGGER tr_change_status_detcompra
BEFORE INSERT ON almacen_detingress
FOR EACH ROW EXECUTE PROCEDURE proc_change_status_detcompra();

CREATE OR REPLACE FUNCTION proc_change_status_compra()
  RETURNS TRIGGER AS
$$
DECLARE
  _complete INTEGER := 0;
  _total INTEGER := 0;
  _status CHAR(2) := '';
  _compra varchar(10);
BEGIN
  _compra := (SELECT purchase_id FROM almacen_noteingress WHERE ingress_id = NEW.ingress_id LIMIT 1);
  _complete := (SELECT COUNT(*) FROM logistica_detcompra WHERE compra_id = _compra AND flag = '2');
  _total := (SELECT COUNT(*) FROM logistica_detcompra WHERE compra_id = _compra);
  CASE
    WHEN _complete = _total THEN _status := 'CO';
    WHEN _complete < _total THEN _status := 'IN';
    ELSE _status := 'PE';
  END CASE;
  UPDATE logistica_compra SET status = _status WHERE compra_id = _compra;
  RETURN NEW;
EXCEPTION
  WHEN OTHERS THEN
    RAISE INFO 'EXCEPTION ERROR %', SQLERRM;
    ROLLBACK;
    RETURN NULL;
END;
$$
LANGUAGE plpgsql VOLATILE
COST 100;
-- DROP TRIGGER tr_change_status_compra ON almacen_detingress;
CREATE TRIGGER tr_change_status_compra
AFTER INSERT ON almacen_detingress
FOR EACH ROW EXECUTE PROCEDURE proc_change_status_compra();
/*=============*/
-- CREATE TRIGGER FOR STORAGE NRO ORDERS IN BEDSIDE
CREATE OR REPLACE FUNCTION proc_more_order_guide_storage_orders()
  RETURNS TRIGGER AS
$$
BEGIN
  IF OLD.orders IS NULL OR OLD.orders = '' THEN
    NEW.orders := NEW.orders;
  ELSE
    NEW.orders := (OLD.orders || ',' || NEW.orders);
  END IF;
  RETURN NEW;
EXCEPTION
  WHEN OTHERS THEN
    RETURN NEW;
END;
$$
LANGUAGE plpgsql VOLATILE
COST 100;
DROP TRIGGER tr_more_order_guide_storage_orders ON almacen_guiaremision;
CREATE TRIGGER tr_more_order_guide_storage_orders
BEFORE UPDATE ON almacen_guiaremision
FOR EACH ROW WHEN ('GE' = NEW.status)
EXECUTE PROCEDURE proc_more_order_guide_storage_orders();

/* ANNULAR GUIDE REMISION */
CREATE OR REPLACE FUNCTION proc_annular_guide_remision()
  RETURNS trigger AS
$$
DECLARE
  x RECORD;
  oord RECORD;
  np RECORD;
  nstk RECORD;
  so RECORD;
BEGIN
  IF OLD.orders <> NULL OR OLD.orders <> '' THEN
    RAISE INFO 'NEW VERSION';
    -- returns items of guide the orders
    FOR x IN (SELECT * FROM almacen_detguiaremision WHERE guia_id = NEW.guia_id AND flag = True)
    LOOP
      raise info 'det guide %', x;
      -- RETURN ITEM ORDERS
      SELECT INTO oord * FROM almacen_detpedido WHERE pedido_id = x.order_id AND materiales_id = x.materiales_id AND brand_id = x.obrand_id AND model_id = x.omodel_id;
      IF oord.pedido_id IS NOT NULL THEN
        UPDATE almacen_detpedido SET cantshop = (oord.cantshop + x.cantguide), cantguide = (cantguide - x.cantguide), tag = '1', flag = True WHERE pedido_id = x.order_id AND materiales_id = x.materiales_id AND brand_id = x.obrand_id AND model_id = x.omodel_id;
      END IF;
      -- RETURN NIPLES ORDER
      IF EXISTS(SELECT * FROM almacen_nipleguiaremision WHERE guia_id = NEW.guia_id AND materiales_id = x.materiales_id AND order_id = x.order_id) THEN
        FOR np IN (SELECT * FROM almacen_nipleguiaremision WHERE guia_id = NEW.guia_id AND materiales_id = x.materiales_id AND order_id = x.order_id)
        LOOP
          UPDATE almacen_niple SET cantshop=(cantshop+np.cantguide), cantguide=(cantguide-np.cantguide), tag='1' WHERE pedido_id = np.order_id AND id = np.related;
        END LOOP;
      END IF;
      -- RETURN ITEM INVENTORYBRAND
      SELECT INTO nstk * FROM almacen_inventorybrand WHERE materials_id = x.materiales_id AND brand_id = x.brand_id AND model_id = x.model_id;
      UPDATE almacen_inventorybrand set stock = (nstk.stock + x.cantguide) WHERE materials_id = x.materiales_id AND brand_id = x.brand_id AND model_id = x.model_id;
      -- UPDATE STATUS DET GUIDE
      UPDATE almacen_detguiaremision SET flag = false WHERE guia_id = NEW.guia_id AND materiales_id = x.materiales_id AND id = x.id;
    END LOOP;
    -- FOR so IN (SELECT DISTINCT order_id FROM almacen_detguiaremision WHERE guia_id = NEW.guia_id AND order_id IS NOT NULL)
    -- LOOP
    --   IF EXISTS(SELECT * FROM almacen_detpedido WHERE pedido_id = so.order_id AND cantshop > 0) THEN
    --     UPDATE almacen_pedido SET status = 'IN' WHERE pedido_id = so.order_id;
    --   END IF;
    -- END LOOP;
    RAISE NOTICE 'FINISH PROCESS';
  ELSE
    RAISE INFO 'OLD VERSION';
    -- RETURNS ITEMS ORDER
    BEGIN
      FOR x IN (SELECT * FROM almacen_detguiaremision WHERE guia_id = NEW.guia_id AND flag = true)
      LOOP
        -- RAISE INFO 'DET GUIDE %', x;
        -- SELECT INTO oord * FROM almacen_detpedido WHERE pedido_id = NEW.pedido_id AND materiales_id = x.materiales_id AND brand_id = x.brand_id AND model_id = x.model_id;
        -- RAISE INFO 'DET ORDER % ', oord;
        -- IF FOUND THEN
        -- raise info 'INSIDE  IF record NOT NULL % % % %', x.brand_id, x.model_id, x.materiales_id, NEW.pedido_id;
        UPDATE almacen_detpedido SET cantshop=(cantshop + x.cantguide), cantguide=(cantguide - x.cantguide), tag='1', flag=true WHERE pedido_id = NEW.pedido_id AND materiales_id = x.materiales_id AND brand_id = x.brand_id AND model_id = x.model_id;
        RAISE INFO 'IS WHEN UPDATE GUIDE DET REMISIOn';
        UPDATE almacen_detguiaremision SET flag = false WHERE guia_id = NEW.guia_id AND materiales_id = x.materiales_id AND id = x.id;
        -- END IF;
        RAISE INFO 'NIP GUIDE ';
        FOR np IN (SELECT * FROM almacen_nipleguiaremision WHERE guia_id = NEW.guia_id AND materiales_id = x.materiales_id)
        LOOP
          UPDATE almacen_niple SET cantshop=(np.cantguide+cantshop), cantguide=(cantguide-np.cantguide), tag='1' WHERE pedido_id = NEW.pedido_id AND tipo = np.tipo AND materiales_id = np.materiales_id AND metrado = np.metrado;
          UPDATE almacen_nipleguiaremision SET flag = false WHERE id = np.id;
        END LOOP;
        RAISE INFO 'DET ORDER IU inventory ';
        -- RETURN ITEM INVENTORYBRAND
        SELECT INTO nstk * FROM almacen_inventorybrand WHERE materials_id = x.materiales_id AND brand_id = x.brand_id AND model_id = x.model_id;
        IF nstk.materials_id IS NOT NULL THEN
          UPDATE almacen_inventorybrand SET stock = (nstk.stock + x.cantguide) WHERE materials_id = x.materiales_id AND brand_id = x.brand_id AND model_id = x.model_id;
        ELSE
          INSERT INTO almacen_inventorybrand(storage_id,period,materials_id,brand_id,model_id,ingress,stock,purchase,flag,sale)
          VALUES ('AL01',to_char(current_date, 'YYYY'),x.materiales_id,x.brand_id,x.model_id,now(),x.cantguide,1,true,1.15);
        END IF;
      END LOOP;
    END;
    -- IF EXISTS(SELECT * FROM almacen_detpedido WHERE pedido_id = NEW.pedido_id AND cantshop > 0) THEN
    --   UPDATE almacen_pedido SET status = 'IN' WHERE pedido_id = NEW.pedido_id;
    -- END IF;
  END IF;
  RETURN NEW;
EXCEPTION
  WHEN OTHERS THEN
    RAISE NOTICE 'EXCEPTION ERROR % %', SQLERRM, SQLSTATE;
    ROLLBACK;
    RETURN NULL;
END;
$$
LANGUAGE plpgsql VOLATILE
COST 100;
CREATE TRIGGER tr_annular_guide_remision
AFTER UPDATE ON almacen_guiaremision
FOR EACH ROW WHEN (NEW.status = 'AN')
EXECUTE PROCEDURE proc_annular_guide_remision();
/* END ANNULAR GUIDE REMISION*/
select * from almacen_detguiaremision where order_id is not null;
update almacen_guiaremision set status = 'AN' where guia_id = '001-00019723';
update almacen_guiaremision set status = 'GE' where guia_id = '001-10019104';
select * from almacen_guiaremision where guia_id = '001-10019104';
update almacen_detguiaremision set guia_id = '001-10019104' WHERE guia_id = '001-00019723' AND order_id is NULL;
delete from almacen_detguiaremision WHERE id = 14495;
-- Para realizar prueba de anulacion
select * from almacen_guiaremision where guia_id = '001-00019723';
SELECT * from almacen_detguiaremision where guia_id = '001-00019723';
select * from almacen_pedido where pedido_id = 'PE16001319';
select * from almacen_detpedido WHERE pedido_id = 'PE16001319';
select * from almacen_inventorybrand where materials_id in ('117010610013001','342032441900004')
-- ---  ---- 
select * from almacen_guiaremision where guia_id = '001-00000147';
SELECT * from almacen_detguiaremision where guia_id = '001-00000147';
select * from almacen_pedido where pedido_id = 'PE16000741';
select * from almacen_detpedido WHERE pedido_id = 'PE16000741';
SELECT * from almacen_nipleguiaremision where guia_id = '001-00000147';
select * from almacen_niple WHERE pedido_id = 'PE16000741';
select * from almacen_inventorybrand where materials_id in ('115100030400040')

select * from almacen_guiaremision where guia_id = '001-00018508';
SELECT * from almacen_detguiaremision where guia_id = '001-00018508';
select * from almacen_pedido where pedido_id = 'PE16000253';
select * from almacen_detpedido WHERE pedido_id = 'PE16000253';
SELECT * from almacen_nipleguiaremision where guia_id = '001-00018508';
select * from almacen_niple WHERE pedido_id = 'PE16000253';
select * from almacen_inventorybrand where materials_id in ('340012441900005','342032441900004','221098036001007','221098036001006') order by stock desc;
select * from almacen_balance where materials_id in ('340012441900005','342032441900004','221098036001007','221098036001006') order by balance desc;

do $$
declare
  x record;
  c integer;
begin
  -- raise INFO 'is record empty % ', x;
  c:= (select count(*) from almacen_pedido where pedido_id = 'PE16000851');
  raise notice 'Number count pedido %', c;
end;
$$;

