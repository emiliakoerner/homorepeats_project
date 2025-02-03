# Load necessary libraries
library(tidyverse)
library(readxl)
library(dplyr)
library(gridExtra)

# Read in data for all organisms
file_paths <- list.files("C:/Users/wrede/OneDrive - JGU/Desktop/Masterarbeit/model organisms/mapped_hk_polyx", 
                         pattern = "*.tsv", full.names = TRUE)
organism_data <- file_paths %>%
  map_dfr(~read_tsv(.x, show_col_types = FALSE) %>%
            mutate(
              Polyx_lengths = as.character(Polyx_lengths),  # Ensure consistent type for Polyx_lengths
              Count_grouped = as.character(Count_grouped),  # Ensure consistent type for Count_grouped
              Organism = str_remove(tools::file_path_sans_ext(basename(.x)), "_mapped_polyx")  # Remove suffix
            ))

# Process the combined data
HkPolyx <- organism_data %>%
  mutate(Hk = recode(Hk, `0` = "not Hk", `1` = "Hk"),
         Hk = as.factor(Hk),
         Hk = factor(Hk, levels = rev(levels(Hk))),
         Count_grouped = factor(Count_grouped, levels = c("0", "1", ">1")))
HkPolyx$Organism <- factor(HkPolyx$Organism, levels = c("ecoli", "yeast", "arabidopsis", "celegans", "fruitfly", "mouse"))
HkPolyx <- HkPolyx %>%
  mutate(Organism = factor(Organism,
                           levels = c("ecoli", "yeast", "celegans", "fruitfly", "arabidopsis", "mouse"),
                           labels = c(
                             "italic('E. coli')",
                             "italic('S. cerevisiae')",
                             "italic('C. elegans')",
                             "italic('D. melanogaster')",
                             "italic('A. thaliana')",
                             "italic('M. musculus')"
                           )
  ))


# Define a custom theme
my_theme <- theme(
  axis.title = element_text(size = 16),
  axis.text = element_text(size = 14),
  legend.text = element_text(size = 14),
  legend.title = element_text(size = 15),
  plot.title = element_text(size = 16, hjust = 0.5),
  strip.text = element_text(size = 12, face = "bold"))

# Visualization 1
# Corrected significance_hk
significance_hk <- tibble(
  Organism = factor(
    c("ecoli", "celegans", "fruitfly", "mouse", "yeast", "arabidopsis"),
    levels = c("ecoli", "yeast", "celegans", "fruitfly", "arabidopsis", "mouse"),
    labels = c(
      "italic('E. coli')",
      "italic('S. cerevisiae')",
      "italic('C. elegans')",
      "italic('D. melanogaster')",
      "italic('A. thaliana')",
      "italic('M. musculus')"
    )
  ),
  x = c(1.5, 1.5, 1.5, 1.5, 1.5, 1.5),  # X coordinates for label placement
  y = c(900, 900, 900, 900, 900, 900),  # Y coordinates for label placement
  label = c("***", "***", "***", "***", "***", "***")  # Significance levels for each organism
)



HkPolyx %>%
  ggplot(aes(x = Hk, y = Length, fill = Hk)) +
  geom_boxplot(size = 1.2, notch = TRUE) +
  #geom_jitter(width = 0.2, alpha = 0.5, size = 0.01) +
  ylab("Protein length (aa)") +
  coord_cartesian(ylim = c(100, 900)) +
  scale_fill_manual(values = c("#ffc8d2", "#ccffee")) +
  stat_summary(fun = "mean", geom = "point", shape = 21, size = 4, color = "black", fill = "white") +
  facet_wrap(~Organism, ncol = 3, labeller = label_parsed) +  # Facet by organism
  my_theme +
  geom_text(data = significance_hk, aes(x = x, y = y, label = label), size = 4, color = "black", inherit.aes = FALSE) +
  geom_text(
    data = HkPolyx %>%
      group_by(Hk, Organism) %>%
      summarize(median_length = median(Length),
        Count = n()),
    aes(x = Hk,
      y = median_length - 50,  # Place the text at the median
      label = Count),
    inherit.aes = FALSE,
    size = 3, color = "black")

