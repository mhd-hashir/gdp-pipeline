-- GDP Data Analysis Queries
-- 1. View all data sorted by 2025 GDP (descending)
SELECT *
FROM gdp_data
ORDER BY gdp_2025 DESC;
-- 2. Top 10 Countries by GDP in 2025
SELECT country,
    gdp_2025
FROM gdp_data
ORDER BY gdp_2025 DESC
LIMIT 10;
-- 3. Calculate GDP Growth (2025 vs 2024)
SELECT country,
    gdp_2024,
    gdp_2025,
    (gdp_2025 - gdp_2024) as gdp_growth_nominal,
    ROUND(
        ((gdp_2025 - gdp_2024) / NULLIF(gdp_2024, 0)) * 100,
        2
    ) as growth_percentage
FROM gdp_data
ORDER BY growth_percentage DESC;
-- 4. Compare 2021 vs 2025 for Top 5 Economies
SELECT country,
    gdp_2021,
    gdp_2025
FROM gdp_data
ORDER BY gdp_2025 DESC
LIMIT 5;