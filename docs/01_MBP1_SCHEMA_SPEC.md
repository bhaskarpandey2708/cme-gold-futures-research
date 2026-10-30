# Market by Price (MBP-1) Level 1 Specification

> **Source:** [https://databento.com/docs/schemas-and-data-formats/mbp-1](https://databento.com/docs/schemas-and-data-formats/mbp-1)
> **Archived For:** Financial Market Research & Algorithmic Trading Systems

---

# Market by price (MBP-1)

MBP-1 (market by price)provides every order book event that updates the top price level, also known as the best bid and offer (BBO). This includes every trade and changes to book depth, alongside total size and order count at the BBO.

This is often called "L1 data".

Databento groups this undertop of book(L1).

### Fields (mbp-1)

| Field | Type | Description |
| --- | --- | --- |
| ts_recv | uint64_t | The capture-server-received timestamp expressed as the number of nanoseconds since the UNIX epoch. See ts_recv . |
| ts_event | uint64_t | The matching-engine-received timestamp expressed as the number of nanoseconds since the UNIX epoch. See ts_event . |
| rtype | uint8_t | A sentinel value indicating the record type. Always 1 in the MBP-1 schema. See Rtype . |
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
| bid_px_00 | int64_t | The bid price at the top level where every 1 unit corresponds to 1e-9, i.e. 1/1,000,000,000 or 0.000000001. See Prices . |
| ask_px_00 | int64_t | The ask price at the top level where every 1 unit corresponds to 1e-9, i.e. 1/1,000,000,000 or 0.000000001. See Prices . |
| bid_sz_00 | uint32_t | The bid size at the top level. |
| ask_sz_00 | uint32_t | The ask size at the top level. |
| bid_ct_00 | uint32_t | The bid order count at the top level. |
| ask_ct_00 | uint32_t | The ask order count at the top level. |

Some venues or data feeds may publish two-sided BBO changes in a single update. In cases like this where thesideis indeterminate, we'll also use the side codeN. Exceptions and edge cases like this can be found in ourVenues and datasetssection.

### Implementation differences between clients and encodings

Bid and ask depth messages (fields starting withbid_andask_) are structured differently in theC++ and Rust clients,the Python record interface, andJSON data. Instead of using the_Nsuffix, they're stored in an array of structures named levels, with the top-of-book at index0.

For example, in C++,levels[5].bid_pxcorresponds tobid_px_05in the Python DataFrame API and CSV format.

MBP-1 has many similarities to the TBBO and BBO schemas. The main distinction is that MBP-1 is in book update space, while TBBO is in trade space, and BBO is in time space. Learn about the differences between each in ourMBP-1 vs. TBBO vs. BBO schemas guide.

#### Consolidated market by price (CMBP-1)

CMBP-1 (consolidated market by price)provides every order book event that updates the top price level across all venues in the dataset, also known as the consolidated best bid and offer (CBBO). This includes every trade and changes to book depth, alongside total size and publisher attribution at the CBBO.

This is often called "L1 data".

### Fields (cmbp-1)

| Field | Type | Description |
| --- | --- | --- |
| ts_recv | uint64_t | The capture-server-received timestamp expressed as the number of nanoseconds since the UNIX epoch. See ts_recv . |
| ts_event | uint64_t | The matching-engine-received timestamp expressed as the number of nanoseconds since the UNIX epoch. See ts_event . |
| rtype | uint8_t | A sentinel value indicating the record type. Always 177 in the CMBP-1 schema. See Rtype . |
| publisher_id | uint16_t | The publisher ID of the event. Refer to the CMBP-1 publisher section below for variants. See Publishers . |
| instrument_id | uint32_t | The numeric instrument ID. See Instrument identifiers . |
| action | char | The event action. Can be A dd, C ancel, M odify, clea R book, or T rade. See Action . |
| side | char | The side that initiates the event. Can be A sk for a sell order (or sell aggressor in a trade), B id for a buy order (or buy aggressor in a trade), or N one where no side is specified. See Side . |
| price | int64_t | The order price where every 1 unit corresponds to 1e-9, i.e. 1/1,000,000,000 or 0.000000001. See Prices . |
| size | uint32_t | The order quantity. |
| flags | uint8_t | A bit field indicating event end, message characteristics, and data quality. See Flags . |
| ts_in_delta | int32_t | The matching-engine-sending timestamp expressed as the number of nanoseconds before ts_recv . See ts_in_delta . |
| bid_px_00 | int64_t | The bid price at the top level where every 1 unit corresponds to 1e-9, i.e. 1/1,000,000,000 or 0.000000001. See Prices . |
| ask_px_00 | int64_t | The ask price at the top level where every 1 unit corresponds to 1e-9, i.e. 1/1,000,000,000 or 0.000000001. See Prices . |
| bid_sz_00 | uint32_t | The bid size at the top level. |
| ask_sz_00 | uint32_t | The ask size at the top level. |
| bid_pb_00 | uint16_t | The publisher ID indicating the venue containing the best bid. See Publishers . |
| ask_pb_00 | uint16_t | The publisher ID indicating the venue containing the best ask. See Publishers . |

Some venues or data feeds may publish two-sided CBBO changes in a single update. In cases like this where thesideis indeterminate, we'll also use the side codeN. Exceptions and edge cases like this can be found in ourVenues and datasetssection.

### CMBP-1 publisher

The value used to populate thepublisher_idfield will vary depending on theaction. ForTrades,publisher_idwill correspond to the venue the trade executed on. For all other actions,publisher_idwill be the consolidated publisher ID for the dataset.

In all scenarios,bid_pb_00andask_pb_00will represent the venues showing the NBBO.

### Implementation differences between clients and encodings

Bid and ask depth messages (fields starting withbid_andask_) are structured differently in theC++ and Rust clients,the Python record interface, andJSON data. Instead of using the_Nsuffix, they're stored in an array of structures named levels, with the top-of-book at index0.

For example, in C++,levels[5].bid_pxcorresponds tobid_px_05in the Python DataFrame API and CSV format.

CMBP-1 has many similarities to the TCBBO and CBBO schemas. The main distinction is that CMBP-1 is in book update space, while TCBBO is in trade space, and CBBO is in time space. Learn about the differences between each in ourCMBP-1 vs. TCBBO vs. CBBO schemas guide.

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

