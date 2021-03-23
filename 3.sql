--Заказы без Кассового аппарата
WITH ord_without_c AS
(
	SELECT O.row_id, C.name
	FROM stack.Orders AS O
	JOIN stack.Customers AS C
	ON O.customer_id = C.row_id
	WHERE YEAR(O.registered_at) = 2020
	GROUP BY O.row_id, C.name
	EXCEPT
	SELECT O.row_id, C.name
	FROM stack.OrderItems AS I
	JOIN stack.Orders AS O
	ON I.order_id = O.row_id
	JOIN stack.Customers AS C
	ON O.customer_id = C.row_id
	WHERE I.name = 'Кассовый аппарат' AND YEAR(O.registered_at) = 2020
	GROUP BY O.row_id, C.name
)
--Все заказчики за 2020 EXCEPT Заказчики у которых есть заказы без Кассового аппарата
SELECT C.name
FROM stack.Orders AS O
JOIN stack.Customers AS C
ON O.customer_id = C.row_id
WHERE YEAR(O.registered_at) = 2020
GROUP BY C.name
EXCEPT
SELECT ord_without_c.name
FROM ord_without_c