from pkg_resources import get_distribution, DistributionNotFound


try:
    VERSION = get_distribution("eero-adguard-sync").version
except DistributionNotFound:
    VERSION = "__missing__"
