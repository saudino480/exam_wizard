get_url <- function(year, quarter){
  url = paste0(
    "https://projects.propublica.org/congress/assets/staffers/", 
    year, quarter, 
    "-house-disburse-detail.csv"
  )
  
  return(url)
}

load_file_get_fname <- function(year, quarter){
  url = get_url(year, quarter)
  
  result = tryCatch(
    {
      print(paste0("Downloading for ", year, " ", quarter))
      read.csv(url)
      }, 
    error = function(e) {
      print(paste0("The url might not exist, no data for ", year, quarter, " is loaded."))
      NULL}
  )
  
  fname = paste0(year, "-", quarter, ".csv")
  path = paste0("./data/", fname)
  
  if(length(result)!=0){
    write.csv(result, path, row.names = FALSE)
  } else {
    fname = NULL
  }
  
  return(fname)
}

lst_fnames = character()
four_quarters = paste("Q", 1:4, sep = "")
for(year in 2009:2018){
  for(quarter in four_quarters){
    i = length(lst_fnames) + 1
    fname = load_file_get_fname(year, quarter)
    if(length(fname)!=0){
      lst_fnames[i] = fname
    }
  }
}

write(lst_fnames, "data/lst_fnames.txt")

