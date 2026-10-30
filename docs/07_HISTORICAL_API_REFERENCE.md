# Historical API Reference & Endpoints

> **Source:** [https://databento.com/docs/api-reference-historical](https://databento.com/docs/api-reference-historical)
> **Archived For:** Financial Market Research & Algorithmic Trading Systems

---

# API reference - Historical

Databento's historical data service can be accessed programmatically over its HTTP API. To make it easier to integrate the API, we also provide official client libraries that simplify the code you need to write.

Our HTTP API is designed as a collection of RPC-style methods, which can be called using URLs in the formhttps://hist.databento.com/v0/METHOD_FAMILY.METHOD.

Our client libraries wrap these HTTP RPC-style methods with more idiomatic interfaces in their respective languages.

You can use our API tostreamor load data directly into your application. You can also use our API to makebatch downloadrequests, which instruct our service to prepare the data as flat files that can be downloaded from theDownload center.

## Basics

### Overview

Our historical API has the following structure:

### Overview

Our historical API has the following structure:

### Overview

Our historical API has the following structure:

### Overview

Our historical API has the following structure:

### Authentication

Databento uses API keys to authenticate requests. You can view and manage your keys on theAPI keyspage of your portal.

Each API key is a 32-character string. The library will use the environment variableDATABENTO_API_KEYas your API key if theSetKeyFromEnvmethod is called. However, you can pass an API key directly to theHistoricalBuilderthrough theSetKeymethod. Calling theBuildmethod constructs and returns an instance ofHistorical, the historical client.

Related:Securing your API keys.

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
```

```python
#include <databento/historical.hpp>
#include <iostream>

// Establish connection and authenticate
auto client =
    databento::Historical::Builder().SetKeyFromEnv().Build();

// Authenticated request
auto datasets = client.MetadataListDatasets();
for (const auto& dataset : datasets) {
  std::cout << dataset << ", ";
}
std::cout << '\n';
```

### Authentication

Databento uses API keys to authenticate requests. You can view and manage your keys on theAPI keyspage of our web platform.

Each API key is a 32-character string starting withdb-.

Our HTTP API authenticates requests using the HTTP basic auth scheme, which takes a username and password. Use your API key as the username and leave the password blank.

```python
1
2
```

```python
curl -G 'https://hist.databento.com/v0/metadata.list_datasets' \
 -u $YOUR_API_KEY:
```

Appending a colon (:) after$YOUR_API_KEYpreventscurlfrom asking for a password.

Related:Securing your API keys.

### Authentication

Databento uses API keys to authenticate requests. You can view and manage your keys on theAPI keyspage of your portal.

Each API key is a 32-character string starting withdb-. By default, our library uses the environment variableDATABENTO_API_KEYas your API key. However, if you pass an API key to theHistoricalconstructor through thekeyparameter, then this value will be used instead.

Related:Securing your API keys.

```python
1
2
3
4
5
6
7
```

```python
import databento as db

# Establish connection and authenticate
client = db.Historical("$YOUR_API_KEY")

# Authenticated request
print(client.metadata.list_datasets())
```

### Authentication

Databento uses API keys to authenticate requests. You can view and manage your keys on theAPI keyspage of your portal.

Each API key is a 32-character string starting withdb-.

The library will use the environment variableDATABENTO_API_KEYas your API key if thekey_from_envmethod is called. However, you can pass an API key directly to thehistorical::ClientBuilderthrough thekeymethod. Calling thebuildmethod constructs and returns an instance ofHistoricalClient.

Related:Securing your API keys.

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
```

```python
use databento::HistoricalClient;

// Establish connection and authenticate
let mut client =
    HistoricalClient::builder().key_from_env()?.build()?;

// Authenticated request
let datasets = client.metadata().list_datasets(None).await?;
for dataset in datasets {
    println!("{dataset}");
}
```

### Schemas and conventions

A schema is a data record format represented as a collection of different data fields. Our datasets support multiple schemas, such as order book, trades, bar aggregates, and so on. You can see a full list from ourList of market data schemas.

You can get a list of all supported schemas for any given dataset using theMetadataListSchemasmethod. The same information can also be found on each dataset's detail page found through theExplorefeature.

The following table provides details about the data types and conventions used for various fields that you will commonly encounter in the data.

| Name | Field | Description |
| --- | --- | --- |
| Dataset | dataset | A unique string name assigned to each dataset by Databento. Full list of datasets can be found from the metadata . |
| Publisher ID | publisher_id | A unique 16-bit unsigned integer assigned to each publisher by Databento. Full list of publisher IDs can be found from the metadata . |
| Instrument ID | instrument_id | A unique 32-bit unsigned integer assigned to each instrument by the venue. Information about instrument IDs for any given dataset can be found in the symbology . |
| Order ID | order_id | A unique 64-bit unsigned integer assigned to each order by the venue. |
| Timestamp (event) | ts_event | The matching-engine-received timestamp expressed as the number of nanoseconds since the UNIX epoch . |
| Timestamp (receive) | ts_recv | The capture-server-received timestamp expressed as the number of nanoseconds since the UNIX epoch . |
| Timestamp delta (in) | ts_in_delta | The matching-engine-sending timestamp expressed as the number of nanoseconds before ts_recv . See timestamping guide. |
| Timestamp out | ts_out | The Databento gateway-sending timestamp expressed as the number of nanoseconds since the UNIX epoch . See timestamping guide. |
| Price | price | The price expressed as signed integer where every 1 unit corresponds to 1e-9, i.e. 1/1,000,000,000 or 0.000000001. |
| Book side | side | The side that initiates the event. Can be A sk for a sell order (or sell aggressor in a trade), B id for a buy order (or buy aggressor in a trade), or N one where no side is specified by the original source. |
| Size | size | The order quantity. |
| Flag | flag | A bit field indicating event end, message characteristics, and data quality. |
| Action | action | The event type or order book operation. Can be A dd, C ancel, M odify, clea R book, T rade, F ill, or N one. |
| Sequence number | sequence | The original message sequence number from the venue. |

### Schemas and conventions

A schema is a data record format represented as a collection of different data fields. Our datasets support multiple schemas, such as order book, tick data, bar aggregates, and so on. You can get a dictionary describing the fields of each schema from ourList of market data schemas.

You can get a list of all supported schemas for any given dataset using thelist_schemasmethod. The same information can also be found on each dataset's detail page found through theExplorefeature.

The following table provides details about the data types and conventions used for various fields that you will commonly encounter in the data.

| Name | Field | Description |
| --- | --- | --- |
| Dataset | dataset | A unique string name assigned to each dataset by Databento. Full list of datasets can be found from the metadata . |
| Publisher ID | publisher_id | A unique 16-bit unsigned integer assigned to each publisher by Databento. Full list of publisher IDs can be found from the metadata . |
| Instrument ID | instrument_id | A unique 32-bit unsigned integer assigned to each instrument by the venue. Information about instrument IDs for any given dataset can be found in the symbology . |
| Order ID | order_id | A unique 64-bit unsigned integer assigned to each order by the venue. |
| Timestamp (event) | ts_event | The matching-engine-received timestamp expressed as the number of nanoseconds since the UNIX epoch . |
| Timestamp (receive) | ts_recv | The capture-server-received timestamp expressed as the number of nanoseconds since the UNIX epoch . |
| Timestamp delta (in) | ts_in_delta | The matching-engine-sending timestamp expressed as the number of nanoseconds before ts_recv . See timestamping guide. |
| Timestamp out | ts_out | The Databento gateway-sending timestamp expressed as the number of nanoseconds since the UNIX epoch . See timestamping guide. |
| Price | price | The price expressed as signed integer where every 1 unit corresponds to 1e-9, i.e. 1/1,000,000,000 or 0.000000001. |
| Book side | side | The side that initiates the event. Can be A sk for a sell order (or sell aggressor in a trade), B id for a buy order (or buy aggressor in a trade), or N one where no side is specified by the original source. |
| Size | size | The order quantity. |
| Flag | flag | A bit field indicating event end, message characteristics, and data quality. |
| Action | action | The event type or order book operation. Can be A dd, C ancel, M odify, clea R book, T rade, F ill, or N one. |
| Sequence number | sequence | The original message sequence number from the venue. |

### Schemas and conventions

A schema is a data record format represented as a collection of different data fields. Our datasets support multiple schemas, such as order book, trades, bar aggregates, and so on. You can get a dictionary describing the fields of each schema from ourList of market data schemas.

You can get a list of all supported schemas for any given dataset using the Historical client'slist_schemasmethod. The same information can also be found on the dataset details pages on theuser portal.

The following table provides details about the data types and conventions used for various fields that you will commonly encounter in the data.

| Name | Field | Description |
| --- | --- | --- |
| Dataset | dataset | A unique string name assigned to each dataset by Databento. Full list of datasets can be found from the metadata . |
| Publisher ID | publisher_id | A unique 16-bit unsigned integer assigned to each publisher by Databento. Full list of publisher IDs can be found from the metadata . |
| Instrument ID | instrument_id | A unique 32-bit unsigned integer assigned to each instrument by the venue. Information about instrument IDs for any given dataset can be found in the symbology . |
| Order ID | order_id | A unique 64-bit unsigned integer assigned to each order by the venue. |
| Timestamp (event) | ts_event | The matching-engine-received timestamp expressed as the number of nanoseconds since the UNIX epoch . |
| Timestamp (receive) | ts_recv | The capture-server-received timestamp expressed as the number of nanoseconds since the UNIX epoch . |
| Timestamp delta (in) | ts_in_delta | The matching-engine-sending timestamp expressed as the number of nanoseconds before ts_recv . See timestamping guide. |
| Timestamp out | ts_out | The Databento gateway-sending timestamp expressed as the number of nanoseconds since the UNIX epoch . See timestamping guide. |
| Price | price | The price expressed as signed integer where every 1 unit corresponds to 1e-9, i.e. 1/1,000,000,000 or 0.000000001. |
| Book side | side | The side that initiates the event. Can be A sk for a sell order (or sell aggressor in a trade), B id for a buy order (or buy aggressor in a trade), or N one where no side is specified by the original source. |
| Size | size | The order quantity. |
| Flag | flag | A bit field indicating event end, message characteristics, and data quality. |
| Action | action | The event type or order book operation. Can be A dd, C ancel, M odify, clea R book, T rade, F ill, or N one. |
| Sequence number | sequence | The original message sequence number from the venue. |

### Schemas and conventions

A schema is a data record format represented as a collection of different data fields. Our datasets support multiple schemas, such as order book, tick data, bar aggregates, and so on. You can see a full list from ourList of market data schemas.

You can get a list of all supported schemas for any given dataset using themetadata.list_schemasmethod. The same information can also be found on each dataset's detail page found through theExplorefeature.

The following table provides details about the data types and conventions used for various fields that you will commonly encounter in the data.

| Name | Field | Description |
| --- | --- | --- |
| Dataset | dataset | A unique string name assigned to each dataset by Databento. Full list of datasets can be found from the metadata . |
| Publisher ID | publisher_id | A unique u16 assigned to each publisher by Databento. Full list of publisher IDs can be found from the metadata . |
| Instrument ID | instrument_id | A unique u32 assigned to each instrument by the venue. Information about instrument IDs for any given dataset can be found in the symbology . |
| Order ID | order_id | A unique u64 assigned to each order by the venue. |
| Timestamp (event) | ts_event | The matching-engine-received timestamp expressed as the number of nanoseconds since the UNIX epoch . |
| Timestamp (receive) | ts_recv | The capture-server-received timestamp expressed as the number of nanoseconds since the UNIX epoch . |
| Timestamp delta (in) | ts_in_delta | The matching-engine-sending timestamp expressed as the number of nanoseconds before ts_recv . See timestamping guide. |
| Timestamp out | ts_out | The Databento gateway-sending timestamp expressed as the number of nanoseconds since the UNIX epoch . See timestamping guide. |
| Price | price | The price expressed as signed integer where every 1 unit corresponds to 1e-9, i.e. 1/1,000,000,000 or 0.000000001. |
| Book side | side | The side that initiates the event. Can be A sk for a sell order (or sell aggressor in a trade), B id for a buy order (or buy aggressor in a trade), or N one where no side is specified by the original source. |
| Size | size | The order quantity. |
| Flag | flag | A bit field indicating event end, message characteristics, and data quality. |
| Action | action | The event type or order book operation. Can be A dd, C ancel, M odify, clea R book, T rade, F ill, or N one. |
| Sequence number | sequence | The original message sequence number from the venue. |

### Datasets

Databento provides time series datasets for a variety of markets, sourced from different publishers. Our available datasets can be browsed through thesearchfeature on our site.

Each dataset is assigned a unique string identifier (dataset ID) in the formPUBLISHER.DATASET, such asGLBX.MDP3. For publishers that are also markets, we use standard four-character ISO 10383Market Identifier Codes (MIC). Otherwise, Databento arbitrarily assigns a four-character identifier for the publisher.

These dataset IDs are also found on theData catalogandDownload requestfeatures of the Databento user portal.

When a publisher provides multiple data products with different levels of granularity, Databento subscribes to the most-granular product. We then provide this dataset withalternate schemasto make it easy to work with the level of detail most appropriate for your application.

More information about different types of venues and publishers is available in ourFAQs.

### Datasets

Databento provides time series datasets for a variety of markets, sourced from different publishers. Our available datasets can be browsed through thesearchfeature on our site.

Each dataset is assigned a unique string identifier (dataset ID) in the formPUBLISHER.DATASET, such asGLBX.MDP3. For publishers that are also markets, we use standard four-character ISO 10383Market Identifier Codes (MIC). Otherwise, Databento arbitrarily assigns a four-character identifier for the publisher.

These dataset IDs are also found on theData catalogandDownload requestfeatures of the Databento user portal.

When a publisher provides multiple data products with different levels of granularity, Databento subscribes to the most-granular product. We then provide this dataset withalternate schemasto make it easy to work with the level of detail most appropriate for your application.

More information about different types of venues and publishers is available in ourFAQs.

### Datasets

Databento provides time series datasets for a variety of markets, sourced from different publishers. Our available datasets can be browsed through thesearchfeature on our site.

Each dataset is assigned a unique string identifier (dataset ID) in the formPUBLISHER.DATASET, such asGLBX.MDP3. For publishers that are also markets, we use standard four-character ISO 10383Market Identifier Codes (MIC). Otherwise, Databento arbitrarily assigns a four-character identifier for the publisher.

These dataset IDs are also found on theData catalogandDownload requestfeatures of the Databento user portal.

When a publisher provides multiple data products with different levels of granularity, Databento subscribes to the most-granular product. We then provide this dataset withalternate schemasto make it easy to work with the level of detail most appropriate for your application.

More information about different types of venues and publishers is available in ourFAQs.

### Datasets

Databento provides time series datasets for a variety of markets, sourced from different publishers. Our available datasets can be browsed through thesearchfeature on our site.

Each dataset is assigned a unique string identifier (dataset ID) in the formPUBLISHER.DATASET, such asGLBX.MDP3. For publishers that are also markets, we use standard four-character ISO 10383Market Identifier Codes (MIC). Otherwise, Databento arbitrarily assigns a four-character identifier for the publisher.

These dataset IDs are also found on theData catalogandDownload requestfeatures of the Databento user portal.

When a publisher provides multiple data products with different levels of granularity, Databento subscribes to the most-granular product. We then provide this dataset withalternate schemasto make it easy to work with the level of detail most appropriate for your application.

More information about different types of venues and publishers is available in ourFAQs.

### Symbology

Databento's historical API supports several ways to select an instrument in adataset. An instrument is specified using asymboland asymbology type, also referred to as anstype. The supported symbology types are:

When requesting data from ourtimeseries.get_rangeorbatch.submit_jobendpoints, an input and output symbology type can be specified. By default, our client libraries will use raw symbology for the input type and instrument ID symbology for the output type. Not all symbology types are supported for every dataset.

The process of converting between one symbology type to another is calledsymbology resolution. This conversion can be done, for no cost, with thesymbology.resolveendpoint.

For more about symbology at Databento, see ourKnowledge base.

### Symbology

Databento's historical API supports several ways to select an instrument in adataset. An instrument is specified using asymboland asymbology type, also referred to as anstype. The supported symbology types are:

When requesting data from ourtimeseries.get_rangeorbatch.submit_jobendpoints, an input and output symbology type can be specified. By default, our client libraries will use raw symbology for the input type and instrument ID symbology for the output type. Not all symbology types are supported for every dataset.

The process of converting between one symbology type to another is calledsymbology resolution. This conversion can be done, for no cost, with thesymbology.resolveendpoint.

For more about symbology at Databento, see ourKnowledge base.

### Symbology

Databento's historical API supports several ways to select an instrument in adataset. An instrument is specified using asymboland asymbology type, also referred to as anstype. The supported symbology types are:

When requesting data from ourtimeseries.get_rangeorbatch.submit_jobendpoints, an input and output symbology type can be specified. By default, our client libraries will use raw symbology for the input type and instrument ID symbology for the output type. Not all symbology types are supported for every dataset.

The process of converting between one symbology type to another is calledsymbology resolution. This conversion can be done, for no cost, with thesymbology.resolveendpoint.

For more about symbology at Databento, see ourStandards and conventions.

### Symbology

Databento's historical API supports several ways to select an instrument in adataset. An instrument is specified using asymboland asymbology type, also referred to as anstype. The supported symbology types are:

When requesting data from ourtimeseries.get_rangeorbatch.submit_jobendpoints, an input and output symbology type can be specified. By default, our client libraries will use raw symbology for the input type and instrument ID symbology for the output type. Not all symbology types are supported for every dataset.

The process of converting between one symbology type to another is calledsymbology resolution. This conversion can be done, for no cost, with thesymbology.resolveendpoint.

For more about symbology at Databento, see ourStandards and conventions.

### Encodings

Databento Binary Encoding (DBN) is an extremely fast message encoding and highly-compressible storage format for normalized market data. It includes a self-describing metadata header and adopts a binary format with zero-copy serialization.

We recommend using ourPython,C++, orRust client librariesto read DBN files locally. ACLI toolis also available for converting DBN files to CSV or JSON.

Comma-separated values (CSV) is a simple text file format for tabular data, CSVs can be easily opened with Excel, loaded intopandasdata frames, or parsed in C++.

Our CSVs have one header line, followed by one record per line. Lines use UNIX-style\nseparators.

JavaScript Object Notation(JSON) is a flexible text file format with broad language support and wide adoption across web apps.

Our JSON files follow theJSON lines specification, where each line of the file is a JSON record. Lines use UNIX-style\nseparators.

### Encodings

Databento Binary Encoding (DBN) is an extremely fast message encoding and highly-compressible storage format for normalized market data. It includes a self-describing metadata header and adopts a binary format with zero-copy serialization.

We recommend using ourPython,C++, orRust client librariesto read DBN files locally. ACLI toolis also available for converting DBN files to CSV or JSON.

Comma-separated values (CSV) is a simple text file format for tabular data. CSVs can be easily opened with Excel, loaded intopandasdata frames, or parsed in C++.

Our CSVs have one header line, followed by one record per line. Lines use UNIX-style\nseparators.

JavaScript Object Notation(JSON) is a flexible text file format with broad language support and wide adoption across web apps.

Our JSON files follow theJSON lines specification, where each line of the file is a JSON record. Lines use UNIX-style\nseparators.

### Encodings

Databento Binary Encoding (DBN) is an extremely fast message encoding and highly-compressible storage format for normalized market data. It includes a self-describing metadata header and adopts a binary format with zero-copy serialization.

We recommend using ourPython,C++, orRust client librariesto read DBN files locally. ACLI toolis also available for converting DBN files to CSV or JSON.

Comma-separated values (CSV) is a simple text file format for tabular data, CSVs can be easily opened with Excel, loaded intopandasdata frames, or parsed in C++.

Our CSVs have one header line, followed by one record per line. Lines use UNIX-style\nseparators.

JavaScript Object Notation(JSON) is a flexible text file format with broad language support and wide adoption across web apps.

Our JSON files follow theJSON lines specification, where each line of the file is a JSON record. Lines use UNIX-style\nseparators.

### Encodings

Databento Binary Encoding (DBN) is an extremely fast message encoding and highly-compressible storage format for normalized market data. It includes a self-describing metadata header and adopts a binary format with zero-copy serialization.

We recommend using ourPython,C++, orRust client librariesto read DBN files locally. ACLI toolis also available for converting DBN files to CSV or JSON.

Comma-separated values (CSV) is a simple text file format for tabular data. CSVs can be easily opened with Excel, loaded intopandasdata frames, or parsed in C++.

Our CSVs have one header line, followed by one record per line. Lines use UNIX-style\nseparators.

JavaScript Object Notation(JSON) is a flexible text file format with broad language support and wide adoption across web apps.

Our JSON files follow theJSON lines specification, where each line of the file is a JSON record. Lines use UNIX-style\nseparators.

### Compression

Databento provides options for compressing files from our API. Available compression formats depend on theencodingyou select.

Thezstdcompression option uses theZstandardformat.

This option is available for all encodings, and is recommended for faster transfer speeds and smaller files.

Read more aboutworking with Zstandard-compressed files.

Thenonecompression option disables compression entirely, resulting in significantly larger files. However, this can be useful for loading small CSV files directly into Excel.

### Compression

Databento provides options for compressing files from our API. Available compression formats depend on theencodingyou select.

Thezstdcompression option uses theZstandardformat.

This option is available for all encodings, and is recommended for faster transfer speeds and smaller files.

Read more aboutworking with Zstandard-compressed files.

Thenonecompression option disables compression entirely, resulting in significantly larger files. However, this can be useful for loading small CSV files directly into Excel.

### Compression

Databento provides options for compressing files from our API. Available compression formats depend on theencodingyou select.

TheZstdcompression option uses theZstandardformat.

This option is available for all encodings, and is recommended for faster transfer speeds and smaller files.

You can read Zstandard files in Python using thezstandard package.

Read more aboutworking with Zstandard-compressed files.

TheNonecompression option disables compression entirely, resulting in significantly larger files. However, this can be useful for loading small CSV files directly into Excel.

### Compression

Databento provides options for compressing files from our API. Available compression formats depend on theencodingyou select.

TheZstdcompression option uses theZstandardformat.

This option is available for all encodings, and is recommended for faster transfer speeds and smaller files.

The DBN crate comes with support for reading Zstandard-compressedDBNfiles and you can read any Zstandard file in Rust using thezstdlibrary.

Read more aboutworking with Zstandard-compressed files.

TheNonecompression option disables compression entirely, resulting in significantly larger files. However, this can be useful for loading small CSV files directly into Excel.

### Dates and times

Our C++ client library has several methods with timestamp arguments. These arguments will implement separate overloads with typesdatabento::UnixNanosandconst std::string&.

The recommended interface to use isdatabento::UnixNanos. It is a type alias forstd::chrono::time_pointwith nanosecond precision, represented as auint64_t. Thestd::chronosection of the standard library contains functions for parsing and converting human-readable timestamps intoUNIX nanoseconds.

These timestamps are always in UTC. To localize from other timezones, you will need to use features added in C++20, or a third-party library such asdate.

The C++ client library supportsconst std::string&arguments, with supported formatting based onISO 8601as listed below.

Timezone specification is also supported.

Some parameters require a bare date, without a time. These arguments have typeconst std::string&and must be a string inyyyy-mm-ddformat, e.g."2022-02-28".

### Dates and times

Our API exposes several parameters that expect a timestamp. Databento supports several formats based onISO 8601.

Timestamps can be specified asISO 8601string or UNIX nanoseconds.

Timezone specification is also supported.

In our market data, we always useUNIX nanosecondsto encode timestamps as a single number. Our client libraries can help convert this into a human-readable format.

Some parameters require a bare date, without a time. In these cases, the date must be specified inyyyy-mm-ddformat, e.g.2022-02-28.

### Dates and times

Our Python client library has several functions with timestamp arguments. These arguments will have typepandas.Timestamp | datetime.date | str | intand support a variety of formats.

It's recommended to usepandas.Timestamp, which fully supports timezones and nanosecond-precision. If adatetime.dateis used, the time is set to midnight UTC. If anintis provided, the value is interpreted asUNIX nanoseconds.

The client library also handles several string-based timestamp formats based onISO 8601.

Timezone specification is also supported.

Some parameters require a bare date, without a time. These arguments have typedatetime.date | strand must either be adatetime.dateobject, or a string inyyyy-mm-ddformat, e.g."2022-02-28".

### Dates and times

Our Rust client library uses thetime cratefor representing both dates and datetimes.

Dates and datetimes from the historical API will be deserialized intotime::Dateandtime::OffsetDateTimes. To localize these, useOffsetDateTime::to_offset.

In DBN records, timestamps are represented asu64nanosecond-precisionUNIX timestamps. These timestamps are always in UTC. These can be parsed withOffsetDateTime::from_unix_timestamp_nanos.

### Errors

Our historical API uses HTTP response codes to indicate the success or failure of an API request. The client library provides exceptions that wrap these response codes.

You can check the HTTP response code of aHttpResponseErrorwith itsstatus_codemethod.

The full list of the response codes and associated causes is as follows:

| Code | Message | Cause |
| --- | --- | --- |
| 200 | OK | Successful request. |
| 206 | Partial Content | Successful request, with partially resolved symbols. |
| 400 | Bad Request | Invalid request. Usually due to a missing, malformed or unsupported parameter. |
| 401 | Unauthorized | Invalid username or API key. |
| 402 | Payment Required | Issue with your account payment information. |
| 403 | Forbidden | The API key has insufficient permissions to perform the request. |
| 404 | Not Found | A resource is not found, or a requested symbol does not exist. |
| 409 | Conflict | A resource already exists. |
| 422 | Unprocessable Entity | The request is well formed, but we cannot or will not process the contained instructions. |
| 429 | Too Many Requests | API rate limit exceeded. |
| 500 | Internal Server Error | Unexpected condition encountered in our system. |
| 503 | Service Unavailable | Data gateway is offline or overloaded. |
| 504 | Gateway Timeout | Data gateway is available but other parts of our system are offline or overloaded. |

```python
class Exception : public std::exception;
class HttpRequestError : public Exception;
class HttpResponseError : public Exception;
class InvalidArgumentError : public Exception;
class JsonResponseError : public Exception;
class DbnResponseError : public Exception;
```

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
```

```python
#include <databento/exceptions.hpp>  // HttpResponseError
#include <databento/historical.hpp>
#include <iostream>

using namespace databento;

// set invalid key
auto client = Historical::Builder().SetKey("invalid").Build();

try {
  auto datasets = client.MetadataListDatasets();
} catch (const HttpResponseError& err) {
  std::cout << err.what() << '\n';
}
```

```python
1
```

```python
Received an error response from request to /v0/metadata.list_datasets with status 401 and body '{"detail":{"case":"auth_authentication_failed","message":"Authentication failed.","status_code":401,"docs":"https://databento.com/docs/portal/api-keys","payload":null}}'
```

### Errors

Our historical API uses HTTP response codes to indicate the success or failure of an API request. On error, the HTTP body will also contain a JSON object with a human-readable error message in thedetailfield.

The full list of the response codes and associated causes is as follows:

| Code | Message | Cause |
| --- | --- | --- |
| 200 | OK | Successful request. |
| 206 | Partial Content | Successful request, with partially resolved symbols. |
| 400 | Bad Request | Invalid request. Usually due to a missing, malformed or unsupported parameter. |
| 401 | Unauthorized | Invalid username or API key. |
| 402 | Payment Required | Issue with your account payment information. |
| 403 | Forbidden | The API key has insufficient permissions to perform the request. |
| 404 | Not Found | A resource is not found, or a requested symbol does not exist. |
| 409 | Conflict | A resource already exists. |
| 422 | Unprocessable Entity | The request is well formed, but we cannot or will not process the contained instructions. |
| 429 | Too Many Requests | API rate limit exceeded. |
| 500 | Internal Server Error | Unexpected condition encountered in our system. |
| 503 | Service Unavailable | Data gateway is offline or overloaded. |
| 504 | Gateway Timeout | Data gateway is available but other parts of our system are offline or overloaded. |

```python
1
```

```python
curl -i 'https://hist.databento.com/v0/metadata.list_datasets'
```

```python
1
2
3
4
5
6
7
8
```

```python
HTTP/2 401
date: Wed, 30 Nov 2022 17:59:08 GMT
server: uvicorn
www-authenticate: Basic
content-length: 30
content-type: application/json

{"detail":"Not authenticated"}
```

### Errors

Our historical API uses HTTP response codes to indicate the success or failure of an API request. The client library provides exceptions that wrap these response codes.

The full list of the response codes and associated causes is as follows:

| Code | Message | Cause |
| --- | --- | --- |
| 200 | OK | Successful request. |
| 206 | Partial Content | Successful request, with partially resolved symbols. |
| 400 | Bad Request | Invalid request. Usually due to a missing, malformed or unsupported parameter. |
| 401 | Unauthorized | Invalid username or API key. |
| 402 | Payment Required | Issue with your account payment information. |
| 403 | Forbidden | The API key has insufficient permissions to perform the request. |
| 404 | Not Found | A resource is not found, or a requested symbol does not exist. |
| 409 | Conflict | A resource already exists. |
| 422 | Unprocessable Entity | The request is well formed, but we cannot or will not process the contained instructions. |
| 429 | Too Many Requests | API rate limit exceeded. |
| 500 | Internal Server Error | Unexpected condition encountered in our system. |
| 503 | Service Unavailable | Data gateway is offline or overloaded. |
| 504 | Gateway Timeout | Data gateway is available but other parts of our system are offline or overloaded. |

```python
class databento.BentoError(Exception)
class databento.BentoHttpError(databento.BentoError)
class databento.BentoClientError(databento.BentoHttpError)
class databento.BentoServerError(databento.BentoHttpError)
```

```python
1
2
3
4
5
6
7
8
```

```python
import databento as db

client = db.Historical("INVALID_API_KEY")

try:
    print(client.metadata.list_datasets())
except db.BentoClientError as e:
    print(e)
```

```python
1
2
3
```

```python
400 auth_invalid_username_in_basic_auth
Invalid username in Basic auth ('INVALID_API_KEY').
documentation: https://databento.com/docs
```

### Errors

Our historical API uses HTTP response codes to indicate the success or failure of an API request. The client library provides an error enum to wrap these response codes.

Use thestatusmethod to get the status code associated with an error.

The full list of the response codes and associated causes is as follows:

| Code | Message | Cause |
| --- | --- | --- |
| 200 | OK | Successful request. |
| 206 | Partial Content | Successful request, with partially resolved symbols. |
| 400 | Bad Request | Invalid request. Usually due to a missing, malformed or unsupported parameter. |
| 401 | Unauthorized | Invalid username or API key. |
| 402 | Payment Required | Issue with your account payment information. |
| 403 | Forbidden | The API key has insufficient permissions to perform the request. |
| 404 | Not Found | A resource is not found, or a requested symbol does not exist. |
| 409 | Conflict | A resource already exists. |
| 422 | Unprocessable Entity | The request is well formed, but we cannot or will not process the contained instructions. |
| 429 | Too Many Requests | API rate limit exceeded. |
| 500 | Internal Server Error | Unexpected condition encountered in our system. |
| 503 | Service Unavailable | Data gateway is offline or overloaded. |
| 504 | Gateway Timeout | Data gateway is available but other parts of our system are offline or overloaded. |

```python
pub enum Error {
    /// An invalid argument was passed.
    BadArgument {
        /// The name of the parameter to which the bad argument was passed.
        param_name: String,
        /// The description of how the argument was invalid.
        desc: String,
    },
    /// An I/O error while reading or writing DBN or another encoding.
    Io(std::io::Error),
    /// An HTTP error.
    Http(reqwest::Error),
    /// An error related to JSON decoding.
    Json(serde_json::Error),
    /// An error related to invalid UTF-8.
    Utf8(std::str::Utf8Error),
    /// An error from the Databento API.
    Api(ApiError),
    /// An error internal to the client.
    Internal(String),
    /// An error related to DBN encoding.
    Dbn(dbn::Error),
    /// An error when authentication failed.
    Auth(String),
}

pub struct ApiError {
    /// The request ID.
    pub request_id: Option<String>,
    /// The HTTP status code of the response.
    pub status_code: reqwest::StatusCode,
    /// The message from the Databento API.
    pub message: String,
    /// The link to documentation related to the error.
    pub docs_url: Option<String>,
}
```

```python
1
2
3
```

```python
use databento::HistoricalClient;

assert!(HistoricalClient::builder().key("invalid").is_err());
```

### Warnings

Our historical API uses theX-Warningresponse header to attach non-fatal warnings to a successful request. A warning means that your request was processed, but some aspect of the request or its result deserves attention. For example, one or more symbols may not have resolved, or the request may rely on behavior that is scheduled for removal.

A warning does not change the HTTP status code of the response. The header is only sent with2xxresponses, and is omitted entirely when there are no warnings. Failed requests are reported aserrorsinstead.

#### Format

The value of theX-Warningheader is a JSON array of strings. Each string is a single warning in the form<category>: <message>, where<category>is one of the following:

| Category | Cause |
| --- | --- |
| Warning | Something about the request or its result should be reviewed. |
| DeprecationWarning | The request uses an endpoint, parameter, or behavior that will be removed in the future. |

A single response may contain more than one warning. HTTP header names are case-insensitive, so HTTP/2 clients will typically report the header in lowercase asx-warning.

#### Reading warnings

To read warnings, check each response for theX-Warningheader, parse its value as JSON, and split each element on the first:to separate the category from the message.

Messages are intended to be human-readable and may change between releases, so your application should act on the category rather than matching on the text of a message. We recommend logging every warning, and treating aDeprecationWarningas a prompt to update your integration before the date given in the message.

#### Common warnings

Warnings are currently returned in cases such as:

This list is not exhaustive, and new warnings may be added at any time.

Related:Errors.

```python
1
2
3
4
5
6
7
```

```python
curl -i -G 'https://hist.databento.com/v0/metadata.get_record_count' \
 -u $YOUR_API_KEY: \
 -d dataset=GLBX.MDP3 \
 -d symbols=ESM2 \
 -d schema=mbo \
 -d start='2022-06-06T12:00' \
 -d end='2022-06-06T12:10'
```

```python
1
2
3
4
5
6
7
8
```

```python
HTTP/2 200
date: Thu, 01 Oct 2026 14:32:11 GMT
server: uvicorn
content-length: 6
content-type: application/json
x-warning: ["Warning: The request time range does not start at UTC midnight, which contains a synthetic snapshot of the full order book state. See: https://databento.com/docs/schemas-and-data-formats/mbo#snapshots"]

184621
```

### Rate limits

Our historical API allows each IP address up to:

When a request exceeds a rate limit, aHttpResponseErrorexception is raised with a 429 error code.

### Rate limits

Our historical API allows each IP address up to:

When a request exceeds a rate limit, aBentoClientErrorexception is raised with a 429 error code.

Retry-After

The Retry-After response header indicates how long the user should wait before retrying.

If you find that your application has been rate-limited, you can retry after waiting for the time specified in the Retry-After header.

If you are using our HTTP API through cURL, you may want to use thesleep 1command to wait 1 second before your next request.

This code snippet works best for our current APIs with their rate limits. Future APIs may have different rate limits, and might require a different default time delay.

### Rate limits

Our historical API allows each IP address up to:

When a request exceeds a rate limit, aBentoClientErrorexception is raised with a 429 error code.

Retry-After

The Retry-After response header indicates how long the user should wait before retrying.

If you find that your application has been rate-limited, you can retry after waiting for the time specified in the Retry-After header.

If you are using Python, you may use the time.sleep function as seen below to wait for the time specified in the Retry-After header. e.g.time.sleep(int(response.headers("Retry-After", 1)))

This code snippet works best for our current APIs with their rate limits. Future APIs may have different rate limits, and might require a different default time delay.

### Rate limits

Our historical API allows each IP address up to:

When a request exceeds a rate limit, anError::Httpwill be returned with a 429 error code.

### Size limits

There is no size limit for either stream or batch download requests. Batch download is more manageable for large datasets, so we recommend using batch download for requests over 5 GB.

You can also manage the size of your request by splitting it into multiple, smaller requests. The historical API allows you to make stream and batch download requests with time ranges specified up to nanosecond resolution. You can also use thelimitparameter in any request to limit the number of data records returned from the service.

Batch downloadsupports different delivery methods which can be specified using thedeliveryparameter.

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
```

```python
#include <databento/historical.hpp>

using namespace databento;

auto client = Historical::Builder().SetKeyFromEnv().Build();
auto job = client.BatchSubmitJob(
    "GLBX.MDP3", kAllSymbols, Schema::Trades,
    {"2022-08-26", "2022-09-27"}, {}, {}, {}, {}, {}, {}, {}, {},
    {}, SType::RawSymbol, SType::InstrumentId, 1000 /* limit */);
```

### Size limits

There is no size limit for either stream or batch download requests. Batch download is more manageable for large datasets, so we recommend using batch download for requests over 5 GB.

You can also manage the size of your request by splitting it into multiple, smaller requests. The historical API allows you to make stream and batch download requests with time ranges specified up to nanosecond resolution. You can also use thelimitparameter in any request to limit the number of data records returned from the service.

Batch downloadsupports different delivery methods which can be specified using thedeliveryparameter.

```python
1
2
3
4
5
6
7
```

```python
curl -X POST -G 'https://hist.databento.com/v0/batch.submit_job' \
 -u $YOUR_API_KEY: \
 -d dataset=GLBX.MDP3 \
 -d schema=trades \
 -d start='2022-06-06T00:00' \
 -d end='2022-06-10T00:10' \
 -d limit=10000
```

### Size limits

There is no size limit for either stream or batch download requests. Batch download is more manageable for large datasets, so we recommend using batch download for requests over 5 GB.

You can also manage the size of your request by splitting it into multiple, smaller requests. The historical API allows you to make stream and batch download requests with time ranges specified up to nanosecond resolution. You can also use thelimitparameter in any request to limit the number of data records returned from the service.

Batch downloadsupports different delivery methods which can be specified using thedeliveryparameter.

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
```

```python
import databento as db

client = db.Historical("$YOUR_API_KEY")

job = client.batch.submit_job(
    dataset="GLBX.MDP3",
    symbols="CLZ7",
    schema="trades",
    start="2022-06-06T00:00:00",
    end="2022-06-10T00:10:00",
    limit=10000,
)
```

### Size limits

There is no size limit for either stream or batch download requests. Batch download is more manageable for large datasets, so we recommend using batch download for requests over 5 GB.

You can also manage the size of your request by splitting it into multiple, smaller requests. The historical API allows you to make stream and batch download requests with time ranges specified up to nanosecond resolution. You can also use thelimitparameter in any request to limit the number of data records returned from the service.

Batch downloadsupports different delivery methods which can be specified using thedeliveryparameter.

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
18
19
20
21
22
23
24
25
```

```python
use std::num::NonZeroU64;

use databento::{
    HistoricalClient, Symbols, dbn::Schema,
    historical::batch::SubmitJobParams,
};
use time::macros::datetime;

let mut client =
    HistoricalClient::builder().key_from_env()?.build()?;
let job = client
    .batch()
    .submit_job(
        &SubmitJobParams::builder()
            .dataset("GLBX.MDP3")
            .symbols(Symbols::All)
            .schema(Schema::Trades)
            .date_time_range(
                datetime!(2022-08-26 00:00:00 UTC)
                    ..datetime!(2022-09-28 00:00:00 UTC),
            )
            .maybe_limit(NonZeroU64::new(1000))
            .build(),
    )
    .await?;
```

### Metered pricing

Databento only charges for the data that you use. You can find rates (per GB) for the various datasets and estimate pricing on ourData catalog. We meter the data by its uncompressed size inbinary encoding.

When you stream the data, you are billed incrementally for each outbound byte of data sent from our historical gateway. If your connection is interrupted while streaming our data and our historical gateway detects connection timeout over 5 seconds, it will immediately stop sending data and you will not be billed for the remainder of your request.

Duplicate streaming requests will incur repeated charges. If you intend to access the same data multiple times, we recommend using our batch download feature. When you make a batch download request, you are only billed once for the request and, subsequently, you can download the data from theDownload centermultiple times over 30 days for no additional charge.

You will only be billed for usage oftime seriesdata. Access to metadata, symbology, and account management is free.

Related:Billing management.

### Metered pricing

Databento only charges for the data that you use. You can find rates (per GB) for the various datasets and estimate pricing on ourData catalog. We meter the data by its uncompressed size inbinary encoding.

When you stream the data, you are billed incrementally for each outbound byte of data sent from our historical gateway. If your connection is interrupted while streaming our data and our historical gateway detects connection timeout over 5 seconds, it will immediately stop sending data and you will not be billed for the remainder of your request.

Duplicate streaming requests will incur repeated charges. If you intend to access the same data multiple times, we recommend using our batch download feature. When you make a batch download request, you are only billed once for the request and, subsequently, you can download the data from theDownload centermultiple times over 30 days for no additional charge.

You will only be billed for usage oftime seriesdata. Access to metadata, symbology, and account management is free. Themetadata.get_costendpoint can be used to determine cost before you request any data.

Related:Billing management.

### Metered pricing

Databento only charges for the data that you use. You can find rates (per GB) for the various datasets and estimate pricing on ourData catalog. We meter the data by its uncompressed size inbinary encoding.

When you stream the data, you are billed incrementally for each outbound byte of data sent from our historical gateway. If your connection is interrupted while streaming our data and our historical gateway detects connection timeout over 5 seconds, it will immediately stop sending data and you will not be billed for the remainder of your request.

Duplicate streaming requests will incur repeated charges. If you intend to access the same data multiple times, we recommend using our batch download feature. When you make a batch download request, you are only billed once for the request and, subsequently, you can download the data from theDownload centermultiple times over 30 days for no additional charge.

You will only be billed for usage oftime seriesdata. Access to metadata, symbology, and account management is free. TheHistorical.metadata.get_costmethod can be used to determine cost before you request any data.

Related:Billing management.

### Metered pricing

Databento only charges for the data that you use. You can find rates (per GB) for the various datasets and estimate pricing on ourData catalog. We meter the data by its uncompressed size inbinary encoding.

When you stream the data, you are billed incrementally for each outbound byte of data sent from our historical gateway. If your connection is interrupted while streaming our data and our historical gateway detects connection timeout over 5 seconds, it will immediately stop sending data and you will not be billed for the remainder of your request.

Duplicate streaming requests will incur repeated charges. If you intend to access the same data multiple times, we recommend using our batch download feature. When you make a batch download request, you are only billed once for the request and, subsequently, you can download the data from theDownload centermultiple times over 30 days for no additional charge.

You will only be billed for usage oftime seriesdata. Access to metadata, symbology, and account management is free.

Related:Billing management.

### Versioning

Our historical API and its client libraries adoptMAJOR.MINOR.PATCHformat for version numbers. These version numbers conform tosemantic versioning. We are using major version0for initial development, where our API is not considered stable.

Once we release major version1, our public API will be stable. This means that you will be able to upgrade minor or patch versions to pick up new functionality, without breaking your integration.

Starting with major versions after1, we will provide support for previous versions for one year after the date of the subsequent major release. For example, if version2.0.0is released on January 1, 2024, then all versions1.x.yof the API and client libraries will be deprecated. However, they will remain supported until January 1, 2025.

We may introduce backwards-compatible changes between minor versions in the form of:

OurRelease noteswill contain information about both breaking and backwards-compatible changes in each release.

Our API and official client libraries are kept in sync with same-day releases for major versions. For instance,1.x.yof the C++ client library will use the same functionality found in any1.x.yversion of the Python client.

Related:Release notes.

### Versioning

Our historical API and its client libraries adoptMAJOR.MINOR.PATCHformat for version numbers. These version numbers conform tosemantic versioning. We are using major version0for initial development where our API is not considered stable.

Once we release major version1, our public API will be stable. This means that you will be able to upgrade minor or patch versions to pick up new functionality, without breaking your integration.

Starting with major versions after1, we will provide support for previous versions for one year after the date of the subsequent major release. For example, if version2.0.0is released on January 1, 2024, then all versions1.x.yof the API and client libraries will be deprecated. However, they will remain supported until January 1, 2025.

We may introduce backwards-compatible changes between minor versions in the form of:

OurRelease noteswill contain information about both breaking and backwards-compatible changes in each release.

Related:Release notes.

### Versioning

Our historical and live APIs and their client libraries adoptMAJOR.MINOR.PATCHformat for version numbers. These version numbers conform tosemantic versioning. We are using major version0for initial development, where our API is not considered stable.

Once we release major version1, our public API will be stable. This means that you will be able to upgrade minor or patch versions to pick up new functionality, without breaking your integration.

Starting with major versions after1, we will provide support for previous versions for one year after the date of the subsequent major release. For example, if version2.0.0is released on January 1, 2024, then all versions1.x.yof the API and client libraries will be deprecated. However, they will remain supported until January 1, 2025.

We may introduce backwards-compatible changes between minor versions in the form of:

OurRelease noteswill contain information about both breaking and backwards-compatible changes in each release.

Our API and official client libraries are kept in sync with same-day releases for major versions. For instance,1.x.yof the C++ client library will use the same functionality found in any1.x.yversion of the Python client.

Related:Release notes.

### Versioning

Our historical API and its client libraries adoptMAJOR.MINOR.PATCHformat for version numbers. These version numbers conform tosemantic versioning. We are using major version0for initial development, where our API is not considered stable.

Once we release major version1, our public API will be stable. This means that you will be able to upgrade minor or patch versions to pick up new functionality, without breaking your integration.

Starting with major versions after1, we will provide support for previous versions for one year after the date of the subsequent major release. For example, if version2.0.0is released on January 1, 2024, then all versions1.x.yof the API and client libraries will be deprecated. However, they will remain supported until January 1, 2025.

We may introduce backwards-compatible changes between minor versions in the form of:

OurRelease noteswill contain information about both breaking and backwards-compatible changes in each release.

Our API and official client libraries are kept in sync with same-day releases for major versions. For instance,1.x.yof the Rust client library will use the same functionality found in any1.x.yversion of the Python client.

Related:Release notes.

## Client

### Historical

To access Databento's historical API, first create an instance of theHistoricalclient. The entire API is exposed through instance methods of the client.

Note that the API key can be passed as an argument, which isnot recommended for production applications. Instead, you can use theHistoricalBuilderclass which includes theSetKeyFromEnvmethod for settingkeyfrom theDATABENTO_API_KEYenvironment variable.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| log_receiver | ILogReceiver* | Non-null, non-owning pointer to a log receiver . If you wish to disable logging, pass a NullLogReceiver . By default it will use ILogReceiver::Default() which will log Info level and above messages to standard error. |
| key | std::string | 32-character API key. Found on your API keys page. |
| gateway | databento::HistoricalGateway | Site of historical gateway to connect to. Currently only Bo1 is supported. If using HistoricalBuilder , it defaults to Bo1 . |

```python
Historical(ILogReceiver* log_receiver, std::string key, HistoricalGateway gateway);
```

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
```

```python
#include <databento/historical.hpp>
#include <databento/log.hpp>

using namespace databento;

// Pass as an argument
auto client1 =
    Historical{ILogReceiver::Default(), "$YOUR_API_KEY",
               HistoricalGateway::Bo1};
// Or, pass as `DATABENTO_API_KEY` environment variable
auto client2 = Historical::Builder().SetKeyFromEnv().Build();
```

### Historical

To access Databento's historical API, first create an instance of theHistoricalclient. The entire API is exposed through instance methods of the client.

Note that the API key can be passed as a parameter, which isnot recommended for production applications. Instead, you can leave out this parameter to pass your API key via theDATABENTO_API_KEYenvironment variable:

Currently, onlyBO1is supported for historical data.

#### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| key | str | optional | 32-character API key. Found on your API keys page. If None then DATABENTO_API_KEY environment variable is used. |
| gateway | HistoricalGateway or str | optional | Site of historical gateway to connect to. Currently only BO1 is supported. If None then will connect to the default historical gateway. |

```python
class Historical(
    key: str | None = None,
    gateway: HistoricalGateway | str = HistoricalGateway.BO1,
)
```

```python
1
2
3
4
5
6
7
```

```python
import databento as db

# Pass as parameter
client = db.Historical("$YOUR_API_KEY")

# Or, pass as `DATABENTO_API_KEY` environment variable
client = db.Historical()
```

### HistoricalClient

To access Databento's historical API, first create an instance ofHistoricalClient. The API is exposed through four subclients:

Note that the API key can be passed as an argument, which isnot recommended for production applications. Instead, you can use thehistorical::ClientBuilderthroughHistoricalClient::builder(), which includes akey_from_envmethod for settingkeyfrom theDATABENTO_API_KEYenvironment variable.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| key | String | 32-character API key. Found on your API keys page. |
| gateway | databento::HistoricalGateway | Site of historical gateway to connect to. Currently only Bo1 is supported. If using ClientBuilder , it defaults to Bo1 . |
| upgrade_policy | VersionUpgradePolicy | How to handle data from prior DBN versions. By default, records from DBN versions 1 and 2 are upgraded to version 3. |

```python
impl ClientBuilder {
    // Required
    pub fn key(
        self,
        key: impl ToString,
    ) -> databento::Result<Self>;
    pub fn key_from_env(self) -> databento::Result<Self>;

    // Optional
    pub fn gateway(mut self, gateway: HistoricalGateway) -> Self;
    pub fn upgrade_policy(
        mut self,
        upgrade_policy: VersionUpgradePolicy,
    ) -> Self;

    pub async fn build(self) -> databento::Result<Client>;
}
```

```python
1
2
3
4
5
6
```

```python
use databento::HistoricalClient;

let client =
    HistoricalClient::builder().key("$YOUR_API_KEY")?.build()?;
let client =
    HistoricalClient::builder().key_from_env()?.build()?;
```

## Metadata

### Historical::MetadataListPublishers

List allpublisher IDmappings.

Use this method to list the mappings of publisher names to publisher IDs.

#### Returns

std::vector<PublisherDetail>

A list of publisher details, wherePublisherDetailis:

| Field | Type | Description |
| --- | --- | --- |
| publisher_id | uint16_t | The publisher ID assigned by Databento. |
| dataset | std::string | The dataset ID for the publisher. |
| venue | std::string | The venue for the publisher. |
| description | std::string | The publisher description. |

```python
std::vector<PublisherDetail> MetadataListPublishers();
```

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
```

```python
#include <databento/historical.hpp>
#include <iostream>

using namespace databento;

auto client =
    Historical::Builder().SetKey("$YOUR_API_KEY").Build();
auto publishers = client.MetadataListPublishers();
for (const auto& publisher : publishers) {
  std::cout << publisher << '\n';
}
```

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
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
```

```python
PublisherDetail { publisher_id = 1, dataset = "GLBX.MDP3", venue = "GLBX", description = "CME Globex MDP 3.0" }
PublisherDetail { publisher_id = 2, dataset = "XNAS.ITCH", venue = "XNAS", description = "Nasdaq TotalView-ITCH" }
PublisherDetail { publisher_id = 3, dataset = "XBOS.ITCH", venue = "XBOS", description = "Nasdaq Texas TotalView-ITCH" }
PublisherDetail { publisher_id = 4, dataset = "XPSX.ITCH", venue = "XPSX", description = "Nasdaq PSX TotalView-ITCH" }
PublisherDetail { publisher_id = 5, dataset = "BATS.PITCH", venue = "BATS", description = "Cboe BZX Depth" }
PublisherDetail { publisher_id = 6, dataset = "BATY.PITCH", venue = "BATY", description = "Cboe BYX Depth" }
PublisherDetail { publisher_id = 7, dataset = "EDGA.PITCH", venue = "EDGA", description = "Cboe EDGA Depth" }
PublisherDetail { publisher_id = 8, dataset = "EDGX.PITCH", venue = "EDGX", description = "Cboe EDGX Depth" }
PublisherDetail { publisher_id = 9, dataset = "XNYS.PILLAR", venue = "XNYS", description = "NYSE Integrated" }
PublisherDetail { publisher_id = 10, dataset = "XCIS.PILLAR", venue = "XCIS", description = "NYSE National Integrated" }
PublisherDetail { publisher_id = 11, dataset = "XASE.PILLAR", venue = "XASE", description = "NYSE American Integrated" }
PublisherDetail { publisher_id = 12, dataset = "XCHI.PILLAR", venue = "XCHI", description = "NYSE Texas Integrated" }
PublisherDetail { publisher_id = 13, dataset = "XCIS.BBO", venue = "XCIS", description = "NYSE National BBO" }
PublisherDetail { publisher_id = 14, dataset = "XCIS.TRADES", venue = "XCIS", description = "NYSE National Trades" }
PublisherDetail { publisher_id = 15, dataset = "MEMX.MEMOIR", venue = "MEMX", description = "MEMX MEMOIR Depth" }
PublisherDetail { publisher_id = 16, dataset = "EPRL.DOM", venue = "EPRL", description = "MIAX Pearl Depth" }
PublisherDetail { publisher_id = 17, dataset = "XNAS.NLS", venue = "FINN", description = "FINRA/Nasdaq TRF Carteret" }
PublisherDetail { publisher_id = 18, dataset = "XNAS.NLS", venue = "FINC", description = "FINRA/Nasdaq TRF Chicago" }
PublisherDetail { publisher_id = 19, dataset = "XNYS.TRADES", venue = "FINY", description = "FINRA/NYSE TRF" }
PublisherDetail { publisher_id = 20, dataset = "OPRA.PILLAR", venue = "AMXO", description = "OPRA - NYSE American Options" }
PublisherDetail { publisher_id = 21, dataset = "OPRA.PILLAR", venue = "XBOX", description = "OPRA - BOX Options" }
PublisherDetail { publisher_id = 22, dataset = "OPRA.PILLAR", venue = "XCBO", description = "OPRA - Cboe Options" }
PublisherDetail { publisher_id = 23, dataset = "OPRA.PILLAR", venue = "EMLD", description = "OPRA - MIAX Emerald" }
PublisherDetail { publisher_id = 24, dataset = "OPRA.PILLAR", venue = "EDGO", description = "OPRA - Cboe EDGX Options" }
PublisherDetail { publisher_id = 25, dataset = "OPRA.PILLAR", venue = "GMNI", description = "OPRA - Nasdaq GEMX" }
PublisherDetail { publisher_id = 26, dataset = "OPRA.PILLAR", venue = "XISX", description = "OPRA - Nasdaq ISE" }
PublisherDetail { publisher_id = 27, dataset = "OPRA.PILLAR", venue = "MCRY", description = "OPRA - Nasdaq MRX" }
PublisherDetail { publisher_id = 28, dataset = "OPRA.PILLAR", venue = "XMIO", description = "OPRA - MIAX Options" }
PublisherDetail { publisher_id = 29, dataset = "OPRA.PILLAR", venue = "ARCO", description = "OPRA - NYSE Arca Options" }
PublisherDetail { publisher_id = 30, dataset = "OPRA.PILLAR", venue = "OPRA", description = "OPRA - Options Price Reporting Authority" }
PublisherDetail { publisher_id = 31, dataset = "OPRA.PILLAR", venue = "MPRL", description = "OPRA - MIAX Pearl" }
PublisherDetail { publisher_id = 32, dataset = "OPRA.PILLAR", venue = "XNDQ", description = "OPRA - Nasdaq Options" }
PublisherDetail { publisher_id = 33, dataset = "OPRA.PILLAR", venue = "XBXO", description = "OPRA - Nasdaq Texas Options" }
PublisherDetail { publisher_id = 34, dataset = "OPRA.PILLAR", venue = "C2OX", description = "OPRA - Cboe C2 Options" }
PublisherDetail { publisher_id = 35, dataset = "OPRA.PILLAR", venue = "XPHL", description = "OPRA - Nasdaq PHLX" }
PublisherDetail { publisher_id = 36, dataset = "OPRA.PILLAR", venue = "BATO", description = "OPRA - Cboe BZX Options" }
PublisherDetail { publisher_id = 37, dataset = "OPRA.PILLAR", venue = "MXOP", description = "OPRA - MEMX Options" }
PublisherDetail { publisher_id = 38, dataset = "IEXG.TOPS", venue = "IEXG", description = "IEX TOPS" }
PublisherDetail { publisher_id = 39, dataset = "DBEQ.BASIC", venue = "XCHI", description = "DBEQ Basic - NYSE Texas" }
PublisherDetail { publisher_id = 40, dataset = "DBEQ.BASIC", venue = "XCIS", description = "DBEQ Basic - NYSE National" }
PublisherDetail { publisher_id = 41, dataset = "DBEQ.BASIC", venue = "IEXG", description = "DBEQ Basic - IEX" }
PublisherDetail { publisher_id = 42, dataset = "DBEQ.BASIC", venue = "EPRL", description = "DBEQ Basic - MIAX Pearl" }
PublisherDetail { publisher_id = 43, dataset = "ARCX.PILLAR", venue = "ARCX", description = "NYSE Arca Integrated" }
PublisherDetail { publisher_id = 44, dataset = "XNYS.BBO", venue = "XNYS", description = "NYSE BBO" }
PublisherDetail { publisher_id = 45, dataset = "XNYS.TRADES", venue = "XNYS", description = "NYSE Trades" }
PublisherDetail { publisher_id = 46, dataset = "XNAS.QBBO", venue = "XNAS", description = "Nasdaq QBBO" }
PublisherDetail { publisher_id = 47, dataset = "XNAS.NLS", venue = "XNAS", description = "Nasdaq Trades" }
PublisherDetail { publisher_id = 48, dataset = "EQUS.PLUS", venue = "XCHI", description = "Databento US Equities Plus - NYSE Texas" }
PublisherDetail { publisher_id = 49, dataset = "EQUS.PLUS", venue = "XCIS", description = "Databento US Equities Plus - NYSE National" }
PublisherDetail { publisher_id = 50, dataset = "EQUS.PLUS", venue = "IEXG", description = "Databento US Equities Plus - IEX" }
PublisherDetail { publisher_id = 51, dataset = "EQUS.PLUS", venue = "EPRL", description = "Databento US Equities Plus - MIAX Pearl" }
PublisherDetail { publisher_id = 52, dataset = "EQUS.PLUS", venue = "XNAS", description = "Databento US Equities Plus - Nasdaq" }
PublisherDetail { publisher_id = 53, dataset = "EQUS.PLUS", venue = "XNYS", description = "Databento US Equities Plus - NYSE" }
PublisherDetail { publisher_id = 54, dataset = "EQUS.PLUS", venue = "FINN", description = "Databento US Equities Plus - FINRA/Nasdaq TRF Carteret" }
PublisherDetail { publisher_id = 55, dataset = "EQUS.PLUS", venue = "FINY", description = "Databento US Equities Plus - FINRA/NYSE TRF" }
PublisherDetail { publisher_id = 56, dataset = "EQUS.PLUS", venue = "FINC", description = "Databento US Equities Plus - FINRA/Nasdaq TRF Chicago" }
PublisherDetail { publisher_id = 57, dataset = "IFEU.IMPACT", venue = "IFEU", description = "ICE Europe Commodities" }
PublisherDetail { publisher_id = 58, dataset = "NDEX.IMPACT", venue = "NDEX", description = "ICE Endex" }
PublisherDetail { publisher_id = 59, dataset = "DBEQ.BASIC", venue = "DBEQ", description = "Databento US Equities Basic - Consolidated" }
PublisherDetail { publisher_id = 60, dataset = "EQUS.PLUS", venue = "EQUS", description = "EQUS Plus - Consolidated" }
PublisherDetail { publisher_id = 61, dataset = "OPRA.PILLAR", venue = "SPHR", description = "OPRA - MIAX Sapphire" }
PublisherDetail { publisher_id = 62, dataset = "EQUS.ALL", venue = "XCHI", description = "Databento US Equities (All Feeds) - NYSE Texas" }
PublisherDetail { publisher_id = 63, dataset = "EQUS.ALL", venue = "XCIS", description = "Databento US Equities (All Feeds) - NYSE National" }
PublisherDetail { publisher_id = 64, dataset = "EQUS.ALL", venue = "IEXG", description = "Databento US Equities (All Feeds) - IEX" }
PublisherDetail { publisher_id = 65, dataset = "EQUS.ALL", venue = "EPRL", description = "Databento US Equities (All Feeds) - MIAX Pearl" }
PublisherDetail { publisher_id = 66, dataset = "EQUS.ALL", venue = "XNAS", description = "Databento US Equities (All Feeds) - Nasdaq" }
PublisherDetail { publisher_id = 67, dataset = "EQUS.ALL", venue = "XNYS", description = "Databento US Equities (All Feeds) - NYSE" }
PublisherDetail { publisher_id = 68, dataset = "EQUS.ALL", venue = "FINN", description = "Databento US Equities (All Feeds) - FINRA/Nasdaq TRF Carteret" }
PublisherDetail { publisher_id = 69, dataset = "EQUS.ALL", venue = "FINY", description = "Databento US Equities (All Feeds) - FINRA/NYSE TRF" }
PublisherDetail { publisher_id = 70, dataset = "EQUS.ALL", venue = "FINC", description = "Databento US Equities (All Feeds) - FINRA/Nasdaq TRF Chicago" }
PublisherDetail { publisher_id = 71, dataset = "EQUS.ALL", venue = "BATS", description = "Databento US Equities (All Feeds) - Cboe BZX" }
PublisherDetail { publisher_id = 72, dataset = "EQUS.ALL", venue = "BATY", description = "Databento US Equities (All Feeds) - Cboe BYX" }
PublisherDetail { publisher_id = 73, dataset = "EQUS.ALL", venue = "EDGA", description = "Databento US Equities (All Feeds) - Cboe EDGA" }
PublisherDetail { publisher_id = 74, dataset = "EQUS.ALL", venue = "EDGX", description = "Databento US Equities (All Feeds) - Cboe EDGX" }
PublisherDetail { publisher_id = 75, dataset = "EQUS.ALL", venue = "XBOS", description = "Databento US Equities (All Feeds) - Nasdaq Texas" }
PublisherDetail { publisher_id = 76, dataset = "EQUS.ALL", venue = "XPSX", description = "Databento US Equities (All Feeds) - Nasdaq PSX" }
PublisherDetail { publisher_id = 77, dataset = "EQUS.ALL", venue = "MEMX", description = "Databento US Equities (All Feeds) - MEMX" }
PublisherDetail { publisher_id = 78, dataset = "EQUS.ALL", venue = "XASE", description = "Databento US Equities (All Feeds) - NYSE American" }
PublisherDetail { publisher_id = 79, dataset = "EQUS.ALL", venue = "ARCX", description = "Databento US Equities (All Feeds) - NYSE Arca" }
PublisherDetail { publisher_id = 80, dataset = "EQUS.ALL", venue = "LTSE", description = "Databento US Equities (All Feeds) - Long-Term Stock Exchange" }
PublisherDetail { publisher_id = 81, dataset = "XNAS.BASIC", venue = "XNAS", description = "Nasdaq Basic - Nasdaq" }
PublisherDetail { publisher_id = 82, dataset = "XNAS.BASIC", venue = "FINN", description = "Nasdaq Basic - FINRA/Nasdaq TRF Carteret" }
PublisherDetail { publisher_id = 83, dataset = "XNAS.BASIC", venue = "FINC", description = "Nasdaq Basic - FINRA/Nasdaq TRF Chicago" }
PublisherDetail { publisher_id = 84, dataset = "IFEU.IMPACT", venue = "XOFF", description = "ICE Europe - Off-Market Trades" }
PublisherDetail { publisher_id = 85, dataset = "NDEX.IMPACT", venue = "XOFF", description = "ICE Endex - Off-Market Trades" }
PublisherDetail { publisher_id = 86, dataset = "XNAS.NLS", venue = "XBOS", description = "Nasdaq NLS - Nasdaq Texas" }
PublisherDetail { publisher_id = 87, dataset = "XNAS.NLS", venue = "XPSX", description = "Nasdaq NLS - Nasdaq PSX" }
PublisherDetail { publisher_id = 88, dataset = "XNAS.BASIC", venue = "XBOS", description = "Nasdaq Basic - Nasdaq Texas" }
PublisherDetail { publisher_id = 89, dataset = "XNAS.BASIC", venue = "XPSX", description = "Nasdaq Basic - Nasdaq PSX" }
PublisherDetail { publisher_id = 90, dataset = "EQUS.SUMMARY", venue = "EQUS", description = "Databento Equities Summary" }
PublisherDetail { publisher_id = 91, dataset = "XCIS.TRADESBBO", venue = "XCIS", description = "NYSE National Trades and BBO" }
PublisherDetail { publisher_id = 92, dataset = "XNYS.TRADESBBO", venue = "XNYS", description = "NYSE Trades and BBO" }
PublisherDetail { publisher_id = 93, dataset = "XNAS.BASIC", venue = "EQUS", description = "Nasdaq Basic - Consolidated" }
PublisherDetail { publisher_id = 94, dataset = "EQUS.ALL", venue = "EQUS", description = "Databento US Equities (All Feeds) - Consolidated" }
PublisherDetail { publisher_id = 95, dataset = "EQUS.MINI", venue = "EQUS", description = "Databento US Equities Mini" }
PublisherDetail { publisher_id = 96, dataset = "XNYS.TRADES", venue = "EQUS", description = "NYSE Trades - Consolidated" }
PublisherDetail { publisher_id = 97, dataset = "IFUS.IMPACT", venue = "IFUS", description = "ICE Futures US" }
PublisherDetail { publisher_id = 98, dataset = "IFUS.IMPACT", venue = "XOFF", description = "ICE Futures US - Off-Market Trades" }
PublisherDetail { publisher_id = 99, dataset = "IFLL.IMPACT", venue = "IFLL", description = "ICE Europe Financials" }
PublisherDetail { publisher_id = 100, dataset = "IFLL.IMPACT", venue = "XOFF", description = "ICE Europe Financials - Off-Market Trades" }
PublisherDetail { publisher_id = 101, dataset = "XEUR.EOBI", venue = "XEUR", description = "Eurex EOBI" }
PublisherDetail { publisher_id = 102, dataset = "XEEE.EOBI", venue = "XEEE", description = "European Energy Exchange EOBI" }
PublisherDetail { publisher_id = 103, dataset = "XEUR.EOBI", venue = "XOFF", description = "Eurex EOBI - Off-Market Trades" }
PublisherDetail { publisher_id = 104, dataset = "XEEE.EOBI", venue = "XOFF", description = "European Energy Exchange EOBI - Off-Market Trades" }
PublisherDetail { publisher_id = 105, dataset = "XCBF.PITCH", venue = "XCBF", description = "Cboe Futures Exchange (CFE)" }
PublisherDetail { publisher_id = 106, dataset = "XCBF.PITCH", venue = "XOFF", description = "Cboe Futures Exchange (CFE) - Off-Market Trades" }
PublisherDetail { publisher_id = 107, dataset = "OCEA.MEMOIR", venue = "OCEA", description = "Blue Ocean ATS MEMOIR" }
PublisherDetail { publisher_id = 108, dataset = "OPRA.PILLAR", venue = "MXTO", description = "OPRA - MEMX MX2 Options" }
PublisherDetail { publisher_id = 109, dataset = "OPRA.PILLAR", venue = "IEXO", description = "OPRA - IEX Options LLC" }
PublisherDetail { publisher_id = 110, dataset = "MAIN.CGIF", venue = "MAIN", description = "Cboe Global Indices Feed" }
PublisherDetail { publisher_id = 111, dataset = "EQUS.SIP", venue = "XASE", description = "US Equities SIP - NYSE American" }
PublisherDetail { publisher_id = 112, dataset = "EQUS.SIP", venue = "XBOS", description = "US Equities SIP - Nasdaq Texas" }
PublisherDetail { publisher_id = 113, dataset = "EQUS.SIP", venue = "XCIS", description = "US Equities SIP - NYSE National" }
PublisherDetail { publisher_id = 114, dataset = "EQUS.SIP", venue = "TXSE", description = "US Equities SIP - Texas Stock Exchange" }
PublisherDetail { publisher_id = 115, dataset = "EQUS.SIP", venue = "24EQ", description = "US Equities SIP - 24X National Exchange" }
PublisherDetail { publisher_id = 116, dataset = "EQUS.SIP", venue = "EPRL", description = "US Equities SIP - MIAX Pearl" }
PublisherDetail { publisher_id = 117, dataset = "EQUS.SIP", venue = "XISX", description = "US Equities SIP - Nasdaq ISE" }
PublisherDetail { publisher_id = 118, dataset = "EQUS.SIP", venue = "EDGA", description = "US Equities SIP - Cboe EDGA" }
PublisherDetail { publisher_id = 119, dataset = "EQUS.SIP", venue = "EDGX", description = "US Equities SIP - Cboe EDGX" }
PublisherDetail { publisher_id = 120, dataset = "EQUS.SIP", venue = "LTSE", description = "US Equities SIP - Long-Term Stock Exchange" }
PublisherDetail { publisher_id = 121, dataset = "EQUS.SIP", venue = "XCHI", description = "US Equities SIP - NYSE Texas" }
PublisherDetail { publisher_id = 122, dataset = "EQUS.SIP", venue = "XNYS", description = "US Equities SIP - NYSE" }
PublisherDetail { publisher_id = 123, dataset = "EQUS.SIP", venue = "ARCX", description = "US Equities SIP - NYSE Arca" }
PublisherDetail { publisher_id = 124, dataset = "EQUS.SIP", venue = "XNAS", description = "US Equities SIP - Nasdaq" }
PublisherDetail { publisher_id = 125, dataset = "EQUS.SIP", venue = "MEMX", description = "US Equities SIP - MEMX" }
PublisherDetail { publisher_id = 126, dataset = "EQUS.SIP", venue = "IEXG", description = "US Equities SIP - IEX" }
PublisherDetail { publisher_id = 127, dataset = "EQUS.SIP", venue = "XPSX", description = "US Equities SIP - Nasdaq PSX" }
PublisherDetail { publisher_id = 128, dataset = "EQUS.SIP", venue = "BATY", description = "US Equities SIP - Cboe BYX" }
PublisherDetail { publisher_id = 129, dataset = "EQUS.SIP", venue = "BATS", description = "US Equities SIP - Cboe BZX" }
PublisherDetail { publisher_id = 130, dataset = "EQUS.SIP", venue = "FINN", description = "US Equities SIP - FINRA/Nasdaq TRF Carteret" }
PublisherDetail { publisher_id = 131, dataset = "EQUS.SIP", venue = "FINY", description = "US Equities SIP - FINRA/NYSE TRF" }
PublisherDetail { publisher_id = 132, dataset = "EQUS.SIP", venue = "FINC", description = "US Equities SIP - FINRA/Nasdaq TRF Chicago" }
PublisherDetail { publisher_id = 133, dataset = "EQUS.SIP", venue = "XADF", description = "US Equities SIP - FINRA Alternative Display Facility" }
PublisherDetail { publisher_id = 134, dataset = "EQUS.SIP", venue = "CTA", description = "US Equities SIP - CTA" }
PublisherDetail { publisher_id = 135, dataset = "EQUS.SIP", venue = "UTP", description = "US Equities SIP - UTP" }
PublisherDetail { publisher_id = 136, dataset = "MSCI.CGIF", venue = "MSCI", description = "CGIF - Morgan Stanley Capital International" }
PublisherDetail { publisher_id = 137, dataset = "FTSE.CGIF", venue = "FTSE", description = "CGIF - FTSE Russell" }
PublisherDetail { publisher_id = 138, dataset = "INAV.CGIF", venue = "INAV", description = "CGIF - Intraday Net Asset Values" }
PublisherDetail { publisher_id = 139, dataset = "MSTAR.CGIF", venue = "MSTAR", description = "CGIF - Morning Star" }
PublisherDetail { publisher_id = 140, dataset = "CCCY.CGIF", venue = "CCCY", description = "CGIF - Crypto Currency" }
PublisherDetail { publisher_id = 141, dataset = "CGI.CGIF", venue = "CGI", description = "CGIF - CBOE Global Indices" }
PublisherDetail { publisher_id = 142, dataset = "MAIN.CGIF", venue = "DEF", description = "CGIF - Definitions" }
PublisherDetail { publisher_id = 143, dataset = "XTKS.FLEX", venue = "XTKS", description = "JPX - Tokyo Stock Exchange" }
PublisherDetail { publisher_id = 144, dataset = "XTKT.ITCH", venue = "XTKT", description = "JPX - Tokyo Commodity Exchange" }
PublisherDetail { publisher_id = 145, dataset = "XOSE.ITCH", venue = "XOSE", description = "JPX - Osaka Exchange" }
PublisherDetail { publisher_id = 146, dataset = "DBIX.CORE", venue = "MAIN", description = "CGIF - Main Feed" }
PublisherDetail { publisher_id = 147, dataset = "DBIX.CORE", venue = "MSCI", description = "CGIF - Morgan Stanley Capital International" }
PublisherDetail { publisher_id = 148, dataset = "DBIX.CORE", venue = "FTSE", description = "CGIF - FTSE Russell" }
PublisherDetail { publisher_id = 149, dataset = "DBIX.CORE", venue = "INAV", description = "CGIF - Intraday Net Asset Values" }
PublisherDetail { publisher_id = 150, dataset = "DBIX.CORE", venue = "MSTAR", description = "CGIF - Morning Star" }
PublisherDetail { publisher_id = 151, dataset = "DBIX.CORE", venue = "CCCY", description = "CGIF - Crypto Currency" }
PublisherDetail { publisher_id = 152, dataset = "DBIX.CORE", venue = "CGI", description = "CGIF - CBOE Global Indices" }
```

### /metadata.list_publishers

List allpublisher IDmappings.

Use this method to list the details of publishers, including their dataset and venue mappings.

#### Returns

A list of publisher details objects.

| Field | Type | Description |
| --- | --- | --- |
| publisher_id | number | The publisher ID assigned by Databento. |
| dataset | string | The dataset ID for the publisher. |
| venue | string | The venue for the publisher. |
| description | string | The publisher description. |

```python
GET https://hist.databento.com/v0/metadata.list_publishers
```

```python
1
2
```

```python
curl -G 'https://hist.databento.com/v0/metadata.list_publishers' \
 -u $YOUR_API_KEY:
```

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
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
387
388
389
390
391
392
393
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
409
410
411
412
413
414
415
416
417
418
419
420
421
422
423
424
425
426
427
428
429
430
431
432
433
434
435
436
437
438
439
440
441
442
443
444
445
446
447
448
449
450
451
452
453
454
455
456
457
458
459
460
461
462
463
464
465
466
467
468
469
470
471
472
473
474
475
476
477
478
479
480
481
482
483
484
485
486
487
488
489
490
491
492
493
494
495
496
497
498
499
500
501
502
503
504
505
506
507
508
509
510
511
512
513
514
515
516
517
518
519
520
521
522
523
524
525
526
527
528
529
530
531
532
533
534
535
536
537
538
539
540
541
542
543
544
545
546
547
548
549
550
551
552
553
554
555
556
557
558
559
560
561
562
563
564
565
566
567
568
569
570
571
572
573
574
575
576
577
578
579
580
581
582
583
584
585
586
587
588
589
590
591
592
593
594
595
596
597
598
599
600
601
602
603
604
605
606
607
608
609
610
611
612
613
614
615
616
617
618
619
620
621
622
623
624
625
626
627
628
629
630
631
632
633
634
635
636
637
638
639
640
641
642
643
644
645
646
647
648
649
650
651
652
653
654
655
656
657
658
659
660
661
662
663
664
665
666
667
668
669
670
671
672
673
674
675
676
677
678
679
680
681
682
683
684
685
686
687
688
689
690
691
692
693
694
695
696
697
698
699
700
701
702
703
704
705
706
707
708
709
710
711
712
713
714
715
716
717
718
719
720
721
722
723
724
725
726
727
728
729
730
731
732
733
734
735
736
737
738
739
740
741
742
743
744
745
746
747
748
749
750
751
752
753
754
755
756
757
758
759
760
761
762
763
764
765
766
767
768
769
770
771
772
773
774
775
776
777
778
779
780
781
782
783
784
785
786
787
788
789
790
791
792
793
794
795
796
797
798
799
800
801
802
803
804
805
806
807
808
809
810
811
812
813
814
815
816
817
818
819
820
821
822
823
824
825
826
827
828
829
830
831
832
833
834
835
836
837
838
839
840
841
842
843
844
845
846
847
848
849
850
851
852
853
854
855
856
857
858
859
860
861
862
863
864
865
866
867
868
869
870
871
872
873
874
875
876
877
878
879
880
881
882
883
884
885
886
887
888
889
890
891
892
893
894
895
896
897
898
899
900
901
902
903
904
905
906
907
908
909
910
911
912
913
914
915
916
917
918
919
920
```

```python
[
  {
    "publisher_id": 1,
    "dataset": "GLBX.MDP3",
    "venue": "GLBX",
    "description": "CME Globex MDP 3.0"
  },
  {
    "publisher_id": 2,
    "dataset": "XNAS.ITCH",
    "venue": "XNAS",
    "description": "Nasdaq TotalView-ITCH"
  },
  {
    "publisher_id": 3,
    "dataset": "XBOS.ITCH",
    "venue": "XBOS",
    "description": "Nasdaq Texas TotalView-ITCH"
  },
  {
    "publisher_id": 4,
    "dataset": "XPSX.ITCH",
    "venue": "XPSX",
    "description": "Nasdaq PSX TotalView-ITCH"
  },
  {
    "publisher_id": 5,
    "dataset": "BATS.PITCH",
    "venue": "BATS",
    "description": "Cboe BZX Depth"
  },
  {
    "publisher_id": 6,
    "dataset": "BATY.PITCH",
    "venue": "BATY",
    "description": "Cboe BYX Depth"
  },
  {
    "publisher_id": 7,
    "dataset": "EDGA.PITCH",
    "venue": "EDGA",
    "description": "Cboe EDGA Depth"
  },
  {
    "publisher_id": 8,
    "dataset": "EDGX.PITCH",
    "venue": "EDGX",
    "description": "Cboe EDGX Depth"
  },
  {
    "publisher_id": 9,
    "dataset": "XNYS.PILLAR",
    "venue": "XNYS",
    "description": "NYSE Integrated"
  },
  {
    "publisher_id": 10,
    "dataset": "XCIS.PILLAR",
    "venue": "XCIS",
    "description": "NYSE National Integrated"
  },
  {
    "publisher_id": 11,
    "dataset": "XASE.PILLAR",
    "venue": "XASE",
    "description": "NYSE American Integrated"
  },
  {
    "publisher_id": 12,
    "dataset": "XCHI.PILLAR",
    "venue": "XCHI",
    "description": "NYSE Texas Integrated"
  },
  {
    "publisher_id": 13,
    "dataset": "XCIS.BBO",
    "venue": "XCIS",
    "description": "NYSE National BBO"
  },
  {
    "publisher_id": 14,
    "dataset": "XCIS.TRADES",
    "venue": "XCIS",
    "description": "NYSE National Trades"
  },
  {
    "publisher_id": 15,
    "dataset": "MEMX.MEMOIR",
    "venue": "MEMX",
    "description": "MEMX MEMOIR Depth"
  },
  {
    "publisher_id": 16,
    "dataset": "EPRL.DOM",
    "venue": "EPRL",
    "description": "MIAX Pearl Depth"
  },
  {
    "publisher_id": 17,
    "dataset": "XNAS.NLS",
    "venue": "FINN",
    "description": "FINRA/Nasdaq TRF Carteret"
  },
  {
    "publisher_id": 18,
    "dataset": "XNAS.NLS",
    "venue": "FINC",
    "description": "FINRA/Nasdaq TRF Chicago"
  },
  {
    "publisher_id": 19,
    "dataset": "XNYS.TRADES",
    "venue": "FINY",
    "description": "FINRA/NYSE TRF"
  },
  {
    "publisher_id": 20,
    "dataset": "OPRA.PILLAR",
    "venue": "AMXO",
    "description": "OPRA - NYSE American Options"
  },
  {
    "publisher_id": 21,
    "dataset": "OPRA.PILLAR",
    "venue": "XBOX",
    "description": "OPRA - BOX Options"
  },
  {
    "publisher_id": 22,
    "dataset": "OPRA.PILLAR",
    "venue": "XCBO",
    "description": "OPRA - Cboe Options"
  },
  {
    "publisher_id": 23,
    "dataset": "OPRA.PILLAR",
    "venue": "EMLD",
    "description": "OPRA - MIAX Emerald"
  },
  {
    "publisher_id": 24,
    "dataset": "OPRA.PILLAR",
    "venue": "EDGO",
    "description": "OPRA - Cboe EDGX Options"
  },
  {
    "publisher_id": 25,
    "dataset": "OPRA.PILLAR",
    "venue": "GMNI",
    "description": "OPRA - Nasdaq GEMX"
  },
  {
    "publisher_id": 26,
    "dataset": "OPRA.PILLAR",
    "venue": "XISX",
    "description": "OPRA - Nasdaq ISE"
  },
  {
    "publisher_id": 27,
    "dataset": "OPRA.PILLAR",
    "venue": "MCRY",
    "description": "OPRA - Nasdaq MRX"
  },
  {
    "publisher_id": 28,
    "dataset": "OPRA.PILLAR",
    "venue": "XMIO",
    "description": "OPRA - MIAX Options"
  },
  {
    "publisher_id": 29,
    "dataset": "OPRA.PILLAR",
    "venue": "ARCO",
    "description": "OPRA - NYSE Arca Options"
  },
  {
    "publisher_id": 30,
    "dataset": "OPRA.PILLAR",
    "venue": "OPRA",
    "description": "OPRA - Options Price Reporting Authority"
  },
  {
    "publisher_id": 31,
    "dataset": "OPRA.PILLAR",
    "venue": "MPRL",
    "description": "OPRA - MIAX Pearl"
  },
  {
    "publisher_id": 32,
    "dataset": "OPRA.PILLAR",
    "venue": "XNDQ",
    "description": "OPRA - Nasdaq Options"
  },
  {
    "publisher_id": 33,
    "dataset": "OPRA.PILLAR",
    "venue": "XBXO",
    "description": "OPRA - Nasdaq Texas Options"
  },
  {
    "publisher_id": 34,
    "dataset": "OPRA.PILLAR",
    "venue": "C2OX",
    "description": "OPRA - Cboe C2 Options"
  },
  {
    "publisher_id": 35,
    "dataset": "OPRA.PILLAR",
    "venue": "XPHL",
    "description": "OPRA - Nasdaq PHLX"
  },
  {
    "publisher_id": 36,
    "dataset": "OPRA.PILLAR",
    "venue": "BATO",
    "description": "OPRA - Cboe BZX Options"
  },
  {
    "publisher_id": 37,
    "dataset": "OPRA.PILLAR",
    "venue": "MXOP",
    "description": "OPRA - MEMX Options"
  },
  {
    "publisher_id": 38,
    "dataset": "IEXG.TOPS",
    "venue": "IEXG",
    "description": "IEX TOPS"
  },
  {
    "publisher_id": 39,
    "dataset": "DBEQ.BASIC",
    "venue": "XCHI",
    "description": "DBEQ Basic - NYSE Texas"
  },
  {
    "publisher_id": 40,
    "dataset": "DBEQ.BASIC",
    "venue": "XCIS",
    "description": "DBEQ Basic - NYSE National"
  },
  {
    "publisher_id": 41,
    "dataset": "DBEQ.BASIC",
    "venue": "IEXG",
    "description": "DBEQ Basic - IEX"
  },
  {
    "publisher_id": 42,
    "dataset": "DBEQ.BASIC",
    "venue": "EPRL",
    "description": "DBEQ Basic - MIAX Pearl"
  },
  {
    "publisher_id": 43,
    "dataset": "ARCX.PILLAR",
    "venue": "ARCX",
    "description": "NYSE Arca Integrated"
  },
  {
    "publisher_id": 44,
    "dataset": "XNYS.BBO",
    "venue": "XNYS",
    "description": "NYSE BBO"
  },
  {
    "publisher_id": 45,
    "dataset": "XNYS.TRADES",
    "venue": "XNYS",
    "description": "NYSE Trades"
  },
  {
    "publisher_id": 46,
    "dataset": "XNAS.QBBO",
    "venue": "XNAS",
    "description": "Nasdaq QBBO"
  },
  {
    "publisher_id": 47,
    "dataset": "XNAS.NLS",
    "venue": "XNAS",
    "description": "Nasdaq Trades"
  },
  {
    "publisher_id": 48,
    "dataset": "EQUS.PLUS",
    "venue": "XCHI",
    "description": "Databento US Equities Plus - NYSE Texas"
  },
  {
    "publisher_id": 49,
    "dataset": "EQUS.PLUS",
    "venue": "XCIS",
    "description": "Databento US Equities Plus - NYSE National"
  },
  {
    "publisher_id": 50,
    "dataset": "EQUS.PLUS",
    "venue": "IEXG",
    "description": "Databento US Equities Plus - IEX"
  },
  {
    "publisher_id": 51,
    "dataset": "EQUS.PLUS",
    "venue": "EPRL",
    "description": "Databento US Equities Plus - MIAX Pearl"
  },
  {
    "publisher_id": 52,
    "dataset": "EQUS.PLUS",
    "venue": "XNAS",
    "description": "Databento US Equities Plus - Nasdaq"
  },
  {
    "publisher_id": 53,
    "dataset": "EQUS.PLUS",
    "venue": "XNYS",
    "description": "Databento US Equities Plus - NYSE"
  },
  {
    "publisher_id": 54,
    "dataset": "EQUS.PLUS",
    "venue": "FINN",
    "description": "Databento US Equities Plus - FINRA/Nasdaq TRF Carteret"
  },
  {
    "publisher_id": 55,
    "dataset": "EQUS.PLUS",
    "venue": "FINY",
    "description": "Databento US Equities Plus - FINRA/NYSE TRF"
  },
  {
    "publisher_id": 56,
    "dataset": "EQUS.PLUS",
    "venue": "FINC",
    "description": "Databento US Equities Plus - FINRA/Nasdaq TRF Chicago"
  },
  {
    "publisher_id": 57,
    "dataset": "IFEU.IMPACT",
    "venue": "IFEU",
    "description": "ICE Europe Commodities"
  },
  {
    "publisher_id": 58,
    "dataset": "NDEX.IMPACT",
    "venue": "NDEX",
    "description": "ICE Endex"
  },
  {
    "publisher_id": 59,
    "dataset": "DBEQ.BASIC",
    "venue": "DBEQ",
    "description": "Databento US Equities Basic - Consolidated"
  },
  {
    "publisher_id": 60,
    "dataset": "EQUS.PLUS",
    "venue": "EQUS",
    "description": "EQUS Plus - Consolidated"
  },
  {
    "publisher_id": 61,
    "dataset": "OPRA.PILLAR",
    "venue": "SPHR",
    "description": "OPRA - MIAX Sapphire"
  },
  {
    "publisher_id": 62,
    "dataset": "EQUS.ALL",
    "venue": "XCHI",
    "description": "Databento US Equities (All Feeds) - NYSE Texas"
  },
  {
    "publisher_id": 63,
    "dataset": "EQUS.ALL",
    "venue": "XCIS",
    "description": "Databento US Equities (All Feeds) - NYSE National"
  },
  {
    "publisher_id": 64,
    "dataset": "EQUS.ALL",
    "venue": "IEXG",
    "description": "Databento US Equities (All Feeds) - IEX"
  },
  {
    "publisher_id": 65,
    "dataset": "EQUS.ALL",
    "venue": "EPRL",
    "description": "Databento US Equities (All Feeds) - MIAX Pearl"
  },
  {
    "publisher_id": 66,
    "dataset": "EQUS.ALL",
    "venue": "XNAS",
    "description": "Databento US Equities (All Feeds) - Nasdaq"
  },
  {
    "publisher_id": 67,
    "dataset": "EQUS.ALL",
    "venue": "XNYS",
    "description": "Databento US Equities (All Feeds) - NYSE"
  },
  {
    "publisher_id": 68,
    "dataset": "EQUS.ALL",
    "venue": "FINN",
    "description": "Databento US Equities (All Feeds) - FINRA/Nasdaq TRF Carteret"
  },
  {
    "publisher_id": 69,
    "dataset": "EQUS.ALL",
    "venue": "FINY",
    "description": "Databento US Equities (All Feeds) - FINRA/NYSE TRF"
  },
  {
    "publisher_id": 70,
    "dataset": "EQUS.ALL",
    "venue": "FINC",
    "description": "Databento US Equities (All Feeds) - FINRA/Nasdaq TRF Chicago"
  },
  {
    "publisher_id": 71,
    "dataset": "EQUS.ALL",
    "venue": "BATS",
    "description": "Databento US Equities (All Feeds) - Cboe BZX"
  },
  {
    "publisher_id": 72,
    "dataset": "EQUS.ALL",
    "venue": "BATY",
    "description": "Databento US Equities (All Feeds) - Cboe BYX"
  },
  {
    "publisher_id": 73,
    "dataset": "EQUS.ALL",
    "venue": "EDGA",
    "description": "Databento US Equities (All Feeds) - Cboe EDGA"
  },
  {
    "publisher_id": 74,
    "dataset": "EQUS.ALL",
    "venue": "EDGX",
    "description": "Databento US Equities (All Feeds) - Cboe EDGX"
  },
  {
    "publisher_id": 75,
    "dataset": "EQUS.ALL",
    "venue": "XBOS",
    "description": "Databento US Equities (All Feeds) - Nasdaq Texas"
  },
  {
    "publisher_id": 76,
    "dataset": "EQUS.ALL",
    "venue": "XPSX",
    "description": "Databento US Equities (All Feeds) - Nasdaq PSX"
  },
  {
    "publisher_id": 77,
    "dataset": "EQUS.ALL",
    "venue": "MEMX",
    "description": "Databento US Equities (All Feeds) - MEMX"
  },
  {
    "publisher_id": 78,
    "dataset": "EQUS.ALL",
    "venue": "XASE",
    "description": "Databento US Equities (All Feeds) - NYSE American"
  },
  {
    "publisher_id": 79,
    "dataset": "EQUS.ALL",
    "venue": "ARCX",
    "description": "Databento US Equities (All Feeds) - NYSE Arca"
  },
  {
    "publisher_id": 80,
    "dataset": "EQUS.ALL",
    "venue": "LTSE",
    "description": "Databento US Equities (All Feeds) - Long-Term Stock Exchange"
  },
  {
    "publisher_id": 81,
    "dataset": "XNAS.BASIC",
    "venue": "XNAS",
    "description": "Nasdaq Basic - Nasdaq"
  },
  {
    "publisher_id": 82,
    "dataset": "XNAS.BASIC",
    "venue": "FINN",
    "description": "Nasdaq Basic - FINRA/Nasdaq TRF Carteret"
  },
  {
    "publisher_id": 83,
    "dataset": "XNAS.BASIC",
    "venue": "FINC",
    "description": "Nasdaq Basic - FINRA/Nasdaq TRF Chicago"
  },
  {
    "publisher_id": 84,
    "dataset": "IFEU.IMPACT",
    "venue": "XOFF",
    "description": "ICE Europe - Off-Market Trades"
  },
  {
    "publisher_id": 85,
    "dataset": "NDEX.IMPACT",
    "venue": "XOFF",
    "description": "ICE Endex - Off-Market Trades"
  },
  {
    "publisher_id": 86,
    "dataset": "XNAS.NLS",
    "venue": "XBOS",
    "description": "Nasdaq NLS - Nasdaq Texas"
  },
  {
    "publisher_id": 87,
    "dataset": "XNAS.NLS",
    "venue": "XPSX",
    "description": "Nasdaq NLS - Nasdaq PSX"
  },
  {
    "publisher_id": 88,
    "dataset": "XNAS.BASIC",
    "venue": "XBOS",
    "description": "Nasdaq Basic - Nasdaq Texas"
  },
  {
    "publisher_id": 89,
    "dataset": "XNAS.BASIC",
    "venue": "XPSX",
    "description": "Nasdaq Basic - Nasdaq PSX"
  },
  {
    "publisher_id": 90,
    "dataset": "EQUS.SUMMARY",
    "venue": "EQUS",
    "description": "Databento Equities Summary"
  },
  {
    "publisher_id": 91,
    "dataset": "XCIS.TRADESBBO",
    "venue": "XCIS",
    "description": "NYSE National Trades and BBO"
  },
  {
    "publisher_id": 92,
    "dataset": "XNYS.TRADESBBO",
    "venue": "XNYS",
    "description": "NYSE Trades and BBO"
  },
  {
    "publisher_id": 93,
    "dataset": "XNAS.BASIC",
    "venue": "EQUS",
    "description": "Nasdaq Basic - Consolidated"
  },
  {
    "publisher_id": 94,
    "dataset": "EQUS.ALL",
    "venue": "EQUS",
    "description": "Databento US Equities (All Feeds) - Consolidated"
  },
  {
    "publisher_id": 95,
    "dataset": "EQUS.MINI",
    "venue": "EQUS",
    "description": "Databento US Equities Mini"
  },
  {
    "publisher_id": 96,
    "dataset": "XNYS.TRADES",
    "venue": "EQUS",
    "description": "NYSE Trades - Consolidated"
  },
  {
    "publisher_id": 97,
    "dataset": "IFUS.IMPACT",
    "venue": "IFUS",
    "description": "ICE Futures US"
  },
  {
    "publisher_id": 98,
    "dataset": "IFUS.IMPACT",
    "venue": "XOFF",
    "description": "ICE Futures US - Off-Market Trades"
  },
  {
    "publisher_id": 99,
    "dataset": "IFLL.IMPACT",
    "venue": "IFLL",
    "description": "ICE Europe Financials"
  },
  {
    "publisher_id": 100,
    "dataset": "IFLL.IMPACT",
    "venue": "XOFF",
    "description": "ICE Europe Financials - Off-Market Trades"
  },
  {
    "publisher_id": 101,
    "dataset": "XEUR.EOBI",
    "venue": "XEUR",
    "description": "Eurex EOBI"
  },
  {
    "publisher_id": 102,
    "dataset": "XEEE.EOBI",
    "venue": "XEEE",
    "description": "European Energy Exchange EOBI"
  },
  {
    "publisher_id": 103,
    "dataset": "XEUR.EOBI",
    "venue": "XOFF",
    "description": "Eurex EOBI - Off-Market Trades"
  },
  {
    "publisher_id": 104,
    "dataset": "XEEE.EOBI",
    "venue": "XOFF",
    "description": "European Energy Exchange EOBI - Off-Market Trades"
  },
  {
    "publisher_id": 105,
    "dataset": "XCBF.PITCH",
    "venue": "XCBF",
    "description": "Cboe Futures Exchange (CFE)"
  },
  {
    "publisher_id": 106,
    "dataset": "XCBF.PITCH",
    "venue": "XOFF",
    "description": "Cboe Futures Exchange (CFE) - Off-Market Trades"
  },
  {
    "publisher_id": 107,
    "dataset": "OCEA.MEMOIR",
    "venue": "OCEA",
    "description": "Blue Ocean ATS MEMOIR"
  },
  {
    "publisher_id": 108,
    "dataset": "OPRA.PILLAR",
    "venue": "MXTO",
    "description": "OPRA - MEMX MX2 Options"
  },
  {
    "publisher_id": 109,
    "dataset": "OPRA.PILLAR",
    "venue": "IEXO",
    "description": "OPRA - IEX Options LLC"
  },
  {
    "publisher_id": 110,
    "dataset": "MAIN.CGIF",
    "venue": "MAIN",
    "description": "Cboe Global Indices Feed"
  },
  {
    "publisher_id": 111,
    "dataset": "EQUS.SIP",
    "venue": "XASE",
    "description": "US Equities SIP - NYSE American"
  },
  {
    "publisher_id": 112,
    "dataset": "EQUS.SIP",
    "venue": "XBOS",
    "description": "US Equities SIP - Nasdaq Texas"
  },
  {
    "publisher_id": 113,
    "dataset": "EQUS.SIP",
    "venue": "XCIS",
    "description": "US Equities SIP - NYSE National"
  },
  {
    "publisher_id": 114,
    "dataset": "EQUS.SIP",
    "venue": "TXSE",
    "description": "US Equities SIP - Texas Stock Exchange"
  },
  {
    "publisher_id": 115,
    "dataset": "EQUS.SIP",
    "venue": "24EQ",
    "description": "US Equities SIP - 24X National Exchange"
  },
  {
    "publisher_id": 116,
    "dataset": "EQUS.SIP",
    "venue": "EPRL",
    "description": "US Equities SIP - MIAX Pearl"
  },
  {
    "publisher_id": 117,
    "dataset": "EQUS.SIP",
    "venue": "XISX",
    "description": "US Equities SIP - Nasdaq ISE"
  },
  {
    "publisher_id": 118,
    "dataset": "EQUS.SIP",
    "venue": "EDGA",
    "description": "US Equities SIP - Cboe EDGA"
  },
  {
    "publisher_id": 119,
    "dataset": "EQUS.SIP",
    "venue": "EDGX",
    "description": "US Equities SIP - Cboe EDGX"
  },
  {
    "publisher_id": 120,
    "dataset": "EQUS.SIP",
    "venue": "LTSE",
    "description": "US Equities SIP - Long-Term Stock Exchange"
  },
  {
    "publisher_id": 121,
    "dataset": "EQUS.SIP",
    "venue": "XCHI",
    "description": "US Equities SIP - NYSE Texas"
  },
  {
    "publisher_id": 122,
    "dataset": "EQUS.SIP",
    "venue": "XNYS",
    "description": "US Equities SIP - NYSE"
  },
  {
    "publisher_id": 123,
    "dataset": "EQUS.SIP",
    "venue": "ARCX",
    "description": "US Equities SIP - NYSE Arca"
  },
  {
    "publisher_id": 124,
    "dataset": "EQUS.SIP",
    "venue": "XNAS",
    "description": "US Equities SIP - Nasdaq"
  },
  {
    "publisher_id": 125,
    "dataset": "EQUS.SIP",
    "venue": "MEMX",
    "description": "US Equities SIP - MEMX"
  },
  {
    "publisher_id": 126,
    "dataset": "EQUS.SIP",
    "venue": "IEXG",
    "description": "US Equities SIP - IEX"
  },
  {
    "publisher_id": 127,
    "dataset": "EQUS.SIP",
    "venue": "XPSX",
    "description": "US Equities SIP - Nasdaq PSX"
  },
  {
    "publisher_id": 128,
    "dataset": "EQUS.SIP",
    "venue": "BATY",
    "description": "US Equities SIP - Cboe BYX"
  },
  {
    "publisher_id": 129,
    "dataset": "EQUS.SIP",
    "venue": "BATS",
    "description": "US Equities SIP - Cboe BZX"
  },
  {
    "publisher_id": 130,
    "dataset": "EQUS.SIP",
    "venue": "FINN",
    "description": "US Equities SIP - FINRA/Nasdaq TRF Carteret"
  },
  {
    "publisher_id": 131,
    "dataset": "EQUS.SIP",
    "venue": "FINY",
    "description": "US Equities SIP - FINRA/NYSE TRF"
  },
  {
    "publisher_id": 132,
    "dataset": "EQUS.SIP",
    "venue": "FINC",
    "description": "US Equities SIP - FINRA/Nasdaq TRF Chicago"
  },
  {
    "publisher_id": 133,
    "dataset": "EQUS.SIP",
    "venue": "XADF",
    "description": "US Equities SIP - FINRA Alternative Display Facility"
  },
  {
    "publisher_id": 134,
    "dataset": "EQUS.SIP",
    "venue": "CTA",
    "description": "US Equities SIP - CTA"
  },
  {
    "publisher_id": 135,
    "dataset": "EQUS.SIP",
    "venue": "UTP",
    "description": "US Equities SIP - UTP"
  },
  {
    "publisher_id": 136,
    "dataset": "MSCI.CGIF",
    "venue": "MSCI",
    "description": "CGIF - Morgan Stanley Capital International"
  },
  {
    "publisher_id": 137,
    "dataset": "FTSE.CGIF",
    "venue": "FTSE",
    "description": "CGIF - FTSE Russell"
  },
  {
    "publisher_id": 138,
    "dataset": "INAV.CGIF",
    "venue": "INAV",
    "description": "CGIF - Intraday Net Asset Values"
  },
  {
    "publisher_id": 139,
    "dataset": "MSTAR.CGIF",
    "venue": "MSTAR",
    "description": "CGIF - Morning Star"
  },
  {
    "publisher_id": 140,
    "dataset": "CCCY.CGIF",
    "venue": "CCCY",
    "description": "CGIF - Crypto Currency"
  },
  {
    "publisher_id": 141,
    "dataset": "CGI.CGIF",
    "venue": "CGI",
    "description": "CGIF - CBOE Global Indices"
  },
  {
    "publisher_id": 142,
    "dataset": "MAIN.CGIF",
    "venue": "CDEF",
    "description": "CGIF - Definitions"
  },
  {
    "publisher_id": 143,
    "dataset": "XTKS.FLEX",
    "venue": "XTKS",
    "description": "JPX - Tokyo Stock Exchange"
  },
  {
    "publisher_id": 144,
    "dataset": "XTKT.ITCH",
    "venue": "XTKT",
    "description": "JPX - Tokyo Commodity Exchange"
  },
  {
    "publisher_id": 145,
    "dataset": "XOSE.ITCH",
    "venue": "XOSE",
    "description": "JPX - Osaka Exchange"
  },
  {
    "publisher_id": 146,
    "dataset": "DBIX.CORE",
    "venue": "MAIN",
    "description": "CGIF - Main Feed"
  },
  {
    "publisher_id": 147,
    "dataset": "DBIX.CORE",
    "venue": "MSCI",
    "description": "CGIF - Morgan Stanley Capital International"
  },
  {
    "publisher_id": 148,
    "dataset": "DBIX.CORE",
    "venue": "FTSE",
    "description": "CGIF - FTSE Russell"
  },
  {
    "publisher_id": 149,
    "dataset": "DBIX.CORE",
    "venue": "INAV",
    "description": "CGIF - Intraday Net Asset Values"
  },
  {
    "publisher_id": 150,
    "dataset": "DBIX.CORE",
    "venue": "MSTAR",
    "description": "CGIF - Morning Star"
  },
  {
    "publisher_id": 151,
    "dataset": "DBIX.CORE",
    "venue": "CCCY",
    "description": "CGIF - Crypto Currency"
  },
  {
    "publisher_id": 152,
    "dataset": "DBIX.CORE",
    "venue": "CGI",
    "description": "CGIF - CBOE Global Indices"
  },
  {
    "publisher_id": 153,
    "dataset": "DBIX.CORE",
    "venue": "CDEF",
    "description": "CGIF - Definitions"
  }
]
```

### Historical.metadata.list_publishers

List allpublisher IDmappings.

Use this method to list the details of publishers, including their dataset and venue mappings.

#### Returns

list[dict[str, int | str]]

A list of publisher details objects.

| Field | Type | Description |
| --- | --- | --- |
| publisher_id | int | The publisher ID assigned by Databento. |
| dataset | str | The dataset ID for the publisher. |
| venue | str | The venue for the publisher. |
| description | str | The publisher description. |

```python
Historical.metadata.list_publishers() -> list[dict[str, int | str]]
```

```python
1
2
3
4
5
6
```

```python
import databento as db

client = db.Historical("$YOUR_API_KEY")

publishers = client.metadata.list_publishers()
print(publishers)
```

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
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
387
388
389
390
391
392
393
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
409
410
411
412
413
414
415
416
417
418
419
420
421
422
423
424
425
426
427
428
429
430
431
432
433
434
435
436
437
438
439
440
441
442
443
444
445
446
447
448
449
450
451
452
453
454
455
456
457
458
459
460
461
462
463
464
465
466
467
468
469
470
471
472
473
474
475
476
477
478
479
480
481
482
483
484
485
486
487
488
489
490
491
492
493
494
495
496
497
498
499
500
501
502
503
504
505
506
507
508
509
510
511
512
513
514
515
516
517
518
519
520
521
522
523
524
525
526
527
528
529
530
531
532
533
534
535
536
537
538
539
540
541
542
543
544
545
546
547
548
549
550
551
552
553
554
555
556
557
558
559
560
561
562
563
564
565
566
567
568
569
570
571
572
573
574
575
576
577
578
579
580
581
582
583
584
585
586
587
588
589
590
591
592
593
594
595
596
597
598
599
600
601
602
603
604
605
606
607
608
609
610
611
612
613
```

```python
[{'dataset': 'GLBX.MDP3',
  'description': 'CME Globex MDP 3.0',
  'publisher_id': 1,
  'venue': 'GLBX'},
 {'dataset': 'XNAS.ITCH',
  'description': 'Nasdaq TotalView-ITCH',
  'publisher_id': 2,
  'venue': 'XNAS'},
 {'dataset': 'XBOS.ITCH',
  'description': 'Nasdaq Texas TotalView-ITCH',
  'publisher_id': 3,
  'venue': 'XBOS'},
 {'dataset': 'XPSX.ITCH',
  'description': 'Nasdaq PSX TotalView-ITCH',
  'publisher_id': 4,
  'venue': 'XPSX'},
 {'dataset': 'BATS.PITCH',
  'description': 'Cboe BZX Depth',
  'publisher_id': 5,
  'venue': 'BATS'},
 {'dataset': 'BATY.PITCH',
  'description': 'Cboe BYX Depth',
  'publisher_id': 6,
  'venue': 'BATY'},
 {'dataset': 'EDGA.PITCH',
  'description': 'Cboe EDGA Depth',
  'publisher_id': 7,
  'venue': 'EDGA'},
 {'dataset': 'EDGX.PITCH',
  'description': 'Cboe EDGX Depth',
  'publisher_id': 8,
  'venue': 'EDGX'},
 {'dataset': 'XNYS.PILLAR',
  'description': 'NYSE Integrated',
  'publisher_id': 9,
  'venue': 'XNYS'},
 {'dataset': 'XCIS.PILLAR',
  'description': 'NYSE National Integrated',
  'publisher_id': 10,
  'venue': 'XCIS'},
 {'dataset': 'XASE.PILLAR',
  'description': 'NYSE American Integrated',
  'publisher_id': 11,
  'venue': 'XASE'},
 {'dataset': 'XCHI.PILLAR',
  'description': 'NYSE Texas Integrated',
  'publisher_id': 12,
  'venue': 'XCHI'},
 {'dataset': 'XCIS.BBO',
  'description': 'NYSE National BBO',
  'publisher_id': 13,
  'venue': 'XCIS'},
 {'dataset': 'XCIS.TRADES',
  'description': 'NYSE National Trades',
  'publisher_id': 14,
  'venue': 'XCIS'},
 {'dataset': 'MEMX.MEMOIR',
  'description': 'MEMX MEMOIR Depth',
  'publisher_id': 15,
  'venue': 'MEMX'},
 {'dataset': 'EPRL.DOM',
  'description': 'MIAX Pearl Depth',
  'publisher_id': 16,
  'venue': 'EPRL'},
 {'dataset': 'XNAS.NLS',
  'description': 'FINRA/Nasdaq TRF Carteret',
  'publisher_id': 17,
  'venue': 'FINN'},
 {'dataset': 'XNAS.NLS',
  'description': 'FINRA/Nasdaq TRF Chicago',
  'publisher_id': 18,
  'venue': 'FINC'},
 {'dataset': 'XNYS.TRADES',
  'description': 'FINRA/NYSE TRF',
  'publisher_id': 19,
  'venue': 'FINY'},
 {'dataset': 'OPRA.PILLAR',
  'description': 'OPRA - NYSE American Options',
  'publisher_id': 20,
  'venue': 'AMXO'},
 {'dataset': 'OPRA.PILLAR',
  'description': 'OPRA - BOX Options',
  'publisher_id': 21,
  'venue': 'XBOX'},
 {'dataset': 'OPRA.PILLAR',
  'description': 'OPRA - Cboe Options',
  'publisher_id': 22,
  'venue': 'XCBO'},
 {'dataset': 'OPRA.PILLAR',
  'description': 'OPRA - MIAX Emerald',
  'publisher_id': 23,
  'venue': 'EMLD'},
 {'dataset': 'OPRA.PILLAR',
  'description': 'OPRA - Cboe EDGX Options',
  'publisher_id': 24,
  'venue': 'EDGO'},
 {'dataset': 'OPRA.PILLAR',
  'description': 'OPRA - Nasdaq GEMX',
  'publisher_id': 25,
  'venue': 'GMNI'},
 {'dataset': 'OPRA.PILLAR',
  'description': 'OPRA - Nasdaq ISE',
  'publisher_id': 26,
  'venue': 'XISX'},
 {'dataset': 'OPRA.PILLAR',
  'description': 'OPRA - Nasdaq MRX',
  'publisher_id': 27,
  'venue': 'MCRY'},
 {'dataset': 'OPRA.PILLAR',
  'description': 'OPRA - MIAX Options',
  'publisher_id': 28,
  'venue': 'XMIO'},
 {'dataset': 'OPRA.PILLAR',
  'description': 'OPRA - NYSE Arca Options',
  'publisher_id': 29,
  'venue': 'ARCO'},
 {'dataset': 'OPRA.PILLAR',
  'description': 'OPRA - Options Price Reporting Authority',
  'publisher_id': 30,
  'venue': 'OPRA'},
 {'dataset': 'OPRA.PILLAR',
  'description': 'OPRA - MIAX Pearl',
  'publisher_id': 31,
  'venue': 'MPRL'},
 {'dataset': 'OPRA.PILLAR',
  'description': 'OPRA - Nasdaq Options',
  'publisher_id': 32,
  'venue': 'XNDQ'},
 {'dataset': 'OPRA.PILLAR',
  'description': 'OPRA - Nasdaq Texas Options',
  'publisher_id': 33,
  'venue': 'XBXO'},
 {'dataset': 'OPRA.PILLAR',
  'description': 'OPRA - Cboe C2 Options',
  'publisher_id': 34,
  'venue': 'C2OX'},
 {'dataset': 'OPRA.PILLAR',
  'description': 'OPRA - Nasdaq PHLX',
  'publisher_id': 35,
  'venue': 'XPHL'},
 {'dataset': 'OPRA.PILLAR',
  'description': 'OPRA - Cboe BZX Options',
  'publisher_id': 36,
  'venue': 'BATO'},
 {'dataset': 'OPRA.PILLAR',
  'description': 'OPRA - MEMX Options',
  'publisher_id': 37,
  'venue': 'MXOP'},
 {'dataset': 'IEXG.TOPS',
  'description': 'IEX TOPS',
  'publisher_id': 38,
  'venue': 'IEXG'},
 {'dataset': 'DBEQ.BASIC',
  'description': 'DBEQ Basic - NYSE Texas',
  'publisher_id': 39,
  'venue': 'XCHI'},
 {'dataset': 'DBEQ.BASIC',
  'description': 'DBEQ Basic - NYSE National',
  'publisher_id': 40,
  'venue': 'XCIS'},
 {'dataset': 'DBEQ.BASIC',
  'description': 'DBEQ Basic - IEX',
  'publisher_id': 41,
  'venue': 'IEXG'},
 {'dataset': 'DBEQ.BASIC',
  'description': 'DBEQ Basic - MIAX Pearl',
  'publisher_id': 42,
  'venue': 'EPRL'},
 {'dataset': 'ARCX.PILLAR',
  'description': 'NYSE Arca Integrated',
  'publisher_id': 43,
  'venue': 'ARCX'},
 {'dataset': 'XNYS.BBO',
  'description': 'NYSE BBO',
  'publisher_id': 44,
  'venue': 'XNYS'},
 {'dataset': 'XNYS.TRADES',
  'description': 'NYSE Trades',
  'publisher_id': 45,
  'venue': 'XNYS'},
 {'dataset': 'XNAS.QBBO',
  'description': 'Nasdaq QBBO',
  'publisher_id': 46,
  'venue': 'XNAS'},
 {'dataset': 'XNAS.NLS',
  'description': 'Nasdaq Trades',
  'publisher_id': 47,
  'venue': 'XNAS'},
 {'dataset': 'EQUS.PLUS',
  'description': 'Databento US Equities Plus - NYSE Texas',
  'publisher_id': 48,
  'venue': 'XCHI'},
 {'dataset': 'EQUS.PLUS',
  'description': 'Databento US Equities Plus - NYSE National',
  'publisher_id': 49,
  'venue': 'XCIS'},
 {'dataset': 'EQUS.PLUS',
  'description': 'Databento US Equities Plus - IEX',
  'publisher_id': 50,
  'venue': 'IEXG'},
 {'dataset': 'EQUS.PLUS',
  'description': 'Databento US Equities Plus - MIAX Pearl',
  'publisher_id': 51,
  'venue': 'EPRL'},
 {'dataset': 'EQUS.PLUS',
  'description': 'Databento US Equities Plus - Nasdaq',
  'publisher_id': 52,
  'venue': 'XNAS'},
 {'dataset': 'EQUS.PLUS',
  'description': 'Databento US Equities Plus - NYSE',
  'publisher_id': 53,
  'venue': 'XNYS'},
 {'dataset': 'EQUS.PLUS',
  'description': 'Databento US Equities Plus - FINRA/Nasdaq TRF Carteret',
  'publisher_id': 54,
  'venue': 'FINN'},
 {'dataset': 'EQUS.PLUS',
  'description': 'Databento US Equities Plus - FINRA/NYSE TRF',
  'publisher_id': 55,
  'venue': 'FINY'},
 {'dataset': 'EQUS.PLUS',
  'description': 'Databento US Equities Plus - FINRA/Nasdaq TRF Chicago',
  'publisher_id': 56,
  'venue': 'FINC'},
 {'dataset': 'IFEU.IMPACT',
  'description': 'ICE Europe Commodities',
  'publisher_id': 57,
  'venue': 'IFEU'},
 {'dataset': 'NDEX.IMPACT',
  'description': 'ICE Endex',
  'publisher_id': 58,
  'venue': 'NDEX'},
 {'dataset': 'DBEQ.BASIC',
  'description': 'Databento US Equities Basic - Consolidated',
  'publisher_id': 59,
  'venue': 'DBEQ'},
 {'dataset': 'EQUS.PLUS',
  'description': 'EQUS Plus - Consolidated',
  'publisher_id': 60,
  'venue': 'EQUS'},
 {'dataset': 'OPRA.PILLAR',
  'description': 'OPRA - MIAX Sapphire',
  'publisher_id': 61,
  'venue': 'SPHR'},
 {'dataset': 'EQUS.ALL',
  'description': 'Databento US Equities (All Feeds) - NYSE Texas',
  'publisher_id': 62,
  'venue': 'XCHI'},
 {'dataset': 'EQUS.ALL',
  'description': 'Databento US Equities (All Feeds) - NYSE National',
  'publisher_id': 63,
  'venue': 'XCIS'},
 {'dataset': 'EQUS.ALL',
  'description': 'Databento US Equities (All Feeds) - IEX',
  'publisher_id': 64,
  'venue': 'IEXG'},
 {'dataset': 'EQUS.ALL',
  'description': 'Databento US Equities (All Feeds) - MIAX Pearl',
  'publisher_id': 65,
  'venue': 'EPRL'},
 {'dataset': 'EQUS.ALL',
  'description': 'Databento US Equities (All Feeds) - Nasdaq',
  'publisher_id': 66,
  'venue': 'XNAS'},
 {'dataset': 'EQUS.ALL',
  'description': 'Databento US Equities (All Feeds) - NYSE',
  'publisher_id': 67,
  'venue': 'XNYS'},
 {'dataset': 'EQUS.ALL',
  'description': 'Databento US Equities (All Feeds) - FINRA/Nasdaq TRF Carteret',
  'publisher_id': 68,
  'venue': 'FINN'},
 {'dataset': 'EQUS.ALL',
  'description': 'Databento US Equities (All Feeds) - FINRA/NYSE TRF',
  'publisher_id': 69,
  'venue': 'FINY'},
 {'dataset': 'EQUS.ALL',
  'description': 'Databento US Equities (All Feeds) - FINRA/Nasdaq TRF Chicago',
  'publisher_id': 70,
  'venue': 'FINC'},
 {'dataset': 'EQUS.ALL',
  'description': 'Databento US Equities (All Feeds) - Cboe BZX',
  'publisher_id': 71,
  'venue': 'BATS'},
 {'dataset': 'EQUS.ALL',
  'description': 'Databento US Equities (All Feeds) - Cboe BYX',
  'publisher_id': 72,
  'venue': 'BATY'},
 {'dataset': 'EQUS.ALL',
  'description': 'Databento US Equities (All Feeds) - Cboe EDGA',
  'publisher_id': 73,
  'venue': 'EDGA'},
 {'dataset': 'EQUS.ALL',
  'description': 'Databento US Equities (All Feeds) - Cboe EDGX',
  'publisher_id': 74,
  'venue': 'EDGX'},
 {'dataset': 'EQUS.ALL',
  'description': 'Databento US Equities (All Feeds) - Nasdaq Texas',
  'publisher_id': 75,
  'venue': 'XBOS'},
 {'dataset': 'EQUS.ALL',
  'description': 'Databento US Equities (All Feeds) - Nasdaq PSX',
  'publisher_id': 76,
  'venue': 'XPSX'},
 {'dataset': 'EQUS.ALL',
  'description': 'Databento US Equities (All Feeds) - MEMX',
  'publisher_id': 77,
  'venue': 'MEMX'},
 {'dataset': 'EQUS.ALL',
  'description': 'Databento US Equities (All Feeds) - NYSE American',
  'publisher_id': 78,
  'venue': 'XASE'},
 {'dataset': 'EQUS.ALL',
  'description': 'Databento US Equities (All Feeds) - NYSE Arca',
  'publisher_id': 79,
  'venue': 'ARCX'},
 {'dataset': 'EQUS.ALL',
  'description': 'Databento US Equities (All Feeds) - Long-Term Stock Exchange',
  'publisher_id': 80,
  'venue': 'LTSE'},
 {'dataset': 'XNAS.BASIC',
  'description': 'Nasdaq Basic - Nasdaq',
  'publisher_id': 81,
  'venue': 'XNAS'},
 {'dataset': 'XNAS.BASIC',
  'description': 'Nasdaq Basic - FINRA/Nasdaq TRF Carteret',
  'publisher_id': 82,
  'venue': 'FINN'},
 {'dataset': 'XNAS.BASIC',
  'description': 'Nasdaq Basic - FINRA/Nasdaq TRF Chicago',
  'publisher_id': 83,
  'venue': 'FINC'},
 {'dataset': 'IFEU.IMPACT',
  'description': 'ICE Europe - Off-Market Trades',
  'publisher_id': 84,
  'venue': 'XOFF'},
 {'dataset': 'NDEX.IMPACT',
  'description': 'ICE Endex - Off-Market Trades',
  'publisher_id': 85,
  'venue': 'XOFF'},
 {'dataset': 'XNAS.NLS',
  'description': 'Nasdaq NLS - Nasdaq Texas',
  'publisher_id': 86,
  'venue': 'XBOS'},
 {'dataset': 'XNAS.NLS',
  'description': 'Nasdaq NLS - Nasdaq PSX',
  'publisher_id': 87,
  'venue': 'XPSX'},
 {'dataset': 'XNAS.BASIC',
  'description': 'Nasdaq Basic - Nasdaq Texas',
  'publisher_id': 88,
  'venue': 'XBOS'},
 {'dataset': 'XNAS.BASIC',
  'description': 'Nasdaq Basic - Nasdaq PSX',
  'publisher_id': 89,
  'venue': 'XPSX'},
 {'dataset': 'EQUS.SUMMARY',
  'description': 'Databento Equities Summary',
  'publisher_id': 90,
  'venue': 'EQUS'},
 {'dataset': 'XCIS.TRADESBBO',
  'description': 'NYSE National Trades and BBO',
  'publisher_id': 91,
  'venue': 'XCIS'},
 {'dataset': 'XNYS.TRADESBBO',
  'description': 'NYSE Trades and BBO',
  'publisher_id': 92,
  'venue': 'XNYS'},
 {'dataset': 'XNAS.BASIC',
  'description': 'Nasdaq Basic - Consolidated',
  'publisher_id': 93,
  'venue': 'EQUS'},
 {'dataset': 'EQUS.ALL',
  'description': 'Databento US Equities (All Feeds) - Consolidated',
  'publisher_id': 94,
  'venue': 'EQUS'},
 {'dataset': 'EQUS.MINI',
  'description': 'Databento US Equities Mini',
  'publisher_id': 95,
  'venue': 'EQUS'},
 {'dataset': 'XNYS.TRADES',
  'description': 'NYSE Trades - Consolidated',
  'publisher_id': 96,
  'venue': 'EQUS'},
 {'dataset': 'IFUS.IMPACT',
  'description': 'ICE Futures US',
  'publisher_id': 97,
  'venue': 'IFUS'},
 {'dataset': 'IFUS.IMPACT',
  'description': 'ICE Futures US - Off-Market Trades',
  'publisher_id': 98,
  'venue': 'XOFF'},
 {'dataset': 'IFLL.IMPACT',
  'description': 'ICE Europe Financials',
  'publisher_id': 99,
  'venue': 'IFLL'},
 {'dataset': 'IFLL.IMPACT',
  'description': 'ICE Europe Financials - Off-Market Trades',
  'publisher_id': 100,
  'venue': 'XOFF'},
 {'dataset': 'XEUR.EOBI',
  'description': 'Eurex EOBI',
  'publisher_id': 101,
  'venue': 'XEUR'},
 {'dataset': 'XEEE.EOBI',
  'description': 'European Energy Exchange EOBI',
  'publisher_id': 102,
  'venue': 'XEEE'},
 {'dataset': 'XEUR.EOBI',
  'description': 'Eurex EOBI - Off-Market Trades',
  'publisher_id': 103,
  'venue': 'XOFF'},
 {'dataset': 'XEEE.EOBI',
  'description': 'European Energy Exchange EOBI - Off-Market Trades',
  'publisher_id': 104,
  'venue': 'XOFF'},
 {'dataset': 'XCBF.PITCH',
  'description': 'Cboe Futures Exchange (CFE)',
  'publisher_id': 105,
  'venue': 'XCBF'},
 {'dataset': 'XCBF.PITCH',
  'description': 'Cboe Futures Exchange (CFE) - Off-Market Trades',
  'publisher_id': 106,
  'venue': 'XOFF'},
 {'dataset': 'OCEA.MEMOIR',
  'description': 'Blue Ocean ATS MEMOIR',
  'publisher_id': 107,
  'venue': 'OCEA'},
 {'dataset': 'OPRA.PILLAR',
  'description': 'OPRA - MEMX MX2 Options',
  'publisher_id': 108,
  'venue': 'MXTO'},
 {'dataset': 'OPRA.PILLAR',
  'description': 'OPRA - IEX Options LLC',
  'publisher_id': 109,
  'venue': 'IEXO'},
 {'dataset': 'MAIN.CGIF',
  'description': 'Cboe Global Indices Feed',
  'publisher_id': 110,
  'venue': 'MAIN'},
 {'dataset': 'EQUS.SIP',
  'description': 'US Equities SIP - NYSE American',
  'publisher_id': 111,
  'venue': 'XASE'},
 {'dataset': 'EQUS.SIP',
  'description': 'US Equities SIP - Nasdaq Texas',
  'publisher_id': 112,
  'venue': 'XBOS'},
 {'dataset': 'EQUS.SIP',
  'description': 'US Equities SIP - NYSE National',
  'publisher_id': 113,
  'venue': 'XCIS'},
 {'dataset': 'EQUS.SIP',
  'description': 'US Equities SIP - Texas Stock Exchange',
  'publisher_id': 114,
  'venue': 'TXSE'},
 {'dataset': 'EQUS.SIP',
  'description': 'US Equities SIP - 24X National Exchange',
  'publisher_id': 115,
  'venue': '24EQ'},
 {'dataset': 'EQUS.SIP',
  'description': 'US Equities SIP - MIAX Pearl',
  'publisher_id': 116,
  'venue': 'EPRL'},
 {'dataset': 'EQUS.SIP',
  'description': 'US Equities SIP - Nasdaq ISE',
  'publisher_id': 117,
  'venue': 'XISX'},
 {'dataset': 'EQUS.SIP',
  'description': 'US Equities SIP - Cboe EDGA',
  'publisher_id': 118,
  'venue': 'EDGA'},
 {'dataset': 'EQUS.SIP',
  'description': 'US Equities SIP - Cboe EDGX',
  'publisher_id': 119,
  'venue': 'EDGX'},
 {'dataset': 'EQUS.SIP',
  'description': 'US Equities SIP - Long-Term Stock Exchange',
  'publisher_id': 120,
  'venue': 'LTSE'},
 {'dataset': 'EQUS.SIP',
  'description': 'US Equities SIP - NYSE Texas',
  'publisher_id': 121,
  'venue': 'XCHI'},
 {'dataset': 'EQUS.SIP',
  'description': 'US Equities SIP - NYSE',
  'publisher_id': 122,
  'venue': 'XNYS'},
 {'dataset': 'EQUS.SIP',
  'description': 'US Equities SIP - NYSE Arca',
  'publisher_id': 123,
  'venue': 'ARCX'},
 {'dataset': 'EQUS.SIP',
  'description': 'US Equities SIP - Nasdaq',
  'publisher_id': 124,
  'venue': 'XNAS'},
 {'dataset': 'EQUS.SIP',
  'description': 'US Equities SIP - MEMX',
  'publisher_id': 125,
  'venue': 'MEMX'},
 {'dataset': 'EQUS.SIP',
  'description': 'US Equities SIP - IEX',
  'publisher_id': 126,
  'venue': 'IEXG'},
 {'dataset': 'EQUS.SIP',
  'description': 'US Equities SIP - Nasdaq PSX',
  'publisher_id': 127,
  'venue': 'XPSX'},
 {'dataset': 'EQUS.SIP',
  'description': 'US Equities SIP - Cboe BYX',
  'publisher_id': 128,
  'venue': 'BATY'},
 {'dataset': 'EQUS.SIP',
  'description': 'US Equities SIP - Cboe BZX',
  'publisher_id': 129,
  'venue': 'BATS'},
 {'dataset': 'EQUS.SIP',
  'description': 'US Equities SIP - FINRA/Nasdaq TRF Carteret',
  'publisher_id': 130,
  'venue': 'FINN'},
 {'dataset': 'EQUS.SIP',
  'description': 'US Equities SIP - FINRA/NYSE TRF',
  'publisher_id': 131,
  'venue': 'FINY'},
 {'dataset': 'EQUS.SIP',
  'description': 'US Equities SIP - FINRA/Nasdaq TRF Chicago',
  'publisher_id': 132,
  'venue': 'FINC'},
 {'dataset': 'EQUS.SIP',
  'description': 'US Equities SIP - FINRA Alternative Display Facility',
  'publisher_id': 133,
  'venue': 'XADF'},
 {'dataset': 'EQUS.SIP',
  'description': 'US Equities SIP - CTA',
  'publisher_id': 134,
  'venue': 'CTA'},
 {'dataset': 'EQUS.SIP',
  'description': 'US Equities SIP - UTP',
  'publisher_id': 135,
  'venue': 'UTP'},
 {'dataset': 'MSCI.CGIF',
  'description': 'CGIF - Morgan Stanley Capital International',
  'publisher_id': 136,
  'venue': 'MSCI'},
 {'dataset': 'FTSE.CGIF',
  'description': 'CGIF - FTSE Russell',
  'publisher_id': 137,
  'venue': 'FTSE'},
 {'dataset': 'INAV.CGIF',
  'description': 'CGIF - Intraday Net Asset Values',
  'publisher_id': 138,
  'venue': 'INAV'},
 {'dataset': 'MSTAR.CGIF',
  'description': 'CGIF - Morning Star',
  'publisher_id': 139,
  'venue': 'MSTAR'},
 {'dataset': 'CCCY.CGIF',
  'description': 'CGIF - Crypto Currency',
  'publisher_id': 140,
  'venue': 'CCCY'},
 {'dataset': 'CGI.CGIF',
  'description': 'CGIF - CBOE Global Indices',
  'publisher_id': 141,
  'venue': 'CGI'},
 {'dataset': 'MAIN.CGIF',
  'description': 'CGIF - Definitions',
  'publisher_id': 142,
  'venue': 'CDEF'},
 {'dataset': 'XTKS.FLEX',
  'description': 'JPX - Tokyo Stock Exchange',
  'publisher_id': 143,
  'venue': 'XTKS'},
 {'dataset': 'XTKT.ITCH',
  'description': 'JPX - Tokyo Commodity Exchange',
  'publisher_id': 144,
  'venue': 'XTKT'},
 {'dataset': 'XOSE.ITCH',
  'description': 'JPX - Osaka Exchange',
  'publisher_id': 145,
  'venue': 'XOSE'},
 {'dataset': 'DBIX.CORE',
  'description': 'CGIF - Main Feed',
  'publisher_id': 146,
  'venue': 'MAIN'},
 {'dataset': 'DBIX.CORE',
  'description': 'CGIF - Morgan Stanley Capital International',
  'publisher_id': 147,
  'venue': 'MSCI'},
 {'dataset': 'DBIX.CORE',
  'description': 'CGIF - FTSE Russell',
  'publisher_id': 148,
  'venue': 'FTSE'},
 {'dataset': 'DBIX.CORE',
  'description': 'CGIF - Intraday Net Asset Values',
  'publisher_id': 149,
  'venue': 'INAV'},
 {'dataset': 'DBIX.CORE',
  'description': 'CGIF - Morning Star',
  'publisher_id': 150,
  'venue': 'MSTAR'},
 {'dataset': 'DBIX.CORE',
  'description': 'CGIF - Crypto Currency',
  'publisher_id': 151,
  'venue': 'CCCY'},
 {'dataset': 'DBIX.CORE',
  'description': 'CGIF - CBOE Global Indices',
  'publisher_id': 152,
  'venue': 'CGI'},
 {'dataset': 'DBIX.CORE',
  'description': 'CGIF - Definitions',
  'publisher_id': 153,
  'venue': 'CDEF'}
 ]
```

### HistoricalClient::metadata::list_publishers

List allpublisher IDmappings.

Use this method to list the mappings of publisher names to publisher IDs.

#### Returns

Vec<PublisherDetail>

A list of publisher details, wherePublisherDetailis:

| Field | Type | Description |
| --- | --- | --- |
| publisher_id | u16 | The publisher ID assigned by Databento. |
| dataset | String | The dataset ID for the publisher. |
| venue | String | The venue for the publisher. |
| description | String | The publisher description. |

```python
pub async fn list_publishers(
    &mut self,
) -> databento::Result<Vec<PublisherDetail>>;
```

```python
1
2
3
4
5
6
7
```

```python
use databento::HistoricalClient;

let mut client =
    HistoricalClient::builder().key_from_env()?.build()?;
let publisher_mappings =
    client.metadata().list_publishers().await?;
println!("{publisher_mappings:#?}");
```

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
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
387
388
389
390
391
392
393
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
409
410
411
412
413
414
415
416
417
418
419
420
421
422
423
424
425
426
427
428
429
430
431
432
433
434
435
436
437
438
439
440
441
442
443
444
445
446
447
448
449
450
451
452
453
454
455
456
457
458
459
460
461
462
463
464
465
466
467
468
469
470
471
472
473
474
475
476
477
478
479
480
481
482
483
484
485
486
487
488
489
490
491
492
493
494
495
496
497
498
499
500
501
502
503
504
505
506
507
508
509
510
511
512
513
514
515
516
517
518
519
520
521
522
523
524
525
526
527
528
529
530
531
532
533
534
535
536
537
538
539
540
541
542
543
544
545
546
547
548
549
550
551
552
553
554
555
556
557
558
559
560
561
562
563
564
565
566
567
568
569
570
571
572
573
574
575
576
577
578
579
580
581
582
583
584
585
586
587
588
589
590
591
592
593
594
595
596
597
598
599
600
601
602
603
604
605
606
607
608
609
610
611
612
613
614
615
616
617
618
619
620
621
622
623
624
625
626
627
628
629
630
631
632
633
634
635
636
637
638
639
640
641
642
643
644
645
646
647
648
649
650
651
652
653
654
655
656
657
658
659
660
661
662
663
664
665
666
667
668
669
670
671
672
673
674
675
676
677
678
679
680
681
682
683
684
685
686
687
688
689
690
691
692
693
694
695
696
697
698
699
700
701
702
703
704
705
706
707
708
709
710
711
712
713
714
715
716
717
718
719
720
721
722
723
724
725
726
727
728
729
730
731
732
733
734
735
736
737
738
739
740
741
742
743
744
745
746
747
748
749
750
751
752
753
754
755
756
757
758
759
760
761
762
763
764
765
766
767
768
769
770
771
772
773
774
775
776
777
778
779
780
781
782
783
784
785
786
787
788
789
790
791
792
793
794
795
796
797
798
799
800
801
802
803
804
805
806
807
808
809
810
811
812
813
814
815
816
817
818
819
820
821
822
823
824
825
826
827
828
829
830
831
832
833
834
835
836
837
838
839
840
841
842
843
844
845
846
847
848
849
850
851
852
853
854
855
856
857
858
859
860
861
862
863
864
865
866
867
868
869
870
871
872
873
874
875
876
877
878
879
880
881
882
883
884
885
886
887
888
889
890
891
892
893
894
895
896
897
898
899
900
901
902
903
904
905
906
907
908
909
910
911
912
913
914
915
916
917
918
919
920
```

```python
[
    PublisherDetail {
        publisher_id: 1,
        dataset: "GLBX.MDP3",
        venue: "GLBX",
        description: "CME Globex MDP 3.0",
    },
    PublisherDetail {
        publisher_id: 2,
        dataset: "XNAS.ITCH",
        venue: "XNAS",
        description: "Nasdaq TotalView-ITCH",
    },
    PublisherDetail {
        publisher_id: 3,
        dataset: "XBOS.ITCH",
        venue: "XBOS",
        description: "Nasdaq Texas TotalView-ITCH",
    },
    PublisherDetail {
        publisher_id: 4,
        dataset: "XPSX.ITCH",
        venue: "XPSX",
        description: "Nasdaq PSX TotalView-ITCH",
    },
    PublisherDetail {
        publisher_id: 5,
        dataset: "BATS.PITCH",
        venue: "BATS",
        description: "Cboe BZX Depth",
    },
    PublisherDetail {
        publisher_id: 6,
        dataset: "BATY.PITCH",
        venue: "BATY",
        description: "Cboe BYX Depth",
    },
    PublisherDetail {
        publisher_id: 7,
        dataset: "EDGA.PITCH",
        venue: "EDGA",
        description: "Cboe EDGA Depth",
    },
    PublisherDetail {
        publisher_id: 8,
        dataset: "EDGX.PITCH",
        venue: "EDGX",
        description: "Cboe EDGX Depth",
    },
    PublisherDetail {
        publisher_id: 9,
        dataset: "XNYS.PILLAR",
        venue: "XNYS",
        description: "NYSE Integrated",
    },
    PublisherDetail {
        publisher_id: 10,
        dataset: "XCIS.PILLAR",
        venue: "XCIS",
        description: "NYSE National Integrated",
    },
    PublisherDetail {
        publisher_id: 11,
        dataset: "XASE.PILLAR",
        venue: "XASE",
        description: "NYSE American Integrated",
    },
    PublisherDetail {
        publisher_id: 12,
        dataset: "XCHI.PILLAR",
        venue: "XCHI",
        description: "NYSE Texas Integrated",
    },
    PublisherDetail {
        publisher_id: 13,
        dataset: "XCIS.BBO",
        venue: "XCIS",
        description: "NYSE National BBO",
    },
    PublisherDetail {
        publisher_id: 14,
        dataset: "XCIS.TRADES",
        venue: "XCIS",
        description: "NYSE National Trades",
    },
    PublisherDetail {
        publisher_id: 15,
        dataset: "MEMX.MEMOIR",
        venue: "MEMX",
        description: "MEMX MEMOIR Depth",
    },
    PublisherDetail {
        publisher_id: 16,
        dataset: "EPRL.DOM",
        venue: "EPRL",
        description: "MIAX Pearl Depth",
    },
    PublisherDetail {
        publisher_id: 17,
        dataset: "XNAS.NLS",
        venue: "FINN",
        description: "FINRA/Nasdaq TRF Carteret",
    },
    PublisherDetail {
        publisher_id: 18,
        dataset: "XNAS.NLS",
        venue: "FINC",
        description: "FINRA/Nasdaq TRF Chicago",
    },
    PublisherDetail {
        publisher_id: 19,
        dataset: "XNYS.TRADES",
        venue: "FINY",
        description: "FINRA/NYSE TRF",
    },
    PublisherDetail {
        publisher_id: 20,
        dataset: "OPRA.PILLAR",
        venue: "AMXO",
        description: "OPRA - NYSE American Options",
    },
    PublisherDetail {
        publisher_id: 21,
        dataset: "OPRA.PILLAR",
        venue: "XBOX",
        description: "OPRA - BOX Options",
    },
    PublisherDetail {
        publisher_id: 22,
        dataset: "OPRA.PILLAR",
        venue: "XCBO",
        description: "OPRA - Cboe Options",
    },
    PublisherDetail {
        publisher_id: 23,
        dataset: "OPRA.PILLAR",
        venue: "EMLD",
        description: "OPRA - MIAX Emerald",
    },
    PublisherDetail {
        publisher_id: 24,
        dataset: "OPRA.PILLAR",
        venue: "EDGO",
        description: "OPRA - Cboe EDGX Options",
    },
    PublisherDetail {
        publisher_id: 25,
        dataset: "OPRA.PILLAR",
        venue: "GMNI",
        description: "OPRA - Nasdaq GEMX",
    },
    PublisherDetail {
        publisher_id: 26,
        dataset: "OPRA.PILLAR",
        venue: "XISX",
        description: "OPRA - Nasdaq ISE",
    },
    PublisherDetail {
        publisher_id: 27,
        dataset: "OPRA.PILLAR",
        venue: "MCRY",
        description: "OPRA - Nasdaq MRX",
    },
    PublisherDetail {
        publisher_id: 28,
        dataset: "OPRA.PILLAR",
        venue: "XMIO",
        description: "OPRA - MIAX Options",
    },
    PublisherDetail {
        publisher_id: 29,
        dataset: "OPRA.PILLAR",
        venue: "ARCO",
        description: "OPRA - NYSE Arca Options",
    },
    PublisherDetail {
        publisher_id: 30,
        dataset: "OPRA.PILLAR",
        venue: "OPRA",
        description: "OPRA - Options Price Reporting Authority",
    },
    PublisherDetail {
        publisher_id: 31,
        dataset: "OPRA.PILLAR",
        venue: "MPRL",
        description: "OPRA - MIAX Pearl",
    },
    PublisherDetail {
        publisher_id: 32,
        dataset: "OPRA.PILLAR",
        venue: "XNDQ",
        description: "OPRA - Nasdaq Options",
    },
    PublisherDetail {
        publisher_id: 33,
        dataset: "OPRA.PILLAR",
        venue: "XBXO",
        description: "OPRA - Nasdaq Texas Options",
    },
    PublisherDetail {
        publisher_id: 34,
        dataset: "OPRA.PILLAR",
        venue: "C2OX",
        description: "OPRA - Cboe C2 Options",
    },
    PublisherDetail {
        publisher_id: 35,
        dataset: "OPRA.PILLAR",
        venue: "XPHL",
        description: "OPRA - Nasdaq PHLX",
    },
    PublisherDetail {
        publisher_id: 36,
        dataset: "OPRA.PILLAR",
        venue: "BATO",
        description: "OPRA - Cboe BZX Options",
    },
    PublisherDetail {
        publisher_id: 37,
        dataset: "OPRA.PILLAR",
        venue: "MXOP",
        description: "OPRA - MEMX Options",
    },
    PublisherDetail {
        publisher_id: 38,
        dataset: "IEXG.TOPS",
        venue: "IEXG",
        description: "IEX TOPS",
    },
    PublisherDetail {
        publisher_id: 39,
        dataset: "DBEQ.BASIC",
        venue: "XCHI",
        description: "DBEQ Basic - NYSE Texas",
    },
    PublisherDetail {
        publisher_id: 40,
        dataset: "DBEQ.BASIC",
        venue: "XCIS",
        description: "DBEQ Basic - NYSE National",
    },
    PublisherDetail {
        publisher_id: 41,
        dataset: "DBEQ.BASIC",
        venue: "IEXG",
        description: "DBEQ Basic - IEX",
    },
    PublisherDetail {
        publisher_id: 42,
        dataset: "DBEQ.BASIC",
        venue: "EPRL",
        description: "DBEQ Basic - MIAX Pearl",
    },
    PublisherDetail {
        publisher_id: 43,
        dataset: "ARCX.PILLAR",
        venue: "ARCX",
        description: "NYSE Arca Integrated",
    },
    PublisherDetail {
        publisher_id: 44,
        dataset: "XNYS.BBO",
        venue: "XNYS",
        description: "NYSE BBO",
    },
    PublisherDetail {
        publisher_id: 45,
        dataset: "XNYS.TRADES",
        venue: "XNYS",
        description: "NYSE Trades",
    },
    PublisherDetail {
        publisher_id: 46,
        dataset: "XNAS.QBBO",
        venue: "XNAS",
        description: "Nasdaq QBBO",
    },
    PublisherDetail {
        publisher_id: 47,
        dataset: "XNAS.NLS",
        venue: "XNAS",
        description: "Nasdaq Trades",
    },
    PublisherDetail {
        publisher_id: 48,
        dataset: "EQUS.PLUS",
        venue: "XCHI",
        description: "Databento US Equities Plus - NYSE Texas",
    },
    PublisherDetail {
        publisher_id: 49,
        dataset: "EQUS.PLUS",
        venue: "XCIS",
        description: "Databento US Equities Plus - NYSE National",
    },
    PublisherDetail {
        publisher_id: 50,
        dataset: "EQUS.PLUS",
        venue: "IEXG",
        description: "Databento US Equities Plus - IEX",
    },
    PublisherDetail {
        publisher_id: 51,
        dataset: "EQUS.PLUS",
        venue: "EPRL",
        description: "Databento US Equities Plus - MIAX Pearl",
    },
    PublisherDetail {
        publisher_id: 52,
        dataset: "EQUS.PLUS",
        venue: "XNAS",
        description: "Databento US Equities Plus - Nasdaq",
    },
    PublisherDetail {
        publisher_id: 53,
        dataset: "EQUS.PLUS",
        venue: "XNYS",
        description: "Databento US Equities Plus - NYSE",
    },
    PublisherDetail {
        publisher_id: 54,
        dataset: "EQUS.PLUS",
        venue: "FINN",
        description: "Databento US Equities Plus - FINRA/Nasdaq TRF Carteret",
    },
    PublisherDetail {
        publisher_id: 55,
        dataset: "EQUS.PLUS",
        venue: "FINY",
        description: "Databento US Equities Plus - FINRA/NYSE TRF",
    },
    PublisherDetail {
        publisher_id: 56,
        dataset: "EQUS.PLUS",
        venue: "FINC",
        description: "Databento US Equities Plus - FINRA/Nasdaq TRF Chicago",
    },
    PublisherDetail {
        publisher_id: 57,
        dataset: "IFEU.IMPACT",
        venue: "IFEU",
        description: "ICE Europe Commodities",
    },
    PublisherDetail {
        publisher_id: 58,
        dataset: "NDEX.IMPACT",
        venue: "NDEX",
        description: "ICE Endex",
    },
    PublisherDetail {
        publisher_id: 59,
        dataset: "DBEQ.BASIC",
        venue: "DBEQ",
        description: "Databento US Equities Basic - Consolidated",
    },
    PublisherDetail {
        publisher_id: 60,
        dataset: "EQUS.PLUS",
        venue: "EQUS",
        description: "EQUS Plus - Consolidated",
    },
    PublisherDetail {
        publisher_id: 61,
        dataset: "OPRA.PILLAR",
        venue: "SPHR",
        description: "OPRA - MIAX Sapphire",
    },
    PublisherDetail {
        publisher_id: 62,
        dataset: "EQUS.ALL",
        venue: "XCHI",
        description: "Databento US Equities (All Feeds) - NYSE Texas",
    },
    PublisherDetail {
        publisher_id: 63,
        dataset: "EQUS.ALL",
        venue: "XCIS",
        description: "Databento US Equities (All Feeds) - NYSE National",
    },
    PublisherDetail {
        publisher_id: 64,
        dataset: "EQUS.ALL",
        venue: "IEXG",
        description: "Databento US Equities (All Feeds) - IEX",
    },
    PublisherDetail {
        publisher_id: 65,
        dataset: "EQUS.ALL",
        venue: "EPRL",
        description: "Databento US Equities (All Feeds) - MIAX Pearl",
    },
    PublisherDetail {
        publisher_id: 66,
        dataset: "EQUS.ALL",
        venue: "XNAS",
        description: "Databento US Equities (All Feeds) - Nasdaq",
    },
    PublisherDetail {
        publisher_id: 67,
        dataset: "EQUS.ALL",
        venue: "XNYS",
        description: "Databento US Equities (All Feeds) - NYSE",
    },
    PublisherDetail {
        publisher_id: 68,
        dataset: "EQUS.ALL",
        venue: "FINN",
        description: "Databento US Equities (All Feeds) - FINRA/Nasdaq TRF Carteret",
    },
    PublisherDetail {
        publisher_id: 69,
        dataset: "EQUS.ALL",
        venue: "FINY",
        description: "Databento US Equities (All Feeds) - FINRA/NYSE TRF",
    },
    PublisherDetail {
        publisher_id: 70,
        dataset: "EQUS.ALL",
        venue: "FINC",
        description: "Databento US Equities (All Feeds) - FINRA/Nasdaq TRF Chicago",
    },
    PublisherDetail {
        publisher_id: 71,
        dataset: "EQUS.ALL",
        venue: "BATS",
        description: "Databento US Equities (All Feeds) - Cboe BZX",
    },
    PublisherDetail {
        publisher_id: 72,
        dataset: "EQUS.ALL",
        venue: "BATY",
        description: "Databento US Equities (All Feeds) - Cboe BYX",
    },
    PublisherDetail {
        publisher_id: 73,
        dataset: "EQUS.ALL",
        venue: "EDGA",
        description: "Databento US Equities (All Feeds) - Cboe EDGA",
    },
    PublisherDetail {
        publisher_id: 74,
        dataset: "EQUS.ALL",
        venue: "EDGX",
        description: "Databento US Equities (All Feeds) - Cboe EDGX",
    },
    PublisherDetail {
        publisher_id: 75,
        dataset: "EQUS.ALL",
        venue: "XBOS",
        description: "Databento US Equities (All Feeds) - Nasdaq Texas",
    },
    PublisherDetail {
        publisher_id: 76,
        dataset: "EQUS.ALL",
        venue: "XPSX",
        description: "Databento US Equities (All Feeds) - Nasdaq PSX",
    },
    PublisherDetail {
        publisher_id: 77,
        dataset: "EQUS.ALL",
        venue: "MEMX",
        description: "Databento US Equities (All Feeds) - MEMX",
    },
    PublisherDetail {
        publisher_id: 78,
        dataset: "EQUS.ALL",
        venue: "XASE",
        description: "Databento US Equities (All Feeds) - NYSE American",
    },
    PublisherDetail {
        publisher_id: 79,
        dataset: "EQUS.ALL",
        venue: "ARCX",
        description: "Databento US Equities (All Feeds) - NYSE Arca",
    },
    PublisherDetail {
        publisher_id: 80,
        dataset: "EQUS.ALL",
        venue: "LTSE",
        description: "Databento US Equities (All Feeds) - Long-Term Stock Exchange",
    },
    PublisherDetail {
        publisher_id: 81,
        dataset: "XNAS.BASIC",
        venue: "XNAS",
        description: "Nasdaq Basic - Nasdaq",
    },
    PublisherDetail {
        publisher_id: 82,
        dataset: "XNAS.BASIC",
        venue: "FINN",
        description: "Nasdaq Basic - FINRA/Nasdaq TRF Carteret",
    },
    PublisherDetail {
        publisher_id: 83,
        dataset: "XNAS.BASIC",
        venue: "FINC",
        description: "Nasdaq Basic - FINRA/Nasdaq TRF Chicago",
    },
    PublisherDetail {
        publisher_id: 84,
        dataset: "IFEU.IMPACT",
        venue: "XOFF",
        description: "ICE Europe - Off-Market Trades",
    },
    PublisherDetail {
        publisher_id: 85,
        dataset: "NDEX.IMPACT",
        venue: "XOFF",
        description: "ICE Endex - Off-Market Trades",
    },
    PublisherDetail {
        publisher_id: 86,
        dataset: "XNAS.NLS",
        venue: "XBOS",
        description: "Nasdaq NLS - Nasdaq Texas",
    },
    PublisherDetail {
        publisher_id: 87,
        dataset: "XNAS.NLS",
        venue: "XPSX",
        description: "Nasdaq NLS - Nasdaq PSX",
    },
    PublisherDetail {
        publisher_id: 88,
        dataset: "XNAS.BASIC",
        venue: "XBOS",
        description: "Nasdaq Basic - Nasdaq Texas",
    },
    PublisherDetail {
        publisher_id: 89,
        dataset: "XNAS.BASIC",
        venue: "XPSX",
        description: "Nasdaq Basic - Nasdaq PSX",
    },
    PublisherDetail {
        publisher_id: 90,
        dataset: "EQUS.SUMMARY",
        venue: "EQUS",
        description: "Databento Equities Summary",
    },
    PublisherDetail {
        publisher_id: 91,
        dataset: "XCIS.TRADESBBO",
        venue: "XCIS",
        description: "NYSE National Trades and BBO",
    },
    PublisherDetail {
        publisher_id: 92,
        dataset: "XNYS.TRADESBBO",
        venue: "XNYS",
        description: "NYSE Trades and BBO",
    },
    PublisherDetail {
        publisher_id: 93,
        dataset: "XNAS.BASIC",
        venue: "EQUS",
        description: "Nasdaq Basic - Consolidated",
    },
    PublisherDetail {
        publisher_id: 94,
        dataset: "EQUS.ALL",
        venue: "EQUS",
        description: "Databento US Equities (All Feeds) - Consolidated",
    },
    PublisherDetail {
        publisher_id: 95,
        dataset: "EQUS.MINI",
        venue: "EQUS",
        description: "Databento US Equities Mini",
    },
    PublisherDetail {
        publisher_id: 96,
        dataset: "XNYS.TRADES",
        venue: "EQUS",
        description: "NYSE Trades - Consolidated",
    },
    PublisherDetail {
        publisher_id: 97,
        dataset: "IFUS.IMPACT",
        venue: "IFUS",
        description: "ICE Futures US",
    },
    PublisherDetail {
        publisher_id: 98,
        dataset: "IFUS.IMPACT",
        venue: "XOFF",
        description: "ICE Futures US - Off-Market Trades",
    },
    PublisherDetail {
        publisher_id: 99,
        dataset: "IFLL.IMPACT",
        venue: "IFLL",
        description: "ICE Europe Financials",
    },
    PublisherDetail {
        publisher_id: 100,
        dataset: "IFLL.IMPACT",
        venue: "XOFF",
        description: "ICE Europe Financials - Off-Market Trades",
    },
    PublisherDetail {
        publisher_id: 101,
        dataset: "XEUR.EOBI",
        venue: "XEUR",
        description: "Eurex EOBI",
    },
    PublisherDetail {
        publisher_id: 102,
        dataset: "XEEE.EOBI",
        venue: "XEEE",
        description: "European Energy Exchange EOBI",
    },
    PublisherDetail {
        publisher_id: 103,
        dataset: "XEUR.EOBI",
        venue: "XOFF",
        description: "Eurex EOBI - Off-Market Trades",
    },
    PublisherDetail {
        publisher_id: 104,
        dataset: "XEEE.EOBI",
        venue: "XOFF",
        description: "European Energy Exchange EOBI - Off-Market Trades",
    },
    PublisherDetail {
        publisher_id: 105,
        dataset: "XCBF.PITCH",
        venue: "XCBF",
        description: "Cboe Futures Exchange (CFE)",
    },
    PublisherDetail {
        publisher_id: 106,
        dataset: "XCBF.PITCH",
        venue: "XOFF",
        description: "Cboe Futures Exchange (CFE) - Off-Market Trades",
    },
    PublisherDetail {
        publisher_id: 107,
        dataset: "OCEA.MEMOIR",
        venue: "OCEA",
        description: "Blue Ocean ATS MEMOIR",
    },
    PublisherDetail {
        publisher_id: 108,
        dataset: "OPRA.PILLAR",
        venue: "MXTO",
        description: "OPRA - MEMX MX2 Options",
    },
    PublisherDetail {
        publisher_id: 109,
        dataset: "OPRA.PILLAR",
        venue: "IEXO",
        description: "OPRA - IEX Options LLC",
    },
    PublisherDetail {
        publisher_id: 110,
        dataset: "MAIN.CGIF",
        venue: "MAIN",
        description: "Cboe Global Indices Feed",
    },
    PublisherDetail {
        publisher_id: 111,
        dataset: "EQUS.SIP",
        venue: "XASE",
        description: "US Equities SIP - NYSE American",
    },
    PublisherDetail {
        publisher_id: 112,
        dataset: "EQUS.SIP",
        venue: "XBOS",
        description: "US Equities SIP - Nasdaq Texas",
    },
    PublisherDetail {
        publisher_id: 113,
        dataset: "EQUS.SIP",
        venue: "XCIS",
        description: "US Equities SIP - NYSE National",
    },
    PublisherDetail {
        publisher_id: 114,
        dataset: "EQUS.SIP",
        venue: "TXSE",
        description: "US Equities SIP - Texas Stock Exchange",
    },
    PublisherDetail {
        publisher_id: 115,
        dataset: "EQUS.SIP",
        venue: "24EQ",
        description: "US Equities SIP - 24X National Exchange",
    },
    PublisherDetail {
        publisher_id: 116,
        dataset: "EQUS.SIP",
        venue: "EPRL",
        description: "US Equities SIP - MIAX Pearl",
    },
    PublisherDetail {
        publisher_id: 117,
        dataset: "EQUS.SIP",
        venue: "XISX",
        description: "US Equities SIP - Nasdaq ISE",
    },
    PublisherDetail {
        publisher_id: 118,
        dataset: "EQUS.SIP",
        venue: "EDGA",
        description: "US Equities SIP - Cboe EDGA",
    },
    PublisherDetail {
        publisher_id: 119,
        dataset: "EQUS.SIP",
        venue: "EDGX",
        description: "US Equities SIP - Cboe EDGX",
    },
    PublisherDetail {
        publisher_id: 120,
        dataset: "EQUS.SIP",
        venue: "LTSE",
        description: "US Equities SIP - Long-Term Stock Exchange",
    },
    PublisherDetail {
        publisher_id: 121,
        dataset: "EQUS.SIP",
        venue: "XCHI",
        description: "US Equities SIP - NYSE Texas",
    },
    PublisherDetail {
        publisher_id: 122,
        dataset: "EQUS.SIP",
        venue: "XNYS",
        description: "US Equities SIP - NYSE",
    },
    PublisherDetail {
        publisher_id: 123,
        dataset: "EQUS.SIP",
        venue: "ARCX",
        description: "US Equities SIP - NYSE Arca",
    },
    PublisherDetail {
        publisher_id: 124,
        dataset: "EQUS.SIP",
        venue: "XNAS",
        description: "US Equities SIP - Nasdaq",
    },
    PublisherDetail {
        publisher_id: 125,
        dataset: "EQUS.SIP",
        venue: "MEMX",
        description: "US Equities SIP - MEMX",
    },
    PublisherDetail {
        publisher_id: 126,
        dataset: "EQUS.SIP",
        venue: "IEXG",
        description: "US Equities SIP - IEX",
    },
    PublisherDetail {
        publisher_id: 127,
        dataset: "EQUS.SIP",
        venue: "XPSX",
        description: "US Equities SIP - Nasdaq PSX",
    },
    PublisherDetail {
        publisher_id: 128,
        dataset: "EQUS.SIP",
        venue: "BATY",
        description: "US Equities SIP - Cboe BYX",
    },
    PublisherDetail {
        publisher_id: 129,
        dataset: "EQUS.SIP",
        venue: "BATS",
        description: "US Equities SIP - Cboe BZX",
    },
    PublisherDetail {
        publisher_id: 130,
        dataset: "EQUS.SIP",
        venue: "FINN",
        description: "US Equities SIP - FINRA/Nasdaq TRF Carteret",
    },
    PublisherDetail {
        publisher_id: 131,
        dataset: "EQUS.SIP",
        venue: "FINY",
        description: "US Equities SIP - FINRA/NYSE TRF",
    },
    PublisherDetail {
        publisher_id: 132,
        dataset: "EQUS.SIP",
        venue: "FINC",
        description: "US Equities SIP - FINRA/Nasdaq TRF Chicago",
    },
    PublisherDetail {
        publisher_id: 133,
        dataset: "EQUS.SIP",
        venue: "XADF",
        description: "US Equities SIP - FINRA Alternative Display Facility",
    },
    PublisherDetail {
        publisher_id: 134,
        dataset: "EQUS.SIP",
        venue: "CTA",
        description: "US Equities SIP - CTA",
    },
    PublisherDetail {
        publisher_id: 135,
        dataset: "EQUS.SIP",
        venue: "UTP",
        description: "US Equities SIP - UTP",
    },
    PublisherDetail {
        publisher_id: 136,
        dataset: "MSCI.CGIF",
        venue: "MSCI",
        description: "CGIF - Morgan Stanley Capital International",
    },
    PublisherDetail {
        publisher_id: 137,
        dataset: "FTSE.CGIF",
        venue: "FTSE",
        description: "CGIF - FTSE Russell",
    },
    PublisherDetail {
        publisher_id: 138,
        dataset: "INAV.CGIF",
        venue: "INAV",
        description: "CGIF - Intraday Net Asset Values",
    },
    PublisherDetail {
        publisher_id: 139,
        dataset: "MSTAR.CGIF",
        venue: "MSTAR",
        description: "CGIF - Morning Star",
    },
    PublisherDetail {
        publisher_id: 140,
        dataset: "CCCY.CGIF",
        venue: "CCCY",
        description: "CGIF - Crypto Currency",
    },
    PublisherDetail {
        publisher_id: 141,
        dataset: "CGI.CGIF",
        venue: "CGI",
        description: "CGIF - CBOE Global Indices",
    },
    PublisherDetail {
        publisher_id: 142,
        dataset: "MAIN.CGIF",
        venue: "CDEF",
        description: "CGIF - Definitions",
    },
    PublisherDetail {
        publisher_id: 143,
        dataset: "XTKS.FLEX",
        venue: "XTKS",
        description: "JPX - Tokyo Stock Exchange",
    },
    PublisherDetail {
        publisher_id: 144,
        dataset: "XTKT.ITCH",
        venue: "XTKT",
        description: "JPX - Tokyo Commodity Exchange",
    },
    PublisherDetail {
        publisher_id: 145,
        dataset: "XOSE.ITCH",
        venue: "XOSE",
        description: "JPX - Osaka Exchange",
    },
    PublisherDetail {
        publisher_id: 146,
        dataset: "DBIX.CORE",
        venue: "MAIN",
        description: "CGIF - Main Feed",
    },
    PublisherDetail {
        publisher_id: 147,
        dataset: "DBIX.CORE",
        venue: "MSCI",
        description: "CGIF - Morgan Stanley Capital International",
    },
    PublisherDetail {
        publisher_id: 148,
        dataset: "DBIX.CORE",
        venue: "FTSE",
        description: "CGIF - FTSE Russell",
    },
    PublisherDetail {
        publisher_id: 149,
        dataset: "DBIX.CORE",
        venue: "INAV",
        description: "CGIF - Intraday Net Asset Values",
    },
    PublisherDetail {
        publisher_id: 150,
        dataset: "DBIX.CORE",
        venue: "MSTAR",
        description: "CGIF - Morning Star",
    },
    PublisherDetail {
        publisher_id: 151,
        dataset: "DBIX.CORE",
        venue: "CCCY",
        description: "CGIF - Crypto Currency",
    },
    PublisherDetail {
        publisher_id: 152,
        dataset: "DBIX.CORE",
        venue: "CGI",
        description: "CGIF - CBOE Global Indices",
    },
    PublisherDetail {
        publisher_id: 153,
        dataset: "DBIX.CORE",
        venue: "CDEF",
        description: "CGIF - Definitions",
    },
]
```

### Historical::MetadataListDatasets

List all validdatasetIDs on Databento.

Use this method to list the available dataset IDs (string identifiers), so you can use other methods which take thedatasetparameter.

Constants for dataset IDs are also available in<databento/constants.hpp>.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| date_range | databento::DateRange | The request range with an inclusive UTC start date and an optional exclusive UTC end date. Takes YYYY-MM-DD ISO 8601 date strings. If end is not specified, will return through the last date available. |

#### Returns

std::vector<std::string>

A list of dataset IDs.

```python
std::vector<std::string> MetadataListDatasets();
std::vector<std::string> MetadataListDatasets(
    const DateRange& date_range);
```

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
```

```python
#include <databento/historical.hpp>
#include <iostream>

using namespace databento;

auto client =
    Historical::Builder().SetKey("$YOUR_API_KEY").Build();
auto datasets = client.MetadataListDatasets();
for (const auto& dataset : datasets) {
  std::cout << dataset << '\n';
}
```

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
18
19
20
21
22
23
24
25
26
27
28
29
```

```python
ARCX.PILLAR
BATS.PITCH
BATY.PITCH
DBEQ.BASIC
EDGA.PITCH
EDGX.PITCH
EPRL.DOM
EQUS.MINI
EQUS.SUMMARY
GLBX.MDP3
IEXG.TOPS
IFEU.IMPACT
IFLL.IMPACT
IFUS.IMPACT
MEMX.MEMOIR
NDEX.IMPACT
OCEA.MEMOIR
OPRA.PILLAR
XASE.PILLAR
XBOS.ITCH
XCBF.PITCH
XCHI.PILLAR
XCIS.TRADESBBO
XEEE.EOBI
XEUR.EOBI
XNAS.BASIC
XNAS.ITCH
XNYS.PILLAR
XPSX.ITCH
```

### /metadata.list_datasets

List all availabledatasetIDs on Databento.

Use this method to list the available dataset IDs (string identifiers), so you can use other endpoints which take thedatasetparameter.

#### Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| start_date | optional | The inclusive UTC start date of the request range as an ISO 8601 date string. Defaults to the first date available. |
| end_date | optional | The exclusive UTC end date of the request range as an ISO 8601 date string. Defaults to the last date available. |

#### Returns

A list of available dataset IDs.

```python
GET https://hist.databento.com/v0/metadata.list_datasets
```

```python
1
2
```

```python
curl -G 'https://hist.databento.com/v0/metadata.list_datasets' \
 -u $YOUR_API_KEY:
```

```python
1
2
3
4
```

```python
[
  "GLBX.MDP3",
  "XNAS.ITCH"
]
```

### Historical.metadata.list_datasets

List all validdatasetIDs on Databento.

Use this method to list the available dataset IDs (string identifiers), so you can use other methods which take thedatasetparameter.

#### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| start_date | date or str | optional | The inclusive UTC start date of the request range as a Python date or ISO 8601 date string. If None then first date available. |
| end_date | date or str | optional | The exclusive UTC end date of the request range as a Python date or ISO 8601 date string. If None then last date available. |

#### Returns

A list of available dataset IDs.

```python
Historical.metadata.list_datasets(
    start_date: date | str | None = None,
    end_date: date | str | None = None,
) -> list[str]
```

```python
1
2
3
4
5
6
```

```python
import databento as db

client = db.Historical("$YOUR_API_KEY")

datasets = client.metadata.list_datasets()
print(datasets)
```

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
18
19
20
21
22
23
24
25
26
27
28
29
30
31
```

```python
[
    "ARCX.PILLAR",
    "BATS.PITCH",
    "BATY.PITCH",
    "DBEQ.BASIC",
    "EDGA.PITCH",
    "EDGX.PITCH",
    "EPRL.DOM",
    "EQUS.MINI",
    "EQUS.SUMMARY",
    "GLBX.MDP3",
    "IEXG.TOPS",
    "IFEU.IMPACT",
    "IFLL.IMPACT",
    "IFUS.IMPACT",
    "MEMX.MEMOIR",
    "NDEX.IMPACT",
    "OCEA.MEMOIR",
    "OPRA.PILLAR",
    "XASE.PILLAR",
    "XBOS.ITCH",
    "XCBF.PITCH",
    "XCHI.PILLAR",
    "XCIS.TRADESBBO",
    "XEEE.EOBI",
    "XEUR.EOBI",
    "XNAS.BASIC",
    "XNAS.ITCH",
    "XNYS.PILLAR",
    "XPSX.ITCH"
]
```

### HistoricalClient::metadata::list_datasets

List all availabledatasetIDs on Databento.

Use this method to list the dataset IDs (string identifiers) of all available datasets, so you can use other methods which take thedatasetparameter.

Constants for dataset IDs are also available indatabento::dbn::datasets.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| date_range | Option<DateRange> | The UTC date request range with an inclusive start date and an exclusive end date. If None then all available dates. |

#### Returns

Vec<String>

A list of dataset IDs.

```python
pub async fn list_datasets(
    &mut self,
    date_range: Option<DateRange>,
) -> databento::Result<Vec<String>>;
```

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
```

```python
use databento::HistoricalClient;
use time::{Duration, macros::date};

let mut client =
    HistoricalClient::builder().key("$YOUR_API_KEY")?.build()?;
let dataset_codes = client
    .metadata()
    .list_datasets(Some(date!(2024 - 01 - 28).into()))
    .await?;
println!("{dataset_codes:#?}");
```

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
18
19
20
21
22
23
24
25
26
27
```

```python
[
    "ARCX.PILLAR",
    "BATS.PITCH",
    "BATY.PITCH",
    "DBEQ.BASIC",
    "EDGA.PITCH",
    "EDGX.PITCH",
    "EPRL.DOM",
    "EQUS.MINI",
    "GLBX.MDP3",
    "IEXG.TOPS",
    "IFEU.IMPACT",
    "IFLL.IMPACT",
    "IFUS.IMPACT",
    "MEMX.MEMOIR",
    "NDEX.IMPACT",
    "OPRA.PILLAR",
    "XASE.PILLAR",
    "XBOS.ITCH",
    "XCBF.PITCH",
    "XCHI.PILLAR",
    "XCIS.TRADESBBO",
    "XEEE.EOBI",
    "XNAS.ITCH",
    "XNYS.PILLAR",
    "XPSX.ITCH",
]
```

### Historical::MetadataListSchemas

List all available schemas for a dataset.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| dataset | std::string | The dataset code (string identifier). Must be one of the values from MetadataListDatasets . Constants are provided in the databento::dataset namespace in <databento/constants.hpp> . |

#### Returns

std::vector<databento::Schema>

A list of available data schemas.

```python
std::vector<Schema> MetadataListSchemas(
    const std::string& dataset);
```

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
```

```python
#include <databento/constants.hpp>  // kGlbxMdp3
#include <databento/historical.hpp>
#include <iostream>

using namespace databento;

auto client =
    Historical::Builder().SetKey("$YOUR_API_KEY").Build();
auto schemas = client.MetadataListSchemas(dataset::kGlbxMdp3);
for (const auto& schema : schemas) {
  std::cout << schema << '\n';
}
```

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
```

```python
mbo
mbp-1
mbp-10
tbbo
trades
bbo-1s
bbo-1m
ohlcv-1s
ohlcv-1m
ohlcv-1h
ohlcv-1d
definition
statistics
status
```

### /metadata.list_schemas

List all available schemas for a dataset.

#### Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| dataset | required | The dataset code (string identifier). Must be one of the values from list_datasets . |

#### Returns

A list of available data schemas.

```python
GET https://hist.databento.com/v0/metadata.list_schemas
```

```python
1
2
3
```

```python
curl -G 'https://hist.databento.com/v0/metadata.list_schemas' \
 -u $YOUR_API_KEY: \
 -d dataset=GLBX.MDP3 \
```

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
```

```python
[
  "mbo",
  "mbp-1",
  "mbp-10",
  "tbbo",
  "trades",
  "ohlcv-1s",
  "ohlcv-1m",
  "ohlcv-1h",
  "ohlcv-1d",
  "definition",
  "statistics",
  "status"
]
```

### Historical.metadata.list_schemas

List all available schemas for a dataset.

#### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| dataset | Dataset or str | required | The dataset code (string identifier). Must be one of the values from list_datasets . |

#### Returns

A list of available data schemas.

```python
Historical.metadata.list_schemas(
    dataset: Dataset | str,
) -> list[str]
```

```python
1
2
3
4
5
6
```

```python
import databento as db

client = db.Historical("$YOUR_API_KEY")

schemas = client.metadata.list_schemas(dataset="GLBX.MDP3")
print(schemas)
```

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
```

```python
[
    "mbo",
    "mbp-1",
    "mbp-10",
    "tbbo",
    "trades",
    "bbo-1s",
    "bbo-1m",
    "ohlcv-1s",
    "ohlcv-1m",
    "ohlcv-1h",
    "ohlcv-1d",
    "definition",
    "statistics",
    "status"
]
```

### HistoricalClient::metadata::list_schemas

List all available schemas for a dataset.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| dataset | impl AsRef<str> | The dataset code (string identifier). Must be one of the values from list_datasets . |

#### Returns

Vec<Schema>

A list of available data schemas for the dataset.

```python
pub async fn list_schemas(
    &mut self,
    dataset: &str,
) -> databento::Result<Vec<Schema>>;
```

```python
1
2
3
4
5
6
7
```

```python
use databento::{HistoricalClient, dbn::Dataset};

let mut client =
    HistoricalClient::builder().key("$YOUR_API_KEY")?.build()?;
let schemas =
    client.metadata().list_schemas(Dataset::XnasItch).await?;
println!("{schemas:#?}");
```

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
[
    Mbo,
    Mbp1,
    Mbp10,
    Bbo1S,
    Bbo1M,
    Tbbo,
    Trades,
    Ohlcv1S,
    Ohlcv1M,
    Ohlcv1H,
    Ohlcv1D,
    Definition,
    Statistics,
    Status,
    Imbalance,
]
```

### Historical::MetadataListFields

List all fields for a particular schema and encoding.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| schema | databento::Schema | The data record schema . Must be one of the values from MetadataListSchemas . |
| encoding | databento::Encoding | The data encoding . Encoding::Dbn is recommended. |
| dataset | std::string | The optional dataset used to determine which fields are relevant. If omitted, fields for the latest DBN encoding version are returned, which may differ from a specific dataset's schema. |

#### Returns

std::vector<FieldDetail>

A list of field details objects, whereFieldDetailis:

| Field | Type | Description |
| --- | --- | --- |
| name | std::string | The name of the field. |
| type | std::string | The type of the field. |

```python
std::vector<FieldDetail> MetadataListFields(Encoding encoding,
                                            Schema schema);
std::vector<FieldDetail> MetadataListFields(Encoding encoding,
                                            Schema schema,
                                            const std::string& dataset);
```

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
```

```python
#include <databento/constants.hpp>  // kGlbxMdp3
#include <databento/historical.hpp>
#include <iostream>

using namespace databento;

auto client =
    Historical::Builder().SetKey("$YOUR_API_KEY").Build();
auto fields =
    client.MetadataListFields(Encoding::Dbn, Schema::Trades);
for (const auto& field_detail : fields) {
  std::cout << field_detail << '\n';
}
```

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
```

```python
FieldDetail { name = "length", type = "uint8_t" }
FieldDetail { name = "rtype", type = "uint8_t" }
FieldDetail { name = "publisher_id", type = "uint16_t" }
FieldDetail { name = "instrument_id", type = "uint32_t" }
FieldDetail { name = "ts_event", type = "uint64_t" }
FieldDetail { name = "price", type = "int64_t" }
FieldDetail { name = "size", type = "uint32_t" }
FieldDetail { name = "action", type = "char" }
FieldDetail { name = "side", type = "char" }
FieldDetail { name = "flags", type = "uint8_t" }
FieldDetail { name = "depth", type = "uint8_t" }
FieldDetail { name = "ts_recv", type = "uint64_t" }
FieldDetail { name = "ts_in_delta", type = "int32_t" }
FieldDetail { name = "sequence", type = "uint32_t" }
```

### /metadata.list_fields

List all fields for a particular schema and encoding.

#### Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| schema | required | The data record schema . Must be one of the values from list_schemas . |
| encoding | required | The data encoding . Must be one of 'dbn', 'csv', or 'json'. 'dbn' is recommended. |
| dataset | optional | The dataset used to determine which fields are relevant. If omitted, the fields for the latest DBN encoding version are returned, which may differ from a specific dataset's schema. |

#### Returns

A list of field details objects.

| Field | Type | Description |
| --- | --- | --- |
| name | string | The name of the field. |
| type | string | The type of the field. |

```python
GET https://hist.databento.com/v0/metadata.list_fields
```

```python
1
2
3
4
```

```python
curl -G 'https://hist.databento.com/v0/metadata.list_fields' \
 -u $YOUR_API_KEY: \
 -d schema=trades \
 -d encoding=dbn
```

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
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
```

```python
[
  {
    "name": "length",
    "type": "uint8_t"
  },
  {
    "name": "rtype",
    "type": "uint8_t"
  },
  {
    "name": "publisher_id",
    "type": "uint16_t"
  },
  {
    "name": "instrument_id",
    "type": "uint32_t"
  },
  {
    "name": "ts_event",
    "type": "uint64_t"
  },
  {
    "name": "price",
    "type": "int64_t"
  },
  {
    "name": "size",
    "type": "uint32_t"
  },
  {
    "name": "action",
    "type": "char"
  },
  {
    "name": "side",
    "type": "char"
  },
  {
    "name": "flags",
    "type": "uint8_t"
  },
  {
    "name": "depth",
    "type": "uint8_t"
  },
  {
    "name": "ts_recv",
    "type": "uint64_t"
  },
  {
    "name": "ts_in_delta",
    "type": "int32_t"
  },
  {
    "name": "sequence",
    "type": "uint32_t"
  }
]
```

### Historical.metadata.list_fields

List all fields for a particular schema and encoding.

#### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| schema | Schema or str | required | The data record schema . Must be one of the values from list_schemas . |
| encoding | Encoding or str | required | The data encoding . Must be one of 'dbn', 'csv', or 'json'. 'dbn' is recommended. |
| dataset | Dataset or str | optional | The dataset used to determine which fields are relevant. If None then the fields for the latest DBN encoding version are returned, which may differ from a specific dataset's schema. |

#### Returns

list[dict[str, str]]

A list of field details objects.

| Field | Type | Description |
| --- | --- | --- |
| name | str | The field name. |
| type | str | The field data type. |

```python
Historical.metadata.list_fields(
    schema: Schema | str,
    encoding: Encoding | str,
    dataset: Dataset | str | None = None,
) -> list[dict[str, str]]
```

```python
1
2
3
4
5
6
```

```python
import databento as db

client = db.Historical("$YOUR_API_KEY")

fields = client.metadata.list_fields(schema="trades", encoding="dbn")
print(fields)
```

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
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
```

```python
[
    {
        "name": "length",
        "type": "uint8_t"
    },
    {
        "name": "rtype",
        "type": "uint8_t"
    },
    {
        "name": "publisher_id",
        "type": "uint16_t"
    },
    {
        "name": "instrument_id",
        "type": "uint32_t"
    },
    {
        "name": "ts_event",
        "type": "uint64_t"
    },
    {
        "name": "price",
        "type": "int64_t"
    },
    {
        "name": "size",
        "type": "uint32_t"
    },
    {
        "name": "action",
        "type": "char"
    },
    {
        "name": "side",
        "type": "char"
    },
    {
        "name": "flags",
        "type": "uint8_t"
    },
    {
        "name": "depth",
        "type": "uint8_t"
    },
    {
        "name": "ts_recv",
        "type": "uint64_t"
    },
    {
        "name": "ts_in_delta",
        "type": "int32_t"
    },
    {
        "name": "sequence",
        "type": "uint32_t"
    }
]
```

### HistoricalClient::metadata::list_fields

List all fields for a schema and encoding.

#### Parameters

| Field | Type | Description |
| --- | --- | --- |
| params | ListFieldsParams | See ListFieldsParams for details. |

#### Returns

Vec<FieldDetail>

A list of field details objects, whereFieldDetailis:

| Field | Type | Description |
| --- | --- | --- |
| name | String | The name of the field. |
| type | String | The type of the field. |

```python
pub async fn list_fields(
    &mut self,
    params: &ListFieldsParams,
) -> databento::Result<Vec<FieldDetail>>;
```

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
18
```

```python
use databento::{
    HistoricalClient,
    dbn::{Encoding, Schema},
    historical::metadata::ListFieldsParams,
};

let mut client =
    HistoricalClient::builder().key("$YOUR_API_KEY")?.build()?;
let fields = client
    .metadata()
    .list_fields(
        &ListFieldsParams::builder()
            .schema(Schema::Trades)
            .encoding(Encoding::Dbn)
            .build(),
    )
    .await?;
println!("{fields:#?}");
```

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
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
```

```python
[
    FieldDetail {
        name: "length",
        type_name: "uint8_t",
    },
    FieldDetail {
        name: "rtype",
        type_name: "uint8_t",
    },
    FieldDetail {
        name: "publisher_id",
        type_name: "uint16_t",
    },
    FieldDetail {
        name: "instrument_id",
        type_name: "uint32_t",
    },
    FieldDetail {
        name: "ts_event",
        type_name: "uint64_t",
    },
    FieldDetail {
        name: "price",
        type_name: "int64_t",
    },
    FieldDetail {
        name: "size",
        type_name: "uint32_t",
    },
    FieldDetail {
        name: "action",
        type_name: "char",
    },
    FieldDetail {
        name: "side",
        type_name: "char",
    },
    FieldDetail {
        name: "flags",
        type_name: "uint8_t",
    },
    FieldDetail {
        name: "depth",
        type_name: "uint8_t",
    },
    FieldDetail {
        name: "ts_recv",
        type_name: "uint64_t",
    },
    FieldDetail {
        name: "ts_in_delta",
        type_name: "int32_t",
    },
    FieldDetail {
        name: "sequence",
        type_name: "uint32_t",
    },
]
```

### Historical::MetadataListUnitPrices

List unit prices for each data schema in US dollars per gigabyte.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| dataset | std::string | The dataset code (string identifier). Must be one of the values from MetadataListDatasets . Constants are provided in the databento::dataset namespace in <databento/constants.hpp> . |

#### Returns

std::vector<UnitPricesForMode>

A list of objects with the unit prices for a feed mode, whereUnitPricesForModeis:

| Field | Type | Description |
| --- | --- | --- |
| mode | databento::FeedMode | The feed mode. |
| unit_prices | std::map<Schema, double> | The map of unit prices in US dollars by schema. |

```python
std::vector<UnitPricesForMode> MetadataListUnitPrices(
    const std::string& dataset);
```

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
#include <databento/historical.hpp>
#include <iostream>

using namespace databento;

auto client =
    Historical::Builder().SetKey("$YOUR_API_KEY").Build();
std::vector<UnitPricesForMode> unit_prices =
    client.MetadataListUnitPrices("OPRA.PILLAR");
for (const auto& unit_prices_for_mode : unit_prices) {
  std::cout << "- " << unit_prices_for_mode.mode << '\n';
  for (const auto& schema_and_price :
       unit_prices_for_mode.unit_prices) {
    std::cout << "  " << schema_and_price.first << ": "
              << schema_and_price.second << '\n';
  }
}
```

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
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
```

```python
- historical
  trades: 280
  ohlcv-1s: 280
  ohlcv-1m: 280
  ohlcv-1h: 600
  ohlcv-1d: 600
  definition: 5
  statistics: 11
  status: 5
  cmbp-1: 0.16
  cbbo-1s: 2
  cbbo-1m: 2
  tcbbo: 210
- historical-streaming
  trades: 280
  ohlcv-1s: 280
  ohlcv-1m: 280
  ohlcv-1h: 600
  ohlcv-1d: 600
  definition: 5
  statistics: 11
  status: 5
  cmbp-1: 0.16
  cbbo-1s: 2
  cbbo-1m: 2
  tcbbo: 210
- live
  trades: 336
  ohlcv-1s: 336
  ohlcv-1m: 336
  ohlcv-1h: 720
  ohlcv-1d: 720
  definition: 6
  statistics: 13.2
  status: 6
  cmbp-1: 0.2
  cbbo-1s: 2.4
  cbbo-1m: 2.4
  tcbbo: 252
```

### /metadata.list_unit_prices

List unit prices for each data schema in dollars per gigabyte.

#### Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| dataset | required | The dataset code (string identifier). Must be one of the values from list_datasets . |

#### Returns

A list of objects with the unit prices for a feed mode.

| Field | Type | Description |
| --- | --- | --- |
| mode | string | The feed mode. |
| unit_prices | object | The map of unit prices in US dollars by schema. |

```python
GET https://hist.databento.com/v0/metadata.list_unit_prices
```

```python
1
2
3
```

```python
curl -G 'https://hist.databento.com/v0/metadata.list_unit_prices' \
 -u $YOUR_API_KEY: \
 -d dataset=OPRA.PILLAR
```

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
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
```

```python
[
  {
    "mode": "historical",
    "unit_prices": {
      "mbp-1": 0.04,
      "ohlcv-1s": 280.0,
      "ohlcv-1m": 280.0,
      "ohlcv-1h": 600.0,
      "ohlcv-1d": 600.0,
      "tbbo": 210.0,
      "trades": 280.0,
      "statistics": 11.0,
      "definition": 5.0
    }
  },
  {
    "mode": "historical-streaming",
    "unit_prices": {
      "mbp-1": 0.04,
      "ohlcv-1s": 280.0,
      "ohlcv-1m": 280.0,
      "ohlcv-1h": 600.0,
      "ohlcv-1d": 600.0,
      "tbbo": 210.0,
      "trades": 280.0,
      "statistics": 11.0,
      "definition": 5.0
    }
  },
  {
    "mode": "live",
    "unit_prices": {
      "mbp-1": 0.05,
      "ohlcv-1s": 336.0,
      "ohlcv-1m": 336.0,
      "ohlcv-1h": 720.0,
      "ohlcv-1d": 720.0,
      "tbbo": 252.0,
      "trades": 336.0,
      "statistics": 13.2,
      "definition": 6.0
    }
  }
]
```

### Historical.metadata.list_unit_prices

List unit prices for each feed mode and data schema in US dollars per gigabyte.

#### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| dataset | Dataset or str | required | The dataset code (string identifier). Must be one of the values from list_datasets . |

#### Returns

list[dict[str, Any]]

A list of maps of feed mode to schema to unit price.

| Field | Type | Description |
| --- | --- | --- |
| mode | str | The feed mode. Will be one of "historical", "historical-streaming", or "live". |
| unit_prices | dict[str \| float] | A mapping of schemas to unit prices in US dollars per gigabyte. |

```python
Historical.metadata.list_unit_prices(
    dataset: Dataset | str,
) -> list[dict[str, Any]]
```

```python
1
2
3
4
5
6
```

```python
import databento as db

client = db.Historical("$YOUR_API_KEY")

unit_prices = client.metadata.list_unit_prices(dataset="OPRA.PILLAR")
print(unit_prices)
```

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
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
```

```python
[
    {
        "mode": "historical",
        "unit_prices": {
            "cmbp-1": 0.16,
            "cbbo-1s": 2.0,
            "cbbo-1m": 2.0,
            "tcbbo": 210.0,
            "trades": 280.0,
            "ohlcv-1s": 280.0,
            "ohlcv-1m": 280.0,
            "ohlcv-1h": 600.0,
            "ohlcv-1d": 600.0,
            "statistics": 11.0,
            "status": 5.0,
            "definition": 5.0
        }
    },
    {
        "mode": "historical-streaming",
        "unit_prices": {
            "cmbp-1": 0.16,
            "cbbo-1s": 2.0,
            "cbbo-1m": 2.0,
            "tcbbo": 210.0,
            "trades": 280.0,
            "ohlcv-1s": 280.0,
            "ohlcv-1m": 280.0,
            "ohlcv-1h": 600.0,
            "ohlcv-1d": 600.0,
            "statistics": 11.0,
            "status": 5.0,
            "definition": 5.0
        }
    },
    {
        "mode": "live",
        "unit_prices": {
            "cmbp-1": 0.2,
            "cbbo-1s": 2.4,
            "cbbo-1m": 2.4,
            "tcbbo": 252.0,
            "trades": 336.0,
            "ohlcv-1s": 336.0,
            "ohlcv-1m": 336.0,
            "ohlcv-1h": 720.0,
            "ohlcv-1d": 720.0,
            "statistics": 13.2,
            "status": 6.0,
            "definition": 6.0
        }
    }
]
```

### HistoricalClient::metadata::list_unit_prices

List unit prices for each data schema in US dollars per gigabyte.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| dataset | impl AsRef<str> | The dataset code (string identifier). Must be one of the values from list_datasets . |

#### Returns

Vec<UnitPricesForMode>

A list of objects with the unit prices for a feed mode, whereUnitPricesForModeis:

| Field | Type | Description |
| --- | --- | --- |
| mode | FeedMode | The feed mode. |
| unit_prices | HashMap<Schema, double> | The map of unit prices in US dollars by schema. |

```python
pub async fn list_unit_prices(
    &mut self,
    dataset: &str,
) -> databento::Result<Vec<UnitPricesForMode>>;
```

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
```

```python
use databento::{
    HistoricalClient, dbn::Dataset,
    historical::metadata::FeedMode,
};

let mut client =
    HistoricalClient::builder().key("$YOUR_API_KEY")?.build()?;
let unit_prices = client
    .metadata()
    .list_unit_prices(Dataset::OpraPillar)
    .await?;
println!("{unit_prices:#?}");
```

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
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
```

```python
[
    UnitPricesForMode {
        mode: Historical,
        unit_prices: {
            Cmbp1: 0.16,
            Statistics: 11.0,
            Ohlcv1M: 280.0,
            Ohlcv1S: 280.0,
            Trades: 280.0,
            Tcbbo: 210.0,
            Ohlcv1H: 600.0,
            Definition: 5.0,
            Cbbo1S: 2.0,
            Ohlcv1D: 600.0,
            Status: 5.0,
            Cbbo1M: 2.0,
        },
    },
    UnitPricesForMode {
        mode: HistoricalStreaming,
        unit_prices: {
            Ohlcv1M: 280.0,
            Cmbp1: 0.16,
            Ohlcv1H: 600.0,
            Statistics: 11.0,
            Status: 5.0,
            Trades: 280.0,
            Cbbo1S: 2.0,
            Definition: 5.0,
            Ohlcv1S: 280.0,
            Cbbo1M: 2.0,
            Tcbbo: 210.0,
            Ohlcv1D: 600.0,
        },
    },
    UnitPricesForMode {
        mode: Live,
        unit_prices: {
            Cbbo1M: 2.4,
            Status: 6.0,
            Definition: 6.0,
            Cmbp1: 0.2,
            Ohlcv1D: 720.0,
            Ohlcv1H: 720.0,
            Tcbbo: 252.0,
            Statistics: 13.2,
            Ohlcv1S: 336.0,
            Trades: 336.0,
            Ohlcv1M: 336.0,
            Cbbo1S: 2.4,
        },
    },
]
```

### Historical::MetadataGetDatasetCondition

Get thedatasetcondition from Databento.

Use this method to discover data availability and quality.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| dataset | std::string | The dataset code (string identifier). Must be one of the values from MetadataListDatasets . Constants are provided in the databento::dataset namespace in <databento/constants.hpp> . |
| date_range | databento::DateRange | The request range with an inclusive UTC start date and an optional inclusive UTC end date. Takes YYYY-MM-DD ISO 8601 date strings. If end is not specified, will return through the last date available. |

#### Returns

std::vector<DatasetConditionDetail>

A list of conditions per date, whereDatasetConditionDetailis:

| Field | Type | Description |
| --- | --- | --- |
| date | std::string | The day of the described data, as an ISO 8601 date string. |
| condition | DatasetCondition | The condition code describing the quality and availability of the data on the given day. Possible values are listed below. |
| last_modified_date | std::optional<std::string> | The date when any schema in the dataset on the given day was last generated or modified as an ISO 8601 date string. Will be null when condition is Missing . |

Possible values for condition:

```python
std::vector<DatasetConditionDetail> MetadataGetDatasetCondition(
    const std::string& dataset);
std::vector<DatasetConditionDetail> MetadataGetDatasetCondition(
    const std::string& dataset, const DateRange& date_range);
```

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
```

```python
#include <databento/constants.hpp>  // kGlbxMdp3
#include <databento/historical.hpp>
#include <iostream>

using namespace databento;

auto client =
    Historical::Builder().SetKey("$YOUR_API_KEY").Build();
auto conditions = client.MetadataGetDatasetCondition(
    dataset::kGlbxMdp3, {"2019-06-06", "2019-06-10"});
for (const DatasetConditionDetail& condition : conditions) {
  std::cout << condition << '\n';
}
```

```python
1
2
3
4
```

```python
DatasetConditionDetail { date = "2019-06-06", condition = available, last_modified_date = "2024-05-13" }
DatasetConditionDetail { date = "2019-06-07", condition = available, last_modified_date = "2024-05-13" }
DatasetConditionDetail { date = "2019-06-09", condition = available, last_modified_date = "2024-05-13" }
DatasetConditionDetail { date = "2019-06-10", condition = available, last_modified_date = "2024-05-13" }
```

### /metadata.get_dataset_condition

Get thedatasetcondition from Databento.

Use this method to discover data availability and quality.

#### Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| dataset | required | The dataset code (string identifier). Must be one of the values from list_datasets . |
| start_date | optional | The inclusive UTC start date of the request range as an ISO 8601 date string. Defaults to the first date available. |
| end_date | optional | The inclusive UTC end date of the request range as an ISO 8601 date string. Defaults to the last date available. |

#### Returns

A list of conditions per date.

| Field | Type | Description |
| --- | --- | --- |
| date | string | The day of the described data, as an ISO 8601 date string. |
| condition | string | The condition code describing the quality and availability of the data on the given day. Possible values are listed below. |
| last_modified_date | string | The date when any schema in the dataset on the given day was last generated or modified, as an ISO 8601 date string. |

Possible values for condition:

```python
GET https://hist.databento.com/v0/metadata.get_dataset_condition
```

```python
1
2
3
4
5
```

```python
curl -G 'https://hist.databento.com/v0/metadata.get_dataset_condition' \
 -u $YOUR_API_KEY: \
 -d dataset=GLBX.MDP3 \
 -d start_date='2022-06-06' \
 -d end_date='2022-06-10'
```

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
18
19
20
21
22
```

```python
[
  {
    "date": "2022-06-06",
    "condition": "available",
    "last_modified_date": "2023-03-01"
  },
  {
    "date": "2022-06-07",
    "condition": "available",
    "last_modified_date": "2023-03-01"
  },
  {
    "date": "2022-06-08",
    "condition": "available",
    "last_modified_date": "2023-03-01"
  },
  {
    "date": "2022-06-09",
    "condition": "available",
    "last_modified_date": "2023-03-01"
  }
]
```

### Historical.metadata.get_dataset_condition

Get thedatasetcondition from Databento.

Use this method to discover data availability and quality.

#### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| dataset | Dataset or str | required | The dataset code (string identifier). Must be one of the values from list_datasets . |
| start_date | date or str | optional | The inclusive UTC start date of the request range as a Python date or ISO 8601 date string. If None then first date available. |
| end_date | date or str | optional | The inclusive UTC end date of the request range as a Python date or ISO 8601 date string. If None then last date available. |

#### Returns

list[dict[str, str | None]]

A list of conditions per date.

| Field | Type | Description |
| --- | --- | --- |
| date | str | The day of the described data, as an ISO 8601 date string. |
| condition | str | The condition code describing the quality and availability of the data on the given day. Possible values are listed below. |
| last_modified_date | str or None | The date when any schema in the dataset on the given day was last generated or modified, as an ISO 8601 date string. Will be None when condition is 'missing'. |

Possible values for condition:

```python
Historical.metadata.get_dataset_condition(
    dataset: Dataset | str,
    start_date: date | str | None = None,
    end_date: date | str | None = None,
) -> list[dict[str, str | None]]
```

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
```

```python
import databento as db

client = db.Historical("$YOUR_API_KEY")

conditions = client.metadata.get_dataset_condition(
    dataset="GLBX.MDP3",
    start_date="2022-06-06",
    end_date="2022-06-10",
)
print(conditions)
```

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
18
19
20
21
22
23
24
25
26
27
```

```python
[
    {
        "date": "2022-06-06",
        "condition": "available",
        "last_modified_date": "2024-05-18"
    },
    {
        "date": "2022-06-07",
        "condition": "available",
        "last_modified_date": "2024-05-21"
    },
    {
        "date": "2022-06-08",
        "condition": "available",
        "last_modified_date": "2024-05-21"
    },
    {
        "date": "2022-06-09",
        "condition": "available",
        "last_modified_date": "2024-05-21"
    },
    {
        "date": "2022-06-10",
        "condition": "available",
        "last_modified_date": "2024-05-22"
    }
]
```

### HistoricalClient::metadata::get_dataset_condition

Get thedatasetcondition from Databento.

Use this method to discover data availability and quality.

#### Parameters

| Field | Type | Description |
| --- | --- | --- |
| params | GetDatasetConditionParams | See GetDatasetConditionParams for details. |

#### Returns

Vec<DatasetConditionDetail>

A list of conditions per date, whereDatasetConditionDetailis:

| Field | Type | Description |
| --- | --- | --- |
| date | time::Date | The UTC date of the described data. |
| condition | DatasetCondition | The condition code describing the quality and availability of the data on the given day. Possible values are listed below. |
| last_modified_date | Option<time::Date> | The UTC date when any schema in the dataset on the given day was last generated or modified. Will be None when condition is Missing . |

Possible values for condition:

```python
pub async fn get_dataset_condition(
    &mut self,
    params: &GetDatasetConditionParams,
) -> databento::Result<Vec<DatasetConditionDetail>>;
```

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
18
19
20
```

```python
use databento::{
    HistoricalClient,
    historical::metadata::GetDatasetConditionParams,
};
use time::macros::date;

let mut client =
    HistoricalClient::builder().key("$YOUR_API_KEY")?.build()?;
let conditions = client
    .metadata()
    .get_dataset_condition(
        &GetDatasetConditionParams::builder()
            .dataset("GLBX.MDP3")
            .date_range(
                date!(2019 - 06 - 06)..date!(2019 - 06 - 10),
            )
            .build(),
    )
    .await?;
println!("{conditions:#?}");
```

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
18
19
20
21
22
23
24
25
26
27
28
29
30
```

```python
[
    DatasetConditionDetail {
        date: 2019-06-06,
        condition: Available,
        last_modified_date: Some(
            2024-05-13,
        ),
    },
    DatasetConditionDetail {
        date: 2019-06-07,
        condition: Available,
        last_modified_date: Some(
            2024-05-13,
        ),
    },
    DatasetConditionDetail {
        date: 2019-06-09,
        condition: Available,
        last_modified_date: Some(
            2024-05-13,
        ),
    },
    DatasetConditionDetail {
        date: 2019-06-10,
        condition: Available,
        last_modified_date: Some(
            2024-05-13,
        ),
    },
]
```

### Historical::MetadataGetDatasetRange

Get the available range for thedatasetgiven the user's entitlements.

Use this method to discover data availability. Thestartandendvalues in the response can be used withTimeseriesGetRangeandBatchSubmitJobendpoints.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| dataset | std::string | The dataset code (string identifier). Must be one of the values from MetadataListDatasets . |

#### Returns

DatasetRange

The available range for the dataset.

| Field | Type | Description |
| --- | --- | --- |
| start | std::string | The ISO 8601 start timestamp of the available range. |
| end | std::string | The ISO 8601 end timestamp of the available range (exclusive). |
| range_by_schema | std::unordered_map<Schema, DateTimeRange<std::string>> | A mapping of schema names to per-schema start and end timestamps. |

```python
DatasetRange MetadataGetDatasetRange(const std::string& dataset);
```

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
```

```python
#include <databento/historical.hpp>
#include <iostream>

using namespace databento;

auto client =
    Historical::Builder().SetKey("$YOUR_API_KEY").Build();
auto available_range =
    client.MetadataGetDatasetRange("XNAS.ITCH");
std::cout << available_range << '\n';
```

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
18
19
20
21
```

```python
DatasetRange {
    start = "2018-05-01T00:00:00.000000000Z",
    end = "2026-03-13T23:10:00.000000000Z",
    range_by_schema = {
        mbo: DateTimeRange { start = "2018-05-01T00:00:00.000000000Z", end = "2026-03-13T23:10:00.000000000Z" },
        mbp-1: DateTimeRange { start = "2018-05-01T00:00:00.000000000Z", end = "2026-03-13T23:10:00.000000000Z" },
        mbp-10: DateTimeRange { start = "2018-05-01T00:00:00.000000000Z", end = "2026-03-13T23:10:00.000000000Z" },
        tbbo: DateTimeRange { start = "2018-05-01T00:00:00.000000000Z", end = "2026-03-13T23:10:00.000000000Z" },
        trades: DateTimeRange { start = "2018-05-01T00:00:00.000000000Z", end = "2026-03-13T23:10:00.000000000Z" },
        ohlcv-1s: DateTimeRange { start = "2018-05-01T00:00:00.000000000Z", end = "2026-03-13T23:10:00.000000000Z" },
        ohlcv-1m: DateTimeRange { start = "2018-05-01T00:00:00.000000000Z", end = "2026-03-13T23:10:00.000000000Z" },
        ohlcv-1h: DateTimeRange { start = "2018-05-01T00:00:00.000000000Z", end = "2026-03-13T23:00:00.000000000Z" },
        ohlcv-1d: DateTimeRange { start = "2018-05-01T00:00:00.000000000Z", end = "2026-03-13T00:00:00.000000000Z" },
        definition: DateTimeRange { start = "2018-05-01T00:00:00.000000000Z", end = "2026-03-13T23:10:00.000000000Z" },
        statistics: DateTimeRange { start = "2018-05-01T00:00:00.000000000Z", end = "2026-03-13T23:10:00.000000000Z" },
        status: DateTimeRange { start = "2018-05-01T00:00:00.000000000Z", end = "2026-03-13T23:10:00.000000000Z" },
        imbalance: DateTimeRange { start = "2018-05-01T00:00:00.000000000Z", end = "2026-03-13T23:10:00.000000000Z" },
        bbo-1s: DateTimeRange { start = "2018-05-01T00:00:00.000000000Z", end = "2026-03-13T23:10:00.000000000Z" },
        bbo-1m: DateTimeRange { start = "2018-05-01T00:00:00.000000000Z", end = "2026-03-13T23:10:00.000000000Z" }
    }
}
```

### /metadata.get_dataset_range

Get the available range for thedatasetgiven the user's entitlements.

Use this method to discover data availability. Thestartandendvalues in the response can be used with thetimeseries.get_rangeandbatch.submit_jobendpoints.

This endpoint will return thestartandendtimestamps over the entire dataset as well as the per-schemastartandendtimestamps under theschemakey. In some cases, a schema's availability is a subset of the entire dataset availability.

#### Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| dataset | required | The dataset code (string identifier). Must be one of the values from list_datasets . |

#### Returns

The available range for the dataset.

| Field | Type | Description |
| --- | --- | --- |
| start | string | The inclusive start of the available range as an ISO 8601 timestamp . |
| end | string | The exclusive end of the available range as an ISO 8601 timestamp . |
| schema | object | A mapping of schema names to per-schema start and end timestamps. |

```python
GET https://hist.databento.com/v0/metadata.get_dataset_range
```

```python
1
2
3
```

```python
curl -G 'https://hist.databento.com/v0/metadata.get_dataset_range' \
 -u $YOUR_API_KEY: \
 -d dataset=XNAS.ITCH \
```

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
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
```

```python
{
    "start":"2018-05-01T00:00:00.000000000Z",
    "end":"2025-01-30T00:00:00.000000000Z",
    "schema": {
        "mbo": {
            "start":"2018-05-01T00:00:00.000000000Z",
            "end":"2025-01-30T00:00:00.000000000Z"
        },
        "mbp-1": {
            "start":"2018-05-01T00:00:00.000000000Z",
            "end":"2025-01-30T00:00:00.000000000Z"
        },
        "mbp-10": {
            "start":"2018-05-01T00:00:00.000000000Z",
            "end":"2025-01-30T00:00:00.000000000Z"
        },
        "bbo-1s": {
            "start":"2018-05-01T00:00:00.000000000Z",
            "end":"2025-01-30T00:00:00.000000000Z"
        },
        "bbo-1m": {
            "start":"2018-05-01T00:00:00.000000000Z",
            "end":"2025-01-30T00:00:00.000000000Z"
        },
        "tbbo": {
            "start":"2018-05-01T00:00:00.000000000Z",
            "end":"2025-01-30T00:00:00.000000000Z"
        },
        "trades": {
            "start":"2018-05-01T00:00:00.000000000Z",
            "end":"2025-01-30T00:00:00.000000000Z"
        },
        "ohlcv-1s": {
            "start":"2018-05-01T00:00:00.000000000Z",
            "end":"2025-01-30T00:00:00.000000000Z"
        },
        "ohlcv-1m": {
            "start":"2018-05-01T00:00:00.000000000Z",
            "end":"2025-01-30T00:00:00.000000000Z"
        },
        "ohlcv-1h": {
            "start":"2018-05-01T00:00:00.000000000Z",
            "end":"2025-01-30T00:00:00.000000000Z"
        },
        "ohlcv-1d": {
            "start":"2018-05-01T00:00:00.000000000Z",
            "end":"2025-01-30T00:00:00.000000000Z"
        },
        "definition": {
            "start":"2018-05-01T00:00:00.000000000Z",
            "end":"2025-01-30T00:00:00.000000000Z"
        },
        "statistics": {
            "start":"2018-05-01T00:00:00.000000000Z",
            "end":"2025-01-30T00:00:00.000000000Z"
        },
        "status": {
            "start":"2018-05-01T00:00:00.000000000Z",
            "end":"2025-01-30T00:00:00.000000000Z"
        },
        "imbalance": {
            "start":"2018-05-01T00:00:00.000000000Z",
            "end":"2025-01-30T00:00:00.000000000Z"
        }
    }
}
```

### Historical.metadata.get_dataset_range

Get the available range for thedatasetgiven the user's entitlements.

Use this method to discover data availability. Thestartandendvalues in the response can be used with thetimeseries.get_rangeandbatch.submit_jobendpoints.

This endpoint will return thestartandendtimestamps over the entire dataset as well as the per-schemastartandendtimestamps under theschemakey. In some cases, a schema's availability is a subset of the entire dataset availability.

#### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| dataset | Dataset or str | required | The dataset code (string identifier). Must be one of the values from list_datasets . |

#### Returns

dict[str, str | dict[str, dict[str, str]]]

The available range for the dataset.

| Field | Type | Description |
| --- | --- | --- |
| start | str | The inclusive start of the available range as an ISO 8601 timestamp . |
| end | str | The exclusive end of the available range as an ISO 8601 timestamp . |
| schema | dict[str, dict[str, str]] | A mapping of schema names to per-schema start and end timestamps. |

```python
Historical.metadata.get_dataset_range(
    dataset: Dataset | str,
) -> dict[str, str | dict[str, dict[str, str]]]
```

```python
1
2
3
4
5
6
7
```

```python
import databento as db

client = db.Historical("$YOUR_API_KEY")

available_range = client.metadata.get_dataset_range(dataset="XNAS.BASIC")

print(available_range)
```

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
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
```

```python
{
    "start":"2018-05-01T00:00:00.000000000Z",
    "end":"2025-01-30T00:00:00.000000000Z",
    "schema": {
        "mbo": {
            "start":"2018-05-01T00:00:00.000000000Z",
            "end":"2025-01-30T00:00:00.000000000Z"
        },
        "mbp-1": {
            "start":"2018-05-01T00:00:00.000000000Z",
            "end":"2025-01-30T00:00:00.000000000Z"
        },
        "mbp-10": {
            "start":"2018-05-01T00:00:00.000000000Z",
            "end":"2025-01-30T00:00:00.000000000Z"
        },
        "bbo-1s": {
            "start":"2018-05-01T00:00:00.000000000Z",
            "end":"2025-01-30T00:00:00.000000000Z"
        },
        "bbo-1m": {
            "start":"2018-05-01T00:00:00.000000000Z",
            "end":"2025-01-30T00:00:00.000000000Z"
        },
        "tbbo": {
            "start":"2018-05-01T00:00:00.000000000Z",
            "end":"2025-01-30T00:00:00.000000000Z"
        },
        "trades": {
            "start":"2018-05-01T00:00:00.000000000Z",
            "end":"2025-01-30T00:00:00.000000000Z"
        },
        "ohlcv-1s": {
            "start":"2018-05-01T00:00:00.000000000Z",
            "end":"2025-01-30T00:00:00.000000000Z"
        },
        "ohlcv-1m": {
            "start":"2018-05-01T00:00:00.000000000Z",
            "end":"2025-01-30T00:00:00.000000000Z"
        },
        "ohlcv-1h": {
            "start":"2018-05-01T00:00:00.000000000Z",
            "end":"2025-01-30T00:00:00.000000000Z"
        },
        "ohlcv-1d": {
            "start":"2018-05-01T00:00:00.000000000Z",
            "end":"2025-01-30T00:00:00.000000000Z"
        },
        "definition": {
            "start":"2018-05-01T00:00:00.000000000Z",
            "end":"2025-01-30T00:00:00.000000000Z"
        },
        "statistics": {
            "start":"2018-05-01T00:00:00.000000000Z",
            "end":"2025-01-30T00:00:00.000000000Z"
        },
        "status": {
            "start":"2018-05-01T00:00:00.000000000Z",
            "end":"2025-01-30T00:00:00.000000000Z"
        },
        "imbalance": {
            "start":"2018-05-01T00:00:00.000000000Z",
            "end":"2025-01-30T00:00:00.000000000Z"
        }
    }
}
```

### HistoricalClient::metadata::get_dataset_range

Get the available range for thedatasetgiven the user's entitlements.

Use this method to discover data availability. Thestartandendvalues in the response can be used with thetimeseries::get_rangeandbatch::submit_jobendpoints.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| dataset | impl AsRef<str> | The dataset code (string identifier). Must be one of the values from list_datasets . |

#### Returns

DatasetRange

The available range for the dataset.

| Field | Type | Description |
| --- | --- | --- |
| start | time::OffsetDateTime | The inclusive UTC start timestamp of the available range. |
| end | time::OffsetDateTime | The exclusive UTC end timestamp of the available range. |
| range_by_schema | HashMap<Schema, DateTimeRange> | A mapping of schema names to per-schema start and end timestamps. |

```python
pub async fn get_dataset_range(
    &mut self,
    dataset: &str,
) -> databento::Result<DatasetRange>;
```

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
```

```python
use databento::{HistoricalClient, dbn::Dataset};

let mut client =
    HistoricalClient::builder().key("$YOUR_API_KEY")?.build()?;
let range = client
    .metadata()
    .get_dataset_range(Dataset::XnasItch)
    .await?;
println!("{range:#?}");
```

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
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
```

```python
DatasetRange {
    start: 2018-05-01 0:00:00.0 +00:00:00,
    end: 2026-03-13 21:30:00.0 +00:00:00,
    range_by_schema: {
        Statistics: DateTimeRange {
            start: 2018-05-01 0:00:00.0 +00:00:00,
            end: 2026-03-13 21:30:00.0 +00:00:00,
        },
        Imbalance: DateTimeRange {
            start: 2018-05-01 0:00:00.0 +00:00:00,
            end: 2026-03-13 21:30:00.0 +00:00:00,
        },
        Ohlcv1M: DateTimeRange {
            start: 2018-05-01 0:00:00.0 +00:00:00,
            end: 2026-03-13 21:30:00.0 +00:00:00,
        },
        Definition: DateTimeRange {
            start: 2018-05-01 0:00:00.0 +00:00:00,
            end: 2026-03-13 21:30:00.0 +00:00:00,
        },
        Mbp10: DateTimeRange {
            start: 2018-05-01 0:00:00.0 +00:00:00,
            end: 2026-03-13 21:30:00.0 +00:00:00,
        },
        Bbo1S: DateTimeRange {
            start: 2018-05-01 0:00:00.0 +00:00:00,
            end: 2026-03-13 21:30:00.0 +00:00:00,
        },
        Bbo1M: DateTimeRange {
            start: 2018-05-01 0:00:00.0 +00:00:00,
            end: 2026-03-13 21:30:00.0 +00:00:00,
        },
        Tbbo: DateTimeRange {
            start: 2018-05-01 0:00:00.0 +00:00:00,
            end: 2026-03-13 21:30:00.0 +00:00:00,
        },
        Ohlcv1S: DateTimeRange {
            start: 2018-05-01 0:00:00.0 +00:00:00,
            end: 2026-03-13 21:30:00.0 +00:00:00,
        },
        Status: DateTimeRange {
            start: 2018-05-01 0:00:00.0 +00:00:00,
            end: 2026-03-13 21:30:00.0 +00:00:00,
        },
        Trades: DateTimeRange {
            start: 2018-05-01 0:00:00.0 +00:00:00,
            end: 2026-03-13 21:30:00.0 +00:00:00,
        },
        Ohlcv1H: DateTimeRange {
            start: 2018-05-01 0:00:00.0 +00:00:00,
            end: 2026-03-13 21:00:00.0 +00:00:00,
        },
        Mbo: DateTimeRange {
            start: 2018-05-01 0:00:00.0 +00:00:00,
            end: 2026-03-13 21:30:00.0 +00:00:00,
        },
        Mbp1: DateTimeRange {
            start: 2018-05-01 0:00:00.0 +00:00:00,
            end: 2026-03-13 21:30:00.0 +00:00:00,
        },
        Ohlcv1D: DateTimeRange {
            start: 2018-05-01 0:00:00.0 +00:00:00,
            end: 2026-03-13 0:00:00.0 +00:00:00,
        },
    },
}
```

### Historical::MetadataGetRecordCount

Get the record count of the time series data query.

This method may not be accurate for time ranges that are not discrete multiples of 10 minutes, potentially over-reporting the number of records in such cases. The definition schema is only accurate for discrete multiples of 24 hours.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| dataset | std::string | The dataset code (string identifier). Must be one of the values from MetadataListDatasets . Constants are provided in the databento::dataset namespace in <databento/constants.hpp> . |
| datetime_range | databento::DateTimeRange<UnixNanos> or databento::DateTimeRange<std::string> | The request range with an inclusive start and an optional exclusive end. Takes an ISO 8601 string or a UNIX timestamp in nanoseconds. Assumes UTC as timezone unless otherwise specified. If not specified, end defaults to the forward filled value of start based on the resolution provided. |
| symbols | std::vector<std::string> | The product symbols to filter for. Takes up to 2,000 symbols per request. Use databento::kAllSymbols from <databento/symbology.hpp> to request all symbols. |
| schema | databento::Schema | The data record schema . Must be one of the values from MetadataListSchemas . |
| stype_in | databento::SType | The symbology type of input symbols . Defaults to RawSymbol . |
| limit | std::uint64_t | The maximum number of records to return. Use 0 or {} for no limit. Defaults to no limit. |

#### Returns

std::uint64_t

The number of records.

```python
std::uint64_t MetadataGetRecordCount(
    const std::string& dataset,
    const DateTimeRange<UnixNanos>& datetime_range,
    const std::vector<std::string>& symbols, Schema schema);
std::uint64_t MetadataGetRecordCount(
    const std::string& dataset,
    const DateTimeRange<std::string>& datetime_range,
    const std::vector<std::string>& symbols, Schema schema);
std::uint64_t MetadataGetRecordCount(
    const std::string& dataset,
    const DateTimeRange<UnixNanos>& datetime_range,
    const std::vector<std::string>& symbols, Schema schema,
    SType stype_in, std::uint64_t limit);
std::uint64_t MetadataGetRecordCount(
    const std::string& dataset,
    const DateTimeRange<std::string>& datetime_range,
    const std::vector<std::string>& symbols, Schema schema,
    SType stype_in, std::uint64_t limit);
```

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
```

```python
#include <databento/historical.hpp>
#include <iostream>

using namespace databento;

auto client =
    Historical::Builder().SetKey("$YOUR_API_KEY").Build();
auto record_count = client.MetadataGetRecordCount(
    "GLBX.MDP3", {"2022-01-06T12:00", "2022-03-10"}, {"ESM2"},
    Schema::Mbo);
std::cout << record_count << '\n';
```

```python
1
```

```python
86913546
```

### /metadata.get_record_count

Get the record count of the time series data query.

This method may not be accurate for time ranges that are not discrete multiples of 10 minutes, potentially over-reporting the number of records in such cases. The definition schema is only accurate for discrete multiples of 24 hours.

#### Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| dataset | required | The dataset code (string identifier). Must be one of the values from list_datasets . |
| symbols | optional | The product symbols to filter for. Takes up to 2,000 symbols per request. If 'ALL_SYMBOLS' or not specified then will select all symbols. |
| schema | optional, default 'trades' | The data record schema . Must be one of the values from list_schemas . |
| start | required | The inclusive start of the request range. Takes an ISO 8601 string or UNIX timestamp in nanoseconds. Assumes UTC as timezone unless otherwise specified. |
| end | optional | The exclusive end of the request range. Takes an ISO 8601 string or UNIX timestamp in nanoseconds. Assumes UTC as timezone unless otherwise specified. Defaults to the forward filled value of start based on the resolution provided. |
| stype_in | optional, default 'raw_symbol' | The symbology type of input symbols . Must be one of 'raw_symbol', 'instrument_id', 'parent', or 'continuous'. |
| limit | optional | The maximum number of records to return. If not specified, then no limit. |

#### Returns

The record count.

```python
GET https://hist.databento.com/v0/metadata.get_record_count
```

```python
1
2
3
4
5
6
7
```

```python
curl -G 'https://hist.databento.com/v0/metadata.get_record_count' \
 -u $YOUR_API_KEY: \
 -d dataset=GLBX.MDP3 \
 -d symbols=ESM2 \
 -d schema=trades \
 -d start='2022-06-06T00:00' \
 -d end='2022-06-10T00:10'
```

```python
1
```

```python
1990595
```

### Historical.metadata.get_record_count

Get the record count of the time series data query.

This method may not be accurate for time ranges that are not discrete multiples of 10 minutes, potentially over-reporting the number of records in such cases. The definition schema is only accurate for discrete multiples of 24 hours.

#### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| dataset | Dataset or str | required | The dataset code (string identifier). Must be one of the values from list_datasets . |
| start | pd.Timestamp, datetime, date, str, or int | required | The inclusive start of the request range. Takes pd.Timestamp , Python datetime , Python date , ISO 8601 string, or UNIX timestamp in nanoseconds. Assumes UTC as timezone unless otherwise specified. |
| end | pd.Timestamp, datetime, date, str, or int | optional | The exclusive end of the request range. Takes pd.Timestamp , Python datetime , Python date , ISO 8601 string, or UNIX timestamp in nanoseconds. Assumes UTC as timezone unless otherwise specified. Defaults to the forward filled value of start based on the resolution provided. |
| symbols | Iterable[str \| int] or str or int | optional | The product symbols to filter for. Takes up to 2,000 symbols per request. If 'ALL_SYMBOLS' or None then will select all symbols. |
| schema | Schema or str, default 'trades' | optional | The data record schema . Must be one of the values from list_schemas . |
| stype_in | SType or str, default 'raw_symbol' | optional | The symbology type of input symbols . Must be one of 'raw_symbol', 'instrument_id', 'parent', or 'continuous'. |
| limit | int | optional | The maximum number of records to return. If None then no limit. |

#### Returns

The record count.

```python
Historical.metadata.get_record_count(
    dataset: Dataset | str,
    start: pd.Timestamp | datetime | date | str | int,
    end: pd.Timestamp | datetime | date | str | int | None = None,
    symbols: Iterable[str | int] | str | int | None = None,
    schema: Schema | str = "trades",
    stype_in: SType | str = "raw_symbol",
    limit: int | None = None,
) -> int
```

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
```

```python
import databento as db

client = db.Historical("$YOUR_API_KEY")

count = client.metadata.get_record_count(
    dataset="GLBX.MDP3",
    symbols=["ESM2"],
    schema="mbo",
    start="2022-01-06",
)
print(count)
```

```python
1
```

```python
1329107
```

### HistoricalClient::metadata::get_record_count

Get the record count of the time series data query.

This method may not be accurate for time ranges that are not discrete multiples of 10 minutes, potentially over-reporting the number of records in such cases. The definition schema is only accurate for discrete multiples of 24 hours.

#### Parameters

| Field | Type | Description |
| --- | --- | --- |
| params | GetRecordCountParams | See GetRecordCountParams for details. |

#### Returns

The record count.

```python
pub async fn get_record_count(
    &mut self,
    params: &GetRecordCountParams,
) -> databento::Result<u64>;
```

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
18
19
20
21
22
23
```

```python
use databento::{
    HistoricalClient, dbn::Schema,
    historical::metadata::GetRecordCountParams,
};
use time::macros::datetime;

let mut client =
    HistoricalClient::builder().key("$YOUR_API_KEY")?.build()?;
let record_count = client
    .metadata()
    .get_record_count(
        &GetRecordCountParams::builder()
            .dataset("GLBX.MDP3")
            .date_time_range(
                datetime!(2022-01-06 12:00 UTC)
                    ..datetime!(2022-03-10 00:00 UTC),
            )
            .symbols("ESM2")
            .schema(Schema::Mbo)
            .build(),
    )
    .await?;
println!("{record_count}");
```

```python
1
```

```python
86913546
```

### Historical::MetadataGetBillableSize

Get the billable uncompressed raw binary size for historical streaming or batched files.

This method may not be accurate for time ranges that are not discrete multiples of 10 minutes, potentially over-reporting the size in such cases. The definition schema is only accurate for discrete multiples of 24 hours.

The amount billed will be based on the actual amount of bytes sent; see ourpricing documentationfor more details.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| dataset | std::string | The dataset code (string identifier). Must be one of the values from MetadataListDatasets . Constants are provided in the databento::dataset namespace in <databento/constants.hpp> . |
| datetime_range | databento::DateTimeRange<UnixNanos> or databento::DateTimeRange<std::string> | The request range with an inclusive start and an optional exclusive end. Takes an ISO 8601 string or a UNIX timestamp in nanoseconds. Assumes UTC as timezone unless otherwise specified. If not specified, end defaults to the forward filled value of start based on the resolution provided. |
| symbols | std::vector<std::string> | The product symbols to filter for. Takes up to 2,000 symbols per request. Use databento::kAllSymbols from <databento/symbology.hpp> to request all symbols. |
| schema | databento::Schema | The data record schema . Must be one of the values from MetadataListSchemas . |
| stype_in | databento::SType | The symbology type of input symbols . Defaults to RawSymbol . |
| limit | std::uint64_t | The maximum number of records to return. Use 0 or {} for no limit. Defaults to no limit. |

#### Returns

std::uint64_t

The size in number of bytes used for billing.

```python
std::uint64_t MetadataGetBillableSize(
    const std::string& dataset,
    const DateTimeRange<UnixNanos>& datetime_range,
    const std::vector<std::string>& symbols, Schema schema);
std::uint64_t MetadataGetBillableSize(
    const std::string& dataset,
    const DateTimeRange<std::string>& datetime_range,
    const std::vector<std::string>& symbols, Schema schema);
std::uint64_t MetadataGetBillableSize(
    const std::string& dataset,
    const DateTimeRange<UnixNanos>& datetime_range,
    const std::vector<std::string>& symbols, Schema schema,
    SType stype_in, std::uint64_t limit);
std::uint64_t MetadataGetBillableSize(
    const std::string& dataset,
    const DateTimeRange<std::string>& datetime_range,
    const std::vector<std::string>& symbols, Schema schema,
    SType stype_in, std::uint64_t limit);
```

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
```

```python
#include <databento/historical.hpp>
#include <iostream>

using namespace databento;

auto client =
    Historical::Builder().SetKey("$YOUR_API_KEY").Build();
auto billable_size = client.MetadataGetBillableSize(
    "GLBX.MDP3", {"2022-06-06T00:00", "2022-06-10T12:10"},
    {"ESM2"}, Schema::Trades);
std::cout << billable_size << '\n';
```

```python
1
```

```python
99219648
```

### /metadata.get_billable_size

Get the billable uncompressed raw binary size for historical streaming or batched files.

This method may not be accurate for time ranges that are not discrete multiples of 10 minutes, potentially over-reporting the size in such cases. The definition schema is only accurate for discrete multiples of 24 hours.

The amount billed will be based on the actual amount of bytes sent; see ourpricing documentationfor more details.

#### Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| dataset | required | The dataset code (string identifier). Must be one of the values from list_datasets . |
| symbols | optional | The product symbols to filter for. Takes up to 2,000 symbols per request. If 'ALL_SYMBOLS' or not specified then will select all symbols. |
| schema | optional, default 'trades' | The data record schema . Must be one of the values from list_schemas . |
| start | required | The inclusive start of the request range. Takes an ISO 8601 string or UNIX timestamp in nanoseconds. Assumes UTC as timezone unless otherwise specified. |
| end | optional | The exclusive end of the request range. Takes an ISO 8601 string or UNIX timestamp in nanoseconds. Assumes UTC as timezone unless otherwise specified. Defaults to the forward filled value of start based on the resolution provided. |
| stype_in | optional, default 'raw_symbol' | The symbology type of input symbols . Must be one of 'raw_symbol', 'instrument_id', 'parent', or 'continuous'. |
| limit | optional | The maximum number of records to return. If not specified, then no limit. |

#### Returns

The size in number of bytes used for billing.

```python
GET https://hist.databento.com/v0/metadata.get_billable_size
```

```python
1
2
3
4
5
6
7
```

```python
curl -G 'https://hist.databento.com/v0/metadata.get_billable_size' \
 -u $YOUR_API_KEY: \
 -d dataset=GLBX.MDP3 \
 -d symbols=ESM2 \
 -d schema=trades \
 -d start='2022-06-02T00:00' \
 -d end='2022-06-10T00:10'
```

```python
1
```

```python
142505232
```

### Historical.metadata.get_billable_size

Get the billable uncompressed raw binary size for historical streaming or batched files.

This method may not be accurate for time ranges that are not discrete multiples of 10 minutes, potentially over-reporting the size in such cases. The definition schema is only accurate for discrete multiples of 24 hours.

The amount billed will be based on the actual amount of bytes sent; see ourpricing documentationfor more details.

#### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| dataset | Dataset or str | required | The dataset code (string identifier). Must be one of the values from list_datasets . |
| start | pd.Timestamp, datetime, date, str, or int | required | The inclusive start of the request range. Takes pd.Timestamp , Python datetime , Python date , ISO 8601 string, or UNIX timestamp in nanoseconds. Assumes UTC as timezone unless otherwise specified. |
| end | pd.Timestamp, datetime, date, str, or int | optional | The exclusive end of the request range. Takes pd.Timestamp , Python datetime , Python date , ISO 8601 string, or UNIX timestamp in nanoseconds. Assumes UTC as timezone unless otherwise specified. Defaults to the forward filled value of start based on the resolution provided. |
| symbols | Iterable[str \| int] or str or int | optional | The product symbols to filter for. Takes up to 2,000 symbols per request. If 'ALL_SYMBOLS' or None then will select all symbols. |
| schema | Schema or str, default 'trades' | optional | The data record schema . Must be one of the values from list_schemas . |
| stype_in | SType or str, default 'raw_symbol' | optional | The symbology type of input symbols . Must be one of 'raw_symbol', 'instrument_id', 'parent', or 'continuous'. |
| limit | int | optional | The maximum number of records to return. If None then no limit. |

#### Returns

The size in number of bytes used for billing.

```python
Historical.metadata.get_billable_size(
    dataset: Dataset | str,
    start: pd.Timestamp | datetime | date | str | int,
    end: pd.Timestamp | datetime | date | str | int | None = None,
    symbols: Iterable[str | int] | str | int | None = None,
    schema: Schema | str = "trades",
    stype_in: Stype | str = "raw_symbol",
    limit: int | None = None,
) -> int
```

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
```

```python
import databento as db

client = db.Historical("$YOUR_API_KEY")

size = client.metadata.get_billable_size(
    dataset="GLBX.MDP3",
    symbols=["ESM2"],
    schema="trades",
    start="2022-06-06T00:00:00",
    end="2022-06-10T12:10:00",
)
print(size)
```

```python
1
```

```python
99219648
```

### HistoricalClient::metadata::get_billable_size

Get the billable uncompressed raw binary size for historical streaming or batched files.

This method may not be accurate for time ranges that are not discrete multiples of 10 minutes, potentially over-reporting the size in such cases. The definition schema is only accurate for discrete multiples of 24 hours.

The amount billed will be based on the actual amount of bytes sent; see ourpricing documentationfor more details.

#### Parameters

| Field | Type | Description |
| --- | --- | --- |
| params | GetBillableSizeParams | See GetBillableSizeParams for details. |

#### Returns

The size in number of bytes used for billing.

```python
pub async fn get_billable_size(
    &mut self,
    params: &GetBillableSizeParams,
) -> databento::Result<u64>;
```

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
18
19
20
21
22
23
24
```

```python
use databento::{
    HistoricalClient,
    dbn::{Dataset, Schema},
    historical::metadata::GetBillableSizeParams,
};
use time::macros::datetime;

let mut client =
    HistoricalClient::builder().key("$YOUR_API_KEY")?.build()?;
let billable_size = client
    .metadata()
    .get_billable_size(
        &GetBillableSizeParams::builder()
            .dataset(Dataset::GlbxMdp3)
            .date_time_range(
                datetime!(2022-06-06 00:00 UTC)
                    ..datetime!(2022-06-10 12:10 UTC),
            )
            .symbols("ESM2")
            .schema(Schema::Trades)
            .build(),
    )
    .await?;
println!("{billable_size}");
```

```python
1
```

```python
99219648
```

### Historical::MetadataGetCost

Get the cost in US dollars for a historical streaming or batch download request. This cost respects any discounts provided by flat rate plans.

This method may not be accurate for time ranges that are not discrete multiples of 10 minutes, potentially over-reporting the cost in such cases. The definition schema is only accurate for discrete multiples of 24 hours.

The amount billed will be based on the actual amount of bytes sent; see ourpricing documentationfor more details.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| dataset | std::string | The dataset code (string identifier). Must be one of the values from MetadataListDatasets . Constants are provided in the databento::dataset namespace in <databento/constants.hpp> . |
| datetime_range | databento::DateTimeRange<UnixNanos> or databento::DateTimeRange<std::string> | The request range with an inclusive start and an optional exclusive end. Takes an ISO 8601 string or a UNIX timestamp in nanoseconds. Assumes UTC as timezone unless otherwise specified. If not specified, end defaults to the forward filled value of start based on the resolution provided. |
| symbols | std::vector<std::string> | The product symbols to filter for. Takes up to 2,000 symbols per request. Use databento::kAllSymbols from <databento/symbology.hpp> to request all symbols. |
| schema | databento::Schema | The data record schema . Must be one of the values from MetadataListSchemas . |
| stype_in | databento::SType | The symbology type of input symbols . Defaults to RawSymbol . |
| limit | std::uint64_t | The maximum number of records to return. Use 0 or {} for no limit. Defaults to no limit. |

#### Returns

The cost in US dollars.

```python
double MetadataGetCost(
    const std::string& dataset,
    const DateTimeRange<UnixNanos>& datetime_range,
    const std::vector<std::string>& symbols, Schema schema);
double MetadataGetCost(
    const std::string& dataset,
    const DateTimeRange<std::string>& datetime_range,
    const std::vector<std::string>& symbols, Schema schema);
double MetadataGetCost(
    const std::string& dataset,
    const DateTimeRange<UnixNanos>& datetime_range,
    const std::vector<std::string>& symbols, Schema schema,
    SType stype_in, std::uint64_t limit);
double MetadataGetCost(
    const std::string& dataset,
    const DateTimeRange<std::string>& datetime_range,
    const std::vector<std::string>& symbols, Schema schema,
    SType stype_in, std::uint64_t limit);
```

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
```

```python
#include <databento/historical.hpp>
#include <iostream>

using namespace databento;

auto client =
    Historical::Builder().SetKey("$YOUR_API_KEY").Build();
auto cost = client.MetadataGetCost(
    "GLBX.MDP3", {"2022-06-06T00:00", "2022-06-10T12:10"},
    {"ESM2"}, Schema::Trades);
std::cout << cost << '\n';
```

```python
1
```

```python
2.58735
```

### /metadata.get_cost

Get the cost in US dollars for a historical streaming or batch download request. This cost respects any discounts provided by flat rate plans.

This method may not be accurate for time ranges that are not discrete multiples of 10 minutes, potentially over-reporting the cost in such cases. The definition schema is only accurate for discrete multiples of 24 hours.

The amount billed will be based on the actual amount of bytes sent; see ourpricing documentationfor more details.

#### Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| dataset | required | The dataset code. Must be one of the values from list_datasets . |
| symbols | optional | The product symbols to filter for. Takes up to 2,000 symbols per request. If 'ALL_SYMBOLS' or not specified then will select all symbols. |
| schema | optional, default 'trades' | The data record schema . Must be one of the values from list_schemas . |
| start | required | The inclusive start of the request range. Takes an ISO 8601 string or UNIX timestamp in nanoseconds. Assumes UTC as timezone unless otherwise specified. |
| end | optional | The exclusive end of the request range. Takes an ISO 8601 string or UNIX timestamp in nanoseconds. Assumes UTC as timezone unless otherwise specified. Defaults to the forward filled value of start based on the resolution provided. |
| stype_in | optional, default 'raw_symbol' | The symbology type of input symbols . Must be one of 'raw_symbol', 'instrument_id', 'parent', or 'continuous'. |
| limit | optional | The maximum number of records to return. If not specified, then no limit. |

#### Returns

The cost in US dollars.

```python
GET https://hist.databento.com/v0/metadata.get_cost
```

```python
1
2
3
4
5
6
7
```

```python
curl -G 'https://hist.databento.com/v0/metadata.get_cost' \
 -u $YOUR_API_KEY: \
 -d dataset=GLBX.MDP3 \
 -d symbols=ESM2 \
 -d schema=mbo \
 -d start='2022-06-06T00:00' \
 -d end='2022-06-10T00:10'
```

```python
1
```

```python
4.923090054095
```

### Historical.metadata.get_cost

Get the cost in US dollars for a historical streaming or batch download request. This cost respects any discounts provided by flat rate plans.

This method may not be accurate for time ranges that are not discrete multiples of 10 minutes, potentially over-reporting the cost in such cases. The definition schema is only accurate for discrete multiples of 24 hours.

The amount billed will be based on the actual amount of bytes sent; see ourpricing documentationfor more details.

#### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| dataset | Dataset or str | required | The dataset code (string identifier). Must be one of the values from list_datasets . |
| start | pd.Timestamp, datetime, date, str, or int | required | The inclusive start of the request range. Takes pd.Timestamp , Python datetime , Python date , ISO 8601 string, or UNIX timestamp in nanoseconds. Assumes UTC as timezone unless otherwise specified. |
| end | pd.Timestamp, datetime, date, str, or int | optional | The exclusive end of the request range. Takes pd.Timestamp , Python datetime , Python date , ISO 8601 string, or UNIX timestamp in nanoseconds. Assumes UTC as timezone unless otherwise specified. Defaults to the forward filled value of start based on the resolution provided. |
| symbols | Iterable[str \| int] or str or int | optional | The product symbols to filter for. Takes up to 2,000 symbols per request. If 'ALL_SYMBOLS' or None then will select all symbols. |
| schema | Schema or str, default 'trades' | optional | The data record schema . Must be one of the values from list_schemas . |
| stype_in | SType or str, default 'raw_symbol' | optional | The symbology type of input symbols . Must be one of 'raw_symbol', 'instrument_id', 'parent', or 'continuous'. |
| limit | int | optional | The maximum number of records to return. If None then no limit. |

#### Returns

The cost in US dollars.

```python
Historical.metadata.get_cost(
    dataset: Dataset | str,
    start: pd.Timestamp | datetime | date | str | int,
    end: pd.Timestamp | datetime | date | str | int | None = None,
    symbols: Iterable[str | int] | str | int | None = None,
    schema: Schema | str = "trades",
    stype_in: SType | str = "raw_symbol",
    limit: int | None = None,
) -> float
```

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
```

```python
import databento as db

client = db.Historical("$YOUR_API_KEY")

cost = client.metadata.get_cost(
    dataset="GLBX.MDP3",
    symbols=["ESM2"],
    schema="trades",
    start="2022-06-06T00:00:00",
    end="2022-06-10T12:10:00",
)
print(cost)
```

```python
1
```

```python
2.587353944778
```

### HistoricalClient::metadata::get_cost

Get the cost in US dollars for a historical streaming or batch download request. This cost respects any discounts provided by flat rate plans.

This method may not be accurate for time ranges that are not discrete multiples of 10 minutes, potentially over-reporting the cost in such cases. The definition schema is only accurate for discrete multiples of 24 hours.

The amount billed will be based on the actual amount of bytes sent; see ourpricing documentationfor more details.

#### Parameters

| Field | Type | Description |
| --- | --- | --- |
| params | GetCostParams | See GetCostParams for details. |

#### Returns

The cost in US dollars.

```python
pub async fn get_cost(
    &mut self,
    params: &GetCostParams,
) -> databento::Result<f64>;
```

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
18
19
20
21
22
23
```

```python
use databento::{
    HistoricalClient, dbn::Schema,
    historical::metadata::GetCostParams,
};
use time::macros::datetime;

let mut client =
    HistoricalClient::builder().key("$YOUR_API_KEY")?.build()?;
let cost = client
    .metadata()
    .get_cost(
        &GetCostParams::builder()
            .dataset("GLBX.MDP3")
            .date_time_range(
                datetime!(2022-06-06 00:00 UTC)
                    ..datetime!(2022-06-10 12:10 UTC),
            )
            .symbols("ESM2")
            .schema(Schema::Trades)
            .build(),
    )
    .await?;
println!("{cost:.4}");
```

```python
1
```

```python
2.5874
```

## Time series

### Historical::TimeseriesGetRange

Make a streaming request for time series data from Databento.

Primary method for getting historical intraday and daily market data, instrument definitions, and market status data directly into your application.

There are two consumption patterns:

For large requests, consider usingBatchSubmitJobinstead. Consider usingTimeseriesGetRangeToFileto save the data directly to a file.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| dataset | std::string | The dataset code (string identifier). Must be one of the values from MetadataListDatasets . Constants are provided in the databento::dataset namespace in <databento/constants.hpp> . |
| datetime_range | databento::DateTimeRange<UnixNanos> or databento::DateTimeRange<std::string> | The request range with an inclusive start and an optional exclusive end. Filters on ts_recv if it exists in the schema, otherwise ts_event . Takes an ISO 8601 string or a UNIX timestamp in nanoseconds. Assumes UTC as timezone unless otherwise specified. If not specified, end defaults to the forward filled value of start based on the resolution provided. |
| symbols | std::vector<std::string> | The product symbols to filter for. Takes up to 2,000 symbols per request. Use databento::kAllSymbols from <databento/symbology.hpp> to request all symbols. |
| schema | databento::Schema | The data record schema . Must be one of the values from MetadataListSchemas . |
| stype_in | databento::SType | The symbology type of input symbols . Defaults to RawSymbol . |
| stype_out | databento::SType | The symbology type of output symbols. Defaults to InstrumentId . Must be a valid symbology combination with stype_in . See symbology combinations . |
| limit | std::uint64_t | The maximum number of records to return. Use 0 or {} for no limit. Defaults to no limit. |
| metadata_callback | std::function<void(Metadata&&)> | A callback for receiving the Metadata associated with the result of the query. This callback will be called only once, immediately before the first time record_callback is called. Only used in callback-based overloads. |
| record_callback | std::function<KeepGoing(const Record&)> | A callback for receiving the Record s from the query. The particular record type will depend on the schema . The callback will be called as data is received. Return KeepGoing::Continue to continue receiving records or KeepGoing::Stop to stop streaming. Only used in callback-based overloads. |

#### Returns

Pull-based overloads:Returns aDbnStorethat can be iterated withGetMetadataandNextRecord.

A full list of fields returned for each schema is available throughHistorical.MetadataListFieldsor the struct definitions in<databento/record.hpp>.

Callback overloads:Returns data via the callbacksmetadata_callbackandrecord_callback.

The reference passed torecord_callbackis only valid during the callback. Copy the record or particular fields to persist data between calls to the callback.

Won't return until all records for the query have been passed torecord_callbackor the callback returnedKeepGoing::Stop.

```python
// Pull-based
DbnStore TimeseriesGetRange(
    const std::string& dataset,
    const DateTimeRange<UnixNanos>& datetime_range,
    const std::vector<std::string>& symbols, Schema schema);
DbnStore TimeseriesGetRange(
    const std::string& dataset,
    const DateTimeRange<std::string>& datetime_range,
    const std::vector<std::string>& symbols, Schema schema);
DbnStore TimeseriesGetRange(
    const std::string& dataset,
    const DateTimeRange<UnixNanos>& datetime_range,
    const std::vector<std::string>& symbols, Schema schema,
    SType stype_in, SType stype_out, std::uint64_t limit);
DbnStore TimeseriesGetRange(
    const std::string& dataset,
    const DateTimeRange<std::string>& datetime_range,
    const std::vector<std::string>& symbols, Schema schema,
    SType stype_in, SType stype_out, std::uint64_t limit);
// Callback-based
void TimeseriesGetRange(
    const std::string& dataset,
    const DateTimeRange<UnixNanos>& datetime_range,
    const std::vector<std::string>& symbols, Schema schema,
    const RecordCallback& record_callback);
void TimeseriesGetRange(
    const std::string& dataset,
    const DateTimeRange<std::string>& datetime_range,
    const std::vector<std::string>& symbols, Schema schema,
    const RecordCallback& record_callback);
void TimeseriesGetRange(
    const std::string& dataset,
    const DateTimeRange<UnixNanos>& datetime_range,
    const std::vector<std::string>& symbols, Schema schema,
    SType stype_in, SType stype_out, std::uint64_t limit,
    const MetadataCallback& metadata_callback,
    const RecordCallback& record_callback);
void TimeseriesGetRange(
    const std::string& dataset,
    const DateTimeRange<std::string>& datetime_range,
    const std::vector<std::string>& symbols, Schema schema,
    SType stype_in, SType stype_out, std::uint64_t limit,
    const MetadataCallback& metadata_callback,
    const RecordCallback& record_callback);
```

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
```

```python
#include <databento/historical.hpp>
#include <databento/record.hpp>
#include <iostream>

using namespace databento;

auto client =
    Historical::Builder().SetKey("$YOUR_API_KEY").Build();
auto store = client.TimeseriesGetRange(
    "GLBX.MDP3", {"2022-06-06T00:00", "2022-06-10T00:10"},
    {"ESM2"}, Schema::Trades, SType::RawSymbol,
    SType::InstrumentId, 1);
while (const Record* record = store.NextRecord()) {
  const auto& trade_msg = record->Get<TradeMsg>();
  std::cout << trade_msg << '\n';
}
```

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
```

```python
TradeMsg {
    hd = RecordHeader { length = 12, rtype = mbp-0, publisher_id = 1, instrument_id = 3403, ts_event = 2022-06-06T00:00:00.070033767Z },
    price = 4108.500000000,
    size = 1,
    action = Trade,
    side = Ask,
    flags = 0,
    depth = 0,
    ts_recv = 2022-06-06T00:00:00.070314216Z,
    ts_in_delta = 18681,
    sequence = 157862
}
```

### /timeseries.get_range

Make a streaming request for time series data from Databento.

Primary method for getting historical intraday and daily market data, instrument definitions, and market status data directly into your application.

For large requests, consider using/batch.submit_jobinstead.

#### Parameters

The following parameters should be encoded as form data (not in a JSON body).

| Parameter | Required | Description |
| --- | --- | --- |
| dataset | required | The dataset code (string identifier). Must be one of the values from list_datasets . |
| start | required | The inclusive start of the request range. Filters on ts_recv if it exists in the schema, otherwise ts_event . Takes an ISO 8601 string or UNIX timestamp in nanoseconds. Assumes UTC as timezone unless otherwise specified. |
| end | optional | The exclusive end of the request range. Filters on ts_recv if it exists in the schema, otherwise ts_event . Takes an ISO 8601 string or UNIX timestamp in nanoseconds. Assumes UTC as timezone unless otherwise specified. Defaults to the forward filled value of start based on the resolution provided. |
| symbols | optional | The product symbols to filter for. Takes up to 2,000 symbols per request. If more than 1 symbol is specified, the data is merged and sorted by time. If 'ALL_SYMBOLS' or not specified then will select all symbols. |
| schema | optional, default 'trades' | The data record schema . Must be one of the values from list_schemas . |
| encoding | optional, default 'csv' | The data encoding . Must be one of 'dbn', 'csv', 'json'. For fastest transfer speed, 'dbn' is recommended. |
| compression | optional, default 'none' | The data compression mode. Must be either 'zstd' or 'none'. For fastest transfer speed, 'zstd' is recommended. |
| stype_in | optional, default 'raw_symbol' | The symbology type of input symbols . Must be one of 'raw_symbol', 'instrument_id', 'parent', or 'continuous'. |
| stype_out | optional, default 'instrument_id' | The symbology type of output symbols. Must be one of 'raw_symbol', 'instrument_id', 'parent', or 'continuous'. Must be a valid symbology combination with stype_in . See symbology combinations . |
| limit | optional | The maximum number of records to return. If not specified, then no limit. |
| pretty_px | optional, default 'false' | If prices should be formatted to the correct scale (using the fixed-precision scalar 1e-9). Only applicable for 'csv' or 'json' encodings. Must be a boolean-like value 'true' or 'false'. |
| pretty_ts | optional, default 'false' | If timestamps should be formatted as ISO 8601 strings. Only applicable for 'csv' or 'json' encodings. Must be a boolean-like value 'true' or 'false'. |
| map_symbols | optional, default 'false' | If a symbol field should be included with each text-encoded record. Only applicable for 'csv' or 'json' encodings. Must be a boolean-like value 'true' or 'false'. |

#### Returns

Either a DBN, CSV, or JSON file depending on theencodingparameter.

The JSON encoding follows theJSON lines specificationwith one record per line.

A full list of fields for each schema is available through/metadata.list_fields.

```python
POST https://hist.databento.com/v0/timeseries.get_range
```

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
```

```python
curl -X POST 'https://hist.databento.com/v0/timeseries.get_range' \
 -u $YOUR_API_KEY: \
 -d dataset=GLBX.MDP3 \
 -d symbols=ESM2 \
 -d schema=trades \
 -d start='2022-06-06T00:00' \
 -d end='2022-06-10T00:10' \
 -d encoding=json \
 -d pretty_px=true \
 -d pretty_ts=true \
 -d map_symbols=true \
 -d limit=1
```

```python
1
```

```python
{"ts_recv":"2022-06-06T00:00:00.070314216Z","hd":{"ts_event":"2022-06-06T00:00:00.070033767Z","rtype":0,"publisher_id":1,"instrument_id":3403},"action":"T","side":"A","depth":0,"price":"4108.500000000","size":1,"flags":0,"ts_in_delta":18681,"sequence":157862,"symbol":"ESM2"}
```

### Historical.timeseries.get_range

Makes a streaming request for time series data from Databento.

This is the primary method for getting historical market data, instrument definitions, and status data directly into your application.

This method only returns after all of the data has been downloaded, which can take a long time. For large requests, consider usingbatch.submit_jobinstead.

#### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| dataset | Dataset or str | required | The dataset code (string identifier). Must be one of the values from list_datasets . |
| start | pd.Timestamp, datetime, date, str, or int | required | The inclusive start of the request range. Filters on ts_recv if it exists in the schema, otherwise ts_event . Takes pd.Timestamp , Python datetime , Python date , ISO 8601 string, or UNIX timestamp in nanoseconds. Assumes UTC as timezone unless otherwise specified. |
| end | pd.Timestamp, datetime, date, str, or int | optional | The exclusive end of the request range. Filters on ts_recv if it exists in the schema, otherwise ts_event . Takes pd.Timestamp , Python datetime , Python date , ISO 8601 string, or UNIX timestamp in nanoseconds. Assumes UTC as timezone unless otherwise specified. Defaults to the forward filled value of start based on the resolution provided. |
| symbols | Iterable[str \| int] or str or int | optional | The product symbols to filter for. Takes up to 2,000 symbols per request. If more than 1 symbol is specified, the data is merged and sorted by time. If 'ALL_SYMBOLS' or None then will select all symbols. |
| schema | Schema or str, default 'trades' | optional | The data record schema . Must be one of the values from list_schemas . |
| stype_in | SType or str, default 'raw_symbol' | optional | The symbology type of input symbols . Must be one of 'raw_symbol', 'instrument_id', 'parent', or 'continuous'. |
| stype_out | SType or str, default 'instrument_id' | optional | The symbology type of output symbols. Must be one of 'raw_symbol', 'instrument_id', 'parent', or 'continuous'. Must be a valid symbology combination with stype_in . See symbology combinations . |
| limit | int | optional | The maximum number of records to return. If None then no limit. |
| path | PathLike[str] or str | optional | The file path to stream the data to. It is recommended to use the ".dbn.zst" suffix. |

#### Returns

ADBNStoreobject.

A full list of fields for each schema is available throughHistorical.metadata.list_fields.

```python
Historical.timeseries.get_range(
    dataset: Dataset | str,
    start: pd.Timestamp | datetime | date | str | int,
    end: pd.Timestamp | datetime | date | str | int | None = None,
    symbols: Iterable[str | int] | str | int | None = None,
    schema: Schema | str = "trades",
    stype_in: SType | str = "raw_symbol",
    stype_out: SType | str = "instrument_id",
    limit: int | None = None,
    path: PathLike[str] | str | None = None,
) -> DBNStore
```

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
```

```python
import databento as db

client = db.Historical("$YOUR_API_KEY")

data = client.timeseries.get_range(
    dataset="GLBX.MDP3",
    symbols=["ESM2"],
    schema="trades",
    start="2022-06-06T00:00:00",
    end="2022-06-10T00:10:00",
    limit=1,
)
df = data.to_df()
print(df.iloc[0].to_json(indent=4))
```

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
```

```python
{
    "ts_event":1654473600070,
    "rtype":0,
    "publisher_id":1,
    "instrument_id":3403,
    "action":"T",
    "side":"A",
    "depth":0,
    "price":4108.5,
    "size":1,
    "flags":0,
    "ts_in_delta":18681,
    "sequence":157862,
    "symbol":"ESM2"
}
```

### HistoricalClient::timeseries::get_range

Makes a streaming request for time series data from Databento.

This is the primary method for getting historical market data, instrument definitions, and status data directly into your application.

This method returns anasync decoder. To persist the data immediately, usetimeseries::get_range_to_file. For large requests, consider usingbatch::submit_jobinstead.

#### Parameters

| Field | Type | Description |
| --- | --- | --- |
| params | GetRangeParams | See GetRangeParams for details. |

#### Returns

AnAsyncDbnDecoderobject for incrementally decoding the records from the stream.

A full list of fields for each schema is available throughHistorical.metadata.list_fields.

```python
pub async fn get_range(
    &mut self,
    params: &GetRangeParams,
) -> databento::Result<AsyncDbnDecoder>;
```

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
18
19
20
21
22
23
24
25
26
27
28
```

```python
use std::num::NonZeroU64;

use databento::{
    HistoricalClient,
    dbn::{Dataset, Schema, TradeMsg},
    historical::timeseries::GetRangeParams,
};
use time::macros::datetime;

let mut client =
    HistoricalClient::builder().key("$YOUR_API_KEY")?.build()?;
let mut decoder = client
    .timeseries()
    .get_range(
        &GetRangeParams::builder()
            .dataset(Dataset::GlbxMdp3)
            .date_time_range(
                datetime!(2022-06-06 00:00 UTC)
                    ..datetime!(2022-06-10 12:10 UTC),
            )
            .symbols("ESM2")
            .schema(Schema::Trades)
            .maybe_limit(NonZeroU64::new(1))
            .build(),
    )
    .await?;
let trade = decoder.decode_record::<TradeMsg>().await?.unwrap();
println!("{trade:#?}");
```

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
18
```

```python
TradeMsg {
    hd: RecordHeader {
        length: 12,
        rtype: Mbp0,
        publisher_id: GlbxMdp3Glbx,
        instrument_id: 3403,
        ts_event: 1654473600070033767,
    },
    price: 4108.500000000,
    size: 1,
    action: 'T',
    side: 'A',
    flags: 0,
    depth: 0,
    ts_recv: 1654473600070314216,
    ts_in_delta: 18681,
    sequence: 157862,
}
```

### Historical.timeseries.get_range_async

Asynchronously request a historical time series data stream from Databento.

Primary method for getting historical intraday market data, daily data, instrument definitions and market status data directly into your application.

This method only returns after all of the data has been downloaded, which can take a long time. For large requests, consider usingbatch.submit_jobinstead.

#### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| dataset | Dataset or str | required | The dataset code (string identifier). Must be one of the values from list_datasets . |
| start | pd.Timestamp, datetime, date, str, or int | required | The inclusive start of the request range. Filters on ts_recv if it exists in the schema, otherwise ts_event . Takes pd.Timestamp , Python datetime , Python date , ISO 8601 string, or UNIX timestamp in nanoseconds. Assumes UTC as timezone unless otherwise specified. |
| end | pd.Timestamp, datetime, date, str, or int | optional | The exclusive end of the request range. Filters on ts_recv if it exists in the schema, otherwise ts_event . Takes pd.Timestamp , Python datetime , Python date , ISO 8601 string, or UNIX timestamp in nanoseconds. Assumes UTC as timezone unless otherwise specified. Defaults to the forward filled value of start based on the resolution provided. |
| symbols | Iterable[str \| int] or str or int | optional | The product symbols to filter for. Takes up to 2,000 symbols per request. If more than 1 symbol is specified, the data is merged and sorted by time. If 'ALL_SYMBOLS' or None then will select all symbols. |
| schema | Schema or str, default 'trades' | optional | The data record schema . Must be one of the values from list_schemas . |
| stype_in | SType or str, default 'raw_symbol' | optional | The symbology type of input symbols . Must be one of 'raw_symbol', 'instrument_id', 'parent', or 'continuous'. |
| stype_out | SType or str, default 'instrument_id' | optional | The symbology type of output symbols. Must be one of 'raw_symbol', 'instrument_id', 'parent', or 'continuous'. Must be a valid symbology combination with stype_in . See symbology combinations . |
| limit | int | optional | The maximum number of records to return. If None then no limit. |
| path | PathLike[str] or str | optional | The file path to stream the data to. It is recommended to use the ".dbn.zst" suffix. |

#### Returns

ADBNStoreobject.

A full list of fields for each schema is available throughHistorical.metadata.list_fields.

```python
Historical.timeseries.get_range_async(
    dataset: Dataset | str,
    start: pd.Timestamp | datetime | date | str | int,
    end: pd.Timestamp | datetime | date | str | int | None = None,
    symbols: Iterable[str | int] | str | int | None = None,
    schema: Schema | str = "trades",
    stype_in: SType | str = "raw_symbol",
    stype_out: SType | str = "instrument_id",
    limit: int | None = None,
    path: PathLike[str] | str | None = None,
) -> Awaitable[DBNStore]
```

This method is acoroutineand must be used with anawaitexpression.

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
import asyncio
import databento as db

client = db.Historical("$YOUR_API_KEY")

coro = client.timeseries.get_range_async(
    dataset="GLBX.MDP3",
    symbols=["ESM2"],
    schema="trades",
    start="2022-06-06T00:00:00",
    end="2022-06-10T00:10:00",
    limit=1,
)
data = asyncio.run(coro)

df = data.to_df()
print(df.iloc[0].to_json(indent=4))
```

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
```

```python
{
    "ts_event":1654473600070,
    "rtype":0,
    "publisher_id":1,
    "instrument_id":3403,
    "action":"T",
    "side":"A",
    "depth":0,
    "price":4108.5,
    "size":1,
    "flags":0,
    "ts_in_delta":18681,
    "sequence":157862,
    "symbol":"ESM2"
}
```

### Historical::TimeseriesGetRangeToFile

Make a streaming request for time series data from Databento.

Primary method for getting historical intraday and daily market data, instrument definitions, and market status data directly into your application.

Data is streamed directly to the file atfile_path. If the file atfile_pathalready exists, it will be overwritten.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| dataset | std::string | The dataset code (string identifier). Must be one of the values from MetadataListDatasets . Constants are provided in the databento::dataset namespace in <databento/constants.hpp> . |
| datetime_range | databento::DateTimeRange<UnixNanos> or databento::DateTimeRange<std::string> | The request range with an inclusive start and an optional exclusive end. Filters on ts_recv if it exists in the schema, otherwise ts_event . Takes an ISO 8601 string or a UNIX timestamp in nanoseconds. Assumes UTC as timezone unless otherwise specified. If not specified, end defaults to the forward filled value of start based on the resolution provided. |
| symbols | std::vector<std::string> | The product symbols to filter for. Takes up to 2,000 symbols per request. Use databento::kAllSymbols from <databento/symbology.hpp> to request all symbols. |
| schema | databento::Schema | The data record schema . Must be one of the values from MetadataListSchemas . |
| stype_in | databento::SType | The symbology type of input symbols . Defaults to RawSymbol . |
| stype_out | databento::SType | The symbology type of output symbols. Defaults to InstrumentId . Must be a valid symbology combination with stype_in . See symbology combinations . |
| limit | std::uint64_t | The maximum number of records to return. Use 0 or {} for no limit. Defaults to no limit. |
| file_path | std::filesystem::path | The path of the file where the data should be saved. If the file already exists, it will be overwritten. It is recommended to use the ".dbn.zst" suffix. |

#### Returns

ADbnStoreobject.

A full list of fields for the records read throughNextRecordorReplayfor each schema is available throughHistorical.MetadataListFieldsor the struct definitions in<databento/record.hpp>.

```python
DbnStore TimeseriesGetRangeToFile(
    const std::string& dataset,
    const DateTimeRange<UnixNanos>& datetime_range,
    const std::vector<std::string>& symbols, Schema schema,
    const std::filesystem::path& file_path);
DbnStore TimeseriesGetRangeToFile(
    const std::string& dataset,
    const DateTimeRange<std::string>& datetime_range,
    const std::vector<std::string>& symbols, Schema schema,
    const std::filesystem::path& file_path);
DbnStore TimeseriesGetRangeToFile(
    const std::string& dataset,
    const DateTimeRange<UnixNanos>& datetime_range,
    const std::vector<std::string>& symbols, Schema schema,
    SType stype_in, SType stype_out, std::uint64_t limit,
    const std::filesystem::path& file_path);
DbnStore TimeseriesGetRangeToFile(
    const std::string& dataset,
    const DateTimeRange<std::string>& datetime_range,
    const std::vector<std::string>& symbols, Schema schema,
    SType stype_in, SType stype_out, std::uint64_t limit,
    const std::filesystem::path& file_path);
```

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
18
```

```python
#include <databento/historical.hpp>
#include <iostream>

using namespace databento;

auto client =
    Historical::Builder().SetKey("$YOUR_API_KEY").Build();
auto file_bento = client.TimeseriesGetRangeToFile(
    "GLBX.MDP3", {"2022-06-06T00:00", "2022-06-10T00:10"},
    {"ESM2"}, Schema::Trades, SType::RawSymbol,
    SType::InstrumentId, 1, "ESM2_20220606-20220610.dbn.zst");
file_bento.Replay([](const Record& record) {
  // Convert the generic `Record` to a `TradeMsg`, the
  // record type associated with `Schema::Trades`
  const auto& trade_msg = record.Get<TradeMsg>();
  std::cout << trade_msg << '\n';
  return KeepGoing::Continue;
});
```

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
```

```python
TradeMsg {
    hd = RecordHeader { length = 12, rtype = mbp-0, publisher_id = 1, instrument_id = 3403, ts_event = 2022-06-06T00:00:00.070033767Z },
    price = 4108.500000000,
    size = 1,
    action = Trade,
    side = Ask,
    flags = 0,
    depth = 0,
    ts_recv = 2022-06-06T00:00:00.070314216Z,
    ts_in_delta = 18681,
    sequence = 157862
}
```

### HistoricalClient::timeseries::get_range_to_file

Makes a streaming request for time series data from Databento.

This is the primary method for getting historical market data, instrument definitions, and status data directly into your application.

This method persists the stream to a file at the given path before returning anasync decoderon that file. For large requests, consider usingbatch::submit_jobinstead.

#### Parameters

| Field | Type | Description |
| --- | --- | --- |
| params | GetRangeToFileParams | See GetRangeToFileParams for details. |

#### Returns

AnAsyncDbnDecoderobject for incrementally decoding the records from the file.

A full list of fields for each schema is available throughHistorical.metadata.list_fields.

```python
pub async fn get_range_to_file(
    &mut self,
    params: &GetRangeToFileParams,
) -> databento::Result<
    AsyncDbnDecoder<ZstdDecoder<BufReader<File>>>,
>;
```

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
18
19
20
21
22
23
24
25
26
27
28
29
```

```python
use std::num::NonZeroU64;

use databento::{
    HistoricalClient,
    dbn::{Schema, TradeMsg},
    historical::timeseries::GetRangeToFileParams,
};
use time::macros::datetime;

let mut client =
    HistoricalClient::builder().key("$YOUR_API_KEY")?.build()?;
let mut decoder = client
    .timeseries()
    .get_range_to_file(
        &GetRangeToFileParams::builder()
            .dataset("GLBX.MDP3")
            .date_time_range(
                datetime!(2022-06-06 00:00 UTC)
                    ..datetime!(2022-06-10 12:10 UTC),
            )
            .symbols("ESM2")
            .schema(Schema::Trades)
            .maybe_limit(NonZeroU64::new(1))
            .path("ESM2_20220606-20220610.dbn.zst")
            .build(),
    )
    .await?;
let trade = decoder.decode_record::<TradeMsg>().await?.unwrap();
println!("{trade:#?}");
```

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
18
```

```python
TradeMsg {
    hd: RecordHeader {
        length: 12,
        rtype: Mbp0,
        publisher_id: GlbxMdp3Glbx,
        instrument_id: 3403,
        ts_event: 1654473600070033767,
    },
    price: 4108.500000000,
    size: 1,
    action: 'T',
    side: 'A',
    flags: 0,
    depth: 0,
    ts_recv: 1654473600070314216,
    ts_in_delta: 18681,
    sequence: 157862,
}
```

## Symbology

### Historical::SymbologyResolve

Resolve a list of symbols from an inputsymbology type, to an output symbology type.

Take, for example, a raw symbol to an instrument ID:ESM2â3403.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| dataset | std::string | The dataset code (string identifier). Must be one of the values from MetadataListDatasets . Constants are provided in the databento::dataset namespace in <databento/constants.hpp> . |
| date_range | databento::DateRange | The request range with an inclusive UTC start date and an optional exclusive UTC end date. Takes YYYY-MM-DD ISO 8601 date strings. If not specified, end defaults to the forward filled value of start based on the resolution provided. |
| symbols | std::vector<std::string> | The symbols to resolve. Takes up to 2,000 symbols per request. Use databento::kAllSymbols from <databento/symbology.hpp> to request all symbols (not available for every dataset). |
| stype_in | databento::SType | The symbology type of input symbols . |
| stype_out | databento::SType | The symbology type of output symbols. Must be a valid symbology combination with stype_in . See symbology combinations . |

#### Returns

SymbologyResolution, which is defined in<databento/symbology.hpp>

The results for the symbology resolution.

Can be converted to aTsSymbolMapvia theCreateSymbolMap()method.

```python
SymbologyResolution SymbologyResolve(
    const std::string& dataset,
    const std::vector<std::string>& symbols, SType stype_in,
    SType stype_out, const DateRange& date_range);
```

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
```

```python
#include <databento/historical.hpp>
#include <iostream>

using namespace databento;

auto client =
    Historical::Builder().SetKey("$YOUR_API_KEY").Build();
auto resolution = client.SymbologyResolve(
    "GLBX.MDP3", {"ESM2"}, SType::RawSymbol, SType::InstrumentId,
    {"2022-06-01", "2022-06-30"});
std::cout << resolution << '\n';
```

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
```

```python
SymbologyResolution {
    mappings = {
        { "ESM2", { MappingInterval { start_date = 2022-06-01, end_date = 2022-06-26, symbol = "3403" } } }
    },
    partial = {},
    not_found = {},
    stype_in = raw_symbol,
    stype_out = instrument_id
}
```

### /symbology.resolve

Resolve a list of symbols from an inputsymbology type, to an output symbology type.

Take, for example, a raw symbol to an instrument ID:ESM2â3403.

#### Parameters

The following parameters should be encoded as form data (not in a JSON body).

| Parameter | Required | Description |
| --- | --- | --- |
| dataset | required | The dataset code (string identifier). Must be one of the values from list_datasets . |
| symbols | required | The symbols to resolve. Takes up to 2,000 symbols per request. Use 'ALL_SYMBOLS' to request all symbols (not available for every dataset). |
| stype_in | required | The symbology type of input symbols . Must be one of 'raw_symbol', 'instrument_id', 'parent', or 'continuous'. |
| stype_out | required | The symbology type of output symbols. Must be one of 'raw_symbol', 'instrument_id', 'parent', or 'continuous'. Must be a valid symbology combination with stype_in . See symbology combinations . |
| start_date | required | The inclusive UTC start date of the request range as an ISO 8601 date string. |
| end_date | optional | The exclusive UTC end date of the request range as an ISO 8601 date string. Defaults to the forward filled value of start based on the resolution provided. |

#### Returns

A JSON object containing symbol resolutions and any symbols or time periods for which a symbol could not be resolved.

```python
POST https://hist.databento.com/v0/symbology.resolve
```

```python
1
2
3
4
5
6
7
8
```

```python
curl -X POST 'https://hist.databento.com/v0/symbology.resolve' \
 -u $YOUR_API_KEY: \
 -d dataset=GLBX.MDP3 \
 -d symbols=ESM2 \
 -d stype_in=raw_symbol \
 -d stype_out=instrument_id \
 -d start_date='2022-06-06' \
 -d end_date='2022-06-10'
```

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
18
19
20
21
22
```

```python
{
  "result": {
    "ESM2": [
      {
        "d0": "2022-06-06",
        "d1": "2022-06-10",
        "s": "3403"
      }
    ]
  },
  "symbols": [
    "ESM2"
  ],
  "stype_in": "raw_symbol",
  "stype_out": "instrument_id",
  "start_date": "2022-06-06",
  "end_date": "2022-06-10",
  "partial": [],
  "not_found": [],
  "message": "OK",
  "status": 0
}
```

### Historical.symbology.resolve

Resolve a list of symbols from an inputsymbology type, to an output symbology type.

Take, for example, a raw symbol to an instrument ID:ESM2â3403.

#### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| dataset | Dataset or str | required | The dataset code (string identifier). Must be one of the values from list_datasets . |
| symbols | Iterable[str \| int] or str or int | required | The symbols to resolve. Takes up to 2,000 symbols per request. Use 'ALL_SYMBOLS' to request all symbols (not available for every dataset). |
| stype_in | SType or str | required | The symbology type of input symbols . Must be one of 'raw_symbol', 'instrument_id', 'parent', or 'continuous'. |
| stype_out | SType or str | required | The symbology type of output symbols. Must be one of 'raw_symbol', 'instrument_id', 'parent', or 'continuous'. Must be a valid symbology combination with stype_in . See symbology combinations . |
| start_date | date or str | required | The inclusive UTC start date of the request range as a Python date or ISO 8601 date string. |
| end_date | date or str | optional | The exclusive UTC end date of the request range as a Python date or ISO 8601 date string. Defaults to the forward filled value of start based on the resolution provided. |

#### Returns

dict[str, Any]

The results for the symbology resolution.

For more information on symbology resolution, visit oursymbology documentation.

| Field | Type | Description |
| --- | --- | --- |
| result | dict[str, list[dict[str, str]]] | The symbology mapping result. For each requested symbol, a list of symbology mappings is provided. |
| symbols | list[str] | The requested symbols. |
| stype_in | str | The requested input symbology type. |
| stype_out | str | The requested output symbology type. |
| start_date | str | The requested symbology start date as an ISO 8601 date string. |
| end_date | str | The requested symbology end date as an ISO 8601 date string. |
| partial | list[str] | The list of symbols, if any, that partially resolved inside the start date and end date interval. |
| not_found | list[str] | The list of symbols, if any, that failed to resolve inside the start date and end date interval. |
| message | str | A short message indicating the overall symbology result. Can be one of: "OK", or "Partially resolved", or "Not found" |
| status | int | A numerical status field indicating the overall symbology result. Can be one of: 0 (OK), 1 (Partially resolved), or 2 (Not found). |

```python
Historical.symbology.resolve(
    dataset: Dataset | str,
    symbols: Iterable[str | int] | str | int,
    stype_in: SType | str,
    stype_out: SType | str,
    start_date: date | str,
    end_date: date | str | None = None,
) -> dict[str, Any]
```

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
```

```python
import databento as db

client = db.Historical("$YOUR_API_KEY")

result = client.symbology.resolve(
    dataset="GLBX.MDP3",
    symbols=["ESM2"],
    stype_in="raw_symbol",
    stype_out="instrument_id",
    start_date="2022-06-01",
    end_date="2022-06-30",
)
print(result)
```

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
18
19
20
21
22
```

```python
{
    "result": {
        "ESM2": [
            {
                "d0": "2022-06-01",
                "d1": "2022-06-26",
                "s": "3403"
            }
        ]
    },
    "symbols": [
        "ESM2"
    ],
    "stype_in": "raw_symbol",
    "stype_out": "instrument_id",
    "start_date": "2022-06-01",
    "end_date": "2022-06-30",
    "partial": [],
    "not_found": [],
    "message": "OK",
    "status": 0
}
```

### HistoricalClient::symbology::resolve

Resolve a list of symbols from an inputsymbology type, to an output symbology type.

Take, for example, a raw symbol to an instrument ID:ESM2â3403.

#### Parameters

| Field | Type | Description |
| --- | --- | --- |
| params | ResolveParams | See ResolveParams for details. |

#### Returns

The results for the symbology resolution.

| Field | Type | Description |
| --- | --- | --- |
| mappings | HashMap<String, Vec<MappingInterval>> | The symbol mappings for historical data. |
| partial | Vec<String> | The symbols that did not resolve for any day in the query time range. |
| not_found | Vec<String> | The symbols that did not resolve for at least one day in the query time range. |

Can be converted to aTsSymbolMapvia theCreateSymbolMap()method.

```python
pub async fn resolve(
    &mut self,
    params: &ResolveParams,
) -> databento::Result<Resolution>;
```

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
18
19
20
21
```

```python
use databento::{
    HistoricalClient, dbn::Dataset,
    historical::symbology::ResolveParams,
};
use time::macros::date;

let mut client =
    HistoricalClient::builder().key("$YOUR_API_KEY")?.build()?;
let resolution = client
    .symbology()
    .resolve(
        &ResolveParams::builder()
            .dataset(Dataset::GlbxMdp3)
            .date_range(
                date!(2022 - 06 - 01)..date!(2022 - 06 - 30),
            )
            .symbols("ESM2")
            .build(),
    )
    .await?;
println!("{resolution:#?}");
```

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
```

```python
Resolution {
    mappings: {
        "ESM2": [
            MappingInterval {
                start_date: 2022-06-01,
                end_date: 2022-06-26,
                symbol: "3403",
            },
        ],
    },
    partial: [],
    not_found: [],
    stype_in: RawSymbol,
    stype_out: InstrumentId,
}
```

## Batch downloads

Batch downloads allow you to download flat files directly from within your portal. For more information, seeStreaming vs. batch download.

### Historical::BatchSubmitJob

Make a batch download job request for flat files.

Once a request is submitted, our system processes the request and prepares the batch files in the background. The status of your request and the files can be accessed from theDownload centerfrom your user portal.

This method takes longer than a streaming request, but is advantageous for larger requests as it supports delivery mechanisms that allow multiple accesses of the data without additional cost for each subsequent download after the first.

Related:BatchListJobs,BatchGetJobDetails.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| dataset | std::string | The dataset code (string identifier). Must be one of the values from MetadataListDatasets . Constants are provided in the databento::dataset namespace in <databento/constants.hpp> . |
| symbols | std::vector<std::string> | The product symbols to filter for. Takes up to 2,000 symbols per request. Use databento::kAllSymbols from <databento/symbology.hpp> to request all symbols. |
| schema | databento::Schema | The data record schema . Must be one of the values from MetadataListSchemas . |
| datetime_range | databento::DateTimeRange<UnixNanos> or databento::DateTimeRange<std::string> | The request range with an inclusive start and an optional exclusive end. Filters on ts_recv if it exists in the schema, otherwise ts_event . Takes an ISO 8601 string or a UNIX timestamp in nanoseconds. Assumes UTC as timezone unless otherwise specified. If not specified, end defaults to the forward filled value of start based on the resolution provided. |
| compression | databento::Compression | The data compression mode. Defaults to Zstd for fastest transfer speed. |
| pretty_px | bool | If prices should be formatted to the correct scale (using the fixed-precision scalar 1e-9). Only applicable for Csv or Json encodings. Defaults to false . |
| pretty_ts | bool | If timestamps should be formatted as ISO 8601 strings. Only applicable for Csv or Json encodings. Defaults to false . |
| map_symbols | bool | If a symbol field should be included with each text-encoded record. Only applicable for Csv or Json encodings. Defaults to false . |
| split_symbols | bool | If files should be split by raw symbol. Defaults to false . Cannot be used with limit . |
| split_duration | databento::SplitDuration | The maximum time duration before batched data is split into multiple files. A week starts on Sunday UTC. Defaults to Day . |
| split_size | std::uint64_t | The maximum size (in bytes) of each batched data file before being split. Must be an integer between 1e9 and 10e9 inclusive (1GB - 10GB). Defaults to no split size. |
| delivery | databento::Delivery | The delivery mechanism for the batched data files once processed. Only Download is supported at this time. |
| stype_in | databento::SType | The symbology type of input symbols . Defaults to RawSymbol . |
| stype_out | databento::SType | The symbology type of output symbols. Defaults to InstrumentId . Must be a valid symbology combination with stype_in . See symbology combinations . |
| limit | std::uint64_t | The maximum number of records to return. Use 0 or {} for no limit. Defaults to no limit. Cannot be used with split_symbols . |

#### Returns

BatchJob, which is defined in<databento/batch.hpp>.

The description of the submitted batch job.

| Field | Type | Description |
| --- | --- | --- |
| id | std::string | The unique job ID for the request. |
| user_id | std::string | The user ID of the user who made the request. |
| cost_usd | double | The cost of the job in US dollars. |
| dataset | std::string | The dataset code (string identifier). |
| symbols | std::vector<std::string> | The list of symbols specified in the request. |
| stype_in | SType | The symbology type of input symbols . |
| stype_out | SType | The symbology type of output symbols. |
| schema | Schema | The data record schema . |
| start | std::string | The ISO 8601 timestamp start of request time range (inclusive). |
| end | std::string | The ISO 8601 timestamp end of request time range (exclusive). |
| limit | std::uint64_t | The maximum number of records to return or 0 if there's no limit. |
| encoding | Encoding | The data encoding . |
| compression | Compression | The data compression mode. |
| pretty_px | bool | If prices are formatted to the correct scale (using the fixed-precision scalar 1e-9). |
| pretty_ts | bool | If timestamps are formatted as ISO 8601 strings. |
| map_symbols | bool | If a symbol field is included with each text-encoded record. |
| split_symbols | bool | If files are split by raw symbol. |
| split_duration | SplitDuration | The maximum time interval for an individual file before splitting into multiple files. |
| split_size | std::uint64_t | The maximum size for an individual file before splitting into multiple files. |
| delivery | Delivery | The delivery mechanism of the batch data. Only Download is supported at this time. |
| record_count | std::uint64_t | The number of data records. |
| billed_size | std::uint64_t | The size of the raw binary data used to process the batch job (used for billing purposes). |
| actual_size | std::uint64_t | The total size of the result of the batch job after splitting and compression. |
| package_size | std::uint64_t | The total size of the result of the batch job after any packaging (including metadata). |
| state | JobState | The current status of the batch job. |
| ts_received | std::string | The ISO 8601 timestamp when Databento received the batch job. |
| ts_queued | std::string | The ISO 8601 timestamp when the batch job was queued. |
| ts_process_start | std::string | The ISO 8601 timestamp when the batch job began processing (if it's begun). |
| ts_process_done | std::string | The ISO 8601 timestamp when the batch job finished processing (if it's finished). |
| ts_expiration | std::string | The ISO 8601 timestamp when the batch job will expire from the Download center . |
| progress | std::optional<std::uint8_t> | The progress percentage (0-100). Always nullopt in submit responses. |

```python
BatchJob BatchSubmitJob(
    const std::string& dataset,
    const std::vector<std::string>& symbols, Schema schema,
    const DateTimeRange<UnixNanos>& datetime_range);
BatchJob BatchSubmitJob(
    const std::string& dataset,
    const std::vector<std::string>& symbols, Schema schema,
    const DateTimeRange<std::string>& datetime_range);
BatchJob BatchSubmitJob(
    const std::string& dataset,
    const std::vector<std::string>& symbols, Schema schema,
    const DateTimeRange<UnixNanos>& datetime_range,
    Encoding encoding, Compression compression, bool pretty_px,
    bool pretty_ts, bool map_symbols, bool split_symbols,
    SplitDuration split_duration, std::uint64_t split_size,
    Delivery delivery, SType stype_in, SType stype_out,
    std::uint64_t limit);
BatchJob BatchSubmitJob(
    const std::string& dataset,
    const std::vector<std::string>& symbols, Schema schema,
    const DateTimeRange<std::string>& datetime_range,
    Encoding encoding, Compression compression, bool pretty_px,
    bool pretty_ts, bool map_symbols, bool split_symbols,
    SplitDuration split_duration, std::uint64_t split_size,
    Delivery delivery, SType stype_in, SType stype_out,
    std::uint64_t limit);
```

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
```

```python
#include <databento/historical.hpp>
#include <iostream>

using namespace databento;

auto client =
    Historical::Builder().SetKey("$YOUR_API_KEY").Build();
auto job = client.BatchSubmitJob(
    "GLBX.MDP3", {"ESM2"}, Schema::Trades,
    {"2022-06-06T12:00", "2022-06-10T00:00:00"});
std::cout << job << '\n';
```

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
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
```

```python
BatchJob {
    id = "GLBX-20260313-4C4VEQXXEN",
    user_id = "NBPDLF33",
    cost_usd = 0,
    dataset = "GLBX.MDP3",
    symbols = { "ESM2" },
    stype_in = raw_symbol,
    stype_out = instrument_id,
    schema = trades,
    start = "2022-06-06T12:00:00.000000000Z",
    end = "2022-06-10T00:00:00.000000000Z",
    limit = 0,
    encoding = dbn,
    compression = zstd,
    pretty_px = false,
    pretty_ts = false,
    map_symbols = false,
    split_duration = day,
    split_size = 0,
    split_symbols = false,
    delivery = download,
    record_count = 0,
    billed_size = 0,
    actual_size = 0,
    package_size = 0,
    state = queued,
    ts_received = "2026-03-13T23:24:10.922687000Z",
    ts_queued = "",
    ts_process_start = "",
    ts_process_done = "",
    ts_expiration = "",
    progress = nullopt
}
```

### /batch.submit_job

Make a batch download job request for flat files.

Once a request is submitted, our system processes the request and prepares the batch files in the background. The status of your request and the files can be accessed from theDownload centerfrom your user portal.

This method takes longer than a streaming request, but is advantageous for larger requests as it supports delivery mechanisms that allow multiple accesses of the data without additional cost for each subsequent download after the first.

Related:batch.list_jobs,batch.get_job_details.

#### Parameters

The following parameters should be encoded as form data (not in a JSON body).

| Parameter | Required | Description |
| --- | --- | --- |
| dataset | required | The dataset code (string identifier). Must be one of the values from list_datasets . |
| start | required | The inclusive start of the request range. Filters on ts_recv if it exists in the schema, otherwise ts_event . Takes an ISO 8601 string or UNIX timestamp in nanoseconds. Assumes UTC as timezone unless otherwise specified. |
| end | optional | The exclusive end of the request range. Filters on ts_recv if it exists in the schema, otherwise ts_event . Takes an ISO 8601 string or UNIX timestamp in nanoseconds. Assumes UTC as timezone unless otherwise specified. Defaults to the forward filled value of start based on the resolution provided. |
| symbols | optional | The product symbols to filter for. Takes up to 2,000 symbols per request. If more than 1 symbol is specified, the data is merged and sorted by time. If 'ALL_SYMBOLS' or not specified then will select all symbols. |
| schema | required | The data record schema . Must be one of the values from list_schemas . |
| encoding | required | The data encoding . Must be one of 'dbn', 'csv', 'json'. For fastest transfer speed, 'dbn' is recommended. |
| compression | optional, default 'none' | The data compression mode. Must be either 'zstd' or 'none'. For fastest transfer speed, 'zstd' is recommended. |
| stype_in | optional, default 'raw_symbol' | The symbology type of input symbols . Must be one of 'raw_symbol', 'instrument_id', 'parent', or 'continuous'. |
| stype_out | optional, default 'instrument_id' | The symbology type of output symbols. Must be one of 'raw_symbol', 'instrument_id', 'parent', or 'continuous'. Must be a valid symbology combination with stype_in . See symbology combinations . |
| limit | optional | The maximum number of records to return. Defaults to no limit. Cannot be used with split_symbols . |
| pretty_px | optional, default 'false' | If prices should be formatted to the correct scale (using the fixed-precision scalar 1e-9). Only applicable for 'csv' or 'json' encodings. Must be a boolean-like value 'true' or 'false'. |
| pretty_ts | optional, default 'false' | If timestamps should be formatted as ISO 8601 strings. Only applicable for 'csv' or 'json' encodings. Must be a boolean-like value 'true' or 'false'. |
| map_symbols | optional, default 'false' | If a symbol field should be included with each text-encoded record. Only applicable for 'csv' or 'json' encodings. Must be a boolean-like value 'true' or 'false'. |
| split_symbols | optional, default 'false' | If files should be split by raw symbol. Cannot be requested with 'ALL_SYMBOLS' . Must be a boolean-like value 'true' or 'false'. Cannot be used with limit . |
| split_duration | optional, default 'day' | The maximum time duration before batched data files are split into multiple files. Must be one of 'day', 'week', 'month', 'year', or 'none'. A week starts on Sunday UTC. |
| split_size | optional | The maximum size (in bytes) of each batched data file before being split. Must be an integer between 1e9 and 10e9 inclusive (1GB - 10GB). Defaults to no split size. |
| delivery | optional, default 'download' | The delivery mechanism for the batched data files once processed. Only 'download' is supported at this time. |

#### Returns

A JSON object containing a description of the submitted batch job.

| Field | Type | Description |
| --- | --- | --- |
| id | string | The unique job ID for the request. |
| user_id | string | The user ID of the user who made the request. |
| api_key | string or null | The API key name for the request (if Basic Auth was used). |
| cost_usd | number or null | The cost of the job in US dollars (null until the job is processed). |
| dataset | string | The dataset code (string identifier). |
| symbols | string | The list of symbols specified in the request. |
| stype_in | string | The symbology type of input symbols . |
| stype_out | string | The symbology type of output symbols. |
| schema | string | The data record schema . |
| start | string | The ISO 8601 timestamp start of request time range (inclusive). |
| end | string | The ISO 8601 timestamp end of request time range (exclusive). |
| limit | number or null | The maximum number of records to return. |
| encoding | string | The data encoding . |
| compression | string | The data compression mode. |
| pretty_px | bool | If prices are formatted to the correct scale (using the fixed-precision scalar 1e-9). |
| pretty_ts | bool | If timestamps are formatted as ISO 8601 strings. |
| map_symbols | bool | If a symbol field is included with each text-encoded record. |
| split_symbols | bool | If files are split by raw symbol. |
| split_duration | string | The maximum time interval for an individual file before splitting into multiple files. |
| split_size | number or null | The maximum size for an individual file before splitting into multiple files. |
| packaging | string or null | The archive packaging method of the batched data, one of 'none', 'zip', or 'tar' (deprecated). |
| delivery | string | The delivery mechanism of the batched data. Only 'download' is supported at this time. |
| record_count | number or null | The number of data records (null until the job is processed). |
| billed_size | number or null | The size of the raw binary data used to process the batch job (used for billing purposes). |
| actual_size | number or null | The total size of the result of the batch job after splitting and compression. |
| package_size | number or null | The total size of the result of the batch job after any packaging (including metadata). |
| state | string | The current status of the batch job. One of 'queued', 'processing', 'done', or 'expired'. |
| ts_received | string | The ISO 8601 timestamp when Databento received the batch job. |
| ts_queued | string or null | The ISO 8601 timestamp when the batch job was queued. |
| ts_process_start | string or null | The ISO 8601 timestamp when the batch job began processing (if it's begun). |
| ts_process_done | string or null | The ISO 8601 timestamp when the batch job finished processing (if it's finished). |
| ts_expiration | string or null | The ISO 8601 timestamp when the batch job will expire from the Download center . |
| progress | number or null | The progress percentage of the batch job (0-100). Always null in submit responses. |

```python
POST https://hist.databento.com/v0/batch.submit_job
```

```python
1
2
3
4
5
6
7
8
```

```python
curl -X POST 'https://hist.databento.com/v0/batch.submit_job' \
 -u $YOUR_API_KEY: \
 -d dataset=GLBX.MDP3 \
 -d symbols=ESH2 \
 -d schema=trades \
 -d start='2022-01-03' \
 -d end='2022-01-20' \
 -d encoding=dbn
```

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
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
```

```python
{
  "id": "GLBX-20220901-5DEFXVTMSM",
  "user_id": "46PCMCVF",
  "api_key": "prod-001",
  "cost_usd": null,
  "dataset": "GLBX.MDP3",
  "symbols": "ESH2",
  "stype_in": "raw_symbol",
  "stype_out": "instrument_id",
  "schema": "trades",
  "start": "2022-01-03T00:00:00.000000000Z",
  "end": "2022-01-20T00:00:00.000000000Z",
  "limit": null,
  "encoding": "dbn",
  "compression": "none",
  "pretty_px": false,
  "pretty_ts": false,
  "map_symbols": false,
  "split_symbols": false,
  "split_duration": "day",
  "split_size": null,
  "packaging": "none",
  "delivery": "download",
  "record_count": null,
  "billed_size": null,
  "actual_size": null,
  "package_size": null,
  "state": "queued",
  "ts_received": "2022-11-30T20:33:08.006406.000000000Z",
  "ts_queued": null,
  "ts_process_start": null,
  "ts_process_done": null,
  "ts_expiration": null
}
```

### Historical.batch.submit_job

Make a batch download job request for flat files.

Once a request is submitted, our system processes the request and prepares the batch files in the background. The status of your request and the files can be accessed from theDownload centerfrom your user portal.

This method takes longer than a streaming request, but is advantageous for larger requests as it supports delivery mechanisms that allow multiple accesses of the data without additional cost for each subsequent download after the first.

Related:batch.list_jobs,batch.get_job_details.

#### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| dataset | Dataset or str | required | The dataset code (string identifier). Must be one of the values from list_datasets . |
| symbols | Iterable[str \| int] or str or int | required | The product symbols to filter for. Takes up to 2,000 symbols per request. If more than 1 symbol is specified, the data is merged and sorted by time. If 'ALL_SYMBOLS' then will select all symbols. |
| schema | Schema or str | required | The data record schema . Must be one of the values from list_schemas . |
| start | pd.Timestamp, datetime, date, str, or int | required | The inclusive start of the request range. Filters on ts_recv if it exists in the schema, otherwise ts_event . Takes pd.Timestamp , Python datetime , Python date , ISO 8601 string, or UNIX timestamp in nanoseconds. Assumes UTC as timezone unless otherwise specified. |
| end | pd.Timestamp, datetime, date, str, or int | optional | The exclusive end of the request range. Filters on ts_recv if it exists in the schema, otherwise ts_event . Takes pd.Timestamp , Python datetime , Python date , ISO 8601 string, or UNIX timestamp in nanoseconds. Assumes UTC as timezone unless otherwise specified. Defaults to the forward filled value of start based on the resolution provided. |
| encoding | Encoding or str | optional | The data encoding . Must be one of 'dbn', 'csv', 'json'. For fastest transfer speed, 'dbn' is recommended. |
| compression | Compression or str | optional | The data compression mode. Must be either 'zstd', 'none', or None. For fastest transfer speed, 'zstd' is recommended. |
| pretty_px | bool, default False | optional | If prices should be formatted to the correct scale (using the fixed-precision scalar 1e-9). Only applicable for 'csv' or 'json' encodings. |
| pretty_ts | bool, default False | optional | If timestamps should be formatted as ISO 8601 strings. Only applicable for 'csv' or 'json' encodings. |
| map_symbols | bool | optional | If a symbol field should be included with each text-encoded record. If None , will default to True for csv and json encodings and False for dbn . |
| split_symbols | bool, default False | optional | If files should be split by raw symbol. Cannot be requested with 'ALL_SYMBOLS' . Cannot be used with limit . |
| split_duration | Duration or str, default 'day' | optional | The maximum time duration before batched data is split into multiple files. Must be one of 'day', 'week', 'month', 'year', or 'none'. A week starts on Sunday UTC. |
| split_size | int | optional | The maximum size (in bytes) of each batched data file before being split. Must be an integer between 1e9 and 10e9 inclusive (1GB - 10GB). Defaults to no split size. |
| delivery | Delivery or str, default 'download' | optional | The delivery mechanism for the batched data files once processed. Only 'download' is supported at this time. |
| stype_in | SType or str, default 'raw_symbol' | optional | The symbology type of input symbols . Must be one of 'raw_symbol', 'instrument_id', 'parent', or 'continuous'. |
| stype_out | SType or str, default 'instrument_id' | optional | The symbology type of output symbols. Must be one of 'raw_symbol', 'instrument_id', 'parent', or 'continuous'. Must be a valid symbology combination with stype_in . See symbology combinations . |
| limit | int | optional | The maximum number of records to return. If None then no limit. Cannot be used with split_symbols . |

#### Returns

dict[str, Any]

The description of the submitted batch job.

| Field | Type | Description |
| --- | --- | --- |
| id | str | The unique job ID for the request. |
| user_id | str | The user ID of the user who made the request. |
| api_key | str or None | The API key name for the request (if Basic Auth was used). |
| cost_usd | float or None | The cost of the job in US dollars ( None until the job is done processing). |
| dataset | str | The dataset code (string identifier). |
| symbols | str | The list of symbols specified in the request. |
| stype_in | str | The symbology type of input symbols . |
| stype_out | str | The symbology type of output symbols. |
| schema | str | The data record schema . |
| start | str | The ISO 8601 timestamp start of request time range (inclusive). |
| end | str | The ISO 8601 timestamp end of request time range (exclusive). |
| limit | int or None | The maximum number of records to return. |
| encoding | str | The data encoding . |
| compression | str | The data compression mode. |
| pretty_px | bool | If prices are formatted to the correct scale (using the fixed-precision scalar 1e-9). |
| pretty_ts | bool | If timestamps are formatted as ISO 8601 strings. |
| map_symbols | bool | If a symbol field is included with each text-encoded record. |
| split_symbols | bool | If files are split by raw symbol. |
| split_duration | str | The maximum time interval for an individual file before splitting into multiple files. |
| split_size | int or None | The maximum size for an individual file before splitting into multiple files. |
| packaging | str or None | The packaging method of the batch data, one of 'none', 'zip', or 'tar' (deprecated). |
| delivery | str | The delivery mechanism of the batch data. Only 'download' is supported at this time. |
| record_count | int or None | The number of data records ( None until the job is processed). |
| billed_size | int or None | The size of the raw binary data used to process the batch job (used for billing purposes). |
| actual_size | int or None | The total size of the result of the batch job after splitting and compression. |
| package_size | int or None | The total size of the result of the batch job after any packaging (including metadata). |
| state | str | The current status of the batch job. One of 'queued', 'processing', 'done', or 'expired'. |
| ts_received | str | The ISO 8601 timestamp when Databento received the batch job. |
| ts_queued | str or None | The ISO 8601 timestamp when the batch job was queued. |
| ts_process_start | str or None | The ISO 8601 timestamp when the batch job began processing (if it's begun). |
| ts_process_done | str or None | The ISO 8601 timestamp when the batch job finished processing (if it's finished). |
| ts_expiration | str or None | The ISO 8601 timestamp when the batch job will expire from the Download center . |
| progress | int or None | The progress percentage (0-100). Always None in submit responses. |

```python
Historical.batch.submit_job(
    dataset: Dataset | str,
    symbols: Iterable[str | int] | str | int,
    schema: Schema | str,
    start: pd.Timestamp | datetime | date | str | int,
    end: pd.Timestamp | datetime | date | str | int | None = None,
    encoding: Encoding | str = "dbn",
    compression: Compression | str = "zstd",
    pretty_px: bool = False,
    pretty_ts: bool = False,
    map_symbols: bool | None = None,
    split_symbols: bool = False,
    split_duration: Duration | str = "day",
    split_size: int | None = None,
    delivery: Delivery | str = "download",
    stype_in: SType | str = "raw_symbol",
    stype_out: SType | str = "instrument_id",
    limit: int | None = None,
) -> dict[str, Any]
```

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
```

```python
import databento as db

client = db.Historical("$YOUR_API_KEY")

details = client.batch.submit_job(
    dataset="GLBX.MDP3",
    symbols=["ESM2"],
    schema="trades",
    encoding="dbn",
    start="2022-06-06T12:00:00+00:00",
    end="2022-06-10T00:00:00+00:00",
)
print(details)
```

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
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
```

```python
{
    "id": "GLBX-20221217-MN5S5S4WAS",
    "user_id": "NBPDLF33",
    "api_key": "prod-001",
    "cost_usd": None,
    "dataset": "GLBX.MDP3",
    "symbols": "ESM2",
    "stype_in": "raw_symbol",
    "stype_out": "instrument_id",
    "schema": "trades",
    "start": "2022-06-06T12:00:00.000000000Z",
    "end": "2022-06-10T00:00:00.000000000Z",
    "limit": None,
    "encoding": "dbn",
    "compression": "zstd",
    "pretty_px": False,
    "pretty_ts": False,
    "map_symbols": False,
    "split_symbols": False,
    "split_duration": "day",
    "split_size": None,
    "packaging": None,
    "delivery": "download",
    "record_count": None,
    "billed_size": None,
    "actual_size": None,
    "package_size": None,
    "state": "queued",
    "ts_received": "2022-12-17T00:36:37.844913000Z",
    "ts_queued": None,
    "ts_process_start": None,
    "ts_process_done": None,
    "ts_expiration": None
}
```

### HistoricalClient::batch::submit_job

Make a batch download job request for flat files.

Once a request is submitted, our system processes the request and prepares the batch files in the background. The status of your request and the files can be accessed from theDownload centerfrom your user portal or downloaded withbatch::download.

This method takes longer than a streaming request, but is advantageous for larger requests as it supports delivery mechanisms that allow multiple accesses of the data without additional cost for each subsequent download after the first.

Related:batch::list_jobs,batch::get_job_details.

#### Parameters

| Field | Type | Description |
| --- | --- | --- |
| params | SubmitJobParams | See SubmitJobParams for details. |

#### Returns

The description of the submitted batch job.

| Field | Type | Description |
| --- | --- | --- |
| id | String | The unique job ID for the request. |
| user_id | Option<String> | The user ID of the user who made the request. |
| cost_usd | Option<f64> | The cost of the job in US dollars ( None until the job is done processing). |
| dataset | String | The dataset code (string identifier). |
| symbols | Symbols | The list of symbols specified in the request. |
| stype_in | SType | The symbology type of input symbols . |
| stype_out | SType | The symbology type of output symbols. |
| schema | Schema | The data record schema . |
| start | time::OffsetDateTime | The inclusive UTC timestamp start of request time range. |
| end | time::OffsetDateTime | The exclusive UTC timestamp end of request time range. |
| limit | Option<NonZeroU64> | The maximum number of records to return. |
| encoding | Encoding | The data encoding . |
| compression | Compression | The data compression mode. |
| pretty_px | bool | If prices are formatted to the correct scale (using the fixed-precision scalar 1e-9). |
| pretty_ts | bool | If timestamps are formatted as ISO 8601 strings. |
| map_symbols | bool | If a symbol field is included with each text-encoded record. |
| split_symbols | bool | If files are split by raw symbol. |
| split_duration | SplitDuration | The maximum time interval for an individual file before splitting into multiple files. None means no time-based splitting. Defaults to Day . |
| split_size | Option<NonZeroU64> | The maximum size for an individual file before splitting into multiple files. |
| delivery | Delivery | The delivery mechanism of the batch data. Only Download is supported at this time. |
| record_count | Option<u64> | The number of data records ( None until the job is processed). |
| billed_size | Option<u64> | The size of the raw binary data used to process the batch job (used for billing purposes). |
| actual_size | Option<u64> | The total size of the result of the batch job after splitting and compression. |
| package_size | Option<u64> | The total size of the result of the batch job after any packaging (including metadata). |
| state | JobState. | The current status of the batch job. |
| ts_received | time::OffsetDateTime | The UTC timestamp when Databento received the batch job. |
| ts_queued | Option<time::OffsetDateTime> | The UTC timestamp when the batch job was queued. |
| ts_process_start | Option<time::OffsetDateTime> | The UTC timestamp when the batch job began processing (if it's begun). |
| ts_process_done | Option<time::OffsetDateTime> | The UTC timestamp when the batch job finished processing (if it's finished). |
| ts_expiration | Option<time::OffsetDateTime> | The UTC timestamp when the batch job will expire from the Download center . |
| progress | Option<u8> | The progress percentage (0-100). Always None in submit responses. |

```python
pub async fn submit_job(
    &mut self,
    params: &SubmitJobParams,
) -> databento::Result<BatchJob>;
```

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
18
19
20
21
22
23
```

```python
use databento::{
    HistoricalClient, dbn::Schema,
    historical::batch::SubmitJobParams,
};
use time::macros::datetime;

let mut client =
    HistoricalClient::builder().key("$YOUR_API_KEY")?.build()?;
let job = client
    .batch()
    .submit_job(
        &SubmitJobParams::builder()
            .dataset("GLBX.MDP3")
            .date_time_range(
                datetime!(2022-06-06 12:00 UTC)
                    ..datetime!(2022-06-10 00:00 UTC),
            )
            .symbols("ESM2")
            .schema(Schema::Trades)
            .build(),
    )
    .await?;
println!("{job:#?}");
```

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
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
```

```python
BatchJob {
    id: "GLBX-20220720-BTW9J5HY5C",
    user_id: Some(
        "46PCMCVF",
    ),
    cost_usd: None,
    dataset: "GLBX.MDP3",
    symbols: Symbols(
        [
            "ESM2",
        ],
    ),
    stype_in: RawSymbol,
    stype_out: InstrumentId,
    schema: Trades,
    start: 2022-06-06 12:00:00.0 +00:00:00,
    end: 2022-06-10 0:00:00.0 +00:00:00,
    limit: None,
    encoding: Dbn,
    compression: Zstd,
    pretty_px: false,
    pretty_ts: false,
    map_symbols: false,
    split_duration: Some(Day),
    split_size: None,
    delivery: Download,
    record_count: None,
    billed_size: None,
    actual_size: None,
    package_size: None,
    state: Queued,
    ts_received: 2023-07-28 21:44:15.77437 +00:00:00,
    ts_queued: None,
    ts_process_start: None,
    ts_process_done: None,
    ts_expiration: None,
    progress: None,
}
```

### Historical::BatchListJobs

The response format of this endpoint was changed on 2026-09-29. As of version 0.66.0, these methods request the new short response format. For information about this change, see thisannouncement.

List batch jobs for the user account. Returns the short form of each job, which only contains theid,state, andts_receivedfields.

The job details will be sorted in order ofts_received.

To obtain the full details for a job, usebatch.get_job_details, which returns the full set of fields for a single job.

Related:Download center.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| states | std::vector<JobState> | The filter for job states as a list of comma separated values. Can include Queued , Processing , Done , and Expired . Defaults to all except Expired . |
| since | UnixNanos or std::string | The filter for timestamp submitted (will not include jobs prior to this). Takes an ISO 8601 string or a UNIX timestamp in nanoseconds. Assumes UTC as timezone unless otherwise specified. |

#### Returns

std::vector<databento::BatchJobShort>

A list of short-form batch job details.

#### Full response

The deprecatedBatchListJobsFullmethods return the full job details, asBatchListJobsdid prior to version 0.66.0. Thebatch.list_jobsendpoint will stop returning full job details on 2026-10-27, after which these methods will no longer work and will be removed.

```python
1
2
3
4
5
```

```python
std::vector<BatchJob> BatchListJobsFull();
std::vector<BatchJob> BatchListJobsFull(
    const std::vector<JobState>& states, UnixNanos since);
std::vector<BatchJob> BatchListJobsFull(
    const std::vector<JobState>& states, const std::string& since);
```

```python
std::vector<BatchJobShort> BatchListJobs();
std::vector<BatchJobShort> BatchListJobs(
    const std::vector<JobState>& states, UnixNanos since);
std::vector<BatchJobShort> BatchListJobs(
    const std::vector<JobState>& states, const std::string& since);
```

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
```

```python
#include <databento/historical.hpp>
#include <iostream>

using namespace databento;

auto client =
    Historical::Builder().SetKey("$YOUR_API_KEY").Build();
auto jobs = client.BatchListJobs(
    {JobState::Queued, JobState::Processing, JobState::Done},
    "2022-06-01");
for (const BatchJobShort& job : jobs) {
  std::cout << job << '\n';
}
```

```python
1
2
3
4
5
6
```

```python
BatchJobShort {
    id = "GLBX-20240509-T473UFYPSK",
    state = done,
    ts_received = "2024-05-09T00:20:45.473577000Z"
}
...
```

### /batch.list_jobs

The response format of this endpoint was changed on 2026-09-29. Users can obtain the deprecated response format by specifyingshort=falseuntil 2026-10-27. For information about this change, see thisannouncement.

List batch job details for the user account.

The job details will be sorted in order ofts_received.

To obtain the full details for a job, usebatch.get_job_details, which returns the full set of fields for a single job.

Related:Download center.

#### Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| states | optional, default 'queued,processing,done,expired' | The filter for job states as a list of comma separated values. Can include 'queued', 'processing', 'done', and 'expired'. Defaults to all except 'expired'. |
| since | optional | The filter for timestamp submitted (will not include jobs prior to this). Takes an ISO 8601 string or UNIX timestamp in nanoseconds. Assumes UTC as timezone unless otherwise specified. |
| short | optional, default 'true' | If 'false', return the deprecated long form response for each job, which includes all job fields reported by batch.get_job_details . |

#### Returns

A list of JSON objects containing batch job details.

| Field | Type | Description |
| --- | --- | --- |
| id | string | The unique job ID for the request. |
| state | string | The current status of the batch job. One of 'queued', 'processing', 'done', or 'expired'. |
| ts_received | string | The ISO 8601 timestamp when Databento received the batch job. |

```python
GET https://hist.databento.com/v0/batch.list_jobs
```

```python
1
2
3
4
```

```python
curl -G 'https://hist.databento.com/v0/batch.list_jobs' \
 -u $YOUR_API_KEY: \
 -d states=queued,processing,done \
 -d since='20220601T00:00:00'
```

```python
1
2
3
4
5
6
7
8
```

```python
[
  {
    "id": "GLBX-20220901-5DEFXVTMSM",
    "state": "queued",
    "ts_received": "2022-11-30T20:33:08.006406000Z"
  },
  ...
]
```

### Historical.batch.list_jobs

The response format of this endpoint was changed on 2026-09-29. Users can obtain the deprecated response format by specifyingshort=Falseuntil 2026-10-27. For information about this change, see thisannouncement.

List batch job details for the user account.

The job details will be sorted in order ofts_received.

To obtain the full details for a job, usebatch.get_job_details, which returns the full set of fields for a single job.

Related:Download center.

#### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| states | Iterable[JobState \| str] or JobState or str | optional | The filter for job states as a list of comma separated values. Can include 'queued', 'processing', 'done', and 'expired'. Defaults to all except 'expired'. |
| since | pd.Timestamp, datetime, date, str, or int | optional | The filter for timestamp submitted (will not include jobs prior to this). Takes pd.Timestamp , Python datetime , Python date , ISO 8601 string, or UNIX timestamp in nanoseconds. Assumes UTC as timezone unless otherwise specified. |
| short | bool | optional | If False, return the deprecated long form response for each job, which includes all job fields reported by batch.get_job_details . Defaults to the short form. |

#### Returns

list[dict[str, Any]]

A list of batch job details.

| Field | Type | Description |
| --- | --- | --- |
| id | str | The unique job ID for the request. |
| state | str | The current status of the batch job. One of 'queued', 'processing', 'done', or 'expired'. |
| ts_received | str | The ISO 8601 timestamp when Databento received the batch job. |

```python
Historical.batch.list_jobs(
    states: Iterable[JobState | str] | JobState | str | None = "queued,processing,done",
    since: pd.Timestamp | datetime | date | str | int | None = None,
    short: bool | None = None,
) -> list[dict[str, Any]]
```

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
```

```python
import databento as db

client = db.Historical("$YOUR_API_KEY")

jobs = client.batch.list_jobs(
    states=["queued", "processing", "done"],
    since="2022-06-01",
)
print(jobs)
```

```python
1
2
3
4
5
6
7
```

```python
[
    {
        "id": "GLBX-20221126-DBVXWPJJQN",
        "state": "done",
        "ts_received": "2022-11-26T09:23:17.519708000Z"
    },
...
```

### HistoricalClient::batch::list_jobs

The response format of this endpoint was changed on 2026-09-29. As of version 0.60.0, this method requests the new short response format. For information about this change, see thisannouncement.

List batch jobs for the user account. Returns the short form of each job, which only contains theid,state, andts_receivedfields.

The job details will be sorted in order ofts_received.

To obtain the full details for a job, usebatch.get_job_details, which returns the full set of fields for a single job.

Related:Download center.

#### Parameters

| Field | Type | Description |
| --- | --- | --- |
| params | ListJobsParams | See ListJobsParams for details. |

#### Returns

Vec<BatchJobShort>

A list of short-form batch job details.

#### Full response

The deprecatedlist_jobs_fullmethod returns the full job details, aslist_jobsdid prior to version 0.60.0. Thebatch.list_jobsendpoint will stop returning full job details on 2026-10-27, after which this method will no longer work and will be removed.

```python
1
2
3
4
```

```python
pub async fn list_jobs_full(
    &mut self,
    params: &ListJobsParams,
) -> databento::Result<Vec<BatchJob>>;
```

```python
pub async fn list_jobs(
    &mut self,
    params: &ListJobsParams,
) -> databento::Result<Vec<BatchJobShort>>;
```

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
18
19
20
21
22
```

```python
use databento::{
    HistoricalClient,
    historical::batch::{JobState, ListJobsParams},
};
use time::macros::datetime;

let mut client =
    HistoricalClient::builder().key("$YOUR_API_KEY")?.build()?;
let jobs = client
    .batch()
    .list_jobs(
        &ListJobsParams::builder()
            .states(vec![
                JobState::Queued,
                JobState::Processing,
                JobState::Done,
            ])
            .since(datetime!(2025-01-01 00:00 UTC))
            .build(),
    )
    .await?;
println!("{jobs:#?}");
```

```python
1
2
3
4
5
6
7
8
```

```python
[
    BatchJobShort {
        id: "XNAS-20230704-NMN5T38NUD",
        state: Done,
        ts_received: 2023-07-04 12:22:30.06656 +00:00:00,
    },
    ...
]
```

### Historical::BatchListFiles

List files for a batch job.

This will include all data files andsupport files.

Related:Download center.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| job_id | std::string | The batch job identifier. |

#### Returns

std::vector<BatchFileDesc>, whereBatchFileDescis defined in<databento/batch.hpp>.

The file details for the batch job.

| Field | Type | Description |
| --- | --- | --- |
| filename | std::string | The file name. |
| size | std::uint64_t | The size of the file in bytes. |
| hash | std::string | The SHA256 hash of the file. |
| https_url | std::string | The URL for the HTTPS download. |
| ftp_url | std::string | The URL for the FTP download. |

```python
std::vector<BatchFileDesc> BatchListFiles(
    const std::string& job_id);
```

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
```

```python
#include <databento/historical.hpp>
#include <iostream>

using namespace databento;

auto client =
    Historical::Builder().SetKey("$YOUR_API_KEY").Build();
auto files = client.BatchListFiles("XNAS-20250108-VVS57U5PD8");
for (const BatchFileDesc& file : files) {
  std::cout << file << '\n';
}
```

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
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
```

```python
BatchFileDesc {
    filename = "manifest.json",
    size = 1889,
    hash = "sha256:9f43e431be88c403e73ce244bb2e94b293c9c05ac74d93a00443311fc0c9ef09",
    https_url = "https://api.databento.com/v0/batch/download/NBPDLF33/XNAS-20250108-VVS57U5PD8/manifest.json",
    ftp_url = "ftp://ftp.databento.com/NBPDLF33/XNAS-20250108-VVS57U5PD8/manifest.json"
}
BatchFileDesc {
    filename = "condition.json",
    size = 122,
    hash = "sha256:43dba9f90ba29334f233de4f76541f3d78f5378ed4baff0227673a680fde95d7",
    https_url = "https://api.databento.com/v0/batch/download/NBPDLF33/XNAS-20250108-VVS57U5PD8/condition.json",
    ftp_url = "ftp://ftp.databento.com/NBPDLF33/XNAS-20250108-VVS57U5PD8/condition.json"
}
BatchFileDesc {
    filename = "metadata.json",
    size = 699,
    hash = "sha256:001a0e2b8e285875b8f1ac1aa5fa3dfadc39b4b92f664b12d99734c6a1bae148",
    https_url = "https://api.databento.com/v0/batch/download/NBPDLF33/XNAS-20250108-VVS57U5PD8/metadata.json",
    ftp_url = "ftp://ftp.databento.com/NBPDLF33/XNAS-20250108-VVS57U5PD8/metadata.json"
}
BatchFileDesc {
    filename = "symbology.json",
    size = 1753497,
    hash = "sha256:3f3908205ec8b24def7cb3589d9f1be523ec64b4ac63be1c706d8dfca2051d78",
    https_url = "https://api.databento.com/v0/batch/download/NBPDLF33/XNAS-20250108-VVS57U5PD8/symbology.json",
    ftp_url = "ftp://ftp.databento.com/NBPDLF33/XNAS-20250108-VVS57U5PD8/symbology.json"
}
BatchFileDesc {
    filename = "xnas-itch-20250106.imbalance.dbn.zst",
    size = 88237480,
    hash = "sha256:7d0945aa1f04dad3e263237dcbdb7529ce7f0f41d902e468bb99d686754ce599",
    https_url = "https://api.databento.com/v0/batch/download/NBPDLF33/XNAS-20250108-VVS57U5PD8/xnas-itch-20250106.imbalance.dbn.zst",
    ftp_url = "ftp://ftp.databento.com/NBPDLF33/XNAS-20250108-VVS57U5PD8/xnas-itch-20250106.imbalance.dbn.zst"
}
```

### /batch.list_files

List files for a batch job.

This will include all data files andsupport files.

Related:Download center.

#### Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| job_id | required | The batch job identifier. |

#### Returns

A list of JSON objects containing file details for the batch job.

| Field | Type | Description |
| --- | --- | --- |
| filename | string | The file name. |
| size | number | The size of the file in bytes. |
| hash | string | The SHA256 hash of the file. |
| urls | object | A map of download protocol to URL. |

```python
GET https://hist.databento.com/v0/batch.list_files
```

```python
1
2
3
```

```python
curl -G 'https://hist.databento.com/v0/batch.list_files' \
 -u $YOUR_API_KEY: \
 -d job_id=GLBX-20220610-5DEFXVTMSM
```

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
18
19
20
```

```python
[
  {
    "filename": "metadata.json",
    "size": 1102,
    "hash": "sha256:0168d53e1705b69b1d6407f10bb3ab48aac492fa0f68f863cc9b092931cc67a7",
    "urls": {
      "https": "https://api.databento.com/v0/batch/download/46PCMCVF/GLBX-20230203-WF9WJYSCDU/metadata.json",
      "ftp": "ftp://ftp.databento.com/46PCMCVF/GLBX-20230203-WF9WJYSCDU/metadata.json"
    }
  },
  {
    "filename": "glbx-mdp3-20220610.mbo.csv.zst",
    "size": 21832,
    "hash": "sha256:1218930af153b4953632216044ef87607afa467fc7ab7fbb1f031fceacf9d52a",
    "urls": {
      "https": "https://api.databento.com/v0/batch/download/46PCMCVF/GLBX-20230203-WF9WJYSCDU/glbx-mdp3-20220610.mbo.csv.zst",
      "ftp": "ftp://ftp.databento.com/46PCMCVF/GLBX-20230203-WF9WJYSCDU/glbx-mdp3-20220610.mbo.csv.zst"
    }
  }
]
```

### Historical.batch.list_files

List files for a batch job.

This will include all data files andsupport files.

Related:Download center.

#### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| job_id | str | required | The batch job identifier. |

#### Returns

list[dict[str, Any]]

The file details for the batch job.

| Field | Type | Description |
| --- | --- | --- |
| filename | str | The file name. |
| size | int | The size of the file in bytes. |
| hash | str | The SHA256 hash of the file. |
| urls | dict | A map of download protocol to URL. |

```python
Historical.batch.list_files(
    job_id: str,
) -> list[dict[str, Any]]
```

```python
1
2
3
4
5
6
```

```python
import databento as db

client = db.Historical("$YOUR_API_KEY")

files = client.batch.list_files(job_id="GLBX-20220610-5DEFXVTMSM")
print(files)
```

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
18
19
20
```

```python
[
    {
        "filename": "metadata.json",
        "size": 1102,
        "hash": "sha256:0168d53e1705b69b1d6407f10bb3ab48aac492fa0f68f863cc9b092931cc67a7",
        "urls": {
            "https": "https://api.databento.com/v0/batch/download/46PCMCVF/GLBX-20230203-WF9WJYSCDU/metadata.json",
            "ftp": "ftp://ftp.databento.com/46PCMCVF/GLBX-20230203-WF9WJYSCDU/metadata.json",
        }
    },
    {
        "filename": "glbx-mdp3-20220610.mbo.csv.zst",
        "size": 21832,
        "hash": "sha256:1218930af153b4953632216044ef87607afa467fc7ab7fbb1f031fceacf9d52a",
        "urls": {
            "https": "https://api.databento.com/v0/batch/download/46PCMCVF/GLBX-20230203-WF9WJYSCDU/glbx-mdp3-20220610.mbo.csv.zst",
            "ftp": "ftp://ftp.databento.com/46PCMCVF/GLBX-20230203-WF9WJYSCDU/glbx-mdp3-20220610.mbo.csv.zst",
        }
    }
]
```

### HistoricalClient::batch::list_files

List files for a batch job.

This will include all data files andsupport files.

Related:Download center.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| job_id | &str | The batch job identifier. |

#### Returns

Vec<BatchFileDesc>

The file details for the batch job.

| Field | Type | Description |
| --- | --- | --- |
| filename | String | The file name. |
| size | u64 | The size of the file in bytes. |
| hash | String | The SHA256 hash of the file. |
| urls | HashMap<String, String> | A map of download protocol to URL. |

```python
pub async fn list_files(
    &mut self,
    job_id: &str,
) -> databento::Result<Vec<BatchFileDesc>>;
```

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
```

```python
use databento::HistoricalClient;
use time::macros::date;

let mut client =
    HistoricalClient::builder().key("$YOUR_API_KEY")?.build()?;
let files = client
    .batch()
    .list_files("XNAS-20250108-VVS57U5PD8")
    .await?;
println!("{files:#?}");
```

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
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
```

```python
[
    BatchFileDesc {
        filename: "manifest.json",
        size: 1889,
        hash: "sha256:9f43e431be88c403e73ce244bb2e94b293c9c05ac74d93a00443311fc0c9ef09",
        urls: {
            "https": "https://api.databento.com/v0/batch/download/NBPDLF33/XNAS-20250108-VVS57U5PD8/manifest.json",
            "ftp": "ftp://ftp.databento.com/NBPDLF33/XNAS-20250108-VVS57U5PD8/manifest.json",
        },
    },
    BatchFileDesc {
        filename: "condition.json",
        size: 122,
        hash: "sha256:43dba9f90ba29334f233de4f76541f3d78f5378ed4baff0227673a680fde95d7",
        urls: {
            "ftp": "ftp://ftp.databento.com/NBPDLF33/XNAS-20250108-VVS57U5PD8/condition.json",
            "https": "https://api.databento.com/v0/batch/download/NBPDLF33/XNAS-20250108-VVS57U5PD8/condition.json",
        },
    },
    BatchFileDesc {
        filename: "metadata.json",
        size: 699,
        hash: "sha256:001a0e2b8e285875b8f1ac1aa5fa3dfadc39b4b92f664b12d99734c6a1bae148",
        urls: {
            "https": "https://api.databento.com/v0/batch/download/NBPDLF33/XNAS-20250108-VVS57U5PD8/metadata.json",
            "ftp": "ftp://ftp.databento.com/NBPDLF33/XNAS-20250108-VVS57U5PD8/metadata.json",
        },
    },
    BatchFileDesc {
        filename: "symbology.json",
        size: 1753497,
        hash: "sha256:3f3908205ec8b24def7cb3589d9f1be523ec64b4ac63be1c706d8dfca2051d78",
        urls: {
            "https": "https://api.databento.com/v0/batch/download/NBPDLF33/XNAS-20250108-VVS57U5PD8/symbology.json",
            "ftp": "ftp://ftp.databento.com/NBPDLF33/XNAS-20250108-VVS57U5PD8/symbology.json",
        },
    },
    BatchFileDesc {
        filename: "xnas-itch-20250106.imbalance.dbn.zst",
        size: 88237480,
        hash: "sha256:7d0945aa1f04dad3e263237dcbdb7529ce7f0f41d902e468bb99d686754ce599",
        urls: {
            "https": "https://api.databento.com/v0/batch/download/NBPDLF33/XNAS-20250108-VVS57U5PD8/xnas-itch-20250106.imbalance.dbn.zst",
            "ftp": "ftp://ftp.databento.com/NBPDLF33/XNAS-20250108-VVS57U5PD8/xnas-itch-20250106.imbalance.dbn.zst",
        },
    },
]
```

### Historical::BatchGetJobDetails

Get the full job details of a batch job.

Related:Download center.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| job_id | std::string | The batch job ID. This can be found in the download center . |

#### Returns

BatchJob, whereBatchJobis defined in<databento/batch.hpp>.

The batch job details. Seebatch.submit_jobfor a detailed list of returned values.

```python
BatchJob BatchGetJobDetails(
    const std::string& job_id);
```

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
```

```python
#include <databento/historical.hpp>
#include <iostream>

using namespace databento;

auto client =
    Historical::Builder().SetKey("$YOUR_API_KEY").Build();
auto job = client.BatchGetJobDetails("GLBX-20240509-T473UFYPSK");

std::cout << job << '\n';
```

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
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
```

```python
BatchJob {
    id = "GLBX-20240509-T473UFYPSK",
    user_id = "NBPDLF33",
    cost_usd = 0.015481,
    dataset = "GLBX.MDP3",
    symbols = { "OZN.OPT" },
    stype_in = parent,
    stype_out = instrument_id,
    schema = trades,
    start = "2022-12-12T00:00:00.000000000Z",
    end = "2022-12-17T00:00:00.000000000Z",
    limit = 0,
    encoding = dbn,
    compression = zstd,
    pretty_px = false,
    pretty_ts = false,
    map_symbols = false,
    split_duration = day,
    split_size = 0,
    split_symbols = false,
    delivery = download,
    record_count = 12368,
    billed_size = 593664,
    actual_size = 458219,
    package_size = 1019169,
    state = done,
    ts_received = "2024-05-09T00:20:45.473577000Z",
    ts_queued = "2024-05-09T00:20:47.037110000Z",
    ts_process_start = "2024-05-09T00:20:55.593991000Z",
    ts_process_done = "2024-05-09T00:21:25.354614000Z",
    ts_expiration = "2024-06-08T00:21:25.354614000Z",
    progress = 100
}
```

### /batch.get_job_details

Get the full job details of a batch job.

Related:Download center.

#### Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| job_id | required | The batch job ID. This can be found in the download center . |

#### Returns

A JSON object containing the job details.

| Field | Type | Description |
| --- | --- | --- |
| id | string | The unique job ID for the request. |
| user_id | string | The user ID of the user who made the request. |
| api_key | string or null | The API key name for the request (if Basic Auth was used). |
| cost_usd | number or null | The cost of the job in US dollars (null until the job is processed). |
| dataset | string | The dataset code (string identifier). |
| symbols | string | The list of symbols specified in the request. |
| stype_in | string | The symbology type of input symbols . |
| stype_out | string | The symbology type of output symbols. |
| schema | string | The data record schema . |
| start | string | The ISO 8601 timestamp start of request time range (inclusive). |
| end | string | The ISO 8601 timestamp end of request time range (exclusive). |
| limit | number or null | The maximum number of records to return. |
| encoding | string | The data encoding . |
| compression | string | The data compression mode. |
| pretty_px | bool | If prices are formatted to the correct scale (using the fixed-precision scalar 1e-9). |
| pretty_ts | bool | If timestamps are formatted as ISO 8601 strings. |
| map_symbols | bool | If a symbol field is included with each text-encoded record. |
| split_symbols | bool | If files are split by raw symbol. |
| split_duration | string | The maximum time interval for an individual file before splitting into multiple files. |
| split_size | number or null | The maximum size for an individual file before splitting into multiple files. |
| packaging | string or null | The packaging method of the batch data, one of 'none', 'zip', or 'tar' (deprecated). |
| delivery | string | The delivery mechanism of the batch data, one of 'download', 's3', or 'disk'. |
| record_count | number or null | The number of data records (null until the job is processed). |
| billed_size | number or null | The size of the raw binary data used to process the batch job (used for billing purposes). |
| actual_size | number or null | The total size of the result of the batch job after splitting and compression. |
| package_size | number or null | The total size of the result of the batch job after any packaging (including metadata). |
| state | string | The current status of the batch job. One of 'queued', 'processing', 'done', or 'expired'. |
| ts_received | string | The ISO 8601 timestamp when Databento received the batch job. |
| ts_queued | string or null | The ISO 8601 timestamp when the batch job was queued. |
| ts_process_start | string or null | The ISO 8601 timestamp when the batch job began processing (if it's begun). |
| ts_process_done | string or null | The ISO 8601 timestamp when the batch job finished processing (if it's finished). |
| ts_expiration | string or null | The ISO 8601 timestamp when the batch job will expire from the Download center . |
| progress | int | The jobs progress as a percentage. For the 'processing' state, this indicates how much of the job has been processed. |

```python
GET https://hist.databento.com/v0/batch.get_job_details
```

```python
1
2
3
```

```python
curl -G 'https://hist.databento.com/v0/batch.get_job_details' \
 -u $YOUR_API_KEY: \
 -d job_id="XNAS-20240711-Q5D8WRF377"
```

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
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
```

```python
{
  "id": "GLBX-20220901-5DEFXVTMSM",
  "user_id": "46PCMCVF",
  "api_key": "prod-001",
  "cost_usd": 6.72198,
  "dataset": "GLBX.MDP3",
  "symbols": "ESH2",
  "stype_in": "raw_symbol",
  "stype_out": "instrument_id",
  "schema": "trades",
  "start": "2022-01-03T00:00:00.000000000Z",
  "end": "2022-01-20T00:00:00.000000000Z",
  "limit": null,
  "encoding": "dbn",
  "compression": "zstd",
  "pretty_px": false,
  "pretty_ts": false,
  "map_symbols": false,
  "split_symbols": false,
  "split_duration": "day",
  "split_size": null,
  "packaging": null,
  "delivery": "download",
  "record_count": 6063235,
  "billed_size": 291035280,
  "actual_size": null,
  "package_size": null,
  "state": "queued",
  "ts_received": "2022-11-30T20:33:08.006406.000000000Z",
  "ts_queued": null,
  "ts_process_start": null,
  "ts_process_done": null,
  "ts_expiration": null,
  "progress": 100
}
```

### Historical.batch.get_job_details

Get the full job details of a batch job.

Related:Download center.

#### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| job_id | str | required | The batch job ID. This can be found in the download center . |

#### Returns

dict[str, Any]

The batch job details. Seebatch.submit_jobfor a detailed list of returned values.

```python
Historical.batch.get_job_details(
    job_id: str,
) -> dict[str, Any]
```

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
```

```python
import databento as db

client = db.Historical("$YOUR_API_KEY")

job_details = client.batch.get_job_details(
    job_id="GLBX-20221126-DBVXWPJJQN",
)

print(job_details)
```

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
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
```

```python
{
    "id": "GLBX-20221126-DBVXWPJJQN",
    "user_id": "NBPDLF33",
    "api_key": "prod-001",
    "cost_usd": 23.6454,
    "dataset": "GLBX.MDP3",
    "symbols": "ZC.FUT,ES.FUT",
    "stype_in": "parent",
    "stype_out": "instrument_id",
    "schema": "mbo",
    "start": "2022-10-24T00:00:00.000000000Z",
    "end": "2022-11-24T00:00:00.000000000Z",
    "limit": None,
    "encoding": "csv",
    "compression": "zstd",
    "pretty_px": False,
    "pretty_ts": False,
    "map_symbols": False,
    "split_symbols": False,
    "split_duration": "day",
    "split_size": None,
    "packaging": None,
    "delivery": "download",
    "record_count": 412160224,
    "billed_size": 23080972544,
    "actual_size": 8144595219,
    "package_size": 8144628684,
    "state": "done",
    "ts_received": "2022-11-26T09:23:17.519708000Z",
    "ts_queued": "2022-12-03T14:34:57.897790000Z",
    "ts_process_start": "2022-12-03T14:35:00.495167000Z",
    "ts_process_done": "2022-12-03T14:48:15.710116000Z",
    "ts_expiration": "2023-01-02T14:48:15.710116000Z",
    "progress": 100
}
```

### HistoricalClient::batch::get_job_details

Get the full job details of a batch job.

Related:Download center.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| job_id | &str | The batch job ID. This can be found in the download center . |

#### Returns

The batch job details. Seebatch.submit_jobfor a detailed list of returned values.

```python
pub async fn get_job_details(
    &mut self,
    job_id: &str,
) -> databento::Result<BatchJob>;
```

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
```

```python
use databento::HistoricalClient;

let mut client =
    HistoricalClient::builder().key("$YOUR_API_KEY")?.build()?;
let jobs = client
    .batch()
    .get_job_details("XNAS-20230704-NMN5T38NUD")
    .await?;

println!("{jobs:#?}");
```

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
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
```

```python
BatchJob {
    id: "XNAS-20230704-NMN5T38NUD",
    user_id: Some(
        "NBPDLF33",
    ),
    cost_usd: Some(
        0.00075096637011,
    ),
    dataset: "XNAS.ITCH",
    symbols: Symbols(
        [
            "QQQ",
        ],
    ),
    stype_in: RawSymbol,
    stype_out: InstrumentId,
    schema: Ohlcv1M,
    start: 2023-06-01 0:00:00.0 +00:00:00,
    end: 2023-06-02 0:00:00.0 +00:00:00,
    limit: None,
    encoding: Csv,
    compression: None,
    pretty_px: false,
    pretty_ts: false,
    map_symbols: false,
    split_duration: Some(Day),
    split_size: None,
    delivery: Download,
    record_count: Some(
        1267,
    ),
    billed_size: Some(
        47432,
    ),
    actual_size: Some(
        71023,
    ),
    package_size: Some(
        74450,
    ),
    state: Done,
    ts_received: 2023-07-04 12:22:30.06656 +00:00:00,
    ts_queued: Some(
        2023-07-04 12:22:30.352526 +00:00:00,
    ),
    ts_process_start: Some(
        2023-07-04 12:22:44.992907 +00:00:00,
    ),
    ts_process_done: Some(
        2023-07-04 12:22:45.93711 +00:00:00,
    ),
    ts_expiration: Some(
        2023-08-03 12:22:45.93711 +00:00:00,
    ),
    progress: Some(100),
}
```

### Historical::BatchDownload

Download a batch job or a specific file to{output_dir}/{job_id}/.

Will automatically generateoutput_dirandjob_iddirectories if they do not already exist.

Related:Download center.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| output_dir | std::filesystem::path | The directory to download the file(s) to. |
| job_id | std::string | The batch job identifier. |
| filename_to_download | std::string | The specific file to download. If not specified, then will download all files for the batch job. |

#### Returns

std::vector<std::filesystem::path>orstd::filesystem::path

The paths of the downloaded files.

```python
std::vector<std::filesystem::path> BatchDownload(
    const std::filesystem::path& output_dir,
    const std::string& job_id);
std::filesystem::path BatchDownload(
    const std::filesystem::path& output_dir,
    const std::string& job_id,
    const std::string& filename_to_download);
```

```python
1
2
3
4
5
6
7
8
```

```python
#include <databento/historical.hpp>

using namespace databento;

auto client =
    Historical::Builder().SetKey("$YOUR_API_KEY").Build();
client.BatchDownload("my_data", "XNAS-20250108-VVS57U5PD8",
                     "metadata.json");
```

### /batch.download

Download a file from a batch job.

All files for a job can be downloaded as a single ZIP archive by using the job ID appended with ".zip" as thefilename.

Related:Download center.

#### Parameters

This endpoint uses path parameters.

| Parameter | Required | Description |
| --- | --- | --- |
| user_id | required | The user ID for the batch job. This can be found on the API key management page of the portal . |
| job_id | required | The batch job ID. This can be found in the download center . |
| filename | required | The filename from the job to download. |

#### Returns

The file data. It is recommended to output this to a file.

```python
GET https://hist.databento.com/v0/batch/download/{user_id}/{job_id}/{filename}
```

```python
1
2
```

```python
curl -G 'https://hist.databento.com/v0/batch/download/WJSPXEQK/XNAS-20240711-Q5D8WRF377/XNAS-20240711-Q5D8WRF377.zip' \
 -u $YOUR_API_KEY:
```

### Historical.batch.download

Download a batch job or a specific file to{output_dir}/{job_id}/.

Will automatically generate any necessary directories if they do not already exist.

Related:Download center.

#### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| job_id | str | required | The batch job identifier. |
| output_dir | PathLike[str] or str | optional | The directory to download the file(s) to. If None , defaults to the current working directory. |
| filename_to_download | str | optional | The specific file to download. If None then will download all files for the batch job. |
| keep_zip | bool, default False | optional | If True , and filename_to_download is None , all job files will be saved as a .zip archive in the output_dir . |

#### Returns

A list of paths to the downloaded files.

```python
Historical.batch.download(
    job_id: str,
    output_dir: PathLike[str] | str | None = None,
    filename_to_download: str | None = None,
    keep_zip: bool = False,
) -> list[Path]
```

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
```

```python
import databento as db

client = db.Historical("$YOUR_API_KEY")

# Download all files for the batch job
client.batch.download(
    job_id="GLBX-20220610-5DEFXVTMSM",
    output_dir="my_data/",
)

# Alternatively, you can download a specific file
client.batch.download(
    job_id="GLBX-20220610-5DEFXVTMSM",
    output_dir="my_data/",
    filename_to_download="metadata.json",
)
```

### HistoricalClient::batch::download

Download a batch job or a specific file to{output_dir}/{job_id}/.

Will automatically create any necessary directories if they do not already exist. Verifies the checksum of each downloaded file and will retry on a download failure.

Related:Download center.

#### Parameters

| Field | Type | Description |
| --- | --- | --- |
| params | DownloadParams | See DownloadParams for details. |

#### Returns

Vec<PathBuf>

A list of paths to the downloaded files.

```python
pub async fn download(
    &mut self,
    params: &DownloadParams,
) -> databento::Result<Vec<PathBuf>>;
```

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
18
19
20
21
```

```python
use std::path::PathBuf;

use databento::{
    HistoricalClient, historical::batch::DownloadParams,
};

let mut params = DownloadParams::builder()
    .output_dir(PathBuf::from("my_data"))
    .job_id("XNAS-20250108-VVS57U5PD8")
    .build();
let mut client =
    HistoricalClient::builder().key("$YOUR_API_KEY")?.build()?;
// Download all files for the batch job
let files = client.batch().download(&params).await?;
println!("{files:#?}");

// Download all files for the batch job
params.filename_to_download = Some("metadata.json".to_owned());
let file = client.batch().download(&params).await?;
assert_eq!(file.len(), 1);
println!("{}", file[0].display());
```

```python
1
2
3
4
5
6
7
```

```python
[
    "my_data/XNAS-20230704-NMN5T38NUD/manifest.json",
    "my_data/XNAS-20230704-NMN5T38NUD/condition.json",
    "my_data/XNAS-20230704-NMN5T38NUD/metadata.json",
    "my_data/XNAS-20230704-NMN5T38NUD/symbology.json",
    "my_data/XNAS-20230704-NMN5T38NUD/xnas-itch-20230601.ohlcv-1m.csv",
]
```

### Historical.batch.download_async

Asynchronously download a batch job or a specific file to{output_dir}/{job_id}/.

Will automatically generate any necessary directories if they do not already exist.

Related:Download center.

#### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| job_id | str | required | The batch job identifier. |
| output_dir | PathLike[str] or str | optional | The directory to download the file(s) to. If None , defaults to the current working directory. |
| filename_to_download | str | optional | The specific file to download. If None then will download all files for the batch job. |
| keep_zip | bool, default False | optional | If True , and filename_to_download is None , all job files will be saved as a .zip archive in the output_dir . |

#### Returns

A list of paths to the downloaded files.

```python
Historical.batch.download_async(
    job_id: str,
    output_dir: PathLike[str] | str | None = None,
    filename_to_download: str | None = None,
    keep_zip: bool = False,
) -> Awaitable[list[Path]]
```

This method is acoroutineand must be used with anawaitexpression.

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
18
19
```

```python
import asyncio
import databento as db

client = db.Historical("$YOUR_API_KEY")

# Download all files for the batch job
coro = client.batch.download_async(
    job_id="GLBX-20220610-5DEFXVTMSM",
    output_dir="my_data/",
)
asyncio.run(coro)

# Alternatively, you can download a specific file
coro = client.batch.download_async(
    job_id="GLBX-20220610-5DEFXVTMSM",
    output_dir="my_data/",
    filename_to_download="metadata.json",
)
asyncio.run(coro)
```

## Helpers

### DbnStore

TheDbnStoreobject is a reader forDBNdata from files or anyIReadablesource (e.g., historical HTTP streams).DbnFileStoreis a backwards-compatible type alias forDbnStore.

TimeseriesGetRange(without callbacks) returns aDbnStore.

This class provides both a callback API (Replay) similar toTimeseriesGetRangein historical data andLiveThreadedfor live data, as well as a blocking API (GetMetadataandNextRecord) similar to that ofLiveBlocking. Only one set of methods should be used on a given instance.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| log_receiver | ILogReceiver* | Non-null, non-owning pointer to a log receiver . To disable logging, pass a NullLogReceiver . |
| file_path | std::filesystem::path | File path to the DBN file ( .dbn ) or Zstd-compressed DBN ( .dbn.zst ). |
| input | std::unique_ptr<IReadable> | An IReadable source (e.g., HTTP stream from TimeseriesGetRange ). Used in place of file_path . |
| upgrade_policy | VersionUpgradePolicy | How to handle records from previous DBN versions. By default, records from DBN versions 1 and 2 are upgraded to version 3. |

```python
DbnStore(const std::filesystem::path& file_path);
DbnStore(ILogReceiver* log_receiver,
         const std::filesystem::path& file_path,
         VersionUpgradePolicy upgrade_policy);
DbnStore(ILogReceiver* log_receiver,
         std::unique_ptr<IReadable> input,
         VersionUpgradePolicy upgrade_policy);
```

### DBNStore

TheDBNStoreobject is an I/O helper class for working withDBN-encoded data. Typically, this object is created when performing historical requests. However, it can be created directly using DBN data on disk or in memory using provided factory methods:

#### Attributes

| Parameter | Type | Description |
| --- | --- | --- |
| nbytes | int | The size of the data in bytes. |
| raw | bytes | The raw data from the I/O stream. |
| metadata | Metadata | The metadata header for the DBNStore . |
| dataset | str | The dataset ID. |
| schema | Schema or None | The data record schema. If None , the DBNStore may contain multiple schemas. |
| symbols | list[str] | The query symbols for the data. |
| stype_in | SType or None | The query input symbology type for the data. If None , the DBNStore may contain mixed STypes. |
| stype_out | SType | The query output symbology type for the data. |
| start | pd.Timestamp | The query start for the data as a pd.Timestamp . |
| end | pd.Timestamp or None | The query end for the data as a pd.Timestamp . If None , the DBNStore data was created without a known end time. |
| limit | int or None | The query limit for the data. |
| encoding | Encoding | The data encoding. |
| compression | Compression | Return the data compression format (if any). |
| mappings | dict[str, list[dict[str, Any]]] | Return the symbology mappings for the data. |
| symbology | dict[str, Any] | Return the symbology resolution information for the data. |

### AsyncDbnDecoder

An object for working withDBN-encoded data. Typically this object is created when performing historical requests. However, it can be created directly using DBN data on disk or in memory using the provided associated functions:

Thecrate documentationfor a comprehensive list of methods and implemented traits.

### DBNStore.from_bytes

Read data from a DBN byte stream.

#### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| data | BytesIO or bytes or IO[bytes] | required | The bytes to read from. |

#### Returns

ADBNStoreobject.

```python
DBNStore.from_bytes(
    data: BytesIO | bytes | IO[bytes],
) -> DBNStore
```

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
18
19
20
21
22
```

```python
import databento as db

client = db.Historical("$YOUR_API_KEY")

data = client.timeseries.get_range(
    dataset="GLBX.MDP3",
    symbols=["ESM2"],
    schema="trades",
    start="2022-06-06",
)

# Save streamed data to .dbn.zst
path = "GLBX-ESM2-20220606.trades.dbn.zst"
data.to_file(path)

# Open saved data as a byte stream.
with open(path, "rb") as saved:
    stored_data = db.DBNStore.from_bytes(saved)

# Convert to dataframe
df = stored_data.to_df()
print(df.head())
```

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
```

```python
ts_event  rtype  publisher_id  instrument_id action  ... size  flags  ts_in_delta  sequence  symbol
ts_recv                                                                                                             ...
2022-06-06 00:00:00.070314216+00:00 2022-06-06 00:00:00.070033767+00:00      0             1           3403      T  ...    1      0        18681    157862    ESM2
2022-06-06 00:00:00.090544076+00:00 2022-06-06 00:00:00.089830441+00:00      0             1           3403      T  ...    1      0        18604    157922    ESM2
2022-06-06 00:00:00.807324169+00:00 2022-06-06 00:00:00.807018955+00:00      0             1           3403      T  ...    4      0        18396    158072    ESM2
2022-06-06 00:00:01.317722490+00:00 2022-06-06 00:00:01.317385867+00:00      0             1           3403      T  ...    1      0        22043    158111    ESM2
2022-06-06 00:00:01.317736158+00:00 2022-06-06 00:00:01.317385867+00:00      0             1           3403      T  ...    7      0        17280    158112    ESM2

[5 rows x 13 columns]
```

### AsyncDbnStore::new

Create a new decoder from a DBN stream that implementsAsyncReadExt. Immediately decodes the DBNMetadata.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| reader | R: tokio::io::AsyncReadExt + Unpin | A readable DBN byte stream. |

#### Returns

AnAsyncDbnStoreobject.

This function will return an error if it is unable to parse the metadata inreaderor the input is encoded in a newer version of DBN.

```python
pub async fn new<R>(mut reader: R) -> dbn::Result<Self>
where
    R: tokio::io::AsyncReadExt + Unpin;
```

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
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
```

```python
use std::io::SeekFrom;

use databento::{
    HistoricalClient,
    dbn::{
        Dataset, Schema, TradeMsg,
        decode::{AsyncDbnDecoder, DbnMetadata},
        encode::{AsyncDbnEncoder, AsyncEncodeRecord},
    },
    historical::timeseries::GetRangeParams,
};
use time::macros::datetime;
use tokio::{fs::OpenOptions, io::AsyncSeekExt};

let mut client =
    HistoricalClient::builder().key("$YOUR_API_KEY")?.build()?;
let mut decoder = client
    .timeseries()
    .get_range(
        &GetRangeParams::builder()
            .dataset(Dataset::GlbxMdp3)
            .date_time_range(
                datetime!(2022-06-06 00:00 UTC)
                    ..datetime!(2022-06-07 00:00 UTC),
            )
            .symbols("ESM2")
            .schema(Schema::Trades)
            .build(),
    )
    .await?;

// Save streamed data to .dbn
let path = "GLBX-ESM2-20220606.trades.dbn.zst";
let mut file = OpenOptions::new()
    .read(true)
    .write(true)
    .create(true)
    .truncate(true)
    .open(path)
    .await?;
let mut encoder =
    AsyncDbnEncoder::new(&mut file, decoder.metadata()).await?;
while let Some(trade) =
    decoder.decode_record::<TradeMsg>().await?
{
    encoder.encode_record(trade).await?;
}
encoder.flush().await?;

// Open saved data
file.seek(SeekFrom::Start(0)).await?;
let mut decoder = AsyncDbnDecoder::new(file).await?;
for i in 0..5 {
    let trade =
        decoder.decode_record::<TradeMsg>().await?.unwrap();
    println!("{trade:?}");
}
```

```python
1
2
3
4
5
```

```python
TradeMsg { hd: RecordHeader { length: 12, rtype: Mbp0, publisher_id: GlbxMdp3Glbx, instrument_id: 3403, ts_event: 1654473600070033767 }, price: 4108.500000000, size: 1, action: 'T', side: 'A', flags: 0, depth: 0, ts_recv: 1654473600070314216, ts_in_delta: 18681, sequence: 157862 }
TradeMsg { hd: RecordHeader { length: 12, rtype: Mbp0, publisher_id: GlbxMdp3Glbx, instrument_id: 3403, ts_event: 1654473600089830441 }, price: 4108.250000000, size: 1, action: 'T', side: 'A', flags: 0, depth: 0, ts_recv: 1654473600090544076, ts_in_delta: 18604, sequence: 157922 }
TradeMsg { hd: RecordHeader { length: 12, rtype: Mbp0, publisher_id: GlbxMdp3Glbx, instrument_id: 3403, ts_event: 1654473600807018955 }, price: 4108.250000000, size: 4, action: 'T', side: 'B', flags: 0, depth: 0, ts_recv: 1654473600807324169, ts_in_delta: 18396, sequence: 158072 }
TradeMsg { hd: RecordHeader { length: 12, rtype: Mbp0, publisher_id: GlbxMdp3Glbx, instrument_id: 3403, ts_event: 1654473601317385867 }, price: 4108.000000000, size: 1, action: 'T', side: 'A', flags: 0, depth: 0, ts_recv: 1654473601317722490, ts_in_delta: 22043, sequence: 158111 }
TradeMsg { hd: RecordHeader { length: 12, rtype: Mbp0, publisher_id: GlbxMdp3Glbx, instrument_id: 3403, ts_event: 1654473601317385867 }, price: 4108.000000000, size: 7, action: 'T', side: 'A', flags: 0, depth: 0, ts_recv: 1654473601317736158, ts_in_delta: 17280, sequence: 158112 }
```

### DbnStore::Replay

Replay data by passing records sequentially to the given callback.

Should only be called once per instance.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| metadata_callback | std::function<void(Metadata&&)> | A callback for receiving the Metadata of the file. This callback will be called only once, immediately before the first time record_callback is called. |
| record_callback | std::function<KeepGoing(const Record&)> | A callback for receiving the Record s from the file. The particular record type (or record types if saved live data) will depend on the schema in the metadata. Return KeepGoing::Continue to continue receiving records or KeepGoing::Stop to stop replaying. |

#### Returns

Returns data via the callbacksmetadata_callbackandrecord_callback.

The reference passed torecord_callbackis only valid during the callback. Copy the record or particular fields to persist data between calls to the callback.

A full list of fields returned through therecord_callbackfor each schema is available in thelist of fields by schemaor the struct definitions in<databento/record.hpp>.

```python
void Replay(const MetadataCallback& metadata_callback,
            const RecordCallback& record_callback);
void Replay(const RecordCallback& record_callback);
```

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
18
19
```

```python
#include <databento/historical.hpp>
#include <iostream>

using namespace databento;

auto print_large_trades = [](const Record& record) {
  const auto& trade_msg = record.Get<TradeMsg>();
  if (trade_msg.size > 100) {
    std::cout << trade_msg << '\n';
  }
  return KeepGoing::Continue;
};

auto client =
    Historical::Builder().SetKey("$YOUR_API_KEY").Build();
DbnStore dbn_store = client.TimeseriesGetRangeToFile(
    "GLBX.MDP3", {"2022-06-06", "2022-06-10"}, {"ESM2"},
    Schema::Trades, "ESM2_20220606-20220610.dbn.zst");
dbn_store.Replay(print_large_trades);
```

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
18
19
20
21
22
23
24
25
```

```python
TradeMsg {
    hd = RecordHeader { length = 12, rtype = mbp-0, publisher_id = 1, instrument_id = 3403, ts_event = 2022-06-06T06:52:51.478093125Z },
    price = 4132.000000000,
    size = 109,
    action = Trade,
    side = Ask,
    flags = 0,
    depth = 0,
    ts_recv = 2022-06-06T06:52:51.478443918Z,
    ts_in_delta = 18569,
    sequence = 890656
}
TradeMsg {
    hd = RecordHeader { length = 12, rtype = mbp-0, publisher_id = 1, instrument_id = 3403, ts_event = 2022-06-06T13:50:42.622492841Z },
    price = 4140.000000000,
    size = 165,
    action = Trade,
    side = Ask,
    flags = 0,
    depth = 0,
    ts_recv = 2022-06-06T13:50:42.623069413Z,
    ts_in_delta = 26961,
    sequence = 3070868
}
...
```

### DBNStore.from_file

Read data from a DBN file.

databento.read_dbnis an alias forDBNStore.from_file.

#### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| path | PathLike[str] or str | required | The file path to read from. |

#### Returns

ADBNStoreobject.

```python
DBNStore.from_file(
    path: PathLike[str] | str,
) -> DBNStore
```

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
18
19
20
21
```

```python
import databento as db

client = db.Historical("$YOUR_API_KEY")

data = client.timeseries.get_range(
    dataset="GLBX.MDP3",
    symbols=["ESM2"],
    schema="trades",
    start="2022-06-06",
)

# Save streamed data to .dbn.zst
path = "GLBX-ESM2-20220606.trades.dbn.zst"
data.to_file(path)

# Read saved .dbn.zst
stored_data = db.DBNStore.from_file(path)

# Convert to dataframe
df = stored_data.to_df()
print(df.head())
```

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
```

```python
ts_event  rtype  publisher_id  instrument_id action  ... size  flags  ts_in_delta  sequence  symbol
ts_recv                                                                                                             ...
2022-06-06 00:00:00.070314216+00:00 2022-06-06 00:00:00.070033767+00:00      0             1           3403      T  ...    1      0        18681    157862    ESM2
2022-06-06 00:00:00.090544076+00:00 2022-06-06 00:00:00.089830441+00:00      0             1           3403      T  ...    1      0        18604    157922    ESM2
2022-06-06 00:00:00.807324169+00:00 2022-06-06 00:00:00.807018955+00:00      0             1           3403      T  ...    4      0        18396    158072    ESM2
2022-06-06 00:00:01.317722490+00:00 2022-06-06 00:00:01.317385867+00:00      0             1           3403      T  ...    1      0        22043    158111    ESM2
2022-06-06 00:00:01.317736158+00:00 2022-06-06 00:00:01.317385867+00:00      0             1           3403      T  ...    7      0        17280    158112    ESM2

[5 rows x 13 columns]
```

### AsyncDbnStore::from_file

Create a new decoder from a DBN file. If the file is zstd-compressed, usefrom_zstd_fileinstead.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| path | impl AsRef<Path> | A path to an uncompressed DBN file. |

#### Returns

AnAsyncDbnStoreobject.

This function will return an error if it is unable to parse the metadata in the file or the input is encoded in a newer version of DBN.

```python
pub async fn from_file(
    path: impl AsRef<Path>,
) -> dbn::Result<Self>;
```

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
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
```

```python
use databento::{
    HistoricalClient,
    dbn::{
        Schema, TradeMsg,
        decode::{AsyncDbnDecoder, DbnMetadata},
        encode::{
            AsyncEncodeRecord,
            dbn::AsyncEncoder as AsyncDbnEncoder,
        },
    },
    historical::timeseries::GetRangeParams,
};
use time::macros::datetime;
use tokio::fs::File;

let mut client =
    HistoricalClient::builder().key("$YOUR_API_KEY")?.build()?;
let mut decoder = client
    .timeseries()
    .get_range(
        &GetRangeParams::builder()
            .dataset("GLBX.MDP3")
            .date_time_range(
                datetime!(2022-06-06 00:00 UTC)
                    ..datetime!(2022-06-07 00:00 UTC),
            )
            .symbols("ESM2")
            .schema(Schema::Trades)
            .build(),
    )
    .await?;

// Save streamed data to .dbn
let path = "GLBX-ESM2-20220606.trades.dbn.zst";
let file = File::create(path).await?;
let mut encoder =
    AsyncDbnEncoder::new(file, decoder.metadata()).await?;
while let Some(trade) =
    decoder.decode_record::<TradeMsg>().await?
{
    encoder.encode_record(trade).await?;
}
encoder.flush().await?;

// Open saved data
let mut decoder = AsyncDbnDecoder::from_file(path).await?;
for i in 0..5 {
    let trade =
        decoder.decode_record::<TradeMsg>().await?.unwrap();
    println!("{trade:?}");
}
```

```python
1
2
3
4
5
```

```python
TradeMsg { hd: RecordHeader { length: 12, rtype: Mbp0, publisher_id: GlbxMdp3Glbx, instrument_id: 3403, ts_event: 1654473600070033767 }, price: 4108.500000000, size: 1, action: 'T', side: 'A', flags: 0, depth: 0, ts_recv: 1654473600070314216, ts_in_delta: 18681, sequence: 157862 }
TradeMsg { hd: RecordHeader { length: 12, rtype: Mbp0, publisher_id: GlbxMdp3Glbx, instrument_id: 3403, ts_event: 1654473600089830441 }, price: 4108.250000000, size: 1, action: 'T', side: 'A', flags: 0, depth: 0, ts_recv: 1654473600090544076, ts_in_delta: 18604, sequence: 157922 }
TradeMsg { hd: RecordHeader { length: 12, rtype: Mbp0, publisher_id: GlbxMdp3Glbx, instrument_id: 3403, ts_event: 1654473600807018955 }, price: 4108.250000000, size: 4, action: 'T', side: 'B', flags: 0, depth: 0, ts_recv: 1654473600807324169, ts_in_delta: 18396, sequence: 158072 }
TradeMsg { hd: RecordHeader { length: 12, rtype: Mbp0, publisher_id: GlbxMdp3Glbx, instrument_id: 3403, ts_event: 1654473601317385867 }, price: 4108.000000000, size: 1, action: 'T', side: 'A', flags: 0, depth: 0, ts_recv: 1654473601317722490, ts_in_delta: 22043, sequence: 158111 }
TradeMsg { hd: RecordHeader { length: 12, rtype: Mbp0, publisher_id: GlbxMdp3Glbx, instrument_id: 3403, ts_event: 1654473601317385867 }, price: 4108.000000000, size: 7, action: 'T', side: 'A', flags: 0, depth: 0, ts_recv: 1654473601317736158, ts_in_delta: 17280, sequence: 158112 }
```

### DbnStore::GetMetadata

Decodes theDBNmetadata if it has not already been decoded and returns a reference to it.

#### Returns

const Metadata&

DBNMetadataabout the file.

```python
const Metadata& GetMetadata();
```

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
```

```python
#include <databento/historical.hpp>
#include <iostream>

using namespace databento;

auto client =
    Historical::Builder().SetKey("$YOUR_API_KEY").Build();
DbnStore dbn_store = client.TimeseriesGetRangeToFile(
    "XNAS.ITCH", {"2024-06-24", "2024-06-29"}, {"META"},
    Schema::Trades, "META_20240624-20240629.dbn.zst");
std::cout << dbn_store.GetMetadata() << '\n';
```

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
18
```

```python
Metadata {
    version = 3,
    dataset = "XNAS.ITCH",
    schema = trades,
    start = 2024-06-24T00:00:00.000000000Z,
    end = 2024-06-29T00:00:00.000000000Z,
    limit = 0,
    stype_in = raw_symbol,
    stype_out = instrument_id,
    ts_out = false,
    symbol_cstr_len = 71,
    symbols = { "META" },
    partial = {},
    not_found = {},
    mappings = {
        SymbolMapping { raw_symbol = "META", intervals = { MappingInterval { start_date = 2024-06-24, end_date = 2024-06-29, symbol = "10451" } } }
    }
}
```

### AsyncDbnStore::from_zstd_file

Create a new decoder from a Zstandard-compressed DBN file. If the file is uncompressed, usefrom_fileinstead.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| path | impl AsRef<Path> | A path to a Zstandard-compressed DBN file. |

#### Returns

AnAsyncDbnStoreobject.

This function will return an error if it is unable to parse the metadata in the file or the input is encoded in a newer version of DBN.

```python
pub async fn from_zstd_file(
    path: impl AsRef<Path>,
) -> dbn::Result<Self>;
```

### DbnStore::NextRecord

Returns the next record from the data source.

#### Returns

const Record*

The next record. The particular record type will depend on theschemain the metadata.

The returned reference or pointer is only valid until the next call toNextRecord. Copy the record or relevant fields to persist data across calls toNextRecord.

Returnsnullptrwhen all records have been decoded.

```python
const Record* NextRecord();
```

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
#include <databento/historical.hpp>
#include <databento/record.hpp>
#include <iostream>

using namespace databento;

auto client =
    Historical::Builder().SetKey("$YOUR_API_KEY").Build();
DbnStore dbn_store = client.TimeseriesGetRangeToFile(
    "XNAS.ITCH", {"2024-06-24", "2024-06-29"}, {"META"},
    Schema::Trades, "META_20240624-20240629.dbn.zst");
while (const Record* record = dbn_store.NextRecord()) {
  const auto& trade_msg = record->Get<TradeMsg>();
  if (trade_msg.size > 100) {
    std::cout << trade_msg << '\n';
  }
}
```

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
18
19
20
21
22
23
24
25
```

```python
TradeMsg {
    hd = RecordHeader { length = 12, rtype = mbp-0, publisher_id = 2, instrument_id = 10451, ts_event = 2024-06-24T08:01:59.771923047Z },
    price = 498.380000000,
    size = 228,
    action = Trade,
    side = Ask,
    flags = LAST | PUBLISHER_SPECIFIC (130),
    depth = 0,
    ts_recv = 2024-06-24T08:01:59.772093551Z,
    ts_in_delta = 170504,
    sequence = 383997
}
TradeMsg {
    hd = RecordHeader { length = 12, rtype = mbp-0, publisher_id = 2, instrument_id = 10451, ts_event = 2024-06-24T08:02:10.254849369Z },
    price = 498.380000000,
    size = 120,
    action = Trade,
    side = Ask,
    flags = LAST (128),
    depth = 0,
    ts_recv = 2024-06-24T08:02:10.255020595Z,
    ts_in_delta = 171226,
    sequence = 397630
}
...
```

### DBNStore.reader

Return an I/O reader for the data.

#### Returns

A rawIO streamfor reading the DBNStore data.

```python
DBNStore.reader() -> IO[bytes]
```

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
```

```python
import databento as db

client = db.Historical("$YOUR_API_KEY")

bento = client.timeseries.get_range(
    dataset="GLBX.MDP3",
    symbols="ZWZ3",
    start="2022-06-06",
)

# Create an IO stream reader
reader = bento.reader
```

### DBNStore.replay

Replay data by passing records sequentially to the given callback.

Refer to theList of fields by schemaarticle for documentation on the fields contained with each record type.

#### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| callback | Callable | required | The callback function or method to be dispatched on every event. |

#### Returns

```python
DBNStore.replay(
    callback: Callable[[DBNRecord], None],
) -> None
```

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
18
```

```python
import databento as db

client = db.Historical("$YOUR_API_KEY")

data = client.timeseries.get_range(
    dataset="GLBX.MDP3",
    symbols=["ESM2"],
    start="2022-06-06",
)

def print_large_trades(trade):
    size = getattr(trade, "size", 0)
    if size >= 200:
        print(trade)

data.replay(print_large_trades)
```

```python
1
2
3
```

```python
TradeMsg(ts_recv=1654524078342408839, pretty_ts_recv='2022-06-06T14:01:18.342408839Z', rtype=<RType.MBP_0: 0>, publisher_id=GLBX.MDP3.GLBX (1), instrument_id=3403, ts_event=1654524078339857609, pretty_ts_event='2022-06-06T14:01:18.339857609Z', action='T', side='B', depth=0, price=4164000000000, pretty_price=4164, size=291, flags=0, ts_in_delta=20352, sequence=3605032)
TradeMsg(ts_recv=1654524133737794739, pretty_ts_recv='2022-06-06T14:02:13.737794739Z', rtype=<RType.MBP_0: 0>, publisher_id=GLBX.MDP3.GLBX (1), instrument_id=3403, ts_event=1654524133736900455, pretty_ts_event='2022-06-06T14:02:13.736900455Z', action='T', side='B', depth=0, price=4160000000000, pretty_price=4160, size=216, flags=0, ts_in_delta=28024, sequence=3659203)
TradeMsg(ts_recv=1654538295589900967, pretty_ts_recv='2022-06-06T17:58:15.589900967Z', rtype=<RType.MBP_0: 0>, publisher_id=GLBX.MDP3.GLBX (1), instrument_id=3403, ts_event=1654538295588752739, pretty_ts_event='2022-06-06T17:58:15.588752739Z', action='T', side='B', depth=0, price=4140000000000, pretty_price=4140, size=200, flags=0, ts_in_delta=21708, sequence=10031624)
```

### AsyncDbnStore::with_zstd

Create a new decoder from a Zstandard-compressed DBN stream that implementsAsyncReadExt. IfreaderimplementsAsyncBufRead, it's better to usewith_zstd_bufferto avoid unnecessary additional buffering.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| reader | R: tokio::io::AsyncReadExt + Unpin | A readable Zstandard-compressed DBN byte stream. |

#### Returns

AnAsyncDbnStoreobject.

This function will return an error if it is unable to parse the metadata inreaderor the input is encoded in a newer version of DBN.

```python
pub async fn with_zstd<R>(mut reader: R) -> dbn::Result<Self>
where
    R: tokio::io::AsyncReadExt + Unpin;
```

### AsyncDbnStore::with_zstd_buffer

Create a new decoder from a buffered Zstandard-compressed DBN stream that implementsAsyncBufReadExt.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| reader | R: tokio::io::AsyncBufReadExt + Unpin | A readable buffered Zstandard-compressed DBN byte stream. |

#### Returns

AnAsyncDbnStoreobject.

This function will return an error if it is unable to parse the metadata inreaderor the input is encoded in a newer version of DBN.

```python
pub async fn with_zstd_buffer<R>(
    mut reader: R,
) -> dbn::Result<Self>
where
    R: tokio::io::AsyncBufReadExt + Unpin;
```

### DBNStore.request_full_definitions

Request for full instrumentDefinition(s) for all symbols based on the metadata properties. This is useful for retrieving the instrument definitions for saved DBN data.

Atimeseries.get_rangerequest is made to obtain the definitions data which will incur a cost.

#### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| client | Historical | required | The historical client to use for the request (contains the API key). |
| path | PathLike[str] or str | optional | The path to stream the data to on disk (will then return a DBNStore ). |

#### Returns

ADBNStoreobject.

A full list of fields for each schema is available throughHistorical.metadata.list_fields.

```python
DBNStore.request_full_definitions(
    client: Historical,
    path: PathLike[str] | str | None = None,
) -> DBNStore
```

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
18
```

```python
import databento as db

client = db.Historical(
    key="$YOUR_API_KEY",
)

trades = client.timeseries.get_range(
    dataset="GLBX.MDP3",
    symbols=["ES.FUT"],
    stype_in="parent",
    schema="trades",
    start="2022-06-06",
)

definitions = trades.request_full_definitions(client).to_df()
definitions = definitions.sort_values(["expiration", "symbol"]).set_index("expiration")

print(definitions[["symbol"]])
```

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
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
```

```python
symbol
expiration
2022-06-17 13:30:00+00:00       ESM2
2022-06-17 13:30:00+00:00  ESM2-ESH3
2022-06-17 13:30:00+00:00  ESM2-ESM3
2022-06-17 13:30:00+00:00  ESM2-ESU2
2022-06-17 13:30:00+00:00  ESM2-ESZ2
2022-09-16 13:30:00+00:00       ESU2
2022-09-16 13:30:00+00:00  ESU2-ESH3
2022-09-16 13:30:00+00:00  ESU2-ESM3
2022-09-16 13:30:00+00:00  ESU2-ESU3
2022-09-16 13:30:00+00:00  ESU2-ESZ2
2022-12-16 14:30:00+00:00       ESZ2
2022-12-16 14:30:00+00:00  ESZ2-ESH3
2022-12-16 14:30:00+00:00  ESZ2-ESM3
2022-12-16 14:30:00+00:00  ESZ2-ESU3
2023-03-17 13:30:00+00:00       ESH3
2023-03-17 13:30:00+00:00  ESH3-ESM3
2023-03-17 13:30:00+00:00  ESH3-ESU3
2023-03-17 13:30:00+00:00  ESH3-ESZ3
2023-06-16 13:30:00+00:00       ESM3
2023-06-16 13:30:00+00:00  ESM3-ESU3
2023-06-16 13:30:00+00:00  ESM3-ESZ3
2023-09-15 13:30:00+00:00       ESU3
2023-09-15 13:30:00+00:00  ESU3-ESH4
2023-09-15 13:30:00+00:00  ESU3-ESZ3
2023-12-15 14:30:00+00:00       ESZ3
2023-12-15 14:30:00+00:00  ESZ3-ESH4
2024-03-15 13:30:00+00:00       ESH4
2024-03-15 13:30:00+00:00  ESH4-ESM4
2024-06-21 13:30:00+00:00       ESM4
2024-09-20 13:30:00+00:00       ESU4
2024-12-20 14:30:00+00:00       ESZ4
2025-12-19 14:30:00+00:00       ESZ5
2026-12-18 14:30:00+00:00       ESZ6
```

### AsyncDbnStore::decode_record

Decode a single record of a specific type. If the record type is unknown, such as when working with Live data where the stream can contain several different record types, usedecode_record_ref.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| T | HasRType | A DBN record type. |

#### Returns

A reference to the decoded record of typeTorOk(None)if the stream has been exhausted.

This function will return an error if the record is not of typeTor there's an error reading from the input stream.

```python
pub async fn decode_record<T: HasRType>(
    &mut self,
) -> dbn::Result<Option<&T>>;
```

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
18
19
20
21
22
23
24
25
```

```python
use databento::{
    HistoricalClient,
    dbn::{Dataset, OhlcvMsg, Schema},
    historical::timeseries::GetRangeParams,
};
use time::macros::datetime;

let mut client =
    HistoricalClient::builder().key("$YOUR_API_KEY")?.build()?;
let mut decoder = client
    .timeseries()
    .get_range(
        &GetRangeParams::builder()
            .dataset(Dataset::XnasItch)
            .date_time_range(
                datetime!(2023-08-07 00:00 UTC)
                    ..datetime!(2023-08-08 00:00 UTC),
            )
            .symbols("AAPL")
            .schema(Schema::Ohlcv1M)
            .build(),
    )
    .await?;
let bar = decoder.decode_record::<OhlcvMsg>().await?.unwrap();
println!("{bar:#?}");
```

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
```

```python
OhlcvMsg {
    hd: RecordHeader {
        length: 14,
        rtype: Ohlcv1M,
        publisher_id: XnasItchXnas,
        instrument_id: 32,
        ts_event: 1691395200000000000,
    },
    open: 183.440000000,
    high: 183.460000000,
    low: 182.750000000,
    close: 183.300000000,
    volume: 2030,
}
```

### DBNStore.request_symbology

Request to resolvesymbologymappings based on the metadata properties.

#### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| client | Historical | required | The historical client to use for the request (contains the API key). |

#### Returns

dict[str, Any]

A result including a map of input symbol to output symbol across a date range.

```python
DBNStore.request_symbology(
    client: Historical,
) -> dict[str, Any]
```

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
18
19
20
```

```python
import databento as db

client = db.Historical("$YOUR_API_KEY")

data = client.timeseries.get_range(
    dataset="GLBX.MDP3",
    symbols=["ESM2"],
    schema="trades",
    start="2022-06-06",
)

# Save streamed data to .dbn.zst
data.to_file("GLBX-ESM2-20220606.trades.dbn.zst")

# Read saved .dbn.zst
stored_data = db.DBNStore.from_file("GLBX-ESM2-20220606.trades.dbn.zst")

# Request symbology from .dbn.zst metadata
symbology = stored_data.request_symbology(client=client)
print(symbology)
```

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
18
19
20
21
22
```

```python
{
    "result": {
        "ESM2": [
            {
                "d0": "2022-06-06",
                "d1": "2022-06-07",
                "s": "3403"
            }
        ]
    },
    "symbols": [
        "ESM2"
    ],
    "stype_in": "raw_symbol",
    "stype_out": "instrument_id",
    "start_date": "2022-06-06",
    "end_date": "2022-06-07",
    "partial": [],
    "not_found": [],
    "message": "OK",
    "status": 0
}
```

### AsyncDbnStore::decode_record_ref

Decode a single record of an unknown type.

#### Returns

ARecordRefâa wrapper around a record of a dynamic typeâorOk(None)if the stream has been exhausted.

This function will return an error if there's an error reading from the input stream.

```python
pub async fn decode_record_ref(
    &mut self,
) -> dbn::Result<Option<RecordRef>>;
```

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
18
19
20
21
22
23
24
25
26
```

```python
use databento::{
    HistoricalClient,
    dbn::{OhlcvMsg, SType, Schema},
    historical::timeseries::GetRangeParams,
};
use time::macros::datetime;

let mut client =
    HistoricalClient::builder().key("$YOUR_API_KEY")?.build()?;
let mut decoder = client
    .timeseries()
    .get_range(
        &GetRangeParams::builder()
            .dataset("OPRA.PILLAR")
            .stype_in(SType::Parent)
            .date_time_range(
                datetime!(2023-08-07 00:00 UTC)
                    ..datetime!(2023-08-08 00:00 UTC),
            )
            .symbols("SPXW.OPT")
            .schema(Schema::Ohlcv1H)
            .build(),
    )
    .await?;
let bar = decoder.decode_record::<OhlcvMsg>().await?.unwrap();
println!("{bar:#?}");
```

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
```

```python
OhlcvMsg {
    hd: RecordHeader {
        length: 14,
        rtype: Ohlcv1H,
        publisher_id: OpraPillarXcbo,
        instrument_id: 587251818,
        ts_event: 1691413200000000000,
    },
    open: 85.060000000,
    high: 85.060000000,
    low: 85.060000000,
    close: 85.060000000,
    volume: 1,
}
```

### DBNStore.to_csv

Write data to a file in CSV format.

#### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| path | PathLike[str] or str | required | The file path to write to. |
| pretty_ts | bool, default True | optional | Whether timestamp columns are converted to tz-aware pandas.Timestamp (UTC). |
| pretty_px | bool, default True | optional | Whether price columns are correctly scaled as display prices. |
| map_symbols | bool, default True | optional | If symbology mappings from the metadata should be used to create a 'symbol' column, mapping the instrument ID to its native symbol for every record. |
| compression | Compression or str | optional | The output compression for writing. Must be either 'zstd' or 'none'. |
| schema | Schema or str | optional | The data record schema for the output CSV. Must be one of the values from list_schemas . This is only required when reading a DBNStore with mixed record types. |
| mode | str | optional | The file write mode to use, either "x" or "w". Defaults to "w". |

#### Returns

```python
DBNStore.to_csv(
    path: PathLike[str] | str,
    pretty_ts: bool = True,
    pretty_px: bool = True,
    map_symbols: bool = True,
    compression: Compression | str = Compression.NONE,
    schema: Schema | str | None = None,
    mode: Literal["w", "x"] = "w",
) -> None
```

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
```

```python
import databento as db

client = db.Historical("$YOUR_API_KEY")

data = client.timeseries.get_range(
    dataset="GLBX.MDP3",
    symbols=["ESM2"],
    schema="trades",
    start="2022-06-06",
)

# Save streamed data to .csv
data.to_csv("GLBX-ESM2-20220606-trades.csv")
```

### AsyncDbnStore::metadata

Get a reference to the decoded DBNMetadata.

#### Returns

A reference to the DBNMetadata.

```python
pub fn metadata(&self) -> &dbn::Metadata;
```

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
18
19
20
21
22
23
24
```

```python
use databento::{
    HistoricalClient,
    dbn::{Dataset, OhlcvMsg, Schema, decode::DbnMetadata},
    historical::timeseries::GetRangeParams,
};
use time::macros::datetime;

let mut client =
    HistoricalClient::builder().key("$YOUR_API_KEY")?.build()?;
let mut decoder = client
    .timeseries()
    .get_range(
        &GetRangeParams::builder()
            .dataset(Dataset::XnasItch)
            .date_time_range(
                datetime!(2023-08-07 00:00 UTC)
                    ..datetime!(2023-08-08 00:00 UTC),
            )
            .symbols("META")
            .schema(Schema::Ohlcv1H)
            .build(),
    )
    .await?;
println!("{:#?}", decoder.metadata());
```

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
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
```

```python
Metadata {
    version: 3,
    dataset: "XNAS.ITCH",
    schema: Some(
        Ohlcv1H,
    ),
    start: 1691366400000000000,
    end: Some(
        1691452800000000000,
    ),
    limit: None,
    stype_in: Some(
        RawSymbol,
    ),
    stype_out: InstrumentId,
    ts_out: false,
    symbol_cstr_len: 71,
    symbols: [
        "META",
    ],
    partial: [],
    not_found: [],
    mappings: [
        SymbolMapping {
            raw_symbol: "META",
            intervals: [
                MappingInterval {
                    start_date: 2023-08-07,
                    end_date: 2023-08-08,
                    symbol: "6508",
                },
            ],
        },
    ],
}
```

### DBNStore.to_df

Converts data to apandasDataFrame.

The DataFrame index will be set tots_recvif it exists in the schema, otherwise it will be set tots_event.

While not optimized for use with live data due to their column-oriented format, pandas DataFrames can still be used with live data by first streaming DBN data to a file, then converting to a DataFrame with DBNStore.from_file().to_df(). Seethis examplefor more information.

#### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| price_type | PriceType or str, default "float" | optional | The price type to use for price fields. If "fixed", prices will have a type of int in fixed decimal format; each unit representing 1e-9 or 0.000000001. If "float", prices will have a type of float . If "decimal", prices will be instances of decimal.Decimal . |
| pretty_ts | bool, default True | optional | Whether timestamp columns are converted to tz-aware pandas.Timestamp . The timezone can be specified using the tz parameter. |
| map_symbols | bool, default True | optional | If symbology mappings from the metadata should be used to create a 'symbol' column, mapping the instrument ID to its raw symbol for every record. |
| schema | Schema or str | optional | The data record schema for the output DataFrame. Must be one of the values from list_schemas . This is only required when reading a DBNStore with mixed record types. |
| tz | datetime.tzinfo or str, default UTC | optional | If pretty_ts is True , all timestamps will be converted to the specified timezone. |
| count | int | optional | If set, instead of returning a single DataFrame a DataFrameIterator instance will be returned. When iterated, this object will yield a DataFrame with at most count elements until the entire contents of the DBNStore are exhausted. |

#### Returns

A pandasDataFrameobject.

```python
DBNStore.to_df(
    price_type: PriceType | str = "float",
    pretty_ts: bool = True,
    map_symbols: bool = True,
    schema: Schema | str | None = None,
    tz: datetime.tzinfo | str = zoneinfo.ZoneInfo("UTC"),
    count: int | None = None,
) -> pd.DataFrame | DataFrameIterator
```

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
```

```python
import databento as db

client = db.Historical("$YOUR_API_KEY")

data = client.timeseries.get_range(
    dataset="GLBX.MDP3",
    schema="trades",
    symbols=["ESM2"],
    start="2022-03-06",
)

df = data.to_df()
print(df.head())
```

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
```

```python
ts_event  rtype  publisher_id  instrument_id action  ... size  flags  ts_in_delta  sequence  symbol
ts_recv                                                                                                             ...
2022-03-06 23:00:00.039463300+00:00 2022-03-06 23:00:00.036436177+00:00      0             1           3403      T  ...    1      0        18828      5178    ESM2
2022-03-06 23:00:01.098111252+00:00 2022-03-06 23:00:01.097477845+00:00      0             1           3403      T  ...    1      0        19122      6816    ESM2
2022-03-06 23:00:04.612334175+00:00 2022-03-06 23:00:04.611714663+00:00      0             1           3403      T  ...    1      0        18687     10038    ESM2
2022-03-06 23:00:04.613776789+00:00 2022-03-06 23:00:04.613240435+00:00      0             1           3403      T  ...    1      0        18452     10045    ESM2
2022-03-06 23:00:06.881864467+00:00 2022-03-06 23:00:06.880575603+00:00      0             1           3403      T  ...    1      0        18478     11343    ESM2

[5 rows x 13 columns]
```

### DBNStore.to_file

Write data to a DBN file.

#### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| path | PathLike[str] or str | required | The file path to write to. |
| mode | str | optional | The file write mode to use, either "x" or "w". Defaults to "w". |
| compression | Compression or str | optional | The compression format to write. If None , uses the same compression as the underlying data. |

#### Returns

ADBNStoreobject.

```python
DBNStore.to_file(
    path: PathLike[str] | str,
    mode: Literal["w", "x"] = "w",
    compression: Compression | str | None = None,
) -> None
```

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
```

```python
import databento as db

client = db.Historical("$YOUR_API_KEY")

data = client.timeseries.get_range(
    dataset="GLBX.MDP3",
    symbols=["ESM2"],
    schema="trades",
    start="2022-06-06",
)

# Save streamed data to .dbn.zst
data.to_file("GLBX-ESM2-20220606.trades.dbn.zst")
```

### pretty::Px

A wrapper class for formatting fixed-precision prices returned from Databento APIs.

It supports configurable precision withstd::setprecision; by default the precision is 9. Width and fill can be configured withstd::setwandstd::setfill.

```python
namespace pretty {
struct Px {
  std::int64_t val;
};
}
```

```python
1
2
3
4
5
6
```

```python
#include <databento/pretty.hpp>
#include <iomanip>
#include <iostream>

std::cout << std::setprecision(2)
          << databento::pretty::Px{4'149'500'000'000} << '\n';
```

```python
1
```

```python
4149.50
```

### DBNStore.to_json

Write data to a file in JSON format.

#### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| path | PathLike[str] or str | required | The file path to write to. |
| pretty_ts | bool, default True | optional | Whether timestamp columns are converted to tz-aware pandas.Timestamp (UTC). |
| pretty_px | bool, default True | optional | Whether price columns are correctly scaled as display prices. |
| map_symbols | bool, default True | optional | If symbology mappings from the metadata should be used to create a 'symbol' column, mapping the instrument ID to its raw symbol for every record. |
| compression | Compression or str | optional | The output compression for writing. Must be either 'zstd' or 'none'. |
| schema | Schema or str | optional | The data record schema for the output JSON. Must be one of the values from list_schemas . This is only required when reading a DBNStore with mixed record types. |
| mode | str | optional | The file write mode to use, either "x" or "w". Defaults to "w". |

#### Returns

```python
DBNStore.to_json(
    path: PathLike[str] | str,
    pretty_ts: bool = True,
    pretty_px: bool = True,
    map_symbols: bool = True,
    compression: Compression | str = Compression.NONE,
    schema: Schema | str | None = None,
    mode: Literal["w", "x"] = "w",
) -> None
```

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
```

```python
import databento as db

client = db.Historical("$YOUR_API_KEY")

data = client.timeseries.get_range(
    dataset="GLBX.MDP3",
    symbols=["ESM2"],
    schema="trades",
    start="2022-06-06",
)

# Save streamed data to .json
data.to_json("GLBX-ESM2-20220606-trades.json")
```

### DBNStore.to_ndarray

Converts data to anumpyN-dimensional array. Each element will contain a Python representation of the binary fields as aTuple.

#### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| schema | Schema or str | optional | The data record schema for the output array. Must be one of the values from list_schemas . This is only required when reading a DBNStore with mixed record types. |
| count | int | optional | If set, instead of returning a single np.ndarray a NDArrayIterator instance will be returned. When iterated, this object will yield a np.ndarray with at most count elements until the entire contents of the DBNStore are exhausted. |

#### Returns

Anumpy.ndarrayobject.

```python
DBNStore.to_ndarray(
    schema: Schema | str | None = None,
    count: int | None = None,
) -> np.ndarray | NDArrayIterator
```

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
```

```python
import databento as db

client = db.Historical("$YOUR_API_KEY")

data = client.timeseries.get_range(
    dataset="GLBX.MDP3",
    symbols=["ESM2"],
    start="2022-06-06",
)

array = data.to_ndarray()
print(array[0].item())
```

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
```

```python
(12,
0,
1,
3403,
1654473600070033767,
4108500000000,
1,
b'T',
b'A',
0,
0,
1654473600070314216,
18681,
157862)
```

### DBNStore.to_parquet

Write data to a file inApache parquetformat.

#### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| path | PathLike[str] or str | required | The file path to write the data to. |
| price_type | PriceType or str, default "float" | optional | The price type to use for price fields. If "fixed", prices will have a type of int in fixed decimal format; each unit representing 1e-9 or 0.000000001. If "float", prices will have a type of float . |
| pretty_ts | bool, default True | optional | Whether timestamp columns are converted to tz-aware pyarrow.TimestampType (UTC). |
| map_symbols | bool, default True | optional | If symbology mappings from the metadata should be used to create a 'symbol' column, mapping the instrument ID to its raw symbol for every record. |
| schema | Schema or str | optional | The data record schema for the output parquet file. Must be one of the values from list_schemas . This is only required when reading a DBNStore with mixed record types. |
| mode | str | optional | The file write mode to use, either "x" or "w". Defaults to "w". |
| **kwargs | Any | optional | Keyword arguments to pass to pyarrow.parquet.ParquetWriter . These can be used to override the default behavior of the writer. |

```python
DBNStore.to_parquet(
    path: PathLike[str] | str,
    price_type: PriceType | str = "float",
    pretty_ts: bool = True,
    map_symbols: bool = True,
    schema: Schema | str | None = None,
    mode: Literal["w", "x"] = "w",
    **kwargs: Any,
) -> None
```

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
```

```python
import databento as db

client = db.Historical("$YOUR_API_KEY")

data = client.timeseries.get_range(
    dataset="GLBX.MDP3",
    symbols=["ESM2"],
    schema="trades",
    start="2022-06-06",
)

# Save streamed data to .parquet
data.to_parquet("GLBX-ESM2-20220606-trades.parquet")
```

### DBNStore.__iter__

Usingfor; records will be iterated one at a time. Iteration will stop when there are no more records in theDBNStoreinstance.

Refer to theList of fields by schemaarticle for documentation on the fields contained with each record type.

```python
DBNStore.__iter__() -> Iterator[DBNRecord]
```

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
```

```python
import databento as db

client = db.Historical("$YOUR_API_KEY")

data = client.timeseries.get_range(
    dataset="GLBX.MDP3",
    symbols=["ESM2"],
    start="2022-06-06",
)

for trade in data:
    size = getattr(trade, "size", 0)
    if size >= 200:
        print(trade)
```

```python
1
2
3
```

```python
TradeMsg(ts_recv=1654524078342408839, pretty_ts_recv='2022-06-06T14:01:18.342408839Z', rtype=<RType.MBP_0: 0>, publisher_id=GLBX.MDP3.GLBX (1), instrument_id=3403, ts_event=1654524078339857609, pretty_ts_event='2022-06-06T14:01:18.339857609Z', action='T', side='B', depth=0, price=4164000000000, pretty_price=4164, size=291, flags=0, ts_in_delta=20352, sequence=3605032)
TradeMsg(ts_recv=1654524133737794739, pretty_ts_recv='2022-06-06T14:02:13.737794739Z', rtype=<RType.MBP_0: 0>, publisher_id=GLBX.MDP3.GLBX (1), instrument_id=3403, ts_event=1654524133736900455, pretty_ts_event='2022-06-06T14:02:13.736900455Z', action='T', side='B', depth=0, price=4160000000000, pretty_price=4160, size=216, flags=0, ts_in_delta=28024, sequence=3659203)
TradeMsg(ts_recv=1654538295589900967, pretty_ts_recv='2022-06-06T17:58:15.589900967Z', rtype=<RType.MBP_0: 0>, publisher_id=GLBX.MDP3.GLBX (1), instrument_id=3403, ts_event=1654538295588752739, pretty_ts_event='2022-06-06T17:58:15.588752739Z', action='T', side='B', depth=0, price=4140000000000, pretty_price=4140, size=200, flags=0, ts_in_delta=21708, sequence=10031624)
```

### DBNStore.insert_symbology_json

Insert JSON symbology data which may be obtained from a symbology request or loaded from a file.

#### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| json_data | str or Mapping[str, Any] or TextIO | required | The JSON data to insert. |
| clear_existing | bool | optional | If existing symbology data should be cleared from the internal mappings. |

```python
DBNStore.insert_symbology_json(
    json_data: str | Mapping[str, Any] | TextIO,
    clear_existing: bool = True,
) -> None
```

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
```

```python
import databento as db

client = db.Historical("$YOUR_API_KEY")

data = client.timeseries.get_range(
    dataset="XNAS.ITCH",
    symbols=["ALL_SYMBOLS"],
    schema="trades",
    start="2022-06-06",
    end="2022-06-07",
)

# Request symbology for all symbols and then insert this data
symbology_json = data.request_symbology(client)
data.insert_symbology_json(symbology_json, clear_existing=True)
```

### map_symbols_csv

Use asymbology.jsonfile to map a symbols column onto an existing CSV file. The result is written toout_file.

#### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| symbology_file | PathLike[str] or str | required | Path to a symbology.json file to use as a symbology source. |
| csv_file | PathLike[str] or str | required | Path to a CSV file that contains encoded DBN data; must contain a ts_recv or ts_event and instrument_id column. |
| out_file | PathLike[str] or str | optional | Path to a file to write results to. If unspecified, _mapped will be appended to the csv_file name. |

#### Returns

Pathto the written file.

```python
map_symbols_csv(
    symbology_file: PathLike[str] | str,
    csv_file: PathLike[str] | str,
    out_file: PathLike[str] | str | None = None,
) -> Path:
```

```python
1
2
3
4
5
6
7
8
```

```python
import databento as db

result = db.map_symbols_csv(
    "symbology.json",
    "xnas-itch-20230821-20230825.ohlcv-1d.csv",
)

print(result.read_text())
```

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
ts_event,rtype,publisher_id,instrument_id,open,high,low,close,volume,symbol
1692576000000000000,35,2,523,133550000000,135200000000,132710000000,134360000000,11015261,AMZN
1692576000000000000,35,2,7290,439090000000,472900000000,437260000000,470990000000,11098972,NVDA
1692576000000000000,35,2,10157,217000000000,233500000000,217000000000,233380000000,21336884,TSLA
1692576000000000000,35,2,7130,430170000000,434700000000,0,433000000000,68661,NOC
1692662400000000000,35,2,7132,431610000000,438480000000,0,437740000000,86950,NOC
1692662400000000000,35,2,10161,236710000000,241550000000,229560000000,232870000000,17069349,TSLA
1692662400000000000,35,2,523,135320000000,135900000000,133740000000,134200000000,8133698,AMZN
1692662400000000000,35,2,7293,475120000000,483440000000,453340000000,457910000000,11700447,NVDA
1692748800000000000,35,2,523,135120000000,137860000000,133220000000,137060000000,11430081,AMZN
1692748800000000000,35,2,7296,463190000000,518870000000,452080000000,502150000000,13361964,NVDA
1692748800000000000,35,2,7135,0,440000000000,0,434030000000,68411,NOC
1692748800000000000,35,2,10163,236590000000,243750000000,226500000000,240810000000,13759234,TSLA
1692835200000000000,35,2,7287,508190000000,512600000000,466720000000,468700000000,21611800,NVDA
1692835200000000000,35,2,10154,242000000000,244140000000,228180000000,229980000000,13724054,TSLA
1692835200000000000,35,2,7126,433650000000,437730000000,0,429880000000,54570,NOC
1692835200000000000,35,2,521,137250000000,137820000000,131410000000,131880000000,11990573,AMZN
```

### map_symbols_json

Use asymbology.jsonfile to insert a symbols key into records of an existing JSON file. The result is written toout_file.

#### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| symbology_file | PathLike[str] or str | required | Path to a symbology.json file to use as a symbology source. |
| json_file | PathLike[str] or str | required | Path to a JSON file that contains encoded DBN data. |
| out_file | PathLike[str] or str | optional | Path to a file to write results to. If unspecified, _mapped will be appended to the csv_file name. |

#### Returns

Pathto the written file.

```python
map_symbols_json(
    symbology_file: PathLike[str] | str,
    json_file: PathLike[str] | str,
    out_file: PathLike[str] | str | None = None,
) -> Path:
```

```python
1
2
3
4
5
6
7
8
```

```python
import databento as db

result = db.map_symbols_json(
    "symbology.json",
    "xnas-itch-20230821-20230825.ohlcv-1d.json",
)

print(result.read_text())
```

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
```

```python
{"hd":{"ts_event":"1692576000000000000","rtype":35,"publisher_id":2,"instrument_id":523},"open":"133550000000","high":"135200000000","low":"132710000000","close":"134360000000","volume":"11015261","symbol":"AMZN"}
{"hd":{"ts_event":"1692576000000000000","rtype":35,"publisher_id":2,"instrument_id":7290},"open":"439090000000","high":"472900000000","low":"437260000000","close":"470990000000","volume":"11098972","symbol":"NVDA"}
{"hd":{"ts_event":"1692576000000000000","rtype":35,"publisher_id":2,"instrument_id":10157},"open":"217000000000","high":"233500000000","low":"217000000000","close":"233380000000","volume":"21336884","symbol":"TSLA"}
{"hd":{"ts_event":"1692576000000000000","rtype":35,"publisher_id":2,"instrument_id":7130},"open":"430170000000","high":"434700000000","low":"0","close":"433000000000","volume":"68661","symbol":"NOC"}
{"hd":{"ts_event":"1692662400000000000","rtype":35,"publisher_id":2,"instrument_id":10161},"open":"236710000000","high":"241550000000","low":"229560000000","close":"232870000000","volume":"17069349","symbol":"TSLA"}
{"hd":{"ts_event":"1692662400000000000","rtype":35,"publisher_id":2,"instrument_id":523},"open":"135320000000","high":"135900000000","low":"133740000000","close":"134200000000","volume":"8133698","symbol":"AMZN"}
{"hd":{"ts_event":"1692662400000000000","rtype":35,"publisher_id":2,"instrument_id":7293},"open":"475120000000","high":"483440000000","low":"453340000000","close":"457910000000","volume":"11700447","symbol":"NVDA"}
{"hd":{"ts_event":"1692662400000000000","rtype":35,"publisher_id":2,"instrument_id":7132},"open":"431610000000","high":"438480000000","low":"0","close":"437740000000","volume":"86950","symbol":"NOC"}
{"hd":{"ts_event":"1692748800000000000","rtype":35,"publisher_id":2,"instrument_id":523},"open":"135120000000","high":"137860000000","low":"133220000000","close":"137060000000","volume":"11430081","symbol":"AMZN"}
{"hd":{"ts_event":"1692748800000000000","rtype":35,"publisher_id":2,"instrument_id":7296},"open":"463190000000","high":"518870000000","low":"452080000000","close":"502150000000","volume":"13361964","symbol":"NVDA"}
{"hd":{"ts_event":"1692748800000000000","rtype":35,"publisher_id":2,"instrument_id":7135},"open":"0","high":"440000000000","low":"0","close":"434030000000","volume":"68411","symbol":"NOC"}
{"hd":{"ts_event":"1692748800000000000","rtype":35,"publisher_id":2,"instrument_id":10163},"open":"236590000000","high":"243750000000","low":"226500000000","close":"240810000000","volume":"13759234","symbol":"TSLA"}
{"hd":{"ts_event":"1692835200000000000","rtype":35,"publisher_id":2,"instrument_id":7287},"open":"508190000000","high":"512600000000","low":"466720000000","close":"468700000000","volume":"21611800","symbol":"NVDA"}
{"hd":{"ts_event":"1692835200000000000","rtype":35,"publisher_id":2,"instrument_id":10154},"open":"242000000000","high":"244140000000","low":"228180000000","close":"229980000000","volume":"13724054","symbol":"TSLA"}
{"hd":{"ts_event":"1692835200000000000","rtype":35,"publisher_id":2,"instrument_id":7126},"open":"433650000000","high":"437730000000","low":"0","close":"429880000000","volume":"54570","symbol":"NOC"}
{"hd":{"ts_event":"1692835200000000000","rtype":35,"publisher_id":2,"instrument_id":521},"open":"137250000000","high":"137820000000","low":"131410000000","close":"131880000000","volume":"11990573","symbol":"AMZN"}
```

### Metadata

The contents of theheader of a DBNstream.

#### Fields

| Field | Type | Description |
| --- | --- | --- |
| version | std::uint8_t | The DBN schema version. |
| dataset | std::string | The dataset code. |
| schema | std::optional<Schema> | The data record schema . Will be nullopt for live data which can mix schemas. |
| start | UnixNanos | The timestamp of the start of request time range (inclusive) expressed as the number nanoseconds since the UNIX epoch . |
| end | UnixNanos | The timestamp of the end of request time range (exclusive) expressed as the number nanoseconds since the UNIX epoch . |
| limit | std::uint64_t | The maximum number of records to return. |
| stype_in | std::optional<SType> | The symbology type of input symbols . Will be nullopt for live data. |
| stype_out | SType | The symbology type of output symbols. |
| ts_out | bool | Whether the stream contains live data with the send timestamps appended to every record. |
| symbol_cstr_len | std::size_t | The length of fixed-length symbol strings. |
| symbols | std::vector<std::string> | The product symbols from the original request. |
| partial | std::vector<std::string> | The symbols that did not resolve for at least one day in the query time range. |
| not_found | std::vector<std::string> | The symbols that did not resolve for any day in the query time range. |
| mappings | std::vector<SymbolMapping> | The symbol mappings for historical data. |

```python
struct MappingInterval {
  date::year_month_day start_date;
  date::year_month_day end_date;
  std::string symbol;
};

struct SymbolMapping {
  std::string raw_symbol;
  std::vector<MappingInterval> intervals;
};

struct Metadata {
  std::uint8_t version;
  std::string dataset;
  std::optional<Schema> schema;
  UnixNanos start;
  UnixNanos end;
  std::uint64_t limit;
  std::optional<SType> stype_in;
  SType stype_out;
  bool ts_out;
  std::size_t symbol_cstr_len;
  std::vector<std::string> symbols;
  std::vector<std::string> partial;
  std::vector<std::string> not_found;
  std::vector<SymbolMapping> mappings;
}
```

### Metadata

The contents of theheader of a DBNstream.

Thecrate documentationfor a comprehensive list of methods and implemented traits.

#### Fields

| Field | Type | Description |
| --- | --- | --- |
| version | u8 | The DBN schema version. |
| dataset | String | The dataset code. |
| schema | Option<Schema> | The data record schema . Will be None for live data which can mix schemas. |
| start | u64 | The timestamp of the start of request time range (inclusive) expressed as the number nanoseconds since the UNIX epoch . |
| end | Option<NonZeroU64> | The timestamp of the end of request time range (exclusive) expressed as the number nanoseconds since the UNIX epoch . Will be None for live data. |
| limit | Option<NonZeroU64> | The maximum number of records to return. |
| stype_in | Option<SType> | The symbology type of input symbols . Will be None for live data. |
| stype_out | SType | The symbology type of output symbols. |
| ts_out | bool | Whether the stream contains live data with the send timestamps appended to every record. |
| symbol_cstr_len | usize | The length of fixed-length symbol strings. |
| symbols | Vec<String> | The product symbols from the original request. |
| partial | Vec<String> | The symbols that did not resolve for at least one day in the query time range. |
| not_found | Vec<String> | The symbols that did not resolve for any day in the query time range. |
| mappings | Vec<SymbolMapping> | The symbol mappings for historical data. |

```python
pub struct Metadata {
    pub version: u8,
    pub dataset: String,
    pub schema: Option<Schema>,
    pub start: u64,
    pub end: Option<NonZeroU64>,
    pub limit: Option<NonZeroU64>,
    pub stype_in: Option<SType>,
    pub stype_out: SType,
    pub ts_out: bool,
    pub symbol_cstr_len: usize,
    pub symbols: Vec<String>,
    pub partial: Vec<String>,
    pub not_found: Vec<String>,
    pub mappings: Vec<SymbolMapping>,
}

pub struct SymbolMapping {
    pub raw_symbol: String,
    pub intervals: Vec<MappingInterval>,
}

pub struct MappingInterval {
    pub start_date: time::Date,
    pub end_date: time::Date,
    pub symbol: String,
}
```

### Metadata::CreateSymbolMap

Create a symbology map from instrument ID and date to text symbol from themappingsin the metadata. Useful for multi-day requests.

#### Returns

ATsSymbolMapwith the symbol mappings for the query range indexed by instrument ID and date.

```python
TsSymbolMap CreateSymbolMap() const;
```

### Metadata::symbol_map

Create a symbology map from instrument ID and date to text symbol from themappingsin the metadata. Useful for multi-day requests.

#### Returns

ATsSymbolMapwith the symbol mappings for the query range indexed by instrument ID and date.

This function returns an error if it fails to parse a symbol mapping into au32instrument ID.

```python
pub fn symbol_map(&self) -> dbn::Result<TsSymbolMap>;
```

### Metadata::CreateSymbolMapForDate

Create a symbology mapping from themappingsin the metadata for the specified date. Useful for requests that span a single day. For multi-day requests, it's better to useMetadata::CreateSymbolMap.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| date | date::year_month_day | The date to create the symbol map for. |

#### Returns

APitSymbolMapwith the symbol mappings for the query range indexed by instrument ID.

```python
PitSymbolMap CreateSymbolMapForDate(
    date::year_month_day date) const;
```

### Metadata::symbol_map_for_date

Create a symbology map from themappingsin the metadata for the specified date. Useful for requests that span a single day. For multi-day requests, it's better to useMetadata::symbol_map.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| date | time::Date | The date to create the symbol map for. |

#### Returns

APitSymbolMapwith the symbol mappings for the query range indexed by instrument ID.

This function returns an error if it fails to parse a symbol mapping into au32instrument ID or the provided date is outside the query range.

```python
pub fn symbol_map_for_date(
    &self,
    date: time::Date,
) -> dbn::Result<PitSymbolMap>;
```

### RecordRef

A wrapper around a non-owning immutable reference to aDBNrecord. This wrapper allows for mixing of record types andschemas, and runtime record polymorphism.

BothAsyncRecordDecoder::decode_record_refandLiveClient::next_recordreturnRecordRefobjects.

Thecrate documentationfor a comprehensive list of methods and implemented traits.

```python
pub struct RecordRef<'a> { /* private fields */ }
```

### RecordRef::header

Get a reference to theRecordHeaderwhich is found at the start of every DBN record. This provides some basic information about the record like instrument ID without first determining its type.

This method is part of theRecordtrait, so you must import the trait to call this method.

#### Returns

An immutable reference to the record's header (RecordHeader).

```python
pub fn header(&self) -> &'a RecordHeader;
```

### RecordRef::rtype

Get the record's record type enum which can be used formatchexpressions with different handling for different types of records.

#### Returns

This function returns an error if the header contains an unknownRType.

```python
pub fn rtype(&self) -> dbn::Result<RType>;
```

### RecordRef::has

Check if the record reference points to a record of a particular type.

#### Returns

Whether the record reference points to a record of typeT.

```python
pub fn has<T: HasRType>(&self) -> bool;
```

### RecordRef::get

Get a reference to a particular record type. Usually paired withif let Some(...)or withhas.

#### Returns

Option<&'a T

A reference to the underlying record of typeTorNoneif theRecordRefpoints to another type.

```python
pub fn get<T: HasRType>(&self) -> Option<&'a T>;
```

### TsSymbolMap

A timeseries symbol map, i.e. instrument IDs to text symbols by date. These objects can be obtained fromMetadata::CreateSymbolMap.

```python
TsSymbolMap();
TsSymbolMap(const Metadata& metadata);
```

### TsSymbolMap

A timeseries symbol map, i.e. instrument IDs to text symbols by date. Useful for working with historical requests over multiple days. These objects can be obtained fromMetadata::symbol_map.

Thecrate documentationfor a comprehensive list of methods and implemented traits.

```python
pub struct TsSymbolMap(/* private fields */);
```

### TsSymbolMap::At

Get the symbol mapping for a record.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| rec | R | The record to fetch a symbol mapping for. |

#### Returns

const std::string&

The corresponding text symbol for the record's instrument ID and timestamp.

Raises an exception if no mapping is found.

```python
template <typename R>
const std::string& At(const R& rec) const;
```

### TsSymbolMap::get_for_rec

Get the symbol mapping for a record.

This method is part of theSymbolIndextrait, so you must import the trait to call this method.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| record | Record | The record to fetch a symbol mapping for. |

#### Returns

Option<&String>

The corresponding text symbol for the record's instrument ID and timestamp.

```python
pub fn get_for_rec<R: Record>(&self, record: &R) -> Option<&String>;
```

### PitSymbolMap

A point-in-time symbol map. Useful for working with real-time symbology or a historical request over a single day and other situations where the symbol mappings are known to not change. These objects can be obtained fromMetadata::CreateSymbolMapForDatefor historical data.

```python
PitSymbolMap();
PitSymbolMap(const Metadata& metadata, date::year_month_day date);
```

### PitSymbolMap

A point-in-time symbol map. Useful for working with real-time symbology or a historical request over a single day and other situations where the symbol mappings are known to not change. These objects can be obtained fromMetadata::symbol_map_for_datefor historical data.

Thecrate documentationfor a comprehensive list of methods and implemented traits.

```python
pub struct PitSymbolMap(/* private fields */);
```

### PitSymbolMap::At

Get the symbol mapping for a record.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| rec | R | The record to fetch a symbol mapping for. |

#### Returns

const std::string&

The corresponding text symbol for the record's instrument ID.

Raises an exception if no mapping is found.

```python
template <typename R>
const std::string& At(const R& rec) const;
```

### PitSymbolMap::get_for_rec

Get the symbol mapping for a record.

This method is part of theSymbolIndextrait, so you must import the trait to call this method.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| record | Record | The record to fetch a symbol mapping for. |

#### Returns

Option<&String>

The corresponding text symbol for the record's instrument ID.

```python
pub fn get_for_rec<R: Record>(&self, record: &R) -> Option<&String>;
```

### PitSymbolMap::OnRecord

Update the symbol map with the contents of the record. OnlySymbolMappingMsgrecords affect the map; all other record types will be ignored.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| rec | Record | The record to update the map from. |

```python
void OnRecord(const Record& rec);
```

### PitSymbolMap::on_record

Update the symbol map with the contents of the record. OnlySymbolMappingMsgrecords affect the map; all other record types will be ignored.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| record | RecordRef | The record to update the map from. |

#### Returns

This function returns an error ifrecordcontains aSymbolMappingMsgwith invalid UTF-8 symbols.

```python
pub fn on_record(&mut self, record: RecordRef) -> dbn::Result<()>;
```

### PitSymbolMap::OnSymbolMapping

Update the symbol map with the contents of the record, either aSymbolMappingMsgor aSymbolMappingMsgV1.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| symbol_mapping | SymbolMappingMsgV1 or SymbolMappingMsg | The record to update the map from. |

```python
void OnSymbolMapping(const SymbolMappingMsgV1& symbol_mapping);
void OnSymbolMapping(const SymbolMappingMsg& symbol_mapping);
```

### PitSymbolMap::on_symbol_mapping

Update the symbol map with the contents of the record, either aSymbolMappingMsgor aSymbolMappingMsgV1.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| symbol_mapping | SymbolMappingRec | The record to update the map from. |

#### Returns

This function returns an error ifrecordcontains invalid UTF-8 symbols.

```python
pub fn on_symbol_mapping<S: SymbolMappingRec>(&mut self, symbol_mapping: &S) -> dbn::Result<()>;
```

### ILogReceiver

TheILogReceiveris an interface for objects that accept log messages from the databento client library. Two implementations are provided, but the interface can be extended for additional configuration.

Implementations

### ILogReceiver::Receive

Receive a log message from the databento client library.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| level | LogLevel | The severity of the log event. |
| msg | std::string | The message describing the event. |

#### Returns

```python
void Receive(LogLevel level, const std::string& msg);
```

### ILogReceiver::Default

Get the defaultILogReceiverimplementation.

#### Returns

ILogReceiver*

Returns a pointer to the default log receiver, aConsoleLogReceiverwhich logs info-level messages and above tostd::clog.

```python
static ILogReceiver* Default();
```

### ConsoleLogReceiver

TheConsoleLogReceiverimplements theILogReceiverinterface forwarding messages to the console, one of the followingstd::ostreamobjects.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| min_level | LogLevel | The minimum severity required to be forwarded to stream . Defaults to Info , meaning Debug messages will be ignored. |
| stream | std::ostream& | The output stream to forward messages to. Defaults to std::clog which writes to standard error. |

```python
ConsoleLogReceiver();
ConsoleLogReceiver(LogLevel min_level);
ConsoleLogReceiver(std::ostream& stream);
ConsoleLogReceiver(LogLevel min_level, std::ostream& stream);
```

### ConsoleLogReceiver::Receive

Receive a log message from the databento client library.

#### Parameters

| Parameter | Type | Description |
| --- | --- | --- |
| level | LogLevel | The severity of the log event. |
| msg | std::string | The message describing the event. |

#### Returns

```python
void Receive(LogLevel level, const std::string& msg);
```

### ListFieldsParams

The parameter struct and builder forHistoricalClient::metadata::list_fields.

The builder can be instantiated with the associated functionbuilder(), and the struct is created from the builder with thebuild()method. For every field, there is an identically named setter method on the builder.

#### Fields

| Field | Type | Description |
| --- | --- | --- |
| encoding | Encoding | The data encoding . Encoding::Dbn is recommended. |
| schema | Schema | The data record schema . Must be one of the values from list_schemas . |
| dataset | Option<String> | The dataset used to determine which fields are relevant. If None then the fields for the latest DBN encoding version are returned, which may differ from a specific dataset's schema. |

```python
pub struct ListFieldsParams {
    pub encoding: Encoding,
    pub schema: Schema,
    pub dataset: Option<String>,
}
```

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
```

```python
use databento::{
    dbn::{Encoding, Schema},
    historical::metadata::ListFieldsParams,
};

assert_eq!(
    ListFieldsParams {
        schema: Schema::Tbbo,
        encoding: Encoding::Csv,
        dataset: None,
    },
    ListFieldsParams::builder()
        .schema(Schema::Tbbo)
        .encoding(Encoding::Csv)
        .build()
);
```

### GetDatasetConditionParams

The parameter struct and builder forHistoricalClient::metadata::get_dataset_condition.

The builder can be instantiated with the associated functionbuilder(), and the struct is created from the builder with thebuild()method. For every field, there is an identically named setter method on the builder.

#### Fields

| Field | Type | Description |
| --- | --- | --- |
| dataset | String | The dataset code (string identifier). Must be one of the values from list_datasets . |
| date_range | Option<DateRange> | The UTC date request range with an inclusive start date and an inclusive end date. If None then will return all available dates. |

```python
pub struct GetDatasetConditionParams {
    pub dataset: String,
    pub date_range: Option<DateRange>,
}
```

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
```

```python
use databento::{
    dbn::Dataset,
    historical::metadata::GetDatasetConditionParams,
};

assert_eq!(
    GetDatasetConditionParams {
        dataset: "XNAS.ITCH".to_owned(),
        date_range: None
    },
    GetDatasetConditionParams::builder()
        .dataset(Dataset::XnasItch)
        .build()
);
```

### GetQueryParams

The parameter struct and builder for several historical metadata endpoints:

The builder can be instantiated with the associated functionbuilder(), and the struct is created from the builder with thebuild()method. For every field, there is an identically named setter method on the builder.

#### Fields

| Parameter | Type | Description |
| --- | --- | --- |
| dataset | String | The dataset code (string identifier). Must be one of the values from list_datasets . |
| symbols | Symbols | The product symbols to filter for. Takes up to 2,000 symbols per request. If Symbols::All then will select all symbols. |
| schema | Schema | The data record schema . Must be one of the values from list_schemas . |
| date_time_range | DateTimeRange | The request range with an inclusive start and an exclusive end. |
| stype_in | SType | The symbology type of input symbols . Defaults to RawSymbol . |
| limit | Option<NonZeroU64> | The maximum number of records to return. If None then no limit. Defaults to None . |

```python
pub struct GetQueryParams {
    pub dataset: String,
    pub symbols: Symbols,
    pub schema: Schema,
    pub date_time_range: DateTimeRange,
    pub stype_in: SType,
    pub limit: Option<NonZeroU64>,
}
pub type GetRecordCountParams = GetQueryParams;
pub type GetBillableSizeParams = GetQueryParams;
pub type GetCostParams = GetQueryParams;
```

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
18
19
20
21
22
23
24
25
26
27
28
```

```python
use databento::{
    dbn::{Dataset, SType, Schema},
    historical::metadata::GetQueryParams,
};
use time::macros::datetime;

assert_eq!(
    GetQueryParams {
        dataset: "OPRA.PILLAR".to_owned(),
        date_time_range: (datetime!(2023-08-01 00:00 UTC)
            ..datetime!(2023-08-08 00:00 UTC))
            .into(),
        symbols: vec!["VIX.OPT".to_owned()].into(),
        schema: Schema::Trades,
        stype_in: SType::Parent,
        limit: None,
    },
    GetQueryParams::builder()
        .dataset(Dataset::OpraPillar)
        .date_time_range(
            datetime!(2023-08-01 00:00 UTC)
                ..datetime!(2023-08-08 00:00 UTC)
        )
        .symbols("VIX.OPT")
        .schema(Schema::Trades)
        .stype_in(SType::Parent)
        .build()
);
```

### GetRangeParams

The parameter struct and builder forHistoricalClient::timeseries::get_range.

The builder can be instantiated with the associated functionbuilder(), and the struct is created from the builder with thebuild()method. For every field, there is an identically named setter method on the builder.

This struct can also be created from aGetRangeToFileParamsstruct via theFromtrait.

#### Fields

| Parameter | Type | Description |
| --- | --- | --- |
| dataset | String | The dataset code (string identifier). Must be one of the values from list_datasets . |
| symbols | Symbols | The product symbols to filter for. Takes up to 2,000 symbols per request. If Symbols::All then will select all symbols. |
| schema | Schema | The data record schema . Must be one of the values from list_schemas . |
| date_time_range | DateTimeRange | The request range with an inclusive start and an exclusive end. Filters on ts_recv if it exists in the schema, otherwise ts_event . |
| stype_in | SType | The symbology type of input symbols . Defaults to RawSymbol . |
| stype_out | SType | The symbology type of output symbols. Defaults to InstrumentId . Must be a valid symbology combination with stype_in . See symbology combinations . |
| limit | Option<NonZeroU64> | The maximum number of records to return. If None then no limit. Defaults to None . |

```python
pub struct GetRangeParams {
    pub dataset: String,
    pub symbols: Symbols,
    pub schema: Schema,
    pub date_time_range: DateTimeRange,
    pub stype_in: SType,
    pub stype_out: SType,
    pub limit: Option<NonZeroU64>,
}
```

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
18
19
20
21
22
23
24
25
26
27
28
29
30
```

```python
use databento::{
    dbn::{Dataset, SType, Schema, VersionUpgradePolicy},
    historical::timeseries::GetRangeParams,
};
use time::macros::datetime;

assert_eq!(
    GetRangeParams {
        dataset: "XNAS.ITCH".to_owned(),
        date_time_range: (datetime!(2023-11-03 14:00 -4)
            ..datetime!(2023-11-03 16:00 -4))
            .into(),
        symbols: "NVDA".into(),
        schema: Schema::Trades,
        stype_in: SType::RawSymbol,
        stype_out: SType::InstrumentId,
        limit: None,
        #[expect(deprecated)]
        upgrade_policy: None,
    },
    GetRangeParams::builder()
        .dataset(Dataset::XnasItch)
        .symbols("NVDA")
        .date_time_range(
            datetime!(2023-11-03 14:00 -4)
                ..datetime!(2023-11-03 16:00 -4)
        )
        .schema(Schema::Trades)
        .build()
);
```

### GetRangeToFileParams

The parameter struct and builder forHistoricalClient::timeseries::get_range_to_file.

The builder can be instantiated with the associated functionbuilder(), and the struct is created from the builder with thebuild()method. For every field, there is an identically named setter method on the builder.

This struct can also be created from aGetRangeParamsstruct via theGetRangeParams::with_path()method.

#### Fields

| Parameter | Type | Description |
| --- | --- | --- |
| dataset | String | The dataset code (string identifier). Must be one of the values from list_datasets . |
| symbols | Symbols | The product symbols to filter for. Takes up to 2,000 symbols per request. If Symbols::All then will select all symbols. |
| schema | Schema | The data record schema . Must be one of the values from list_schemas . |
| date_time_range | DateTimeRange | The request range with an inclusive start and an exclusive end. Filters on ts_recv if it exists in the schema, otherwise ts_event . |
| stype_in | SType | The symbology type of input symbols . Defaults to RawSymbol . |
| stype_out | SType | The symbology type of output symbols. Defaults to InstrumentId . Must be a valid symbology combination with stype_in . See symbology combinations . |
| limit | Option<NonZeroU64> | The maximum number of records to return. If None then no limit. Defaults to None . |
| path | PathBuf | The file path to persist the stream data to. |

```python
pub struct GetRangeToFileParams {
    pub dataset: String,
    pub symbols: Symbols,
    pub schema: Schema,
    pub date_time_range: DateTimeRange,
    pub stype_in: SType,
    pub stype_out: SType,
    pub limit: Option<NonZeroU64>,
    pub path: PathBuf,
}
```

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
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
```

```python
use std::path::PathBuf;

use databento::{
    dbn::{Dataset, SType, Schema, VersionUpgradePolicy},
    historical::timeseries::GetRangeToFileParams,
};
use time::macros::datetime;

assert_eq!(
    GetRangeToFileParams {
        dataset: Dataset::IfeuImpact.to_string(),
        date_time_range: (datetime!(2024-05-17 00:00 UTC)
            ..datetime!(2024-05-20 00:00 UTC))
            .into(),
        symbols: "BRN.OPT".into(),
        schema: Schema::Statistics,
        stype_in: SType::Parent,
        stype_out: SType::InstrumentId,
        limit: None,
        #[expect(deprecated)]
        upgrade_policy: None,
        path: PathBuf::from(
            "ifeu-impact.statistics.20240517.dbn.zst"
        ),
    },
    GetRangeToFileParams::builder()
        .dataset(Dataset::IfeuImpact)
        .symbols("BRN.OPT")
        .stype_in(SType::Parent)
        .date_time_range(
            datetime!(2024-05-17 00:00 UTC)
                ..datetime!(2024-05-20 00:00 UTC)
        )
        .schema(Schema::Statistics)
        .path("ifeu-impact.statistics.20240517.dbn.zst")
        .build()
);
```

### ResolveParams

The parameter struct and builder forHistoricalClient::symbology::resolve.

The builder can be instantiated with the associated functionbuilder(), and the struct is created from the builder with thebuild()method. For every field, there is an identically named setter method on the builder.

#### Fields

| Parameter | Type | Description |
| --- | --- | --- |
| dataset | String | The dataset code (string identifier). Must be one of the values from list_datasets . |
| symbols | Symbols | The symbols to filter for. Takes up to 2,000 symbols per request. If Symbols::All then will select all symbols (not available for every dataset). |
| stype_in | SType | The symbology type of input symbols . Defaults to RawSymbol . |
| stype_out | SType | The symbology type of output symbols. Defaults to InstrumentId . Must be a valid symbology combination with stype_in . See symbology combinations . |
| date_range | DateRange | The UTC date range with an inclusive start and an exclusive end. |

```python
pub struct ResolveParams {
    pub dataset: String,
    pub symbols: Symbols,
    pub stype_in: SType,
    pub stype_out: SType,
    pub date_range: DateRange,
}
```

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
18
19
20
21
22
```

```python
use databento::{
    dbn::{Dataset, SType},
    historical::symbology::ResolveParams,
};
use time::macros::date;

assert_eq!(
    ResolveParams {
        dataset: "XNAS.ITCH".to_owned(),
        date_range: (date!(2020 - 01 - 01)
            ..date!(2022 - 01 - 01))
            .into(),
        symbols: vec!["IWM", "SPY", "QQQ"].into(),
        stype_in: SType::RawSymbol,
        stype_out: SType::InstrumentId,
    },
    ResolveParams::builder()
        .dataset(Dataset::XnasItch)
        .symbols(vec!["IWM", "SPY", "QQQ"])
        .date_range(date!(2020 - 01 - 01)..date!(2022 - 01 - 01))
        .build()
);
```

### SubmitJobParams

The parameter struct and builder forHistoricalClient::batch::submit_job.

The builder can be instantiated with the associated functionbuilder(), and the struct is created from the builder with thebuild()method. For every field, there is an identically named setter method on the builder.

#### Fields

| Parameter | Type | Description |
| --- | --- | --- |
| dataset | String | The dataset code (string identifier). Must be one of the values from list_datasets . |
| symbols | Symbols | The product symbols to filter for. Takes up to 2,000 symbols per request. If Symbols::All then will select all symbols. |
| schema | Schema | The data record schema . Must be one of the values from list_schemas . |
| date_time_range | DateTimeRange | The request range with an inclusive start and an exclusive end. Filters on ts_recv if it exists in the schema, otherwise ts_event . |
| encoding | Encoding | The data encoding . Defaults to Dbn . |
| compression | Compression | The data compression mode. For fastest transfer speed, Zstd is recommended. Defaults to Zstd . |
| pretty_px | bool | If prices should be formatted to the correct scale (using the fixed-precision scalar 1e-9). Only applicable for Csv or Json encodings. Defaults to false . |
| pretty_ts | bool | If timestamps should be formatted as ISO 8601 strings. Only applicable for Csv or Json encodings. Defaults to false . |
| map_symbols | Option<bool> | If a symbol field should be included with each text-encoded record. Defaults to true for Csv or Json encodings, and false for Dbn . |
| split_symbols | bool | If files should be split by raw symbol. Cannot be used with limit . Defaults to false . |
| split_duration | SplitDuration | The maximum time duration before batched data is split into multiple files. A week starts on Sunday UTC. None means no time-based splitting. Defaults to Day . |
| split_size | Option<NonZeroU64> | The maximum size (in bytes) of each batched data file before being split. Must be an integer between 1e9 and 10e9 inclusive (1GB - 10GB). Defaults to None . |
| delivery | Delivery | The delivery mechanism for the batched data files once processed. Only Download is supported at this time. |
| stype_in | SType | The symbology type of input symbols . Defaults to RawSymbol . |
| stype_out | SType | The symbology type of output symbols. Defaults to InstrumentId . Must be a valid symbology combination with stype_in . See symbology combinations . |
| limit | Option<NonZeroU64> | The maximum number of records to return. If None then no limit. Cannot be used with split_symbols . |

```python
pub struct SubmitJobParams {
    pub dataset: String,
    pub symbols: Symbols,
    pub schema: Schema,
    pub date_time_range: DateTimeRange,
    pub encoding: Encoding,
    pub compression: Compression,
    pub pretty_px: bool,
    pub pretty_ts: bool,
    pub map_symbols: Option<bool>,
    pub split_symbols: bool,
    pub split_duration: SplitDuration,
    pub split_size: Option<NonZeroU64>,
    pub delivery: Delivery,
    pub stype_in: SType,
    pub stype_out: SType,
    pub limit: Option<NonZeroU64>,
}
```

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
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
```

```python
use databento::{
    dbn::{Compression, Dataset, Encoding, SType, Schema},
    historical::batch::{
        Delivery, SplitDuration, SubmitJobParams,
    },
};
use time::macros::datetime;

assert_eq!(
    SubmitJobParams {
        dataset: "GLBX.MDP3".to_owned(),
        date_time_range: (datetime!(2019-01-01 00:00 UTC)
            ..datetime!(2020-09-03 00:00 UTC))
            .into(),
        symbols: vec!["CL.c.0", "NG.c.0"].into(),
        schema: Schema::Ohlcv1M,
        stype_in: SType::Continuous,
        stype_out: SType::InstrumentId,
        limit: None,
        encoding: Encoding::Csv,
        compression: Compression::None,
        pretty_px: true,
        pretty_ts: true,
        map_symbols: Some(true),
        split_symbols: false,
        split_duration: SplitDuration::Day,
        split_size: None,
        delivery: Delivery::Download,
    },
    SubmitJobParams::builder()
        .dataset(Dataset::GlbxMdp3)
        .symbols(vec!["CL.c.0", "NG.c.0"])
        .stype_in(SType::Continuous)
        .date_time_range(
            datetime!(2019-01-01 00:00 UTC)
                ..datetime!(2020-09-03 00:00 UTC)
        )
        .schema(Schema::Ohlcv1M)
        .encoding(Encoding::Csv)
        .compression(Compression::None)
        .pretty_px(true)
        .pretty_ts(true)
        .map_symbols(true)
        .build()
);
```

### ListJobsParams

The parameter struct and builder forHistoricalClient::batch::list_jobsandlist_jobs_full.

The builder can be instantiated with the associated functionbuilder(), and the struct is created from the builder with thebuild()method. For every field, there is an identically named setter method on the builder.

#### Fields

| Parameter | Type | Description |
| --- | --- | --- |
| states | Option<Vec<JobState>> | The filter for job states. Can include Queued , Processing , Done , and Expired . If None , defaults to all except Expired . |
| since | Option<time::OffsetDateTime> | The filter for timestamp submitted (will not include jobs prior to this). |

```python
pub struct ListJobsParams {
    pub states: Option<Vec<JobState>>,
    pub since: Option<OffsetDateTime>,
}
```

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
```

```python
use databento::historical::batch::{JobState, ListJobsParams};
use time::macros::datetime;

assert_eq!(
    ListJobsParams {
        states: Some(vec![JobState::Done]),
        since: Some(datetime!(2023-11-06 00:00 UTC))
    },
    ListJobsParams::builder()
        .states(vec![JobState::Done])
        .since(datetime!(2023-11-06 00:00 UTC))
        .build()
);
```

### DownloadParams

The parameter struct and builder forHistoricalClient::batch::download.

The builder can be instantiated with the associated functionbuilder(), and the struct is created from the builder with thebuild()method. For every field, there is an identically named setter method on the builder.

#### Fields

| Parameter | Type | Description |
| --- | --- | --- |
| output_dir | PathBuf | The directory to download the file(s) to. |
| job_id | String | The batch job identifier. |
| filename_to_download | Option<String> | The specific file to download. If None then will download all files for the batch job. |

```python
pub struct DownloadParams {
    pub output_dir: PathBuf,
    pub job_id: String,
    pub filename_to_download: Option<String>,
}
```

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
```

```python
use std::path::PathBuf;

use databento::historical::batch::DownloadParams;
use time::macros::datetime;

assert_eq!(
    DownloadParams {
        output_dir: PathBuf::from("/tmp"),
        job_id: "GLBX-20230926-ANMGJK7JB6".to_owned(),
        filename_to_download: None,
    },
    DownloadParams::builder()
        .output_dir("/tmp")
        .job_id("GLBX-20230926-ANMGJK7JB6")
        .build()
);
```
