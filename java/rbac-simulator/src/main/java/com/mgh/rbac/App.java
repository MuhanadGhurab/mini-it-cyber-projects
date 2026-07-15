package com.mgh.rbac;

/**
 * Tiny CLI that checks whether a role may perform a permission.
 *
 * <p>Example: {@code java -jar rbac-simulator.jar OPERATOR UPDATE_ASSET}
 */
public final class App {
    private App() {}

    public static void main(String[] args) {
        if (args.length != 2) {
            System.err.println("Usage: rbac-simulator <ROLE> <PERMISSION>");
            System.err.println("Roles: VIEWER, OPERATOR, ADMIN");
            System.err.println("Permissions: READ_ASSET, UPDATE_ASSET, MANAGE_USERS, VIEW_AUDIT");
            System.exit(1);
        }
        try {
            AccessRegistry.Role role = AccessRegistry.parseRole(args[0]);
            AccessRegistry.Permission permission = AccessRegistry.parsePermission(args[1]);
            boolean allowed = AccessRegistry.isAllowed(role, permission);
            System.out.println(allowed ? "ALLOW" : "DENY");
            System.exit(allowed ? 0 : 2);
        } catch (IllegalArgumentException ex) {
            System.err.println("error: " + ex.getMessage());
            System.exit(1);
        }
    }
}
