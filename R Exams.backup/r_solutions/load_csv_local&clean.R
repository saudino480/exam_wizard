source("helpers.R")

lst_fnames = read.csv(
  "./data/lst_fnames.txt", header = FALSE)[[1]]


# Load all files and combine
lst_dfs = list()
for(fname in lst_fnames){
  path = paste0("./data/", fname)
  print(path)
  lst_dfs[[fname]] = read.csv(path, stringsAsFactors = F)
}

lst_cleaned_dfs = lapply(lst_dfs, clean_single_df)


