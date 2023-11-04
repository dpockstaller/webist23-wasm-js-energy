#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install pandas matplotlib seaborn numpy scipy statsmodels scikits.bootstrap


# In[2]:


import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy
from scipy import stats
import scipy
import helper.cliffs_delta as cliff
import statsmodels.api as sm
import itertools
import scikits.bootstrap as boot


# # Table of contents
# 1. [RQ1: JS vs. WASM Energy Consumption](#rq1)
# 2. [RQ2: JS Browsers Energy Consumption](#rq2js)
# 3. [RQ2: WASM Browsers Energy Consumption](#rq2wasm)

# # Prepare Data

# In[3]:


sns.set(rc = {'figure.figsize':(10,10)})
confidence_level = 0.95

df = pd.read_csv('./data/energy.csv',sep=';',quotechar='"',names=["browser", "language", "algorithm", "device", "energy"])
df['energy_total'] = df['energy'].astype(float)
df['implementation'] = numpy.where(df['language'] == 'js', 'js', 'wasm')

## unique values in columns
browsers = numpy.sort(df['browser'].unique())
browserpairs = list(itertools.combinations(browsers, 2))
languages = df['language'].unique()
implementations = numpy.sort(df['implementation'].unique())
implementationpairs = list(itertools.combinations(implementations, 2))
languagepairs = list(itertools.combinations(languages, 2))
algorithms = df['algorithm'].unique()
devices = df['device'].unique()

df.head()


# ## Count samples

# In[4]:


data = []

for browser in browsers:
    for language in languages:
        for algorithm in algorithms:
            for device in devices:
                #print(browser,device,numpy.mean(df[(df['browser'] == browser) & (df['language'] == language) & (df['algorithm'] == algorithm) & (df['device'] == device)]['energy']))
                data.append(
                    [browser, language, algorithm, device, df[(df['browser'] == browser) & (df['language'] == language) & (df['algorithm'] == algorithm) & (df['device'] == device)]['energy_total'].count()]
                )

# Create the pandas DataFrame
count = pd.DataFrame(data, columns = ['browser', 'language', 'algorithm', 'device', 'count'])
print(count.to_string())


# ## Total Energy

# In[5]:


data = []
for device in devices:
    for implementation in implementations:
        x = df[(df['device'] == device) & (df['implementation'] == implementation)]
        sum = numpy.round(numpy.sum(x['energy']), 2)

        data.append(
            [device, implementation, sum]
        )
        
# Create the pandas DataFrame
stat = pd.DataFrame(data, columns = ['device', 'implementation', 'sum'])
print(stat.to_string())


# # Violinplot (Algorithms)

# In[6]:


for device in devices:
    for browser in browsers:
        data = df[(df['device'] == device) & (df['browser'] == browser)].sort_values(by=['algorithm'])
        plt.figure()
        plt.xticks(rotation=90)
        plt.ylim(0, 35)
        sns.violinplot(x='algorithm', y='energy', hue='implementation', hue_order=implementations, data=data, palette='colorblind', split=True).set_title(device + " - " + browser)


# # RQ1: JavaScript vs. WebAssembly <a name="rq1"></a>

# ## Shapiro Wilk Test

# In[7]:


data = []
non_normal = 0

for implementation in implementations:
    energy = df[(df['implementation'] == implementation)]['energy']

    if len(energy) >= 3:
        shapiro_test = stats.shapiro(energy)

        non_normal += (1 if shapiro_test.pvalue <= 0.05 else 0)

        data.append(
            [implementation,
             shapiro_test.statistic,
             shapiro_test.pvalue
            ]
        )
        
# Create the pandas DataFrame
swt = pd.DataFrame(data, columns = ['implementation', 'w', 'p'])
#print(swt.to_string())
display(swt)

print("\n{} non-normally distributed samples".format(non_normal))
print("{} normally distributed samples".format(len(swt) - non_normal))
print("{:.2f}% non-normally distributed samples".format(non_normal/len(swt)*100)) 


# ## Shapiro Wilk Test (By Device)

# In[8]:


data = []
non_normal = 0

for device in devices:
    for implementation in implementations:
        energy = df[(df['implementation'] == implementation) & (df['device'] == device)]['energy']

        if len(energy) >= 3:
            shapiro_test = stats.shapiro(energy)

            non_normal += (1 if shapiro_test.pvalue <= 0.05 else 0)

            data.append(
                [
                 device,
                 implementation,
                 shapiro_test.statistic,
                 shapiro_test.pvalue
                ]
            )
        
# Create the pandas DataFrame
swt = pd.DataFrame(data, columns = ['device', 'implementation', 'w', 'p'])
#print(swt.to_string())
display(swt)

print("\n{} non-normally distributed samples".format(non_normal))
print("{} normally distributed samples".format(len(swt) - non_normal))
print("{:.2f}% non-normally distributed samples".format(non_normal/len(swt)*100)) 


# ## Mann-Whitney-U-Test

# In[9]:


data = []

for implementationpair in implementationpairs:
    impl1_energy = df[(df['implementation'] == implementationpair[0])]['energy']
    impl2_energy = df[(df['implementation'] == implementationpair[1])]['energy']
    eff = cliff.cliffs_delta(impl1_energy, impl2_energy)

    u = stats.mannwhitneyu(impl1_energy, impl2_energy, alternative='two-sided')            

    data.append(
        [
         implementationpair[0] + ' vs. ' + implementationpair[1],
         u.statistic,
         u.pvalue,
         eff[0],
         eff[1]
        ]
    )
        
# Create the pandas DataFrame
ut = pd.DataFrame(data, columns = ['implementation', 'u', 'p', 'eff', 'interp'])
display(ut)

interp = ut['interp'].value_counts()
interp = pd.DataFrame(interp, columns = ['interp', 'percent'])
interp['percent'] = (interp['interp'] / interp['interp'].sum()) * 100

display(interp)


# ## Violinplot

# In[10]:


data = df
plt.ylim(0, 35)
vp = sns.violinplot(x='implementation', y='energy', hue='implementation', hue_order=implementations, data=data, palette='colorblind' ,dodge=False)
vp.set_title("Energy Consumption by Implementations - " + device + " - " + browser)
vp.set_ylabel("Energy (Joules)")
plt.show()


# ## Violinplot (By Browser)

# In[11]:


data = []
for browser in browsers:
    data = df[(df['browser'] == browser)]
    plt.ylim(0, 35)
    vp = sns.violinplot(x='implementation', y='energy', hue='implementation', hue_order=implementations, data=data, palette='colorblind' ,dodge=False)
    vp.set_title("Energy Consumption by Implementations - " + device + " - " + browser)
    vp.set_ylabel("Energy (Joules)")
    plt.show()


# ## Violinplot (By Browser & By Device)

# In[12]:


data = []
for device in devices:
    for browser in browsers:
        data = df[(df['browser'] == browser) & (df['device'] == device)].sort_values(by=['implementation'])
        plt.ylim(0, 35)
        vp = sns.violinplot(x='implementation', y='energy', hue='implementation', hue_order=implementations, data=data, palette='colorblind', dodge=False)
        vp.set_title(device + " - " + browser)
        vp.set_ylabel("Energy (Joules)")
        plt.show()


# In[13]:


data = []
index=0
fig, axes = plt.subplots(1, 4, figsize=(20, 5))

