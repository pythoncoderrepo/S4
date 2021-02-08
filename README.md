## A Framework for Statistically-Sound Customer Segment Search
#### I. Approach
> 1. First we use our *PivotHandler* to split the data into a reference set and a holdout set
> 2. Each set is then split with *SegmentationHandler* to have multiple candidates on each set
> 3. We evaluate each subset of the holdout and reference segment with a statistical test using *StatisticalTestHandler


#### II. Structure
> - The classes implementation is in ```source_code/core```
> - To run queries use notebook in ```source_code/notebook```