significance_labels <- tibble(
  Organism = c("ecoli", "celegans", "fruitfly", "mouse", "yeast", "arabidopsis", "celegans", "fruitfly", "mouse", "yeast", "arabidopsis"),  # Replace with actual organism names
  x = c(1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 2.5, 2.5, 2.5, 2.5, 2.5),  # X coordinates for label placement
  y = c(1350, 1350, 1350, 1350, 1350, 1350, 1350, 1350, 1350, 1350, 1350),  # Y coordinates for label placement
  label = c("ns", "***", "***", "***", "***", "***", "***", "***", "***", "***", "***")  # Significance levels for each organism
)
# Visualization 2: Protein Length by Homorepeats (Faceted by Organism)
counts <- HkPolyx %>%
  group_by(Count_grouped, Organism) %>%
  summarize(Count = n(), .groups = "drop")
HkPolyx %>%
  ggplot(aes(x = Count_grouped, y = Length, fill = Count_grouped)) +
  geom_boxplot(size = 1.2, notch = TRUE) +
  xlab("Number of Homorepeats") +
  ylab("Protein length (aa)") +
  coord_cartesian(ylim = c(100, 1400)) +
  scale_fill_manual(name = "HR count", values = c("#4d79ff", "#ccffee", "#ffffff")) +
  stat_summary(fun = "mean", geom = "point", shape = 21, size = 4, color = "black", fill = "white") +
  facet_wrap(~Organism, ncol = 3) +
  geom_text(
    data = HkPolyx %>%
      group_by(Count_grouped, Organism) %>%
      summarize(
        median_length = median(Length),
        Count = n()
      ),
    aes(
      x = Count_grouped,
      y = median_length - 70,  # Place the text at the median
      label = Count
    ),
    inherit.aes = FALSE,
    size = 3,
    color = "black"
  ) +
  geom_text(data = significance_labels, aes(x = x, y = y, label = label), size = 4, color = "black", inherit.aes = FALSE) +
  my_theme

############# complete histograms ###############
# Update the Count_grouped variable to include 0, 1, 2, 3, 4, and >4 categories
HkPolyx <- HkPolyx %>%
  mutate(Count_grouped = case_when(
    Polyx_count == 0 ~ "0",
    Polyx_count == 1 ~ "1",
    Polyx_count == 2 ~ "2",
    Polyx_count == 3 ~ "3",
    Polyx_count == 4 ~ "4",
    Polyx_count == 5 ~ "5",
    Polyx_count >5 ~ ">5"
  ))

HkPolyx$Count_grouped <- factor(HkPolyx$Count_grouped, levels = c("0", "1", "2", "3", "4", ">4"))  # desired order for boxplots


# Check the new groups
table(HkPolyx$Count_grouped)

significance_labels <- tibble(
  Organism = c("ecoli", "celegans", "fruitfly", "mouse", "yeast", "arabidopsis", "celegans", "fruitfly", "mouse", "yeast", "arabidopsis", "celegans", "fruitfly", "mouse", "yeast", "arabidopsis"),  # Replace with actual organism names
  x = c(1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 2.5, 2.5, 2.5, 2.5, 2.5, 3.5, 3.5, 3.5, 3.5, 3.5),  # X coordinates for label placement
  y = c(1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500),  # Y coordinates for label placement
  label = c("ns", "***", "***", "***", "***", "***", "***", "***", "***", "***", "***", "ns", "***", "ns", "ns", "ns")  # Significance levels for each organism
)