for device in devices:
    for browser in browsers:
        data = df[(df['browser'] == browser) & (df['device'] == device)].sort_values(by=['implementation'])
        vp = sns.violinplot(x='implementation', y='energy', hue='implementation', hue_order=implementations, data=data, palette='colorblind', dodge=False, ax=axes[index])
        vp.set_title(device + " - " + browser)
        axes[index].set_ylim(0, 35)
        axes[index].set_xlabel("")
        if index == 0:
            axes[0].set_ylabel("Energy (Joules)")
        else:
            axes[index].set_ylabel("")
        index+=1


# ## Violinplot (By Browser & Low End Device)

# In[14]:


data = []

index=0
fig, axes = plt.subplots(1, 2, figsize=(18, 8))
for browser in browsers:
    data = df[(df['browser'] == browser) & (df['device'] == 'Nexus 5')].sort_values(by=['implementation'])
    vp = sns.violinplot(x='implementation', y='energy', hue='implementation', hue_order=implementations, data=data, palette='colorblind', dodge=False, ax=axes[index])
    vp.set_title("Nexus 5 - " + browser)
    axes[index].set_ylim(0, 35)
    axes[index].set_xlabel("")
    if index == 0:
        axes[0].set_ylabel("Energy (Joules)")
    else:
        axes[index].set_ylabel("")
    index+=1


# ## Violinplot (By Browser & High End Device)

# In[15]:


data = []

index=0
fig, axes = plt.subplots(1, 2, figsize=(18, 8))
for browser in browsers:
    data = df[(df['browser'] == browser) & (df['device'] == 'SM-G991B')].sort_values(by=['implementation'])
    vp = sns.violinplot(x='implementation', y='energy', hue='implementation', hue_order=implementations, data=data, palette='colorblind', dodge=False, ax=axes[index])
    vp.set_title("SM-G991B - " + browser)
    axes[index].set_ylim(0, 35)
    axes[index].set_xlabel("")
    if index == 0:
        axes[0].set_ylabel("Energy (Joules)")
    else:
        axes[index].set_ylabel("")
    index+=1
        #plt.show()


# ## Violinplot (By Browser & Device Types)

# In[16]:


## Prepare naming of values for final violinplot
df_violin = df.copy()
df_violin['implementation'] = df_violin['implementation'].replace(['wasm'], 'Wasm')
df_violin['implementation'] = df_violin['implementation'].replace(['js'], 'JS')
df_violin['browser'] = df_violin['browser'].replace(['chrome'], 'Chrome')
df_violin['browser'] = df_violin['browser'].replace(['firefox'], 'Firefox')
df_violin['device'] = df_violin['device'].replace(['SM-G991B'], 'Samsung Galaxy S21')
browsers_violin = numpy.sort(df_violin['browser'].unique())
devices_violin = numpy.sort(df_violin['device'].unique())


# In[17]:


sns.set(font_scale=2)
data = []
index=0
fig, axes = plt.subplots(1, 2, figsize=(18, 8))
for device in devices_violin:
    data = df_violin[(df_violin['device'] == device)].sort_values(by=['implementation'])
    vp = sns.violinplot(x='implementation', y='energy', hue='browser', hue_order=browsers_violin, data=data, palette='colorblind', dodge=False, ax=axes[index], split=True)
    vp.set_title(device)
    axes[index].legend(title="Browsers")
    axes[index].set_ylim(0, 35)
    axes[index].set_xlabel("")
    axes[index].set_ylabel("Energy Consumption (Joules)")
    if index == 0:
        axes[0].set_ylabel("Energy Consumption (Joules)")
    else:
        axes[index].set_ylabel("")
        axes[index].set_yticklabels([])
    index+=1


# ## Histogram

# In[18]:


sns.histplot(data=df, x="energy", hue="implementation", hue_order=implementations).set_title("Energy Consumption by Implementations")
plt.xlabel("Energy (Joules)")
plt.ylim(0, 400)
plt.xlim(0, 40)


# ## Histogram (By Device)

# In[19]:


data = []
for device in devices:
    data = df[(df['device'] == device)]
    plt.xlabel("Energy (Joules)")
    plt.ylim(0, 400)
    plt.xlim(0, 40)
    sns.histplot(data=data, x="energy", hue="implementation", hue_order=implementations).set_title("Energy Consumption by Implementations - " + device)
    plt.show()


# ## Q-Q-Plot

# In[20]:


data = []
for implementation in implementations:
    data = df[(df['implementation'] == implementation)]
    qq = sm.qqplot(data.energy, line='s')
    h = plt.title(implementation)


# ## Q-Q-plot (By Device)

# In[21]:


data = []
for device in devices:
    for implementation in implementations:
        data = df[(df['implementation'] == implementation) & (df['device'] == device)]
        qq = sm.qqplot(data.energy, line='s')
        h = plt.title(implementation + " - " + device)


# ## Mann Whitney U Test (same Browsers)

# In[22]:


data = []

for browser in browsers:
    for implementationpair in implementationpairs:
        impl1_energy = df[(df['implementation'] == implementationpair[0]) & (df['browser'] == browser)]['energy']
        impl2_energy = df[(df['implementation'] == implementationpair[1]) & (df['browser'] == browser)]['energy']
        eff = cliff.cliffs_delta(impl1_energy, impl2_energy)

        u = stats.mannwhitneyu(impl1_energy, impl2_energy, alternative='two-sided')            

        data.append(
            [
             browser,
             implementationpair[0] + ' vs. ' + implementationpair[1],
             u.statistic,
             u.pvalue,
             eff[0],
             eff[1]
            ]
        )
        
# Create the pandas DataFrame
ut = pd.DataFrame(data, columns = ['browser', 'implementation', 'u', 'p', 'eff', 'interp'])
display(ut)

interp = ut['interp'].value_counts()
interp = pd.DataFrame(interp, columns = ['interp', 'percent'])
interp['percent'] = (interp['interp'] / interp['interp'].sum()) * 100

display(interp)


# ## Mann Whitney U Test (same Browsers - by Device)

# In[23]:


data = []

for device in devices:
    for browser in browsers:
        for implementationpair in implementationpairs:
            impl1_energy = df[(df['implementation'] == implementationpair[0]) & (df['browser'] == browser) & (df['device'] == device)]['energy']
            impl2_energy = df[(df['implementation'] == implementationpair[1]) & (df['browser'] == browser) & (df['device'] == device)]['energy']
            eff = cliff.cliffs_delta(impl1_energy, impl2_energy)

            u = stats.mannwhitneyu(impl1_energy, impl2_energy, alternative='two-sided')            

            data.append(
                [
                 device,
                 browser,
                 implementationpair[0] + ' vs. ' + implementationpair[1],
                 u.statistic,
                 u.pvalue,
                 eff[0],
                 eff[1]
                ]
            )
        
# Create the pandas DataFrame
ut = pd.DataFrame(data, columns = ['device', 'browser', 'implementation', 'u', 'p', 'eff', 'interp'])
display(ut)

interp = ut['interp'].value_counts()
interp = pd.DataFrame(interp, columns = ['interp', 'percent'])
interp['percent'] = (interp['interp'] / interp['interp'].sum()) * 100

display(interp)


# ## Mann Whitney U Test (Cross Browsers)

# In[24]:


data = []

for pairswitch in [[0,1],[1,0]]:
    for implementationpair in implementationpairs:
        for browserpair in browserpairs:
            browser1_energy = df[(df['browser'] == browserpair[0]) & (df['implementation'] == implementationpair[pairswitch[0]])]['energy']
            browser2_energy = df[(df['browser'] == browserpair[1]) & (df['implementation'] == implementationpair[pairswitch[1]])]['energy']
            eff = cliff.cliffs_delta(browser1_energy, browser2_energy)

            u = stats.mannwhitneyu(browser1_energy, browser2_energy, alternative='two-sided')            

            data.append(
                [
                 browserpair[0] + ' vs. ' + browserpair[1],
                 implementationpair[pairswitch[0]] + ' vs. ' + implementationpair[pairswitch[1]],
                 u.statistic,
                 u.pvalue,
                 eff[0],
                 eff[1]
                ]
            )
        
