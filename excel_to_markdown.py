
## Imports
import pandas as pd
from tabulate import tabulate
from datetime import datetime

## Read Data
df = pd.read_excel("data_sources.xlsx")

## Format Cells
newline_replace = lambda x: x.replace("\n","<br/>") if not isinstance(x, float) else x
strip_space = lambda x: x.strip() if not isinstance(x, float) else x
columns_to_format = ["Paper",
                     "Authors",
                     "Platform",
                     "Target Outcomes",
                     "Labeling Methodology",
                     "Size",
                     "Availability",
                     "Additional Comments",
                     "Dataset Link (if any)",
                     "Reference Link"]
for col in columns_to_format:
    df[col] = df[col].map(newline_replace)
    df[col] = df[col].map(strip_space)

## Link in Title
title_formatter = lambda row: "[{}]({})".format(row["Paper"], row["Reference Link"])
df["Paper"] = df.apply(title_formatter, axis = 1)

## Subset Columns
col_subset = ["Paper",
              "Authors",
              "Platform",
              "Year",
              "Target Outcomes"]
df = df[col_subset].copy()

## Sort by Date
df = df.sort_values("Year", ascending=False)
df = df.reset_index(drop=True)

## Generate Markdown Table
md_table = tabulate(df, tablefmt="pipe", headers="keys", showindex="never")

## Output
md_output = """
# Mental Health Datasets

The information below is an evolving list of data sets (primarily from electronic/social media) that have been used to model mental-health phenomena. The raw data (with additional columns) can be found in `data_sources.xlsx`. If you are an author of any of these papers and feel that anything is misrepresented, please do not hesitate to reach out to me at kharrigian@jhu.edu.

For an overview of existing datasets, please consider reading our paper [*On the State of Social Media Data for Mental Health Research*](https://arxiv.org/abs/2011.05233).

```
@inproceedings{harrigian2020state,
  title={On the State of Social Media Data for Mental Health Research},
  author={Harrigian, Keith and Aguirre, Carlos and Dredze, Mark},
  booktitle={Proceedings of the 7th Workshop on Computational Linguistics and Clinical Psychology: Improving Access},
  year={2021}
}
```
"""+"""
**Last Update**: {}

{}
""".format(datetime.now().isoformat(), md_table)

## Write Out
with open("README.md", "w") as the_file:
    the_file.write(md_output)