HkPolyx %>%
  ggplot(aes(x = Count_grouped, y = Length, fill = Count_grouped)) +
  geom_boxplot(size = 1.2, notch = FALSE) +
  geom_jitter(width = 0.2, alpha = 0.5, size = 0.01) +
  xlab("Number of Homorepeats") +
  ylab("Protein length (aa)") +
  coord_cartesian(ylim = c(100, 1800)) +
  scale_fill_manual(name = "HR count", values = c("#4d79ff", "#80cfff", "#a3d8ff", "#d1edee", "#e1f1f1", "#ffffff")) +
  stat_summary(fun = "mean", geom = "point", shape = 21, size = 4, color = "black", fill = "white") +
  facet_wrap(~Organism, ncol = 3) +
  my_theme +
  geom_text(
    data = HkPolyx %>%
      group_by(Count_grouped, Organism) %>%
      summarize(
        median_length = median(Length),
        Count = n()
      ),
    aes(
      x = Count_grouped,
      y = median_length - 70,  # Place the text at the median
      label = Count
    ),
    inherit.aes = FALSE,
    size = 3,
    color = "black"
  )  +
  geom_text(data = significance_labels, aes(x = x, y = y, label = label), size = 4, color = "black", inherit.aes = FALSE)




#######################


# Visualization 3: Density Plot of Protein Length (Housekeeping vs. Non-Housekeeping)
HkPolyx %>%
  ggplot(aes(x = Length, fill = Hk)) +
  geom_density(adjust = 0.7, alpha = 0.5) +
  xlab("Protein length (aa)") +
  ylab("Density") +
  coord_cartesian(xlim = c(0, 1500), ylim = c(0, 0.01)) +
  scale_fill_manual(values = c("#ffc8d2", "#ccffee")) +
  facet_wrap(~Organism, ncol = 3) +  # Facet by organism
  my_theme

# Visualization 4: Density Plot of Protein Length (Homorepeats)
HkPolyx %>%
  ggplot(aes(x = Length, fill = Count_grouped)) +
  geom_density(adjust = 0.7, alpha = 0.5) +
  xlab("Protein length (aa)") +
  ylab("Density") +
  coord_cartesian(xlim = c(0, 2000)) +
  scale_fill_manual(name = "HR count", values = c("#4d79ff", "#ccffee", "#ffffff")) +
  facet_wrap(~Organism, ncol = 3) +  # Facet by organism
  my_theme

# Wilcoxon Rank-Sum Test for Plot 1: Protein Length by Housekeeping Status
plot1_stats <- HkPolyx %>%
  group_by(Organism) %>%
  summarise(
    p_value = wilcox.test(Length ~ Hk)$p.value
  ) %>%
  mutate(significance = case_when(
    p_value < 0.001 ~ "***",
    p_value < 0.01 ~ "**",
    p_value < 0.05 ~ "*",
    TRUE ~ "ns"
  ))

print(plot1_stats)


# Apply Wilcoxon test for each organism for 0 vs. 1
results <- HkPolyx %>%
  group_by(Organism) %>%
  filter(Count_grouped %in% c("0", "1")) %>%
  do({
    # Perform the Wilcoxon test for the current organism
    test_result <- wilcox.test(Length ~ Count_grouped, data = ., correct = TRUE)
    # Return the p-value for the test
    tibble(p_value_0_1 = test_result$p.value)
  })

# View the results
print(results)


# Apply Wilcoxon test for each organism for 1 vs. >1
results <- HkPolyx %>%
  filter(Organism != "ecoli") %>%
  group_by(Organism) %>%
  filter(Count_grouped %in% c("1", ">1")) %>%
  do({
    # Perform the Wilcoxon test for the current organism
    test_result <- wilcox.test(Length ~ Count_grouped, data = ., correct = TRUE)
    # Return the p-value for the test
    tibble(p_value_0_1 = test_result$p.value)
  })

print(results)


# Apply Wilcoxon test for each organism for 2 vs. 3
results <- HkPolyx %>%
  filter(Organism != "ecoli") %>%
  filter(Organism == "fruitfly") %>%
  group_by(Organism) %>%
  filter(Count_grouped %in% c("4", ">4")) %>%
  do({
    # Perform the Wilcoxon test for the current organism
    test_result <- wilcox.test(Length ~ Count_grouped, data = ., correct = TRUE)
    # Return the p-value for the test
    tibble(p_value_0_1 = test_result$p.value)
  })

print(results)

