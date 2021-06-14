# --------------------------------------------------------------------
# Packages
library(readxl)
library(lme4)
library(lmerTest)
library(ppcor)
library(Hmisc)
library(corrplot)
library(tidyr)
library(dplyr)
library(ppcor)
library(outliers)
library(irr)
library(foreign)

# Packages to plot model
library(sjPlot)
library(sjmisc)
library(sjlabelled)
library(ggplot2)
library(lattice)
library(ggthemes)
library(ggpubr)
library(outliers)
library(ggsci)
library(tidyverse)

# Import general functions
# source("/Users/CN/Documents/repos/my_scripts/r/PlotCorrelation.R")
# source("/Users/CN/Documents/repos/my_scripts/r/PlotCorrelation_line_if_significant.R")
# source("/Users/CN/Documents/Projects/Joystick_M1_MRS/Analysis/RS/scripts/Test_difference_spearman.R")
# source('~/Documents/Projects/Joystick_Cereb_MRS/bin/mrsi_code/Test_difference_pearsons.R')

# Import project data
data_path='/Users/CN/Dropbox/speech_graphs/oasis/output'
file= "graph_data_with_pca.csv"
data <- data.frame(read.csv(file.path(data_path, file)))

data$subj <- as.factor(data$subj)
data$tat <- as.factor(data$tat)
data$group <- as.factor(data$group)

# Check that the correct variables are numeric (all apart from subj, tat, group)
unlist(lapply(data, is.numeric))

# Bring wide format table into long format
head(data)

# ---- Test for significant effect of group on PC1 score ----
model <- lmer( PC1_score ~ group + (1 | subj) + (1 | tat), data=data, na.action=na.omit)
model_reduced <- lmer( PC1_score ~ (1 | subj) + (1 | tat), data=data, na.action=na.omit)
print(anova(model, model_reduced))
anova(model)

# Test for significant effect of group on PC1 score controlling for number of nodes
model <- lmer( PC1_score ~ nodes + group + (1 | subj) + (1 | tat), data=data, na.action=na.omit)
model_reduced <- lmer( PC1_score ~ nodes + (1 | subj) + (1 | tat), data=data, na.action=na.omit)
print(anova(model, model_reduced))
anova(model)

# Test for significant effect of group on PC1 score without tat as random effect
model <- lmer( PC1_score ~ group + (1 | subj) , data=data, na.action=na.omit)
model_reduced <- lmer( PC1_score ~ (1 | subj) , data=data, na.action=na.omit)
print(anova(model, model_reduced))
anova(model)

# Test for significant effect of group on PC1 score controlling for number of nodes without tat as random effect
model <- lmer( PC1_score ~ nodes + group + (1 | subj) , data=data, na.action=na.omit)
model_reduced <- lmer( PC1_score ~ nodes + (1 | subj) , data=data, na.action=na.omit)
print(anova(model, model_reduced))
anova(model)

# ---- Test for significant effect of group on PC2_score ----
model <- lmer( PC2_score ~ group + (1 | subj) + (1 | tat), data=data, na.action=na.omit)
model_reduced <- lmer( PC2_score ~ (1 | subj) + (1 | tat), data=data, na.action=na.omit)
print(anova(model, model_reduced))
anova(model)

# Test for significant effect of group on PC2_score controlling for number of nodes
model <- lmer( PC2_score ~ nodes + group + (1 | subj) + (1 | tat), data=data, na.action=na.omit)
model_reduced <- lmer( PC2_score ~ nodes + (1 | subj) + (1 | tat), data=data, na.action=na.omit)
print(anova(model, model_reduced))
anova(model)

# Test for significant effect of group on PC2_score without tat as random effect
model <- lmer( PC2_score ~ group + (1 | subj) , data=data, na.action=na.omit)
model_reduced <- lmer( PC2_score ~ (1 | subj) , data=data, na.action=na.omit)
print(anova(model, model_reduced))
anova(model)

# Test for significant effect of group on PC2_score controlling for number of nodes without tat as random effect
model <- lmer( PC2_score ~ nodes + group + (1 | subj) , data=data, na.action=na.omit)
model_reduced <- lmer( PC2_score ~ nodes + (1 | subj) , data=data, na.action=na.omit)
print(anova(model, model_reduced))
anova(model)

