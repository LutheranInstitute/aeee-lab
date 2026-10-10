# environment branch decision

## Date
2026-07-01

## State
computer_use with cua-driver 0.6.8 is not returning usable capture.
Verified: 0x0 result in som and ax modes after driver restart.
Restart is the likely unblock.

## Decision
- Stop active Windows capture/powershell inspection.
- Branch into ubuntu/linux supervisor setup as the active work.
- Revisit cua-driver/fix after restart.
