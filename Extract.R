#Storing the names of different PDFs in character vector "file_names"
directory = "C:/Users/HP/Documents/R Directories/EgregoreLabs/Docs/"
file_names = list.files(path = directory)
number_of_files = length(file_names)
index=-1

#Loading required libraries
library(pdftools)
library(stringr)
library(tidyverse)

month = month.abb
dateC = ""
output = data.frame("Name_of_Company"=character(),"Date_of_Call"=character(),"No_of_Pages"=character(),"File_Path"=character())

#selecting files one by one
for(i in 1:number_of_files)
{
   #Reading the pdf file as text
   FilePath = paste(directory,file_names[i],sep = "")
   TextFile = pdf_text(FilePath) %>% readr::read_lines()
   
   #No of pages
   pages=length(pdf_text(FilePath))
   
   #Company Name
   cleanName1= TextFile[1] %>% str_replace_all( "[[:punct:]]", "") %>% str_squish() %>% strsplit(split = " ") %>% unlist()
   
   #finding the word limited or ltd
   if(sum(grepl("ltd",cleanName1,ignore.case = TRUE))==0){
      index=grep("limited",cleanName1,ignore.case = TRUE)}
   else{
      index=grep("ltd",cleanName1,ignore.case = TRUE)
   }
   
   CompanyName = paste(cleanName1[1:index],collapse = " ")
   
   
   #Date
   cleanName2= TextFile[3:4] %>% str_replace_all( "[[:punct:]]", "") %>% str_squish()
   for(j in month){
      if(sum(grepl(j,cleanName2,ignore.case = TRUE))==1){
         pos = grep(j,cleanName2,ignore.case = TRUE)
         dateC = cleanName2[pos]
         break()
      }
   }
  
   
   
   print(CompanyName)
   print(dateC)
   print(paste("File path:",FilePath))
   print(paste("No of pages:",pages))
   record = data.frame("Name_of_Company"=CompanyName,"Date_of_Call"=dateC,"No_of_Pages"=pages,"File_Path"=FilePath)
   output = rbind(output, record)
   print("")
   print("")
}

write.csv(output, file = "records.csv")