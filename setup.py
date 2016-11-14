"""Installation script for all1input."""
from setuptools import setup, find_packages

setup(
    name='all1input',
    version='1.0alpha',
    description='software kvm',
    author='nihlaeth',
    author_email='info@nihlaeth.nl',
    python_requires='>=3.5',
    packages=find_packages(),
    package_data={'': ['*.crt', '*.key', '*.pem', '*.cfg']},
    extras_require={
        ':sys_platform == "win32"': [],
        ':sys_platform == "darwin"': [
            # AppKit can't be installed on my osx 10.8 box, but
            # can still be imported
            'pyobjc-core', 'pyobjc-framework-Quartz'],
        ':"linux" in sys_platform': ['python3-xlib', 'evdev']},
    entry_points={
        'console_scripts': [
            'all1input_server = all1input.server:start',
            'all1input_client = all1input.client:start',
            'all1input_keys = all1input.cert_manager:start']})
