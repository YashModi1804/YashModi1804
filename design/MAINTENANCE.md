# Maintaining this profile

The profile introduces Yash Modi, then gives visible evidence of his engineering
work. Its compact identity animation breaks the title-case name into an open
particle cloud and gathers it back into ordinary lettering. Every letter disperses;
there is no sculpture or stationary replacement for the O. The palette, artwork,
project illustrations and activity cards are stored in this repository. The README
contains images and native content, with no embedded animation script or copied
banner template. The existing visitor counter remains an external image.

## Restore the previous profile

`archive/README.before-redesign.md` is an exact copy of the README at commit
`7309c02`, before this redesign. Its SHA-256 is:

```text
5ede94f54b90ad3e84c0db7a7acda417cd7e15f09546a4fee49b1493b580d311
```

To restore the old public profile without deleting the new artwork:

```sh
cp archive/README.before-redesign.md README.md
git add README.md
git commit -m "Restore the previous profile"
git push
```

The original source commit is also retained by the `profile-before-redesign-2026-11-03`
tag. The archive intentionally keeps the original wording and original external
widget URLs. The active README corrects its broken questions link and updates the
role to **Associate Engineer at Oracle**, as requested.

## Artwork and motion

The owner's chosen public direction is dark carbon (`#0B1417`), ivory and a
restrained warm accent, including when a visitor uses GitHub's light theme. The
hero uses a moderate title-case name, the role **Associate Engineer at Oracle ·
India**, and a static supporting line. The quote and learning interests belong in
the native profile content below it. Essential facts remain readable independently
of the animation.

`scripts/render_identity.py` builds the hero using
`scripts/particle_wordmark.py`. The latter seeds **3,000 decorative particles** with
stable paths. Particle destinations are sampled independently of the source glyph
coordinates across a broad ellipse. The choreography is readable hold → staged
breakup → fully dispersed drifting cloud → gathering → readable hold. At maximum
dispersion the solid text mask is entirely absent and the cloud retains no letter
silhouette. This is a designed visual effect, not a physical nanoparticle simulation.

The current delivery assets are:

- `assets/identity-dark.png`: **1200 × 360**, showing the fully formed name.
- `assets/identity-dark.gif`: **960 × 288**, a **12-second** loop with a shared
  **64-color** palette, **6,786,587 bytes** (approximately **6.79 MB**).
- The renderer supplies 300 frames at 40 ms. GIF encoding merges identical holds:
  the current file has **181 encoded frames**, comprising **179 moving frames at
  40 ms**, a **2,040 ms opening hold**, and a **2,800 ms closing hold**. Movement is
  25 fps; the holds remain still. The first and last decoded images are identical.

The README's `<picture>` requests the dark PNG for `prefers-reduced-motion: reduce`.
The active hero uses dark assets in both GitHub themes. A light rendering option
exists, but regenerate and inspect it before linking it; unused older light assets
are not the current public hero.

The raster generators require Pillow and an installed macOS Avenir Next font
collection. They distribute only rendered pixels, never the font files. To rebuild
the current hero from the repository root:

```sh
python3 scripts/render_identity.py --theme dark
```

Use `--still-only` for a fast review. Ignored `assets/.review-*.png` files show
representative breakup, dispersed, gathering and held-name stages. `--font` accepts
another installed font collection; typography and bounds will change. Inspect the
actual GIF, not only contact sheets: confirm complete dispersion, clean gathering,
static role/supporting text, readable pauses, narrow-screen rendering and the loop
seam. Recheck decoded durations and file size after any motion or palette change.

After publication, verify the image GitHub actually serves, since raw-image caches
can briefly retain an earlier asset. If hero URLs are pinned to an artwork commit,
publish the assets first and then update the pin. Keep the activity ledger on the
default branch so weekly updates remain visible.

## Project illustrations, screenshots and navigation

`scripts/render_pipeline.py` generates Folio's architecture illustration:

- `assets/folio-pipeline.gif`: an **8-second** sequence, supplied as 200 frames at
  40 ms, showing document intake, extraction, independent Decimal verification and
  human review.
