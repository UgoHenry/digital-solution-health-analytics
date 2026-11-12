import os
import time
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# 1. File Paths (Update path if your full CSV is located elsewhere)
csv_path = "powerbi/analysis_sample.csv"
parquet_path = "data/full_survey_compressed.parquet"
os.makedirs("data", exist_ok=True)

if not os.path.exists(csv_path):
    # Fallback search if located in root or data/
    for alt in ["analysis_sample.csv", "data/analysis_sample.csv"]:
        if os.path.exists(alt):
            csv_path = alt
            break

print(f"Source CSV: {csv_path}")
print(f"Target Parquet: {parquet_path}\n")

# 2. Convert CSV to Parquet in Chunks using PyArrow ParquetWriter
chunk_size = 50_000
writer = None
schema = None

print("Converting CSV to Parquet in chunks...")
start_conv = time.time()

for i, chunk in enumerate(pd.read_csv(csv_path, chunksize=chunk_size)):
    # Enforce consistent types across chunks before converting to PyArrow Table
    table = pa.Table.from_pandas(chunk, preserve_index=False)

    if writer is None:
        schema = table.schema
        writer = pq.ParquetWriter(parquet_path, schema, compression='snappy')

    # Cast chunk to match the initial schema (prevents null-column type mismatches across chunks)
    table = table.cast(schema)
    writer.write_table(table)
    print(f"  -> Processed chunk {i + 1} ({len(chunk):,} rows)")

if writer:
    writer.close()

conv_time = time.time() - start_conv
print(f"Conversion complete in {conv_time:.2f} seconds.\n")

# 3. Measure File Sizes (in Megabytes)
csv_size_mb = os.path.getsize(csv_path) / (1024 * 1024)
parquet_size_mb = os.path.getsize(parquet_path) / (1024 * 1024)
space_saved_pct = (1 - (parquet_size_mb / csv_size_mb)) * 100

# 4. Benchmark Single-Column Read Speed ('SYSTOLIC_BP')
target_col = 'SYSTOLIC_BP'

# Time CSV single-column read
t0 = time.time()
_ = pd.read_csv(csv_path, usecols=[target_col])
csv_read_time = time.time() - t0

# Time Parquet single-column read (columnar projection)
t0 = time.time()
_ = pd.read_parquet(parquet_path, columns=[target_col])
parquet_read_time = time.time() - t0

speedup_factor = csv_read_time / parquet_read_time if parquet_read_time > 0 else 0

# 5. Output Comparison Table
comparison = pd.DataFrame([
    {
        "Format": "CSV (Uncompressed Text)",
        "File Size (MB)": round(csv_size_mb, 2),
        "Single-Column Read (s)": round(csv_read_time, 4),
        "Relative Efficiency": "Baseline (1.0x)"
    },
    {
        "Format": "Parquet (Snappy Columnar)",
        "File Size (MB)": round(parquet_size_mb, 2),
        "Single-Column Read (s)": round(parquet_read_time, 4),
        "Relative Efficiency": f"{space_saved_pct:.1f}% smaller | {speedup_factor:.1f}x faster read"
    }
])

print("=== Storage & Read Speed Benchmark (US-12) ===")
print(comparison.to_string(index=False))