# Data preparation
polyx_freq_percentage <- HkPolyx %>%
  filter(Polyx_types != "-") %>%
  separate_rows(Polyx_types, sep = "/") %>%
  group_by(Organism, Hk, Polyx_types) %>% 
  summarise(Count = n(), .groups = "drop") %>% 
  group_by(Organism, Hk) %>% 
  mutate(Total_in_Category = sum(Count),
         Percentage = (Count / Total_in_Category) * 100) %>% 
  ungroup() %>% 
  arrange(Polyx_types) %>%
  mutate(Hk = factor(Hk, levels = c("Hk", "not Hk")))  # Set order: Hk first

# Custom colors
custom_colors <- c("red", "blue", "yellow", "green", "purple", "orange", "pink", 
                   "cyan", "magenta", "orange", "brown", "darkblue", 
                   "gold", "darkgreen", "coral", "turquoise", "black", "yellow", "pink")

print(polyx_freq_percentage, n=150)

# Facet plot
ggplot(polyx_freq_percentage, aes(x = Hk, y = Percentage, fill = Polyx_types)) +
  geom_bar(stat = "identity", position = "stack") +
  scale_fill_manual(values = custom_colors) +
  labs(title = "Percentage of PolyX Types in Hk and not Hk Proteins by Organism",
       x = "Hk or not", y = "Percentage", fill = "PolyX Type") +
  facet_wrap(~ Organism, ncol = 3) +  # Facet by organism
  theme_minimal()


expanded_HkPolyx <- HkPolyx %>%
  separate_rows(Polyx_types, Polyx_lengths, sep = "/") %>%
  filter(Polyx_types != "-")  # Remove entries without Poly-X

expanded_HkPolyx$Polyx_lengths <- as.numeric(expanded_HkPolyx$Polyx_lengths)
expanded_HkPolyx <- expanded_HkPolyx %>%
  mutate(ratio_hrcount = Length / Polyx_count) %>%
  mutate(ratio_hrlength = Length / Polyx_lengths)
expanded_HkPolyx

# Distribution of Protein Length / Number of PolyX Regions by Organism
ggplot(expanded_HkPolyx, aes(x = ratio_hrcount)) +
  geom_density(fill = "blue", alpha = 0.5) +
  labs(title = "Distribution of Protein Length / Number of PolyX Regions by Organism",
       x = "Protein Length / Number of PolyX Regions",
       y = "Density") +
  coord_cartesian(xlim = c(0, 3000)) +
  facet_wrap(~ Organism, ncol = 3) +  # Facet by organism
  my_theme

# Distribution of Protein Length / Number of PolyX Regions by PolyX Types and Organism
ggplot(expanded_HkPolyx, aes(x = ratio_hrcount, fill = Polyx_types)) +
  geom_density(alpha = 0.5) +
  labs(title = "Distribution of Protein Length / Number of PolyX Regions by PolyX Types and Organism",
       x = "Protein Length / Number of PolyX Regions",
       y = "Density") +
  coord_cartesian(xlim = c(0, 1200), ylim= c(0, 0.01)) +
  facet_wrap(~ Organism, ncol = 3) +  # Facet by organism
  my_theme

# Distribution of Protein Length / Length of PolyX Regions by Organism
ggplot(expanded_HkPolyx, aes(x = ratio_hrlength)) +
  geom_density(fill = "blue", alpha = 0.5) +
  labs(title = "Distribution of Protein Length / Length of PolyX Regions by Organism",
       x = "Protein Length / Length of PolyX Regions",
       y = "Density") +
  coord_cartesian(xlim = c(0, 500)) +
  facet_wrap(~ Organism, ncol = 3) +  # Facet by organism
  my_theme

# Distribution of Protein Length / Length of PolyX Regions by PolyX Types and Organism
ggplot(expanded_HkPolyx, aes(x = ratio_hrlength, fill = Polyx_types)) +
  geom_density(alpha = 0.5) +
  labs(title = "Distribution of Protein Length / Length of PolyX Regions by PolyX Types and Organism",
       x = "Protein Length / Length of PolyX Regions",
       y = "Density") +
  coord_cartesian(xlim = c(0, 200), ylim=c(0, 0.06)) +
  facet_wrap(~ Organism, ncol = 3) +  # Facet by organism
  my_theme