- `assets/folio-pipeline.png`: the **1200 × 382** still fallback.
- `assets/folio-pipeline-mobile.svg`: a **480 × 648** static vertical layout that
  preserves readable labels on narrow screens.

The example uses two pages, 18 line items and a USD 125.00 discrepancy. Its visible
label is **SYNTHETIC SCENARIO · ARCHITECTURE ILLUSTRATION**. This is an explanation of
the documented workflow, not a product recording, live telemetry, or evidence of a
live provider execution. Keep that distinction visible when changing the diagram.
The README chooses the mobile SVG on narrow screens and the PNG for reduced motion.

`assets/folio-review.png` is different: it is a screenshot of the actual
[public Folio sample console](https://yashmodi1804.github.io/folio-invoice-verification/),
showing the labeled HelixPoint synthetic fixture and its review state. It is real
UI evidence using sample data, **not a claim of live extraction or a live AI call**.
Recapture the labeled public sample state after UI changes and preserve the fixture
caption in the README. No screenshot is generated by the illustration scripts.

`scripts/render_profile_cards.py` uses the Python standard library to generate the
three `contact-*.svg` buttons and `scholarship-workflow.svg`. The latter is a
source-backed overview of student/admin screens and verification records, not a
product screenshot. Link destinations are maintained in the README.

Rebuild these generated assets with:

```sh
python3 scripts/render_pipeline.py
python3 scripts/render_profile_cards.py
```

## Toolkit icons and attribution

`scripts/render_toolkit.py` uses the Python standard library and pinned SVG files
in `assets/icons`; it does not fetch icons while rendering. It embeds their vector
paths into `toolkit-code.svg`, `toolkit-systems.svg`, `toolkit-project.svg` and
`toolkit-project-mobile.svg`, then validates the generated SVGs for duplicate IDs
and unexpected active or external content.

The first two panels preserve the original **14-tool** list. The separate Folio
strip identifies technologies used in that project; it does not silently extend
the original list or imply a proficiency rating.

```sh
python3 scripts/render_toolkit.py
```

Retain [asset attribution](../assets/ATTRIBUTION.md), the exact source records in
`assets/icons/sources.json`, and the vendored license texts when updating icons.
Devicon sources carry their MIT notice; the Pydantic icon from Simple Icons carries
the CC0 text. The renderer prefixes internal SVG identifiers and keeps the original
logo geometry. Collection licenses do not grant trademark rights or imply endorsement.

## Public activity snapshot

The weekly GitHub Actions job fetches public repository data and the anonymous
profile contribution calendar, runs the calculation tests, then rebuilds the two
activity SVGs. It uses the repository's short-lived `GITHUB_TOKEN` for public REST
rate limits, and requests write access only in the update job. No personal API key
or third-party stats host is required. Calendar requests do not send credentials.

Manual refresh: **Actions → Refresh public profile metrics → Run workflow**.
Locally:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/profile_metrics.py
python3 scripts/render_activity.py
```

- Repository counts cover public owned repositories; the card distinguishes forks.
- Stars and language bytes cover original public repositories. HTML is excluded
  from the language mix to preserve the old profile's preference. Language bytes
  measure repository composition, not expertise or time spent.
- Contributions are counts shown by GitHub's public profile. They may include
  anonymized private activity if enabled on the account; they are not commit totals.
- Current and best streaks are bounded by the displayed 365-day window. An unfinished
  current day does not break a streak that was active yesterday.
- The public calendar HTML is not a versioned API. If GitHub changes its markup or
  any request fails, the job fails without publishing partial or fabricated counts.
  The committed snapshot stays visible, with its observation date.

## Checks before publishing

Confirm native identity and toolkit text against `content-inventory.md` and project
claims against their linked source. Verify the original archive's hash; parse the
SVGs; inspect the dark hero's breakup, full dispersion, gathering and holds; and
review the complete profile on a mobile viewport. Check reduced-motion fallbacks,
the fixture/illustration labels, project and contact links, and actual image loading
in GitHub. Verify decoded GIF timing and seam behavior rather than assuming the
source frame count survives encoding. Check the scheduled workflow after changing
the activity fetcher or renderer. Never publish private repository details in the
profile data file.
