#!/usr/bin/env python3
import distutils.cmd
import distutils.log
import os
import subprocess

import setuptools
from setuptools.command.build_py import build_py


class BuildPyCommand(build_py):
    def __init__(self, dist):
        super().__init__(dist)

    def initialize_options(self):
        super(BuildPyCommand, self).initialize_options()
        self.distribution.command_options.update({
            'npm_install': dict(prefix=('BuildPyCommand', 'frontend')),
            'npm_build': dict(prefix=('BuildPyCommand', 'frontend')),
        })

    def run(self):
        self.run_command('npm_install')
        self.run_command('npm_build')
        super(BuildPyCommand, self).run()


class NpmCommand(distutils.cmd.Command):
    user_options = [
        ('prefix=', None, 'Forces to run the command in the specified folder'),
    ]

    def __init__(self, dist):
        self.prefix = None
        self._command = ['npm']
        super().__init__(dist)

    def initialize_options(self):
        self.prefix = None

    def finalize_options(self):
        if self.prefix:
            assert os.path.exists(self.prefix), f'Prefix path {self.prefix} does not exist'
            self._command.extend(['--prefix', self.prefix])

        if self.dry_run:
            self._command.append('--dry-run')

    def run(self):
        self.announce(f"running command '{' '.join(self._command)}'", level=distutils.log.INFO)
        subprocess.check_call(self._command)


class NpmInstallCommand(NpmCommand):
    description = 'Run `npm install` for installing packages'

    def __init__(self, dist):
        super().__init__(dist)
        self._command.append('install')


class NpmBuildCommand(NpmCommand):
    description = 'Run `npm run build` for building the packages'

    def __init__(self, dist):
        super().__init__(dist)
        self._command.extend(['run', 'build'])


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='undeep',
    version='0.1.1',
    use_scm_version={
        'version_scheme': 'post-release'
    },
    author='Bruno Leupi',
    author_email='bruno.leupi@gmail.com',
    description='Document management system with no structure',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/leupibr/undeep',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django :: 3.0',
        'Framework :: Django',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP',
    ],
    python_requires='>=3.6',
    setup_requires=['wheel', 'setuptools_scm'],
    scripts=['manage.py'],
    packages=setuptools.find_packages(),
    package_data={
        'frontend': [
            'templates/*.html',
            'dist/fonts/*',
            'dist/img/*',
            'dist/js/*',
            'dist/app.css',
            'dist/app.css.map',
            'dist/vendor.css',
            'dist/vendor.css.map',
        ]
    },
    cmdclass={
        'build_py': BuildPyCommand,
        'npm_install': NpmInstallCommand,
        'npm_build': NpmBuildCommand,
    }
)
