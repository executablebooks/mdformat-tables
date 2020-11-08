simple
.
a | bb
- | -
1 | 2
.
| a   | bb  |
| --- | --- |
| 1   | 2   |
.

empty headers
.
|  | |
|- | -
|1 | 2
.
|     |     |
| --- | --- |
| 1   | 2   |
.

no body
.
|  | |
|- | -
.
|     |     |
| --- | --- |
.

alignment
.
a | b | c
:- | -: | :-:
1 | 2 | 3
xxxxxx | yyyyyy | zzzzzz
.
| a      |      b |   c    |
| :----- | -----: | :----: |
| 1      |      2 |   3    |
| xxxxxx | yyyyyy | zzzzzz |
.

nested syntax
.
*a* | [b](link)
- | -
`c` | [d](link)
.
| *a* | [b](link) |
| --- | --------- |
| `c` | [d](link) |
.

paragraph before/after
.
x
a | bb
- | -
1 | 2
y
.
x

| a   | bb  |
| --- | --- |
| 1   | 2   |

y
.

Nested tables in blockquotes:
.
> a|b
> ---|---
> bar|baz
.
> | a   | b   |
> | --- | --- |
> | bar | baz |
.

references
.
| [![a][b]][c] |
| - |
| [![a][b]][c] |

[b]: link1
[c]: link2
.
| [![a][b]][c] |
| ------------ |
| [![a][b]][c] |

[b]: link1
[c]: link2
.
