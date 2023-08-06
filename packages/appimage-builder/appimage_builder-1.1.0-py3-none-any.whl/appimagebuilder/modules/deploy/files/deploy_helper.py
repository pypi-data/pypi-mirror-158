#  Copyright  2020 Alexis Lopez Zubieta
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.

import fnmatch
import glob
import logging
import os
import pathlib
import shutil

from .dependencies_resolver.resolver import Resolver


class FileDeploy:
    """
    Deploy helper that uses the PT_NEEDED entries to resolve dependencies between binaries
    """

    listings = {
        "graphics": [
            "**/libEGL.so*",
            "**/libGL.so*",
            "**/libGLX_mesa.so*",
            "**/libX11-xcb.so*",
            "**/libX11.so",
            "**/libdrm.so*",
            "**/libdrm_*",
            "**/libxcb-glx.so*",
            "**/libxcb-render.so*",
            "**/libxcb-shape.so*",
            "**/libxcb-shm.so*",
            "**/libxcb-xfixes.so*",
            "**/libxcb.so*",
        ],
    }

    def __init__(self, app_dir: str):
        self.app_dir = os.path.abspath(app_dir)
        self.logger = logging.getLogger("FileDeploy")

    def deploy(self, paths: [str]):
        expanded_list = set()
        for path in paths:
            expanded_list = expanded_list.union(glob.glob(path, recursive=True))

        resolver = Resolver()
        expanded_list.update(resolver.resolve(expanded_list))

        for path in expanded_list:
            self._deploy_path(path)

    def _deploy_path(self, path):
        deploy_path = os.path.normpath(self.app_dir + path)

        if not os.path.exists(deploy_path) and os.path.isfile(path):
            self.logger.info("deploying %s" % path)
            os.makedirs(os.path.dirname(deploy_path), exist_ok=True)
            shutil.copy2(path, deploy_path)
        # special files (devices, sockets, etc.) and directories get ignored here

    def _is_a_graphic_library(self, path):
        for pattern in self.listings["graphics"]:
            if fnmatch.fnmatch(path, pattern):
                return True

        return False

    def clean(self, paths: [str]):
        self.logger.info("Removing excluded files")
        base_paths = [
            pathlib.Path(self.app_dir),
            pathlib.Path(self.app_dir) / "runtime" / "compat",
        ]

        for base_path in base_paths:
            for pattern in paths:
                try:
                    for match in base_path.glob(pattern):
                        self.logger.info(match.relative_to(self.app_dir))
                        if match.is_dir():
                            shutil.rmtree(match, ignore_errors=True)
                        else:
                            match.unlink()
                except FileNotFoundError:
                    # it's ok to ignore files that were already deleted
                    pass
