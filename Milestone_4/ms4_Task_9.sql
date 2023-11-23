WITH CombinedTimestamps AS (
    SELECT
        year,
        CAST(year || '-' || month || '-' || day || ' ' || timestamp AS TIMESTAMP) as full_timestamp
    FROM 
        dim_date_times
),
TimeDifferences AS (
    SELECT
        year,
        full_timestamp - LAG(full_timestamp) OVER (PARTITION BY year ORDER BY full_timestamp) AS time_diff
    FROM 
        CombinedTimestamps
)
SELECT 
    year,
    'hours: ' || EXTRACT(HOUR FROM avg_time) || 
    ', minutes: ' || EXTRACT(MINUTE FROM avg_time) || 
    ', seconds: ' || FLOOR(EXTRACT(SECOND FROM avg_time)) || 
    ', milliseconds: ' || ROUND((EXTRACT(SECOND FROM avg_time) - FLOOR(EXTRACT(SECOND FROM avg_time))) * 1000) AS actual_time_taken
FROM (
    SELECT 
        year,
        AVG(time_diff) AS avg_time
    FROM 
        TimeDifferences
    WHERE 
        time_diff IS NOT NULL
    GROUP BY 
        year
) AS YearlyAvg
ORDER BY 
    actual_time_taken DESC
LIMIT 5