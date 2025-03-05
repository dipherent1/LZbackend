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

# Load the JSON data
with open('./data/genes.json', 'r') as f:
    genes_data = json.load(f)

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