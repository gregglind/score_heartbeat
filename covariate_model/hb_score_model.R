


# read the csv

D <- read.csv("./hb-with-covariates.csv")
D$series <- as.factor(D$series)
D <- subset(D,select=c(-flowid,-received, -version))

# do a model?


model <- glm(score ~ ., data=D)
