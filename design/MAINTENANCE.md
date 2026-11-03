# Maintaining this profile

The redesign is original artwork made for Yash Modi. Its visual idea is continuity:
the name breaks into fine particles and reconstructs, while a shaded Möbius surface
forms the O in MODI. The sculpture is drawn from parametric geometry; particle
destinations come from the actual letter shapes. The palette, typography and activity cards are stored
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

The owner's chosen public direction is dark carbon, ivory and warm bronze,
including when a visitor uses GitHub's light theme. The light artwork is retained
as an alternate asset. First-frame PNGs show the fully formed name. The README's
`<picture>` requests the dark static version for reduced-motion preferences.
GitHub also has its own animated-image controls.
All essential facts appear as native Markdown independently of the artwork.
The README pins its hero URLs to the artwork commit so GitHub's raw-image cache
cannot briefly show an earlier design after publication. After a future artwork
change, publish the assets first, then update those three URLs to that commit.
The activity ledger stays on the default branch so weekly updates remain visible.

The particle revision has 300 frames at 40 ms each: 25 fps over a 12-second loop.
The fully formed lettering is held for about 5.4 seconds in total. 4,500 seeded
particles follow eased curves; no new random positions are introduced per frame.
GIF delivery is 960 × 544 with a shared 128-color palette that reserves detail for
the bronze surface, while still artwork is 1200 × 680. The dark GIF is approximately
11 MB; preserve smooth timing and inspect
mobile particle detail if changing that size/quality tradeoff.

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
