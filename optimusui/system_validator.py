from optimusui import prime_select, pci_utils, os_utils


def is_system_supported() -> bool:
    has_prime_select = prime_select.has_prime_select()
    has_nvidia_gpu = pci_utils.has_nvidia_gpu()
    has_supported_prime_tool = os_utils.is_distro_supported()

    return has_prime_select and has_nvidia_gpu and has_supported_prime_tool
