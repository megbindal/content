import pytest
from unittest.mock import patch
import os
import networkx as nx

from Tests.Marketplace.packs_dependencies import calculate_single_pack_dependencies


def find_pack_display_name_mock(pack_folder_name):
    return pack_folder_name


class TestCalculateSinglePackDependencies:
    @classmethod
    def setup_class(cls):
        """ setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        patch('demisto_sdk.commands.find_dependencies.find_dependencies.find_pack_display_name',
              side_effect=find_pack_display_name_mock)
        patch('Tests.scripts.utils.log_util.install_logging')
        dependency_graph_mock_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_data", "graph.yml")
        graph = nx.read_yaml(dependency_graph_mock_path)
        dependencies = calculate_single_pack_dependencies('1', graph)
        cls.first_level_dependencies, cls.all_level_dependencies, _ = dependencies

    def test_calculate_single_pack_dependencies_first_level_dependencies(self):
        all_nodes = {'1', '2', '3', '4', '5'}
        expected_first_level_dependencies = {'2', '4'}
        for node in expected_first_level_dependencies:
            assert node in self.first_level_dependencies
        for node in all_nodes - expected_first_level_dependencies:
            assert node not in self.first_level_dependencies

    def test_calculate_single_pack_dependencies_all_levels_dependencies(self):
        all_nodes = {'1', '2', '3', '4', '5'}
        expected_all_level_dependencies = {'2', '3', '4'}
        for node in expected_all_level_dependencies:
            assert node in self.all_level_dependencies
        for node in all_nodes - expected_all_level_dependencies:
            assert node not in self.all_level_dependencies

    def test_calculate_single_pack_dependencies_mandatory_dependencies(self):
        expected_mandatory_dependency = '4'
        assert self.first_level_dependencies[expected_mandatory_dependency]['mandatory']
        for node in self.first_level_dependencies:
            if node != expected_mandatory_dependency:
                assert not self.first_level_dependencies[node]['mandatory']

    @classmethod
    def teardown_class(cls):
        """ teardown any state that was previously setup with a call to
        setup_class.
        """
