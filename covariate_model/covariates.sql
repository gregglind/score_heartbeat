SELECT
  count(*)
FROM
  heartbeat_answer
WHERE
  CAST(version as UNSIGNED) >= 25     # 'extras' now have covars
  AND received_ts > (NOW() - INTERVAL 2 months)
  AND is_test =0
  AND survey_id = "heartbeat-by-user-first-impression"
LIMIT 5;
