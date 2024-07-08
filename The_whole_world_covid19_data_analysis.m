%% CFR comparison between high-income and low-income (hypothesis test) 
% the path of data excel – maybe you can find in the kaggle
excelFilePath = "C:\Users\jarid\OneDrive\바탕 화면\penguin\covid_data.xlsx"; 

% Read the data from the data excel file
data = readtable(excelFilePath, 'Sheet', 'Tab 1'); 

% Allocate the 'Confirmed' and 'Deaths' columns directly
confirmed = data.Confirmed;
deaths = data.Deaths;

% Calculate the Case Fatality Rate (CFR) 
% this is for the result 
data.CFR = (deaths ./ confirmed) * 100;

% checking for reading the data 
head(data, 10) 

% Create logical areas for high income (5) and low income (2) countries
% for comparison 
highIncomeIndex = data.Income == 5;
lowIncomeIndex = data.Income == 2;

% Extract CFR for high income and low income countries
highIncomeCFR = data.CFR(highIncomeIndex);
lowIncomeCFR = data.CFR(lowIncomeIndex);

H0='mu1=mu2, the average CFR of high income countries is equal to the CFR of low income countries';
HA='mu1<mu2, the average CFR of high income countries is lower than the CFR of low income countries';

% Check if highIncomeCFR and lowIncomeCFR are non-empty vectors 
if ~isempty(highIncomeCFR) && ~isempty(lowIncomeCFR) && isvector(highIncomeCFR) && isvector(lowIncomeCFR)

    [h, p, ~, stats] = ttest2(highIncomeCFR, lowIncomeCFR, 'tail', 'left', 'alpha', 0.05, 'vartype', 'unequal');

    % Display the p-value 
    disp(['h: ',num2str(h)])
    disp(['p: ',num2str(p)])
    disp('Statistics: ')
    disp(stats)

    fprintf('p-value: %f\n', p);
else
    disp('One of the groups is empty or not a vector, cannot perform ttest2.');
end

%% To better know which one is higher than the other one
% cause only p value we can't confirm that 
highIncomeCFRNoNan = highIncomeCFR(~isnan(highIncomeCFR)); % remove NaN values from highIncomeCFR
lowIncomeCFRNoNan = lowIncomeCFR(~isnan(lowIncomeCFR)); % remove NaN values from lowIncomeCFR

medianHighIncomeCFR = median(highIncomeCFRNoNan);
medianLowIncomeCFR = median(lowIncomeCFRNoNan);
disp(['median value of CFR for high income countries : ', num2str(medianHighIncomeCFR)]);
disp(['median value of CFR for low income countries : ', num2str(medianLowIncomeCFR)]);

meanHighIncomeCFR = mean(highIncomeCFRNoNan);
meanLowIncomeCFR = mean(lowIncomeCFRNoNan);
disp(['mean value of CFR for high income countries : ', num2str(meanHighIncomeCFR)]);
disp(['mean value of CFR for low income countries : ', num2str(meanLowIncomeCFR)]);

% meanHighIncomeCFR < meanLowIncomeCFR
%% plot and visualize for CFR comparison between high-income and low-income (hypothesis test) using boxplot 

% For the start 
figure;

% Combine highIncomeCFR and lowIncomeCFR into one array for box plotting
groupedCFR = [highIncomeCFR; lowIncomeCFR];

% Grouping things 
group = [repmat({'High Income'}, length(highIncomeCFR), 1); repmat({'Low Income'}, length(lowIncomeCFR), 1)];

% Create a boxplot
boxplot(groupedCFR, group);

% Title and labels 
title('CFR Comparison Between High-Income and Low-Income Countries');
ylabel('Case Fatality Rate (%)');
xlabel('Income Level');

hold on; 
means = [meanHighIncomeCFR, meanLowIncomeCFR];
plot([1, 2], means, 'g*', 'MarkerSize', 10); 
% then now this boxplot makes sense 

ylim([0 max(groupedCFR)*1.1]); 

hold off; 

