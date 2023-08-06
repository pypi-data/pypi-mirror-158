#  Copyright  2021 Alexis Lopez Zubieta
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

from appimagebuilder.modules.deploy import FileDeploy
from appimagebuilder.context import BundleInfo
from appimagebuilder.modules.deploy.files.dependencies_resolver.resolver import Resolver
from appimagebuilder.modules.generate.recipe_sections.package_manager_recipe_section_generator import (
    PackageManagerSectionGenerator,
)


class FilesSectionGenerator(PackageManagerSectionGenerator):
    def __init__(self):
        self.exclusion_patterns = set(FileDeploy.listings["graphics"])
        self.exclusion_patterns = self.exclusion_patterns.union(
            [
                # cache files should not be bundle as they will be rebuilt in the host system
                "/var/cache/**/*",
                # fonts cache files
                "/**/fonts/**/*.cache",
                "/**/fonts/**/.uuid",
                "/**/fonts/.uuid",
                # generic icons mime type
                "**/share/mime/generic-icons",
            ]
        )

    def id(self) -> str:
        return "files"

    def generate(self, dependencies: [str], bundle_info: BundleInfo) -> ({}, [str]):
        _root_files = self._exclude_resolvable_dependencies(dependencies)
        _black_list_filter_result = self._exclude_blacklisted(_root_files)

        result = {
            "include": sorted(_black_list_filter_result),
            "exclude": [
                "usr/share/man",
                "usr/share/doc/*/README.*",
                "usr/share/doc/*/changelog.*",
                "usr/share/doc/*/NEWS.*",
                "usr/share/doc/*/TODO.*",
            ],
        }
        return result, []

    def _exclude_blacklisted(self, dependencies):
        return [
            str(path) for path in dependencies if not self._is_file_blacklisted(path)
        ]

    def _is_file_blacklisted(self, file_name):
        for pattern in self.exclusion_patterns:
            if fnmatch.fnmatch(file_name, pattern):
                return True
        return False

    def _exclude_resolvable_dependencies(self, _black_list_filter_result):
        resolver = Resolver()
        file_deps = resolver.resolve(_black_list_filter_result)
        _root_files = set(_black_list_filter_result)
        _root_files.difference_update(file_deps)

        return _root_files
