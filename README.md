# Introduction

This repo stems from the [biothings-data-parser-sample](https://github.com/TelentiLab/biothings-data-parser-sample) code, and is used to parse SpliceAI data for Biothings Studio. A small sample dataset is also provided.

## Sample Entry

```json
{
    "_id": "chr10:g.13655739A>C",
    "splice_ai": {
        "chrom": "10",
        "pos": 13655739,
        "ref": "A",
        "alt": "C",
        "data": [
            {
                "hgnc_gene": "PRPF18",
                "pos_strand": true,
                "is_exon": false,
                "distance": 2,
                "acceptor_gain": {
                    "score": 0.6048,
                    "position": 27
                },
                "acceptor_loss": {
                    "score": 0.9898,
                    "position": 2
                },
                "donor_gain": {
                    "score": 0.0001,
                    "position": 21
                },
                "donor_loss": {
                    "score": 0.0000,
                    "position": -24
                }          
            },
            ...
        ]
    }
}
```

SYMBOL,Type=String,Description="HGNC gene symbol"
STRAND,Type=String,Description="+ or - depending on whether the gene lies in the positive or negative strand">
TYPE,Number=1,Type=String,Description="E or I depending on whether the variant position is exonic or intronic (GENCODE V24lift37 canonical annotation)">
DIST,Number=1,Type=Integer,Description="Distance between the variant position and the closest splice site (GENCODE V24lift37 canonical annotation)">
DS_AG,Number=1,Type=Float,Description="Delta score (acceptor gain)">
DS_AL,Number=1,Type=Float,Description="Delta score (acceptor loss)">
DS_DG,Number=1,Type=Float,Description="Delta score (donor gain)">
DS_DL,Number=1,Type=Float,Description="Delta score (donor loss)">
DP_AG,Number=1,Type=Integer,Description="Delta position (acceptor gain) relative to the variant position">
DP_AL,Number=1,Type=Integer,Description="Delta position (acceptor loss) relative to the variant position">
DP_DG,Number=1,Type=Integer,Description="Delta position (donor gain) relative to the variant position">
DP_DL,Number=1,Type=Integer,Description="Delta position (donor loss) relative to the variant position">