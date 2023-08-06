# paddl: Parse Any DDL

Parse DDLs into objects using python. 

Ambitious title, supported SQL languages include:

- Rudamentary `CREATE TABLE` implemented, pursuing MySQL 8 first.
    - `CONSTRAINTS` parsed, including `FOREIGN KEY`s.


```python
from paddl import parse, ColType

schema = parse("CREATE TABLE employees (id int, name varchar(255));", 'mysql')
table = schema.tables[0]

table.name 
# "employees"

table.columns

column = table.columns[0]
column.name == 'id'
column.type == ColType.INT
```

## command line

`paddl` offers "No Code" CLI solutions, such as rendering ER Diagrams.

```sh
> python -m paddl
usage: paddl [-h] [--erd] sql
```