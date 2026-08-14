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

# The base image already sets:
#     ENTRYPOINT ["taguette", "--no-browser", "--bind=0.0.0.0"]
# so this line only appends the subcommand and the config path.
CMD ["server", "/etc/taguette/config.py"]
