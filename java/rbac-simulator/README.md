# RBAC Simulator

Educational role-based access control decision helper.

| Status | Functional Prototype |
|--------|----------------------|

## Purpose

Demonstrate a clear permission matrix (VIEWER / OPERATOR / ADMIN) for interviews and learning. This is **not** a production IAM system.

## Usage

```bash
mvn -q test
mvn -q -DskipTests package
java -jar target/rbac-simulator-0.1.0.jar OPERATOR UPDATE_ASSET
```

## Matrix

| Role | READ_ASSET | UPDATE_ASSET | MANAGE_USERS | VIEW_AUDIT |
|------|------------|--------------|--------------|------------|
| VIEWER | yes | no | no | yes |
| OPERATOR | yes | yes | no | yes |
| ADMIN | yes | yes | yes | yes |

## Limitations

- In-memory only
- No authentication, persistence, or auditing subsystem
- Not suitable as a real authorization service