# Create the pandas DataFrame
ut = pd.DataFrame(data, columns = ['browser', 'implementation', 'u', 'p', 'eff', 'interp'])
display(ut)

interp = ut['interp'].value_counts()
interp = pd.DataFrame(interp, columns = ['interp', 'percent'])
interp['percent'] = (interp['interp'] / interp['interp'].sum()) * 100

display(interp)


# ## Mann Whitney U Test (Cross Browsers - By Device)

# In[25]:


data = []

for device in devices:
    for pairswitch in [[0,1],[1,0]]:
        for implementationpair in implementationpairs:
            for browserpair in browserpairs:
                browser1_energy = df[(df['browser'] == browserpair[0]) & (df['implementation'] == implementationpair[pairswitch[0]]) & (df['device'] == device)]['energy']
                browser2_energy = df[(df['browser'] == browserpair[1]) & (df['implementation'] == implementationpair[pairswitch[1]]) & (df['device'] == device)]['energy']
                eff = cliff.cliffs_delta(browser1_energy, browser2_energy)

                u = stats.mannwhitneyu(browser1_energy, browser2_energy, alternative='two-sided')            

                data.append(
                    [
                     device,
                     browserpair[0] + ' vs. ' + browserpair[1],
                     implementationpair[pairswitch[0]] + ' vs. ' + implementationpair[pairswitch[1]],
                     u.statistic,
                     u.pvalue,
                     eff[0],
                     eff[1]
                    ]
                )
        
# Create the pandas DataFrame
ut = pd.DataFrame(data, columns = ['device', 'browser', 'implementation', 'u', 'p', 'eff', 'interp'])
display(ut)

interp = ut['interp'].value_counts()
interp = pd.DataFrame(interp, columns = ['interp', 'percent'])
interp['percent'] = (interp['interp'] / interp['interp'].sum()) * 100

display(interp)


# ## Descriptive Statistics

# In[26]:


data = []
for implementation in implementations:
    x = df[(df['implementation'] == implementation)]
    mean = numpy.round(numpy.mean(x['energy']), 2)
    median = numpy.round(numpy.median(x['energy']), 2)
    min = numpy.round(numpy.amin(x['energy']), 2)
    max = numpy.round(numpy.amax(x['energy']), 2)
    std = numpy.round(numpy.std(x['energy']), 2)
    sem = numpy.round(stats.sem(x['energy']), 2)
    q1 = numpy.round(numpy.quantile(x['energy'], 0.25), 2)
    q3 = numpy.round(numpy.quantile(x['energy'], 0.75), 2)
    
    data.append(
        [implementation, mean, std, min, q1, median, q3, max, sem]
    )
        
# Create the pandas DataFrame
stat = pd.DataFrame(data, columns = ['implementation', 'mean', 'std', 'min', 'q1', 'median', 'q3', 'max', 'sem'])
# display(stat)
print(stat.to_string())

# Alternative of pandas: x['energy'].describe()


# ## Descriptive Statistics Difference

# In[27]:


data = []

for implementationpair in implementationpairs:
    implementation1 = stat[(stat['implementation'] == implementationpair[1])]
    implementation2 = stat[(stat['implementation'] == implementationpair[0])]
    
    mean_diff = implementation1.iloc[0]['mean']-implementation2.iloc[0]['mean']
    median_diff = implementation1.iloc[0]['median']-implementation2.iloc[0]['median']
    min_diff = implementation1.iloc[0]['min']-implementation2.iloc[0]['min']
    max_diff = implementation1.iloc[0]['max']-implementation2.iloc[0]['max']
    std_diff = implementation1.iloc[0]['std']-implementation2.iloc[0]['std']
    sem_diff = implementation1.iloc[0]['sem']-implementation2.iloc[0]['sem']
    q1_diff = implementation1.iloc[0]['q1']-implementation2.iloc[0]['q1']
    q3_diff = implementation1.iloc[0]['q3']-implementation2.iloc[0]['q3']

    data.append(
        [implementationpair[1] + ' vs. ' + implementationpair[0],
         numpy.round(mean_diff, 2),
         numpy.round(mean_diff/implementation2.iloc[0]['mean']*100, 2),
         numpy.round(median_diff, 2),
         numpy.round(median_diff/implementation2.iloc[0]['median']*100, 2),
         numpy.round(min_diff, 2),
         numpy.round(min_diff/implementation2.iloc[0]['min']*100, 2),
         numpy.round(max_diff, 2),
         numpy.round(max_diff/implementation2.iloc[0]['max']*100, 2),
         numpy.round(std_diff, 2),
         numpy.round(std_diff/implementation2.iloc[0]['std']*100, 2),
         numpy.round(sem_diff, 2),
         numpy.round(sem_diff/implementation2.iloc[0]['sem']*100, 2),
         numpy.round(q1_diff, 2),
         numpy.round(q1_diff/implementation2.iloc[0]['q1']*100, 2),
         numpy.round(q3_diff, 2),
         numpy.round(q3_diff/implementation2.iloc[0]['q3']*100, 2),
        ]
    )
        
# Create the pandas DataFrame
ut = pd.DataFrame(data, columns = ['rq','mean_diff','mean_diff%','median_diff','median_diff%','min_diff','min_diff%','max_diff','max_diff%','std_diff','std_diff%','sem_diff','sem_diff%','q1_diff','q1_diff%','q3_diff','q3_diff%'])
display(ut)
#print(ut.to_string())


# ## Descriptive Statistics (By Browser)

# In[28]:


data = []
for implementation in implementations:
    for browser in browsers:
        x = df[(df['implementation'] == implementation) & (df['browser'] == browser)]
        mean = numpy.round(numpy.mean(x['energy']), 2)
        median = numpy.round(numpy.median(x['energy']), 2)
        min = numpy.round(numpy.amin(x['energy']), 2)
        max = numpy.round(numpy.amax(x['energy']), 2)
        std = numpy.round(numpy.std(x['energy']), 2)
        sem = numpy.round(stats.sem(x['energy']), 2)
        q1 = numpy.round(numpy.quantile(x['energy'], 0.25), 2)
        q3 = numpy.round(numpy.quantile(x['energy'], 0.75), 2)

        data.append(
            [implementation, browser, mean, std, min, q1, median,  q3, max, sem]
        )
        
# Create the pandas DataFrame
stat = pd.DataFrame(data, columns = ['implementation', 'browser', 'mean', 'std', 'min', 'q1', 'median', 'q3', 'max', 'sem'])
# display(stat)
print(stat.to_string())

# Alternative of pandas: x['energy'].describe()


# ## Descriptive Statistics Difference (By Browser)

# In[29]:


data = []

