/*
CREATE or replace FUNCTION update_child() RETURNS trigger AS
  $BODY$
BEGIN
  UPDATE child
  set number = NEW.number
  WHERE id = NEW.id;
  RETURN NEW;
END
$BODY$
LANGUAGE plpgsql;

CREATE TRIGGER update_child_after_update
AFTER UPDATE 
ON parent
FOR EACH ROW
EXECUTE PROCEDURE update_child(); 
*/
CREATE OR REPLACE FUNCTION UPDATESTOCK()
RETURNS TRIGGER AS
$BODY$
BEGIN
	UPDATE ALMACEN_INVENTORYBRAND
	SET STOCK = 0
	WHERE materials_id like ''
	and brand_id like ''
	and model_id like ''
	and period like ''
	and storage_id like 'AL01'
END
$BODY$
LANGUAGE plpgsql;

CREATE TRIGGER UPDATE_STOCK_AFTER_INSERT
AFTER INSERT
ON parent -- table name
FOR EACH ROW
EXECUTE PROCEDURE UPDATESTOCK();

