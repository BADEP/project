# Copyright 2024 Moduon Team S.L. <info@moduon.team>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests.common import TransactionCase

from ..hooks import uninstall_hook


class TestUninstallHook(TransactionCase):
    def test_01_uninstall_hook(self):
        restricted_group = self.env.ref("project.group_project_manager")
        full_group = self.env.ref(
            "project_administrator_restricted_visibility.group_full_project_manager"
        )
        manager_rule = self.env.ref("project.project_project_manager_rule")
        full_rule = self.env.ref(
            "project_administrator_restricted_visibility."
            "project_project_full_manager_rule"
        )
        # Checks Restricted Administrator Group has not project manager rule
        self.assertFalse(manager_rule.active)
        self.assertEqual(manager_rule.group_id, restricted_group)
        # Checks Full Administrator Group has project manager rule
        self.assertEqual(full_rule.group_id, full_group)
        self.assertFalse(full_rule.domain)

        uninstall_hook(self.env)

        # Checks if the rules have been reset
        self.assertTrue(manager_rule.active)
        self.assertFalse(full_group.exists())
        self.assertEqual(restricted_group.name, "Administrator")