for implementationpair in implementationpairs:
    for browser in browsers:
        implementation1 = stat[(stat['implementation'] == implementationpair[1]) & (stat['browser'] == browser)]
        implementation2 = stat[(stat['implementation'] == implementationpair[0]) & (stat['browser'] == browser)]

        mean_diff = implementation1.iloc[0]['mean']-implementation2.iloc[0]['mean']
        median_diff = implementation1.iloc[0]['median']-implementation2.iloc[0]['median']
        min_diff = implementation1.iloc[0]['min']-implementation2.iloc[0]['min']
        max_diff = implementation1.iloc[0]['max']-implementation2.iloc[0]['max']
        std_diff = implementation1.iloc[0]['std']-implementation2.iloc[0]['std']
        sem_diff = implementation1.iloc[0]['sem']-implementation2.iloc[0]['sem']
        q1_diff = implementation1.iloc[0]['q1']-implementation2.iloc[0]['q1']
        q3_diff = implementation1.iloc[0]['q3']-implementation2.iloc[0]['q3']

        data.append(
            [implementationpair[1] + ' vs. ' + implementationpair[0] + ' ' + browser,
             numpy.round(mean_diff, 2),
             numpy.round(mean_diff/implementation2.iloc[0]['mean']*100, 2),
             numpy.round(median_diff, 2),
             numpy.round(median_diff/implementation2.iloc[0]['median']*100, 2),
             numpy.round(min_diff, 2),
             numpy.round(min_diff/implementation2.iloc[0]['min']*100, 2),
             numpy.round(max_diff, 2),
             numpy.round(max_diff/implementation2.iloc[0]['max']*100, 2),
             numpy.round(std_diff, 2),
             numpy.round(std_diff/implementation2.iloc[0]['std']*100, 2),
             numpy.round(sem_diff, 2),
             numpy.round(sem_diff/implementation2.iloc[0]['sem']*100, 2),
             numpy.round(q1_diff, 2),
             numpy.round(q1_diff/implementation2.iloc[0]['q1']*100, 2),
             numpy.round(q3_diff, 2),
             numpy.round(q3_diff/implementation2.iloc[0]['q3']*100, 2),
            ]
        )
        
# Create the pandas DataFrame
ut = pd.DataFrame(data, columns = ['rq','mean_diff','mean_diff%','median_diff','median_diff%','min_diff','min_diff%','max_diff','max_diff%','std_diff','std_diff%','sem_diff','sem_diff%','q1_diff','q1_diff%','q3_diff','q3_diff%'])
display(ut)
#print(ut.to_string())


# ## Descriptive Statistics Difference (Cross Browser)

# In[30]:


data = []

for pairswitch in [[0,1],[1,0]]:
    for implementationpair in implementationpairs:
        for browserpair in browserpairs:
            implementation1 = stat[(stat['browser'] == browserpair[pairswitch[1]]) & (stat['implementation'] == implementationpair[1])]
            implementation2 = stat[(stat['browser'] == browserpair[pairswitch[0]]) & (stat['implementation'] == implementationpair[0])]

#for implementationpair in implementationpairs:
#    for browser in browsers:
#        implementation1 = stat[(stat['implementation'] == implementationpair[0]) & (stat['browser'] == browser)]
#        implementation2 = stat[(stat['implementation'] == implementationpair[1]) & (stat['browser'] == browser)]

        mean_diff = implementation1.iloc[0]['mean']-implementation2.iloc[0]['mean']
        median_diff = implementation1.iloc[0]['median']-implementation2.iloc[0]['median']
        min_diff = implementation1.iloc[0]['min']-implementation2.iloc[0]['min']
        max_diff = implementation1.iloc[0]['max']-implementation2.iloc[0]['max']
        std_diff = implementation1.iloc[0]['std']-implementation2.iloc[0]['std']
        sem_diff = implementation1.iloc[0]['sem']-implementation2.iloc[0]['sem']
        q1_diff = implementation1.iloc[0]['q1']-implementation2.iloc[0]['q1']
        q3_diff = implementation1.iloc[0]['q3']-implementation2.iloc[0]['q3']

        data.append(
            [
             browserpair[pairswitch[1]] + ' ' + implementationpair[1] + ' vs. ' + browserpair[pairswitch[0]] + ' ' + implementationpair[0],
             numpy.round(mean_diff, 2),
             numpy.round(mean_diff/implementation2.iloc[0]['mean']*100, 2),
             numpy.round(median_diff, 2),
             numpy.round(median_diff/implementation2.iloc[0]['median']*100, 2),
             numpy.round(min_diff, 2),
             numpy.round(min_diff/implementation2.iloc[0]['min']*100, 2),
             numpy.round(max_diff, 2),
             numpy.round(max_diff/implementation2.iloc[0]['max']*100, 2),
             numpy.round(std_diff, 2),
             numpy.round(std_diff/implementation2.iloc[0]['std']*100, 2),
             numpy.round(sem_diff, 2),
             numpy.round(sem_diff/implementation2.iloc[0]['sem']*100, 2),
             numpy.round(q1_diff, 2),
             numpy.round(q1_diff/implementation2.iloc[0]['q1']*100, 2),
             numpy.round(q3_diff, 2),
             numpy.round(q3_diff/implementation2.iloc[0]['q3']*100, 2),
            ]
        )
        
# Create the pandas DataFrame
ut = pd.DataFrame(data, columns = ['rq','mean_diff','mean_diff%','median_diff','median_diff%','min_diff','min_diff%','max_diff','max_diff%','std_diff','std_diff%','sem_diff','sem_diff%','q1_diff','q1_diff%','q3_diff','q3_diff%'])
display(ut)
#print(ut.to_string())


# ## Descriptive Statistics (By Browser & By Device)

# In[31]:


data = []
for device in devices:
    for implementation in implementations:
        for browser in browsers:
            x = df[(df['implementation'] == implementation) & (df['browser'] == browser) & (df['device'] == device)]
            mean = numpy.round(numpy.mean(x['energy']), 2)
            median = numpy.round(numpy.median(x['energy']), 2)
            min = numpy.round(numpy.amin(x['energy']), 2)
            max = numpy.round(numpy.amax(x['energy']), 2)
            std = numpy.round(numpy.std(x['energy']), 2)
            sem = numpy.round(stats.sem(x['energy']), 2)
            q1 = numpy.round(numpy.quantile(x['energy'], 0.25), 2)
            q3 = numpy.round(numpy.quantile(x['energy'], 0.75), 2)

            data.append(
                [implementation, device, browser, mean, std, min, q1, median, q3, max, sem]
            )
        
# Create the pandas DataFrame
stat = pd.DataFrame(data, columns = ['implementation', 'device', 'browser', 'mean', 'std', 'min', 'q1', 'median', 'q3', 'max', 'sem'])
# display(stat)
print(stat.to_string())

# Alternative of pandas: x['energy'].describe()


# ## Descriptive Statistics Difference (By Browser & By Device)

# In[32]:


data = []

