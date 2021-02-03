## A Framework for Statistically-Sound Customer Segment Search

#### I. Approach

> 1. First we use our *PivotHandler* to split the data into a reference set and a holdout set
> 2. Each set is then split with *SegmentationHandler* to have multiple candidates on each set
> 3. We evaluate each subset of the holdout and reference segment with a statistical test using *StatisticalTestHandler*

#### II. Structure

> - The main classes are in ```src/core```
> - To run queries use notebooks in ```src/notebook```
> - Amazon, Tafeng and Sales dataset are stored in csv files in ```data/```
> - All the detailed results could be found in  ```experiments/results```

#### III. Queries results

> | dataset   | query#   | pivot        | segmentation                   |   alpha |   #(h,e) |   #e |   #h |   #results |   #result(Bonferoni) |   coverage |        min-p |       budget |
>|:----------|:---------|:-------------|:-------------------------------|--------:|---------:|-----:|-----:|-----------:|---------------------:|-----------:|-------------:|-------------:|
>| Tafeng    | #Q3      | Promotion    | PWindow_2K                     |    0.05 |    27940 |  117 |  294 |          0 |                    0 |          0 | 1            |  0           |
>| Tafeng    | #Q3      | Promotion    | PWindow_30K                    |    0.05 |      151 |    8 |   20 |          0 |                    0 |          0 | 1            |  0           |
>| Tafeng    | #Q3      | Promotion    | PWindow_35K                    |    0.05 |      103 |    7 |   17 |          0 |                    0 |          0 | 1            |  0           |
>| Tafeng    | #Q3      | Promotion    | TWindow_3W                     |    0.05 |       11 |    3 |    5 |          0 |                    0 |          0 | 1            |  0           |
>| Tafeng    | #Q9      | Demographics | PWindow_30K                    |    0.05 |      111 |   23 |    6 |          3 |                    3 |         64 | 0.000133853  |  0.00155844  |
>| Tafeng    | #Q9      | Demographics | PWindow_30K                    |    0.01 |      111 |   23 |    6 |          3 |                    3 |         64 | 0.000133853  |  0.00155844  |
>| Retail    | #Q7      | Demographics | Demographics_[location,gender] |    0.01 |     1904 |   61 |   41 |          7 |                    7 |       2109 | 6.29233e-20  |  0.0228912   |
>| Retail    | #Q7      | Demographics | Demographics_location          |    0.01 |     1904 |   61 |   41 |          7 |                    7 |       2109 | 6.29233e-20  |  0.0228912   |
>| Retail    | #Q4      | Promotion    | Demographics_location          |    0.01 |     2392 |   54 |   58 |          8 |                    8 |       2790 | 1.74887e-90  |  0.000850895 |
>| Retail    | #Q7      | Demographics | Demographics_[location,gender] |    0.05 |     1904 |   61 |   41 |          8 |                    8 |       2109 | 6.29233e-20  |  0.0582079   |
>| Retail    | #Q7      | Demographics | Demographics_location          |    0.05 |     1904 |   61 |   41 |          8 |                    8 |       2109 | 6.29233e-20  |  0.0582079   |
>| Retail    | #Q9      | Demographics | PWindow_10K                    |    0.01 |       69 |   23 |    3 |         12 |                   11 |         59 | 9.53375e-34  |  0.00855199  |
>| Retail    | #Q4      | Promotion    | Demographics_location          |    0.05 |     2392 |   54 |   58 |         12 |                   12 |       2790 | 1.74887e-90  |  0.0800351   |
>| Retail    | #Q9      | Demographics | PWindow_10K                    |    0.05 |       69 |   23 |    3 |         13 |                   12 |         62 | 9.53375e-34  |  0.0523025   |
>| Retail    | #Q4      | Promotion    | Demographics_[location,gender] |    0.01 |      272 |   16 |   17 |         15 |                   15 |        265 | 1.67096e-46  |  5.43818e-06 |
>| Retail    | #Q4      | Promotion    | Demographics_[location,gender] |    0.05 |      272 |   16 |   17 |         15 |                   15 |        265 | 1.67096e-46  |  5.43818e-06 |
>| Amazon    | #Q3      | Promotion    | PWindow_10K                    |    0.05 |      840 |   14 |   60 |         24 |                   24 |        778 | 1.29091e-175 |  8.773e-05   |
>| Amazon    | #Q3      | Promotion    | PWindow_10K                    |    0.01 |      840 |   14 |   60 |         24 |                   24 |        778 | 1.29091e-175 |  8.773e-05   |
>| Amazon    | #Q3      | Promotion    | PWindow_10K                    |    0.01 |      840 |   14 |   60 |         24 |                   24 |        778 | 1.29091e-175 |  8.773e-05   |
>| Amazon    | #Q3      | Promotion    | PWindow_10K                    |    0.05 |      840 |   14 |   60 |         24 |                   24 |        778 | 1.29091e-175 |  8.773e-05   |
>| Retail    | #Q3      | Promotion    | PWindow_2K                     |    0.05 |     2916 |   36 |   81 |         37 |                   37 |       2839 | 1.28508e-43  |  0.0125915   |
>| Retail    | #Q3      | Promotion    | PWindow_2K                     |    0.01 |     2916 |   36 |   81 |         37 |                   34 |       2839 | 1.28508e-43  |  0.0125915   |
>| Retail    | #Q9      | Demographics | PWindow_200                    |    0.01 |      258 |   43 |    6 |         46 |                   34 |        256 | 4.90681e-12  |  0.0656165   |
>| Amazon    | #Q3      | Promotion    | PWindow_5K                     |    0.01 |     3240 |   27 |  120 |         50 |                   49 |       3116 | 6.13579e-202 |  0.00807274  |
>| Amazon    | #Q3      | Promotion    | PWindow_5K                     |    0.05 |     3240 |   27 |  120 |         50 |                   49 |       3116 | 6.13579e-202 |  0.00807274  |
>| Amazon    | #Q3      | Promotion    | PWindow_5K                     |    0.01 |     3240 |   27 |  120 |         50 |                   49 |       3116 | 6.13579e-202 |  0.00807274  |
>| Amazon    | #Q3      | Promotion    | PWindow_5K                     |    0.05 |     3240 |   27 |  120 |         50 |                   49 |       3116 | 6.13579e-202 |  0.00807274  |
>| Retail    | #Q9      | Demographics | PWindow_200                    |    0.05 |      258 |   43 |    6 |         61 |                   42 |        256 | 4.90681e-12  |  0.412263    |
>| Retail    | #Q9      | Demographics | PWindow_5K                     |    0.01 |      270 |   45 |    6 |         61 |                   55 |        263 | 1.42986e-58  |  0.0236532   |
>| Retail    | #Q9      | Demographics | PWindow_5K                     |    0.05 |      270 |   45 |    6 |         67 |                   59 |        263 | 1.42986e-58  |  0.214258    |
>| Retail    | #Q1      | None         | PWindow_2K                     |    0.05 |      230 |   46 |    5 |        229 |                  229 |        228 | 0            |  2.93487e-18 |
>| Retail    | #Q1      | None         | PWindow_2K                     |    0.01 |      230 |   46 |    5 |        229 |                  229 |        228 | 0            |  2.93487e-18 |
>| Retail    | #Q9      | Demographics | PWindow_2K                     |    0.01 |     1665 |  111 |   15 |        278 |                  232 |       1648 | 7.36628e-43  |  0.0993425   |
>| Retail    | #Q9      | Demographics | PWindow_2K                     |    0.05 |     1665 |  111 |   15 |        308 |                  252 |       1648 | 7.36628e-43  |  0.947393    |
>| Amazon    | #Q3      | Promotion    | PWindow_2K                     |    0.01 |    19668 |   66 |  298 |        647 |                  642 |      19361 | 1.41578e-208 |  0.00955437  |
>| Amazon    | #Q3      | Promotion    | PWindow_2K                     |    0.05 |    19668 |   66 |  298 |        649 |                  644 |      19361 | 1.41578e-208 |  0.0353944   |
>| Retail    | #Q9      | Demographics | PWindow_1K                     |    0.01 |     6630 |  221 |   30 |        892 |                  631 |       6629 | 5.84738e-49  |  0.652895    |
>| Retail    | #Q9      | Demographics | PWindow_1K                     |    0.05 |     6630 |  221 |   30 |        998 |                  702 |       6629 | 5.84738e-49  |  3.39522     |
>| Retail    | #Q3      | Promotion    | PWindow_1K                     |    0.01 |    11592 |   72 |  161 |       1688 |                 1515 |      11423 | 2.2463e-38   |  0.339128    |
>| Retail    | #Q3      | Promotion    | PWindow_1K                     |    0.05 |    11592 |   72 |  161 |       1734 |                 1571 |      11423 | 2.2463e-38   |  1.5455      |
>| Retail    | #Q9      | Demographics | PWindow_500                    |    0.01 |    26520 |  442 |   60 |       3266 |                 1958 |      26458 | 2.70051e-30  |  2.87134     |
>| Retail    | #Q9      | Demographics | PWindow_500                    |    0.05 |    26520 |  442 |   60 |       3881 |                 2279 |      26458 | 2.70051e-30  | 18.3959      |
>| Retail    | #Q3      | Promotion    | PWindow_500                    |    0.01 |    45903 |  143 |  321 |       7648 |                 5575 |      45574 | 1.03427e-28  |  3.34045     |
>| Retail    | #Q3      | Promotion    | PWindow_500                    |    0.05 |    45903 |  143 |  321 |       8190 |                 6053 |      45574 | 1.03427e-28  | 16.8852      |
>| Amazon    | #Q3      | Promotion    | PWindow_1K                     |    0.01 |    78076 |  131 |  596 |       9033 |                 8933 |      77463 | 4.16052e-178 |  0.107377    |
>| Amazon    | #Q3      | Promotion    | PWindow_1K                     |    0.05 |    78076 |  131 |  596 |       9071 |                 8955 |      77463 | 4.16052e-178 |  1.41301     |
>| Amazon    | #Q3      | Promotion    | PWindow_500                    |    0.01 |   310851 |  261 | 1191 |      61365 |                58456 |     310013 | 6.13734e-118 |  3.09332     |
>| Amazon    | #Q3      | Promotion    | PWindow_500                    |    0.01 |   310851 |  261 | 1191 |      61365 |                58456 |     310013 | 6.13734e-118 |  3.09332     |
>| Amazon    | #Q3      | Promotion    | PWindow_500                    |    0.05 |   310851 |  261 | 1191 |      61878 |                58929 |     310013 | 6.13734e-118 | 15.3935      |
>| Amazon    | #Q3      | Promotion    | PWindow_500                    |    0.05 |   310851 |  261 | 1191 |      61878 |                58929 |     310013 | 6.13734e-118 | 15.3935      |