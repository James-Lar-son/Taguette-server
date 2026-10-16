# Taguette server image.
#
# This starts from the maintainer's official Taguette container and adds
# nothing but our configuration file, so you inherit their tested build
# (including Calibre, which converts uploaded PDFs and Word files).
#
# If Render ever fails to pull this image, see Dockerfile.pypi for a
# self-building fallback.

FROM quay.io/remram44/taguette:latest

# --- Keep the persistent disk out of $HOME ------------------------
# The base image sets HOME=/data, and /data is where our Render disk
# mounts. Render's docs are explicit: "If your service uses a persistent
# disk, you must not mount it to the $HOME directory of the running
# user." Doing so breaks shell/SSH access, which needs a ~/.ssh
# directory at mode 0700, and quietly spends disk quota on scratch
# files that were never meant to persist.
#
# Moving HOME does not move any application data: config.py sets
# DATABASE to an explicit path on /data.
ENV HOME=/root
RUN mkdir -p /root/.ssh && chmod 0700 /root/.ssh

COPY config.py /etc/taguette/config.py

# --- Knowledge-graph integration patch -------------------------------
# Adds a "Knowledge Graph" nav link (the public graph viewer) to the top
# bar by replacing Taguette's base template with the patched copy in
# patches/. The patch is upstream base.html (v1.5.2) plus one nav item.
# If a future upstream release changes base.html materially, refresh
# the patch from the new template rather than editing it blind.
COPY patches/base.html /tmp/kg-base.html
RUN python3 -c "import pathlib, shutil, taguette; shutil.copy('/tmp/kg-base.html', pathlib.Path(taguette.__file__).parent / 'templates' / 'base.html')"

# The base image already sets:
#     ENTRYPOINT ["taguette", "--no-browser", "--bind=0.0.0.0"]
# so this line only appends the subcommand and the config path.
CMD ["server", "/etc/taguette/config.py"]
