# Load dataset
X <- read.csv("weather-data.csv")

# Define make.project.data
make.project.data <- function(X, F1, F2, ID){
  attach(X)
  set.seed(ID)
  if(!is.data.frame(X)) stop("First Argument must be a data frame")
  if(is.numeric(F1) | is.numeric(F2)) stop("Second and third arguments must be categorical or factor variables")
  F1 <- as.factor(F1)
  F2 <- as.factor(F2)
  treatments <- expand.grid(levels(F1), levels(F2))
  n.treat <- nrow(treatments)
  if(n.treat > 9) stop(paste("Number of treatment combinations must be 9 or fewer. You have", n.treat))
  out.dat <- list()
  for(i in 1:n.treat){
    tempdat <- subset(X, subset = F1 == treatments[i,1] & F2 == treatments[i, 2])
    out.dat[[i]] <- tempdat[sample(nrow(tempdat), 5),]
  }
  detach()
  do.call("rbind", out.dat)
}

# Select random data
project.data <- make.project.data(X = X, F1 = X$source, F2 = X$place, ID = 1234567)
write.csv(project.data, "selected_data.csv", row.names = FALSE)