My MATLAB code focuses on comparing the Case Fatality Rate (CFR) between high-income and low-income countries using a hypothesis test. The first step involves reading data from an Excel file located at "C:\Users\jarid\OneDrive\바탕 화면\penguin\covid_data.xlsx", specifically from the sheet named 'Tab 1'. After loading the data, the code calculates the CFR for each entry by dividing the number of deaths by the number of confirmed cases and multiplying the result by 100 to express it as a percentage. This new CFR value is then added as a column to the data table.
To distinguish between high-income and low-income countries, the code creates logical indices based on the income level, where high-income countries are marked with an income level of 5 and low-income countries with an income level of 2. Using these indices, the code extracts the CFR values for both high-income and low-income groups. The hypothesis test is then set up with the null hypothesis stating that the average CFR of high-income countries is equal to that of low-income countries, while the alternative hypothesis posits that the average CFR of high-income countries is lower.
A two-sample t-test is conducted to compare the CFR values between the two groups, using a one-tailed test to check if the CFR in high-income countries is significantly lower than in low-income countries. The test results include the decision (whether to reject the null hypothesis), the p-value, and other relevant statistics. To further understand the data, the code calculates and displays the median and mean CFR values for both high-income and low-income countries, providing a clearer picture of the central tendencies within each group.
Further more, the code generates a boxplot to visualize the distribution of CFR values for high-income and low-income countries. This plot includes markers for the mean CFR values of each group and sets the y-axis limits to ensure a clear view of the data distribution. Through this comprehensive approach, the code not only performs a statistical comparison but also provides a visual representation of the differences in CFR between countries of different income levels, enhancing the overall understanding of the data.

%% CFR comparison between old countries and young countries (hypothesis test)  

% According to the UN standards, 
% the proportion of peoper aged 65 or older, is more than 7% -> aging society 
% ~ if that proportion > 14% -> aged society
% if more than 20% -> super-aged society 
young_society = data.old <= 7;
aging_society = (data.old > 7) & (data.old <= 14); 
aged_society = (data.old > 14) & (data.old <= 20);
super_aged_society = data.old > 20;


% Extract CFR for each socities
youngCFR = data.CFR(young_society);
agingCFR = data.CFR(aging_society);
agedCFR = data.CFR(aged_society);
superAgedCFR = data.CFR(super_aged_society);

H0 = 'The population means of CFR from all groups are equal.'; 
HA = 'The population means of CFR from all groups are not all equal, at least one group''s distribution of CFR is different from the others.';
% anova1 test is still comparing mean values from each groups 
% so the mechanism is almost the same 

% Check if youngCFR, agingCFR, super_aged_society and agedCFR are non-empty vectors again 
if ~isempty(youngCFR) && ~isempty(agingCFR) && isvector(youngCFR) && isvector(agingCFR) && ~isempty(super_aged_society) && ~isempty(agedCFR) && isvector(super_aged_society) && isvector(agedCFR)
    cfrValues = [youngCFR; agingCFR; agedCFR; superAgedCFR];
    groups = [repmat({'Young'}, length(youngCFR), 1); repmat({'Aging'}, length(agingCFR), 1); ...
             repmat({'Aged'}, length(agedCFR), 1); repmat({'SuperAged'}, length(superAgedCFR), 1)];

        [p,t,stats] = anova1(cfrValues, groups, 'off');
        % https://uk.mathworks.com/help/stats/anova1.html
        % data plotting 'off', honestly I don't understand the output of
        % anova1 plot part of this 

    % Display the p-value 
    fprintf('p-value: %.2e\n', p);
    % and the p-value is very low for this 
    % very interesting 
else
    disp('One of the groups is empty or not a vector, cannot perform anova1 test.');
end

%% to better know which one is higher than the other one

youngCFRNoNan = youngCFR(~isnan(youngCFR));
agingCFRNoNan = agingCFR(~isnan(agingCFR));
agedCFRNoNan = agedCFR(~isnan(agedCFR));
superAgedCFRNoNan = superAgedCFR(~isnan(superAgedCFR));

medianyoungCFR = median(youngCFRNoNan);
medianagingCFR = median(agingCFRNoNan);
medianagedCFR = median(agedCFRNoNan);
mediansuperAgedCFR = median(superAgedCFRNoNan);

meanyoungCFR = mean(youngCFRNoNan);
meanagingCFR = mean(agingCFRNoNan);
meanagedCFR = mean(agedCFRNoNan);
meansuperAgedCFR = mean(superAgedCFRNoNan);

disp(['median value of CFR for young countries : ', num2str(medianyoungCFR)]);
disp(['median value of CFR for aging countries : ', num2str(medianagingCFR)]);
disp(['median value of CFR for aged countries : ', num2str(medianagedCFR)]);
disp(['median value of CFR for super aged countries : ', num2str(mediansuperAgedCFR)]);

disp(['mean value of CFR for young countries : ', num2str(meanyoungCFR)]);
disp(['mean value of CFR for aging countries : ', num2str(meanagingCFR)]);
disp(['mean value of CFR for aged countries : ', num2str(meanagedCFR)]);
disp(['mean value of CFR for super aged countries : ', num2str(meansuperAgedCFR)]);

% medianyoungCFR < medianagingCFR < medianagedCFR < mediansuperAgedCFR 
% about mean there is not a direct conclusion but it still shows the clear trend


