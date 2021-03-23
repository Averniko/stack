IF OBJECT_ID (N'stack.calculate_total_price_for_orders_group') IS NOT NULL  
    DROP FUNCTION stack.calculate_total_price_for_orders_group;  
GO  
CREATE FUNCTION stack.calculate_total_price_for_orders_group (@row_id int)
RETURNS int  
AS  
BEGIN
	DECLARE @ret int;
    WITH tree AS
	(
		SELECT row_id
		FROM stack.Orders WHERE row_id = @row_id
		UNION ALL
		SELECT t.row_id
		FROM tree INNER JOIN stack.Orders AS t
		ON t.parent_id = tree.row_id
	)
	SELECT @ret = SUM(price) FROM stack.OrderItems AS I
	JOIN tree as O
	ON I.order_id = O.row_id
	RETURN @ret;
END;