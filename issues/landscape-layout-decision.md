# Landscape Layout Decision

Parent issue: `issues/005-landscape-mobile-layout-decision.md`

## Representative Mobile Landscape Viewports

Representative checks should use short landscape phone sizes such as:

- 667x375
- 740x360
- 844x390
- 932x430

Real-device Safari iPhone and Chrome Android observations are still recorded in `issues/mobile-qa-checklist.md`.

## Decision

Landscape layout required.

Reason: the current mobile layout is vertically stacked: title, canvas, D-pad, action buttons, and help text. On short landscape phone viewports this creates high risk that controls are pushed below the visible area or require gameplay-disrupting page scroll. A landscape layout should put controls beside the canvas so controls stay reachable, controls do not cover the canvas, and the maze remains readable.

## Required Behavior

- Controls reachable beside the canvas on short landscape phones.
- Controls do not cover the canvas.
- Layout avoids gameplay-disrupting page scroll.
- Portrait layout remains unchanged except for shared CSS variables already introduced by short-portrait tuning.
- Desktop keyboard behavior remains unchanged.

## Implementation Direction

Use a small CSS-only landscape media query for coarse pointers and short heights. Keep the existing HTML order and input JavaScript unchanged. The landscape query should:

- switch the main shell to two columns;
- place the frame/canvas on the left;
- place touch controls on the right;
- hide nonessential help text if vertical space is tight;
- keep D-pad and action buttons thumb-friendly.

## Follow-up Validation

- Re-run Python tests.
- Check representative landscape viewport sizes.
- Fill Safari iPhone and Chrome Android landscape notes in `issues/mobile-qa-checklist.md` when real devices are available.
