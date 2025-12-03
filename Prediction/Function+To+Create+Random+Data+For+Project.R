# This is a function that randomly selects
# 5 replicate values from a larger data set X
# if given the names of two factor variables, F1 and F2, 
# in that dataset. 
#
# Student's ID (minus leading "s") is required so we can
# recover their random data for checking and marking purposes
# if necessary.

# To put this function into R, put your cursor anywhere on the 
# make.project.data line (line 16) and hit the run button at the 
# top of the script file.

# DO NOT MAKE ANY CHANGES TO THE CODE IN THIS FUNCTION!!

make.project.data <- function(X, F1, F2, ID){
  
  attach(X)
  # Set random seed to student ID:
  set.seed(ID)
  
  # Check X, F1, and F2 are the correct object types
  if(!is.data.frame(X)) stop("First Argument must be a data frame")
  if(is.numeric(F1) | is.numeric(F2)) stop("Second and third arguments must be categorical or factor variables")
 
   # check there are no more than 9 treatment combos:
  F1 <- as.factor(F1)
  F2 <- as.factor(F2)
  treatments <- expand.grid(levels(F1), levels(F2))
  n.treat <- nrow(treatments)
  if(n.treat > 9) stop(paste("Number of treatment combinations must be 9 or fewer. 
                                      You have", n.treat))
  
  # Create Treatment combo subsets and randomly select 5 reps from each:
  out.dat <- list()
  for(i in 1:n.treat){
    tempdat <- subset(X, subset = F1 == treatments[i,1] & F2 == treatments[i, 2])
    
    # Randomly select 5 data points from this data set:
    out.dat[[i]] <- tempdat[sample(nrow(tempdat), 5),]
  }
  detach()
  # put all the datasets together and print it out:
  do.call("rbind", out.dat)
}
