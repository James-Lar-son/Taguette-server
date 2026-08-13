# Taguette server image.
#
# This starts from the maintainer's official Taguette container and adds
# nothing but our configuration file, so you inherit their tested build
# (including Calibre, which converts uploaded PDFs and Word files).
#
# If Render ever fails to pull this image, see Dockerfile.pypi for a
# self-building fallback.

FROM quay.io/remram44/taguette:latest

COPY config.py /etc/taguette/config.py

# The base image already sets:
#     ENTRYPOINT ["taguette", "--no-browser", "--bind=0.0.0.0"]
# so this line only appends the subcommand and the config path.
CMD ["server", "/etc/taguette/config.py"]
