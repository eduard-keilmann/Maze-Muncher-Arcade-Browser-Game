# Restart Safety Decision

Parent issue: `issues/006-safer-restart-interaction.md`

## Decision

Safer restart required.

Reason: restart sits near pause in the mobile touch-control cluster. A one-tap restart can erase an active run from an accidental thumb tap. Mobile restart requires deliberate intent, while pause stays one tap for quick interruption.

## Chosen Interaction

Use long press for mobile restart.

- Mobile restart requires deliberate intent through a long press.
- Hold restart for 900 ms to start a new game.
- Releasing, cancelling, or moving away before the timer completes cancels restart.
- Pause stays one tap.
- Desktop restart behavior remains unchanged: Enter still starts/restarts from title or game-over.

## Validation

- Static tests cover the public long-press contract.
- Manual QA should confirm accidental short taps do not restart active gameplay.
- Manual QA should confirm the long-press affordance is discoverable enough on Safari iPhone and Chrome Android.
