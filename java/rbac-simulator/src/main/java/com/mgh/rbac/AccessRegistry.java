package com.mgh.rbac;

import java.util.EnumSet;
import java.util.Locale;
import java.util.Objects;
import java.util.Set;

/** Educational RBAC permission model. Not an enterprise IAM product. */
public final class AccessRegistry {
    public enum Role {
        VIEWER,
        OPERATOR,
        ADMIN
    }

    public enum Permission {
        READ_ASSET,
        UPDATE_ASSET,
        MANAGE_USERS,
        VIEW_AUDIT
    }

    private AccessRegistry() {}

    public static Set<Permission> permissionsFor(Role role) {
        Objects.requireNonNull(role, "role");
        return switch (role) {
            case VIEWER -> EnumSet.of(Permission.READ_ASSET, Permission.VIEW_AUDIT);
            case OPERATOR -> EnumSet.of(
                    Permission.READ_ASSET,
                    Permission.UPDATE_ASSET,
                    Permission.VIEW_AUDIT);
            case ADMIN -> EnumSet.allOf(Permission.class);
        };
    }

    public static boolean isAllowed(Role role, Permission permission) {
        return permissionsFor(role).contains(Objects.requireNonNull(permission, "permission"));
    }

    public static Role parseRole(String raw) {
        try {
            return Role.valueOf(raw.trim().toUpperCase(Locale.ROOT));
        } catch (Exception ex) {
            throw new IllegalArgumentException("Unknown role: " + raw);
        }
    }

    public static Permission parsePermission(String raw) {
        try {
            return Permission.valueOf(raw.trim().toUpperCase(Locale.ROOT));
        } catch (Exception ex) {
            throw new IllegalArgumentException("Unknown permission: " + raw);
        }
    }
}
