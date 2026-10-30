# Databento Symbology Standards (Continuous, Parent, Raw)

> **Source:** [https://databento.com/docs/standards-and-conventions/symbology](https://databento.com/docs/standards-and-conventions/symbology)
> **Archived For:** Financial Market Research & Algorithmic Trading Systems

---

# Symbology

Financial datasets usually contain symbols orproductidentifiers. The mapping of symbols to their corresponding product names can be extracted from ourdefinition schemaas well as the metadata packaged with our data.

Databento supports four symbology types, also referred to asstypes. They are:raw_symbol,instrument_id,parent, andcontinuous.

We include methods for mapping between symbology types and resolving symbols under thesymbologyfamily of methods.

We do not retroactively reassign symbols in our historical data. Symbols found in our historical data are exactly as they appeared in the live data at the original event time. For example, if a stock symbol was changed due to a corporate action, we preserve the original symbol for data before the event and the new symbol for data after the event. This approach guarantees that the historical data looks identical to the live data at the original time, and encourages our users to write their integration in a manner that handles historical and live data in the same way.

A symbol can be reused and point to two different instruments on two different dates.

### Supported symbology combinations

When requesting data, such as with thetimeseries.get_rangeorbatch.submit_jobendpoints, an input (stype_in) and output (stype_out) symbology type are specified. Not all symbology types are supported for output and some symbology types are not available in certain datasets.

| stype_in â / stype_out â | instrument_id | raw_symbol | parent | continuous |
| --- | --- | --- | --- | --- |
| instrument_id | â | â |  |  |
| raw_symbol | â |  |  |  |
| parent | â |  |  |  |
| continuous | â |  |  |  |

All datasets support bidirectional conversion betweenraw_symbolandinstrument_id.

The table below outlines the datasets that supportparent symbologyandcontinuous contract symbology(futures contracts only).

| stype_in | parent | continuous |
| --- | --- | --- |
| GLBX.MDP3 | â | â |
| IFEU.IMPACT | â | â |
| IFLL.IMPACT | â | â |
| IFUS.IMPACT | â | â |
| NDEX.IMPACT | â | â |
| OPRA.PILLAR | â |  |
| XCBF.PITCH | â | â |
| XEEE.EOBI | â | â |
| XEUR.EOBI | â | â |

### Raw symbol

Raw symbols are the original string symbols used by the publisher in the source data. This can be useful for environments with direct market connectivity. Examples of raw symbols includeAAPL,ESH3, etc.

This symbology is used by setting thestype_in=raw_symbolparameter in the API.

#### CMS vs. Nasdaq symbology in US equities

In US equities, the same security may carry slightly different ticker symbols across venues. The two competing conventions areNasdaqandCMS(CTA/UTP Consolidated Market System). For multi-class shares, units, warrants, preferred shares, and similar securities, the conventions differ in the suffix delimiter and codes used:

| Security | Nasdaq | CMS |
| --- | --- | --- |
| Berkshire Hathaway Class B | BRK.B | BRK B |
| AAC Holdings warrant | AAC+ | AAC WS |
| Heico Class A | HEI.A | HEI A |
| Moog Class A | MOG.A | MOG A |

The reference for the suffix mappings is theNasdaq Symbol Conventiondocument.

raw_symbolreturns the symbol as published by the source, so the convention varies with the dataset. The table below shows the convention for each US equities dataset:

| Dataset | Native convention |
| --- | --- |
| ARCX.PILLAR | CMS |
| BATS.PITCH | Nasdaq |
| BATY.PITCH | Nasdaq |
| EDGA.PITCH | Nasdaq |
| EDGX.PITCH | Nasdaq |
| EPRL.DOM | Nasdaq |
| EQUS.MINI | Nasdaq |
| EQUS.SUMMARY | Nasdaq |
| IEXG.TOPS | Nasdaq |
| MEMX.MEMOIR | CMS |
| OCEA.MEMOIR | CMS |
| XASE.PILLAR | CMS |
| XBOS.ITCH | Nasdaq |
| XCHI.PILLAR | CMS |
| XCIS.TRADESBBO | CMS |
| XNAS.BASIC | Nasdaq |
| XNAS.ITCH | Nasdaq |
| XNYS.PILLAR | CMS |
| XPSX.ITCH | Nasdaq |

### Instrument ID

Instrument IDs are the unique numeric ID assigned to each instrument by the publisher. Most venues use such numeric IDs under the hood. Numeric IDs have the benefit of taking less space than most string symbols. However, numeric IDs can be difficult to work with, especially as some publishers remap them daily.

This symbology is used by setting thestype_in=instrument_idparameter in the API.

### Parent

Parent symbology is a smart symbology feature that allows you to easily refer to groups of related symbols using a single root symbol. The root symbols are sourced from theassetfield of thedefinition schema. All futures for a root symbol can be referenced using the parent symbol[ROOT].FUT, for options:[ROOT].OPT. For example,ES.FUTrefers to all E-mini S&P 500 futures and futures spreads andES.OPTrefers to all quarterly E-mini S&P 500 options and option spreads.

The type of instrument will be specified in theinstrument_classfield. When requesting data using futures parent symbology, this field will indicate whether the instrument is a future or futures spread. When requesting data using options parent symbology, it will indicate whether the instrument is a call or put. A full list of variants can be found in theinstrument class documentation.

This symbology is used by setting thestype_in=parentparameter in the API.

### Continuous

Our continuous contract symbology is a notation that maps to an actual, tradable instrument on any given date. The continuous contract prices returned are the original, unadjusted prices. We don't create a synthetic time series by back-adjusting the prices to remove jumps during rollovers.

Continuous contract symbology is a smart symbology feature that allows a single symbol to refer to different instruments over time. For example, continuous contract symbology allows you to query a single symbol that changes orrollsforward before expiration.

For futures outrights, we use the format[ROOT].[ROLL_RULE].[RANK]to refer to continuous contracts that change over time according to a roll rule and rank. Like with parent symbology, the root symbol corresponds with theassetfield of thedefinition schema.

RANKis a zero-indexed integer, andROLL_RULEis eitherc,n, orvfrom the table below.

This symbology is used by setting thestype_in=continuousparameter in the API. It is not currently possible to select continuous contracts through our web portal.

| Roll rule | Code | Overview | Example |
| --- | --- | --- | --- |
| Calendar | c | Refers to the offset from the closest expiration or front month. | On September 28, 2022 NG.c.0 referred to the October NG future (NGV2) and NG.c.1 referred to the November future (NGX2). However, because the October contract expired at the end of trading on September 28 and the continuous smart symbol would be rolled forward, on September 29, 2022, NG.c.0 then referred to the November future (NGX2) and NG.c.1 referred to the December future (NGZ2). |
| Open interest | n | Will rank the expirations by the open interest at the previous day's close. | CL.n.1 refers to the CL future with the second-highest open interest. |
| Volume | v | Will rank the expirations by the previous day's trading volume. | ZN.v.0 refers to the ZN future with the most volume. |

### All symbols

It is possible to request all symbols within a dataset without providing them explicitly. This is done by specifyingALL_SYMBOLSwithstype_in=raw_symbolorstype_in=parentin the API.

When requesting all symbols usingtimeseries.get_rangesymbology data is not provided. This means that for the CSV and JSON encodings the parametermap_symbols=Trueis not allowed. For the DBN encoding, the metadata header will not contain symbology mappings.

When requesting all symbols usingbatch.submit_job, thesymbology.jsonsupport file will not contain symbology mappings.

### Symbology.resolve endpoint

Databento offers symbology resolution for free in oursymbology.resolve endpointand in our client libraries. This endpoint can be used to request mappings from one symbology type to another and contains all the data necessary to perform these conversions.

| Field | Description |
| --- | --- |
| result | The symbology mapping result. For each requested symbol, a list of symbology mappings is provided. |
| symbols | The requested symbols. |
| stype_in | The requested input symbology type. |
| stype_out | The requested output symbology type. |
| start_date | The requested symbology start date, as an ISO 8601 date string. |
| end_date | The requested symbology end date, as an ISO 8601 date string. |
| partial | The list of symbols, if any, that partially resolved inside the start date and end date interval. |
| not_found | The list of symbols, if any, that failed to resolve inside the start date and end date interval. |
| message | A short message indicating the overall symbology result. Can be one of: "OK", "Not found", or "Partially resolved". |
| status | A numerical status field indicating the overall symbology result. Can be one of: 0 (OK), 1 (Partially resolved), or 2 (Not found). |

### Symbology support file

For some batch downloads, symbology information for the job is contained in*.symbology.jsonsupport files. This file is automatically included when the batch job files do not contain symbology information, such as when requesting CSV or JSON encodings when symbol mapping is not requested. Below is a sample file. It's contents are directly obtained from thesymbology.resolveendpoint:

```python
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
```

```python
{
   "result": {
      "ES.c.0": [
         { "d0": "2023-01-01", "d1": "2023-03-19", "s": "206299"},
         { "d0": "2023-03-19", "d1": "2023-06-01", "s": "95414"}
      ]
   },
   "symbols": ["ES.c.0"],
   "stype_in": "continuous",
   "stype_out": "instrument_id",
   "start_date": "2023-01-01",
   "end_date": "2023-06-01",
   "partial": [],
   "not_found": [],
   "message": "OK",
   "status": 0
}
```

Examining this sample we can see a requested mapping of thestype_in("continuous")symbol("ES.c.0") tostype_out("instrument_id") over the date rangestart_date("2023-01-01") to theend_date("2023-06-01").

We can check themessage("OK") andstatus(0) fields to confirm that our request was successful over the entire date interval. Additionally, thenot_foundandpartialfields are empty.

Most importantly, theresultfield contains our symbology mappings keyed by each inputsymbol. Eachsymbolentry in theresultmapping will contain a list of entries. These entries contain a start date in thed0field, and an end date in thed1field for the mapping. Thesfield contains the output symbol.

| Continuous contract | Start date (d0) | End date (d1) | Instrument ID (s) |
| --- | --- | --- | --- |
| ES.c.0 | 2023-01-01 | 2023-03-19 | 206299 |
| ES.c.0 | 2023-03-19 | 2023-06-01 | 95414 |

### SymbolMappingMsg

Databento's live data publishes symbology information using theSymbolMappingMsg. This message will always contain the input symbol and the resolved output symbol. The record header of theSymbolMappingMsgwill always contain theinstrument_id. See ourDBN encodingarticle for more information on our binary format.

| Field | Type | Description |
| --- | --- | --- |
| stype_in | uint8_t | The input symbology type (DBN version 2 only). |
| stype_in_symbol | char[symbol_cstr_len] | The input symbol from the subscription, where symbol_cstr_len is specified in the Metadata . |
| stype_out | uint8_t | The output symbology type (DBN version 2 only). Will always be raw_symbol . |
| stype_out_symbol | char[symbol_cstr_len] | The output symbol from the subscription, where symbol_cstr_len is specified in the Metadata . |
| start_ts | uint64_t | The start of the mapping interval expressed as the number of nanoseconds since the UNIX epoch. |
| end_ts | uint64_t | The end of the mapping interval expressed as the number of nanoseconds since the UNIX epoch. |

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |

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
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

|  |  |  |  |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

|  |  |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |

```python

```

```python

```

|  |  |  |  |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |

|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

