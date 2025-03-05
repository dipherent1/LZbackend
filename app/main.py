from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# Add CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the JSON gene and ld data
try:
    with open('./data/genes.json', 'r') as f:
        genes_data = json.load(f)
    with open('./data/ld.json', 'r') as f:
        ld_data = json.load(f)
    with open('./data/ann.recomb.json', 'r') as f:
        ann_recomb_data = json.load(f)
    with open('./data/single.results.json', 'r') as f:
        single_results_data = json.load(f)

except FileNotFoundError as e:
    raise Exception(f"Data file not found: {e.filename}")
except json.JSONDecodeError:
    raise Exception("Invalid JSON format in data file")

@app.get("/genes")
async def get_genes(
    chrom: str = Query(None, description="Chromosome filter"),
    start: int = Query(None, description="Start position"),
    end: int = Query(None, description="End position")
):
    filtered_genes = []
    for gene in genes_data['data']:
        # Apply filters
        if chrom and gene.get('chrom') != chrom:
            continue
        if start and gene.get('end') < start:
            continue
        if end and gene.get('start') > end:
            continue
        filtered_genes.append(gene)

    return {
        "data": filtered_genes,
        "lastPage": None,
        "meta": genes_data['meta']
    }

@app.get("/ld/genome_builds/{genome_build}/references/{reference}/populations/{population}/variants")
async def get_ld(
    genome_build: str,
    reference: str,
    population: str,
    variant: str = Query(..., description="Variant ID"),
    chrom: str = Query(None, description="Chromosome filter"),
    start: int = Query(None, description="Start position"),
    stop: int = Query(None, description="End position"),
    correlation: str = Query("rsquare", description="Correlation type")
):
    filtered_ld = []
    for entry in ld_data['data']:
        # Convert string to dictionary if needed
        if isinstance(entry, str):
            try:
                entry = json.loads(entry)
            except json.JSONDecodeError:
                continue
                
        # Match variant exactly
        if entry.get('variant1') != variant:
            continue
            
        # Chromosome filter
        if chrom and entry.get('chrom') != chrom:
            continue
            
        # Position range filter
        pos = entry.get('pos')
        if start and pos < start:
            continue
        if stop and pos > stop:
            continue
            
        # Format the entry as LocusZoom expects
        filtered_entry = {
            'variant1': entry.get('variant1'),
            'variant2': entry.get('variant2'),
            'position': entry.get('pos'),
            'chromosome': entry.get('chrom'),
            correlation: entry.get(correlation, 0)  # Default to 0 if correlation not found
        }
        filtered_ld.append(filtered_entry)

    # Structure the response as LocusZoom expects
    return {
        "data": filtered_ld,
        "lastPage": None,  # Required by LocusZoom
        "error": None,     # Required by LocusZoom
        "next": None,      # Required by LocusZoom
        "meta": {
            "name": "LD",
            "type": "ld",
            "source": "local"
        }
    }

