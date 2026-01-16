{{ config(materialized='table') }}

WITH source_data AS (
    -- Read from the raw table created by loader.py
    SELECT * FROM {{ source('raw_layer', 'source_coingecko') }}
)

SELECT
    id AS coin_id,
    symbol,
    name,
    -- Cast columns to correct types
    current_price::numeric AS current_price_usd,
    market_cap::bigint AS market_cap_usd,
    market_cap_rank::int,
    last_updated::timestamp AS last_updated_ts,
    extracted_at::timestamp AS extracted_at_ts
FROM source_data  