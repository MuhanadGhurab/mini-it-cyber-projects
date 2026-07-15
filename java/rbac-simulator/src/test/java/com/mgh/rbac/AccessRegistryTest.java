package com.mgh.rbac;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class AccessRegistryTest {
    @Test
    void viewerCannotManageUsers() {
        assertFalse(
                AccessRegistry.isAllowed(
                        AccessRegistry.Role.VIEWER, AccessRegistry.Permission.MANAGE_USERS));
    }

    @Test
    void adminCanManageUsers() {
        assertTrue(
                AccessRegistry.isAllowed(
                        AccessRegistry.Role.ADMIN, AccessRegistry.Permission.MANAGE_USERS));
    }

    @Test
    void operatorCanUpdateAsset() {
        assertTrue(
                AccessRegistry.isAllowed(
                        AccessRegistry.Role.OPERATOR, AccessRegistry.Permission.UPDATE_ASSET));
    }

    @Test
    void parseRoleIsCaseInsensitive() {
        assertEquals(AccessRegistry.Role.VIEWER, AccessRegistry.parseRole("viewer"));
    }

    @Test
    void parsePermissionRejectsUnknown() {
        assertThrows(IllegalArgumentException.class, () -> AccessRegistry.parsePermission("DELETE_ALL"));
    }
}
