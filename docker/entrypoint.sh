echo "$EAG_CRON_SCHEDULE python -m eero_adguard_sync sync --eero-cookie $EAG_EERO_COOKIE --adguard-host $EAG_ADGUARD_HOST --adguard-user $EAG_ADGUARD_USER --adguard-password $EAG_ADGUARD_PASS -y$EAG_SYNC_FLAGS" | crontab -
exec "$@"
