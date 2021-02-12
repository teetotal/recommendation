SELECT A.aid AS user, A.spid * 10 + A.grade AS item, A.rating / B.max_rating * 5 AS rating
FROM D20210128_CF_COUNT A
	INNER JOIN D20210128_CF_MAX B
		ON A.aid = B.aid 
	INNER JOIN D20210128_CLUSTER_RESULT C
		ON A.aid = C.aid 
WHERE C.`cluster` = 6
