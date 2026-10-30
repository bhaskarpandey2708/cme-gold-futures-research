# Trades Schema Specification

> **Source:** [https://databento.com/docs/schemas-and-data-formats/trades](https://databento.com/docs/schemas-and-data-formats/trades)
> **Archived For:** Financial Market Research & Algorithmic Trading Systems

---

# Trades

Tradesprovides every trade event. This is a subset ofMBO.

This is often referred to as "time and sales", "last sale," or "tick data."

Databento groups this undertop of book(L1).

### Fields (trades)

| Field | Type | Description |
| --- | --- | --- |
| ts_recv | uint64_t | The capture-server-received timestamp expressed as the number of nanoseconds since the UNIX epoch. See ts_recv . |
| ts_event | uint64_t | The matching-engine-received timestamp expressed as the number of nanoseconds since the UNIX epoch. See ts_event . |
| rtype | uint8_t | A sentinel value indicating the record type. Always 0 in the trades schema. See Rtype . |
| publisher_id | uint16_t | The publisher ID assigned by Databento, which denotes the dataset and venue. See Publishers . |
| instrument_id | uint32_t | The numeric instrument ID. See Instrument identifiers . |
| action | char | The event action. Always T rade in the trades schema. See Action . |
| side | char | The side that initiates the trade. Can be A sk for a sell aggressor in a trade, B id for a buy aggressor in a trade, or N one where no side is specified. See Side . |
| depth | uint8_t | The book level where the update event occurred. |
| price | int64_t | The order price where every 1 unit corresponds to 1e-9, i.e. 1/1,000,000,000 or 0.000000001. See Prices . |
| size | uint32_t | The order quantity. |
| flags | uint8_t | A bit field indicating event end, message characteristics, and data quality. See Flags . |
| ts_in_delta | int32_t | The matching-engine-sending timestamp expressed as the number of nanoseconds before ts_recv . See ts_in_delta . |
| sequence | uint32_t | The message sequence number assigned at the venue. |

|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

