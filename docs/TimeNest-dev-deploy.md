# TimeNest-dev Deployment Flow

## Purpose

Use `TimeNest-dev` as the public testing build for PWA cache behavior, mobile/desktop checks, and developer-only route skipping before changes are promoted to the production `TimeNest` GitHub Pages site.

Production URL:
`https://siyingxu.github.io/TimeNest/`

Dev URL:
`https://siyingxu.github.io/TimeNest-dev/`

## Create The GitHub Repository

1. Create a new public GitHub repository named `TimeNest-dev` under the `SiyingXu` account.
2. Do not initialize it with a README, license, or `.gitignore` if pushing from this existing local checkout.
3. Keep GitHub Pages disabled until the first push is complete.

## Files To Push

Push the same static app files used by production:

- `index.html`
- `sw.js`
- `manifest.webmanifest`
- `.nojekyll`
- `assets-manifest.js`
- `supabase-schema.sql`
- `tools/check-assets.ps1`
- `assets/**`

Do not push local preview/tunnel logs such as `.serveo*.log`, `.tunnel*.log`, or `.preview-server*.log`.

## First Push

From a clean local checkout, add the dev remote and push:

```powershell
git remote add dev https://github.com/SiyingXu/TimeNest-dev.git
git push dev main
```

If the remote already exists:

```powershell
git remote set-url dev https://github.com/SiyingXu/TimeNest-dev.git
git push dev main
```

## Enable GitHub Pages

1. Open the `TimeNest-dev` repository on GitHub.
2. Go to `Settings` -> `Pages`.
3. Set source to `Deploy from a branch`.
4. Choose branch `main` and folder `/root`.
5. Save.
6. Wait for GitHub Pages to publish.

Expected testing URL:

```text
https://siyingxu.github.io/TimeNest-dev/
```

Developer-mode testing URL:

```text
https://siyingxu.github.io/TimeNest-dev/?dev=1#rewards
```

## Validation Before Promoting

Run local checks before pushing to `TimeNest-dev`:

```powershell
powershell -ExecutionPolicy Bypass -File tools\check-assets.ps1
node --check sw.js
node --check assets-manifest.js
git diff --check
```

Also verify the inline script syntax with the bundled Node command used by Codex when local `node` is not on PATH.

After deployment, test:

- Normal URL does not show developer tools.
- `?dev=1#rewards` shows only `重启测试` and `无穷金币`.
- In dev mode, clicking any route city asks whether to jump there.
- Confirming a dev jump marks all previous cities' items and tickets complete.
- First load does not precache later chapter image/card assets.
- Mobile and desktop PWA launch, refresh, and offline fallback still work.

## Ongoing Flow

1. Develop locally in `D:\TimeNest`.
2. Run local checks.
3. Push to `TimeNest-dev`.
4. Test desktop/mobile PWA behavior, cache behavior, and `?dev=1`.
5. Once clean, merge or push the same vetted changes to production `TimeNest`.
6. Verify production with a cache-busting URL such as:

```text
https://siyingxu.github.io/TimeNest/?deploy=<commit-sha>
```
