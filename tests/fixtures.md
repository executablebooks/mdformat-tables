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

Escaped table 1
.
| a |
\| - |
.
| a |
| \- |
.

Escaped table 2
.
a
-\:
.
a
\-:
.

Escaped table 3
.
a
:\-
.
a
:\-
.

Table with inline code and emphasis
.
| *`operation-name`*  | *`operation-object`*  | *`input name`*      | *`processing call`*                                             |
| ------------------- | --------------------- | ------------------- | --------------------------------------------------------------- |
| `attestation`       | `Attestation`         | `attestation`       | `process_attestation(state, attestation)`                       |
| `attester_slashing` | `AttesterSlashing`    | `attester_slashing` | `process_attester_slashing(state, attester_slashing)`           |
| `block_header`      | `BeaconBlock`         | **`block`**         | `process_block_header(state, block)`                            |
| `deposit`           | `Deposit`             | `deposit`           | `process_deposit(state, deposit)`                               |
| `proposer_slashing` | `ProposerSlashing`    | `proposer_slashing` | `process_proposer_slashing(state, proposer_slashing)`           |
| `voluntary_exit`    | `SignedVoluntaryExit` | `voluntary_exit`    | `process_voluntary_exit(state, voluntary_exit)`                 |
| `sync_aggregate`    | `SyncAggregate`       | `sync_aggregate`    | `process_sync_committee(state, sync_aggregate)` (new in Altair) |
.
| *`operation-name`*  | *`operation-object`*  | *`input name`*      | *`processing call`*                                             |
| ------------------- | --------------------- | ------------------- | --------------------------------------------------------------- |
| `attestation`       | `Attestation`         | `attestation`       | `process_attestation(state, attestation)`                       |
| `attester_slashing` | `AttesterSlashing`    | `attester_slashing` | `process_attester_slashing(state, attester_slashing)`           |
| `block_header`      | `BeaconBlock`         | **`block`**         | `process_block_header(state, block)`                            |
| `deposit`           | `Deposit`             | `deposit`           | `process_deposit(state, deposit)`                               |
| `proposer_slashing` | `ProposerSlashing`    | `proposer_slashing` | `process_proposer_slashing(state, proposer_slashing)`           |
| `voluntary_exit`    | `SignedVoluntaryExit` | `voluntary_exit`    | `process_voluntary_exit(state, voluntary_exit)`                 |
| `sync_aggregate`    | `SyncAggregate`       | `sync_aggregate`    | `process_sync_committee(state, sync_aggregate)` (new in Altair) |
.