expanded_HkPolyx
ggplot(expanded_HkPolyx, aes(x = ratio_hrcount, color = ifelse(Length > 200, ">200 aa", "<= 200 aa"))) +
  geom_density(alpha = 1) +
  scale_color_manual(values = c("red", "blue")) +  # Customize colors
  labs(x = "Protein Length / Number of PolyX Regions",
       y = "Density",
       color = "Protein Length") +
  facet_wrap(~ Organism, ncol = 3) +
  coord_cartesian(xlim = c(0, 500)) +
  my_theme


expanded_HkPolyx_scatter <- HkPolyx %>%
  separate_rows(Polyx_types, Polyx_lengths, sep = "/")

# each protein is one data point
ggplot(HkPolyx, aes(x = Length, y = Polyx_count)) +
  geom_point(alpha = 0.7, color = "blue", size = 1) +
  labs(
    x = "Protein Length (aa)",
    y = "Number of Homorepeats"
  ) +
  my_theme +
  facet_wrap(~ Organism, ncol = 3) +
  coord_cartesian(xlim = c(0,500), ylim = c(0,8))

# x axis: length of disordered region (sum of all HRs)
ggplot(expanded_HkPolyx_scatter, aes(x = Length, y = Total_length)) +
  geom_point(alpha = 0.7, color = "blue", size = 0.1) +
  labs(
    x = "Protein Length (aa)",
    y = "Total length of HRs in each protein (aa)"
  ) +
  my_theme +
  facet_wrap(~ Organism, ncol = 3) +
  coord_cartesian(xlim = c(0,2000), ylim = c(0,100))

############################################

#Gene length:

file_paths <- list.files("C:/Users/wrede/OneDrive - JGU/Desktop/Masterarbeit/model organisms/mapped_hk_length", 
                         pattern = "*.tsv", full.names = TRUE)
organism_data <- file_paths %>%
  map_dfr(~read_tsv(.x, show_col_types = FALSE) %>%
            mutate(Organism = str_remove(tools::file_path_sans_ext(basename(.x)), "_mapped_length")))

# Process the combined data
HkPolyx <- organism_data %>%
  mutate(Hk = recode(Hk, `0` = "not Hk", `1` = "Hk"),
         Hk = as.factor(Hk),
         Hk = factor(Hk, levels = rev(levels(Hk))),
         genelength = as.numeric(genelength))
HkPolyx <- HkPolyx %>%
  filter(!is.na(genelength))

# Group and calculate average gene length
average_lengths <- HkPolyx %>%
  group_by(Organism, Hk) %>%
  summarize(average_genelength = mean(genelength, na.rm = TRUE),
            .groups = "drop")  # Drop grouping after summarization

# Print the result
print(average_lengths)
         
# Define a custom theme
my_theme <- theme(
  axis.title = element_text(size = 16),
  axis.text = element_text(size = 14),
  legend.text = element_text(size = 14),
  legend.title = element_text(size = 15),
  plot.title = element_text(size = 16, hjust = 0.5),
  strip.text = element_text(size = 12, face = "bold"))

# Visualization 1
significance_length <- tibble(
  Organism = c("mouse", "mouse2", "mouseortholog", "human"),  # Replace with actual organism names
  x = c(1.5, 1.5, 1.5, 1.5),  # X coordinates for label placement
  y = c(90000, 90000, 90000, 90000),  # Y coordinates for label placement
  label = c("***", "***", "***", "***")  # Significance levels for each organism
)

