SELECT
    id,
    MAX(your_date_column) AS max_date
FROM
    your_table
GROUP BY
    id;