My MATLAB code (this part) aims to compare the Case Fatality Rate (CFR) among countries categorized by their aging population, following UN standards. The classification is based on the proportion of people aged 65 or older: a young society has up to 7% elderly, an aging society has between 7% and 14%, an aged society ranges from 14% to 20%, and a super-aged society exceeds 20%. Using this classification, the code extracts CFR values for each group.

To test the hypothesis that the average CFR is the same across all these groups, the code performs a one-way ANOVA. The null hypothesis (H0) asserts that the population means of CFR from all groups are equal, while the alternative hypothesis (HA) states that at least one group's CFR distribution differs from the others. Before conducting the ANOVA, the code checks if the CFR data for each group are non-empty vectors. If this condition is met, the CFR values are concatenated into a single array, and corresponding group labels are assigned. The `anova1` function is then used to perform the test, with the p-value indicating whether there's a statistically significant difference in CFR among the groups.

The code proceeds to calculate and display the median and mean CFR values for each group to provide a deeper understanding of the central tendencies. By removing any NaN values, the median and mean CFRs for young, aging, aged, and super-aged societies are computed. These values are printed to offer insights into the data trends.

Finally, the code discusses the results, noting that while median values show a clear trend with increasing CFR from young to super-aged societies, the mean values, although not as straightforward, still indicate a similar trend. This comprehensive approach, combining statistical testing and descriptive statistics, shows the differences in CFR among countries with varying proportions of elderly populations.








%% CFR comparison between good report system and bad report system (hypothesis test)

%this is to know the mean value
all_numbers_report = data.Report;
all_numbers_reportNoNan = all_numbers_report(~isnan(all_numbers_report));
mean(all_numbers_reportNoNan) % 0.0736
% I need to multiply 100 
% because I got those numbers Report = (total test) / (total population); 
% this is just the ratio not population 
% so the mean of the report system population is 7.3639 
% higher than mean will be good report system countries (sample)
% lower than mean will be bad report system countries (sample) 
% and I found that I don't need to do that
% cause this will be used as the standard, that's all 

goodReportIndex = data.Report >= 0.0736;
badReportIndex = data.Report < 0.0736; 

% Extract CFR for high income and low income countries
goodReportCFR = data.CFR(goodReportIndex);
badReportCFR = data.CFR(badReportIndex );

H0='mu1=mu2, the average CFR of good report countries is equal to the CFR of bad report countries';
HA='mu1<mu2, the average CFR of good report countries is lower than the CFR of bad report countries';

% Check if highIncomeCFR and lowIncomeCFR are non-empty vectors 
if ~isempty(goodReportCFR) && ~isempty(badReportCFR) && isvector(goodReportCFR) && isvector(badReportCFR)
    % Perform a statistical test

    [h, p, ~, stats] = ttest2(goodReportCFR, badReportCFR, 'tail', 'left', 'alpha', 0.05, 'vartype', 'unequal');

    % Display the p-value 
    disp(['h: ',num2str(h)])
    disp(['p: ',num2str(p)])
    disp('Statistics: ')
    disp(stats)

    fprintf('p-value: %f\n', p);
else
    disp('One of the groups is empty or not a vector, cannot perform ttest2.');
end

%% to better know which one is higher than the other one

% Extract CFR for high income and low income countries
goodReportCFR = data.CFR(goodReportIndex);
badReportCFR = data.CFR(badReportIndex);

goodReportCFRNoNan = goodReportCFR(~isnan(goodReportCFR)); % Remove NaN values from goodReportCFR
badReportCFRNoNan = badReportCFR(~isnan(badReportCFR)); % Remove NaN values from badReportCFR

mediangoodReportCFR = median(goodReportCFRNoNan);
medianbadReportCFR = median(badReportCFRNoNan);
disp(['median value of CFR for good report countries : ', num2str(mediangoodReportCFR)]);
disp(['median value of CFR for bad report countries : ', num2str(medianbadReportCFR)]);

meangoodReportCFR = mean(goodReportCFRNoNan);
meanbadReportCFR = mean(badReportCFRNoNan);
disp(['mean value of CFR for good report countries : ', num2str(meangoodReportCFR)]);
disp(['mean value of CFR for bad report countries : ', num2str(meanbadReportCFR)]);

%% plot and visualize for CFR comparison between Good Report and bad Report (hypothesis test) using boxplot 

% For the start 
figure;

% Combine goodReportCFR and badReportCFR into one array for box plotting
groupedCFR = [goodReportCFR; badReportCFR];

% Grouping things 
group = [repmat({'Good Report'}, length(goodReportCFR), 1); repmat({'Bad Report'}, length(badReportCFR), 1)];

