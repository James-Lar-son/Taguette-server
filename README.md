# taguette-server

My private [Taguette](https://www.taguette.org/) instance — a web app for
uploading documents and coding them qualitatively.

Deployed on [Render](https://render.com) from this repository.

## What's here

| File | Purpose |
| --- | --- |
| `render.yaml` | Render Blueprint: instance size, persistent disk, environment variables |
| `Dockerfile` | Starts from the official Taguette image and adds `config.py` |
| `Dockerfile.pypi` | Fallback build, used only if the official image can't be pulled |
| `config.py` | Server settings, all driven by environment variables — no secrets |

## First-time deploy

1. In Render: **+ New** → **Blueprint** → pick this repository → **Apply**.
2. Watch the **Logs** tab. On the very first start Taguette creates an
   `admin` account and prints its password **once**:

   ```
   Can't prompt for a password, setting admin password to: ...
   ```

   Save that password immediately — email-based reset is not configured.
3. Open the service URL, sign in as `admin`, and change the password
   under **Account**.

## Changing settings later

Edit the relevant `value:` in `render.yaml`, commit, and push. Render
redeploys automatically because `autoDeploy: true`. Your data is on the
persistent disk and is untouched by redeploys.

Common knobs:

- `TAGUETTE_NAME` — title shown in the app
- `REGISTRATION_ENABLED` — set to `"true"` to let a collaborator sign up,
  then back to `"false"`
- `CONVERT_TIMEOUT` — seconds allowed for a document import
- `plan` — bump to `standard` if a large PDF import runs out of memory

## Shell access

Easiest: the **Shell** tab on the service page in the Render dashboard.
No keys, no setup.

From your own terminal, add your public key at **Account Settings → SSH
Public Keys** in Render, then define a host alias in `~/.ssh/config`:

```
Host render-taguette
    HostName ssh.oregon.render.com
    User srv-XXXXXXXXXXXX
    IdentityFile ~/.ssh/render_ed25519
    IdentitiesOnly yes
```

Then `ssh render-taguette` connects, and `ssh render-taguette 'ls /data'`
runs a single command — which is also how to let an agent operate the
server without any SSH plugin.

Note that only `/data` persists. Anything you install or edit over SSH
disappears on the next deploy; durable changes belong in this repo.

### Why the Dockerfile moves `HOME`

The official image sets `HOME=/data`, which is where our persistent disk
mounts. Render's SSH docs state: *"If your service uses a persistent
disk, you must not mount it to the `$HOME` directory of the running
user."* So the Dockerfile sets `HOME=/root` and creates `/root/.ssh` at
mode 0700. No application data moves — `config.py` sets `DATABASE` to an
explicit path on `/data`.

## Backups

The persistent disk is durable but is not a backup. Once a month, open
each project and use **Export project → .sqlite3**, and keep the file
somewhere safe. That single file restores everything — documents,
highlights, codebook — into any Taguette, including the free desktop app.

## Updating Taguette

`Dockerfile` tracks `:latest`. To pull a newer Taguette, trigger
**Manual Deploy → Clear build cache & deploy** in Render. To pin a
specific version instead, change the tag in `Dockerfile` (for example
`quay.io/remram44/taguette:1.5.2`) and push.
