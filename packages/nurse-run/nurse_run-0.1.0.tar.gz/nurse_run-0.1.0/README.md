# Nurse run

This package starts and looks after your program, retry when your program fails, and perform the specified action after the number of retries (usually sending an alert notification).

This package works with the python-dotenv package to configure settings via environment variables or .env.

Essentially, this package solves three common types of problems with program running:

- retry
- clean
- alarm

Definition of environment variables:


Name | Description 
----|----
NURSE_RUN_RETRY_TIMES | max retry times
NURSE_RUN_RETRY_DELAY | retry delay (seconds)
NURSE_RUN_CLEANER | Cleanup function (format 'module:func')
NURSE_RUN_ALERTER | Alarm function (format 'module:func')

