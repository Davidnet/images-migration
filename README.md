# Image Migrate using Skopeo and Python

Image Migration is a simple project that automatizes moving tag images from one container registry to another container registry. It is also a simple module that showcases the use of AsyncIO and skopeo.

Usage:

```bash
python migrate.py --registry-src docker://gcr.io/light-sunup-244111/machai/machai --destination-src docker://gcr.io/machai-pipelines/production/machai
```

```bash
usage: dry_run.py [-h] --registry-src registry_src --destination-src destination_src
```