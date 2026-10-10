# ops / experiment decision

## Discovery
- Firecracker is **optional** in the CNCF implementation, not required.
- The user wants a **sandbox container path** that deploys in GCP.
- vhosts localhost setup remains the controlled baseline for eval, not the final target.

## Decision
- **Separate** the experiment spec from the harness config.
- **Run both** in parallel: vhosts localhost + GCP sandbox.
- **Stop** pure vhosts loop if no new signal appears.

## Action
- Lock vhosts at the current working baseline.
- Start CNCF sandbox experiment on GCP next.