# ---- Test for significant effect of group on PC3_score ----
model <- lmer( PC3_score ~ group + (1 | subj) + (1 | tat), data=data, na.action=na.omit)
model_reduced <- lmer( PC3_score ~ (1 | subj) + (1 | tat), data=data, na.action=na.omit)
print(anova(model, model_reduced))
anova(model)

# Test for significant effect of group on PC3_score controlling for number of nodes
model <- lmer( PC3_score ~ nodes + group + (1 | subj) + (1 | tat), data=data, na.action=na.omit)
model_reduced <- lmer( PC3_score ~ nodes + (1 | subj) + (1 | tat), data=data, na.action=na.omit)
print(anova(model, model_reduced))
anova(model)

# Test for significant effect of group on PC3_score without tat as random effect
model <- lmer( PC3_score ~ group + (1 | subj) , data=data, na.action=na.omit)
model_reduced <- lmer( PC3_score ~ (1 | subj) , data=data, na.action=na.omit)
print(anova(model, model_reduced))
anova(model)

# Test for significant effect of group on PC3_score controlling for number of nodes without tat as random effect
model <- lmer( PC3_score ~ nodes + group + (1 | subj) , data=data, na.action=na.omit)
model_reduced <- lmer( PC3_score ~ nodes + (1 | subj) , data=data, na.action=na.omit)
print(anova(model, model_reduced))
anova(model)



# ---- Test for significant effect of group on max_degree_centrality ----
model <- lmer( max_degree_centrality ~ group + (1 | subj) + (1 | tat), data=data, na.action=na.omit)
model_reduced <- lmer( max_degree_centrality ~ (1 | subj) + (1 | tat), data=data, na.action=na.omit)
print(anova(model, model_reduced))
anova(model)

# Test for significant effect of group on max_degree_centrality controlling for number of nodes
model <- lmer( max_degree_centrality ~ nodes + group + (1 | subj) + (1 | tat), data=data, na.action=na.omit)
model_reduced <- lmer( max_degree_centrality ~ nodes + (1 | subj) + (1 | tat), data=data, na.action=na.omit)
print(anova(model, model_reduced))
anova(model)

# Test for significant effect of group on max_degree_centrality without tat as random effect
model <- lmer( max_degree_centrality ~ group + (1 | subj) , data=data, na.action=na.omit)
model_reduced <- lmer( max_degree_centrality ~ (1 | subj) , data=data, na.action=na.omit)
print(anova(model, model_reduced))
anova(model)

# Test for significant effect of group on max_degree_centrality controlling for number of nodes without tat as random effect
model <- lmer( max_degree_centrality ~ nodes + group + (1 | subj) , data=data, na.action=na.omit)
model_reduced <- lmer( max_degree_centrality ~ nodes + (1 | subj) , data=data, na.action=na.omit)
print(anova(model, model_reduced))
anova(model)


# ---- Tat-averaged data----

# Import project data
data_path='/Users/CN/Dropbox/speech_graphs/oasis/output'
file= "graph_data_with_pca_avg.csv"
data_avg <- data.frame(read.csv(file.path(data_path, file)))

data_avg$subj <- as.factor(data_avg$X)
data_avg$group <- as.factor(data_avg$group)

# Check that the correct variables are numeric (all apart from subj, tat, group)
unlist(lapply(data_avg, is.numeric))

# Bring wide format table into long format
head(data_avg)

# ---- Test for significant effect of group on PC1 score ----
# Test for significant effect of group on PC1 score 
model <- lm( PC1_score ~ group  , data=data_avg, na.action=na.omit)
anova(model)

model <- lm( PC2_score ~ nodes + group  , data=data_avg, na.action=na.omit)
anova(model)

model <- lm( PC3_score ~ nodes + group  , data=data_avg, na.action=na.omit)
anova(model)


# ---- Test for significant effect of group on max_degree_centrality ----
# Test for significant effect of group on max_degree_centrality 
model <- lm( max_degree_centrality ~ group  , data=data_avg, na.action=na.omit)
anova(model)

# Test for significant effect of group on max_degree_centrality controlling for number of nodes without tat as random effect
model <- lm( max_degree_centrality ~ nodes + group  , data=data_avg, na.action=na.omit)
anova(model)

# Test for significant effect of group on max_degree_centrality_abs controlling for number of nodes without tat as random effect
model <- lm( max_degree_centrality_abs ~ nodes + group  , data=data_avg, na.action=na.omit)
anova(model)

