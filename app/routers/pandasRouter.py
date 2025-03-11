from fastapi import FastAPI, Query, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import json
from fastapi.responses import JSONResponse
import gzip

import pandas as pd

# def read_vcf_pandas(file_path):
#     # Read file while skipping meta-information lines (starting with '##')
#     df = pd.read_csv(file_path, comment='#', delimiter='\t', header=None)

#     # Assign proper column names
#     df.columns = ["CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "INFO", "FORMAT"] + [f"SAMPLE{i}" for i in range(1, len(df.columns)-9+1)]

#     return df

# # Example usage
# vcf_df = read_vcf_pandas("data/ALL.chr16.shapeit2_integrated_snvindels_v2a_27022019.GRCh38.phased.vcf")
# print(vcf_df.head())

pandasRouter = APIRouter(
    prefix="/pandas",
    tags=["pandas"],
)

@pandasRouter.get("/genes")
async def get_genes(
    chrom: str = Query(None, description="Chromosome filter"),
    start: int = Query(None, description="Start position"),
    end: int = Query(None, description="End position"),
    limit: int = Query(100, description="Maximum number of results to return")
):
    filtered_variants = []
    
    # Path to the gzipped VCF file
    vcf_file = "data/ALL.chr16.shapeit2_integrated_snvindels_v2a_27022019.GRCh38.phased.vcf.gz"

    try:
        # Open and read the gzipped file line by line
        with gzip.open(vcf_file, "rt") as f:
            for line in f:
                if line.startswith("#"):
                    continue  # Skip metadata and header lines
                
                fields = line.strip().split("\t")
                
                # Parse necessary fields
                record = {
                    "CHROM": fields[0],
                    "POS": int(fields[1]),
                    "ID": fields[2],
                    "REF": fields[3],
                    "ALT": fields[4],
                    "QUAL": float(fields[5]) if fields[5] != "." else None  # Handle missing quality values
                }

                # Apply query filters
                if chrom and record["CHROM"] != chrom:
                    continue
                if start and record["POS"] < start:
                    continue
                if end and record["POS"] > end:
                    continue

                filtered_variants.append(record)

                # Stop if we reach the limit
                if len(filtered_variants) >= limit:
                    break

        return JSONResponse(content={"data": filtered_variants, "meta": {"count": len(filtered_variants)}})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@pandasRouter.get("/test/genes")
async def get_genes(
    chrom: str = Query(None, description="Chromosome filter"),
    start: int = Query(None, description="Start position"),
    end: int = Query(None, description="End position"),
    limit: int = Query(100, description="Maximum number of results to return")
):
    filtered_variants = []
    vcf_file = "data/HG00098.vcf.gz"  # Use the small test file

    try:
        with gzip.open(vcf_file, "rt") as f:
            for line in f:
                if line.startswith("#"):
                    continue  # Skip headers
                
                fields = line.strip().split("\t")
                 # **Check if the line has at least 8 required columns**
                if len(fields) < 8 or not fields[0].isdigit():
                    print(f"Skipping corrupted line: {line.strip()}")
                    continue
                
                record = {
                    "CHROM": fields[0],
                    "POS": int(fields[1]),
                    "ID": fields[2],
                    "REF": fields[3],
                    "ALT": fields[4],
                    "QUAL": float(fields[5]) if fields[5] != "." else None
                }

                # Apply filters
                if chrom and record["CHROM"] != chrom:
                    continue
                if start and record["POS"] < start:
                    continue
                if end and record["POS"] > end:
                    continue
                
                print(f"recorded line: {record}")
                filtered_variants.append(record)

                # Stop early when limit is reached
                if len(filtered_variants) >= limit:
                    break

        return JSONResponse(content={"data": filtered_variants, "meta": {"count": len(filtered_variants)}})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)