# assignment_script.R
# Weather forecast analysis for assignment
# Student: Eli Johnson, ID: 1234567
# Date: October 6, 2025

#######################################################
#
#         Set up package installation
#
#######################################################

# Create a user library for package installation
user_lib <- "~/R_libs"
if (!dir.exists(user_lib)) dir.create(user_lib, recursive = TRUE)
.libPaths(c(user_lib, .libPaths()))

# Install and load agricolae
if (!require(agricolae)) install.packages("agricolae", lib = user_lib)
library(agricolae, lib.loc = user_lib)

#######################################################
#
#         Define function to select random data
#
#######################################################

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

#######################################################
#
#         Load and check dataset
#
#######################################################

# Load dataset
X <- read.csv("weather-data.csv")

# Check observation counts per source and place
print("Observation counts by source and place:")
print(table(X$source, X$place))

# Select random data (30 observations, 5 per source x place)
project.data <- make.project.data(X = X, F1 = X$source, F2 = X$place, ID = 1234567)

# save the selected data to a CSV file
write.csv(project.data, "selected_data.csv", row.names = FALSE)

#######################################################
#
#         Optional: Recode factors (example)
#         Combine source levels: web + app = "digital", TV news = "TV"
#
#######################################################

attach(project.data)
new.source <- as.factor(source)
levels(new.source) <- list("digital" = c("web", "app"), "TV" = "TV news")
detach()
project.data$new.source <- new.source
rm(new.source)

# Note: Analysis uses original source, not new.source, per assignment requirements

#######################################################
#
#         Perform ANOVA analysis
#
#######################################################

# Preliminary model (additive)
prelim_model <- aov(maxf ~ source + place, data = project.data)
summary(prelim_model)
# OUTPUT
# 
#             Df Sum Sq Mean Sq F value   Pr(>F)
# source       2   8.87    4.43   1.928    0.166
# place        1  67.50   67.50  29.348 1.12e-05 ***
# Residuals   26  59.80    2.30

# Factorial model (with interaction)
factorial_model <- aov(maxf ~ source * place, data = project.data)
summary(factorial_model)

#              Df Sum Sq Mean Sq F value   Pr(>F)
# source        2   8.87    4.43   1.914    0.169
# place         1  67.50   67.50  29.137 1.52e-05 ***
# source:place  2   4.20    2.10   0.906    0.417
# Residuals    24  55.60    2.32

# #######################################################
# #
# #         Post-hoc LSD tests
# #
# #######################################################

# LSD for source
lsd_source <- LSD.test(factorial_model, "source", console = TRUE)

# OUTPUT
# 
# LSD t Test for maxf

# Mean Square Error:  2.316667

# source,  means and individual ( 95 %) CI

#         maxf      std  r        se      LCL      UCL Min Max   Q25  Q50   Q75
# app     18.4 1.897367 10 0.4813176 17.40661 19.39339  16  22 17.25 18.0 19.75
# TV news 19.6 2.503331 10 0.4813176 18.60661 20.59339  15  23 18.25 19.5 21.75
# web     19.5 2.068279 10 0.4813176 18.50661 20.49339  15  22 18.25 20.0 21.00

# Alpha: 0.05 ; DF Error: 24
# Critical Value of t: 2.063899

# least Significant Difference: 1.404867

# Treatments with the same letter are not significantly different.

#         maxf groups
# TV news 19.6      a
# web     19.5      a
# app     18.4      a

# Study: factorial_model ~ "place"

# LSD for place
lsd_place <- LSD.test(factorial_model, "place", console = TRUE)

# OUTPUT
#
# LSD t Test for maxf

# Mean Square Error:  2.316667

# place,  means and individual ( 95 %) CI

#          maxf      std  r        se      LCL      UCL Min Max  Q25 Q50  Q75
# bris 20.66667 1.397276 15 0.3929942 19.85557 21.47777  18  23 20.0  21 22.0
# syd  17.66667 1.718249 15 0.3929942 16.85557 18.47777  15  21 16.5  18 18.5

# Alpha: 0.05 ; DF Error: 24
# Critical Value of t: 2.063899

# least Significant Difference: 1.147069

# Treatments with the same letter are not significantly different.

#          maxf groups
# bris 20.66667      a
# syd  17.66667      b

#######################################################
#
#         Generate and save plots
#
#######################################################

# Save boxplot
png("boxplot.png")
boxplot(maxf ~ source * place, data = project.data, 
        ylab = "Forecast Max Temp (°C)", xlab = "Source and Location", 
        col = c("lightblue", "lightgreen", "lightyellow"))
dev.off()

# Save interaction plot
png("interaction_plot.png")
interaction.plot(project.data$source, project.data$place, project.data$maxf, 
                 ylab = "Mean Max Temp (°C)", xlab = "Source")
dev.off()
