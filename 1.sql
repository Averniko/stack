IF OBJECT_ID (N'stack.select_orders_by_item_name', N'IF') IS NOT NULL  
    DROP FUNCTION stack.select_orders_by_item_name;  
GO  
CREATE FUNCTION stack.select_orders_by_item_name (@or_id varchar(255))
RETURNS TABLE  
AS  
RETURN   
(  
    SELECT order_id, C.name AS customer, COUNT(order_id) AS items_count
	FROM stack.OrderItems AS I
	JOIN stack.Orders AS O
	ON I.order_id = O.row_id
	JOIN stack.Customers AS C
	ON O.customer_id = C.row_id
	WHERE I.name = @or_id
	GROUP BY I.order_id, C.name
);