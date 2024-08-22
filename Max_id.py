WITH LatestUpdates AS (
    SELECT id, MAX(updated_at) AS latest_updated_at
    FROM your_table_name
    GROUP BY id
)
SELECT t.id, t.updated_at
FROM your_table_name t
JOIN LatestUpdates lu
ON t.id = lu.id AND t.updated_at = lu.latest_updated_at
WHERE lu.latest_updated_at >= DATE_SUB(CURRENT_DATE, INTERVAL 1 YEAR);
