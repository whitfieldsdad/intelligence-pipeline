# Performance

## OASIS CTI

- A shallow clone of `oasis-open/cti-stix-common-objects` is ~1.1GB in size and takes ~35 seconds to clone

```bash
time git clone https://github.com/oasis-open/cti-stix-common-objects.git
 --depth=1
 ...
 git clone https://github.com/oasis-open/cti-stix-common-objects.git --depth=1  7.42s user 14.43s system 61% cpu 35.279 total
```

- The latest release tarball of `oasis-open/cti-stix-common-objects` is ~63MB in size and takes ~8 seconds to download

```bash
time curl -L https://github.com/oasis-open/cti-stix-common-objects/tarball/master -o cti-stix-common-objects.tar.gz
...
curl -L https://github.com/oasis-open/cti-stix-common-objects/tarball/master   0.62s user 0.37s system 11% cpu 8.481 total
```

- Therefore, it is ~77% faster to download the latest release via a tarball, and the tarball is ~94% smaller than a shallow clone - for stateless workloads, this is preferable.
