SELECT
  *
FROM
  heartbeat_answer
WHERE
  CAST(variation_id as UNSIGNED) >= 25     # 'extras' now have covars
  AND received_ts > (NOW() - INTERVAL 1 month)
  AND is_test =0
  AND survey_id = "heartbeat-by-user-first-impression"
;
