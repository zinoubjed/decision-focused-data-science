-- Sunday-ending calendar labels, matching pandas W-SUN.
WITH RECURSIVE totals AS (
 SELECT date(date, '+' || ((7-CAST(strftime('%w',date) AS INTEGER))%7) || ' days') AS week_end,
 SUM(quantity*price) AS positive_sales FROM lines
 WHERE quantity>0 AND price>0 AND upper(substr(invoice,1,1))<>'C' GROUP BY week_end
 ), calendar(week_end) AS (
 SELECT MIN(week_end) FROM totals UNION ALL
 SELECT date(week_end,'+7 days') FROM calendar WHERE week_end<(SELECT MAX(week_end) FROM totals)
 ) SELECT c.week_end,COALESCE(t.positive_sales,0) AS positive_sales
 FROM calendar c LEFT JOIN totals t USING(week_end) ORDER BY c.week_end