for implementationpair in implementationpairs:
    for device in devices:
        for browser in browsers:
            implementation1 = stat[(stat['implementation'] == implementationpair[1]) & (stat['browser'] == browser) & (stat['device'] == device)]
            implementation2 = stat[(stat['implementation'] == implementationpair[0]) & (stat['browser'] == browser) & (stat['device'] == device)]

            mean_diff = implementation1.iloc[0]['mean']-implementation2.iloc[0]['mean']
            median_diff = implementation1.iloc[0]['median']-implementation2.iloc[0]['median']
            min_diff = implementation1.iloc[0]['min']-implementation2.iloc[0]['min']
            max_diff = implementation1.iloc[0]['max']-implementation2.iloc[0]['max']
            std_diff = implementation1.iloc[0]['std']-implementation2.iloc[0]['std']
            sem_diff = implementation1.iloc[0]['sem']-implementation2.iloc[0]['sem']
            q1_diff = implementation1.iloc[0]['q1']-implementation2.iloc[0]['q1']
            q3_diff = implementation1.iloc[0]['q3']-implementation2.iloc[0]['q3']

            data.append(
                [implementationpair[1] + ' vs. ' + implementationpair[0] + ' ' + browser,
                 device,
                 numpy.round(mean_diff, 2),
                 numpy.round(mean_diff/implementation2.iloc[0]['mean']*100, 2),
                 numpy.round(median_diff, 2),
                 numpy.round(median_diff/implementation2.iloc[0]['median']*100, 2),
                 numpy.round(min_diff, 2),
                 numpy.round(min_diff/implementation2.iloc[0]['min']*100, 2),
                 numpy.round(max_diff, 2),
                 numpy.round(max_diff/implementation2.iloc[0]['max']*100, 2),
                 numpy.round(std_diff, 2),
                 numpy.round(std_diff/implementation2.iloc[0]['std']*100, 2),
                 numpy.round(sem_diff, 2),
                 numpy.round(sem_diff/implementation2.iloc[0]['sem']*100, 2),
                 numpy.round(q1_diff, 2),
                 numpy.round(q1_diff/implementation2.iloc[0]['q1']*100, 2),
                 numpy.round(q3_diff, 2),
                 numpy.round(q3_diff/implementation2.iloc[0]['q3']*100, 2),
                ]
            )
        
# Create the pandas DataFrame
ut = pd.DataFrame(data, columns = ['rq','device','mean_diff','mean_diff%','median_diff','median_diff%','min_diff','min_diff%','max_diff','max_diff%','std_diff','std_diff%','sem_diff','sem_diff%','q1_diff','q1_diff%','q3_diff','q3_diff%'])
display(ut)
#print(ut.to_string())


# ## Descriptive Statistics Difference (Cross Browser & By Device)

# In[33]:


data = []

for pairswitch in [[0,1],[1,0]]:
    for device in devices:
        for implementationpair in implementationpairs:
            for browserpair in browserpairs:
                implementation1 = stat[(stat['browser'] == browserpair[pairswitch[1]]) & (stat['implementation'] == implementationpair[1]) & (stat['device'] == device)]
                implementation2 = stat[(stat['browser'] == browserpair[pairswitch[0]]) & (stat['implementation'] == implementationpair[0]) & (stat['device'] == device)]

    #for implementationpair in implementationpairs:
    #    for browser in browsers:
    #        implementation1 = stat[(stat['implementation'] == implementationpair[0]) & (stat['browser'] == browser)]
    #        implementation2 = stat[(stat['implementation'] == implementationpair[1]) & (stat['browser'] == browser)]

            mean_diff = implementation1.iloc[0]['mean']-implementation2.iloc[0]['mean']
            median_diff = implementation1.iloc[0]['median']-implementation2.iloc[0]['median']
            min_diff = implementation1.iloc[0]['min']-implementation2.iloc[0]['min']
            max_diff = implementation1.iloc[0]['max']-implementation2.iloc[0]['max']
            std_diff = implementation1.iloc[0]['std']-implementation2.iloc[0]['std']
            sem_diff = implementation1.iloc[0]['sem']-implementation2.iloc[0]['sem']
            q1_diff = implementation1.iloc[0]['q1']-implementation2.iloc[0]['q1']
            q3_diff = implementation1.iloc[0]['q3']-implementation2.iloc[0]['q3']

            data.append(
                [
                 browserpair[pairswitch[1]] + ' ' + implementationpair[1] + ' vs. ' + browserpair[pairswitch[0]] + ' ' + implementationpair[0],
                 device,
                 numpy.round(mean_diff, 2),
                 numpy.round(mean_diff/implementation2.iloc[0]['mean']*100, 2),
                 numpy.round(median_diff, 2),
                 numpy.round(median_diff/implementation2.iloc[0]['median']*100, 2),
                 numpy.round(min_diff, 2),
                 numpy.round(min_diff/implementation2.iloc[0]['min']*100, 2),
                 numpy.round(max_diff, 2),
                 numpy.round(max_diff/implementation2.iloc[0]['max']*100, 2),
                 numpy.round(std_diff, 2),
                 numpy.round(std_diff/implementation2.iloc[0]['std']*100, 2),
                 numpy.round(sem_diff, 2),
                 numpy.round(sem_diff/implementation2.iloc[0]['sem']*100, 2),
                 numpy.round(q1_diff, 2),
                 numpy.round(q1_diff/implementation2.iloc[0]['q1']*100, 2),
                 numpy.round(q3_diff, 2),
                 numpy.round(q3_diff/implementation2.iloc[0]['q3']*100, 2),
                ]
            )
        
# Create the pandas DataFrame
ut = pd.DataFrame(data, columns = ['rq','device','mean_diff','mean_diff%','median_diff','median_diff%','min_diff','min_diff%','max_diff','max_diff%','std_diff','std_diff%','sem_diff','sem_diff%','q1_diff','q1_diff%','q3_diff','q3_diff%'])
display(ut)
#print(ut.to_string())


# # RQ2: JS Energy Browser <a name="rq2js"></a>

# ## Shapiro Wilk Test

# In[34]:


data = []
non_normal = 0

for browser in browsers:
    energy = df[(df['browser'] == browser) & (df['implementation'] == 'js')]['energy']

    if len(energy) >= 3:
        shapiro_test = stats.shapiro(energy)

        non_normal += (1 if shapiro_test.pvalue <= 0.05 else 0)

        data.append(
            [browser, 'js',
             shapiro_test.statistic,
             shapiro_test.pvalue
            ]
        )
        
# Create the pandas DataFrame
swt = pd.DataFrame(data, columns = ['browser', 'implementation', 'w', 'p'])
#print(swt.to_string())
display(swt)

print("\n{} non-normally distributed samples".format(non_normal))
print("{} normally distributed samples".format(len(swt) - non_normal))
print("{:.2f}% non-normally distributed samples".format(non_normal/len(swt)*100)) 


# ## Shapiro Wilk Test (By Device)

# In[35]:


data = []
non_normal = 0

for device in devices:
    for browser in browsers:
        energy = df[(df['browser'] == browser) & (df['implementation'] == 'js') & (df['device'] == device)]['energy']

        if len(energy) >= 3:
            shapiro_test = stats.shapiro(energy)

            non_normal += (1 if shapiro_test.pvalue <= 0.05 else 0)

            data.append(
                [
                 device,
                 browser, 'js',
                 shapiro_test.statistic,
                 shapiro_test.pvalue
                ]
            )
        
# Create the pandas DataFrame
swt = pd.DataFrame(data, columns = ['device', 'browser', 'implementation', 'w', 'p'])
#print(swt.to_string())
display(swt)

print("\n{} non-normally distributed samples".format(non_normal))
print("{} normally distributed samples".format(len(swt) - non_normal))
print("{:.2f}% non-normally distributed samples".format(non_normal/len(swt)*100)) 


# ## Mann Whitney U Test

# In[36]:


data = []

for browserpair in browserpairs:
    browser1_energy = df[(df['browser'] == browserpair[0]) & (df['implementation'] == 'js')]['energy']
    browser2_energy = df[(df['browser'] == browserpair[1]) & (df['implementation'] == 'js')]['energy']
    eff = cliff.cliffs_delta(browser1_energy, browser2_energy)

    u = stats.mannwhitneyu(browser1_energy, browser2_energy, alternative='two-sided')            

    data.append(
        [
         browserpair[0] + ' vs. ' + browserpair[1],
         u.statistic,
         u.pvalue,
         eff[0],
         eff[1]
        ]
    )
        
# Create the pandas DataFrame
ut = pd.DataFrame(data, columns = ['rq', 'u', 'p', 'eff', 'interp'])
display(ut)

