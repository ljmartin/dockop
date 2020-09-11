import psutil


def format_bytes(size):
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'kilo', 2: 'mega', 3: 'giga', 4: 'tera'}
    while size > power:
        size /= power
        n += 1
    return size, power_labels[n]+'bytes'

def get_memory_usage():
    """Return the current memory usage of this algorithm instance,
    or None if this information is not available."""
    num_bytes = psutil.Process().memory_info().rss

    return format_bytes(num_bytes)
