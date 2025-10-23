# Data Quality Summary (Week 4–6)

## TMDb (100 movies)
- **Columns:** 12 | **Rows:** 100
- **Missing data:** 15% overall
  - `cast_top3`: 85% missing
  - `director`: 95% missing
  - `genres`: 2% missing
- **Budget stats:** mean = $14.9M, max = $98M
- **Notes:** Numeric fields valid; incomplete crew/cast data due to Kaggle extraction.

## Rotten Tomatoes (OMDb) (50 movies)
- **Columns:** 5 | **Rows:** 50
- **Missing data:** `rt_score` 8%, `metascore` 34%
- **IMDb rating:** mean ≈ 7.0
- **Notes:** Good coverage, some missing critic scores for older titles.

## Overall Assessment
✅ Data structure validated, no duplicates.  
⚠️ Missing metadata in cast/director and Metascore columns.  
✅ Ready for normalization and integration (Week 7–9).