interp = ut['interp'].value_counts()
interp = pd.DataFrame(interp, columns = ['interp', 'percent'])
interp['percent'] = (interp['interp'] / interp['interp'].sum()) * 100

display(interp)


# ## Mann Whitney U Test (By Device)

# In[37]:


data = []

for device in devices:
    for browserpair in browserpairs:
        browser1_energy = df[(df['browser'] == browserpair[0]) & (df['implementation'] == 'js') & (df['device'] == device)]['energy']
        browser2_energy = df[(df['browser'] == browserpair[1]) & (df['implementation'] == 'js') & (df['device'] == device)]['energy']
        eff = cliff.cliffs_delta(browser1_energy, browser2_energy)

        u = stats.mannwhitneyu(browser1_energy, browser2_energy, alternative='two-sided')            

        data.append(
            [
             device,
             browserpair[0] + ' vs. ' + browserpair[1],
             u.statistic,
             u.pvalue,
             eff[0],
             eff[1]
            ]
        )
        
# Create the pandas DataFrame
ut = pd.DataFrame(data, columns = ['device', 'rq', 'u', 'p', 'eff', 'interp'])
display(ut)

interp = ut['interp'].value_counts()
interp = pd.DataFrame(interp, columns = ['interp', 'percent'])
interp['percent'] = (interp['interp'] / interp['interp'].sum()) * 100

display(interp)


# ## Q-Q-Plot

# In[38]:


for browser in browsers:
    data = df[(df['implementation'] == 'js') & (df['browser'] == browser)]
    qq = sm.qqplot(data.energy, line='s')
    h = plt.title('JS - ' + browser)


# ## Q-Q-Plot (By Device)

# In[39]:


for device in devices:
    for browser in browsers:
        data = df[(df['implementation'] == 'js') & (df['browser'] == browser) & (df['device'] == device)]
        qq = sm.qqplot(data.energy, line='s')
        h = plt.title('JS - ' + browser + ' - ' + device)


# ## Histogram

# In[40]:


data = df[(df['implementation'] == 'js')]
sns.histplot(data=data, x="energy", hue="browser", hue_order=browsers).set_title("JS Energy Consumption by Browsers")
plt.xlabel("Energy (Joules)")
plt.ylim(0, 200)
plt.xlim(0, 35)


# ## Histogramm (By Device)

# In[41]:


data = []
for device in devices:
    data = df[(df['implementation'] == 'js') & (df['device'] == device)]
    sns.histplot(data=data, x="energy", hue="browser", hue_order=browsers).set_title("JS Energy Consumption by Browsers" + " - " + device)
    plt.xlabel("Energy (Joules)")
    plt.ylim(0, 200)
    plt.xlim(0, 35)
    plt.show()


# ## Descriptive Statistics

# In[42]:


data = []
for browser in browsers:
    x = df[(df['browser'] == browser) & (df['implementation'] == 'js')]
    mean = numpy.round(numpy.mean(x['energy']), 2)
    median = numpy.round(numpy.median(x['energy']), 2)
    min = numpy.round(numpy.amin(x['energy']), 2)
    max = numpy.round(numpy.amax(x['energy']), 2)
    std = numpy.round(numpy.std(x['energy']), 2)
    sem = numpy.round(stats.sem(x['energy']), 2)
    q1 = numpy.round(numpy.quantile(x['energy'], 0.25), 2)
    q3 = numpy.round(numpy.quantile(x['energy'], 0.75), 2)
    
    data.append(
        [browser, mean, std, min, q1, median, q3, max, sem]
    )
        
# Create the pandas DataFrame
stat = pd.DataFrame(data, columns = ['browser', 'mean', 'std', 'min', 'q1', 'median', 'q3', 'max', 'sem'])
display(stat)
#print(stat.to_string())

# Alternative of pandas: x['energy'].describe()


# ## Descriptive Statistics Difference

# In[43]:


data = []

for browserpair in browserpairs:
    browser1 = stat[(stat['browser'] == browserpair[0])]
    browser2 = stat[(stat['browser'] == browserpair[1])]
    
    mean_diff = browser1.iloc[0]['mean']-browser2.iloc[0]['mean']
    median_diff = browser1.iloc[0]['median']-browser2.iloc[0]['median']
    min_diff = browser1.iloc[0]['min']-browser2.iloc[0]['min']
    max_diff = browser1.iloc[0]['max']-browser2.iloc[0]['max']
    std_diff = browser1.iloc[0]['std']-browser2.iloc[0]['std']
    sem_diff = browser1.iloc[0]['sem']-browser2.iloc[0]['sem']
    q1_diff = browser1.iloc[0]['q1']-browser2.iloc[0]['q1']
    q3_diff = browser1.iloc[0]['q3']-browser2.iloc[0]['q3']

    data.append(
        [browserpair[0] + ' vs. ' + browserpair[1],
         numpy.round(mean_diff, 2),
         numpy.round(mean_diff/browser2.iloc[0]['mean']*100, 2),
         numpy.round(median_diff, 2),
         numpy.round(median_diff/browser2.iloc[0]['median']*100, 2),
         numpy.round(min_diff, 2),
         numpy.round(min_diff/browser2.iloc[0]['min']*100, 2),
         numpy.round(max_diff, 2),
         numpy.round(max_diff/browser2.iloc[0]['max']*100, 2),
         numpy.round(std_diff, 2),
         numpy.round(std_diff/browser2.iloc[0]['std']*100, 2),
         numpy.round(sem_diff, 2),
         numpy.round(sem_diff/browser2.iloc[0]['sem']*100, 2),
         numpy.round(q1_diff, 2),
         numpy.round(q1_diff/browser2.iloc[0]['q1']*100, 2),
         numpy.round(q3_diff, 2),
         numpy.round(q3_diff/browser2.iloc[0]['q3']*100, 2),
        ]
    )
        
# Create the pandas DataFrame
ut = pd.DataFrame(data, columns = ['rq','mean_diff','mean_diff%','median_diff','median_diff%','min_diff','min_diff%','max_diff','max_diff%','std_diff','std_diff%','sem_diff','sem_diff%','q1_diff','q1_diff%','q3_diff','q3_diff%'])
display(ut)
#print(ut.to_string())


# ## Descriptive Statistics (By Device)

# In[44]:


data = []
for device in devices:
    for browser in browsers:
        x = df[(df['browser'] == browser) & (df['implementation'] == 'js') & (df['device'] == device)]
        mean = numpy.round(numpy.mean(x['energy']), 2)
        median = numpy.round(numpy.median(x['energy']), 2)
        min = numpy.round(numpy.amin(x['energy']), 2)
        max = numpy.round(numpy.amax(x['energy']), 2)
        std = numpy.round(numpy.std(x['energy']), 2)
        sem = numpy.round(stats.sem(x['energy']), 2)
        q1 = numpy.round(numpy.quantile(x['energy'], 0.25), 2)
        q3 = numpy.round(numpy.quantile(x['energy'], 0.75), 2)

        data.append(
            [device, browser, mean, std, min, q1, median, q3, max, sem]
        )
        
# Create the pandas DataFrame
stat = pd.DataFrame(data, columns = ['device', 'browser', 'mean', 'std', 'min', 'q1', 'median', 'q3', 'max', 'sem'])
display(stat)
#print(stat.to_string())

# Alternative of pandas: x['energy'].describe()


# ## Descriptive Statistics Difference (By Device)

# In[45]:


data = []