% Create a boxplot
boxplot(groupedCFR, group);

% Title and labels 
title('CFR Comparison Between Good Report system countries and Bad Report system countries');
ylabel('Case Fatality Rate (%)');
xlabel('Report System');

hold on; 
means = [meangoodReportCFR, meanbadReportCFR];
plot([1, 2], means, 'g*', 'MarkerSize', 10); 

ylim([0 max(groupedCFR)*1.1]); 

hold off; 

%% Understand the glimpse of replationship between variables 

y = data.CFR;

X = [data.Income, data.old, data.Report];

X = [ones(height(data), 1), X];

[b, bint, r, rint, stats] = regress(y, X);

disp('Regression Coefficients:');
disp(b);

disp('Statistics:');
disp(stats);

% but the r-squared 0.0297 is very low so 
% this only shows very low relationships 
% only 2.97 % can be explained to it 
% so this is not a good model to describe it as a multiple variables linear regression 

figure;
scatter(data.Income, data.old, 'filled');
title('Relationship Between Income Levels and Age Demographics');
xlabel('Income Level');
ylabel('Percentage of Population Aged 65 or Older');
grid on;

figure;
scatter(data.Income, data.Report, 'filled');
title('Relationship Between Income Levels and Reporting System Quality');
xlabel('Income Level');
ylabel('Report Ratio (Total Tests / Total Population)');
grid on;

% Correlation between Income and Age Demographics
[r_age, p_age] = corr(data.Income, data.old);
fprintf('Correlation between Income and Age Demographics: r = %.2f, p-value = %.3f\n', r_age, p_age);

% Correlation between Income and Reporting System
[r_report, p_report] = corr(data.Income, data.Report);
fprintf('Correlation between Income and Reporting System: r = %.2f, p-value = %.3f\n', r_report, p_report);


My MATLAB code this part is designed to compare the Case Fatality Rate (CFR) between countries with good and bad reporting systems using a hypothesis test. Initially, it calculates the mean of the reporting system metric from the dataset, excluding any NaN values. The mean value found is approximately 0.0736, representing the ratio of total tests to the total population. Countries with a reporting system value above this mean are classified as having good reporting systems, while those below are classified as having bad reporting systems.

Once the classification is complete, the code extracts the CFR values for both groups. The null hypothesis (H0) asserts that the average CFR of countries with good reporting systems is equal to that of countries with bad reporting systems. Conversely, the alternative hypothesis (HA) suggests that the average CFR of countries with good reporting systems is lower. A two-sample t-test is conducted to compare the CFRs, using a one-tailed test to check if the good reporting system countries have a significantly lower CFR. The test results, including the p-value, are displayed to determine statistical significance.

To gain deeper insights, the code calculates and displays the median and mean CFR values for both good and bad reporting system groups, excluding any NaN values. This step helps to understand the central tendencies within each group, offering a clearer view of the data trends. The results indicate whether one group has a consistently lower CFR compared to the other.

The code also includes a visualization component, generating a boxplot to compare the CFR distributions between countries with good and bad reporting systems. The plot includes markers for the mean CFR values of each group and sets appropriate y-axis limits to ensure clarity. This visual representation helps to easily compare the distributions and identify any notable differences.

Additionally, the code explores the relationship between various variables, such as income levels, age demographics, and reporting system quality. It performs multiple linear regression to understand how these factors collectively influence the CFR. The regression results, including coefficients and statistics, are displayed, although the low R-squared value suggests that the model does not explain a significant portion of the variance in CFR.

Scatter plots are created to visualize the relationships between income levels and age demographics, as well as between income levels and reporting system quality. These plots help to identify any correlations visually. Further, the code calculates and displays the correlation coefficients and p-values for these relationships, providing a statistical measure of their strength and significance.

My MATLAB code (overall) encompasses a detailed statistical analysis of the Case Fatality Rate (CFR) across different categories of countries, focusing on income levels, aging demographics, and the quality of reporting systems. Initially, the code calculates and compares CFR between high-income and low-income countries using a two-sample t-test, and then similarly analyzes CFR across young, aging, aged, and super-aged societies through ANOVA. It further compares CFR between countries with good and bad reporting systems using another two-sample t-test. For each analysis, the code computes median and mean CFR values, visualizes the results through boxplots, and performs hypothesis testing to determine statistical significance. Additionally, it investigates the relationships between variables such as income levels, age demographics, and reporting quality using multiple linear regression and correlation analyses, providing comprehensive insights into how these factors interrelate and affect CFR. The visualizations and statistical outputs collectively offer a robust understanding of the variations in CFR and the impact of socioeconomic factors.

