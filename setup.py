"""Installation script for all1input."""
from setuptools import setup, find_packages

setup(
    name='all1input',
    version='1.0alpha',
    description='software kvm',
    author='nihlaeth',
    author_email='info@nihlaeth.nl',
    packages=find_packages(),
    package_data={'': ['*.crt', '*.key', '*.pem', '*.cfg']},
    extras_require={
        ':sys_platform == "win32"': [],
        ':sys_platform == "darwin"': [
            'pyobjc-core', 'pyobjc', 'pyobjc-framework-Quartz', 'AppKit'],
        ':"linux" in sys_platform': ['python3-xlib', 'evdev']},
    entry_points={
        'console_scripts': [
            'all1input_server = all1input.server:start',
            'all1input_client = all1input.client:start',
            'all1input_keys = all1input.cert_manager:start']})
