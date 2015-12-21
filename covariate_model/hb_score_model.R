


# read the csv

D <- read.csv("./hb-with-covariates.csv")
D$series <- as.factor(D$series)
D <- subset(D,select=c(-flowid,-received, -version, -extra))

# do a model?


model <- glm(score ~ ., data=D)
summary(model)
model.small <- glm(score ~ weirdEngine + defaultBrowser + channel + dnt + oldFx + clockSkewed, data=D)


summary(glm(score==5 ~ weirdEngine + defaultBrowser + channel + dnt, data=subset(D,score==5||score<=2),family=binomial))


# 5's vs 1,2,  r2 of .03
summary(lm(score==5 ~ weirdEngine + defaultBrowser + channel + dnt + oldFx, data=subset(D,D$score %in% c(1,2,5) )))
