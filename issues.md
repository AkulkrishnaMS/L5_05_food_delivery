# Lab 5: Static Code Analysis — Issue Report

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Unsafe pickle deserialization | Security — Medium | 2, 49 | Bandit B301 and B403 flag the use of pickle, which is unsafe when loading untrusted data. | Replace pickle serialization and deserialization with JSON and use safe file handling. |
| Silent exception handling | Reliability / Security — Low | 22–25 | Bandit B110, Pylint W0702, and Flake8 E722 flag a bare exception handler that silently ignores errors. | Validate the order ID and status, handle specific exceptions, and report invalid operations. |
| Mutable default argument | Bug | 11 | Pylint W0102 flags the default list `order_history=[]`, which is shared across calls. | Use `None` as the default and initialize a new list inside the function. |
| Invalid order statuses accepted | Functional bug | 21–25, 62 | The program accepts an unsupported status such as `teleported`. | Check statuses against `VALID_STATUSES` before updating an order. |
| Unknown menu items silently priced | Functional bug | 16, 59 | An unknown menu item such as `sushi` receives a fallback price of 99. | Reject unknown menu items and report a clear validation error. |
| File handling and encoding | Code quality | 30, 43, 49 | Pylint flags missing explicit encoding and file handles that are not managed with context managers. | Use `with open(...)` and specify the encoding where applicable. |
| Naming, documentation and formatting | Code quality / Style | Multiple | Pylint and Flake8 report missing docstrings, nonconforming names, long lines, and blank-line violations. | Add docstrings, use consistent naming, format strings appropriately, and follow PEP 8 spacing and line-length rules. |

## Summary

The original program was analyzed using Pylint, Bandit, and Flake8. The findings include a medium-severity security issue, low-severity security and reliability issues, functional bugs, and code-quality violations. Each issue will be addressed and verified by rerunning the appropriate analysis tools.
