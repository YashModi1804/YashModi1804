# Maintaining this profile

The redesign is original artwork made for Yash Modi. Its visual idea is continuity:
a shaded Möbius surface, drawn from its parametric geometry and animated through a
complete turn. The palette, typography, illustrations and activity cards are stored
in this repository. There is no animation service, embedded script, or copied banner
template in the profile. The existing visitor counter remains an external image.

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

`assets/identity-light.gif` and `assets/identity-dark.gif` contain 192 frames in a
12.48-second seamless loop. Each file is below 5 MB. First-frame PNGs provide still
artwork. GitHub's native `<picture>` support selects the theme; reduced-motion
sources request the static version. GitHub also has its own animated-image controls.
All essential facts appear as native Markdown independently of the artwork.

The image generators do not bundle fonts. The identity was rendered with macOS
Avenir Next; only the resulting pixels are distributed. To regenerate on the same
machine, install Pillow and run:

```sh
python3 scripts/render_identity.py
```

Use `--still-only` for a fast art review. Files named `assets/.review-*.png` show
quarter-cycle poses and are ignored by Git. `--font` accepts another installed font
collection; output typography will differ. Check every pose and narrow-screen
readability after changing the geometry. These frames are decorative artwork,
not performance telemetry or a representation of Oracle technology.

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

Confirm native text against `content-inventory.md`; verify the original archive's
hash; parse the SVGs; inspect both themes, intermediate GIF frames and a mobile
viewport; confirm image requests and motion in the rendered GitHub profile. Check
the scheduled workflow after changing the fetcher or renderer. Never publish private
repository details in the profile data file.