for device in devices:
    for browserpair in browserpairs:
        browser1 = stat[(stat['browser'] == browserpair[0]) & (stat['device'] == device)]
        browser2 = stat[(stat['browser'] == browserpair[1]) & (stat['device'] == device)]

        mean_diff = browser1.iloc[0]['mean']-browser2.iloc[0]['mean']
        median_diff = browser1.iloc[0]['median']-browser2.iloc[0]['median']
        min_diff = browser1.iloc[0]['min']-browser2.iloc[0]['min']
        max_diff = browser1.iloc[0]['max']-browser2.iloc[0]['max']
        std_diff = browser1.iloc[0]['std']-browser2.iloc[0]['std']
        sem_diff = browser1.iloc[0]['sem']-browser2.iloc[0]['sem']
        q1_diff = browser1.iloc[0]['q1']-browser2.iloc[0]['q1']
        q3_diff = browser1.iloc[0]['q3']-browser2.iloc[0]['q3']

        data.append(
            [
             device,
             browserpair[0] + ' vs. ' + browserpair[1],
             numpy.round(mean_diff, 2),
             numpy.round(mean_diff/browser2.iloc[0]['mean']*100, 2),
             numpy.round(median_diff, 2),
             numpy.round(median_diff/browser2.iloc[0]['median']*100, 2),
             numpy.round(min_diff, 2),
             numpy.round(min_diff/browser2.iloc[0]['min']*100, 2),
             numpy.round(max_diff, 2),
             numpy.round(max_diff/browser2.iloc[0]['max']*100, 2),
             numpy.round(std_diff, 2),
             numpy.round(std_diff/browser2.iloc[0]['std']*100, 2),
             numpy.round(sem_diff, 2),
             numpy.round(sem_diff/browser2.iloc[0]['sem']*100, 2),
             numpy.round(q1_diff, 2),
             numpy.round(q1_diff/browser2.iloc[0]['q1']*100, 2),
             numpy.round(q3_diff, 2),
             numpy.round(q3_diff/browser2.iloc[0]['q3']*100, 2),
            ]
        )
        
# Create the pandas DataFrame
ut = pd.DataFrame(data, columns = ['device', 'rq','mean_diff','mean_diff%','median_diff','median_diff%','min_diff','min_diff%','max_diff','max_diff%','std_diff','std_diff%','sem_diff','sem_diff%','q1_diff','q1_diff%','q3_diff','q3_diff%'])
display(ut)
#print(ut.to_string())


# # RQ2: WASM Energy Browser <a name="rq3wasm"></a>

# ## Shapiro Wilk Test

# In[46]:


data = []
non_normal = 0

for browser in browsers:
    energy = df[(df['browser'] == browser) & (df['implementation'] == 'wasm')]['energy']

    if len(energy) >= 3:
        shapiro_test = stats.shapiro(energy)

        non_normal += (1 if shapiro_test.pvalue <= 0.05 else 0)

        data.append(
            [browser, 'wasm',
             shapiro_test.statistic,
             shapiro_test.pvalue
            ]
        )
        
# Create the pandas DataFrame
swt = pd.DataFrame(data, columns = ['browser', 'implementation', 'w', 'p'])
#print(swt.to_string())
display(swt)

print("\n{} non-normally distributed samples".format(non_normal))
print("{} normally distributed samples".format(len(swt) - non_normal))
print("{:.2f}% non-normally distributed samples".format(non_normal/len(swt)*100)) 


# ## Shapiro Wilk Test (By Device)

# In[47]:


data = []
non_normal = 0

for device in devices:
    for browser in browsers:
        energy = df[(df['browser'] == browser) & (df['implementation'] == 'wasm') & (df['device'] == device)]['energy']

        if len(energy) >= 3:
            shapiro_test = stats.shapiro(energy)

            non_normal += (1 if shapiro_test.pvalue <= 0.05 else 0)

            data.append(
                [
                 device,
                 browser, 'wasm',
                 shapiro_test.statistic,
                 shapiro_test.pvalue
                ]
            )
        
# Create the pandas DataFrame
swt = pd.DataFrame(data, columns = ['device', 'browser', 'implementation', 'w', 'p'])
#print(swt.to_string())
display(swt)

print("\n{} non-normally distributed samples".format(non_normal))
print("{} normally distributed samples".format(len(swt) - non_normal))
print("{:.2f}% non-normally distributed samples".format(non_normal/len(swt)*100)) 


# ## Mann Whitney U Test

# In[48]:


data = []

for browserpair in browserpairs:
    browser1_energy = df[(df['browser'] == browserpair[0]) & (df['implementation'] == 'wasm')]['energy']
    browser2_energy = df[(df['browser'] == browserpair[1]) & (df['implementation'] == 'wasm')]['energy']
    eff = cliff.cliffs_delta(browser1_energy, browser2_energy)

    u = stats.mannwhitneyu(browser1_energy, browser2_energy, alternative='two-sided')            

    data.append(
        [browserpair[0] + ' vs. ' + browserpair[1],
         u.statistic,
         u.pvalue,
         eff[0],
         eff[1]
        ]
    )
        
# Create the pandas DataFrame
ut = pd.DataFrame(data, columns = ['rq','u', 'p', 'eff', 'interp'])
display(ut)

interp = ut['interp'].value_counts()
interp = pd.DataFrame(interp, columns = ['interp', 'percent'])
interp['percent'] = (interp['interp'] / interp['interp'].sum()) * 100

display(interp)


# ## Mann Whitney U Test (By Device)

# In[49]:


data = []

for device in devices:
    for browserpair in browserpairs:
        browser1_energy = df[(df['browser'] == browserpair[0]) & (df['implementation'] == 'wasm') & (df['device'] == device)]['energy']
        browser2_energy = df[(df['browser'] == browserpair[1]) & (df['implementation'] == 'wasm') & (df['device'] == device)]['energy']
        eff = cliff.cliffs_delta(browser1_energy, browser2_energy)

        u = stats.mannwhitneyu(browser1_energy, browser2_energy, alternative='two-sided')            

        data.append(
            [
             device,
             browserpair[0] + ' vs. ' + browserpair[1],
             u.statistic,
             u.pvalue,
             eff[0],
             eff[1]
            ]
        )
        
# Create the pandas DataFrame
ut = pd.DataFrame(data, columns = ['device', 'rq','u', 'p', 'eff', 'interp'])
display(ut)

interp = ut['interp'].value_counts()
interp = pd.DataFrame(interp, columns = ['interp', 'percent'])
interp['percent'] = (interp['interp'] / interp['interp'].sum()) * 100

display(interp)


# ## Q-Q-Plot

# In[50]:


for browser in browsers:
    data = df[(df['implementation'] == 'wasm') & (df['browser'] == browser)]
    qq = sm.qqplot(data.energy, line='s')
    h = plt.title('Wasm - ' + browser)


# ## Q-Q-Plot (By Device)

# In[51]:


for device in devices:
    for browser in browsers:
        data = df[(df['implementation'] == 'wasm') & (df['browser'] == browser) & (df['device'] == device)]
        qq = sm.qqplot(data.energy, line='s')
        h = plt.title('Wasm - ' + browser + ' - ' + device)


# ## Histogram

# In[52]:


data = df[(df['implementation'] == 'wasm')]
sns.histplot(data=data, x="energy", hue="browser", hue_order=browsers).set_title("Wasm Energy Consumption by Browsers")
plt.xlabel("Energy (Joules)")
plt.ylim(0, 200)
plt.xlim(0, 30)


# ## Histogram (By Device)

# In[53]:


data = []
for device in devices:
    data = df[(df['implementation'] == 'wasm') & (df['device'] == device)]
    sns.histplot(data=data, x="energy", hue="browser", hue_order=browsers).set_title("Wasm Energy Consumption by Browsers")
    plt.xlabel("Energy (Joules)")
    plt.ylim(0, 175)
    plt.xlim(0, 30)
    plt.show()


# ## Descriptive Statistics

# In[54]:


data = []
for browser in browsers:
    x = df[(df['browser'] == browser) & (df['implementation'] == 'wasm')]
    mean = numpy.round(numpy.mean(x['energy']), 2)
    median = numpy.round(numpy.median(x['energy']), 2)
    min = numpy.round(numpy.amin(x['energy']), 2)
    max = numpy.round(numpy.amax(x['energy']), 2)
    std = numpy.round(numpy.std(x['energy']), 2)
    sem = numpy.round(stats.sem(x['energy']), 2)
    q1 = numpy.round(numpy.quantile(x['energy'], 0.25), 2)
    q3 = numpy.round(numpy.quantile(x['energy'], 0.75), 2)
    
    data.append(
        [browser, mean, std, min, q1, median, q3, max, sem]
    )
        
# Create the pandas DataFrame
stat = pd.DataFrame(data, columns = ['browser', 'mean', 'std', 'min', 'q1', 'median', 'q3', 'max', 'sem'])
# display(stat)
print(stat.to_string())

# Alternative of pandas: x['energy'].describe()


# ## Descriptive Statistics Difference

# In[55]:


data = []

for browserpair in browserpairs:
    browser1 = stat[(stat['browser'] == browserpair[0])]
    browser2 = stat[(stat['browser'] == browserpair[1])]
    
    mean_diff = browser1.iloc[0]['mean']-browser2.iloc[0]['mean']
    median_diff = browser1.iloc[0]['median']-browser2.iloc[0]['median']
    min_diff = browser1.iloc[0]['min']-browser2.iloc[0]['min']
    max_diff = browser1.iloc[0]['max']-browser2.iloc[0]['max']
    std_diff = browser1.iloc[0]['std']-browser2.iloc[0]['std']
    sem_diff = browser1.iloc[0]['sem']-browser2.iloc[0]['sem']
    q1_diff = browser1.iloc[0]['q1']-browser2.iloc[0]['q1']
    q3_diff = browser1.iloc[0]['q3']-browser2.iloc[0]['q3']

    data.append(
        [browserpair[0] + ' vs. ' + browserpair[1],
         numpy.round(mean_diff, 2),
         numpy.round(mean_diff/browser2.iloc[0]['mean']*100, 2),
         numpy.round(median_diff, 2),
         numpy.round(median_diff/browser2.iloc[0]['median']*100, 2),
         numpy.round(min_diff, 2),
         numpy.round(min_diff/browser2.iloc[0]['min']*100, 2),
         numpy.round(max_diff, 2),
         numpy.round(max_diff/browser2.iloc[0]['max']*100, 2),
         numpy.round(std_diff, 2),
         numpy.round(std_diff/browser2.iloc[0]['std']*100, 2),
         numpy.round(sem_diff, 2),
         numpy.round(sem_diff/browser2.iloc[0]['sem']*100, 2),
         numpy.round(q1_diff, 2),
         numpy.round(q1_diff/browser2.iloc[0]['q1']*100, 2),
         numpy.round(q3_diff, 2),
         numpy.round(q3_diff/browser2.iloc[0]['q3']*100, 2),
        ]
    )
        
# Create the pandas DataFrame
ut = pd.DataFrame(data, columns = ['rq','mean_diff','mean_diff%','median_diff','median_diff%','min_diff','min_diff%','max_diff','max_diff%','std_diff','std_diff%','sem_diff','sem_diff%','q1_diff','q1_diff%','q3_diff','q3_diff%'])
display(ut)
#print(ut.to_string())


# ## Descriptive Statistics (By Device)

# In[56]:


data = []

for device in devices:
    for browser in browsers:
        x = df[(df['browser'] == browser) & (df['implementation'] == 'wasm') & (df['device'] == device)]
        mean = numpy.round(numpy.mean(x['energy']), 2)
        median = numpy.round(numpy.median(x['energy']), 2)
        min = numpy.round(numpy.amin(x['energy']), 2)
        max = numpy.round(numpy.amax(x['energy']), 2)
        std = numpy.round(numpy.std(x['energy']), 2)
        sem = numpy.round(stats.sem(x['energy']), 2)
        q1 = numpy.round(numpy.quantile(x['energy'], 0.25), 2)
        q3 = numpy.round(numpy.quantile(x['energy'], 0.75), 2)

        data.append(
            [device, browser, mean, std, min, q1, median, q3, max, sem]
        )
        
# Create the pandas DataFrame
stat = pd.DataFrame(data, columns = ['device', 'browser', 'mean', 'std', 'min', 'q1', 'median', 'q3', 'max', 'sem'])
# display(stat)
print(stat.to_string())

# Alternative of pandas: x['energy'].describe()


# ## Descriptive Statistics Difference (By Device)

# In[57]:


data = []

for device in devices:
    for browserpair in browserpairs:
        browser1 = stat[(stat['browser'] == browserpair[0]) & (stat['device'] == device)]
        browser2 = stat[(stat['browser'] == browserpair[1]) & (stat['device'] == device)]

        mean_diff = browser1.iloc[0]['mean']-browser2.iloc[0]['mean']
        median_diff = browser1.iloc[0]['median']-browser2.iloc[0]['median']
        min_diff = browser1.iloc[0]['min']-browser2.iloc[0]['min']
        max_diff = browser1.iloc[0]['max']-browser2.iloc[0]['max']
        std_diff = browser1.iloc[0]['std']-browser2.iloc[0]['std']
        sem_diff = browser1.iloc[0]['sem']-browser2.iloc[0]['sem']
        q1_diff = browser1.iloc[0]['q1']-browser2.iloc[0]['q1']
        q3_diff = browser1.iloc[0]['q3']-browser2.iloc[0]['q3']

        data.append(
            [
             device,
             browserpair[0] + ' vs. ' + browserpair[1],
             numpy.round(mean_diff, 2),
             numpy.round(mean_diff/browser2.iloc[0]['mean']*100, 2),
             numpy.round(median_diff, 2),
             numpy.round(median_diff/browser2.iloc[0]['median']*100, 2),
             numpy.round(min_diff, 2),
             numpy.round(min_diff/browser2.iloc[0]['min']*100, 2),
             numpy.round(max_diff, 2),
             numpy.round(max_diff/browser2.iloc[0]['max']*100, 2),
             numpy.round(std_diff, 2),
             numpy.round(std_diff/browser2.iloc[0]['std']*100, 2),
             numpy.round(sem_diff, 2),
             numpy.round(sem_diff/browser2.iloc[0]['sem']*100, 2),
             numpy.round(q1_diff, 2),
             numpy.round(q1_diff/browser2.iloc[0]['q1']*100, 2),
             numpy.round(q3_diff, 2),
             numpy.round(q3_diff/browser2.iloc[0]['q3']*100, 2),
            ]
        )
        
# Create the pandas DataFrame
ut = pd.DataFrame(data, columns = ['device', 'rq','mean_diff','mean_diff%','median_diff','median_diff%','min_diff','min_diff%','max_diff','max_diff%','std_diff','std_diff%','sem_diff','sem_diff%','q1_diff','q1_diff%','q3_diff','q3_diff%'])
display(ut)
#print(ut.to_string())


# In[ ]:




