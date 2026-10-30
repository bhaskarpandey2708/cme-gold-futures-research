# Market by Price (MBP-10) Level 2 Specification

> **Source:** [https://databento.com/docs/schemas-and-data-formats/mbp-10](https://databento.com/docs/schemas-and-data-formats/mbp-10)
> **Archived For:** Financial Market Research & Algorithmic Trading Systems

---

# Market by price (MBP-10)

MBP-10 (market by price)provides every order book event across the top ten price levels, keyed by price. This includes every trade and changes to aggregate market depth, alongside total size and order count at the top ten price levels.

This is often called "L2 data".

Databento groups this undermarket depth(L2).

### Fields (mbp-10)

| Field | Type | Description |
| --- | --- | --- |
| ts_recv | uint64_t | The capture-server-received timestamp expressed as the number of nanoseconds since the UNIX epoch. See ts_recv . |
| ts_event | uint64_t | The matching-engine-received timestamp expressed as the number of nanoseconds since the UNIX epoch. See ts_event . |
| rtype | uint8_t | A sentinel value indicating the record type. Always 10 in the MBP-10 schema. See Rtype . |
| publisher_id | uint16_t | The publisher ID assigned by Databento, which denotes the dataset and venue. See Publishers . |
| instrument_id | uint32_t | The numeric instrument ID. See Instrument identifiers . |
| action | char | The event action. Can be A dd, C ancel, M odify, clea R book, or T rade. See Action . |
| side | char | The side that initiates the event. Can be A sk for a sell order (or sell aggressor in a trade), B id for a buy order (or buy aggressor in a trade), or N one where no side is specified. See Side . |
| depth | uint8_t | The book level where the update event occurred. |
| price | int64_t | The order price where every 1 unit corresponds to 1e-9, i.e. 1/1,000,000,000 or 0.000000001. See Prices . |
| size | uint32_t | The order quantity. |
| flags | uint8_t | A bit field indicating event end, message characteristics, and data quality. See Flags . |
| ts_in_delta | int32_t | The matching-engine-sending timestamp expressed as the number of nanoseconds before ts_recv . See ts_in_delta . |
| sequence | uint32_t | The message sequence number assigned at the venue. |
| bid_px_N | int64_t | The bid price at level N (top level if N = 00) where every 1 unit corresponds to 1e-9, i.e. 1/1,000,000,000 or 0.000000001. See Prices . |
| ask_px_N | int64_t | The ask price at level N (top level if N = 00) where every 1 unit corresponds to 1e-9, i.e. 1/1,000,000,000 or 0.000000001. See Prices . |
| bid_sz_N | uint32_t | The bid size at level N (top level if N = 00). |
| ask_sz_N | uint32_t | The ask size at level N (top level if N = 00). |
| bid_ct_N | uint32_t | The bid order count at level N (top level if N = 00). |
| ask_ct_N | uint32_t | The ask order count at level N (top level if N = 00). |

### Implementation differences between clients and encodings

Bid and ask depth messages (fields starting withbid_andask_) are structured differently in theC++ and Rust clients,the Python record interface, andJSON data. Instead of using the_Nsuffix, they're stored in an array of structures named levels, with the top-of-book at index0.

For example, in C++,levels[5].bid_pxcorresponds tobid_px_05in the Python DataFrame API and CSV format.

It is possible to construct MBP-10 yourself from MBO data if you want more price levels or prefer to reduce your bandwidth use. Learn how to construct a limit order book from MBO data from ourlimit order book constructiontutorial.

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
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