HkPolyx %>%
  filter(Organism %in% c("human", "mouse", "mouse2", "mouseortholog")) %>%  # Replace with your organisms
  ggplot(aes(x = Hk, y = genelength, fill = Hk)) +
  geom_boxplot(size = 1.2, notch = TRUE) +
  ylab("Protein length (aa)") +
  coord_cartesian(ylim = c(0, 100000)) +  # Adjust as needed for your data
  scale_fill_manual(values = c("#ffc8d2", "#ccffee")) +
  stat_summary(fun = "mean", geom = "point", shape = 21, size = 4, color = "black", fill = "white") +
  facet_wrap(~Organism, ncol = 2) +  # Adjust ncol based on how you want to arrange facets
  my_theme +
  geom_text(
    data = HkPolyx %>%
      filter(Organism %in% c("human", "mouse", "mouse2", "mouseortholog")) %>%  # Same filter here
      group_by(Hk, Organism) %>%
      summarize(median_length = median(genelength, na.rm = TRUE),
                Count = n(), .groups = "drop"),
    aes(x = Hk,
        y = median_length - 4000,  # Adjust position as needed
        label = Count),
    inherit.aes = FALSE,
    size = 3, color = "black") +
  geom_text(data = significance_length, aes(x = x, y = y, label = label), size = 4, color = "black", inherit.aes = FALSE)


HkPolyx %>%
  filter(Organism %in% c("fruitfly", "fruitfly2", "yeast", "celegans")) %>%  # Replace with your organisms
  ggplot(aes(x = Hk, y = genelength, fill = Hk)) +
  geom_boxplot(size = 1.2, notch = TRUE) +
  ylab("Protein length (aa)") +
  coord_cartesian(ylim = c(0, 8000)) +  # Adjust as needed for your data
  scale_fill_manual(values = c("#ffc8d2", "#ccffee")) +
  stat_summary(fun = "mean", geom = "point", shape = 21, size = 4, color = "black", fill = "white") +
  facet_wrap(~Organism, ncol = 2) +  # Adjust ncol based on how you want to arrange facets
  my_theme +
  geom_text(
    data = HkPolyx %>%
      filter(Organism %in% c("fruitfly", "fruitfly2", "yeast", "celegans")) %>%  # Same filter here
      group_by(Hk, Organism) %>%
      summarize(median_length = median(genelength),
                Count = n()),
    aes(x = Hk,
        y = median_length + 300,  # Adjust position as needed
        label = Count),
    inherit.aes = FALSE,
    size = 3, color = "black")

# Wilcoxon Rank-Sum Test for Plot 1: Protein Length by Housekeeping Status
plot1_stats <- HkPolyx %>%
  group_by(Organism) %>%
  summarise(
    p_value = wilcox.test(genelength ~ Hk)$p.value
  ) %>%
  mutate(significance = case_when(
    p_value < 0.001 ~ "***",
    p_value < 0.01 ~ "**",
    p_value < 0.05 ~ "*",
    TRUE ~ "ns"
  ))

print(plot1_stats)

setwd("C:/Users/wrede/OneDrive - JGU/Desktop/Masterarbeit/model organisms/mapped_hk_length")  # set working directory
human <- read_tsv("human_mapped_length.tsv") # import data
mouse <- read_tsv("mouse_mapped_length.tsv") # import data
fruitfly <- read_tsv("fruitfly_mapped_length.tsv") # import data
celegans <- read_tsv("celegans_mapped_length.tsv") # import data


human <- human %>%
  mutate(Hk = recode(Hk, `0` = "not Hk", `1` = "Hk"),
         Hk = as.factor(Hk),
         Hk = factor(Hk, levels = rev(levels(Hk))),
         genelength = as.numeric(genelength)) %>%
  filter(!is.na(genelength))
  
ggplot(human, aes(x=genelength, y = Length, color = Hk)) +
  geom_point(size = 0.5) +
  geom_smooth(method = "lm", se = FALSE, color = "black") +
  #scale_x_log10() +
  my_theme +
  ylab("Protein length") +
  xlab("Gene length") +
  coord_cartesian(ylim = c(0, 5000), xlim = c(0, 500000))

mouse <- mouse %>%
  mutate(Hk = recode(Hk, `0` = "not Hk", `1` = "Hk"),
         Hk = as.factor(Hk),
         Hk = factor(Hk, levels = rev(levels(Hk))),
         genelength = as.numeric(genelength)) %>%
  filter(!is.na(genelength))

ggplot(mouse, aes(x=genelength, y = Length, color = Hk)) +
  geom_point(size = 0.1) +
  geom_smooth(method = "lm", se = FALSE, color = "black") +
  scale_x_log10() +
  my_theme +
  coord_cartesian(ylim = c(0, 1000))
